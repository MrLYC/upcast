"""Semantic discovery helpers for Django and Django REST Framework views."""

from __future__ import annotations

from collections.abc import Mapping

from astroid import nodes

from upcast.models.django_views import DjangoView, Recognition, ResolutionStatus, SourceEvidence

_VIEWSET_BASE_NAMES = {
    "ViewSet",
    "GenericViewSet",
    "ModelViewSet",
    "ReadOnlyModelViewSet",
}
_API_VIEW_BASE_NAMES = {
    "APIView",
    "GenericAPIView",
    "CreateAPIView",
    "DestroyAPIView",
    "ListAPIView",
    "ListCreateAPIView",
    "RetrieveAPIView",
    "RetrieveDestroyAPIView",
    "RetrieveUpdateAPIView",
    "RetrieveUpdateDestroyAPIView",
    "UpdateAPIView",
}
_DJANGO_VIEW_BASE_NAMES = {
    "View",
    "TemplateView",
    "RedirectView",
    "ListView",
    "DetailView",
    "CreateView",
    "UpdateView",
    "DeleteView",
    "FormView",
}
_KNOWN_PARTIAL_BASE_NAMES = _VIEWSET_BASE_NAMES | _API_VIEW_BASE_NAMES | _DJANGO_VIEW_BASE_NAMES
_KNOWN_FUNCTION_VIEW_DECORATORS = {
    "rest_framework.decorators.api_view",
}


def discover_views(
    module: nodes.Module,
    file: str,
    module_name: str,
    known_view_bases: Mapping[str, DjangoView] | None = None,
) -> list[DjangoView]:
    """Discover module-level Django/DRF views from imports and syntax.

    Astroid cannot always import a scanned project's framework dependencies.  This
    helper therefore resolves explicit import bindings first, then preserves known
    unqualified framework names as partial evidence rather than silently dropping
    them.
    """
    bindings = _collect_import_bindings(module, module_name)
    views: list[DjangoView] = []
    known_bases = dict(known_view_bases or {})
    class_nodes = [node for node in module.nodes_of_class(nodes.ClassDef) if node.parent is module]
    pending_classes = list(class_nodes)

    while pending_classes:
        next_pending: list[nodes.ClassDef] = []
        discovered_in_pass = False
        for class_node in pending_classes:
            view = _discover_class_view(class_node, file, module_name, bindings, known_bases)
            if view is None:
                next_pending.append(class_node)
                continue
            views.append(view)
            known_bases[view.id] = view
            discovered_in_pass = True
        if not discovered_in_pass:
            break
        pending_classes = next_pending

    for function_node in module.nodes_of_class(nodes.FunctionDef):
        if function_node.parent is not module:
            continue
        view = _discover_function_view(function_node, file, module_name, bindings)
        if view is not None:
            views.append(view)

    return sorted(views, key=lambda view: (view.line, view.id))


def _discover_class_view(
    class_node: nodes.ClassDef,
    file: str,
    module_name: str,
    bindings: dict[str, str],
    known_view_bases: Mapping[str, DjangoView],
) -> DjangoView | None:
    for base_node in class_node.bases:
        qualified_name = _resolve_expression_name(base_node, bindings)
        kind = _classify_view_base(qualified_name)
        inherited_view = known_view_bases.get(qualified_name) if qualified_name else None
        if kind is not None:
            status = ResolutionStatus.CONFIRMED
        elif inherited_view is not None:
            status = inherited_view.recognition.status
        else:
            status = _partial_base_status(base_node, qualified_name)
        if status is ResolutionStatus.UNKNOWN:
            continue

        resolved_kind = kind or (inherited_view.kind if inherited_view else _kind_from_simple_base(_simple_name(base_node)))
        evidence = _evidence(
            file=file,
            node=base_node,
            kind="base_class",
            status=status,
            qualified_name=qualified_name if kind is not None or inherited_view is not None else None,
        )
        return DjangoView(
            id=f"{module_name}.{class_node.name}",
            name=class_node.name,
            kind=resolved_kind,
            file=file,
            line=class_node.lineno,
            recognition=Recognition(status=status, evidence=[evidence]),
        )
    return None


