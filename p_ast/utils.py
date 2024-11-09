from dataclasses import field
from typing import List, Dict, Optional

from ast_grep_py import SgNode


class FunctionArgs:
    args: List[SgNode] = field(default_factory=list)
    kwargs: Dict[str, SgNode] = field(default_factory=dict)

    def parse(self, node: SgNode, group: str):
        for i in node.get_multiple_matches(group):
            if i.matches(kind=","):
                continue
            elif i.matches(kind="keyword_argument"):
                self.kwargs[i.child(0).text()] = i.child(1)
            else:
                self.args.append(i)

    def get_args(self, keys: Dict[str, int]) -> Dict[str, Optional[SgNode]]:
        args: Dict[str, Optional[SgNode]] = {}
        for key, index in keys.items():
            if index < len(self.args):
                args[key] = self.args[index]
            elif key in self.kwargs:
                args[key] = self.kwargs[key]

        return args
