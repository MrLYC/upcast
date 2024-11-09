from typing import Set, List, Protocol, runtime_checkable, Dict, Tuple, Iterable, TextIO

from ast_grep_py import SgNode, SgRoot
from mypy.binder import defaultdict
from pydantic import BaseModel, Field


class EnvVar(BaseModel):
    node: SgNode
    name: str
    position: Tuple[int, int]
    file: str = ""
    cast: str = ""
    value: str = ""

    class Config:
        arbitrary_types_allowed = True

    def location(self) -> str:
        return f"{self.file}:{self.position[0]},{self.position[1]}"

    def statement(self) -> str:
        return self.node.text()

    def merge_from(self, other: "EnvVar") -> bool:
        if self.name != other.name:
            return False

        if self.file != other.file:
            return False

        if self.position != other.position:
            return False

        merged = False
        if not self.cast and other.cast:
            self.cast = other.cast
            merged = True

        if not self.value and other.value:
            self.value = other.value
            merged = True

        my_range = self.node.range()
        other_range = other.node.range()

        if my_range.start.line < other_range.start.line:
            self.node = other.node
            merged = True
        elif (
            my_range.start.line == other_range.start.line
            and my_range.start.column < other_range.start.column
        ):
            self.node = other.node
            merged = True

        if my_range.end.line > other_range.end.line:
            self.node = other.node
            merged = True
        elif (
            my_range.end.line == other_range.end.line
            and my_range.end.column > other_range.end.column
        ):
            self.node = other.node
            merged = True

        return merged


class PYVar(BaseModel):
    node: SgNode
    name: str

    class Config:
        arbitrary_types_allowed = True


class Context(BaseModel):
    filename: str = ""
    imports: Set[str] = Field(default_factory=set)
    star_imports: Set[str] = Field(default_factory=set)
    env_vars: Dict[Tuple[int, int], EnvVar] = Field(default_factory=dict)

    def has_module(self, path: str) -> bool:
        module, _, name = path.rpartition(":")

        return self.has_imports(module, name)

    def has_imports(self, path: str, name: str = "") -> bool:
        if not path:
            return True

        if path in self.imports:
            return True

        if f"{path}:{name}" in self.imports:
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

    def iter_env_vars(self) -> Iterable[EnvVar]:
        return self.env_vars.values()


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
    def plugins(self) -> List[Plugin]:
        raise NotImplementedError

    def run(self, files: Iterable[TextIO]):
        results: Dict[str, List[EnvVar]] = defaultdict(list)
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
