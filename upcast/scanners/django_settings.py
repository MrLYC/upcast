"""Django settings scanner.

This scanner analyzes Django settings definitions and usages across the project,
producing a comprehensive output that combines both.
"""

import logging
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

from astroid import nodes

from upcast.common.django.settings_utils import (
    extract_setting_name,
    is_settings_attribute_access,
    is_settings_getattr_call,
    is_settings_hasattr_call,
)
from upcast.common.file_utils import get_relative_path_str
from upcast.common.scanner_base import BaseScanner
from upcast.models.django_settings import (
    DjangoSettingsOutput,
    DjangoSettingsSummary,
    SettingDefinitionItem,
    SettingInfo,
    SettingUsageItem,
)

logger = logging.getLogger(__name__)


class DjangoSettingsScanner(BaseScanner[DjangoSettingsOutput]):
    """Scanner for Django settings definitions and usages."""

    def __init__(self, verbose: bool = False):
        """Initialize Django settings scanner.

        Args:
            verbose: Enable verbose logging
        """
        super().__init__(verbose=verbose)
        self.current_file = ""

    def scan(self, path: Path) -> DjangoSettingsOutput:  # noqa: C901
        """Scan path for Django settings definitions and usages.

        Args:
            path: Directory or file to scan

        Returns:
            DjangoSettingsOutput with comprehensive setting information
        """
        start_time = time.perf_counter()

        # Collect definitions and usages
        definitions_by_setting: dict[str, dict[str, list[SettingDefinitionItem]]] = defaultdict(
            lambda: defaultdict(list)
        )
        usages_by_setting: dict[str, dict[str, list[SettingUsageItem]]] = defaultdict(lambda: defaultdict(list))

        files_scanned = 0

        # Scan all Python files
        python_files = self.get_files_to_scan(path)

        for file_path in python_files:
            self.current_file = str(file_path)
            files_scanned += 1

            # Check if this is a settings file
            is_settings_file = self._is_settings_file(file_path)

            # Parse the file
            try:
                module = self.parse_file(file_path)
                if not module:
                    continue

                relative_path = get_relative_path_str(file_path, path)

                # Extract definitions if this is a settings file
                if is_settings_file:
                    for node in module.nodes_of_class(nodes.Assign):
                        # Check for uppercase variable assignments
                        for target in node.targets:
                            if isinstance(target, nodes.AssignName) and target.name.isupper():
                                setting_name = target.name

                                # Try to infer value and type
                                value, type_str, statement = self._infer_value(node.value, setting_name)

                                definitions_by_setting[setting_name][relative_path].append(
                                    SettingDefinitionItem(
                                        value=value,
                                        statement=statement,
                                        lineno=node.lineno or 1,
                                        type=type_str,
                                    )
                                )

                # Scan for usages in all files
                for node in module.nodes_of_class(nodes.Attribute):
                    if is_settings_attribute_access(node):
                        setting_name = node.attrname
                        if setting_name and setting_name.isupper() and node.lineno:
                            # Get code context
                            try:
                                code_line = self._get_code_line(file_path, node.lineno)
                                usages_by_setting[setting_name][relative_path].append(
                                    SettingUsageItem(
                                        statement=code_line,
                                        lineno=node.lineno,
                                    )
                                )
                            except Exception:  # noqa: S110
                                pass

                # Check for getattr/hasattr calls
                for node in module.nodes_of_class(nodes.Call):
                    if (is_settings_getattr_call(node) or is_settings_hasattr_call(node)) and node.lineno:
                        setting_name = extract_setting_name(node)
                        if setting_name:
                            try:
                                code_line = self._get_code_line(file_path, node.lineno)
                                usages_by_setting[setting_name][relative_path].append(
                                    SettingUsageItem(
                                        statement=code_line,
                                        lineno=node.lineno,
                                    )
                                )
                            except Exception:  # noqa: S110
                                pass

            except Exception:
                if self.verbose:
                    logger.exception(f"Failed to scan file {file_path}")

        # Merge definitions and usages into SettingInfo
        all_settings = set(definitions_by_setting.keys()) | set(usages_by_setting.keys())
        results: dict[str, SettingInfo] = {}

        for setting_name in sorted(all_settings):
            definitions = definitions_by_setting.get(setting_name, {})
            usages = usages_by_setting.get(setting_name, {})

            # Collect type list
            type_set = set()
            for file_defs in definitions.values():
                for defn in file_defs:
                    type_set.add(defn.type)
            type_list = sorted(type_set)

            # Count totals
            definition_count = sum(len(defs) for defs in definitions.values())
            usage_count = sum(len(uses) for uses in usages.values())

            results[setting_name] = SettingInfo(
                definition_count=definition_count,
                usage_count=usage_count,
                type_list=type_list,
                definitions=dict(definitions),
                usages=dict(usages),
            )

        # Create summary
        total_definitions = sum(info.definition_count for info in results.values())
        total_usages = sum(info.usage_count for info in results.values())
        scan_duration_ms = int((time.perf_counter() - start_time) * 1000)

        summary = DjangoSettingsSummary(
            total_count=len(results),
            files_scanned=files_scanned,
            scan_duration_ms=scan_duration_ms,
            total_settings=len(results),
            total_definitions=total_definitions,
            total_usages=total_usages,
        )

        return DjangoSettingsOutput(
            summary=summary,
            results=results,
            metadata={"scanner_name": "django-settings"},
        )

    def _is_settings_file(self, file_path: Path) -> bool:
        """Check if a file is likely a Django settings file.

        Args:
            file_path: Path to check

        Returns:
            True if file is likely a settings file
        """
        path_str = str(file_path).lower()
        return "settings" in path_str or "config" in path_str

    def _extract_value(self, node: nodes.NodeNG) -> Any:
        """Extract value from an AST node recursively.

        Args:
            node: The AST node to extract value from

        Returns:
            Extracted value or None if cannot extract
        """
        try:
            # Handle constants
            if isinstance(node, nodes.Const):
                return node.value

            # Handle lists
            if isinstance(node, nodes.List):
                return [self._extract_value(elt) for elt in node.elts]

            # Handle tuples
            if isinstance(node, nodes.Tuple):
                return tuple(self._extract_value(elt) for elt in node.elts)

            # Handle dicts
            if isinstance(node, nodes.Dict):
                result = {}
                for key_node, value_node in node.items:
                    key = self._extract_value(key_node)
                    value = self._extract_value(value_node)
                    if key is not None:
                        result[key] = value
                return result

            # Handle sets
            if isinstance(node, nodes.Set):
                return {self._extract_value(elt) for elt in node.elts}

        except Exception:  # noqa: S110
            pass

        return None

    def _infer_value(self, value_node: nodes.NodeNG, var_name: str) -> tuple[Any, str, str]:
        """Infer value, type, and statement from an assignment node.

        Args:
            value_node: The AST node representing the value
            var_name: The variable name being assigned

        Returns:
            Tuple of (value, type_str, statement)
        """
        try:
            # Try to extract value directly
            extracted_value = self._extract_value(value_node)
            if extracted_value is not None:
                type_str = type(extracted_value).__name__
                statement = f"{var_name} = {extracted_value!r}"
                return extracted_value, type_str, statement

            # Try to infer the value
            inferred_values = list(value_node.infer())
            if inferred_values and len(inferred_values) == 1:
                inferred = inferred_values[0]

                # Handle concrete values
                if isinstance(inferred, nodes.Const):
                    value = inferred.value
                    type_str = type(value).__name__
                    statement = f"{var_name} = {value!r}"
                    return value, type_str, statement

                # Handle dicts
                if isinstance(inferred, nodes.Dict):
                    type_str = "dict"
                    statement = f"{var_name} = {{...}}"
                    return None, type_str, statement

        except Exception:  # noqa: S110
            pass

        # Fallback: dynamic/unknown
        type_str = "dynamic"
        statement = value_node.as_string()
        return None, type_str, statement

    def _get_code_line(self, file_path: Path, lineno: int) -> str:
        """Get a single line of code from file.

        Args:
            file_path: Path to file
            lineno: Line number (1-based)

        Returns:
            Code line as string
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                lines = f.readlines()
                if 1 <= lineno <= len(lines):
                    return lines[lineno - 1].strip()
        except Exception:  # noqa: S110
            pass
        return "..."
