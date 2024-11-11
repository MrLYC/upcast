from ast_grep_py import SgNode

from upcast.core import Context, Plugin


class ModuleImportPlugin(Plugin):
    priority: int = 2

    def handle_import(self, context: Context, node: SgNode) -> bool:
        result = node.find(pattern="import $MODULE")
        if not result:
            return False

        module_node = result.get_match("MODULE")
        context.add_module(module_node.text())

    def handle_import_from(self, context: Context, node: SgNode):
        result = node.find_all(pattern="from $MODULE import $$$NAME")
        for i in result:
            module_node = i.get_match("MODULE")
            module_name = module_node.text()

            for name_node in i.get_multiple_matches("NAME"):
                if name_node.kind() == ",":
                    continue

                context.add_imports(module_name, name_node.text())

    def handle(self, context: Context, node: SgNode):
        self.handle_import(context, node)
        self.handle_import_from(context, node)


class PyVarPlugin(Plugin):
    priority: int = 2

    def handle(self, context: Context, node: SgNode):
        if node.matches(kind="assign"):
            name = node.get_match("NAME").text()
            context.add_py_var(name)
