"""HTTP requests scanner implementation with Pydantic models."""

import time
from pathlib import Path
from typing import Any, ClassVar

from astroid import nodes

from upcast.common.ast_utils import get_import_info, safe_as_string, safe_infer_value
from upcast.common.file_utils import get_relative_path_str
from upcast.common.scanner_base import BaseScanner
from upcast.models.http_requests import HttpRequestInfo, HttpRequestOutput, HttpRequestSummary, HttpRequestUsage


class HttpRequestsScanner(BaseScanner[HttpRequestOutput]):
    """Scanner for HTTP request patterns (requests, httpx, aiohttp, urllib)."""

    # HTTP libraries and their request methods
    HTTP_LIBRARIES: ClassVar[dict[str, list[str]]] = {
        "requests": ["get", "post", "put", "patch", "delete", "head", "options", "request"],
        "httpx": ["get", "post", "put", "patch", "delete", "head", "options", "request"],
        "aiohttp": ["get", "post", "put", "patch", "delete", "head", "options", "request"],
        "urllib.request": ["urlopen", "Request"],
    }

    def scan(self, path: Path) -> HttpRequestOutput:
        """Scan for HTTP request patterns."""
        start_time = time.time()
        files = self.get_files_to_scan(path)
        base_path = path if path.is_dir() else path.parent

        requests_by_url: dict[str, list[HttpRequestUsage]] = {}

        for file_path in files:
            module = self.parse_file(file_path)
            if not module:
                continue

            imports = get_import_info(module)
            rel_path = get_relative_path_str(file_path, base_path)

            for node in module.nodes_of_class(nodes.Call):
                usage = self._check_request_call(node, rel_path, imports)
                if usage:
                    url = self._extract_url_with_imports(node, imports) or "..."
                    if url not in requests_by_url:
                        requests_by_url[url] = []
                    requests_by_url[url].append(usage)

        # Aggregate by URL
        requests_info = self._aggregate_requests(requests_by_url)
        scan_duration_ms = int((time.time() - start_time) * 1000)
        summary = self._calculate_summary(requests_info, scan_duration_ms)

        return HttpRequestOutput(summary=summary, results=requests_info)

    def _extract_url_with_imports(self, node: nodes.Call, imports: dict[str, str]) -> str | None:
        """Extract URL from request call with import context.

        Args:
            node: Call node
            imports: Import information from the module

        Returns:
            URL string or None
        """
        func = node.func
        is_request_constructor = self._is_request_constructor(func, imports)

        # Try extracting from keyword args first (works for all cases)
        for keyword in node.keywords or []:
            if keyword.arg == "url":
                return self._extract_url_from_node(keyword.value, node)

        # Try extracting from positional args
        if node.args:
            # For Request constructor: URL is second argument (index 1)
            # For other methods: URL is first argument (index 0)
            url_index = 1 if is_request_constructor else 0
            if len(node.args) > url_index:
                url_node = node.args[url_index]
                return self._extract_url_from_node(url_node, node)

        return None

    def _check_request_call(self, node: nodes.Call, file_path: str, imports: dict[str, str]) -> HttpRequestUsage | None:
        """Check if call is an HTTP request."""
        func = node.func
        library, method = self._identify_request(func, imports)

        if not library:
            return None

        if not method:
            return None

        # For Request constructors, extract method from first argument
        actual_method = method
        if self._is_request_constructor(func, imports):
            actual_method = self._extract_method_from_request_constructor(node)
            if not actual_method:
                actual_method = method

        return HttpRequestUsage(
            file=file_path,
            line=node.lineno if hasattr(node, "lineno") else None,
            statement=safe_as_string(node),
            method=actual_method.upper(),
            params=self._extract_params(node),
            headers=self._extract_headers(node),
            json_body=self._extract_json_body(node),
            data=self._extract_data(node),
            timeout=self._extract_timeout(node),
            session_based="Session" in safe_as_string(func),
            is_async=library == "aiohttp" or "async" in safe_as_string(func),
        )

    def _extract_method_from_request_constructor(self, node: nodes.Call) -> str | None:
        """Extract HTTP method from Request constructor.

        Handles:
        - Request('GET', url) - positional
        - Request(method='GET', url=url) - keyword
        - Request('GET', url=url) - mixed

        Args:
            node: Call node for Request constructor

        Returns:
            HTTP method string or None
        """
        # Check keyword arguments first
        for keyword in node.keywords or []:
            if keyword.arg == "method":
                method_value = safe_infer_value(keyword.value)
                if isinstance(method_value, str):
                    return method_value

        # Check first positional argument
        if node.args and len(node.args) > 0:
            method_value = safe_infer_value(node.args[0])
            if isinstance(method_value, str):
                return method_value

        return None

    def _identify_request(self, func_node: nodes.NodeNG, imports: dict[str, str]) -> tuple[str | None, str | None]:
        """Identify HTTP library and method."""
        if isinstance(func_node, nodes.Attribute):
            method = func_node.attrname
            if isinstance(func_node.expr, nodes.Name):
                module = imports.get(func_node.expr.name, func_node.expr.name)
                for lib, methods in self.HTTP_LIBRARIES.items():
                    if lib in module and method in methods:
                        return lib, method
        elif isinstance(func_node, nodes.Name):
            func_name = func_node.name
            qualified = imports.get(func_name, func_name)
            for lib, methods in self.HTTP_LIBRARIES.items():
                if lib in qualified and any(m in qualified for m in methods):
                    return lib, func_name
        return None, None

    def _is_request_constructor(self, func_node: nodes.NodeNG, imports: dict[str, str]) -> bool:
        """Check if the call is a Request constructor.

        Request constructors have signature: Request(method, url, ...)
        where the first argument is the HTTP method and second is the URL.

        Args:
            func_node: Function node to check
            imports: Import information

        Returns:
            True if this is a Request constructor call
        """
        if isinstance(func_node, nodes.Name):
            func_name = func_node.name
            qualified = imports.get(func_name, func_name)
            # Check for requests.Request or urllib.request.Request
            return "Request" in qualified and func_name == "Request"
        return False

    def _extract_url_from_node(self, url_node: nodes.NodeNG, context_node: nodes.Call) -> str | None:
        """Extract URL from a node, with context inference.

        Args:
            url_node: The node representing the URL
            context_node: The Call node for context lookup

        Returns:
            URL string or pattern (with consecutive ... merged), or None if URL contains Uninferable
        """
        # Try to infer from context (variable assignments)
        inferred_url = self._infer_url_from_context(url_node, context_node)
        if inferred_url:
            # Filter out URLs containing "Uninferable" - replace with ...
            inferred_url = self._clean_uninferable(inferred_url)
            return self._merge_consecutive_dots(inferred_url)

        # Check if it's a dynamic construction (prioritize pattern detection)
        if self._is_dynamic_url(url_node):
            pattern = self._normalize_url_pattern(url_node)
            if pattern:
                # Filter out "Uninferable" strings
                pattern = self._clean_uninferable(pattern)
                return self._merge_consecutive_dots(pattern)

        # Fall back to literal inference for static URLs
        url_value = safe_infer_value(url_node)
        if isinstance(url_value, str):
            # Filter out "Uninferable"
            if "Uninferable" in url_value:
                return None
            return url_value

        return None

    @staticmethod
    def _clean_uninferable(url: str) -> str:
        """Replace 'Uninferable' with '...' in URL patterns.

        Args:
            url: URL pattern that may contain 'Uninferable'

        Returns:
            URL with 'Uninferable' replaced by '...'
        """
        return url.replace("Uninferable", "...")

    @staticmethod
    def _merge_consecutive_dots(url: str) -> str:
        """Merge consecutive ... patterns into a single ...

        Since ... represents dynamic content, multiple consecutive ...
        can be simplified to a single ...

        Args:
            url: URL pattern that may contain multiple ...

        Returns:
            URL with consecutive ... merged

        Examples:
            >>> _merge_consecutive_dots("...:...")
            '...:...'
            >>> _merge_consecutive_dots("......")
            '...'
            >>> _merge_consecutive_dots(".../...")
            '.../...'
            >>> _merge_consecutive_dots("........./......")
            '.../...'
        """
        import re

        # Replace multiple consecutive dots (4 or more) with just ...
        # But preserve patterns like .../... or ...:...
        # Pattern: Replace 4+ dots that are not separated by / or : with ...
        return re.sub(r"\.{4,}", "...", url)

    def _infer_url_from_context(self, url_node: nodes.NodeNG, context_node: nodes.Call) -> str | None:
        """Try to infer URL by looking up variable definitions in context.

        Args:
            url_node: The node representing the URL
            context_node: The Call node for context lookup

        Returns:
            Inferred URL string or None
        """
        # If it's a Name node (variable reference), try to find its assignment
        if isinstance(url_node, nodes.Name):
            # Look for assignments in the same scope
            scope = context_node.scope()
            if scope:
                for node in scope.body:
                    if isinstance(node, nodes.Assign):
                        for target in node.targets:
                            if isinstance(target, nodes.AssignName) and target.name == url_node.name:
                                # Found the assignment, recursively extract from value
                                return self._extract_url_from_node(node.value, context_node)

        # If it's a formatted string or concatenation with resolvable parts
        if isinstance(url_node, (nodes.BinOp, nodes.JoinedStr)):
            # Try to partially resolve it
            partial_url = self._try_partial_resolution(url_node, context_node)
            if partial_url:
                return partial_url

        return None

    def _is_dynamic_url(self, node: nodes.NodeNG) -> bool:
        """Check if URL construction is dynamic.

        Args:
            node: AST node representing the URL expression

        Returns:
            True if the URL is dynamically constructed
        """
        # BinOp indicates concatenation or formatting
        if isinstance(node, (nodes.BinOp, nodes.JoinedStr)):
            return True

        # .format() calls
        if isinstance(node, nodes.Call) and isinstance(node.func, nodes.Attribute) and node.func.attrname == "format":
            return True

        # Variable/attribute references (not Const)
        return isinstance(node, (nodes.Name, nodes.Attribute))

    def _normalize_url_pattern(self, node: nodes.NodeNG) -> str | None:
        """Normalize dynamic URL construction into a pattern.

        Recognizes common URL construction patterns and normalizes them while
        preserving static path components:
        - String concatenation: base + "/api" → ".../api"
        - F-strings: f"{base}/api" → ".../api" or f"{proto}://{host}/path" → "...://.../path"
        - Format strings: "{}/api".format(base) → ".../api"
        - Query params: url + "?" + params → "...?..."

        Args:
            node: AST node representing the URL expression

        Returns:
            Normalized pattern string with static parts preserved or None
        """
        # Handle string concatenation (BinOp with '+')
        if isinstance(node, nodes.BinOp) and node.op == "+":
            return self._normalize_binop_url(node)

        # Handle f-strings (JoinedStr)
        if isinstance(node, nodes.JoinedStr):
            return self._normalize_fstring_url(node)

        # Handle .format() calls
        if isinstance(node, nodes.Call) and isinstance(node.func, nodes.Attribute) and node.func.attrname == "format":
            # Try to extract the template string
            if isinstance(node.func.expr, nodes.Const):
                template = node.func.expr.value
                if isinstance(template, str):
                    # Replace {} placeholders with ...
                    import re

                    pattern = re.sub(r"\{[^}]*\}", "...", template)
                    return pattern
            return "..."

        # Handle % formatting
        if isinstance(node, nodes.BinOp) and node.op == "%":
            # Try to extract the template string
            if isinstance(node.left, nodes.Const) and isinstance(node.left.value, str):
                template = node.left.value
                # Replace %s, %d, etc. with ...
                import re

                pattern = re.sub(r"%[sd]", "...", template)
                return pattern
            return "..."

        return None

    def _normalize_binop_url(self, node: nodes.BinOp) -> str:
        """Normalize BinOp (string concatenation) URL.

        Recursively processes concatenations to preserve static parts.

        Args:
            node: BinOp node with '+' operator

        Returns:
            Normalized URL pattern
        """
        parts = []
        self._collect_binop_parts(node, parts)

        # Convert parts to pattern
        result_parts = []
        for part in parts:
            if isinstance(part, str):
                # Static string - preserve it
                result_parts.append(part)
            else:
                # Dynamic part - replace with ...
                result_parts.append("...")

        url = "".join(result_parts)

        # Check for query params
        if "?" in url:
            return "...?..."

        return url

    def _collect_binop_parts(self, node: nodes.NodeNG, parts: list) -> None:
        """Recursively collect parts from BinOp concatenation.

        Args:
            node: Current node
            parts: List to collect parts into (str for static, NodeNG for dynamic)
        """
        if isinstance(node, nodes.BinOp) and node.op == "+":
            self._collect_binop_parts(node.left, parts)
            self._collect_binop_parts(node.right, parts)
        elif isinstance(node, nodes.Const) and isinstance(node.value, str):
            parts.append(node.value)
        else:
            # Dynamic part (variable, call, etc.)
            parts.append(node)

    def _normalize_fstring_url(self, node: nodes.JoinedStr) -> str:
        """Normalize f-string URL.

        Preserves static string parts and replaces FormattedValue parts with '...'.
        Detects common patterns like f"{proto}://{host}/path".

        Args:
            node: JoinedStr node (f-string)

        Returns:
            Normalized URL pattern
        """
        parts = []
        for value in node.values:
            if isinstance(value, nodes.Const):
                # Static part - preserve it
                parts.append(str(value.value))
            else:
                # Dynamic part (FormattedValue) - replace with ...
                parts.append("...")

        url = "".join(parts)

        # Check for query params
        if "?" in url or "params" in url.lower():
            return "...?..."

        return url

    def _try_partial_resolution(self, node: nodes.NodeNG, context_node: nodes.Call) -> str | None:  # noqa: C901
        """Try to partially resolve a URL by looking up some variables.

        Args:
            node: URL expression node
            context_node: Call node for context

        Returns:
            Partially resolved URL pattern or None
        """
        # For BinOp, try to resolve each part
        if isinstance(node, nodes.BinOp) and node.op == "+":
            parts = []
            self._collect_binop_parts(node, parts)

            resolved_parts = []
            for part in parts:
                if isinstance(part, str):
                    resolved_parts.append(part)
                elif isinstance(part, nodes.Name):
                    # Try to resolve variable
                    resolved = self._resolve_variable(part.name, context_node)
                    if resolved:
                        resolved_parts.append(resolved)
                    else:
                        resolved_parts.append("...")
                else:
                    resolved_parts.append("...")

            return "".join(resolved_parts)

        # For f-strings, try to resolve variables
        if isinstance(node, nodes.JoinedStr):
            parts = []
            for value in node.values:
                if isinstance(value, nodes.Const):
                    parts.append(str(value.value))
                elif isinstance(value, nodes.FormattedValue):
                    # Try to resolve the value
                    if isinstance(value.value, nodes.Name):
                        resolved = self._resolve_variable(value.value.name, context_node)
                        if resolved:
                            parts.append(resolved)
                        else:
                            parts.append("...")
                    elif isinstance(value.value, nodes.Attribute):
                        # For attribute access (e.g., settings.URL), try to infer
                        attr_value = safe_infer_value(value.value)
                        # Only use if it's a valid string and doesn't contain "Uninferable"
                        if isinstance(attr_value, str) and "Uninferable" not in attr_value:
                            parts.append(attr_value)
                        else:
                            parts.append("...")
                    else:
                        parts.append("...")
                else:
                    parts.append("...")

            return "".join(parts)

        return None

    def _resolve_variable(self, var_name: str, context_node: nodes.Call) -> str | None:  # noqa: C901
        """Try to resolve a variable to its string value.

        Args:
            var_name: Variable name to resolve
            context_node: Call node for context

        Returns:
            Resolved string value or None
        """
        scope = context_node.scope()
        if not scope:
            return None

        # Look for assignments in the scope
        for node in scope.body:
            if isinstance(node, nodes.Assign):
                for target in node.targets:
                    if isinstance(target, nodes.AssignName) and target.name == var_name:
                        # Found the assignment, try to infer the value
                        value = safe_infer_value(node.value)
                        # Only return if it's a valid string (not Uninferable)
                        if isinstance(value, str) and value and "Uninferable" not in value:
                            return value

        # Look in module-level assignments
        module = context_node.root()
        for node in module.body:
            if isinstance(node, nodes.Assign):
                for target in node.targets:
                    if isinstance(target, nodes.AssignName) and target.name == var_name:
                        value = safe_infer_value(node.value)
                        # Only return if it's a valid string (not Uninferable)
                        if isinstance(value, str) and value and "Uninferable" not in value:
                            return value

        return None

    def _contains_query_indicator(self, node: nodes.NodeNG) -> bool:
        """Check if node contains query parameter indicators.

        Args:
            node: AST node to check

        Returns:
            True if node likely constructs a URL with query params
        """
        node_str = safe_as_string(node)
        query_indicators = ["?", "urlencode", "params=", "query="]
        return any(indicator in node_str for indicator in query_indicators)

    def _extract_params(self, node: nodes.Call) -> dict[str, Any] | None:
        """Extract query parameters from params keyword argument."""
        for keyword in node.keywords or []:
            if keyword.arg == "params":
                params_value = safe_infer_value(keyword.value)
                if isinstance(params_value, dict):
                    return params_value
                # If we can't infer the exact value, omit field
                return None
        return None

    def _extract_headers(self, node: nodes.Call) -> dict[str, Any] | None:
        """Extract headers from headers keyword argument."""
        for keyword in node.keywords or []:
            if keyword.arg == "headers":
                headers_value = safe_infer_value(keyword.value)
                if isinstance(headers_value, dict):
                    return headers_value
                # If we can't infer the exact value, omit field
                return None
        return None

    def _extract_json_body(self, node: nodes.Call) -> dict[str, Any] | None:
        """Extract JSON body from json keyword argument."""
        for keyword in node.keywords or []:
            if keyword.arg == "json":
                json_value = safe_infer_value(keyword.value)
                if isinstance(json_value, dict):
                    return json_value
                # If we can't infer the exact value, omit field
                return None
        return None

    def _extract_data(self, node: nodes.Call) -> Any | None:
        """Extract form data from data keyword argument."""
        for keyword in node.keywords or []:
            if keyword.arg == "data":
                data_value = safe_infer_value(keyword.value)
                # Data can be dict, string, bytes, or other types
                if data_value is not None:
                    return data_value
                # If we can't infer the exact value, omit field
                return None
        return None

    def _extract_timeout(self, node: nodes.Call) -> float | int | None:
        """Extract timeout parameter."""
        for keyword in node.keywords or []:
            if keyword.arg == "timeout":
                timeout_value = safe_infer_value(keyword.value)
                if isinstance(timeout_value, (int, float)):
                    return timeout_value
        return None

    def _aggregate_requests(self, requests_by_url: dict[str, list[HttpRequestUsage]]) -> dict[str, HttpRequestInfo]:
        """Aggregate requests by URL."""
        result: dict[str, HttpRequestInfo] = {}

        for url, usages in requests_by_url.items():
            if not usages:
                continue

            # Determine primary method and library
            methods = [u.method for u in usages]
            primary_method = max(set(methods), key=methods.count)

            # Determine library from first usage
            library = "requests"  # default
            if usages[0].is_async:
                library = "aiohttp"

            result[url] = HttpRequestInfo(
                method=primary_method,
                library=library,
                usages=usages,
            )

        return result

    def _calculate_summary(self, requests: dict[str, HttpRequestInfo], scan_duration_ms: int) -> HttpRequestSummary:
        """Calculate summary statistics."""
        all_usages = [usage for info in requests.values() for usage in info.usages]
        by_library: dict[str, int] = {}

        for info in requests.values():
            by_library[info.library] = by_library.get(info.library, 0) + len(info.usages)

        return HttpRequestSummary(
            total_count=len(all_usages),
            files_scanned=len({u.file for u in all_usages}),
            scan_duration_ms=scan_duration_ms,
            total_requests=len(all_usages),
            unique_urls=len(requests),
            by_library=by_library,
        )
