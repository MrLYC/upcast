"""Exception handler scanner implementation with Pydantic models."""

import time
from pathlib import Path

from astroid import nodes

from upcast.common.ast_utils import safe_as_string
from upcast.common.file_utils import get_relative_path_str
from upcast.common.scanner_base import BaseScanner
from upcast.models.exceptions import (
    ElseClause,
    ExceptClause,
    ExceptionHandler,
    ExceptionHandlerOutput,
    ExceptionHandlerSummary,
    FinallyClause,
)


class ExceptionHandlerScanner(BaseScanner[ExceptionHandlerOutput]):
    """Scanner for exception handlers (try/except/else/finally)."""

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
            # Calculate try block line count
            try_lines = (node.body[-1].lineno or 0) - (node.lineno or 0) + 1 if node.body else 1

            # Parse all except clauses
            except_clauses = [self._parse_except_clause(handler) for handler in node.handlers]

            # Determine end line
            if node.finalbody:
                end_line = node.finalbody[-1].lineno
            elif node.orelse:
                end_line = node.orelse[-1].lineno
            elif node.handlers:
                last_handler = node.handlers[-1]
                end_line = last_handler.body[-1].lineno if last_handler.body else last_handler.lineno
            else:
                end_line = node.body[-1].lineno if node.body else node.lineno

            # Parse else and finally clauses
            else_clause = self._parse_else_clause(node)
            finally_clause = self._parse_finally_clause(node)

            return ExceptionHandler(
                file=file_path,
                lineno=node.lineno or 0,
                end_lineno=end_line or 0,
                try_lines=try_lines,
                except_clauses=except_clauses,
                else_clause=else_clause,
                finally_clause=finally_clause,
            )
        except Exception:
            return None

    def _parse_except_clause(self, handler: nodes.ExceptHandler) -> ExceptClause:
        """Parse an except clause."""
        exception_types = self._extract_exception_types(handler)
        lines = (handler.body[-1].lineno or 0) - (handler.lineno or 0) + 1 if handler.body else 1
        log_counts = self._count_logging_calls(handler.body)
        flow_counts = self._count_control_flow(handler.body)

        return ExceptClause(
            line=handler.lineno or 0,
            exception_types=exception_types,
            lines=lines,
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

        log_methods = {"debug", "info", "warning", "error", "exception", "critical"}

        for node in body:
            for subnode in node.nodes_of_class(nodes.Call):
                if isinstance(subnode.func, nodes.Attribute):
                    method_name = subnode.func.attrname
                    if method_name in log_methods:
                        if isinstance(subnode.func.expr, nodes.Name):
                            var_name = subnode.func.expr.name
                            if var_name.lower() in {"logger", "log", "_logger"} or var_name in {"LOG", "LOGGER"}:
                                counts[f"log_{method_name}_count"] += 1
                        elif isinstance(subnode.func.expr, nodes.Attribute):
                            if subnode.func.expr.attrname in {"logger", "log"}:
                                counts[f"log_{method_name}_count"] += 1

        return counts

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
            for subnode in node.nodes_of_class((nodes.Pass, nodes.Return, nodes.Break, nodes.Continue, nodes.Raise)):
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

    def _parse_else_clause(self, node: nodes.Try) -> ElseClause | None:
        """Parse else clause if present."""
        if not node.orelse:
            return None

        line = node.orelse[0].lineno or 0
        lines = (node.orelse[-1].lineno or 0) - line + 1

        return ElseClause(line=line, lines=lines)

    def _parse_finally_clause(self, node: nodes.Try) -> FinallyClause | None:
        """Parse finally clause if present."""
        if not node.finalbody:
            return None

        line = node.finalbody[0].lineno or 0
        lines = (node.finalbody[-1].lineno or 0) - line + 1

        return FinallyClause(line=line, lines=lines)

    def _calculate_summary(self, scan_duration_ms: int) -> ExceptionHandlerSummary:
        """Calculate summary statistics."""
        total_handlers = len(self.handlers)
        total_except_clauses = sum(len(h.except_clauses) for h in self.handlers)
        files_scanned = len({h.file for h in self.handlers})

        return ExceptionHandlerSummary(
            total_count=total_except_clauses,
            files_scanned=files_scanned,
            scan_duration_ms=scan_duration_ms,
            total_handlers=total_handlers,
            total_except_clauses=total_except_clauses,
        )
