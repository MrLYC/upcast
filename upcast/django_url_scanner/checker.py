"""AST visitor for detecting Django URL patterns."""

import sys
from typing import Any

from astroid import nodes

from upcast.django_url_scanner.router_parser import parse_router_registrations
from upcast.django_url_scanner.url_parser import parse_url_pattern
from upcast.django_url_scanner.view_resolver import resolve_view


class UrlPatternChecker:
    """AST visitor that extracts Django URL patterns from Python modules."""

    def __init__(self, root_path: str | None = None, verbose: bool = False):
        """Initialize the checker.

        Args:
            root_path: Root path for calculating module names
            verbose: Enable verbose output
        """
        self.root_path = root_path
        self.verbose = verbose
        # Store URL patterns grouped by module path
        self.url_patterns: dict[str, list[dict[str, Any]]] = {}

    def visit_module(self, module: nodes.Module) -> None:
        """Visit a module and extract URL patterns.

        Args:
            module: The astroid Module node to visit
        """
        module_path = module.qname()

        # Find urlpatterns assignments
        for node in module.nodes_of_class(nodes.Assign):
            if self._is_urlpatterns_assignment(node):
                patterns = self._extract_url_patterns(node.value, module)
                if patterns:
                    if module_path not in self.url_patterns:
                        self.url_patterns[module_path] = []
                    self.url_patterns[module_path].extend(patterns)

    def get_url_patterns(self) -> dict[str, list[dict[str, Any]]]:
        """Get all collected URL patterns.

        Returns:
            Dictionary mapping module paths to lists of URL pattern dictionaries
        """
        return self.url_patterns

    def _is_urlpatterns_assignment(self, node: nodes.Assign) -> bool:
        """Check if an assignment is to 'urlpatterns'.

        Args:
            node: Assignment node to check

        Returns:
            True if this assigns to 'urlpatterns'
        """
        return any(isinstance(target, nodes.AssignName) and target.name == "urlpatterns" for target in node.targets)

    def _extract_url_patterns(self, value_node: nodes.NodeNG, module: nodes.Module) -> list[dict[str, Any]]:
        """Extract URL patterns from a value node.

        Args:
            value_node: The value being assigned to urlpatterns
            module: The module context

        Returns:
            List of URL pattern dictionaries
        """
        patterns = []

        # Check if this is a dynamic assignment (needs special marking)
        is_dynamic = self._is_dynamic_urlpatterns(value_node)

        if isinstance(value_node, (nodes.List, nodes.Tuple)):
            # Static list/tuple of patterns
            for element in value_node.elts:
                pattern = self._parse_route_element(element, module)
                if pattern:
                    # Check if this is a router include that should be expanded
                    if self._should_expand_router(pattern):
                        expanded = self._expand_router_include(pattern, module)
                        patterns.extend(expanded)
                    else:
                        patterns.append(pattern)
        elif isinstance(value_node, nodes.BinOp) and value_node.op == "+=":
            # urlpatterns += [...] - mark as dynamic
            patterns.append({
                "type": "dynamic",
                "pattern": "<extended>",
                "note": "URL patterns extended dynamically",
            })
        else:
            # Other expressions - might be dynamic
            if is_dynamic:
                patterns.append({
                    "type": "dynamic",
                    "pattern": "<generated>",
                    "note": "URL patterns generated dynamically",
                })

        return patterns

    def _is_dynamic_urlpatterns(self, node: nodes.NodeNG) -> bool:
        """Check if urlpatterns is dynamically generated.

        Detects patterns like:
        - List comprehensions
        - Generator expressions
        - Function calls that return lists
        - Loop-based construction

        Args:
            node: Node to check

        Returns:
            True if patterns appear to be dynamically generated
        """
        if isinstance(node, (nodes.ListComp, nodes.GeneratorExp)):
            return True
        # Function call that might return dynamic patterns
        return isinstance(node, nodes.Call)

    def _parse_route_element(self, element: nodes.NodeNG, module: nodes.Module) -> dict[str, Any] | None:
        """Parse a single route element (path(), re_path(), include(), etc.).

        Args:
            element: AST node representing a route definition
            module: The module context

        Returns:
            Dictionary with route information, or None if not a valid route
        """
        if not isinstance(element, nodes.Call):
            return None

        func_name = self._get_function_name(element.func)
        if not func_name:
            return None

        # Handle path() and re_path()
        if func_name in ("path", "re_path", "url"):
            return self._parse_path_call(element, module, func_name)

        return None

    def _get_function_name(self, func_node: nodes.NodeNG) -> str | None:
        """Get the function name from a call node.

        Args:
            func_node: Function node

        Returns:
            Function name or None
        """
        if isinstance(func_node, nodes.Name):
            return func_node.name
        elif isinstance(func_node, nodes.Attribute):
            return func_node.attrname
        return None

    def _parse_path_call(  # noqa: C901
        self, call_node: nodes.Call, module: nodes.Module, func_name: str
    ) -> dict[str, Any]:
        """Parse a path() or re_path() call.

        Args:
            call_node: The call node
            module: The module context
            func_name: Name of the function (path, re_path, url)

        Returns:
            Dictionary with URL pattern information
        """
        result: dict[str, Any] = {
            "type": "re_path" if func_name in ("re_path", "url") else "path",
            "pattern": None,
            "view_module": None,
            "view_name": None,
            "name": None,
            "description": None,
        }

        # Extract pattern string (first argument)
        if call_node.args and len(call_node.args) >= 1:
            pattern_node = call_node.args[0]
            if isinstance(pattern_node, nodes.Const):
                result["pattern"] = pattern_node.value

                # Parse pattern for converters/named groups
                pattern_info = parse_url_pattern(pattern_node.value)
                if pattern_info["converters"]:
                    result["converters"] = pattern_info["converters"]
                if pattern_info["named_groups"]:
                    result["named_groups"] = pattern_info["named_groups"]

        # Extract view (second argument)
        if call_node.args and len(call_node.args) >= 2:
            view_node = call_node.args[1]

            # Check if the view is an include() call
            if isinstance(view_node, nodes.Call):
                view_func_name = self._get_function_name(view_node.func)
                if view_func_name == "include":
                    # This is path(..., include(...))
                    result["type"] = "include"
                    include_info = self._parse_include_call(view_node, module)
                    result["include_module"] = include_info["include_module"]
                    if include_info.get("namespace"):
                        result["namespace"] = include_info["namespace"]
                    # Remove view-related fields since this is an include
                    result.pop("view_module", None)
                    result.pop("view_name", None)
                    result.pop("description", None)
                    # Extract name keyword argument for include
                    if call_node.keywords:
                        for keyword in call_node.keywords:
                            if keyword.arg == "name" and isinstance(keyword.value, nodes.Const):
                                result["name"] = keyword.value.value
                    return result

            # Normal view resolution
            view_info = resolve_view(view_node, module, self.verbose)

            result["view_module"] = view_info["view_module"]
            result["view_name"] = view_info["view_name"]
            result["description"] = view_info["description"]

            if not view_info["resolved"] and self.verbose:
                print(f"  Warning: Could not fully resolve view: {view_info['view_name']}", file=sys.stderr)

            # Mark special view types
            if view_info.get("is_partial"):
                result["is_partial"] = True
            if view_info.get("is_conditional"):
                result["is_conditional"] = True

        # Extract name keyword argument
        if call_node.keywords:
            for keyword in call_node.keywords:
                if keyword.arg == "name" and isinstance(keyword.value, nodes.Const):
                    result["name"] = keyword.value.value

        return result

    def _parse_include_call(self, call_node: nodes.Call, module: nodes.Module) -> dict[str, Any]:  # noqa: C901
        """Parse an include() call that appears as a view argument in path().

        Args:
            call_node: The include() call node
            module: The module context

        Returns:
            Dictionary with include information
        """
        result: dict[str, Any] = {
            "include_module": None,
            "namespace": None,
        }

        # The include() is typically inside a path() call
        # We need the parent context to get the pattern
        # For now, just extract the included module

        if call_node.args:
            first_arg = call_node.args[0]

            # Handle include("module.urls") or include(("module.urls", "namespace"))
            if isinstance(first_arg, nodes.Const):
                result["include_module"] = first_arg.value
            elif isinstance(first_arg, (nodes.Tuple, nodes.List)):
                # include((module, namespace))
                if first_arg.elts:
                    if isinstance(first_arg.elts[0], nodes.Const):
                        result["include_module"] = first_arg.elts[0].value
                    if len(first_arg.elts) > 1 and isinstance(first_arg.elts[1], nodes.Const):
                        result["namespace"] = first_arg.elts[1].value
            elif (
                isinstance(first_arg, nodes.Attribute)
                and first_arg.attrname == "urls"
                and isinstance(first_arg.expr, nodes.Name)
            ):
                # include(router.urls) - mark as router for expansion
                router_name = first_arg.expr.name
                result["include_module"] = f"<router:{router_name}>"

        # Check for namespace keyword argument
        if call_node.keywords:
            for keyword in call_node.keywords:
                if keyword.arg == "namespace" and isinstance(keyword.value, nodes.Const):
                    result["namespace"] = keyword.value.value

        return result

    def _should_expand_router(self, pattern: dict[str, Any]) -> bool:
        """Check if a pattern represents a router include that should be expanded.

        Args:
            pattern: Pattern dictionary

        Returns:
            True if this is a router include
        """
        if pattern.get("type") != "include":
            return False
        include_module = pattern.get("include_module", "")
        return isinstance(include_module, str) and include_module.startswith("<router:")

    def _expand_router_include(self, pattern: dict[str, Any], module: nodes.Module) -> list[dict[str, Any]]:
        """Expand a router include into individual ViewSet registrations.

        Args:
            pattern: Pattern dictionary with router include
            module: The module context

        Returns:
            List of expanded router registration patterns
        """
        include_module = pattern.get("include_module", "")
        # Extract router name from "<router:router_name>"
        router_name = include_module[8:-1]  # Remove "<router:" and ">"

        # Parse router registrations
        registrations = parse_router_registrations(module, router_name)

        if not registrations:
            # If we can't parse the router, return the original include
            return [pattern]

        # Build expanded patterns with the base path prefix
        base_pattern = pattern.get("pattern", "")
        expanded = []

        for reg in registrations:
            # Combine base pattern with registration pattern
            reg_pattern = reg.get("pattern", "")
            if base_pattern and base_pattern != "<root>":
                # Remove trailing slash from base if present
                base = base_pattern.rstrip("/")
                # Remove leading slash from registration if present
                reg_part = reg_pattern.lstrip("/") if reg_pattern else ""
                full_pattern = f"{base}/{reg_part}" if reg_part else base
            else:
                full_pattern = reg_pattern

            # Create pattern entry
            entry: dict[str, Any] = {
                "type": "router_registration",
                "pattern": full_pattern or "<root>",
                "viewset_module": reg.get("viewset_module"),
                "viewset_name": reg.get("viewset_name"),
            }

            # Add optional fields
            if reg.get("basename"):
                entry["basename"] = reg["basename"]
            if reg.get("router_type"):
                entry["router_type"] = reg["router_type"]
            if pattern.get("name"):
                entry["name"] = pattern["name"]

            expanded.append(entry)

        return expanded
