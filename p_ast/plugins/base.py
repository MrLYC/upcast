from ast_grep_py import SgNode

from p_ast.core import Plugin, Context


class StarImportPlugin(Plugin):
    priority: int = 2

    def handle(self, context: Context, node: SgNode):
        result = node.find_all(pattern="from $MODULE import *")
        for i in result:
            context.add_imports(i.get_match("MODULE").text(), "*")


class ModuleImportPlugin(Plugin):
    module: str
    priority: int = 2

    def handle_import(self, context: Context, node: SgNode):
        if node.find(pattern=f"import {self.module}"):
            return True

    def handle(self, context: Context, node: SgNode):
        if self.handle_import(context, node):
            context.add_module(self.module)


class PyVarPlugin(Plugin):
    priority: int = 2

    def handle(self, context: Context, node: SgNode):
        if node.matches(kind="assign"):
            name = node.get_match("NAME").text()
            context.add_py_var(name)