def _discover_function_view(
    function_node: nodes.FunctionDef,
    file: str,
    module_name: str,
    bindings: dict[str, str],
) -> DjangoView | None:
    decorators = function_node.decorators.nodes if function_node.decorators else []
    for decorator_node in decorators:
        target_node = decorator_node.func if isinstance(decorator_node, nodes.Call) else decorator_node
        qualified_name = _resolve_expression_name(target_node, bindings)
        if qualified_name in _KNOWN_FUNCTION_VIEW_DECORATORS:
            status = ResolutionStatus.CONFIRMED
        elif _simple_name(target_node) == "api_view":
            status = ResolutionStatus.PARTIAL
        else:
            continue

        evidence = _evidence(
            file=file,
            node=decorator_node,
            kind="decorator",
            status=status,
            qualified_name=qualified_name if status is ResolutionStatus.CONFIRMED else None,
        )
        return DjangoView(
            id=f"{module_name}.{function_node.name}",
            name=function_node.name,
            kind="drf_function_view",
            file=file,
            line=function_node.lineno,
            recognition=Recognition(status=status, evidence=[evidence]),
        )
    return None


def _collect_import_bindings(module: nodes.Module, module_name: str) -> dict[str, str]:
    """Build explicit local-name to qualified-name bindings from imports."""
    bindings: dict[str, str] = {}

    for import_from in module.nodes_of_class(nodes.ImportFrom):
        base_module = _resolve_import_from_module(import_from, module_name)
        if base_module is None:
            continue
        for imported_name, alias in import_from.names:
            if imported_name == "*":
                continue
            bindings[alias or imported_name] = f"{base_module}.{imported_name}"

    for import_node in module.nodes_of_class(nodes.Import):
        for imported_name, alias in import_node.names:
            bindings[alias or imported_name.split(".")[0]] = imported_name

    for node in module.body:
        if isinstance(node, (nodes.ClassDef, nodes.FunctionDef)):
            bindings.setdefault(node.name, f"{module_name}.{node.name}")

    return bindings


def _resolve_import_from_module(import_from: nodes.ImportFrom, module_name: str) -> str | None:
    level = getattr(import_from, "level", 0) or 0
    module_parts = module_name.split(".")[:-1]
    module_parts = module_parts[: max(0, len(module_parts) - (level - 1))] if level else []
    if import_from.modname:
        module_parts.extend(import_from.modname.split("."))
    return ".".join(module_parts) or None


def _resolve_expression_name(node: nodes.NodeNG, bindings: dict[str, str]) -> str | None:
    """Resolve a name/attribute expression using explicit import bindings."""
    if isinstance(node, nodes.Name):
        return bindings.get(node.name)
    if isinstance(node, nodes.Attribute):
        parent_name = _resolve_expression_name(node.expr, bindings)
        if parent_name:
            return f"{parent_name}.{node.attrname}"
    return None


def _classify_view_base(qualified_name: str | None) -> str | None:
    """Return the supported view category for a resolved framework base."""
    if qualified_name is None:
        return None
    simple_name = qualified_name.rsplit(".", maxsplit=1)[-1]
    if qualified_name.startswith("rest_framework.viewsets.") and simple_name in _VIEWSET_BASE_NAMES:
        return "drf_viewset"
    if qualified_name.startswith("rest_framework.") and simple_name in _API_VIEW_BASE_NAMES:
        return "drf_api_view"
    if qualified_name.startswith("django.views.") and simple_name in _DJANGO_VIEW_BASE_NAMES:
        return "django_cbv"
    return None


def _partial_base_status(node: nodes.NodeNG, qualified_name: str | None) -> ResolutionStatus:
    if qualified_name is None and _simple_name(node) in _KNOWN_PARTIAL_BASE_NAMES:
        return ResolutionStatus.PARTIAL
    return ResolutionStatus.UNKNOWN


def _kind_from_simple_base(simple_name: str | None) -> str:
    if simple_name in _VIEWSET_BASE_NAMES:
        return "drf_viewset"
    if simple_name in _API_VIEW_BASE_NAMES:
        return "drf_api_view"
    return "django_cbv"


def _simple_name(node: nodes.NodeNG) -> str | None:
    if isinstance(node, nodes.Name):
        return node.name
    if isinstance(node, nodes.Attribute):
        return node.attrname
    return None


def _evidence(
    file: str,
    node: nodes.NodeNG,
    kind: str,
    status: ResolutionStatus,
    qualified_name: str | None,
) -> SourceEvidence:
    return SourceEvidence(
        file=file,
        line=getattr(node, "lineno", 1),
        column=getattr(node, "col_offset", None),
        expression=node.as_string(),
        kind=kind,
        status=status,
        qualified_name=qualified_name,
    )
