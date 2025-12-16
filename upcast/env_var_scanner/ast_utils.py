"""AST utility functions for environment variable detection."""

from typing import Any, Optional, Union

from astroid import nodes


def is_env_var_call(node: Union[nodes.Call, nodes.NodeNG]) -> bool:
    """Check if a Call node represents an environment variable access pattern.

    Args:
        node: An astroid Call node

    Returns:
        True if the node matches an env var pattern
    """
    if not isinstance(node, nodes.Call):
        return False

    try:
        func_str = safe_as_string(node.func)

        # Check for common patterns
        patterns = [
            "os.getenv",
            "os.environ.get",
            "getenv",
            "env",
            "environ.get",
        ]

        for pattern in patterns:
            if pattern in func_str:
                return True

        # Check for django-environ typed methods (env.str, env.int, etc.)
        if "env." in func_str and any(
            type_method in func_str
            for type_method in [".str(", ".int(", ".bool(", ".float(", ".list(", ".dict(", ".json("]
        ):
            return True

    except Exception:  # noqa: S110
        pass

    return False


def infer_type_from_value(node: Union[nodes.NodeNG, list[nodes.NodeNG]]) -> Optional[str]:  # noqa: C901
    """Infer Python type from an AST value node.

    Args:
        node: An astroid node representing a value

    Returns:
        Type name as string ('str', 'int', 'bool', etc.) or None
    """
    if isinstance(node, list):
        return None

    try:
        # Try direct Const node
        if isinstance(node, nodes.Const):
            value = node.value
            if isinstance(value, bool):
                return "bool"
            elif isinstance(value, int):
                return "int"
            elif isinstance(value, float):
                return "float"
            elif isinstance(value, str):
                return "str"
            elif value is None:
                return None

        # Try astroid inference
        inferred_list = list(node.infer())
        if inferred_list and len(inferred_list) == 1:
            inferred = inferred_list[0]
            if isinstance(inferred, nodes.Const):
                value = inferred.value
                if isinstance(value, bool):
                    return "bool"
                elif isinstance(value, int):
                    return "int"
                elif isinstance(value, float):
                    return "float"
                elif isinstance(value, str):
                    return "str"
    except Exception:  # noqa: S110
        pass

    return None


def infer_literal_value(node: Union[nodes.NodeNG, list[nodes.NodeNG]]) -> Any:
    """Extract literal value from an AST node.

    Args:
        node: An astroid node representing a literal or constant

    Returns:
        Python literal value or string representation as fallback
    """
    if isinstance(node, list):
        return ""

    try:
        # Try to infer the value
        inferred_list = list(node.infer())

        # Skip if inference failed or returned multiple values
        if not inferred_list or len(inferred_list) != 1:
            return safe_as_string(node)

        inferred_value = inferred_list[0]

        # Handle Uninferable nodes
        if inferred_value.__class__.__name__ in ("Uninferable", "UninferableBase"):
            return safe_as_string(node)

        # Handle Const nodes (strings, numbers, booleans, None)
        if isinstance(inferred_value, nodes.Const):
            return inferred_value.value

        # For other types, fall back to string
        return safe_as_string(node)

    except Exception:
        # On any error, fall back to string representation
        return safe_as_string(node)


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
        String representation, or empty string on failure
    """
    if isinstance(node, list):
        return ""

    try:
        return node.as_string()
    except Exception:
        return ""
