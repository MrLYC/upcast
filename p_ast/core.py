from typing import Set, List, Protocol, runtime_checkable, Dict, Tuple

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
        return f"{self.file}:{self.position[0]}, {self.position[1]}"

    def statement(self) -> str:
        return self.node.text()


class PYVar(BaseModel):
    node: SgNode
    name: str

    class Config:
        arbitrary_types_allowed = True


class Context(BaseModel):
    filename: str = ""
    imports: Set[str] = Field(default_factory=set)
    star_imports: Set[str] = Field(default_factory=set)
    env_vars: Dict[str, List[EnvVar]] = Field(default_factory=lambda: defaultdict(list))
    py_vars: Dict[str, PYVar] = Field(default_factory=dict)

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
        self.env_vars[env_var.name].append(env_var)

        return True

    def add_py_var(self, py_var: PYVar) -> bool:
        self.py_vars[py_var.name] = py_var

        return True


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

    def run(self, paths: List[str]):
        results: Dict[str, List[EnvVar]] = defaultdict(list)
        sorted_plugins = sorted(self.plugins, key=lambda p: p.priority)
        self.exporter.begin()
        for path in paths:
            with open(path) as f:
                code = f.read()
                root = SgRoot(code, "python")

            context = Context(filename=path)
            root_node = root.root()
            for plugin in sorted_plugins:
                plugin.run(context, root_node)

            for v in context.env_vars:
                results[v].extend(context.env_vars[v])

        for v in results:
            for var in results[v]:
                self.exporter.handle(var)

        self.exporter.end()
