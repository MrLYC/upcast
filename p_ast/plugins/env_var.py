import ast
from typing import Optional, List

from ast_grep_py import SgNode

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
    priority: int = 9

    def should_run(self, context: Context, node: SgNode) -> bool:
        return context.has_imports(self.module, self.imports)

    def handle_name(self, node: Optional[SgNode]) -> str:
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
        self, type_node: Optional[SgNode], value_node: Optional[SgNode]
    ) -> (str, str):
        type_desc = "str"
        if type_node and type_node.matches(kind="identifier"):
            type_desc = type_node.text()

        if not value_node:
            return type_desc, ""

        return type_desc, value_node.text()

    def handle(self, context: Context, node: SgNode):
        result = node.find_all(pattern=self.pattern)
        for i in result:
            name = self.handle_name(i.get_match("NAME"))
            if not name:
                continue

            value_type, value = self.handle_value(
                i.get_match("TYPE"), i.get_match("VALUE")
            )

            context.add_var(
                Var(
                    node=i,
                    file=context.filename,
                    name=name,
                    value=value,
                    value_type=value_type,
                )
            )


class EnvVarHub(PluginHub):
    @property
    def plugins(self) -> List[Plugin]:
        return [
            StarImportPlugin(),
            ModuleImportPlugin(module="os"),
            EnvRefPlugin(pattern="$TYPE(os.getenv($NAME))", module="os"),
            EnvRefPlugin(pattern="$TYPE(os.getenv($NAME, $VALUE))", module="os"),
            EnvRefPlugin(pattern="$TYPE(os.environ[$NAME])", module="os"),
            EnvRefPlugin(pattern="$TYPE(os.environ.get($NAME))", module="os"),
            EnvRefPlugin(pattern="$TYPE(os.environ.get($NAME, $VALUE))", module="os"),
            EnvRefPlugin(pattern="os.getenv($NAME)", module="os"),
            EnvRefPlugin(pattern="os.getenv($NAME, $VALUE)", module="os"),
            EnvRefPlugin(pattern="os.environ[$NAME]", module="os"),
            EnvRefPlugin(pattern="os.environ.get($NAME)", module="os"),
            EnvRefPlugin(pattern="os.environ.get($NAME, $VALUE)", module="os"),
            EnvRefPlugin(pattern="$TYPE(getenv($NAME))", module="os", imports="getenv"),
            EnvRefPlugin(
                pattern="$TYPE(getenv($NAME, $VALUE))", module="os", imports="getenv"
            ),
            EnvRefPlugin(
                pattern="$TYPE(environ[$NAME])", module="os", imports="environ"
            ),
            EnvRefPlugin(
                pattern="$TYPE(environ.get($NAME))", module="os", imports="environ"
            ),
            EnvRefPlugin(
                pattern="$TYPE(environ.get($NAME, $VALUE))",
                module="os",
                imports="environ",
            ),
            EnvRefPlugin(pattern="getenv($NAME)", module="os", imports="getenv"),
            EnvRefPlugin(
                pattern="getenv($NAME, $VALUE)", module="os", imports="getenv"
            ),
            EnvRefPlugin(pattern="environ[$NAME]", module="os", imports="environ"),
            EnvRefPlugin(pattern="environ.get($NAME)", module="os", imports="environ"),
            EnvRefPlugin(
                pattern="environ.get($NAME, $VALUE)", module="os", imports="environ"
            ),
            EnvRefPlugin(pattern="env.$TYPE($NAME)", module="environ", imports="Env"),
            EnvRefPlugin(
                pattern="env.$TYPE($NAME, default=$VALUE)",
                module="environ",
                imports="Env",
            ),
        ]
