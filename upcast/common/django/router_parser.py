"""DRF Router parsing utilities.

This module contains utilities for parsing Django REST Framework router registrations.
Extracted from django_url_scanner for reuse across scanners.
"""

from typing import Any

from astroid import InferenceError, Uninferable, nodes


def parse_router_registrations(
    module: nodes.Module, router_name: str, module_path: str | None = None
) -> list[dict[str, Any]]:
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
            registration = _parse_register_call(call_node, module, module_path)
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


def _parse_register_call(call_node: nodes.Call, module: nodes.Module, module_path: str | None) -> dict[str, Any] | None:
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
        "line": getattr(call_node, "lineno", None),
    }

    # First argument: pattern prefix
    pattern_node = call_node.args[0]
    if isinstance(pattern_node, nodes.Const):
        result["pattern"] = pattern_node.value

    # Second argument: ViewSet class
    viewset_node = call_node.args[1]
    viewset_info = _resolve_viewset(viewset_node, module, module_path)
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


def _resolve_viewset(viewset_node: nodes.NodeNG, module: nodes.Module, module_path: str | None) -> dict[str, Any]:
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
            else:
                result.update(_resolve_viewset_syntax(viewset_node, module, module_path))
        elif isinstance(viewset_node, nodes.Attribute):
            # Handle imported ViewSet: from app.views import UserViewSet
            inferred = next(viewset_node.infer(), Uninferable)
            if inferred is not Uninferable and isinstance(inferred, nodes.ClassDef):
                result["viewset_module"] = inferred.root().qname()
                result["viewset_name"] = inferred.name
            else:
                result.update(_resolve_viewset_syntax(viewset_node, module, module_path))
    except (InferenceError, StopIteration):
        result.update(_resolve_viewset_syntax(viewset_node, module, module_path))

    return result


def _resolve_viewset_syntax(
    viewset_node: nodes.Name | nodes.Attribute, module: nodes.Module, module_path: str | None
) -> dict[str, str | None]:
    """Resolve common import syntax when astroid inference has no context."""
    if isinstance(viewset_node, nodes.Name):
        imported = _find_import(module, viewset_node.name, module_path)
        if imported is not None:
            imported_module, imported_name = imported
            return {"viewset_module": imported_module, "viewset_name": imported_name or viewset_node.name}
        return {"viewset_module": module_path, "viewset_name": viewset_node.name}

    if isinstance(viewset_node.expr, nodes.Name):
        imported = _find_import(module, viewset_node.expr.name, module_path)
        if imported is not None:
            imported_module, imported_name = imported
            if imported_name is None:
                return {"viewset_module": imported_module, "viewset_name": viewset_node.attrname}
    return {"viewset_module": None, "viewset_name": viewset_node.attrname}


def _find_import(module: nodes.Module, local_name: str, module_path: str | None) -> tuple[str, str | None] | None:
    for node in module.body:
        if isinstance(node, nodes.ImportFrom):
            base = _relative_module(module_path, node.modname, node.level)
            for imported_name, alias in node.names:
                if (alias or imported_name) != local_name:
                    continue
                if imported_name == "*":
                    return base, None
                if node.modname:
                    return base, imported_name
                return f"{base}.{imported_name}" if base else imported_name, None
        elif isinstance(node, nodes.Import):
            for imported_name, alias in node.names:
                if (alias or imported_name.split(".")[0]) != local_name:
                    continue
                return (imported_name if alias else imported_name.split(".")[0]), None
    return None


def _relative_module(module_path: str | None, modname: str | None, level: int) -> str:
    if not level:
        return modname or ""
    if not module_path:
        return modname or ""
    parts = module_path.split(".")
    package = parts[: max(0, len(parts) - level)]
    if modname:
        package.extend(modname.split("."))
    return ".".join(package)
