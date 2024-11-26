import os.path
import re
from collections.abc import Iterable
from contextlib import suppress
from itertools import chain
from textwrap import dedent
from typing import Any, ClassVar, Optional, Protocol, TextIO

from ast_grep_py import SgNode, SgRoot
from pydantic import BaseModel

from upcast.django_model import models
from upcast.utils import AnalysisModuleImport, Evalidate, FunctionArgs


class Plugin(Protocol):
    def should_run(self, context: models.Context, node: SgNode) -> bool: ...

    def run(self, context: models.Context, node: SgNode): ...

    def finish(self, context: models.Context) -> bool: ...


class Runner(BaseModel):
    context: models.Context

    class Config:
        arbitrary_types_allowed = True

    @property
    def plugins(self) -> list[Plugin]:
        return [
            ModuleImportPlugin(),
            ModelDefinitionPlugin(),
            # ClassPathFixPlugin(),
            ExportModelPlugin(),
            ModelReferencePlugin(),
        ]

    def run(self, files: Iterable[TextIO]):
        plugins = self.plugins

        for f in files:
            self.context.switch_to_file(f.name)
            code = f.read()
            root = SgRoot(code, "python")
            root_node = root.root()

            for plugin in plugins:
                if plugin.should_run(self.context, root_node):
                    plugin.run(self.context, root_node)

        self.context.reset()
        while plugins:
            plugin = plugins.pop(0)
            if not plugin.finish(self.context):
                plugins.append(plugin)


class FileBasePlugin(Plugin):
    def finish(self, context: models.Context) -> bool:
        return True


class ModuleImportPlugin(FileBasePlugin):
    """查找模块导入"""

    def should_run(self, context: models.Context, node: SgNode) -> bool:
        return True

    def run(self, context: models.Context, node: SgNode):
        analysis = AnalysisModuleImport(node=node, module=context.module)
        for module, name, alias in analysis.iter_import(node):
            context.add_imported_module(
                models.ImportedModule(
                    module=module,
                    name=name,
                    alias=alias,
                ),
                export=context.current_file.endswith(os.path.join("models", "__init__.py")),
            )


