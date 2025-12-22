"""Django settings scanner.

This scanner analyzes Django settings files and their usage across the project.
It can scan for both settings definitions and settings usages.
"""

import logging
import time
from pathlib import Path

from astroid import nodes

from upcast.common.django.settings_parser import is_settings_module, parse_settings_module
from upcast.common.django.settings_utils import (
    extract_setting_name,
    is_settings_attribute_access,
    is_settings_getattr_call,
    is_settings_hasattr_call,
)
from upcast.common.scanner_base import BaseScanner
from upcast.models.django_settings import (
    DjangoSettingsDefinitionOutput,
    DjangoSettingsSummary,
    DjangoSettingsUsageOutput,
    SettingsLocation,
    SettingsModule,
    SettingsUsage,
)

logger = logging.getLogger(__name__)


class DjangoSettingsScanner(BaseScanner[DjangoSettingsUsageOutput]):
    """Scanner for Django settings usage."""

    def __init__(
        self,
        scan_mode: str = "usage",
        verbose: bool = False,
    ):
        """Initialize Django settings scanner.

        Args:
            scan_mode: "usage" to scan for settings usages, "definitions" for settings definitions
            verbose: Enable verbose logging
        """
        super().__init__(verbose=verbose)
        self.scan_mode = scan_mode
        self.current_file = ""

    def scan(self, path: Path) -> DjangoSettingsUsageOutput | DjangoSettingsDefinitionOutput:
        """Scan path for Django settings.

        Args:
            path: Directory or file to scan

        Returns:
            DjangoSettingsUsageOutput or DjangoSettingsDefinitionOutput
        """
        start_time = time.perf_counter()

        result = self._scan_definitions(path) if self.scan_mode == "definitions" else self._scan_usages(path)

        scan_duration_ms = int((time.perf_counter() - start_time) * 1000)

        # Create a new result with updated scan_duration_ms (models are frozen)
        if self.scan_mode == "definitions":
            summary = DjangoSettingsSummary(
                total_count=result.summary.total_count,
                files_scanned=result.summary.files_scanned,
                scan_duration_ms=scan_duration_ms,
                total_settings=result.summary.total_settings,
                total_usages=result.summary.total_usages,
            )
            return DjangoSettingsDefinitionOutput(
                summary=summary,
                results=result.results,  # type: ignore[attr-defined]
            )
        else:
            summary = DjangoSettingsSummary(
                total_count=result.summary.total_count,
                files_scanned=result.summary.files_scanned,
                scan_duration_ms=scan_duration_ms,
                total_settings=result.summary.total_settings,
                total_usages=result.summary.total_usages,
            )
            return DjangoSettingsUsageOutput(
                summary=summary,
                results=result.results,  # type: ignore[attr-defined]
            )

        return result

    def _scan_usages(self, path: Path) -> DjangoSettingsUsageOutput:
        """Scan for settings usages.

        Args:
            path: Directory or file to scan

        Returns:
            DjangoSettingsUsageOutput
        """
        files = self.get_files_to_scan(path)
        settings_map: dict[str, SettingsUsage] = {}

        for file_path in files:
            # Skip settings modules when scanning for usages
            if is_settings_module(str(file_path)):
                continue

            usages = self._scan_file_for_usages(file_path, path)
            # Merge usages
            for setting_name, usage in usages.items():
                if setting_name not in settings_map:
                    settings_map[setting_name] = usage
                else:
                    settings_map[setting_name].count += usage.count
                    settings_map[setting_name].locations.extend(usage.locations)

        total_settings = len(settings_map)
        total_usages = sum(u.count for u in settings_map.values())

        summary = DjangoSettingsSummary(
            total_count=total_settings,
            files_scanned=len(files),
            scan_duration_ms=0,  # Will be updated
            total_settings=total_settings,
            total_usages=total_usages,
        )

        return DjangoSettingsUsageOutput(summary=summary, results=settings_map)

    def _scan_definitions(self, path: Path) -> DjangoSettingsDefinitionOutput:
        """Scan for settings definitions.

        Args:
            path: Directory or file to scan

        Returns:
            DjangoSettingsDefinitionOutput
        """
        files = self.get_files_to_scan(path)
        modules: dict[str, SettingsModule] = {}

        for file_path in files:
            if is_settings_module(str(file_path)):
                module = self._scan_file_for_definitions(file_path, path)
                if module:
                    # Use relative path as module key
                    try:
                        rel_path = file_path.relative_to(path)
                        module_key = str(rel_path).replace("/", ".").replace(".py", "")
                    except ValueError:
                        module_key = str(file_path)

                    modules[module_key] = module

        total_settings = sum(len(m.definitions) for m in modules.values())

        summary = DjangoSettingsSummary(
            total_count=total_settings,
            files_scanned=len(modules),
            scan_duration_ms=0,  # Will be updated
            total_settings=total_settings,
            total_usages=0,
        )

        return DjangoSettingsDefinitionOutput(summary=summary, results=modules)

    def _scan_file_for_usages(self, file_path: Path, base_path: Path) -> dict[str, SettingsUsage]:
        """Scan a file for settings usages.

        Args:
            file_path: Path to the file
            base_path: Base path for relative paths

        Returns:
            Dictionary of settings usages
        """
        module = self.parse_file(file_path)
        if not module:
            return {}

        self.current_file = str(file_path)
        settings_map: dict[str, SettingsUsage] = {}

        # Visit all nodes in the module
        self._visit_node(module, settings_map, file_path, base_path)

        if self.verbose and settings_map:
            logger.info(f"Found {len(settings_map)} settings in {file_path}")

        return settings_map

    def _visit_node(
        self, node: nodes.NodeNG, settings_map: dict[str, SettingsUsage], file_path: Path, base_path: Path
    ) -> None:
        """Recursively visit AST nodes to find settings usages.

        Args:
            node: The node to visit
            settings_map: Dictionary to store settings usages
            file_path: Current file path
            base_path: Base path for relative paths
        """
        # Check if it's an attribute access (settings.KEY)
        if isinstance(node, nodes.Attribute):
            if is_settings_attribute_access(node):
                setting_name = extract_setting_name(node)
                if setting_name:
                    self._register_usage(setting_name, node, settings_map, file_path, base_path, "attribute_access")

        # Check if it's a call (getattr/hasattr)
        elif isinstance(node, nodes.Call) and (is_settings_getattr_call(node) or is_settings_hasattr_call(node)):
            setting_name = extract_setting_name(node)
            if setting_name:
                pattern = "getattr" if is_settings_getattr_call(node) else "hasattr"
                self._register_usage(setting_name, node, settings_map, file_path, base_path, pattern)

        # Recursively visit child nodes
        for child in node.get_children():
            self._visit_node(child, settings_map, file_path, base_path)

    def _register_usage(
        self,
        setting_name: str,
        node: nodes.NodeNG,
        settings_map: dict[str, SettingsUsage],
        file_path: Path,
        base_path: Path,
        pattern: str,
    ) -> None:
        """Register a settings usage.

        Args:
            setting_name: The settings variable name
            node: The AST node
            settings_map: Dictionary to store settings usages
            file_path: Current file path
            base_path: Base path for relative paths
            pattern: Usage pattern
        """
        # Get relative path
        try:
            rel_path = file_path.relative_to(base_path)
            file_str = str(rel_path)
        except ValueError:
            file_str = str(file_path)

        # Extract code snippet
        code = self._extract_code_snippet(node)

        location = SettingsLocation(
            file=file_str,
            line=node.lineno or 1,
            column=node.col_offset,
            pattern=pattern,
            code=code,
        )

        if setting_name not in settings_map:
            settings_map[setting_name] = SettingsUsage(count=0, locations=[])

        settings_map[setting_name].count += 1
        settings_map[setting_name].locations.append(location)

    def _extract_code_snippet(self, node: nodes.NodeNG) -> str:
        """Extract source code snippet from an AST node.

        Args:
            node: The AST node

        Returns:
            Source code string
        """
        try:
            # Walk up AST to find containing statement
            current = node
            while current.parent:
                # Check if parent is a statement type
                if isinstance(
                    current.parent,
                    (
                        nodes.Assign,
                        nodes.AugAssign,
                        nodes.Expr,
                        nodes.Return,
                        nodes.If,
                    ),
                ):
                    return current.parent.as_string()
                current = current.parent

            # Fallback to original node
            return node.as_string()
        except Exception:
            return "<unknown>"

    def _scan_file_for_definitions(self, file_path: Path, base_path: Path) -> SettingsModule | None:
        """Scan a settings file for definitions.

        Args:
            file_path: Path to the settings file
            base_path: Base path for relative paths

        Returns:
            SettingsModule or None
        """
        try:
            # Parse settings module using the definition parser
            settings_module = parse_settings_module(str(file_path), str(base_path))

            # Convert to Pydantic model
            from upcast.models.django_settings import DynamicImport, SettingDefinition

            definitions = {}
            for name, defn in settings_module.definitions.items():
                definitions[name] = SettingDefinition(
                    value=defn.value if defn.type == "literal" else None,
                    statement=defn.value if defn.type != "literal" else None,
                    lineno=defn.line,
                    overrides=defn.overrides,
                )

            dynamic_imports = [
                DynamicImport(
                    pattern=di.pattern,
                    base_module=di.base_module,
                    file=di.file,
                    line=di.line,
                )
                for di in settings_module.dynamic_imports
            ]

            return SettingsModule(
                definitions=definitions,
                star_imports=settings_module.star_imports,
                dynamic_imports=dynamic_imports,
            )
        except Exception as e:
            if self.verbose:
                logger.warning(f"Failed to parse settings module {file_path}: {e}")
            return None
