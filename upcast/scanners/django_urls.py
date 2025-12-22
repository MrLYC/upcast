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

        url_modules: dict[str, UrlModule] = {}

        for file_path in files:
            patterns = self._scan_file(file_path)
            if patterns:
                module_path = self._get_module_path(file_path, path)
                url_modules[module_path] = UrlModule(urlpatterns=patterns)

        scan_duration_ms = int((time.perf_counter() - start_time) * 1000)
        summary = self._calculate_summary(url_modules, scan_duration_ms)

        return DjangoUrlOutput(summary=summary, results=url_modules)

    def _scan_file(self, file_path: Path) -> list[UrlPattern]:
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
        for node in module.nodes_of_class(nodes.Assign):
            if self._is_urlpatterns_assignment(node):
                url_patterns = self._extract_url_patterns(node.value, module)
                patterns.extend(url_patterns)

        if self.verbose and patterns:
            logger.info(f"Found {len(patterns)} URL patterns in {file_path}")

        return patterns

    def _is_urlpatterns_assignment(self, node: nodes.Assign) -> bool:
        """Check if an assignment is to 'urlpatterns'.

        Args:
            node: Assignment node to check

        Returns:
            True if this assigns to 'urlpatterns'
        """
        return any(isinstance(target, nodes.AssignName) and target.name == "urlpatterns" for target in node.targets)

    def _extract_url_patterns(self, value_node: nodes.NodeNG, module: nodes.Module) -> list[UrlPattern]:
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
                    viewset_module=None,
                    viewset_name=None,
                    basename=None,
                    router_type=None,
                    is_partial=False,
                    is_conditional=False,
                    description=None,
                    note="URL patterns generated dynamically",
                )
            )
            return patterns

        if isinstance(value_node, (nodes.List, nodes.Tuple)):
            # Static list/tuple of patterns
            for element in value_node.elts:
                pattern_list = self._parse_route_element(element, module)  # type: ignore[arg-type]
                patterns.extend(pattern_list)

        return patterns

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

    def _parse_route_element(self, element: nodes.NodeNG, module: nodes.Module) -> list[UrlPattern]:
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
            pattern = self._parse_path_call(element, module, func_name)
            # Check if this is a router include that should be expanded
            if self._should_expand_router(pattern):
                return self._expand_router_include(pattern, module)
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

    def _parse_path_call(self, call_node: nodes.Call, module: nodes.Module, func_name: str) -> UrlPattern:  # noqa: C901
        """Parse a path() or re_path() call.

        Args:
            call_node: The call node
            module: The module context
            func_name: Name of the function (path, re_path, url)

        Returns:
            UrlPattern object
        """
        pattern_type = "re_path" if func_name in ("re_path", "url") else "path"
        pattern_str: str | None = None
        converters: list[str] = []
        named_groups: list[str] = []
        view_module: str | None = None
        view_name: str | None = None
        description: str | None = None
        name: str | None = None
        is_partial = False
        is_conditional = False
        include_module: str | None = None
        namespace: str | None = None

        # Extract pattern string (first argument)
        if call_node.args and len(call_node.args) >= 1:
            pattern_node = call_node.args[0]
            if isinstance(pattern_node, nodes.Const):
                pattern_str = str(pattern_node.value)

                # Parse pattern for converters/named groups
                pattern_info = parse_url_pattern(pattern_str)
                if pattern_info["converters"]:
                    converters = [f"{k}:{v}" for k, v in pattern_info["converters"].items()]
                if pattern_info["named_groups"]:
                    named_groups = pattern_info["named_groups"]

        # Extract view (second argument)
        if call_node.args and len(call_node.args) >= 2:
            view_node = call_node.args[1]

            # Check if the view is an include() call
            if isinstance(view_node, nodes.Call):
                view_func_name = self._get_function_name(view_node.func)
                if view_func_name == "include":
                    # This is path(..., include(...))
                    pattern_type = "include"
                    include_info = self._parse_include_call(view_node, module)
                    include_module = include_info["include_module"]
                    namespace = include_info.get("namespace")

                    # Extract name keyword argument for include
                    for keyword in call_node.keywords:
                        if keyword.arg == "name" and isinstance(keyword.value, nodes.Const):
                            name = str(keyword.value.value)

                    return UrlPattern(
                        type=pattern_type,
                        pattern=pattern_str,
                        view_module=None,
                        view_name=None,
                        include_module=include_module,
                        namespace=namespace,
                        name=name,
                        converters=[],
                        named_groups=[],
                        viewset_module=None,
                        viewset_name=None,
                        basename=None,
                        router_type=None,
                        is_partial=False,
                        is_conditional=False,
                        description=None,
                        note=None,
                    )

            # Normal view resolution
            view_info = resolve_view(view_node, module, self.verbose)
            view_module = view_info["view_module"]
            view_name = view_info["view_name"]
            description = view_info["description"]
            is_partial = view_info.get("is_partial", False)
            is_conditional = view_info.get("is_conditional", False)

        # Extract name keyword argument
        for keyword in call_node.keywords:
            if keyword.arg == "name" and isinstance(keyword.value, nodes.Const):
                name = str(keyword.value.value)

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
            viewset_module=None,
            viewset_name=None,
            basename=None,
            router_type=None,
            is_partial=is_partial,
            is_conditional=is_conditional,
            description=description,
            note=None,
        )

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

    def _expand_router_include(self, pattern: UrlPattern, module: nodes.Module) -> list[UrlPattern]:
        """Expand a router include into individual ViewSet registrations.

        Args:
            pattern: Pattern with router include
            module: The module context

        Returns:
            List of expanded router registration patterns
        """
        include_module = pattern.include_module or ""
        router_name = include_module[8:-1]  # Remove "<router:" and ">"

        registrations = parse_router_registrations(module, router_name)

        if not registrations:
            return [pattern]

        base_pattern = pattern.pattern or ""
        expanded: list[UrlPattern] = []

        for reg in registrations:
            reg_pattern = reg.get("pattern", "")
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
                    view_module=None,
                    view_name=None,
                    include_module=None,
                    namespace=None,
                    name=pattern.name,
                    converters=[],
                    named_groups=[],
                    viewset_module=reg.get("viewset_module"),
                    viewset_name=reg.get("viewset_name"),
                    basename=reg.get("basename"),
                    router_type=reg.get("router_type"),
                    is_partial=False,
                    is_conditional=False,
                    description=None,
                    note=None,
                )
            )

        return expanded

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
