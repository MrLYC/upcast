"""AST utilities for Django settings detection."""

from typing import Any

import astroid
from astroid import nodes

from upcast.common.ast_utils import infer_value_with_fallback
from upcast.django_settings_scanner.definition_parser import is_uppercase_identifier


def _check_inferred_types(node: nodes.Name) -> bool:
    """Check if inferred types match django.conf.settings.

    Args:
        node: Name node to check

    Returns:
        True if inferred type is django.conf.settings
    """
    try:
        for inferred in node.infer():
            # Check if it's the settings module from django.conf
            if isinstance(inferred, nodes.Module) and inferred.qname() == "django.conf.settings":
                return True
            # Check if it's a LazySettings instance from django.conf
            if isinstance(inferred, astroid.Instance) and inferred.qname() == "django.conf.LazySettings":
                return True
    except (astroid.InferenceError, AttributeError):
        pass
    return False


def _check_import_source(node: nodes.Name) -> bool:
    """Check if the name is imported from django.conf.

    Args:
        node: Name node to check

    Returns:
        True if imported from django.conf
    """
    try:
        # Get the module that contains this node
        module = node.root()
        if isinstance(module, nodes.Module):
            # Check imports for both direct and aliased imports
            for import_node in module.nodes_of_class(nodes.ImportFrom):
                if import_node.modname == "django.conf":
                    for name_info in import_node.names:
                        # Handle both tuple (name, alias) and plain string
                        if isinstance(name_info, tuple):
                            imported_name, alias = name_info
                            # Check if this is settings imported with an alias
                            if imported_name == "settings" and (
                                alias == node.name or (alias is None and node.name == "settings")
                            ):
                                return True
                        elif name_info == "settings" and node.name == "settings":
                            return True
    except Exception:  # noqa: S110
        pass
    return False


def is_django_settings(node: nodes.NodeNG) -> bool:
    """Check if a node refers to django.conf.settings.

    Args:
        node: The AST node to check

    Returns:
        True if the node refers to django.conf.settings
    """
    if not isinstance(node, nodes.Name):
        return False

    # Try type inference first
    if _check_inferred_types(node):
        return True

    # Fallback: check import source
    return _check_import_source(node)


def is_settings_attribute_access(node: nodes.NodeNG) -> bool:
    """Check if a node is an attribute access on settings (e.g., settings.KEY).

    Args:
        node: The AST node to check

    Returns:
        True if the node is settings.KEY pattern
    """
    if not isinstance(node, nodes.Attribute):
        return False

    try:
        # Check if the expr (object being accessed) is django settings
        if hasattr(node, "expr") and isinstance(node.expr, nodes.Name):
            return is_django_settings(node.expr)
    except (AttributeError, Exception):  # noqa: S110
        pass

    return False


def is_settings_getattr_call(node: nodes.NodeNG) -> bool:
    """Check if a node is a getattr call on settings.

    Args:
        node: The AST node to check

    Returns:
        True if the node is getattr(settings, "KEY") pattern
    """
    if not isinstance(node, nodes.Call):
        return False

    # Check if the function being called is 'getattr'
    if (
        isinstance(node.func, nodes.Name)
        and node.func.name == "getattr"
        and node.args
        and isinstance(node.args[0], nodes.Name)
    ):
        return is_django_settings(node.args[0])

    return False


def is_settings_hasattr_call(node: nodes.NodeNG) -> bool:
    """Check if a node is a hasattr call on settings.

    Args:
        node: The AST node to check

    Returns:
        True if the node is hasattr(settings, "KEY") pattern
    """
    if not isinstance(node, nodes.Call):
        return False

    # Check if the function being called is 'hasattr'
    if (
        isinstance(node.func, nodes.Name)
        and node.func.name == "hasattr"
        and node.args
        and isinstance(node.args[0], nodes.Name)
    ):
        return is_django_settings(node.args[0])

    return False


def extract_setting_name(node: nodes.NodeNG) -> str | None:
    """Extract the settings variable name from any pattern.

    Args:
        node: The AST node to extract from

    Returns:
        The settings variable name, or None if not extractable
    """
    # Pattern 1: Attribute access (settings.KEY)
    if isinstance(node, nodes.Attribute):
        # Only return uppercase attributes (Django settings convention)
        if is_uppercase_identifier(node.attrname):
            return node.attrname
        return None

    # Pattern 2 & 3: getattr/hasattr calls
    if isinstance(node, nodes.Call) and len(node.args) >= 2:
        key_arg = node.args[1]
        if isinstance(key_arg, nodes.Const) and isinstance(key_arg.value, str):
            # Only return uppercase setting names
            if is_uppercase_identifier(key_arg.value):
                return key_arg.value
            return None
        # Dynamic key (cannot resolve statically)
        return "DYNAMIC"

    return None


def extract_getattr_default(node: nodes.Call) -> Any:
    """Extract the default value from a getattr call.

    Args:
        node: The getattr Call node

    Returns:
        The default value (with backticks if inference failed), or None if not present
    """
    if not isinstance(node, nodes.Call):
        return None

    # getattr takes 2 or 3 arguments: getattr(obj, name[, default])
    if len(node.args) >= 3:
        default_arg = node.args[2]
        # Use common inference with fallback
        value, _success = infer_value_with_fallback(default_arg)
        return value

    return None


def resolve_relative_import(current_module: str, import_level: int, import_module: str | None) -> str:
    """Resolve a relative import to an absolute module path.

    Args:
        current_module: Current module path (e.g., "myproject.settings.dev")
        import_level: Number of dots in relative import (1 for ".", 2 for "..", etc.)
        import_module: Module name after dots (e.g., "base" in "from .base import *")

    Returns:
        Absolute module path

    Examples:
        >>> resolve_relative_import("myproject.settings.dev", 1, "base")
        "myproject.settings.base"
        >>> resolve_relative_import("myproject.settings.dev", 2, "config")
        "myproject.config"
        >>> resolve_relative_import("myproject.settings.dev", 1, None)
        "myproject.settings"
    """
    # Split current module into parts
    parts = current_module.split(".")

    # import_level indicates how many levels up to go
    # Level 1 = current package (remove module name, keep package)
    # Level 2 = parent package (remove module name + 1 level)
    # etc.

    # We need to go up import_level levels from current position
    # Current module is at depth len(parts), we go up import_level
    levels_to_keep = len(parts) - import_level

    # Too many levels up - just return what we can
    base_parts = [] if levels_to_keep < 0 else parts[:levels_to_keep]

    # Add the import module name if provided
    if import_module:
        base_parts.append(import_module)

    return ".".join(base_parts) if base_parts else import_module or ""
