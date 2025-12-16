import bisect
from collections import defaultdict
from collections.abc import Iterable
from typing import Any, Protocol, TextIO, runtime_checkable

import evalidate
from ast_grep_py import SgNode, SgRoot
from pydantic import BaseModel, Field


class EnvVar(BaseModel):
    node: SgNode
    name: str
    position: tuple[int, int]
    file: str = ""
    cast: str = ""
    value: str = ""
    required: bool = False

    class Config:
        arbitrary_types_allowed = True

    def location(self) -> str:
        return f"{self.file}:{self.position[0]},{self.position[1]}"

    def statement(self) -> str:
        return self.node.text()

    def _merge_range(self, other: "EnvVar") -> bool:
        merged = False
        my_range = self.node.range()
        other_range = other.node.range()

        if my_range.start.line < other_range.start.line or (
            my_range.start.line == other_range.start.line and my_range.start.column < other_range.start.column
        ):
            self.node = other.node
            merged = True

        if my_range.end.line > other_range.end.line or (
            my_range.end.line == other_range.end.line and my_range.end.column > other_range.end.column
        ):
            self.node = other.node
            merged = True

        return merged

    def merge_from(self, other: "EnvVar", strict: bool = True) -> bool:
        if self.name != other.name:
            return False

        if strict and self.file != other.file:
            return False

        if strict and self.position != other.position:
            return False

        merged = False
        if not self.cast and other.cast:
            self.cast = other.cast
            merged = True

        if not self.value and other.value:
            self.value = other.value
            merged = True

        if not self.required and other.required:
            self.required = other.required
            merged = True

        if self._merge_range(other):
            merged = True

        return merged


class PYVar(BaseModel):
    node: SgNode
    name: str
    value: Any = None

    class Config:
        arbitrary_types_allowed = True


class Context(BaseModel):
    filename: str = ""
    imports: set[str] = Field(default_factory=set)
    star_imports: set[str] = Field(default_factory=set)
    env_vars: dict[tuple[int, int], EnvVar] = Field(default_factory=dict)
    global_vars: list[PYVar] = Field(default_factory=list)
    eval_model: evalidate.EvalModel = Field(
        default_factory=lambda: evalidate.EvalModel(
            nodes=[
                "JoinedStr",
                "Expression",
                "FormattedValue",
                "Constant",
                "Name",
                "Load",
                "BinOp",
                "Add",
                "Sub",
                "Mult",
                "Div",
                "Mod",
                "Attribute",
            ]
        )
    )

    def has_module(self, path: str) -> bool:
        module, sep, name = path.rpartition(":")

        if sep:
            return self.has_imports(module, name)

        return self.has_imports(name, "")

    def has_imports(self, path: str, name: str = "") -> bool:
        if not path:
            return True

        if path in self.imports:
            return True

        if name and f"{path}:{name}" in self.imports:
            return True

        return self.has_star_imports()

    def has_star_imports(self, path: str = "") -> bool:
        if not path:
            return bool(self.star_imports)

        return path in self.star_imports

    def add_module(self, path: str):
        self.imports.add(path)

    def add_imports(self, module: str, name: str):
        self.imports.add(f"{module}:{name}")

        if name == "*":
            self.star_imports.add(module)

    def add_env_var(self, env_var: EnvVar) -> bool:
        env_var.file = self.filename
        declared = self.env_vars.get(env_var.position)
        if declared:
            declared.merge_from(env_var)
            return False

        self.env_vars[env_var.position] = env_var
        return True

    def add_global_var(self, py_var: PYVar) -> bool:
        def _sort_key(v: PYVar):
            r = v.node.range()
            return r.start.line, r.start.column

        bisect.insort(self.global_vars, py_var, key=_sort_key)
        return True

    def iter_env_vars(self) -> Iterable[EnvVar]:
        return self.env_vars.values()

    def evalidate_node(self, node: SgNode) -> Any:
        scopes: dict[str, Any] = {}
        node_range = node.range()

        for i in self.global_vars:
            var_range = i.node.range()
            if node_range.start.line < var_range.start.line:
                break

            scopes[i.name] = i.value

        return evalidate.Expr(node.text(), model=self.eval_model).eval(scopes)


class Plugin(BaseModel):
    priority: int

    def should_run(self, context: Context, node: SgNode) -> bool:
        return True

    def handle(self, context: Context, node: SgNode):
        raise NotImplementedError

    def run(self, context: Context, node: SgNode):
        if not self.should_run(context, node):
            return

        self.handle(context, node)


@runtime_checkable
class EnvVarExporter(Protocol):
    def begin(self): ...
    def handle(self, var: EnvVar): ...
    def end(self): ...


class PluginHub(BaseModel):
    exporter: EnvVarExporter

    class Config:
        arbitrary_types_allowed = True

    @property
    def plugins(self) -> list[Plugin]:
        raise NotImplementedError

    def run(self, files: Iterable[TextIO]):
        results: dict[str, list[EnvVar]] = defaultdict(list)
        sorted_plugins = sorted(self.plugins, key=lambda p: p.priority)
        self.exporter.begin()
        for f in files:
            code = f.read()
            root = SgRoot(code, "python")

            context = Context(filename=f.name)
            root_node = root.root()
            for plugin in sorted_plugins:
                plugin.run(context, root_node)

            for v in context.iter_env_vars():
                results[v.name].append(v)

        for v in results:
            for var in results[v]:
                self.exporter.handle(var)

        self.exporter.end()
