import ast
from typing import Optional, List, Dict, Tuple

from ast_grep_py import SgNode, Range

from p_ast.core import Plugin, Context, Var, PluginHub


class ModuleImportPlugin(Plugin):
    module: str
    priority: int = 2

    def handle_import(self, context: Context, node: SgNode):
        if node.find(pattern=f"import {self.module}"):
            return True

    def handle(self, context: Context, node: SgNode):
        if self.handle_import(context, node):
            context.add_module(self.module)


class StarImportPlugin(Plugin):
    priority: int = 2

    def handle(self, context: Context, node: SgNode):
        result = node.find_all(pattern="from $MODULE import *")
        for i in result:
            context.add_imports(i.get_match("MODULE").text(), "*")


class EnvRefPlugin(Plugin):
    pattern: str
    module: str = ""
    imports: str = ""
    type_convert: bool = True
    or_default: bool = True
    priority: int = 9

    @property
    def patterns(self) -> List[str]:
        yield self.pattern

        if self.type_convert and self.or_default:
            yield f"$TYPE({self.pattern}) or $VALUE"
            yield f"$TYPE({self.pattern} or $VALUE)"

        if self.type_convert:
            yield f"$TYPE({self.pattern})"

        if self.or_default:
            yield f"{self.pattern} or $VALUE"

    def should_run(self, context: Context, node: SgNode) -> bool:
        return context.has_imports(self.module, self.imports)

    def handle_name(self, node: Optional[SgNode]) -> (str, Range):
        if not node:
            return ""

        if not node.matches(kind="string"):
            return ""

        statement = node.text()
        if statement.startswith("f"):
            # fstring is not supported
            return ""

        return ast.literal_eval(statement)

    def handle_value(
        self, cast_node: Optional[SgNode], value_node: Optional[SgNode]
    ) -> (str, str):
        cast = ""
        if cast_node and cast_node.matches(kind="identifier"):
            cast = cast_node.text()

        if not value_node:
            return cast, ""

        return cast, value_node.text()

    def iter_var_by_pattern(self, pattern: str, context: Context, node: SgNode):
        for i in node.find_all(pattern=pattern):
            name_node = i.get_match("NAME")
            if not name_node:
                continue

            name = self.handle_name(name_node)
            if not name:
                continue

            cast, value = self.handle_value(i.get_match("TYPE"), i.get_match("VALUE"))
            name_node_range = name_node.range()

            yield Var(
                node=i,
                file=context.filename,
                name=name,
                value=value,
                cast=cast,
                position=(name_node_range.start.line, name_node_range.start.column),
            )

    def handle(self, context: Context, node: SgNode):
        discovered_vars: Dict[Tuple[int, int], Var] = {}

        for pattern in self.patterns:
            for i in self.iter_var_by_pattern(pattern, context, node):
                discovered_var = discovered_vars.get(i.position)
                if not discovered_var:
                    discovered_vars[i.position] = i
                    continue

                if i.value and not discovered_var.value:
                    discovered_var.value = i.value

                if i.cast and not discovered_var.cast:
                    discovered_var.cast = i.cast

                var_range = i.node.range()
                discovered_var_range = discovered_var.node.range()

                if var_range.start.line < discovered_var_range.start.line:
                    continue
                if var_range.start.column < discovered_var_range.start.column:
                    continue
                if var_range.end.line > discovered_var_range.end.line:
                    continue
                if var_range.end.column > discovered_var_range.end.column:
                    continue

                discovered_var.node = i.node

        for i in discovered_vars.values():
            context.add_var(i)


class EnvVarHub(PluginHub):
    django_env_name: str = "env"

    @property
    def plugins(self) -> List[Plugin]:
        return [
            StarImportPlugin(),
            ModuleImportPlugin(module="os"),
            # stdlib
            EnvRefPlugin(pattern="os.getenv($NAME)", module="os"),
            EnvRefPlugin(pattern="os.getenv($NAME, $VALUE)", module="os"),
            EnvRefPlugin(pattern="os.environ[$NAME]", module="os"),
            EnvRefPlugin(pattern="os.environ.get($NAME)", module="os"),
            EnvRefPlugin(pattern="os.environ.get($NAME, $VALUE)", module="os"),
            EnvRefPlugin(pattern="getenv($NAME)", module="os", imports="getenv"),
            EnvRefPlugin(
                pattern="getenv($NAME, $VALUE)", module="os", imports="getenv"
            ),
            EnvRefPlugin(pattern="environ[$NAME]", module="os", imports="environ"),
            EnvRefPlugin(pattern="environ.get($NAME)", module="os", imports="environ"),
            EnvRefPlugin(
                pattern="environ.get($NAME, $VALUE)", module="os", imports="environ"
            ),
            # django env
            EnvRefPlugin(
                pattern=f"{self.django_env_name}.$TYPE($NAME)",
                module="environ",
                imports="Env",
                type_convert=False,
            ),
            EnvRefPlugin(
                pattern=f"{self.django_env_name}.$TYPE($NAME, default=$VALUE)",
                module="environ",
                imports="Env",
                type_convert=False,
            ),
        ]
