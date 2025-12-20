"""View reference resolution utilities."""

import sys
from typing import Any

from astroid import InferenceError, Uninferable, nodes


def resolve_view(  # noqa: C901
    view_node: nodes.NodeNG, module_context: nodes.Module, verbose: bool = False
) -> dict[str, Any]:
    """Resolve a view reference to its module and name.

    Handles various view types:
    - Direct function references: views.index
    - Class-based views: MyView.as_view()
    - functools.partial wrapped views
    - Conditional expressions

    Args:
        view_node: AST node representing the view reference
        module_context: The module containing the URL pattern
        verbose: Enable verbose output

    Returns:
        Dictionary with:
        - view_module: Full module path where view is defined
        - view_name: Function or class name
        - description: Docstring from view (if available)
        - resolved: Whether resolution was successful
        - is_partial: Whether view is wrapped with functools.partial
        - is_conditional: Whether view is a conditional expression
    """
    result: dict[str, Any] = {
        "view_module": None,
        "view_name": None,
        "description": None,
        "resolved": False,
        "is_partial": False,
        "is_conditional": False,
    }

    try:
        # Handle .as_view() calls
        if isinstance(view_node, nodes.Call):
            if isinstance(view_node.func, nodes.Attribute) and view_node.func.attrname == "as_view":
                # Class-based view: MyView.as_view()
                return _resolve_as_view_call(view_node.func.expr, module_context, verbose)
            elif _is_partial_call(view_node):
                # functools.partial wrapped view
                result["is_partial"] = True
                if view_node.args:
                    # Resolve the first argument (the wrapped view)
                    wrapped_result = resolve_view(view_node.args[0], module_context, verbose)
                    result.update(wrapped_result)
                    return result
            else:
                # Some other call - try to resolve it
                return _resolve_callable(view_node, module_context, verbose)

        # Handle conditional expressions
        if isinstance(view_node, nodes.IfExp):
            result["is_conditional"] = True
            # Try to resolve the true branch
            true_result = resolve_view(view_node.body, module_context, verbose)
            result.update(true_result)
            return result

        # Handle attribute access (e.g., views.index)
        if isinstance(view_node, nodes.Attribute):
            return _resolve_attribute(view_node, module_context, verbose)

        # Handle name references
        if isinstance(view_node, nodes.Name):
            return _resolve_name(view_node, module_context, verbose)

        # Unknown node type
        if verbose:
            print(f"  Warning: Unknown view node type: {type(view_node).__name__}", file=sys.stderr)

    except InferenceError as e:
        if verbose:
            print(f"  Warning: Could not infer view: {e}", file=sys.stderr)
    except Exception as e:
        if verbose:
            print(f"  Warning: Error resolving view: {e}", file=sys.stderr)

    return result


def _resolve_as_view_call(
    class_node: nodes.NodeNG, module_context: nodes.Module, verbose: bool = False
) -> dict[str, Any]:
    """Resolve a class-based view .as_view() call.

    Args:
        class_node: The node before .as_view()
        module_context: The module context
        verbose: Enable verbose output

    Returns:
        Resolved view information
    """
    result: dict[str, Any] = {
        "view_module": None,
        "view_name": None,
        "description": None,
        "resolved": False,
    }

    try:
        # Try to infer the class
        inferred = next(class_node.infer(), Uninferable)
        if inferred is not Uninferable and isinstance(inferred, nodes.ClassDef):
            result["view_module"] = inferred.root().qname()
            result["view_name"] = inferred.name
            result["description"] = inferred.doc_node.value if inferred.doc_node else None
            result["resolved"] = True
    except (InferenceError, StopIteration):
        # Fall back to extracting from node structure
        if isinstance(class_node, nodes.Attribute):
            result["view_name"] = class_node.attrname
            # Try to get module from the expression
            if isinstance(class_node.expr, nodes.Name):
                result["view_module"] = f"<unresolved>.{class_node.expr.name}"
        elif isinstance(class_node, nodes.Name):
            result["view_name"] = class_node.name

    return result


