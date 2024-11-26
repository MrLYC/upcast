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
            ExportModelPlugin(),
            ModelWeightCalcPlugin(),
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

        return any(i.endswith("Field") for i in cls.rpartition("."))

    def iter_fields(self, context: models.Context, node: SgNode, model: models.Model):
        class_indent = node.range().start.column

        for i in node.find_all(pattern="$ATTR = $CLS($$$ARGS)"):
            if i.range().start.column <= class_indent:
                continue

            attr = i["ATTR"].text()
            cls = i["CLS"].text()
            args = FunctionArgs().parse_args(i, "ARGS")
            class_path = context.get_module_path(cls)

            if not self.is_look_like_django_field(attr, class_path, args):
                continue

            safe_kwargs = {}
            for k, v in args.items():
                if k not in self.field_available_kwargs:
                    continue
                with suppress(Exception):
                    safe_kwargs[k] = v.value()

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
            if kwargs.get("primary_key") or f.name == "id":
                yield models.ModelIndex(
                    node=f.node,
                    fields=[f.name],
                    kind="primary_key",
                )

            if kwargs.get("db_index"):
                yield models.ModelIndex(
                    node=f.node,
                    fields=[f.name],
                    kind="index",
                )

            if kwargs.get("unique"):
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

    def iter_indexes_from_meta_unique_together(self, context: models.Context, node: SgNode, model: models.Model):
        if not model.meta:
            return

        meta_cls = model.meta.node
        evalidate = Evalidate()

        unique_together = meta_cls.find(pattern="unique_together = $FIELDS")
        if not unique_together:
            return

        fields = []
        with suppress(Exception):
            fields.extend(evalidate.eval(unique_together["FIELDS"].text()))

        if not fields:
            return

        if isinstance(fields[0], str):
            yield models.ModelIndex(
                node=unique_together,
                kind="unique",
                fields=list(fields),
            )
            return

        for i in fields:
            yield models.ModelIndex(
                node=unique_together,
                kind="unique",
                fields=list(i),
            )

    def iter_indexes_from_meta(self, context: models.Context, node: SgNode, model: models.Model):
        if not model.meta:
            return

        meta_cls = model.meta.node

        indexes = meta_cls.find(pattern="indexes = $INDEXES")
        if indexes:
            for i in indexes.find_all(pattern="$F($$$ARGS)"):
                args = FunctionArgs().parse_args(i, "ARGS")
                fields = args.get("fields")
                if not fields:
                    continue

                fields_value = fields.value()
                if not fields_value:
                    continue

                unique = args.get("unique")
                if not unique:
                    continue

                unique_value = unique.value()

                yield models.ModelIndex(
                    node=i,
                    fields=fields_value,
                    kind=unique_value,
                )

    def iter_indexes(self, context: models.Context, node: SgNode, model: models.Model):
        yield from self.iter_indexes_from_meta_unique_together(context, node, model)
        yield from self.iter_indexes_from_model(context, node, model)
        yield from self.iter_indexes_from_meta(context, node, model)

    def is_look_like_django_model(self, model: models.Model) -> bool:
        if not model.fields:
            return False

        if not model.bases:
            return False

        for finfo in model.fields:
            if "django." in finfo.class_path:
                return True

        return any("django." in base.class_path for base in model.bases)

    def locations(self, context: models.Context, node: SgNode, model: models.Model):
        yield context.get_module_path(model.name)

    def iter_methods(self, context: models.Context, node: SgNode, model: models.Model):
        for i in chain(
            node.find_all(
                pattern=dedent(
                    """
                def $METHOD($$$ARGS):
                    $$$DEFINITION
                """
                )
            ),
            node.find_all(
                pattern=dedent(
                    """
                def $METHOD($$$ARGS) -> $RETURN:
                    $$$DEFINITION
                """
                )
            ),
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


class ModelWeightCalcPlugin(FileBasePlugin):
    def should_run(self, context: models.Context, node: SgNode) -> bool:
        return True

    def run(self, context: models.Context, node: SgNode):
        related_models: dict[str, str] = {}
        refs: list[str] = []

        for m in node.find_all(pattern="$MODEL.objects.$METHOD($$$ARGS)"):
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
                node.find_all(pattern=f"$V: {model}"),
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
