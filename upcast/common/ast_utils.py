"""Unified AST inference utilities with fallback handling."""

from typing import Any

from astroid import nodes
from astroid.exceptions import InferenceError

from upcast.common.inference import infer_value


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

    except (InferenceError, AttributeError, StopIteration):
        return f"`{safe_as_string(node)}`", False


def find_function_calls(module: nodes.Module, function_names: set[str] | None = None) -> list[nodes.Call]:
    """Find all function call nodes in a module, optionally filtered by function names.

    Args:
        module: Astroid module to search
        function_names: Optional set of function names to match (e.g., {"sleep", "getenv"}).
                       If None, returns all Call nodes.

    Returns:
        List of Call nodes matching the criteria

    Examples:
        >>> calls = find_function_calls(module, {"sleep", "time.sleep"})
        >>> len(calls)
        5
    """
    matching_calls = []

    for call_node in module.nodes_of_class(nodes.Call):
        if function_names is None:
            # Return all calls if no filter
            matching_calls.append(call_node)
        else:
            # Try to get the function name being called
            func_name = safe_as_string(call_node.func)
            # Check if it matches any of the target names
            if func_name in function_names or any(func_name.endswith(f".{name}") for name in function_names):
                matching_calls.append(call_node)

    return matching_calls


def extract_decorator_info(  # noqa: C901
    node: nodes.FunctionDef | nodes.ClassDef,
) -> list[dict[str, Any]]:
    """Extract decorator information from a function or class definition.

    Args:
        node: Function or class definition node

    Returns:
        List of decorator dictionaries with keys:
        - 'name': decorator name (str)
        - 'args': positional arguments (list)
        - 'kwargs': keyword arguments (dict)
        - 'raw': raw decorator expression (str)

    Examples:
        >>> decorators = extract_decorator_info(function_node)
        >>> decorators[0]
        {'name': 'receiver', 'args': ['post_save'], 'kwargs': {'sender': 'User'}, 'raw': '@receiver(post_save, sender=User)'}
    """
    decorators = []

    if not hasattr(node, "decorators") or node.decorators is None:
        return decorators

    for decorator in node.decorators.nodes:
        dec_info: dict[str, Any] = {
            "name": "",
            "args": [],
            "kwargs": {},
            "raw": safe_as_string(decorator),
        }

        # Extract decorator name
        if isinstance(decorator, nodes.Name):
            dec_info["name"] = decorator.name
        elif isinstance(decorator, nodes.Attribute):
            dec_info["name"] = safe_as_string(decorator)
        elif isinstance(decorator, nodes.Call):
            # Decorator with arguments
            if isinstance(decorator.func, nodes.Name):
                dec_info["name"] = decorator.func.name
            elif isinstance(decorator.func, nodes.Attribute):
                dec_info["name"] = safe_as_string(decorator.func)

            # Extract positional arguments
            if hasattr(decorator, "args"):
                for arg in decorator.args:
                    result = infer_value(arg)
                    value = result.value if result.confidence == "exact" else f"`{safe_as_string(arg)}`"
                    dec_info["args"].append(value)

            # Extract keyword arguments
            if hasattr(decorator, "keywords"):
                for keyword in decorator.keywords:
                    key = keyword.arg
                    result = infer_value(keyword.value)
                    value = result.value if result.confidence == "exact" else f"`{safe_as_string(keyword.value)}`"
                    if key:
                        dec_info["kwargs"][key] = value

        decorators.append(dec_info)

    return decorators


def get_import_info(module: nodes.Module) -> dict[str, str]:
    """Extract import information from a module.

    Creates a mapping from local names (aliases or original names) to
    their fully qualified module paths.

    Args:
        module: Astroid module to extract imports from

    Returns:
        Dictionary mapping local name to qualified module path
        Examples: {'sleep': 'time', 'np': 'numpy', 'timezone': 'django.utils.timezone'}

    Examples:
        >>> imports = get_import_info(module)
        >>> imports['sleep']
        'time'
        >>> imports['np']
        'numpy'
    """
    import_map: dict[str, str] = {}

    # Handle 'import x' and 'import x as y'
    for import_node in module.nodes_of_class(nodes.Import):
        for module_name, alias in import_node.names:
            local_name = alias if alias else module_name
            import_map[local_name] = module_name

    # Handle 'from x import y' and 'from x import y as z'
    for import_from in module.nodes_of_class(nodes.ImportFrom):
        module_name = import_from.modname or ""
        for item_name, alias in import_from.names:
            local_name = alias if alias else item_name
            # Build full qualified name
            if module_name:
                qualified = f"{module_name}.{item_name}" if item_name != "*" else module_name
            else:
                qualified = item_name
            import_map[local_name] = qualified

    return import_map