class ModelDefinitionPlugin(FileBasePlugin):
    """查找模型定义"""

    field_name_regex: ClassVar[re.Pattern] = re.compile(r"^\w[\w_]+$")
    field_type_regex: ClassVar[re.Pattern] = re.compile(r"^.*Field.*$")
    field_available_kwargs: ClassVar[set[str]] = {
        "primary_key",
        "db_index",
        "unique",
        "null",
        "blank",
        "help_text",
        "verbose_name",
        "max_length",
        "auto_created",
        "on_delete",
        "related_name",
        "types",
        "editable",
        "db_column",
        "db_comment",
        "db_tablespace",
        "db_default",
    }

    def should_run(self, context: models.Context, node: SgNode) -> bool:
        return "models" in context.current_file

    def iter_base_classes(self, context: models.Context, node: SgNode, model: models.Model):
        for i in node.get_multiple_matches("BASE"):
            kind = i.kind()
            if kind in ["attribute", "identifier"]:
                cls = i.text()
                class_path = context.get_module_path(cls)
                _, name = context.split_module_path(class_path)

                yield models.ModelBase(node=i, name=name, class_path=class_path)

    def is_look_like_django_field(self, attr: str, cls: str, kwargs: dict[str, Any]) -> bool:
        if not self.field_name_regex.match(attr):
            return False

        if not self.field_type_regex.match(cls):
            return False

        if kwargs.keys() & self.field_available_kwargs:
            return True

        return not kwargs

    def iter_fields(self, context: models.Context, node: SgNode, model: models.Model):
        class_indent = node.range().start.column

        for i in node.find_all(pattern="$ATTR = $CLS($$$ARGS)"):
            if i.range().start.column <= class_indent:
                continue

            attr = i["ATTR"].text()
            cls = i["CLS"].text()
            args = FunctionArgs().parse_args(i, "ARGS")

            if not self.is_look_like_django_field(attr, cls, args):
                continue

            safe_kwargs = {}
            for k in self.field_available_kwargs:
                v = args.get(k)
                if not v:
                    continue

                with suppress(Exception):
                    safe_kwargs[k] = v.value()

            class_path = context.get_module_path(cls)
            _, type_ = context.split_module_path(class_path)
            yield models.ModelField(
                node=i,
                name=attr,
                type=type_,
                class_path=class_path,
                kwargs=safe_kwargs,
            )

    def iter_indexes_from_model(self, context: models.Context, node: SgNode, model: models.Model):
        for f in model.fields:
            kwargs = f.kwargs
            if kwargs.get("primary_key") == "True" or f.name == "id":
                yield models.ModelIndex(
                    node=f.node,
                    fields=[f.name],
                    kind="primary_key",
                )

            if kwargs.get("db_index") == "True":
                yield models.ModelIndex(
                    node=f.node,
                    fields=[f.name],
                    kind="index",
                )

            if kwargs.get("unique") == "True":
                yield models.ModelIndex(
                    node=f.node,
                    fields=[f.name],
                    kind="unique",
                )

    def get_model_meta(self, context: models.Context, node: SgNode) -> Optional[models.ModelMeta]:
        meta = node.find(
            pattern=dedent(
                """
                class Meta:
                    $$$DEFINITION
                """
            )
        )
        if not meta:
            return None

        model_meta = models.ModelMeta(node=meta)
        evalidate = Evalidate()

        for i in meta.find_all(pattern="$KEY = $VALUE"):
            key = i["KEY"].text()

            if key not in model_meta.model_fields:
                continue

            with suppress(Exception):
                value = evalidate.eval(i["VALUE"].text())
                setattr(model_meta, key, value)

        return model_meta

    def iter_indexes_from_meta(self, context: models.Context, node: SgNode, model: models.Model):
        if not model.meta:
            return

        meta_cls = model.meta.node

        unique_together = meta_cls.find(pattern="unique_together = ($$$ARGS)")
        if unique_together:
            for i in unique_together.get_multiple_matches("ARGS"):
                yield models.ModelIndex(
                    node=i,
                    fields=[j.text() for j in i.get_multiple_matches("$$$ARGS") if j.kind() == "string"],
                    kind="unique",
                )

        indexes = meta_cls.find(pattern="indexes = [$$$INDEX]")
        if indexes:
            for i in indexes.get_multiple_matches("INDEX"):
                item = i.find(pattern="$F($$$ARGS)")
                if not item:
                    continue

                args = FunctionArgs().parse_args(item, "ARGS")
                fields = args["fields"].value()
                if not fields:
                    continue

                yield models.ModelIndex(
                    node=i,
                    fields=args["fields"].value(),
                    kind="unique" if args.get("unique") == "True" else "index",
                )

    def iter_indexes(self, context: models.Context, node: SgNode, model: models.Model):
        yield from self.iter_indexes_from_model(context, node, model)
        yield from self.iter_indexes_from_meta(context, node, model)

    def is_look_like_django_model(self, model: models.Model) -> bool:
        if not model.fields:
            return False

        if not model.bases:
            return False

        return any("Model" in m.name for m in model.bases)

    def locations(self, context: models.Context, node: SgNode, model: models.Model):
        yield context.get_module_path(model.name)

    def iter_methods(self, context: models.Context, node: SgNode, model: models.Model):
        for i in node.find_all(
            pattern=dedent(
                """
                def $METHOD($$$ARGS):
                    $$$DEFINITION
                """
            )
        ):
            node_range = i.range()
            args = FunctionArgs().parse_args(i, "ARGS")

            yield models.ModelMethod(
                node=i,
                name=i["METHOD"].text(),
                args=len(args),
                lines=node_range.end.line - node_range.start.line,
            )

    def get_model_manager_name(self, context: models.Context, node: SgNode) -> str:
        match = node.find(pattern="objects = $MANAGER($$$ARGS)")
        if not match:
            return ""

        manager = match["MANAGER"].text()
        return context.get_module_path(manager)

    def run(self, context: models.Context, node: SgNode):
        for cls in node.find_all(
            pattern=dedent(
                """
                class $NAME($$$BASE):
                    $$$DEFINITION
                """
            )
        ):
            node_range = cls.range()

            model = models.Model(
                node=cls,
                name=cls["NAME"].text(),
                file=context.current_file,
                position=(node_range.start.line, node_range.start.column),
                lines=node_range.end.line - node_range.start.line,
                manager=self.get_model_manager_name(context, cls),
                meta=self.get_model_meta(context, cls),
            )

            model.bases.extend(self.iter_base_classes(context, cls, model))
            model.fields.extend(self.iter_fields(context, cls, model))
            model.indexes.extend(self.iter_indexes(context, cls, model))
            model.locations.extend(self.locations(context, cls, model))
            model.methods.extend(self.iter_methods(context, cls, model))

            if not self.is_look_like_django_model(model):
                continue

            context.unresolved_models.append(model)

    def finish(self, context: models.Context) -> bool:
        for i in context.unresolved_models:
            for location in i.locations:
                context.resolved_models[location] = i

        context.unresolved_models = []
        return True


