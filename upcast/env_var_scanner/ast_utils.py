"""AST utility functions for environment variable detection."""

from typing import Any, Optional, Union

from astroid import nodes

from upcast.common.ast_utils import (
    infer_type_with_fallback,
    infer_value_with_fallback,
)
from upcast.common.ast_utils import (
    safe_as_string as common_safe_as_string,
)


def is_env_var_call(node: Union[nodes.Call, nodes.NodeNG]) -> bool:  # noqa: C901
    """Check if a Call node represents an environment variable access pattern.

    Uses precise AST analysis to avoid false positives like request.headers.get().

    Args:
        node: An astroid Call node

    Returns:
        True if the node matches an env var pattern
    """
    if not isinstance(node, nodes.Call):
        return False

    try:
        func = node.func

        # Pattern: getenv(...) - direct name reference
        if isinstance(func, nodes.Name) and func.name == "getenv":
            return True

        # Pattern: env(...) - direct name reference (django-environ)
        if isinstance(func, nodes.Name) and func.name == "env":
            return True

        # Pattern: os.getenv(...) or environ.get(...) or env.str(...)
        if isinstance(func, nodes.Attribute):
            attr_name = func.attrname

            # Get the object being accessed (use expr, not value)
            expr = func.expr

            # Pattern: os.getenv
            if isinstance(expr, nodes.Name):
                if expr.name == "os" and attr_name == "getenv":
                    return True
                # Pattern: environ.get
                if expr.name == "environ" and attr_name == "get":
                    return True
                # Pattern: env.str, env.int, etc. (django-environ)
                if expr.name == "env" and attr_name in (
                    "str",
                    "int",
                    "bool",
                    "float",
                    "list",
                    "dict",
                    "json",
                    "url",
                    "db",
                ):
                    return True

            # Pattern: os.environ.get
            if isinstance(expr, nodes.Attribute) and expr.attrname == "environ" and attr_name == "get":
                inner_expr = expr.expr
                if isinstance(inner_expr, nodes.Name) and inner_expr.name == "os":
                    return True

    except Exception:  # noqa: S110
        pass

    return False


def infer_type_from_value(node: Union[nodes.NodeNG, list[nodes.NodeNG]]) -> Optional[str]:
    """Infer Python type from an AST value node.

    Args:
        node: An astroid node representing a value

    Returns:
        Type name as string ('str', 'int', 'bool', etc.) or None
    """
    if isinstance(node, list):
        return None

    # Use common inference with fallback
    type_name, success = infer_type_with_fallback(node)

    # Return None for "unknown" type or "None" type
    if not success or type_name in ("unknown", "None"):
        return None

    return type_name


def infer_literal_value(node: Union[nodes.NodeNG, list[nodes.NodeNG]]) -> Any:
    """Extract literal value from an AST node.

    Args:
        node: An astroid node representing a literal or constant

    Returns:
        Python literal value or string representation with backticks on failure
    """
    if isinstance(node, list):
        return ""

    # Use common inference with fallback
    value, _ = infer_value_with_fallback(node)

    # Return value (will be wrapped in backticks if inference failed)
    return value


def resolve_string_concat(node: Union[nodes.NodeNG, list[nodes.NodeNG]]) -> Optional[str]:
    """Resolve string concatenation expressions to their literal result.

    Args:
        node: An astroid node that may contain string concatenation

    Returns:
        Resolved string value or None if cannot resolve
    """
    if isinstance(node, list):
        return None

    try:
        # Try to infer the concatenated result
        inferred_list = list(node.infer())

        if inferred_list and len(inferred_list) == 1:
            inferred = inferred_list[0]
            if isinstance(inferred, nodes.Const) and isinstance(inferred.value, str):
                return inferred.value
    except Exception:  # noqa: S110
        pass

    return None


def safe_as_string(node: Union[nodes.NodeNG, list[nodes.NodeNG]]) -> str:
    """Safely convert an astroid node to string representation.

    Args:
        node: Astroid node to convert

    Returns:
        String representation
    """
    return common_safe_as_string(node)
