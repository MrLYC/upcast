from dataclasses import field
from dataclasses import dataclass
from ast_grep_py import SgNode


@dataclass
class FunctionArg:
    name: str
    node: SgNode
    value_node: SgNode


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
