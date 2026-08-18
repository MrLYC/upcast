"""Django URL pattern scanner.

This scanner analyzes Django URLconf modules to extract URL routing patterns,
including path(), re_path(), include(), and DRF router registrations.
"""

import logging
import time
from pathlib import Path

from astroid import nodes

from upcast.common.django.router_parser import parse_router_registrations
from upcast.common.django.url_parser import parse_url_pattern
from upcast.common.django.view_resolver import resolve_view
from upcast.common.hybrid_scan_pipeline import (
    LocateStage,
    MapStage,
    PipelineSpec,
    ProjectStage,
    run_pipeline,
)
from upcast.common.scanner_base import BaseScanner
from upcast.models.django_urls import DjangoUrlOutput, DjangoUrlSummary, UrlModule, UrlPattern

logger = logging.getLogger(__name__)


class DjangoUrlScanner(BaseScanner[DjangoUrlOutput]):
    """Scanner for Django URL patterns."""

    def __init__(
        self,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        verbose: bool = False,
    ):
        """Initialize Django URL scanner.

        Args:
            include_patterns: File patterns to include (default: urls.py files)
            exclude_patterns: File patterns to exclude
            verbose: Enable verbose logging
        """
        # Default to scanning urls.py files
        default_includes = ["**/urls.py", "urls.py"]
        include_patterns = include_patterns or default_includes

        super().__init__(
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            verbose=verbose,
        )

    def scan(self, path: Path) -> DjangoUrlOutput:
        """Scan path for Django URL patterns.

        Args:
            path: Directory or file to scan

        Returns:
            DjangoUrlOutput with all detected URL modules
        """
        start_time = time.perf_counter()
        files = self.get_files_to_scan(path)
        scan_root = path if path.is_dir() else path.parent

        url_modules: dict[str, UrlModule] = {}

        for file_path in files:
            patterns = self._scan_file(file_path, scan_root)
            if patterns:
                module_path = self._get_module_path(file_path, scan_root)
                url_modules[module_path] = UrlModule(urlpatterns=patterns)

        scan_duration_ms = int((time.perf_counter() - start_time) * 1000)
        summary = self._calculate_summary(url_modules, scan_duration_ms)

        return DjangoUrlOutput(summary=summary, results=url_modules, metadata={"scanner_name": "django-urls"})

    def _scan_file(self, file_path: Path, scan_root: Path) -> list[UrlPattern]:
        """Scan a single URLs file.

        Args:
            file_path: Path to the urls.py file

        Returns:
            List of detected URL patterns
        """
        module = self.parse_file(file_path)
        if not module:
            return []

        patterns: list[UrlPattern] = []

        # Find urlpatterns assignments
        for node in self._iter_candidate_urlpattern_assignments(module, file_path):
            url_patterns = self._extract_url_patterns(node.value, module, file_path, scan_root)
            patterns.extend(url_patterns)

        patterns.extend(self._extract_augmented_url_patterns(module, file_path, scan_root))
        patterns.extend(self._extract_mutated_url_patterns(module, file_path, scan_root))

        if self.verbose and patterns:
            logger.info(f"Found {len(patterns)} URL patterns in {file_path}")

        return patterns

    def _extract_mutated_url_patterns(
        self, module: nodes.Module, file_path: Path, scan_root: Path
    ) -> list[UrlPattern]:
        """Extract routes added through ``urlpatterns.append/extend``.

        Only modules with a real assignment or augmented assignment to
        ``urlpatterns`` are considered.  This avoids treating local helper
        variables with the same name as Django URLconfs.
        """
        has_urlpatterns_assignment = any(
            self._is_urlpatterns_assignment(node, module)
            for node in module.nodes_of_class((nodes.Assign, nodes.AugAssign))
        )
        if not has_urlpatterns_assignment:
            return []

        patterns: list[UrlPattern] = []
        for call in module.nodes_of_class(nodes.Call):
            if call.frame() is not module:
                continue
            if not isinstance(call.func, nodes.Attribute):
                continue
            if not isinstance(call.func.expr, nodes.Name) or call.func.expr.name != "urlpatterns":
                continue
            if not call.args or call.func.attrname not in {"append", "extend"}:
                continue
            elements = call.args if call.func.attrname == "append" else self._sequence_elements(call.args[0])
            for element in elements:
                patterns.extend(self._parse_route_element(element, module, file_path, scan_root))
        return patterns

    def _sequence_elements(self, node: nodes.NodeNG) -> list[nodes.NodeNG]:
        if isinstance(node, (nodes.List, nodes.Tuple, nodes.Set)):
            return list(node.elts)
        return [node]

    def _extract_augmented_url_patterns(
        self, module: nodes.Module, file_path: Path, scan_root: Path
    ) -> list[UrlPattern]:
        """Extract concrete routes appended to ``urlpatterns``.

        Django projects commonly initialize ``urlpatterns`` with an empty
        list and then append ``router.urls``.  The original list-only parser
        otherwise discarded those router registrations entirely.
        """
        patterns: list[UrlPattern] = []
        for node in module.nodes_of_class(nodes.AugAssign):
            if not self._is_urlpatterns_assignment(node, module):
                continue
            if node.op != "+=":
                continue
            if isinstance(node.value, (nodes.List, nodes.Tuple)):
                for element in node.value.elts:
                    patterns.extend(self._parse_route_element(element, module, file_path, scan_root))
                continue
            router_name = self._router_name(node.value)
            if router_name is not None:
                patterns.extend(
                    self._build_router_registration_patterns(
                        parse_router_registrations(
                            module, router_name, self._get_module_path(file_path, scan_root)
                        ),
                        base_pattern=None,
                        name=None,
                        file_path=file_path,
                        scan_root=scan_root,
                    )
                )
        return patterns

    def _iter_candidate_urlpattern_assignments(self, module: nodes.Module, file_path: Path) -> list[nodes.Assign]:
        """Discover urlpatterns assignments via hybrid pipeline with AST fallback."""
        fallback_nodes = [
            node for node in module.nodes_of_class(nodes.Assign) if self._is_urlpatterns_assignment(node, module)
        ]

        try:
            source = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return fallback_nodes

        try:
            pipeline_result = run_pipeline(
                spec=PipelineSpec(
                    name="scan-django-urls",
                    locate=LocateStage(pattern="urlpatterns = $VALUE"),
                    map=MapStage(),
                    semantic_filters=[],
                    project=ProjectStage(kind="django_urlpatterns_assignment"),
                ),
                source=source,
                file_path=str(file_path),
            )
        except Exception:
            return fallback_nodes

        selected_nodes: list[nodes.Assign] = []
        seen_node_ids: set[int] = set()

        for candidate, decision in zip(
            pipeline_result.candidates,
            pipeline_result.decisions,
            strict=True,
        ):
            if decision.status != "confirmed":
                continue

            node = candidate.captures.get("self")
            if not isinstance(node, nodes.Assign):
                continue
            if not self._is_urlpatterns_assignment(node, module):
                continue

            node_id = id(node)
            if node_id in seen_node_ids:
                continue

            selected_nodes.append(node)
            seen_node_ids.add(node_id)

        return selected_nodes or fallback_nodes

    def _is_urlpatterns_assignment(
        self, node: nodes.Assign | nodes.AugAssign, module: nodes.Module | None = None
    ) -> bool:
        """Check if an assignment is to 'urlpatterns'.

        Args:
            node: Assignment node to check

        Returns:
            True if this assigns to 'urlpatterns'
        """
        if module is not None and node.frame() is not module:
            return False
        target = node.targets[0] if isinstance(node, nodes.Assign) and node.targets else node.target
        return isinstance(target, nodes.AssignName) and target.name == "urlpatterns"

    def _extract_url_patterns(
        self, value_node: nodes.NodeNG, module: nodes.Module, file_path: Path, scan_root: Path
    ) -> list[UrlPattern]:
        """Extract URL patterns from a value node.

        Args:
            value_node: The value being assigned to urlpatterns
            module: The module context

        Returns:
            List of URL patterns
        """
        patterns: list[UrlPattern] = []

        # Check if this is a dynamic assignment
        if self._is_dynamic_urlpatterns(value_node):
            patterns.append(
                UrlPattern(
                    type="dynamic",
                    pattern="<generated>",
                    view_module=None,
                    view_name=None,
                    include_module=None,
                    namespace=None,
                    name=None,
                    converters=[],
                    named_groups=[],
                    basename=None,
                    router_type=None,
                    is_partial=False,
                    is_conditional=False,
                    description=None,
                    note="URL patterns generated dynamically",
                    file=self._get_source_file(file_path, scan_root),
                    line=getattr(value_node, "lineno", None),
                )
            )
            return patterns

        if isinstance(value_node, nodes.BinOp) and value_node.op == "+":
            return self._extract_url_patterns(value_node.left, module, file_path, scan_root) + self._extract_url_patterns(
                value_node.right, module, file_path, scan_root
            )

        if isinstance(value_node, (nodes.List, nodes.Tuple)):
            # Static list/tuple of patterns
            for element in value_node.elts:
                pattern_list = self._parse_route_element(element, module, file_path, scan_root)  # type: ignore[arg-type]
                patterns.extend(pattern_list)

        router_name = self._router_name(value_node)
        if router_name is not None:
            return self._build_router_registration_patterns(
                parse_router_registrations(module, router_name, self._get_module_path(file_path, scan_root)),
                base_pattern=None,
                name=None,
                file_path=file_path,
                scan_root=scan_root,
            )

        return patterns

    def _router_name(self, node: nodes.NodeNG) -> str | None:
        if isinstance(node, nodes.Attribute) and node.attrname == "urls" and isinstance(node.expr, nodes.Name):
            return node.expr.name
        return None

    def _is_dynamic_urlpatterns(self, node: nodes.NodeNG) -> bool:
        """Check if urlpatterns is dynamically generated.

        Args:
            node: Node to check

        Returns:
            True if patterns appear to be dynamically generated
        """
        if isinstance(node, (nodes.ListComp, nodes.GeneratorExp)):
            return True
        return isinstance(node, nodes.Call)

    def _parse_route_element(
        self, element: nodes.NodeNG, module: nodes.Module, file_path: Path, scan_root: Path
    ) -> list[UrlPattern]:
        """Parse a single route element (path(), re_path(), include(), etc.).

        Args:
            element: AST node representing a route definition
            module: The module context

        Returns:
            List of URL patterns (may expand router includes)
        """
        if not isinstance(element, nodes.Call):
            return []

        func_name = self._get_function_name(element.func)
        if not func_name:
            return []

        # Handle path() and re_path()
        if func_name in ("path", "re_path", "url"):
            inline_patterns = self._expand_inline_include(element, module, file_path, scan_root)
            if inline_patterns is not None:
                return inline_patterns

            pattern = self._parse_path_call(element, module, func_name, file_path, scan_root)
            # Check if this is a router include that should be expanded
            if self._should_expand_router(pattern):
                return self._expand_router_include(pattern, module, file_path, scan_root)
            return [pattern]

        return []

    def _get_function_name(self, func_node: nodes.NodeNG) -> str | None:
        """Get the function name from a call node.

        Args:
            func_node: Function node

        Returns:
            Function name or None
        """
        if isinstance(func_node, nodes.Name):
            return func_node.name
        if isinstance(func_node, nodes.Attribute):
            return func_node.attrname
        return None

    def _parse_path_call(
        self, call_node: nodes.Call, module: nodes.Module, func_name: str, file_path: Path, scan_root: Path
    ) -> UrlPattern:
        """Parse a path() or re_path() call.

        Args:
            call_node: The call node
            module: The module context
            func_name: Name of the function (path, re_path, url)

        Returns:
            UrlPattern object
        """
        pattern_type = "re_path" if func_name in ("re_path", "url") else "path"
        source_file = self._get_source_file(file_path, scan_root)
        line = getattr(call_node, "lineno", None)
        pattern_str, converters, named_groups = self._extract_path_pattern_metadata(call_node)
        name = self._extract_pattern_name(call_node)

        include_pattern = self._build_include_pattern(call_node, module, pattern_str, name, source_file, line)
        if include_pattern is not None:
            return include_pattern

        view_module, view_name, description, is_partial, is_conditional = self._resolve_path_view(call_node, module)

        return UrlPattern(
            type=pattern_type,
            pattern=pattern_str,
            view_module=view_module,
            view_name=view_name,
            include_module=None,
            namespace=None,
            name=name,
            converters=converters,
            named_groups=named_groups,
            basename=None,
            router_type=None,
            is_partial=is_partial,
            is_conditional=is_conditional,
            description=description,
            note=None,
            file=source_file,
            line=line,
            full_path=pattern_str,
        )

    def _extract_path_pattern_metadata(self, call_node: nodes.Call) -> tuple[str | None, list[str], list[str]]:
        """Extract the route string plus converters and named groups."""
        if not call_node.args:
            return None, [], []

        pattern_node = call_node.args[0]
        if not isinstance(pattern_node, nodes.Const):
            return None, [], []

        pattern_str = str(pattern_node.value)
        pattern_info = parse_url_pattern(pattern_str)
        converters = [f"{k}:{v}" for k, v in pattern_info["converters"].items()]
        named_groups = pattern_info["named_groups"] or []
        return pattern_str, converters, named_groups

    def _extract_pattern_name(self, call_node: nodes.Call) -> str | None:
        """Extract the optional route name keyword from a path call."""
        for keyword in call_node.keywords:
            if keyword.arg == "name" and isinstance(keyword.value, nodes.Const):
                return str(keyword.value.value)
        return None

    def _build_include_pattern(
        self,
        call_node: nodes.Call,
        module: nodes.Module,
        pattern_str: str | None,
        name: str | None,
        source_file: str,
        line: int | None,
    ) -> UrlPattern | None:
        """Build a UrlPattern for path(..., include(...)) calls."""
        view_node = self._get_include_view_call(call_node)
        if view_node is None:
            return None

        include_info = self._parse_include_call(view_node, module)
        return UrlPattern(
            type="include",
            pattern=pattern_str,
            view_module=None,
            view_name=None,
            include_module=include_info["include_module"],
            namespace=include_info.get("namespace"),
            name=name,
            converters=[],
            named_groups=[],
            basename=None,
            router_type=None,
            is_partial=False,
            is_conditional=False,
            description=None,
            note=None,
            file=source_file,
            line=line,
            full_path=pattern_str,
        )

    def _resolve_path_view(
        self, call_node: nodes.Call, module: nodes.Module
    ) -> tuple[str | None, str | None, str | None, bool, bool]:
        """Resolve normal path view metadata for non-include routes."""
        view_node = self._get_path_view_node(call_node)
        if view_node is None:
            return None, None, None, False, False

        view_info = resolve_view(view_node, module, self.verbose)
        return (
            view_info["view_module"],
            view_info["view_name"],
            view_info["description"],
            view_info.get("is_partial", False),
            view_info.get("is_conditional", False),
        )

    def _get_path_view_node(self, call_node: nodes.Call) -> nodes.NodeNG | None:
        """Return the second positional argument from a path-like call."""
        if len(call_node.args) < 2:
            return None
        return call_node.args[1]

    def _get_include_view_call(self, call_node: nodes.Call) -> nodes.Call | None:
        """Return the include() call used as the second argument, if present."""
        view_node = self._get_path_view_node(call_node)
        if not isinstance(view_node, nodes.Call):
            return None
        func_node = getattr(view_node, "func", None)
        if func_node is None:
            return None
        if self._get_function_name(func_node) != "include":
            return None
        return view_node

    def _parse_include_call(self, call_node: nodes.Call, module: nodes.Module) -> dict[str, str | None]:
        """Parse an include() call.

        Args:
            call_node: The include() call node
            module: The module context

        Returns:
            Dictionary with include_module and namespace
        """
        result: dict[str, str | None] = {
            "include_module": None,
            "namespace": None,
        }

        if call_node.args:
            first_arg = call_node.args[0]

            # Handle include("module.urls") or include(("module.urls", "namespace"))
            if isinstance(first_arg, nodes.Const):
                result["include_module"] = str(first_arg.value)
            elif isinstance(first_arg, (nodes.Tuple, nodes.List)):
                # include((module, namespace))
                if first_arg.elts:
                    if isinstance(first_arg.elts[0], nodes.Const):
                        result["include_module"] = str(first_arg.elts[0].value)
                    if len(first_arg.elts) > 1 and isinstance(first_arg.elts[1], nodes.Const):
                        result["namespace"] = str(first_arg.elts[1].value)
            elif (
                isinstance(first_arg, nodes.Attribute)
                and first_arg.attrname == "urls"
                and isinstance(first_arg.expr, nodes.Name)
            ):
                # include(router.urls) - mark as router for expansion
                router_name = first_arg.expr.name
                result["include_module"] = f"<router:{router_name}>"

        # Check for namespace keyword argument
        for keyword in call_node.keywords:
            if keyword.arg == "namespace" and isinstance(keyword.value, nodes.Const):
                result["namespace"] = str(keyword.value.value)

        return result

    def _should_expand_router(self, pattern: UrlPattern) -> bool:
        """Check if a pattern represents a router include.

        Args:
            pattern: URL pattern

        Returns:
            True if this is a router include
        """
        if pattern.type != "include":
            return False
        include_module = pattern.include_module or ""
        return include_module.startswith("<router:")

    def _expand_router_include(
        self, pattern: UrlPattern, module: nodes.Module, file_path: Path, scan_root: Path
    ) -> list[UrlPattern]:
        """Expand a router include into individual ViewSet registrations.

        Args:
            pattern: Pattern with router include
            module: The module context

        Returns:
            List of expanded router registration patterns
        """
        include_module = pattern.include_module or ""
        router_name = include_module[8:-1]  # Remove "<router:" and ">"

        registrations = parse_router_registrations(
            module, router_name, self._get_module_path(file_path, scan_root)
        )
        if not registrations:
            pattern.include_module = f"{router_name}.urls"
            return [pattern]
        return self._build_router_registration_patterns(
            registrations,
            base_pattern=pattern.pattern,
            name=pattern.name,
            file_path=file_path,
            scan_root=scan_root,
        )

    def _build_router_registration_patterns(
        self,
        registrations: list[dict[str, object]],
        *,
        base_pattern: str | None,
        name: str | None,
        file_path: Path,
        scan_root: Path,
    ) -> list[UrlPattern]:
        if not registrations:
            return []

        expanded: list[UrlPattern] = []
        for registration in registrations:
            reg_pattern = str(registration.get("pattern") or "")
            if base_pattern and base_pattern != "<root>":
                base = base_pattern.rstrip("/")
                reg_part = reg_pattern.lstrip("/") if reg_pattern else ""
                full_pattern = f"{base}/{reg_part}" if reg_part else base
            else:
                full_pattern = reg_pattern

            expanded.append(
                UrlPattern(
                    type="router_registration",
                    pattern=full_pattern or "<root>",
                    view_module=registration.get("viewset_module"),
                    view_name=registration.get("viewset_name"),
                    include_module=None,
                    namespace=None,
                    name=name,
                    converters=[],
                    named_groups=[],
                    basename=registration.get("basename"),
                    router_type=registration.get("router_type"),
                    is_partial=False,
                    is_conditional=False,
                    description=None,
                    note=None,
                    file=self._get_source_file(file_path, scan_root),
                    line=registration.get("line"),
                    full_path=full_pattern or "<root>",
                )
            )
        return expanded

    def _expand_inline_include(
        self, call_node: nodes.Call, module: nodes.Module, file_path: Path, scan_root: Path
    ) -> list[UrlPattern] | None:
        """Expand inline include([...]) patterns into concrete child paths."""
        if len(call_node.args) < 2:
            return None

        view_node = call_node.args[1]
        if not isinstance(view_node, nodes.Call):
            return None

        if self._get_function_name(view_node.func) != "include":
            return None

        if not view_node.args:
            return None

        first_arg = view_node.args[0]
        if not isinstance(first_arg, (nodes.List, nodes.Tuple)):
            return None

        # Preserve existing tuple(module, namespace) include handling.
        if (
            isinstance(first_arg, nodes.Tuple)
            and len(first_arg.elts) >= 2
            and isinstance(first_arg.elts[0], (nodes.Const, nodes.JoinedStr))
        ):
            return None

        parent_prefix = ""
        if isinstance(call_node.args[0], nodes.Const):
            parent_prefix = str(call_node.args[0].value)

        expanded: list[UrlPattern] = []
        for element in first_arg.elts:
            expanded.extend(self._parse_route_element(element, module, file_path, scan_root))

        for pattern in expanded:
            child_path = pattern.full_path or pattern.pattern or ""
            pattern.full_path = self._join_full_path(parent_prefix, child_path)

        return expanded

    def _join_full_path(self, prefix: str | None, child: str | None) -> str | None:
        """Join parent and child URL path fragments."""
        if child == "<root>":
            child = ""

        if prefix is None and child is None:
            return None
        if not prefix:
            return child
        if not child:
            return prefix

        joined = f"{prefix.rstrip('/')}/{child.lstrip('/')}"
        if child.endswith("/") and not joined.endswith("/"):
            joined = f"{joined}/"
        return joined

    def _get_source_file(self, file_path: Path, scan_root: Path) -> str:
        """Get a stable source file path for pattern metadata."""
        try:
            return str(file_path.relative_to(scan_root))
        except ValueError:
            return str(file_path)

    def _get_module_path(self, file_path: Path, base_path: Path) -> str:
        """Get module path from file path.

        Args:
            file_path: Path to the file
            base_path: Base path for relative calculation

        Returns:
            Module path string (e.g., 'myapp.urls')
        """
        try:
            # Try to get relative path
            rel_path = file_path.relative_to(base_path)
            # Convert to module path: path/to/urls.py -> path.to.urls
            module_parts = [*rel_path.parts[:-1], rel_path.stem]
            return ".".join(module_parts)
        except ValueError:
            # File is not under base_path, use absolute
            module_parts = [*file_path.parts[:-1], file_path.stem]
            return ".".join(module_parts)

    def _calculate_summary(self, url_modules: dict[str, UrlModule], scan_duration_ms: int) -> DjangoUrlSummary:
        """Calculate summary statistics.

        Args:
            url_modules: URL modules dictionary
            scan_duration_ms: Time taken to scan in milliseconds

        Returns:
            Summary statistics
        """
        total_modules = len(url_modules)
        total_patterns = sum(len(module.urlpatterns) for module in url_modules.values())

        return DjangoUrlSummary(
            total_count=total_patterns,
            files_scanned=total_modules,
            scan_duration_ms=scan_duration_ms,
            total_modules=total_modules,
            total_patterns=total_patterns,
        )
