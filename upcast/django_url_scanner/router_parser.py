"""DRF Router parsing utilities."""

from typing import Any

from astroid import InferenceError, Uninferable, nodes


def parse_router_registrations(module: nodes.Module, router_name: str) -> list[dict[str, Any]]:
    """Parse router.register() calls to extract ViewSet registrations.

    Args:
        module: The module containing router definitions
        router_name: Name of the router variable

    Returns:
        List of router registration dictionaries with pattern, viewset_module, viewset_name, basename
    """
    registrations = []

    # Find the router assignment
    router_type = _find_router_type(module, router_name)

    # Find all router.register() calls
    for call_node in module.nodes_of_class(nodes.Call):
        if _is_router_register_call(call_node, router_name):
            registration = _parse_register_call(call_node, module)
            if registration:
                registration["router_type"] = router_type
                registrations.append(registration)

    return registrations


def _find_router_type(module: nodes.Module, router_name: str) -> str | None:
    """Find the type of router (DefaultRouter, SimpleRouter, etc.).

    Args:
        module: The module to search
        router_name: Name of the router variable

    Returns:
        Router type name or None if not found
    """
    for assign_node in module.nodes_of_class(nodes.Assign):
        # Check if this assigns to the router variable and value is a router constructor call
        if any(
            isinstance(target, nodes.AssignName) and target.name == router_name for target in assign_node.targets
        ) and isinstance(assign_node.value, nodes.Call):
            func_name = None
            if isinstance(assign_node.value.func, nodes.Name):
                func_name = assign_node.value.func.name
            elif isinstance(assign_node.value.func, nodes.Attribute):
                func_name = assign_node.value.func.attrname

            if func_name and "Router" in func_name:
                return func_name

    return None


def _is_router_register_call(call_node: nodes.Call, router_name: str) -> bool:
    """Check if a call node is a router.register() call.

    Args:
        call_node: The call node to check
        router_name: Name of the router variable

    Returns:
        True if this is a router.register() call
    """
    if not isinstance(call_node.func, nodes.Attribute):
        return False

    if call_node.func.attrname != "register":
        return False

    if not isinstance(call_node.func.expr, nodes.Name):
        return False

    return call_node.func.expr.name == router_name


def _parse_register_call(call_node: nodes.Call, module: nodes.Module) -> dict[str, Any] | None:
    """Parse a router.register() call.

    Args:
        call_node: The register() call node
        module: The module context

    Returns:
        Dictionary with registration info or None
    """
    if not call_node.args or len(call_node.args) < 2:
        return None

    result: dict[str, Any] = {
        "type": "router_registration",
        "pattern": None,
        "viewset_module": None,
        "viewset_name": None,
        "basename": None,
    }

    # First argument: pattern prefix
    pattern_node = call_node.args[0]
    if isinstance(pattern_node, nodes.Const):
        result["pattern"] = pattern_node.value

    # Second argument: ViewSet class
    viewset_node = call_node.args[1]
    viewset_info = _resolve_viewset(viewset_node, module)
    result.update(viewset_info)

    # Third argument or basename keyword: basename
    if len(call_node.args) >= 3:
        basename_node = call_node.args[2]
        if isinstance(basename_node, nodes.Const):
            result["basename"] = basename_node.value

    # Check for basename keyword argument
    for keyword in call_node.keywords:
        if keyword.arg == "basename" and isinstance(keyword.value, nodes.Const):
            result["basename"] = keyword.value.value

    return result


def _resolve_viewset(viewset_node: nodes.NodeNG, module: nodes.Module) -> dict[str, Any]:
    """Resolve a ViewSet reference to its module and name.

    Args:
        viewset_node: The ViewSet node
        module: The module context

    Returns:
        Dictionary with viewset_module and viewset_name
    """
    result: dict[str, Any] = {
        "viewset_module": None,
        "viewset_name": None,
    }

    try:
        # Try to infer the ViewSet class
        if isinstance(viewset_node, nodes.Name):
            inferred = next(viewset_node.infer(), Uninferable)
            if inferred is not Uninferable and isinstance(inferred, nodes.ClassDef):
                result["viewset_module"] = inferred.root().qname()
                result["viewset_name"] = inferred.name
        elif isinstance(viewset_node, nodes.Attribute):
            # Handle imported ViewSet: from app.views import UserViewSet
            inferred = next(viewset_node.infer(), Uninferable)
            if inferred is not Uninferable and isinstance(inferred, nodes.ClassDef):
                result["viewset_module"] = inferred.root().qname()
                result["viewset_name"] = inferred.name
            else:
                # Fall back to node structure
                result["viewset_name"] = viewset_node.attrname
    except (InferenceError, StopIteration):
        # Fall back to extracting from node structure
        if isinstance(viewset_node, nodes.Name):
            result["viewset_name"] = viewset_node.name
        elif isinstance(viewset_node, nodes.Attribute):
            result["viewset_name"] = viewset_node.attrname

    return result
