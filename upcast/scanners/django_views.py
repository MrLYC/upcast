"""Django and Django REST Framework view scanner."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from astroid import nodes

from upcast.common.scanner_base import BaseScanner
from upcast.models.django_views import DjangoView, DjangoViewOutput, DjangoViewSummary, ViewAction, ViewRouteLink

logger = logging.getLogger(__name__)


@dataclass
class _ModuleContext:
    module_path: str
    file_path: Path
    module: nodes.Module
    imports: dict[str, tuple[str, str | None]]
    symbols: dict[str, nodes.NodeNG]


class DjangoViewScanner(BaseScanner[DjangoViewOutput]):
    """Scan Python source for statically identifiable Django views.

    The scanner deliberately keeps raw expressions for permissions, auth
    classes, and decorators.  It does not infer runtime middleware behavior or
    assign meaning to project-specific decorators beyond explicit names.
    """

    _HTTP_METHODS: ClassVar[set[str]] = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "TRACE"}
    _VIEW_BASES: ClassVar[set[str]] = {
        "View",
        "TemplateView",
        "RedirectView",
        "FormView",
        "CreateView",
        "UpdateView",
        "DeleteView",
        "ListView",
        "DetailView",
        "APIView",
        "ViewSet",
        "GenericViewSet",
        "ModelViewSet",
        "ReadOnlyModelViewSet",
    }
    _URL_CALLS: ClassVar[set[str]] = {"path", "re_path", "url"}

    def __init__(
        self,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        verbose: bool = False,
    ) -> None:
        super().__init__(
            include_patterns=include_patterns or ["**/*.py"],
            exclude_patterns=exclude_patterns,
            verbose=verbose,
        )

    def scan(self, path: Path) -> DjangoViewOutput:  # noqa: C901
        """Scan Python files and return views grouped by source module."""
        start_time = time.perf_counter()
        files = self.get_files_to_scan(path)
        scan_root = path if path.is_dir() else path.parent
        # View semantics are not tied to filenames or route reachability. Parse
        # every eligible Python file so an unreferenced or unusually named view
        # is not silently omitted from the inventory.
        candidate_files = files

        contexts: list[_ModuleContext] = []
        for file_path in candidate_files:
            module = self.parse_file(file_path)
            if module is None:
                continue
            module_path = self._get_module_path(file_path, scan_root)
            contexts.append(
                _ModuleContext(
                    module_path=module_path,
                    file_path=file_path,
                    module=module,
                    imports=self._collect_imports(module, module_path, file_path.stem == "__init__"),
                    symbols=self._collect_symbols(module),
                )
            )

        module_by_alias = self._build_module_aliases(contexts)
        contexts_by_module = {context.module_path: context for context in contexts}
        symbol_index = {
            (context.module_path, name): node
            for context in contexts
            for name, node in context.symbols.items()
        }
        export_aliases = self._build_export_aliases(contexts, module_by_alias)
        route_links = self._discover_route_links(contexts, module_by_alias, export_aliases, scan_root)
        method_index = self._build_method_index(contexts)

        results: dict[str, list[DjangoView]] = {}
        view_class_cache: dict[tuple[str, str], bool] = {}
        for context in contexts:
            views: list[DjangoView] = []
            for node in context.module.body:
                if isinstance(node, nodes.ClassDef):
                    key = (context.module_path, node.name)
                    is_view = self._is_view_class(
                        node,
                        context,
                        symbol_index,
                        contexts_by_module,
                        module_by_alias,
                        view_class_cache,
                        set(),
                    )
                    has_route = key in route_links
                    if not is_view and not has_route:
                        continue
                    view = self._build_class_view(
                        node=node,
                        context=context,
                        is_view=is_view,
                        route_links=route_links.get(key, []),
                        scan_root=scan_root,
                    )
                    views.append(view)
                elif isinstance(node, nodes.FunctionDef):
                    key = (context.module_path, node.name)
                    decorator_names = self._decorator_names(node)
                    explicit = self._is_explicit_function_view(decorator_names)
                    has_route = key in route_links
                    if not explicit and not has_route:
                        continue
                    views.append(
                        self._build_function_view(
                            node=node,
                            context=context,
                            route_links=route_links.get(key, []),
                            scan_root=scan_root,
                            identified_by=(
                                ["drf_api_view_decorator"]
                                if "api_view" in decorator_names
                                else ["view_marker_decorator"] if explicit else ["route_reference"]
                            ),
                        )
                    )

            for key, links in route_links.items():
                if key[0] != context.module_path or key in context.symbols:
                    continue
                method_info = method_index.get(key)
                if method_info is None:
                    continue
                class_node, method_node = method_info
                views.append(
                    self._build_method_view(
                        class_node=class_node,
                        node=method_node,
                        context=context,
                        route_links=links,
                        scan_root=scan_root,
                    )
                )

            if views:
                results[context.module_path] = views

        duration_ms = int((time.perf_counter() - start_time) * 1000)
        total_views = sum(len(views) for views in results.values())
        summary = DjangoViewSummary(
            total_count=total_views,
            files_scanned=len(candidate_files),
            scan_duration_ms=duration_ms,
            total_modules=len(results),
            total_views=total_views,
        )
        return DjangoViewOutput(
            summary=summary,
            results=results,
            metadata={
                "scanner_name": "django-views",
                "files_considered": len(files),
                "candidate_files": len(candidate_files),
            },
        )

    def _build_method_index(
        self, contexts: list[_ModuleContext]
    ) -> dict[tuple[str, str], tuple[nodes.ClassDef, nodes.FunctionDef]]:
        methods: dict[tuple[str, str], tuple[nodes.ClassDef, nodes.FunctionDef]] = {}
        for context in contexts:
            for node in context.module.body:
                if not isinstance(node, nodes.ClassDef):
                    continue
                for child in node.body:
                    if isinstance(child, nodes.FunctionDef):
                        methods[(context.module_path, f"{node.name}.{child.name}")] = (node, child)
        return methods

    def _build_class_view(
        self,
        *,
        node: nodes.ClassDef,
        context: _ModuleContext,
        is_view: bool,
        route_links: list[ViewRouteLink],
        scan_root: Path,
    ) -> DjangoView:
        decorators = self._decorator_strings(node)
        decorator_names = self._decorator_names(node)
        bases = [self._expression(base) for base in node.bases]
        identified_by: list[str] = []
        if is_view:
            if any(self._base_name(base) in {"View", "TemplateView"} for base in node.bases):
                identified_by.append("django_view_base")
            if any(self._looks_like_drf_base(self._base_name(base)) for base in node.bases):
                identified_by.append("drf_view_base")
            if not identified_by:
                identified_by.append("inherited_view_base")
        if route_links:
            identified_by.append("route_reference")

        permissions = self._class_attribute_values(node, "permission_classes")
        authentications = self._class_attribute_values(node, "authentication_classes")
        serializer_class = self._class_attribute_value(node, "serializer_class")
        actions: list[ViewAction] = []
        methods: set[str] = set()
        model_references = set(self._model_references(node))
        for child in node.body:
            if not isinstance(child, nodes.FunctionDef):
                continue
            method_name = child.name.upper()
            if method_name in self._HTTP_METHODS:
                methods.add(method_name)
            action = self._build_action(child, context, scan_root)
            if action is not None:
                actions.append(action)
            model_references.update(self._model_references(child))

        login_exempt, csrf_exempt = self._security_evidence(decorator_names)
        return DjangoView(
            module=context.module_path,
            name=node.name,
            qualname=f"{context.module_path}.{node.name}",
            kind="class",
            status="confirmed" if is_view else "unknown",
            identified_by=self._unique(identified_by),
            route_linkage=route_links,
            bases=bases,
            decorators=decorators,
            http_methods=sorted(methods),
            actions=actions,
            permission_classes=permissions,
            authentication_classes=authentications,
            login_exempt=login_exempt,
            csrf_exempt=csrf_exempt,
            model_references=sorted(model_references),
            serializer_class=serializer_class,
            file=self._source_file(context.file_path, scan_root),
            line=getattr(node, "lineno", None),
        )

    def _build_function_view(
        self,
        *,
        node: nodes.FunctionDef,
        context: _ModuleContext,
        route_links: list[ViewRouteLink],
        scan_root: Path,
        identified_by: list[str],
    ) -> DjangoView:
        decorator_names = self._decorator_names(node)
        methods = self._api_view_methods(node)
        if not methods:
            for name in decorator_names:
                upper = name.removeprefix("require_").upper()
                if upper in self._HTTP_METHODS:
                    methods = [upper]
        login_exempt, csrf_exempt = self._security_evidence(decorator_names)
        return DjangoView(
            module=context.module_path,
            name=node.name,
            qualname=f"{context.module_path}.{node.name}",
            kind="function",
            status="confirmed",
            identified_by=identified_by,
            route_linkage=route_links,
            decorators=self._decorator_strings(node),
            http_methods=methods,
            login_exempt=login_exempt,
            csrf_exempt=csrf_exempt,
            model_references=self._model_references(node),
            file=self._source_file(context.file_path, scan_root),
            line=getattr(node, "lineno", None),
        )

    def _build_method_view(
        self,
        *,
        class_node: nodes.ClassDef,
        node: nodes.FunctionDef,
        context: _ModuleContext,
        route_links: list[ViewRouteLink],
        scan_root: Path,
    ) -> DjangoView:
        decorator_names = self._decorator_names(node)
        login_exempt, csrf_exempt = self._security_evidence(decorator_names)
        return DjangoView(
            module=context.module_path,
            name=node.name,
            qualname=f"{context.module_path}.{class_node.name}.{node.name}",
            kind="method",
            status="confirmed",
            identified_by=["route_reference"],
            route_linkage=route_links,
            decorators=self._decorator_strings(node),
            http_methods=[],
            login_exempt=login_exempt,
            csrf_exempt=csrf_exempt,
            model_references=self._model_references(node),
            file=self._source_file(context.file_path, scan_root),
            line=getattr(node, "lineno", None),
        )

    def _build_action(self, node: nodes.FunctionDef, context: _ModuleContext, scan_root: Path) -> ViewAction | None:  # noqa: C901
        action_call = next(
            (
                decorator
                for decorator in (node.decorators.nodes if node.decorators else [])
                if self._decorator_name(decorator) == "action"
            ),
            None,
        )
        if action_call is None:
            return None

        methods: list[str] = []
        detail: bool | None = None
        url_path: str | None = None
        url_name: str | None = None
        permission_classes: list[str] = []
        authentication_classes: list[str] = []
        if isinstance(action_call, nodes.Call):
            if action_call.args:
                methods = self._string_values(action_call.args[0])
            for keyword in action_call.keywords:
                if keyword.arg == "methods":
                    methods = self._string_values(keyword.value)
                elif keyword.arg == "detail":
                    detail = self._bool_value(keyword.value)
                elif keyword.arg == "url_path":
                    url_path = self._literal_value(keyword.value)
                elif keyword.arg == "url_name":
                    url_name = self._literal_value(keyword.value)
                elif keyword.arg == "permission_classes":
                    permission_classes = self._string_values(keyword.value)
                elif keyword.arg == "authentication_classes":
                    authentication_classes = self._string_values(keyword.value)
        method_decorators = self._decorator_names(node)
        login_exempt, csrf_exempt = self._security_evidence(method_decorators)
        return ViewAction(
            name=node.name,
            methods=self._normalize_methods(methods),
            detail=detail,
            url_path=url_path,
            url_name=url_name,
            decorators=self._decorator_strings(node),
            permission_classes=permission_classes,
            authentication_classes=authentication_classes,
            login_exempt=login_exempt,
            csrf_exempt=csrf_exempt,
            file=self._source_file(context.file_path, scan_root),
            line=getattr(node, "lineno", None),
        )

    def _discover_route_links(  # noqa: C901
        self,
        contexts: list[_ModuleContext],
        module_by_alias: dict[str, str],
        export_aliases: dict[tuple[str, str], tuple[str, str]],
        scan_root: Path,
    ) -> dict[tuple[str, str], list[ViewRouteLink]]:
        links: dict[tuple[str, str], list[ViewRouteLink]] = {}
        router_mounts: dict[tuple[str, str], list[_ModuleContext]] = {}
        for context in contexts:
            if not self._is_url_module(context):
                continue
            for router_name in self._mounted_router_names(context):
                router_key = self._router_key(context, router_name, module_by_alias)
                router_mounts.setdefault(router_key, []).append(context)
            for call in context.module.nodes_of_class(nodes.Call):
                if not self._is_module_level(call, context.module):
                    continue
                function_name = self._call_name(call.func)
                if function_name in self._URL_CALLS and len(call.args) >= 2:
                    target = self._resolve_target(call.args[1], context, module_by_alias, export_aliases)
                    if target is None:
                        continue
                    pattern = self._literal_value(call.args[0])
                    link = ViewRouteLink(
                        type=function_name,
                        url_module=context.module_path,
                        pattern=pattern,
                        full_path=pattern,
                        name=self._keyword_literal(call, "name"),
                        file=self._source_file(context.file_path, scan_root),
                        line=getattr(call, "lineno", None),
                    )
                    links.setdefault(target, []).append(link)

        for context in contexts:
            for call in context.module.nodes_of_class(nodes.Call):
                if (
                    not self._is_module_level(call, context.module)
                    or self._call_name(call.func) != "register"
                    or not isinstance(call.func, nodes.Attribute)
                    or not isinstance(call.func.expr, nodes.Name)
                    or len(call.args) < 2
                ):
                    continue
                router_key = self._router_key(context, call.func.expr.name, module_by_alias)
                mounts = router_mounts.get(router_key, [])
                if not mounts:
                    continue
                target = self._resolve_target(call.args[1], context, module_by_alias, export_aliases)
                if target is None:
                    continue
                basename = self._literal_value(call.args[2]) if len(call.args) >= 3 else None
                basename = basename or self._keyword_literal(call, "basename")
                prefix = self._literal_value(call.args[0])
                for mount in mounts:
                    link = ViewRouteLink(
                        type="router_registration",
                        url_module=mount.module_path,
                        pattern=prefix,
                        full_path=prefix,
                        name=basename,
                        file=self._source_file(context.file_path, scan_root),
                        line=getattr(call, "lineno", None),
                    )
                    links.setdefault(target, []).append(link)
        return links

    def _mounted_router_names(self, context: _ModuleContext) -> set[str]:
        """Return Router variables whose ``.urls`` are mounted in this URLconf."""
        mounted: set[str] = set()
        for node in context.module.nodes_of_class(nodes.Call):
            if (
                self._is_module_level(node, context.module)
                and self._call_name(node.func) == "include"
                and node.args
            ):
                mounted.update(self._router_names_in(node.args[0]))
            if (
                isinstance(node.func, nodes.Attribute)
                and isinstance(node.func.expr, nodes.Name)
                and node.func.expr.name == "urlpatterns"
                and node.func.attrname in {"append", "extend"}
                and self._is_module_level(node, context.module)
            ):
                for argument in node.args:
                    mounted.update(self._router_names_in(argument))

        for node in context.module.nodes_of_class((nodes.Assign, nodes.AugAssign)):
            if not self._is_module_level(node, context.module):
                continue
            target = node.targets[0] if isinstance(node, nodes.Assign) and node.targets else node.target
            if isinstance(target, nodes.AssignName) and target.name == "urlpatterns":
                mounted.update(self._router_names_in(node.value))
        return mounted

    def _router_names_in(self, node: nodes.NodeNG) -> set[str]:
        """Find Router variable names in ``router.urls`` expressions."""
        candidates = [node, *node.nodes_of_class(nodes.Attribute)]
        return {
            candidate.expr.name
            for candidate in candidates
            if isinstance(candidate, nodes.Attribute)
            and candidate.attrname == "urls"
            and isinstance(candidate.expr, nodes.Name)
        }

    def _router_key(
        self, context: _ModuleContext, local_name: str, module_by_alias: dict[str, str]
    ) -> tuple[str, str]:
        imported = context.imports.get(local_name)
        if imported is None:
            return context.module_path, local_name
        module_name, imported_name = imported
        canonical_module = module_by_alias.get(module_name, module_name)
        return canonical_module, imported_name or local_name

    def _resolve_target(
        self,
        node: nodes.NodeNG,
        context: _ModuleContext,
        module_by_alias: dict[str, str],
        export_aliases: dict[tuple[str, str], tuple[str, str]],
    ) -> tuple[str, str] | None:
        target = self._resolve_raw_target(node, context, module_by_alias)
        seen: set[tuple[str, str]] = set()
        while target in export_aliases and target not in seen:
            seen.add(target)
            target = export_aliases[target]
        return target

    def _resolve_raw_target(  # noqa: C901
        self,
        node: nodes.NodeNG,
        context: _ModuleContext,
        module_by_alias: dict[str, str],
    ) -> tuple[str, str] | None:
        if isinstance(node, nodes.Call) and isinstance(node.func, nodes.Attribute) and node.func.attrname == "as_view":
            return self._resolve_raw_target(node.func.expr, context, module_by_alias)
        if isinstance(node, nodes.Attribute) and isinstance(node.expr, nodes.Call):
            class_target = self._resolve_raw_target(node.expr.func, context, module_by_alias)
            if class_target is not None:
                return class_target[0], f"{class_target[1]}.{node.attrname}"
        if isinstance(node, nodes.Name):
            local = context.symbols.get(node.name)
            if isinstance(local, (nodes.FunctionDef, nodes.ClassDef)):
                return context.module_path, node.name
            imported = context.imports.get(node.name)
            if imported and imported[1]:
                return module_by_alias.get(imported[0], imported[0]), imported[1]
            wildcard_modules = [
                value for key, value in context.imports.items() if key == "*" or key.startswith("*:")
            ]
            if wildcard_modules:
                return module_by_alias.get(wildcard_modules[0][0], wildcard_modules[0][0]), node.name
            return None
        if isinstance(node, nodes.Attribute):
            root, parts = self._attribute_parts(node)
            imported = context.imports.get(root)
            if not parts:
                return None
            if imported is None:
                local = context.symbols.get(root)
                if isinstance(local, nodes.ClassDef):
                    return context.module_path, f"{root}.{'.'.join(parts)}"
                return None

            module_name, imported_name = imported
            module_name = module_by_alias.get(module_name, module_name)
            if imported_name is not None:
                candidate_module = f"{module_name}.{imported_name}"
                if candidate_module in module_by_alias:
                    module_name = module_by_alias[candidate_module]
                    return module_name, parts[-1]
                return module_name, f"{imported_name}.{'.'.join(parts)}"

            if len(parts) > 1:
                candidate = f"{module_name}.{'.'.join(parts[:-1])}"
                if candidate in module_by_alias:
                    return module_by_alias[candidate], parts[-1]
                return module_name, f"{parts[-2]}.{parts[-1]}"
            return module_name, parts[-1]
        return None

    def _build_export_aliases(  # noqa: C901
        self,
        contexts: list[_ModuleContext],
        module_by_alias: dict[str, str],
    ) -> dict[tuple[str, str], tuple[str, str]]:
        aliases: dict[tuple[str, str], tuple[str, str]] = {}
        contexts_by_alias = {
            module_by_alias.get(context.module_path, context.module_path): context for context in contexts
        }

        def resolve(target: tuple[str, str]) -> tuple[str, str]:
            seen: set[tuple[str, str]] = set()
            while target in aliases and target not in seen:
                seen.add(target)
                target = aliases[target]
            return target

        # Package exports can be nested (for example package -> viewsets ->
        # concrete module).  Iterate until all wildcard and direct imports have
        # reached a fixed point instead of resolving only one re-export layer.
        for _ in range(len(contexts) + 1):
            changed = False
            for context in contexts:
                source_module = module_by_alias.get(context.module_path, context.module_path)
                for local_name, (module_name, imported_name) in context.imports.items():
                    target_module = module_by_alias.get(module_name, module_name)
                    if local_name == "*" or local_name.startswith("*:"):
                        target_context = contexts_by_alias.get(target_module)
                        if target_context is None:
                            continue
                        exported_names = set(target_context.symbols)
                        exported_names.update(
                            name for (export_module, name) in aliases if export_module == target_module
                        )
                        for exported_name in exported_names:
                            key = (source_module, exported_name)
                            target = resolve((target_module, exported_name))
                            if aliases.get(key) != target:
                                aliases[key] = target
                                changed = True
                        continue
                    if imported_name is None:
                        continue
                    key = (source_module, local_name)
                    target = resolve((target_module, imported_name))
                    if aliases.get(key) != target:
                        aliases[key] = target
                        changed = True
            if not changed:
                break
        return aliases

    def _is_view_class(
        self,
        node: nodes.ClassDef,
        context: _ModuleContext,
        symbol_index: dict[tuple[str, str], nodes.NodeNG],
        contexts_by_module: dict[str, _ModuleContext],
        module_by_alias: dict[str, str],
        cache: dict[tuple[str, str], bool],
        visiting: set[tuple[str, str]],
    ) -> bool:
        key = (context.module_path, node.name)
        if key in cache:
            return cache[key]
        if key in visiting:
            return False
        visiting.add(key)
        result = False
        for base in node.bases:
            base_name = self._base_name(base)
            if self._looks_like_view_base(base_name):
                result = True
                break
            imported = context.imports.get(base_name)
            target_key = None
            if imported and imported[1]:
                target_key = (module_by_alias.get(imported[0], imported[0]), imported[1])
            elif (context.module_path, base_name) in symbol_index:
                target_key = (context.module_path, base_name)
            if target_key and target_key in symbol_index and isinstance(symbol_index[target_key], nodes.ClassDef):
                target_context = contexts_by_module.get(target_key[0])
                if target_context is not None and self._is_view_class(
                    symbol_index[target_key],
                    target_context,
                    symbol_index,
                    contexts_by_module,
                    module_by_alias,
                    cache,
                    visiting,
                ):
                    result = True
                    break
        visiting.remove(key)
        cache[key] = result
        return result

    def _collect_imports(
        self,
        module: nodes.Module,
        module_path: str,
        is_package: bool = False,
    ) -> dict[str, tuple[str, str | None]]:
        imports: dict[str, tuple[str, str | None]] = {}
        import_context = f"{module_path}.__init__" if is_package else module_path
        for node in module.body:
            if isinstance(node, nodes.Import):
                for name in node.names:
                    imported_name, alias = name
                    local = alias or imported_name.split(".")[0]
                    imports[local] = (imported_name, None)
            elif isinstance(node, nodes.ImportFrom):
                base = self._relative_import_module(import_context, node.modname, node.level)
                for imported_name, alias in node.names:
                    if imported_name == "*":
                        imports[f"*:{len(imports)}"] = (base, None)
                        continue
                    local = alias or imported_name
                    if node.modname is None:
                        imports[local] = (f"{base}.{imported_name}" if base else imported_name, None)
                    else:
                        imports[local] = (base or imported_name, imported_name)
        return imports

    def _collect_symbols(self, module: nodes.Module) -> dict[str, nodes.NodeNG]:
        return {
            node.name: node
            for node in module.body
            if isinstance(node, (nodes.FunctionDef, nodes.ClassDef))
        }

    def _build_module_aliases(self, contexts: list[_ModuleContext]) -> dict[str, str]:
        alias_targets: dict[str, set[str]] = {}
        for context in contexts:
            for module_alias in self._module_aliases(context.module_path):
                alias_targets.setdefault(module_alias, set()).add(context.module_path)
        return {
            module_alias: next(iter(targets))
            for module_alias, targets in alias_targets.items()
            if len(targets) == 1
        }

    @staticmethod
    def _module_aliases(module_path: str) -> set[str]:
        parts = module_path.split(".")
        aliases = {module_path}
        for index in range(1, len(parts)):
            suffix = parts[index:]
            if all(part.isidentifier() for part in suffix):
                aliases.add(".".join(suffix))
        return aliases

    def _is_url_module(self, context: _ModuleContext) -> bool:
        if context.file_path.name == "urls.py":
            return True
        for node in context.module.nodes_of_class((nodes.Assign, nodes.AugAssign)):
            if not self._is_module_level(node, context.module):
                continue
            target = node.targets[0] if isinstance(node, nodes.Assign) and node.targets else node.target
            if isinstance(target, nodes.AssignName) and target.name == "urlpatterns":
                return True
        return any(
            isinstance(call.func, nodes.Attribute)
            and isinstance(call.func.expr, nodes.Name)
            and call.func.expr.name == "urlpatterns"
            and call.func.attrname in {"append", "extend"}
            and self._is_module_level(call, context.module)
            for call in context.module.nodes_of_class(nodes.Call)
        )

    @staticmethod
    def _is_module_level(node: nodes.NodeNG, module: nodes.Module) -> bool:
        return node.frame() is module

    def _class_attribute_values(self, node: nodes.NodeNG, name: str) -> list[str]:
        value = self._class_attribute_node(node, name)
        return self._string_values(value) if value is not None else []

    def _class_attribute_value(self, node: nodes.NodeNG, name: str) -> str | None:
        value = self._class_attribute_node(node, name)
        return self._expression(value) if value is not None else None

    def _class_attribute_node(self, node: nodes.NodeNG, name: str) -> nodes.NodeNG | None:
        for child in getattr(node, "body", []):
            if isinstance(child, nodes.Assign):
                if any(isinstance(target, nodes.AssignName) and target.name == name for target in child.targets):
                    return child.value
            elif isinstance(child, nodes.AnnAssign) and isinstance(child.target, nodes.AssignName) and child.target.name == name:
                return child.value
        return None

    def _model_references(self, node: nodes.NodeNG) -> list[str]:
        references: set[str] = set()
        for candidate in node.nodes_of_class(nodes.Attribute):
            if candidate.attrname == "objects":
                references.add(self._expression(candidate.expr))
        for call in node.nodes_of_class(nodes.Call):
            if self._call_name(call.func) == "get_object_or_404" and call.args:
                references.add(self._expression(call.args[0]))
        return sorted(reference for reference in references if reference)

    def _decorator_strings(self, node: nodes.NodeNG) -> list[str]:
        return [self._expression(decorator) for decorator in (node.decorators.nodes if node.decorators else [])]

    def _decorator_names(self, node: nodes.NodeNG) -> list[str]:
        return [self._decorator_name(decorator) for decorator in (node.decorators.nodes if node.decorators else [])]

    def _decorator_name(self, decorator: nodes.NodeNG) -> str:
        target = decorator.func if isinstance(decorator, nodes.Call) else decorator
        return self._call_name(target)

    def _is_explicit_function_view(self, decorator_names: list[str]) -> bool:
        return any(
            name
            in {
                "api_view",
                "login_exempt",
                "login_csrf_exempt",
                "csrf_exempt",
                "require_http_methods",
                "require_GET",
                "require_POST",
                "require_safe",
            }
            for name in decorator_names
        )

    def _security_evidence(self, decorator_names: list[str]) -> tuple[bool | None, bool | None]:
        lowered = {name.lower() for name in decorator_names}
        login = True if lowered.intersection({"login_exempt", "login_csrf_exempt"}) else None
        csrf = True if lowered.intersection({"csrf_exempt", "login_csrf_exempt"}) else None
        return login, csrf

    def _api_view_methods(self, node: nodes.FunctionDef) -> list[str]:
        for decorator in (node.decorators.nodes if node.decorators else []):
            if self._decorator_name(decorator) != "api_view" or not isinstance(decorator, nodes.Call):
                continue
            if decorator.args:
                return self._normalize_methods(self._string_values(decorator.args[0]))
        return []

    def _string_values(self, node: nodes.NodeNG) -> list[str]:
        if isinstance(node, (nodes.List, nodes.Tuple, nodes.Set)):
            values: list[str] = []
            for element in node.elts:
                value = self._literal_value(element)
                values.append(value if value is not None else self._expression(element))
            return values
        value = self._literal_value(node)
        return [value] if value is not None else [self._expression(node)]

    def _normalize_methods(self, methods: list[str]) -> list[str]:
        return sorted({method.upper() for method in methods if method.upper() in self._HTTP_METHODS})

    def _bool_value(self, node: nodes.NodeNG) -> bool | None:
        if isinstance(node, nodes.Const) and isinstance(node.value, bool):
            return node.value
        return None

    def _keyword_literal(self, call: nodes.Call, name: str) -> str | None:
        for keyword in call.keywords:
            if keyword.arg == name:
                return self._literal_value(keyword.value)
        return None

    def _literal_value(self, node: nodes.NodeNG) -> str | None:
        if isinstance(node, nodes.Const):
            return str(node.value) if node.value is not None else None
        return None

    def _expression(self, node: nodes.NodeNG | None) -> str:
        if node is None:
            return ""
        try:
            return node.as_string()
        except Exception:
            return str(node)

    def _call_name(self, node: nodes.NodeNG | None) -> str:
        if isinstance(node, nodes.Name):
            return node.name
        if isinstance(node, nodes.Attribute):
            return node.attrname
        return ""

    def _base_name(self, node: nodes.NodeNG) -> str:
        if isinstance(node, nodes.Name):
            return node.name
        if isinstance(node, nodes.Attribute):
            return node.attrname
        return self._expression(node).split(".")[-1]

    def _looks_like_view_base(self, name: str) -> bool:
        return name in self._VIEW_BASES or name.endswith("ViewSet") or name.endswith("APIView")

    def _looks_like_drf_base(self, name: str) -> bool:
        return name in {
            "APIView",
            "ViewSet",
            "GenericViewSet",
            "ModelViewSet",
            "ReadOnlyModelViewSet",
        } or name.endswith("ViewSet") or name.endswith("APIView")

    def _attribute_parts(self, node: nodes.Attribute) -> tuple[str, list[str]]:
        parts = [node.attrname]
        current = node.expr
        while isinstance(current, nodes.Attribute):
            parts.append(current.attrname)
            current = current.expr
        if isinstance(current, nodes.Name):
            parts.reverse()
            return current.name, parts
        return "", []

    def _relative_import_module(self, module_path: str, modname: str | None, level: int) -> str:
        if not level:
            return modname or ""
        parts = module_path.split(".")
        package = parts[: max(0, len(parts) - level)]
        if modname:
            package.extend(modname.split("."))
        return ".".join(package)

    def _source_file(self, file_path: Path, scan_root: Path) -> str:
        try:
            return str(file_path.relative_to(scan_root))
        except ValueError:
            return str(file_path)

    def _get_module_path(self, file_path: Path, base_path: Path) -> str:
        try:
            relative = file_path.relative_to(base_path)
            parts = [*relative.parts[:-1]]
            if relative.stem != "__init__":
                parts.append(relative.stem)
            return ".".join(parts)
        except ValueError:
            parts = [*file_path.parts[:-1]]
            if file_path.stem != "__init__":
                parts.append(file_path.stem)
            return ".".join(parts)

    @staticmethod
    def _unique(values: list[str]) -> list[str]:
        return list(dict.fromkeys(values))
