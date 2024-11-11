from dataclasses import field
from typing import Optional

from ast_grep_py import SgNode


class FunctionArgs:
    args: list[SgNode] = field(default_factory=list)
    kwargs: dict[str, SgNode] = field(default_factory=dict)

    def parse(self, node: SgNode, group: str):
        for i in node.get_multiple_matches(group):
            if i.matches(kind=","):
                continue
            elif i.matches(kind="keyword_argument"):
                self.kwargs[i.child(0).text()] = i.child(1)
            else:
                self.args.append(i)

    def get_args(self, keys: dict[str, int]) -> dict[str, Optional[SgNode]]:
        args: dict[str, Optional[SgNode]] = {}
        for key, index in keys.items():
            if index < len(self.args):
                args[key] = self.args[index]
            elif key in self.kwargs:
                args[key] = self.kwargs[key]

        return args
