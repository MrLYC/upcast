"""Settings usage parsing and data structures."""

from dataclasses import dataclass, field
from pathlib import Path

from astroid import nodes

from upcast.django_settings_scanner.ast_utils import (
    extract_setting_name,
)


@dataclass
class SettingsUsage:
    """Represents a single usage of a Django settings variable."""

    file: str  # Relative path from project root
    line: int  # Line number (1-based)
    column: int  # Column number (0-based)
    pattern: str  # "attribute_access" | "getattr" | "hasattr"
    code: str  # Source code snippet


@dataclass
class SettingsVariable:
    """Represents all usages of a Django settings variable."""

    name: str  # Variable name (e.g., "DATABASES")
    count: int  # Total usage count
    locations: list[SettingsUsage] = field(default_factory=list)  # All usages


def _extract_source_code_snippet(node: nodes.NodeNG) -> str:
    """Extract source code snippet from an AST node.

    Args:
        node: The AST node

    Returns:
        Source code string
    """
    try:
        return node.as_string()
    except Exception:
        return "<unknown>"


def parse_settings_attribute(node: nodes.Attribute, base_path: str, file_path: str) -> SettingsUsage | None:
    """Parse an attribute access pattern (settings.KEY).

    Args:
        node: The Attribute node
        base_path: Project root path
        file_path: Absolute file path

    Returns:
        SettingsUsage object or None if parsing fails
    """
    setting_name = extract_setting_name(node)
    if not setting_name:
        return None

    try:
        rel_path = Path(file_path).relative_to(base_path)
    except ValueError:
        rel_path = Path(file_path).name

    return SettingsUsage(
        file=str(rel_path),
        line=node.lineno,
        column=node.col_offset,
        pattern="attribute_access",
        code=_extract_source_code_snippet(node),
    )


def parse_settings_getattr(node: nodes.Call, base_path: str, file_path: str) -> SettingsUsage | None:
    """Parse a getattr call pattern (getattr(settings, "KEY")).

    Args:
        node: The Call node
        base_path: Project root path
        file_path: Absolute file path

    Returns:
        SettingsUsage object or None if parsing fails
    """
    setting_name = extract_setting_name(node)
    if not setting_name:
        return None

    try:
        rel_path = Path(file_path).relative_to(base_path)
    except ValueError:
        rel_path = Path(file_path).name

    return SettingsUsage(
        file=str(rel_path),
        line=node.lineno,
        column=node.col_offset,
        pattern="getattr",
        code=_extract_source_code_snippet(node),
    )


def parse_settings_hasattr(node: nodes.Call, base_path: str, file_path: str) -> SettingsUsage | None:
    """Parse a hasattr call pattern (hasattr(settings, "KEY")).

    Args:
        node: The Call node
        base_path: Project root path
        file_path: Absolute file path

    Returns:
        SettingsUsage object or None if parsing fails
    """
    setting_name = extract_setting_name(node)
    if not setting_name:
        return None

    try:
        rel_path = Path(file_path).relative_to(base_path)
    except ValueError:
        rel_path = Path(file_path).name

    return SettingsUsage(
        file=str(rel_path),
        line=node.lineno,
        column=node.col_offset,
        pattern="hasattr",
        code=_extract_source_code_snippet(node),
    )


def parse_settings_usage(node: nodes.NodeNG, base_path: str, file_path: str) -> SettingsUsage | None:
    """Parse any settings usage pattern into SettingsUsage.

    Args:
        node: The AST node
        base_path: Project root path
        file_path: Absolute file path

    Returns:
        SettingsUsage object or None if not a valid pattern
    """
    if isinstance(node, nodes.Attribute):
        return parse_settings_attribute(node, base_path, file_path)
    elif isinstance(node, nodes.Call) and isinstance(node.func, nodes.Name):
        # Determine if it's getattr or hasattr
        if node.func.name == "getattr":
            return parse_settings_getattr(node, base_path, file_path)
        elif node.func.name == "hasattr":
            return parse_settings_hasattr(node, base_path, file_path)

    return None