def _resolve_attribute(
    attr_node: nodes.Attribute, module_context: nodes.Module, verbose: bool = False
) -> dict[str, Any]:
    """Resolve an attribute access like views.index.

    Args:
        attr_node: Attribute node
        module_context: The module context
        verbose: Enable verbose output

    Returns:
        Resolved view information
    """
    result: dict[str, Any] = {
        "view_module": None,
        "view_name": None,
        "description": None,
        "resolved": False,
    }

    try:
        # Try to infer the target
        inferred = next(attr_node.infer(), Uninferable)
        if inferred is not Uninferable and isinstance(inferred, (nodes.FunctionDef, nodes.ClassDef)):
            result["view_module"] = inferred.root().qname()
            result["view_name"] = inferred.name
            result["description"] = inferred.doc_node.value if inferred.doc_node else None
            result["resolved"] = True
    except (InferenceError, StopIteration):
        # Fall back to extracting from node structure
        result["view_name"] = attr_node.attrname
        if isinstance(attr_node.expr, nodes.Name):
            # views.index -> try to resolve 'views' import
            module_name = _resolve_import_name(attr_node.expr.name, module_context)
            if module_name:
                result["view_module"] = module_name

    return result


def _resolve_name(name_node: nodes.Name, module_context: nodes.Module, verbose: bool = False) -> dict[str, Any]:
    """Resolve a simple name reference.

    Args:
        name_node: Name node
        module_context: The module context
        verbose: Enable verbose output

    Returns:
        Resolved view information
    """
    result: dict[str, Any] = {
        "view_module": None,
        "view_name": None,
        "description": None,
        "resolved": False,
    }

    try:
        inferred = next(name_node.infer(), Uninferable)
        if inferred is not Uninferable and isinstance(inferred, (nodes.FunctionDef, nodes.ClassDef)):
            result["view_module"] = inferred.root().qname()
            result["view_name"] = inferred.name
            result["description"] = inferred.doc_node.value if inferred.doc_node else None
            result["resolved"] = True
    except (InferenceError, StopIteration):
        result["view_name"] = name_node.name

    return result


def _resolve_callable(call_node: nodes.Call, module_context: nodes.Module, verbose: bool = False) -> dict[str, Any]:
    """Resolve a generic callable.

    Args:
        call_node: Call node
        module_context: The module context
        verbose: Enable verbose output

    Returns:
        Resolved view information
    """
    # Try to resolve the function being called
    if isinstance(call_node.func, nodes.Attribute):
        return _resolve_attribute(call_node.func, module_context, verbose)
    elif isinstance(call_node.func, nodes.Name):
        return _resolve_name(call_node.func, module_context, verbose)

    return {
        "view_module": None,
        "view_name": None,
        "description": None,
        "resolved": False,
    }


def _is_partial_call(call_node: nodes.Call) -> bool:
    """Check if a call is functools.partial.

    Args:
        call_node: Call node to check

    Returns:
        True if this is a functools.partial call
    """
    if isinstance(call_node.func, nodes.Attribute):
        return call_node.func.attrname == "partial"
    elif isinstance(call_node.func, nodes.Name):
        return call_node.func.name == "partial"
    return False


def _resolve_import_name(name: str, module_context: nodes.Module) -> str | None:
    """Resolve an imported name to its full module path.

    Args:
        name: The imported name
        module_context: The module containing the import

    Returns:
        Full module path or None if not found
    """
    try:
        # Look for imports in the module
        for import_node in module_context.nodes_of_class(nodes.Import):
            for import_name, alias in import_node.names:
                if (alias and alias == name) or (not alias and import_name == name):
                    return import_name

        for import_from in module_context.nodes_of_class(nodes.ImportFrom):
            if import_from.modname:
                for import_name, alias in import_from.names:
                    if (alias and alias == name) or (not alias and import_name == name):
                        return f"{import_from.modname}.{import_name}"
    except Exception:  # noqa: S110
        pass

    return None
