import os.path
import re
from collections.abc import Iterable
from textwrap import dedent
from typing import Any, ClassVar, Protocol, TextIO

from ast_grep_py import SgNode, SgRoot
from pydantic import BaseModel

from upcast.django_model import models
from upcast.utils import AnalysisModuleImport, FunctionArgs


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
            ClassPathFixPlugin(),
            ExportModelPlugin(),
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
            for plugin in plugins:
                if plugin.finish(self.context):
                    plugins.remove(plugin)


class FileBasePlugin(Plugin):
    def finish(self, context: models.Context) -> bool:
        return True


class ModuleImportPlugin(FileBasePlugin):
    """查找模块导入"""

    def should_run(self, context: models.Context, node: SgNode) -> bool:
        return "models" in context.current_file

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
        "choices",
        "default",
        "help_text",
        "verbose_name",
        "max_length",
        "auto_created",
        "on_delete",
        "related_name",
    }

    def should_run(self, context: models.Context, node: SgNode) -> bool:
        return "models" in context.current_file

    def iter_base_classes(self, context: models.Context, node: SgNode, model: models.Model):
        for i in node.get_multiple_matches("BASE"):
            kind = i.kind()
            if kind in ["attribute", "identifier"]:
                yield models.ModelBase(node=i, name=i.text(), class_path=i.text())

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

            imported, _, type_ = cls.partition(".")

            yield models.ModelField(
                node=i,
                name=attr,
                type=type_ or imported,
                class_path=cls,
                kwargs={name: value.value_node.text() for name, value in args.items()},
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

    def iter_indexes_from_meta(self, context: models.Context, node: SgNode, model: models.Model):
        meta_cls = node.find(
            pattern=dedent(
                """
                class Meta:
                    $$$DEFINITION
                """
            )
        )
        if not meta_cls:
            return

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
        yield f"{context.module}.{model.name}"

    def run(self, context: models.Context, node: SgNode):
        for i in node.find_all(
            pattern=dedent(
                """
                class $NAME($$$BASE):
                    $$$DEFINITION
                """
            )
        ):
            node_range = i.range()

            model = models.Model(
                node=i,
                name=i["NAME"].text(),
                file=context.current_file,
                position=(node_range.start.line, node_range.start.column),
            )

            model.bases.extend(self.iter_base_classes(context, i, model))
            model.fields.extend(self.iter_fields(context, i, model))
            model.indexes.extend(self.iter_indexes(context, i, model))
            model.locations.extend(self.locations(context, i, model))

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

    def get_module_path(self, context: models.Context, class_path: str):
        imported, _, attribute = class_path.partition(".")
        module = context.module_imports.get(imported)
        if module:
            return f"{module.module}.{class_path}"

        return f"{context.module}.{class_path}"

    def fix_bases(self, context: models.Context, model: models.Model):
        for i in model.bases:
            i.class_path = self.get_module_path(context, i.class_path)

    def fix_fields(self, context: models.Context, model: models.Model):
        for i in model.fields:
            i.class_path = self.get_module_path(context, i.class_path)

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
