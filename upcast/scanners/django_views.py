"""Standalone static scanner for Django and Django REST Framework views."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from pathlib import Path

from astroid import nodes

from upcast.common.django.permission_resolver import (
    PermissionModule,
    apply_drf_defaults,
    extract_drf_defaults,
    resolve_permission_definitions,
)
from upcast.common.django.route_index import RouteModule, build_route_index
from upcast.common.django.view_discovery import discover_views
from upcast.common.django.view_model_usage import (
    ModelModule,
    extract_class_model_usages,
    extract_function_model_usages,
)
from upcast.common.django.view_security import analyze_function_security, analyze_view_security
from upcast.common.scanner_base import BaseScanner
from upcast.models.django_views import (
    DjangoView,
    DjangoViewOutput,
    DjangoViewSummary,
    Recognition,
    ResolutionStatus,
    SourceEvidence,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class _ParsedModule:
    """A parsed source module and the stable context used in output evidence."""

    module: nodes.Module
    module_name: str
    file: str


@dataclass(frozen=True)
class _SymbolDefinition:
    """A top-level function or class available for route fallback/enrichment."""

    node: nodes.ClassDef | nodes.FunctionDef
    context: _ParsedModule


class DjangoViewScanner(BaseScanner[DjangoViewOutput]):
    """Find semantic Django/DRF views and bounded source-located evidence."""

    markdown_title = "Django View Analysis"

    def scan(self, path: Path) -> DjangoViewOutput:
        """Scan all eligible Python source files below *path*."""
        started = time.perf_counter()
        scan_root = path if path.is_dir() else path.parent
        parsed_modules = self._parse_modules(self.get_files_to_scan(path), scan_root)
        route_modules = [RouteModule(item.module, item.module_name, item.file) for item in parsed_modules]
        route_index = build_route_index(route_modules)
        symbols = self._symbol_index(parsed_modules)

        views = self._discover_semantic_views(parsed_modules)
        self._add_route_fallbacks(views, route_index.by_target, symbols)
        self._attach_route_references(views, route_index.by_target)
        self._enrich_views(views, parsed_modules, symbols)

        ordered_views = {view_id: views[view_id] for view_id in sorted(views)}
        summary = DjangoViewSummary(
            total_count=len(ordered_views),
            files_scanned=len(parsed_modules),
            scan_duration_ms=int((time.perf_counter() - started) * 1000),
            total_views=len(ordered_views),
            total_actions=sum(len(view.actions) for view in ordered_views.values()),
        )
        return DjangoViewOutput(
            summary=summary,
            results=ordered_views,
            unresolved_route_references=route_index.unresolved,
            metadata={"scanner_name": "django-views"},
        )

    def _parse_modules(self, files: list[Path], scan_root: Path) -> list[_ParsedModule]:
        parsed_modules: list[_ParsedModule] = []
        for file_path in files:
            module = self.parse_file(file_path)
            if module is None:
                continue
            parsed_modules.append(
                _ParsedModule(
                    module=module,
                    module_name=self._module_name(file_path, scan_root),
                    file=self._relative_file(file_path, scan_root),
                )
            )
        return parsed_modules

    def _discover_semantic_views(self, parsed_modules: list[_ParsedModule]) -> dict[str, DjangoView]:
        views: dict[str, DjangoView] = {}
        while True:
            discovered_in_pass = False
            for context in parsed_modules:
                candidates = discover_views(
                    context.module,
                    file=context.file,
                    module_name=context.module_name,
                    known_view_bases=views,
                )
                for candidate in candidates:
                    if candidate.id in views:
                        continue
                    views[candidate.id] = candidate
                    discovered_in_pass = True
            if not discovered_in_pass:
                return views

    def _symbol_index(self, parsed_modules: list[_ParsedModule]) -> dict[str, _SymbolDefinition]:
        symbols: dict[str, _SymbolDefinition] = {}
        for context in parsed_modules:
            for node in context.module.body:
                if isinstance(node, (nodes.ClassDef, nodes.FunctionDef)):
                    symbols[f"{context.module_name}.{node.name}"] = _SymbolDefinition(node=node, context=context)
        return symbols

    def _add_route_fallbacks(
        self,
        views: dict[str, DjangoView],
        references_by_target: dict[str, list],
        symbols: dict[str, _SymbolDefinition],
    ) -> None:
        for target_id, references in references_by_target.items():
            if target_id in views:
                continue
            symbol = symbols.get(target_id)
            if symbol is None:
                continue
            if isinstance(symbol.node, nodes.FunctionDef):
                kind = "django_function_view"
                status = ResolutionStatus.CONFIRMED
            elif isinstance(symbol.node, nodes.ClassDef):
                kind = "route_class_candidate"
                status = ResolutionStatus.PARTIAL
            else:
                continue
            route_evidence = references[0].evidence[0] if references and references[0].evidence else None
            evidence = (
                route_evidence.model_copy(
                    update={
                        "kind": "route_target",
                        "status": status,
                        "qualified_name": target_id,
                    }
                )
                if route_evidence is not None
                else SourceEvidence(
                    file=symbol.context.file,
                    line=symbol.node.lineno,
                    expression=symbol.node.name,
                    kind="route_target",
                    status=status,
                    qualified_name=target_id,
                )
            )
            views[target_id] = DjangoView(
                id=target_id,
                name=symbol.node.name,
                kind=kind,
                file=symbol.context.file,
                line=symbol.node.lineno,
                recognition=Recognition(status=status, evidence=[evidence]),
            )

    def _attach_route_references(
        self,
        views: dict[str, DjangoView],
        references_by_target: dict[str, list],
    ) -> None:
        for view_id, view in views.items():
            view.route_refs = list(references_by_target.get(view_id, []))

    def _enrich_views(
        self,
        views: dict[str, DjangoView],
        parsed_modules: list[_ParsedModule],
        symbols: dict[str, _SymbolDefinition],
    ) -> None:
        permission_modules = [PermissionModule(item.module, item.module_name, item.file) for item in parsed_modules]
        model_modules = [ModelModule(item.module, item.module_name, item.file) for item in parsed_modules]
        defaults = extract_drf_defaults(permission_modules)
        pending = set(views)

        while pending:
            progressed = False
            for view_id in sorted(pending):
                symbol = symbols.get(view_id)
                inherited_view = self._parent_view(symbol, views) if symbol is not None else None
                if inherited_view is not None and inherited_view.id in pending:
                    continue
                self._enrich_view(
                    views[view_id],
                    symbol,
                    defaults,
                    permission_modules,
                    model_modules,
                    inherited_view,
                )
                pending.remove(view_id)
                progressed = True
            if progressed:
                continue
            for view_id in sorted(pending):
                self._enrich_view(
                    views[view_id],
                    symbols.get(view_id),
                    defaults,
                    permission_modules,
                    model_modules,
                    None,
                )
                pending.remove(view_id)

    def _enrich_view(
        self,
        view: DjangoView,
        symbol: _SymbolDefinition | None,
        defaults,
        permission_modules: list[PermissionModule],
        model_modules: list[ModelModule],
        inherited_view: DjangoView | None,
    ) -> None:
        if symbol is None:
            return
        if isinstance(symbol.node, nodes.ClassDef):
            self._enrich_class_view(
                view,
                symbol,
                defaults,
                permission_modules,
                model_modules,
                inherited_view,
            )
        elif isinstance(symbol.node, nodes.FunctionDef):
            self._enrich_function_view(view, symbol, defaults, permission_modules, model_modules)

    def _parent_view(
        self,
        symbol: _SymbolDefinition,
        views: dict[str, DjangoView],
    ) -> DjangoView | None:
        if not isinstance(symbol.node, nodes.ClassDef):
            return None
        bindings = _collect_import_bindings(symbol.context.module, symbol.context.module_name)
        for base_node in symbol.node.bases:
            qualified_name = _resolve_expression_name(base_node, bindings)
            if qualified_name and qualified_name in views:
                return views[qualified_name]
        return None

    def _enrich_class_view(
        self,
        view: DjangoView,
        symbol: _SymbolDefinition,
        defaults,
        permission_modules: list[PermissionModule],
        model_modules: list[ModelModule],
        inherited_view: DjangoView | None,
    ) -> None:
        class_node = symbol.node
        if not isinstance(class_node, nodes.ClassDef):
            return
        security, actions = analyze_view_security(
            class_node,
            file=view.file,
            module_name=symbol.context.module_name,
            view_id=view.id,
            kind=view.kind,
            recognition_status=view.recognition.status,
            inherited_security=inherited_view.security if inherited_view else None,
            inherited_actions=inherited_view.actions if inherited_view else None,
        )
        view.security = resolve_permission_definitions(apply_drf_defaults(security, defaults), permission_modules)
        local_model_usages = extract_class_model_usages(
            class_node,
            file=view.file,
            module_name=symbol.context.module_name,
            modules=model_modules,
        )
        view.model_usages = _merge_model_usages(inherited_view.model_usages if inherited_view else [], local_model_usages)
        methods = {method.name: method for method in class_node.body if isinstance(method, nodes.FunctionDef)}
        for action in actions:
            action.security = resolve_permission_definitions(apply_drf_defaults(action.security, defaults), permission_modules)
            action_node = methods.get(action.name)
            if action.origin == "decorator" and action_node is not None:
                action.model_usages = extract_function_model_usages(
                    action_node,
                    file=view.file,
                    module_name=symbol.context.module_name,
                    modules=model_modules,
                )
        view.actions = actions

    def _enrich_function_view(
        self,
        view: DjangoView,
        symbol: _SymbolDefinition,
        defaults,
        permission_modules: list[PermissionModule],
        model_modules: list[ModelModule],
    ) -> None:
        function_node = symbol.node
        if not isinstance(function_node, nodes.FunctionDef):
            return
        security = analyze_function_security(
            function_node,
            file=view.file,
            module_name=symbol.context.module_name,
        )
        view.security = resolve_permission_definitions(apply_drf_defaults(security, defaults), permission_modules)
        view.model_usages = extract_function_model_usages(
            function_node,
            file=view.file,
            module_name=symbol.context.module_name,
            modules=model_modules,
        )

    def _module_name(self, file_path: Path, scan_root: Path) -> str:
        relative = file_path.relative_to(scan_root)
        parts = list(relative.with_suffix("").parts)
        if parts[-1] == "__init__":
            parts.pop()
        return ".".join(parts) or file_path.stem

    def _relative_file(self, file_path: Path, scan_root: Path) -> str:
        return file_path.relative_to(scan_root).as_posix()


def _collect_import_bindings(module: nodes.Module, module_name: str) -> dict[str, str]:
    bindings: dict[str, str] = {}
    for import_from in module.nodes_of_class(nodes.ImportFrom):
        base_module = _resolve_import_from_module(import_from, module_name)
        if base_module is None:
            continue
        for imported_name, alias in import_from.names:
            if imported_name != "*":
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
    parts = module_name.split(".")[:-1]
    parts = parts[: max(0, len(parts) - (level - 1))] if level else []
    if import_from.modname:
        parts.extend(import_from.modname.split("."))
    return ".".join(parts) or None


def _resolve_expression_name(node: nodes.NodeNG, bindings: dict[str, str]) -> str | None:
    if isinstance(node, nodes.Name):
        return bindings.get(node.name)
    if isinstance(node, nodes.Attribute):
        parent_name = _resolve_expression_name(node.expr, bindings)
        return f"{parent_name}.{node.attrname}" if parent_name else None
    return None


def _merge_model_usages(inherited, local):
    unique = {
        (
            usage.evidence.file,
            usage.evidence.line,
            usage.evidence.expression,
            usage.role,
            usage.model,
            usage.operation,
        ): usage
        for usage in [*inherited, *local]
    }
    return sorted(
        unique.values(),
        key=lambda usage: (usage.evidence.file, usage.evidence.line, usage.role, usage.model or "", usage.operation),
    )
