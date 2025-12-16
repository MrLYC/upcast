"""Visitor pattern implementation for environment variable detection."""

import astroid
from astroid import nodes

from upcast.env_var_scanner.ast_utils import infer_literal_value, safe_as_string
from upcast.env_var_scanner.env_var_parser import (
    EnvVarInfo,
    EnvVarUsage,
    parse_env_var_usage,
)


class EnvVarChecker:
    """Checker that visits AST nodes to detect environment variable usage."""

    def __init__(self):
        """Initialize the checker with empty results."""
        self.env_vars: dict[str, EnvVarInfo] = {}
        self.current_file: str = ""

    def check_file(self, file_path: str) -> None:
        """Analyze a Python file for environment variable usage.

        Args:
            file_path: Path to the Python file to analyze
        """
        self.current_file = file_path

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            module = astroid.parse(content, path=file_path)
            self._visit_module(module)

        except Exception:  # noqa: S110
            # Silently skip files with parsing errors
            pass

    def _visit_module(self, module: nodes.Module) -> None:
        """Visit a module node and process its contents."""
        # Visit all nodes recursively
        for node in module.nodes_of_class((nodes.Call, nodes.Subscript)):
            if isinstance(node, nodes.Call):
                self._visit_call(node)
            elif isinstance(node, nodes.Subscript):
                self._visit_subscript(node)

    def _visit_call(self, node: nodes.Call) -> None:
        """Visit a Call node and extract env var usage if applicable."""
        try:
            usage = parse_env_var_usage(node, self.current_file)
            if usage:
                self._add_usage(usage)
        except Exception:  # noqa: S110
            # Skip nodes that fail to parse
            pass

    def _visit_subscript(self, node: nodes.Subscript) -> None:
        """Visit a Subscript node to detect os.environ[KEY] patterns."""
        try:
            value_str = safe_as_string(node.value)

            # Check if it's os.environ or environ subscript
            if "environ" not in value_str:
                return

            # Extract the key
            var_name = node.slice.value if isinstance(node.slice, nodes.Const) else infer_literal_value(node.slice)

            if not isinstance(var_name, str):
                return

            # Create usage for os.environ[KEY] - always required
            location = f"{self.current_file}:{node.lineno}"
            statement = safe_as_string(node)

            usage = EnvVarUsage(
                name=var_name,
                location=location,
                statement=statement,
                type=None,  # No type inference for environ[]
                default=None,
                required=True,  # os.environ[KEY] raises KeyError if not found
                node=node,
            )

            self._add_usage(usage)

        except Exception:  # noqa: S110
            pass

    def _add_usage(self, usage: EnvVarUsage) -> None:
        """Add a usage to the aggregated results."""
        if usage.name not in self.env_vars:
            self.env_vars[usage.name] = EnvVarInfo(name=usage.name)

        self.env_vars[usage.name].add_usage(usage)

    def _visit_node(self, node: nodes.NodeNG) -> None:
        """Visit an AST node and detect environment variable patterns."""
        # Recursively visit all child nodes
        for child in node.get_children():
            if isinstance(child, nodes.Call):
                self._visit_call(child)
            elif isinstance(child, nodes.Subscript):
                self._visit_subscript(child)
            else:
                self._visit_node(child)

    def get_results(self) -> dict[str, EnvVarInfo]:
        """Get the aggregated environment variable information.

        Returns:
            Dictionary mapping variable names to EnvVarInfo objects
        """
        return self.env_vars
