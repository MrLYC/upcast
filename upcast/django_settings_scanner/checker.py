"""AST visitor for Django settings usage detection."""

from pathlib import Path

import astroid
from astroid import nodes

from upcast.django_settings_scanner.ast_utils import (
    extract_setting_name,
    is_settings_attribute_access,
    is_settings_getattr_call,
    is_settings_hasattr_call,
)
from upcast.django_settings_scanner.settings_parser import (
    SettingsUsage,
    SettingsVariable,
    parse_settings_usage,
)


class DjangoSettingsChecker:
    """Checker to detect and aggregate Django settings usage."""

    def __init__(self, base_path: str) -> None:
        """Initialize the checker.

        Args:
            base_path: Project root path for relative path calculation
        """
        self.base_path = Path(base_path)
        self.settings: dict[str, SettingsVariable] = {}
        self.current_file: str = ""

    def _visit_node(self, node: nodes.NodeNG) -> None:
        """Recursively visit AST nodes.

        Args:
            node: The node to visit
        """
        # Check if it's an attribute access (settings.KEY)
        if isinstance(node, nodes.Attribute):
            if is_settings_attribute_access(node):
                usage = parse_settings_usage(node, str(self.base_path), self.current_file)
                if usage:
                    setting_name = extract_setting_name(node)
                    if setting_name:
                        self._register_usage(setting_name, usage)

        # Check if it's a call (getattr/hasattr)
        elif isinstance(node, nodes.Call) and (is_settings_getattr_call(node) or is_settings_hasattr_call(node)):
            usage = parse_settings_usage(node, str(self.base_path), self.current_file)
            if usage:
                setting_name = extract_setting_name(node)
                if setting_name:
                    self._register_usage(setting_name, usage)

        # Recursively visit child nodes
        for child in node.get_children():
            self._visit_node(child)

    def _register_usage(self, setting_name: str, usage: SettingsUsage) -> None:
        """Register a settings usage and aggregate by variable name.

        Args:
            setting_name: The settings variable name
            usage: The usage details
        """
        if setting_name not in self.settings:
            self.settings[setting_name] = SettingsVariable(name=setting_name, count=0, locations=[])

        self.settings[setting_name].count += 1
        self.settings[setting_name].locations.append(usage)

    def check_file(self, file_path: str) -> None:
        """Parse and visit a Python file to detect settings usage.

        Args:
            file_path: Absolute path to the Python file
        """
        self.current_file = file_path

        try:
            # Parse the file with astroid
            module = astroid.MANAGER.ast_from_file(file_path)
            # Visit the AST
            self._visit_node(module)
        except Exception as e:
            # Log error but continue with other files
            print(f"Error parsing {file_path}: {e!s}")
