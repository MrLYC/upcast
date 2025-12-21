"""Blocking operations scanner implementation with Pydantic models."""

from pathlib import Path
from typing import ClassVar

from astroid import nodes

from upcast.common.ast_utils import get_import_info, safe_as_string
from upcast.common.file_utils import get_relative_path_str
from upcast.common.scanner_base import BaseScanner
from upcast.models.blocking_operations import (
    BlockingOperation,
    BlockingOperationsOutput,
    BlockingOperationsSummary,
)


class BlockingOperationsScanner(BaseScanner[BlockingOperationsOutput]):
    """Scanner for blocking operations (sleep, locks, subprocess, DB queries)."""

    # Blocking patterns to detect
    BLOCKING_PATTERNS: ClassVar[dict[str, list[tuple[str, ...]]]] = {
        "time_based": [("time", "sleep"), ("asyncio", "sleep")],
        "database": [("select_for_update",)],
        "synchronization": [
            ("threading", "Lock"),
            ("threading", "RLock"),
            ("threading", "Semaphore"),
            ("multiprocessing", "Lock"),
        ],
        "subprocess": [
            ("subprocess", "run"),
            ("subprocess", "call"),
            ("subprocess", "check_call"),
            ("subprocess", "check_output"),
            ("os", "system"),
        ],
    }

    def scan(self, path: Path) -> BlockingOperationsOutput:
        """Scan for blocking operations."""
        files = self.get_files_to_scan(path)
        base_path = path if path.is_dir() else path.parent

        operations_by_category: dict[str, list[BlockingOperation]] = {
            "time_based": [],
            "database": [],
            "synchronization": [],
            "subprocess": [],
        }

        for file_path in files:
            module = self.parse_file(file_path)
            if not module:
                continue

            imports = get_import_info(module)
            rel_path = get_relative_path_str(file_path, base_path)

            for node in module.nodes_of_class((nodes.Call, nodes.With)):
                operation = self._check_node(node, rel_path, imports)
                if operation:
                    operations_by_category[operation.category].append(operation)

        summary = self._calculate_summary(operations_by_category)
        return BlockingOperationsOutput(summary=summary, operations=operations_by_category)

    def _check_node(self, node: nodes.NodeNG, file_path: str, imports: dict[str, str]) -> BlockingOperation | None:
        """Check a node for blocking operations."""
        if isinstance(node, nodes.Call):
            return self._check_call(node, file_path, imports)
        elif isinstance(node, nodes.With):
            return self._check_with(node, file_path, imports)
        return None

    def _check_call(self, node: nodes.Call, file_path: str, imports: dict[str, str]) -> BlockingOperation | None:
        """Check function call for blocking patterns."""
        func = node.func
        func_name = self._get_qualified_name(func, imports)

        if not func_name:
            return None

        # Check against patterns
        for category, patterns in self.BLOCKING_PATTERNS.items():
            for pattern in patterns:
                if self._matches_pattern(func_name, pattern):
                    return BlockingOperation(
                        file=file_path,
                        line=node.lineno or 0,
                        column=node.col_offset or 0,
                        category=category,
                        operation=func_name,
                        statement=safe_as_string(node),
                        function=self._get_function_name(node),
                        class_name=self._get_class_name(node),
                    )

        return None

    def _check_with(self, node: nodes.With, file_path: str, imports: dict[str, str]) -> BlockingOperation | None:
        """Check with statement for lock context managers."""
        for item in node.items:
            context_expr = item[0]
            if isinstance(context_expr, nodes.Call):
                func_name = self._get_qualified_name(context_expr.func, imports)
                if func_name and any(
                    self._matches_pattern(func_name, p) for p in self.BLOCKING_PATTERNS["synchronization"]
                ):
                    return BlockingOperation(
                        file=file_path,
                        line=node.lineno or 0,
                        column=node.col_offset or 0,
                        category="synchronization",
                        operation=f"{func_name} (context)",
                        statement=safe_as_string(node),
                        function=self._get_function_name(node),
                        class_name=self._get_class_name(node),
                    )
        return None

    def _get_qualified_name(self, node: nodes.NodeNG, imports: dict[str, str]) -> str | None:
        """Get qualified name of a function/attribute."""
        if isinstance(node, nodes.Name):
            name = node.name
            return imports.get(name, name)
        elif isinstance(node, nodes.Attribute):
            if isinstance(node.expr, nodes.Name):
                module = imports.get(node.expr.name, node.expr.name)
                return f"{module}.{node.attrname}"
            return node.attrname
        return None

    def _matches_pattern(self, func_name: str, pattern: tuple[str, ...]) -> bool:
        """Check if function name matches pattern."""
        parts = func_name.split(".")
        if len(pattern) == 1:
            return pattern[0] in parts
        elif len(pattern) == 2:
            return len(parts) >= 2 and parts[-2] == pattern[0] and parts[-1] == pattern[1]
        return False

    def _get_function_name(self, node: nodes.NodeNG) -> str | None:
        """Get containing function name."""
        parent = node.parent
        while parent:
            if isinstance(parent, (nodes.FunctionDef, nodes.AsyncFunctionDef)):
                return parent.name
            parent = parent.parent
        return None

    def _get_class_name(self, node: nodes.NodeNG) -> str | None:
        """Get containing class name."""
        parent = node.parent
        while parent:
            if isinstance(parent, nodes.ClassDef):
                return parent.name
            parent = parent.parent
        return None

    def _calculate_summary(self, operations: dict[str, list[BlockingOperation]]) -> BlockingOperationsSummary:
        """Calculate summary statistics."""
        by_category = {cat: len(ops) for cat, ops in operations.items() if ops}
        total = sum(by_category.values())
        files = len({op.file for ops in operations.values() for op in ops})

        return BlockingOperationsSummary(
            total_count=total,
            files_scanned=files,
            by_category=by_category,
            scan_duration_ms=0,  # TODO: Add timing
        )
