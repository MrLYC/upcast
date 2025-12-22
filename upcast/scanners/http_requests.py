"""HTTP requests scanner implementation with Pydantic models."""

from pathlib import Path
from typing import ClassVar

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
                    url = self._extract_url(node) or "unknown_url"
                    if url not in requests_by_url:
                        requests_by_url[url] = []
                    requests_by_url[url].append(usage)

        # Aggregate by URL
        requests_info = self._aggregate_requests(requests_by_url)
        summary = self._calculate_summary(requests_info)

        return HttpRequestOutput(summary=summary, results=requests_info)

    def _check_request_call(self, node: nodes.Call, file_path: str, imports: dict[str, str]) -> HttpRequestUsage | None:
        """Check if call is an HTTP request."""
        func = node.func
        library, method = self._identify_request(func, imports)

        if not library:
            return None

        return HttpRequestUsage(
            location=f"{file_path}:{node.lineno}",
            statement=safe_as_string(node),
            method=method.upper(),
            timeout=self._extract_timeout(node),
            session_based="Session" in safe_as_string(func),
            is_async=library == "aiohttp" or "async" in safe_as_string(func),
        )

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

    def _extract_url(self, node: nodes.Call) -> str | None:
        """Extract URL from request call with pattern normalization.

        Tries to detect dynamic URL construction patterns first, then falls back
        to literal inference. This ensures we normalize URLs even when astroid
        can partially infer them.

        Returns:
            Literal URL string, normalized pattern, or None
        """
        # Try extracting from positional args
        if node.args:
            url_node = node.args[0]

            # Check if it's a dynamic construction (prioritize pattern detection)
            if self._is_dynamic_url(url_node):
                pattern = self._normalize_url_pattern(url_node)
                if pattern:
                    return pattern

            # Fall back to literal inference for static URLs
            url_value = safe_infer_value(url_node)
            if isinstance(url_value, str):
                return url_value

        # Try extracting from keyword args
        for keyword in node.keywords or []:
            if keyword.arg == "url":
                url_node = keyword.value

                # Check if it's a dynamic construction
                if self._is_dynamic_url(url_node):
                    pattern = self._normalize_url_pattern(url_node)
                    if pattern:
                        return pattern

                # Fall back to literal inference
                url_value = safe_infer_value(url_node)
                if isinstance(url_value, str):
                    return url_value

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

        Recognizes common URL construction patterns and normalizes them:
        - String concatenation: base + path → "..."
        - F-strings: f"{base}/api" → "..." or ".../..."
        - Format strings: "{}/api".format(base) → "..."
        - Query params: url + "?" + params → "...?..."

        Args:
            node: AST node representing the URL expression

        Returns:
            Normalized pattern string or None if unrecognizable
        """
        # Handle string concatenation (BinOp with '+')
        if isinstance(node, nodes.BinOp) and node.op == "+":
            if self._contains_query_indicator(node):
                return "...?..."
            return "..."

        # Handle f-strings (JoinedStr)
        if isinstance(node, nodes.JoinedStr):
            node_str = safe_as_string(node)
            if "?" in node_str or "params" in node_str.lower():
                return "...?..."
            if "/" in node_str:
                return ".../..."
            return "..."

        # Handle .format() calls
        if isinstance(node, nodes.Call) and isinstance(node.func, nodes.Attribute) and node.func.attrname == "format":
            return "..."

        # Handle % formatting
        if isinstance(node, nodes.BinOp) and node.op == "%":
            return "..."

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

    def _calculate_summary(self, requests: dict[str, HttpRequestInfo]) -> HttpRequestSummary:
        """Calculate summary statistics."""
        all_usages = [usage for info in requests.values() for usage in info.usages]
        by_library: dict[str, int] = {}

        for info in requests.values():
            by_library[info.library] = by_library.get(info.library, 0) + len(info.usages)

        return HttpRequestSummary(
            total_count=len(all_usages),
            files_scanned=len({u.location.split(":")[0] for u in all_usages}),
            total_requests=len(all_usages),
            unique_urls=len(requests),
            by_library=by_library,
        )
