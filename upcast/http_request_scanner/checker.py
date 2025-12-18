"""HTTP request checker and aggregator."""

import logging
from pathlib import Path

from astroid import nodes, parse

from upcast.http_request_scanner.request_parser import (
    HttpRequest,
    detect_request_call,
    parse_request,
)

logger = logging.getLogger(__name__)


class HttpRequestChecker:
    """Checker to detect and aggregate HTTP requests across files."""

    def __init__(self, base_path: Path):
        """Initialize the checker.

        Args:
            base_path: Base path for relative path calculation
        """
        self.base_path = base_path
        self.requests: dict[str, list[HttpRequest]] = {}  # URL -> list of requests

    def check_file(self, file_path: Path) -> None:
        """Process a single file to extract HTTP requests.

        Args:
            file_path: Path to Python file to check
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = parse(content)
            relative_path = str(file_path.relative_to(self.base_path))

            # Visit all call nodes in the file
            for node in tree.nodes_of_class(nodes.Call):
                self.visit_call(node, relative_path)

        except Exception as e:
            # Skip files that cannot be parsed
            logger.debug(f"Failed to parse {file_path}: {e}")

    def visit_call(self, node: nodes.Call, file_path: str) -> None:
        """Check if a call node is an HTTP request.

        Args:
            node: astroid Call node
            file_path: Relative file path
        """
        library = detect_request_call(node)
        if library:
            # Parse the full request
            request = parse_request(node, file_path, library)

            # Skip requests with None URL (completely unresolvable, e.g., function parameters)
            if request.url is None:
                return

            # Add to requests dict grouped by URL
            if request.url not in self.requests:
                self.requests[request.url] = []
            self.requests[request.url].append(request)

    def get_requests_by_url(self) -> dict[str, list[HttpRequest]]:
        """Get all requests grouped by URL.

        Returns:
            Dictionary mapping URLs to list of requests
        """
        return self.requests

    def get_summary(self) -> dict:
        """Calculate summary statistics.

        Returns:
            Dictionary with summary statistics
        """
        all_requests = [req for reqs in self.requests.values() for req in reqs]
        libraries = list({req.library for req in all_requests})
        session_count = sum(1 for req in all_requests if req.session_based)
        no_timeout_count = sum(1 for req in all_requests if req.timeout is None)
        async_count = sum(1 for req in all_requests if req.is_async)

        return {
            "total_requests": len(all_requests),
            "unique_urls": len(self.requests),
            "libraries_used": sorted(libraries),
            "session_based_count": session_count,
            "requests_without_timeout": no_timeout_count,
            "async_requests": async_count,
        }
