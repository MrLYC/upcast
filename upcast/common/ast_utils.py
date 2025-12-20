"""Unified AST inference utilities with fallback handling."""

from typing import Any

import astroid
from astroid import nodes


def safe_as_string(node: Any) -> str:
    """Safely convert an astroid node or value to string representation.

    Args:
        node: Astroid node or any value to convert

    Returns:
        String representation
    """
    if isinstance(node, nodes.NodeNG):
        try:
            return node.as_string()
        except Exception:
            return ""
    return str(node)


def infer_value_with_fallback(node: nodes.NodeNG) -> tuple[Any, bool]:  # noqa: C901
    """Infer literal value from node with explicit fallback.

    When inference fails, wraps the expression in backticks for clarity.

    Args:
        node: Astroid node to infer

    Returns:
        Tuple of (value, success_flag):
        - If successful: (literal_value, True)
        - If failed: (`expression`, False)

    Examples:
        >>> infer_value_with_fallback(Const(42))
        (42, True)
        >>> infer_value_with_fallback(Name("unknown_var"))
        ('`unknown_var`', False)
    """
    try:
        inferred_list = list(node.infer())

        # Check for inference failure
        if not inferred_list or len(inferred_list) != 1:
            return f"`{safe_as_string(node)}`", False

        inferred = inferred_list[0]

        # Check for Uninferable
        if inferred is astroid.Uninferable or inferred.__class__.__name__ in (
            "Uninferable",
            "UninferableBase",
        ):
            return f"`{safe_as_string(node)}`", False

        # Handle Const nodes (literals)
        if isinstance(inferred, nodes.Const):
            return inferred.value, True

        # Handle List nodes recursively
        if isinstance(inferred, nodes.List):
            result = []
            all_success = True
            for elem in inferred.elts:
                if isinstance(elem, nodes.NodeNG):
                    val, success = infer_value_with_fallback(elem)
                    result.append(val)
                    all_success = all_success and success
                else:
                    result.append(f"`{safe_as_string(elem)}`")
                    all_success = False
            return result, all_success

        # Handle Tuple nodes recursively
        if isinstance(inferred, nodes.Tuple):
            result = []
            all_success = True
            for elem in inferred.elts:
                if isinstance(elem, nodes.NodeNG):
                    val, success = infer_value_with_fallback(elem)
                    result.append(val)
                    all_success = all_success and success
                else:
                    result.append(f"`{safe_as_string(elem)}`")
                    all_success = False
            return tuple(result), all_success

        # Handle Dict nodes recursively
        if isinstance(inferred, nodes.Dict):
            result = {}
            all_success = True
            for key_node, value_node in inferred.items:
                if isinstance(key_node, nodes.NodeNG) and isinstance(value_node, nodes.NodeNG):
                    key, key_success = infer_value_with_fallback(key_node)
                    val, val_success = infer_value_with_fallback(value_node)

                    # Only add if key is hashable
                    if isinstance(key, (str, int, float, bool, type(None))):
                        result[key] = val
                        all_success = all_success and key_success and val_success
            return result, all_success

        # For other types, fallback to string
        return f"`{safe_as_string(node)}`", False

    except (astroid.InferenceError, StopIteration, AttributeError):
        return f"`{safe_as_string(node)}`", False


def infer_type_with_fallback(node: nodes.NodeNG) -> tuple[str, bool]:  # noqa: C901
    """Infer Python type from node with fallback to 'unknown'.

    Args:
        node: Astroid node to infer type from

    Returns:
        Tuple of (type_name, success_flag):
        - If successful: ("int"|"str"|"bool"|"float"|..., True)
        - If failed: ("unknown", False)

    Examples:
        >>> infer_type_with_fallback(Const(42))
        ('int', True)
        >>> infer_type_with_fallback(Call(...))
        ('unknown', False)
    """
    try:
        # Try direct Const node first
        if isinstance(node, nodes.Const):
            value = node.value
            if isinstance(value, bool):
                return "bool", True
            elif isinstance(value, int):
                return "int", True
            elif isinstance(value, float):
                return "float", True
            elif isinstance(value, str):
                return "str", True
            elif value is None:
                return "None", True

        # Try astroid inference
        inferred_list = list(node.infer())

        if inferred_list and len(inferred_list) == 1:
            inferred = inferred_list[0]

            if isinstance(inferred, nodes.Const):
                value = inferred.value
                if isinstance(value, bool):
                    return "bool", True
                elif isinstance(value, int):
                    return "int", True
                elif isinstance(value, float):
                    return "float", True
                elif isinstance(value, str):
                    return "str", True
                elif value is None:
                    return "None", True
        else:
            return "unknown", False

    except (astroid.InferenceError, StopIteration, AttributeError):
        return "unknown", False


def get_qualified_name(node: nodes.NodeNG) -> tuple[str, bool]:
    """Get fully qualified name for a class or function.

    Args:
        node: Astroid ClassDef, FunctionDef, or other node

    Returns:
        Tuple of (qualified_name, success_flag):
        - If successful: ("module.path.ClassName", True)
        - If failed: ("`node.as_string()`", False)

    Examples:
        >>> get_qualified_name(CharField_node)
        ('django.db.models.fields.CharField', True)
        >>> get_qualified_name(unknown_node)
        ('`UnknownType`', False)
    """
    try:
        # For ClassDef and FunctionDef, use qname
        if hasattr(node, "qname"):
            qname = node.qname()
            if qname and qname != "":
                return qname, True

        # Try inference for other node types
        inferred_list = list(node.infer())

        if inferred_list and len(inferred_list) == 1:
            inferred = inferred_list[0]
            if hasattr(inferred, "qname"):
                qname = inferred.qname()
                if qname and qname != "":
                    return qname, True

        # Fallback
        return f"`{safe_as_string(node)}`", False

    except (astroid.InferenceError, AttributeError, StopIteration):
        return f"`{safe_as_string(node)}`", False
