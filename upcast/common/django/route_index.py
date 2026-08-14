"""Internal reverse index for Django URL and DRF Router view references."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from astroid import nodes

from upcast.models.django_views import ResolutionStatus, RouteReference, SourceEvidence


@dataclass(frozen=True)
class RouteModule:
    """Parsed URLconf source needed to build a route index."""

    module: nodes.Module
    module_name: str
    file: str


@dataclass
class RouteIndex:
    """Route references grouped by canonical target identifier."""

    by_target: dict[str, list[RouteReference]] = field(default_factory=dict)
    unresolved: list[RouteReference] = field(default_factory=list)

    def references_for(self, target_id: str) -> list[RouteReference]:
        """Return stable route references for one resolved view target."""
        return list(self.by_target.get(target_id, []))


@dataclass(frozen=True)
class _RouterRegistration:
    router_id: str
    router_type: str
    target_id: str
    prefix: str | None
    basename: str | None
    evidence: SourceEvidence


@dataclass(frozen=True)
class _Router:
    """A local Router binding and its canonical variable identity."""

    id: str
    router_type: str


def build_route_index(route_modules: Iterable[RouteModule]) -> RouteIndex:
    """Build direct-route and DRF Router references from parsed URLconf modules."""
    index = RouteIndex()
    contexts = list(route_modules)
    bindings_by_module = {
        context.module_name: _collect_import_bindings(context.module, context.module_name) for context in contexts
    }
    router_types = _declared_router_types(contexts, bindings_by_module)
    registrations: list[_RouterRegistration] = []
    mounts: dict[str, list[SourceEvidence]] = {}

    for context in contexts:
        bindings = bindings_by_module[context.module_name]
        _add_direct_references(index, context, bindings)
        routers = _find_supported_routers(context, bindings, router_types)
        registrations.extend(_find_router_registrations(context, bindings, routers))
        for router_id, evidence in _find_router_mounts(context, bindings, routers).items():
            mounts.setdefault(router_id, []).extend(evidence)

    for registration in registrations:
        mount_evidence = mounts.get(registration.router_id, [])
        status = ResolutionStatus.CONFIRMED if mount_evidence else ResolutionStatus.PARTIAL
        reference = RouteReference(
            kind="router",
            status=status,
            target_id=registration.target_id,
            prefix=registration.prefix,
            basename=registration.basename,
            router_type=registration.router_type,
            evidence=[registration.evidence, *mount_evidence],
        )
        index.by_target.setdefault(registration.target_id, []).append(reference)

    for references in index.by_target.values():
        references.sort(key=_reference_sort_key)
    index.unresolved.sort(key=_reference_sort_key)

    return index


def _add_direct_references(index: RouteIndex, context: RouteModule, bindings: dict[str, str]) -> None:
    for call_node in context.module.nodes_of_class(nodes.Call):
        if not _is_route_call(call_node, bindings) or len(call_node.args) < 2:
            continue
        pattern = _const_string(call_node.args[0])
        target_id = _resolve_route_target(call_node.args[1], bindings)
        status = ResolutionStatus.CONFIRMED if target_id else ResolutionStatus.UNKNOWN
        evidence = _evidence(
            context.file,
            call_node,
            kind="direct_route",
            status=status,
            qualified_name=target_id,
        )
        reference = RouteReference(
            kind="direct",
            status=status,
            target_id=target_id,
            pattern=pattern,
            evidence=[evidence],
        )
        if target_id is None:
            index.unresolved.append(reference)
        else:
            index.by_target.setdefault(target_id, []).append(reference)


def _declared_router_types(
    contexts: list[RouteModule],
    bindings_by_module: dict[str, dict[str, str]],
) -> dict[str, str]:
    router_types: dict[str, str] = {}
    for context in contexts:
        for local_name, router_type in _direct_router_types(context.module, bindings_by_module[context.module_name]).items():
            router_types[f"{context.module_name}.{local_name}"] = router_type
    return router_types


def _find_supported_routers(
    context: RouteModule,
    bindings: dict[str, str],
    router_types: dict[str, str],
) -> dict[str, _Router]:
    routers = {
        local_name: _Router(id=f"{context.module_name}.{local_name}", router_type=router_type)
        for local_name, router_type in _direct_router_types(context.module, bindings).items()
    }
    for local_name, qualified_name in bindings.items():
        router_type = router_types.get(qualified_name)
        if router_type is not None:
            routers[local_name] = _Router(id=qualified_name, router_type=router_type)
    return routers


def _direct_router_types(module: nodes.Module, bindings: dict[str, str]) -> dict[str, str]:
    router_types: dict[str, str] = {}
    for assign_node in module.nodes_of_class(nodes.Assign):
        if not isinstance(assign_node.value, nodes.Call):
            continue
        router_type = _resolve_expression_name(assign_node.value.func, bindings)
        if not _is_supported_router(router_type):
            continue
        for target in assign_node.targets:
            if isinstance(target, nodes.AssignName):
                router_types[target.name] = router_type.rsplit(".", maxsplit=1)[-1]
    return router_types


def _find_router_registrations(
    context: RouteModule,
    bindings: dict[str, str],
    routers: dict[str, _Router],
) -> list[_RouterRegistration]:
    registrations: list[_RouterRegistration] = []
    for call_node in context.module.nodes_of_class(nodes.Call):
        if not _is_router_register_call(call_node):
            continue
        router_name = call_node.func.expr.name
        router = routers.get(router_name)
        if router is None or len(call_node.args) < 2:
            continue
        target_id = _resolve_expression_name(call_node.args[1], bindings)
        if target_id is None:
            continue
        registrations.append(
            _RouterRegistration(
                router_id=router.id,
                router_type=router.router_type,
                target_id=target_id,
                prefix=_const_string(call_node.args[0]),
                basename=_registration_basename(call_node),
                evidence=_evidence(
                    context.file,
                    call_node,
                    kind="router_registration",
                    status=ResolutionStatus.CONFIRMED,
                    qualified_name=target_id,
                ),
            )
        )
    return registrations


def _find_router_mounts(
    context: RouteModule,
    bindings: dict[str, str],
    routers: dict[str, _Router],
) -> dict[str, list[SourceEvidence]]:
    mounts: dict[str, list[SourceEvidence]] = {}

    for call_node in context.module.nodes_of_class(nodes.Call):
        if not _is_include_call(call_node, bindings) or not call_node.args:
            continue
        router_name = _router_name_from_urls_attribute(call_node.args[0])
        router = routers.get(router_name) if router_name else None
        if router:
            mounts.setdefault(router.id, []).append(
                _evidence(
                    context.file,
                    call_node,
                    kind="router_mount",
                    status=ResolutionStatus.CONFIRMED,
                    qualified_name=router.id,
                )
            )

    for assign_node in context.module.nodes_of_class(nodes.Assign):
        if not any(isinstance(target, nodes.AssignName) and target.name == "urlpatterns" for target in assign_node.targets):
            continue
        router_name = _router_name_from_urls_attribute(assign_node.value)
        router = routers.get(router_name) if router_name else None
        if router:
            mounts.setdefault(router.id, []).append(
                _evidence(
                    context.file,
                    assign_node,
                    kind="router_mount",
                    status=ResolutionStatus.CONFIRMED,
                    qualified_name=router.id,
                )
            )

    return mounts


def _collect_import_bindings(module: nodes.Module, module_name: str) -> dict[str, str]:
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
    return bindings


def _resolve_import_from_module(import_from: nodes.ImportFrom, module_name: str) -> str | None:
    level = getattr(import_from, "level", 0) or 0
    if level:
        module_parts = module_name.split(".")[:-1]
        module_parts = module_parts[: max(0, len(module_parts) - (level - 1))]
    else:
        module_parts = []
    imported_module = import_from.modname or ""
    if imported_module:
        module_parts.extend(imported_module.split("."))
    return ".".join(module_parts) or None


def _resolve_expression_name(node: nodes.NodeNG, bindings: dict[str, str]) -> str | None:
    if isinstance(node, nodes.Name):
        return bindings.get(node.name)
    if isinstance(node, nodes.Attribute):
        parent_name = _resolve_expression_name(node.expr, bindings)
        if parent_name:
            return f"{parent_name}.{node.attrname}"
    return None


def _resolve_route_target(node: nodes.NodeNG, bindings: dict[str, str]) -> str | None:
    if isinstance(node, nodes.Call) and isinstance(node.func, nodes.Attribute) and node.func.attrname == "as_view":
        return _resolve_expression_name(node.func.expr, bindings)
    return _resolve_expression_name(node, bindings)


def _is_route_call(call_node: nodes.Call, bindings: dict[str, str]) -> bool:
    qualified_name = _resolve_expression_name(call_node.func, bindings)
    if qualified_name in {"django.urls.path", "django.urls.re_path", "django.conf.urls.url"}:
        return True
    return isinstance(call_node.func, nodes.Name) and call_node.func.name in {"path", "re_path", "url"}


def _is_include_call(call_node: nodes.Call, bindings: dict[str, str]) -> bool:
    qualified_name = _resolve_expression_name(call_node.func, bindings)
    if qualified_name in {"django.urls.include", "django.conf.urls.include"}:
        return True
    return isinstance(call_node.func, nodes.Name) and call_node.func.name == "include"


def _is_supported_router(qualified_name: str | None) -> bool:
    if qualified_name is None:
        return False
    return qualified_name.startswith("rest_framework.routers.") and qualified_name.endswith("Router")


def _is_router_register_call(call_node: nodes.Call) -> bool:
    return (
        isinstance(call_node.func, nodes.Attribute)
        and call_node.func.attrname == "register"
        and isinstance(call_node.func.expr, nodes.Name)
    )


def _router_name_from_urls_attribute(node: nodes.NodeNG) -> str | None:
    if (
        isinstance(node, nodes.Attribute)
        and node.attrname == "urls"
        and isinstance(node.expr, nodes.Name)
    ):
        return node.expr.name
    return None


def _registration_basename(call_node: nodes.Call) -> str | None:
    if len(call_node.args) >= 3:
        basename = _const_string(call_node.args[2])
        if basename is not None:
            return basename
    for keyword in call_node.keywords:
        if keyword.arg == "basename":
            return _const_string(keyword.value)
    return None


def _const_string(node: nodes.NodeNG) -> str | None:
    return node.value if isinstance(node, nodes.Const) and isinstance(node.value, str) else None


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


def _reference_sort_key(reference: RouteReference) -> tuple[int, str, str]:
    first_line = reference.evidence[0].line if reference.evidence else 0
    return first_line, reference.kind, reference.target_id or ""