class ClassPathFixPlugin(FileBasePlugin):
    """修复类路径"""

    def should_run(self, context: models.Context, node: SgNode) -> bool:
        return True

    def fix_bases(self, context: models.Context, model: models.Model):
        for i in model.bases:
            i.class_path = context.get_module_path(i.class_path)

    def fix_fields(self, context: models.Context, model: models.Model):
        for i in model.fields:
            i.class_path = context.get_module_path(i.class_path)

    def run(self, context: models.Context, node: SgNode):
        for model in context.unresolved_models:
            if model.file != context.current_file:
                continue

            self.fix_bases(context, model)
            self.fix_fields(context, model)


class ExportModelPlugin(FileBasePlugin):
    def should_run(self, context: models.Context, node: SgNode) -> bool:
        return False

    def finish(self, context: models.Context) -> bool:
        for model in context.resolved_models.values():
            for location in model.locations:
                module, _, name = location.rpartition(".")
                module_refs = context.module_refs.get(module)
                if not module_refs:
                    continue

                for imported in [name, "*"]:
                    module_ref = module_refs.get(imported)
                    if not module_ref:
                        continue

                    model.locations.append(f"{module_ref.module}.{module_ref.alias or name}")

        return True


class ModelReferencePlugin(FileBasePlugin):
    def should_run(self, context: models.Context, node: SgNode) -> bool:
        return True

    def run(self, context: models.Context, node: SgNode):
        related_models: dict[str, str] = {}
        refs: list[str] = []

        for m in chain(
            node.find_all(pattern="$MODEL.objects.$METHOD($$$ARGS)"),
            node.find_all(pattern="$MODEL.objects.$METHOD()"),
        ):
            model = m["MODEL"].text()
            related_models[model] = context.module

            refs.append(model)

        for module in context.module_imports.values():
            name = module.real_name()
            if name == "*":
                continue

            if module.name == "models" or "models" in module.module:
                path = f"{module.module}.{name}"

            else:
                continue

            related_models[name] = path

        for model in related_models:
            for _ in chain(
                node.find_all(pattern=f"{model}($$$ARGS)"),
                node.find_all(pattern=f"$K = {model}"),
            ):
                refs.append(model)

        for ref in refs:
            imported, _, name = ref.partition(".")
            path = related_models.get(imported)
            if not path:
                continue

            context.weight.update([f"{path}.{name}" if name else path])

    def finish(self, context: models.Context) -> bool:
        for model in context.resolved_models.values():
            for location in model.locations:
                weight = context.weight.get(location)
                if weight:
                    model.weight += weight

        return True
