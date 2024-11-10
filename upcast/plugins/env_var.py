import ast
from typing import Optional, List, Set

from ast_grep_py import SgNode, Range

from upcast.core import Plugin, Context, EnvVar, PluginHub
from upcast.plugins.base import ModuleImportPlugin


class FixMixin:
    value_kind_to_cast_mappings = {
        "string": "str",
        "integer": "int",
        "float": "float",
        "true": "bool",
        "false": "bool",
        "list": "list",
        "tuple": "tuple",
        "dictionary": "dictionary",
    }

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

        if not cast and value_node.kind() in self.value_kind_to_cast_mappings:
            cast = self.value_kind_to_cast_mappings[value_node.kind()]

        return cast, value_node.text()

    def make_env_var(
        self,
        result: SgNode,
        required: bool,
    ) -> Optional[EnvVar]:
        name_node = result.get_match("NAME")
        if not name_node:
            return None

        name = self.handle_name(name_node)
        if not name:
            return None

        cast, value = self.handle_value(
            result.get_match("TYPE"), result.get_match("VALUE")
        )

        name_node_range = name_node.range()

        return EnvVar(
            node=result,
            name=name,
            value=value,
            cast=cast,
            required=required,
            position=(name_node_range.start.line, name_node_range.start.column),
        )


class EnvRefPlugin(Plugin, FixMixin):
    pattern: str
    module: str = ""
    imports: str = ""
    type_convert: bool = True
    or_default: bool = True
    required: bool = False
    priority: int = 8

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

    def iter_var_by_pattern(self, pattern: str, node: SgNode):
        for i in node.find_all(pattern=pattern):
            env_var = self.make_env_var(i, self.required)
            if env_var:
                yield env_var

    def handle(self, context: Context, node: SgNode):
        for pattern in self.patterns:
            for i in self.iter_var_by_pattern(pattern, node):
                context.add_env_var(i)


class DjangoEnvPlugin(EnvRefPlugin, FixMixin):
    pattern: str = ""
    priority: int = 7
    var_class: str = "Env"
    var_name: str = "env"
    defined_vars: Set[str] = set()

    @property
    def patterns(self) -> List[str]:
        yield f"{self.var_name}.$TYPE($NAME)"
        yield f"{self.var_name}($NAME)"
        yield f"{self.var_name}.$TYPE($NAME, default=$VALUE)"
        yield f"{self.var_name}.$TYPE($NAME, $VALUE)"

    def should_run(self, context: Context, node: SgNode) -> bool:
        if context.has_module("environ"):
            self.var_class = "environ.Env"

            return True

        if context.has_imports("environ", "Env"):
            return True

        return False

    def handle_declare(self, context: Context, node: SgNode) -> str:
        declare_node = node.find(pattern=f"$NAME = {self.var_class}($$$ARGS)")
        if not declare_node:
            return self.var_name

        self.var_name = declare_node["NAME"].text()

        for i in declare_node.get_multiple_matches("ARGS"):
            if not i.matches(kind="keyword_argument"):
                continue

            name_node = i.child(0)
            name = name_node.text()
            name_node_range = name_node.range()
            arg_node = i.child(2)
            cast_node = arg_node.child(1)
            value_node = arg_node.child(3)

            self.defined_vars.add(name)
            context.add_env_var(
                EnvVar(
                    node=i,
                    name=name,
                    value=value_node.text(),
                    cast=cast_node.text(),
                    position=(
                        name_node_range.start.line,
                        name_node_range.start.column,
                    ),
                )
            )

    def handle(self, context: Context, node: SgNode):
        self.handle_declare(context, node)
        for pattern in self.patterns:
            for i in self.iter_var_by_pattern(pattern, node):
                if not i.value and i.name not in self.defined_vars:
                    i.required = True

                context.add_env_var(i)


class EnvVarHub(PluginHub):
    django_env_name: str = "env"

    @property
    def plugins(self) -> List[Plugin]:
        return [
            ModuleImportPlugin(),
            # stdlib
            EnvRefPlugin(pattern="os.getenv($NAME)", module="os"),
            EnvRefPlugin(pattern="os.getenv($NAME, $VALUE)", module="os"),
            EnvRefPlugin(pattern="os.environ[$NAME]", module="os", required=True),
            EnvRefPlugin(pattern="os.environ.get($NAME)", module="os"),
            EnvRefPlugin(pattern="os.environ.get($NAME, $VALUE)", module="os"),
            EnvRefPlugin(pattern="getenv($NAME)", module="os", imports="getenv"),
            EnvRefPlugin(
                pattern="getenv($NAME, $VALUE)", module="os", imports="getenv"
            ),
            EnvRefPlugin(
                pattern="environ[$NAME]", module="os", imports="environ", required=True
            ),
            EnvRefPlugin(pattern="environ.get($NAME)", module="os", imports="environ"),
            EnvRefPlugin(
                pattern="environ.get($NAME, $VALUE)", module="os", imports="environ"
            ),
            # django env
            DjangoEnvPlugin(),
        ]
