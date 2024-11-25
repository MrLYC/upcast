from dataclasses import dataclass, field
from typing import Any, Optional

import evalidate
from ast_grep_py import SgNode


@dataclass
class Evalidate:
    eval_model: evalidate.EvalModel = field(
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
                "List",
            ]
        )
    )

    def eval(self, code: str, scopes: Optional[dict[str, Any]] = None) -> Any:
        return evalidate.Expr(code, self.eval_model).eval(scopes)


@dataclass
class FunctionArg:
    name: str
    node: SgNode
    value_node: SgNode

    def value(self, **scopes) -> str:
        return Evalidate().eval(self.value_node.text(), scopes)


@dataclass
class FunctionArgs:
    args: dict[str, FunctionArg] = field(default_factory=dict)

    def parse(self, node: SgNode, group: str, args: tuple[str] = ()) -> "FunctionArgs":
        pos = 0
        len_args = len(args)

        for i in node.get_multiple_matches(group):
            kind = i.kind()

            if kind == ",":
                continue

            elif kind == "keyword_argument":
                pos = len_args
                name_node = i.child(0)
                name = name_node.text()

                self.args[name] = FunctionArg(name=name, node=i, value_node=i.child(2))

            elif pos < len_args:
                pos += 1
                name = args[pos]

                self.args[name] = FunctionArg(name=name, node=i, value_node=i)

        return self

    def parse_args(self, node: SgNode, group: str, args: tuple[str] = ()) -> dict[str, FunctionArg]:
        return self.parse(node, group, args).args


def make_path_absolute(root_module: str, path: str) -> str:
    if not path.startswith("."):
        return path

    relpath = path.lstrip(".")
    module_list = root_module.rsplit(".", maxsplit=len(path) - len(relpath))
    return ".".join(module_list) + relpath


@dataclass
class AnalysisModuleImport:
    node: SgNode
    module: str


    def parse_multiple_matches(self, matches: list[SgNode]):
        for i in matches:
            node_kind = i.kind()
            if node_kind in ("dotted_name", "wildcard_import"):
                yield i.text(), ""

            elif node_kind == "aliased_import":
                # x as y
                yield i.child(0).text(), i.child(2).text()

    def iter_import_directly(self, node: SgNode):
        for i in node.find_all(pattern="import $$$NAME"):
            for path, alias in self.parse_multiple_matches(i.get_multiple_matches("NAME")):
                path, _, name = path.rpartition(".")
                yield path, name, alias

    def iter_import_from(self, node: SgNode):
        for i in node.find_all(pattern="from $MODULE import $$$NAME"):
            path = make_path_absolute(self.module, i["MODULE"].text())

            for name, alias in self.parse_multiple_matches(i.get_multiple_matches("NAME")):
                yield path, name, alias

    def iter_import(self, node: SgNode):
        yield from self.iter_import_directly(node)
        yield from self.iter_import_from(node)
