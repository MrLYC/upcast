"""Exception handler scanner implementation with Pydantic models."""

import time
from pathlib import Path
from typing import ClassVar

from astroid import nodes

from upcast.common.ast_utils import safe_as_string
from upcast.common.file_utils import get_relative_path_str
from upcast.common.inference import infer_value
from upcast.common.scanner_base import BaseScanner
from upcast.models.exceptions import (
    ExceptionBlock,
    ExceptionHandler,
    ExceptionHandlerOutput,
    ExceptionHandlerSummary,
)


class ExceptionHandlerScanner(BaseScanner[ExceptionHandlerOutput]):
    """Scanner for exception handlers (try/except/else/finally)."""

    _CONTROL_FLOW_NODES = (nodes.Pass, nodes.Return, nodes.Break, nodes.Continue, nodes.Raise)
    _NESTED_SCOPE_NODES = (nodes.FunctionDef, nodes.AsyncFunctionDef, nodes.ClassDef, nodes.Lambda)
    _DYNAMIC_LOG_LEVELS: ClassVar[dict[int, str]] = {
        10: "debug",
        20: "info",
        30: "warning",
        40: "error",
        50: "critical",
    }

    def __init__(
        self,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        verbose: bool = False,
    ):
        """Initialize scanner."""
        super().__init__(include_patterns, exclude_patterns, verbose)
        self.base_path: Path | None = None
        self.handlers: list[ExceptionHandler] = []

    def scan(self, path: Path) -> ExceptionHandlerOutput:
        """Scan for exception handlers."""
        start_time = time.time()
        self.base_path = path.resolve() if path.is_dir() else path.parent.resolve()
        self.handlers = []

        files = self.get_files_to_scan(path)
        for file_path in files:
            self._scan_file(file_path)

        summary = self._calculate_summary(
            scan_duration_ms=int((time.time() - start_time) * 1000),
        )

        return ExceptionHandlerOutput(
            summary=summary,
            results=self.handlers,
            metadata={"scanner_name": "exception-handlers"},
        )

    def _scan_file(self, file_path: Path) -> None:
        """Scan a single file for exception handlers."""
        module = self.parse_file(file_path)
        if not module:
            return

        relative_path = get_relative_path_str(file_path, self.base_path or Path.cwd())

        # Visit all try blocks
        for node in module.nodes_of_class(nodes.Try):
            handler = self._parse_try_block(node, relative_path)
            if handler:
                self.handlers.append(handler)

    def _parse_try_block(self, node: nodes.Try, file_path: str) -> ExceptionHandler | None:
        """Parse a try block into an ExceptionHandler."""
        try:
            try_lines = (node.body[-1].lineno or 0) - (node.lineno or 0) + 1 if node.body else 1

            exception_blocks = [self._parse_except_clause(handler) for handler in node.handlers]

            else_lineno = None
            else_lines = None
            if node.orelse:
                else_lineno = node.orelse[0].lineno
                else_lines = (node.orelse[-1].lineno or 0) - (else_lineno or 0) + 1

            finally_lineno = None
            finally_lines = None
            if node.finalbody:
                finally_lineno = node.finalbody[0].lineno
                finally_lines = (node.finalbody[-1].lineno or 0) - (finally_lineno or 0) + 1

            nested_exceptions = self._check_nested_exceptions(node.body)

            return ExceptionHandler(
                file=file_path,
                try_lineno=node.lineno,
                try_lines=try_lines,
                else_lineno=else_lineno,
                else_lines=else_lines,
                finally_lineno=finally_lineno,
                finally_lines=finally_lines,
                nested_exceptions=nested_exceptions,
                exception_blocks=exception_blocks,
            )
        except Exception:
            return None

    def _parse_except_clause(self, handler: nodes.ExceptHandler) -> ExceptionBlock:
        """Parse an except clause."""
        exceptions = self._extract_exception_types(handler)
        lines = (handler.body[-1].lineno or 0) - (handler.lineno or 0) + 1 if handler.body else 1
        log_counts = self._count_logging_calls(handler.body)
        flow_counts = self._count_control_flow(handler.body)

        return ExceptionBlock(
            lineno=handler.lineno,
            lines=lines,
            exceptions=exceptions,
            **log_counts,
            **flow_counts,
        )

    def _extract_exception_types(self, handler: nodes.ExceptHandler) -> list[str]:
        """Extract exception type names from an except handler."""
        if handler.type is None:
            return []  # Bare except

        exception_types = []
        if isinstance(handler.type, nodes.Tuple):
            # Multiple exceptions: except (ValueError, KeyError):
            for elt in handler.type.elts:
                if isinstance(elt, (nodes.Name, nodes.Attribute)):
                    exception_types.append(safe_as_string(elt))
        elif isinstance(handler.type, (nodes.Name, nodes.Attribute)):
            # Single exception
            exception_types.append(safe_as_string(handler.type))

        return exception_types

    def _count_logging_calls(self, body: list[nodes.NodeNG]) -> dict[str, int]:
        """Count logging calls by level."""
        counts = {
            "log_debug_count": 0,
            "log_info_count": 0,
            "log_warning_count": 0,
            "log_error_count": 0,
            "log_exception_count": 0,
            "log_critical_count": 0,
        }

        for node in body:
            for subnode in node.nodes_of_class(nodes.Call):
                if isinstance(subnode.func, nodes.Attribute):
                    method_name = self._resolve_log_method_name(subnode)
                    if not method_name:
                        continue

                    if isinstance(subnode.func.expr, nodes.Name):
                        var_name = subnode.func.expr.name
                        if (
                            var_name == "logging"
                            or var_name.lower() in {"logger", "log", "_logger"}
                            or var_name in {"LOG", "LOGGER"}
                        ):
                            counts[f"log_{method_name}_count"] += 1
                    elif isinstance(subnode.func.expr, nodes.Attribute):
                        if subnode.func.expr.attrname in {"logger", "log"}:
                            counts[f"log_{method_name}_count"] += 1

        return counts

    def _resolve_log_method_name(self, call: nodes.Call) -> str | None:
        """Resolve a canonical log method name for counting."""
        if not isinstance(call.func, nodes.Attribute):
            return None

        method_name = call.func.attrname
        if method_name in {"debug", "info", "warning", "error", "exception", "critical"}:
            return method_name

        if method_name != "log" or len(call.args) < 2:
            return None

        level_node = call.args[0]
        inferred_level = infer_value(level_node).get_if_type(int)

        if isinstance(inferred_level, int):
            return self._DYNAMIC_LOG_LEVELS.get(inferred_level)

        level_name = safe_as_string(level_node)
        if not level_name:
            return None

        normalized = level_name.split(".")[-1].lower()
        if normalized == "warn":
            normalized = "warning"
        if normalized == "fatal":
            normalized = "critical"
        if normalized in {"debug", "info", "warning", "error", "exception", "critical"}:
            return normalized
        return None

    def _count_control_flow(self, body: list[nodes.NodeNG]) -> dict[str, int]:
        """Count control flow statements."""
        counts = {
            "pass_count": 0,
            "return_count": 0,
            "break_count": 0,
            "continue_count": 0,
            "raise_count": 0,
        }

        for node in body:
            for subnode in self._iter_control_flow_nodes(node):
                if isinstance(subnode, nodes.Pass):
                    counts["pass_count"] += 1
                elif isinstance(subnode, nodes.Return):
                    counts["return_count"] += 1
                elif isinstance(subnode, nodes.Break):
                    counts["break_count"] += 1
                elif isinstance(subnode, nodes.Continue):
                    counts["continue_count"] += 1
                elif isinstance(subnode, nodes.Raise):
                    counts["raise_count"] += 1

        return counts

    def _iter_control_flow_nodes(self, node: nodes.NodeNG):
        """Yield control-flow nodes without descending into nested scopes."""
        if isinstance(node, self._NESTED_SCOPE_NODES):
            return

        stack = [node]

        while stack:
            current = stack.pop()
            if isinstance(current, self._CONTROL_FLOW_NODES):
                yield current
                continue

            if current is not node and isinstance(current, self._NESTED_SCOPE_NODES):
                continue

            children = list(current.get_children())
            stack.extend(reversed(children))

    def _check_nested_exceptions(self, body: list[nodes.NodeNG]) -> bool:
        """Check if the try block contains nested try-except blocks."""
        for node in body:
            if isinstance(node, nodes.Try):
                return True
            for subnode in node.nodes_of_class(nodes.Try):
                if subnode is not node:
                    return True
        return False

    def _calculate_summary(self, scan_duration_ms: int) -> ExceptionHandlerSummary:
        """Calculate summary statistics."""
        total_handlers = len(self.handlers)
        total_except_clauses = sum(len(h.exception_blocks) for h in self.handlers)
        files_scanned = len({h.file for h in self.handlers})

        return ExceptionHandlerSummary(
            total_count=total_except_clauses,
            files_scanned=files_scanned,
            scan_duration_ms=scan_duration_ms,
            total_handlers=total_handlers,
            total_except_clauses=total_except_clauses,
        )
