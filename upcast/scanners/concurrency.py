"""Concurrency patterns scanner implementation with Pydantic models."""

from pathlib import Path
from typing import ClassVar

from astroid import nodes

from upcast.common.ast_utils import get_import_info, safe_as_string
from upcast.common.file_utils import get_relative_path_str
from upcast.common.scanner_base import BaseScanner
from upcast.models.concurrency import ConcurrencyPatternOutput, ConcurrencyPatternSummary, ConcurrencyUsage


class ConcurrencyScanner(BaseScanner[ConcurrencyPatternOutput]):
    """Scanner for concurrency patterns (threading, multiprocessing, asyncio, celery)."""

    CONCURRENCY_PATTERNS: ClassVar[dict[str, list[str]]] = {
        "threading": [
            "Thread",
            "ThreadPoolExecutor",
            "Lock",
            "RLock",
            "Semaphore",
            "Event",
            "Queue",
        ],
        "multiprocessing": [
            "Process",
            "Pool",
            "ProcessPoolExecutor",
            "Queue",
            "Manager",
        ],
        "asyncio": [
            "create_task",
            "gather",
            "wait",
            "run",
            "ensure_future",
            "sleep",
            "Lock",
            "Semaphore",
            "Queue",
        ],
        "celery": ["task", "Task", "group", "chain", "chord"],
    }

    def scan(self, path: Path) -> ConcurrencyPatternOutput:
        """Scan for concurrency patterns."""
        files = self.get_files_to_scan(path)
        base_path = path if path.is_dir() else path.parent

        patterns: dict[str, dict[str, list[ConcurrencyUsage]]] = {
            "threading": {},
            "multiprocessing": {},
            "asyncio": {},
            "celery": {},
        }

        for file_path in files:
            module = self.parse_file(file_path)
            if not module:
                continue

            imports = get_import_info(module)
            rel_path = get_relative_path_str(file_path, base_path)

            # Check async functions
            for node in module.nodes_of_class((nodes.AsyncFunctionDef, nodes.FunctionDef)):
                if isinstance(node, nodes.AsyncFunctionDef):
                    usage = ConcurrencyUsage(
                        file=rel_path,
                        line=node.lineno,
                        column=node.col_offset,
                        pattern="async function",
                        statement=f"async def {node.name}",
                    )
                    self._add_pattern(patterns, "asyncio", "async_function", usage)

            # Check calls and await
            for node in module.nodes_of_class((nodes.Call, nodes.Await)):
                usage = self._check_node(node, rel_path, imports)
                if usage:
                    category = self._categorize_pattern(usage.pattern)
                    self._add_pattern(patterns, category, usage.pattern, usage)

        summary = self._calculate_summary(patterns)
        return ConcurrencyPatternOutput(summary=summary, concurrency_patterns=patterns)

    def _check_node(self, node: nodes.NodeNG, file_path: str, imports: dict[str, str]) -> ConcurrencyUsage | None:
        """Check node for concurrency patterns."""
        if isinstance(node, nodes.Await):
            return ConcurrencyUsage(
                file=file_path,
                line=node.lineno,
                column=node.col_offset,
                pattern="await",
                statement=safe_as_string(node),
            )
        elif isinstance(node, nodes.Call):
            return self._check_call(node, file_path, imports)
        return None

    def _check_call(self, node: nodes.Call, file_path: str, imports: dict[str, str]) -> ConcurrencyUsage | None:
        """Check function call for concurrency patterns."""
        func_name = self._get_qualified_name(node.func, imports)
        if not func_name:
            return None

        # Check against patterns
        for _category, patterns in self.CONCURRENCY_PATTERNS.items():
            for pattern in patterns:
                if pattern.lower() in func_name.lower():
                    return ConcurrencyUsage(
                        file=file_path,
                        line=node.lineno,
                        column=node.col_offset,
                        pattern=func_name,
                        statement=safe_as_string(node),
                    )

        return None

    def _get_qualified_name(self, node: nodes.NodeNG, imports: dict[str, str]) -> str | None:
        """Get qualified name of a function/attribute."""
        if isinstance(node, nodes.Name):
            return imports.get(node.name, node.name)
        elif isinstance(node, nodes.Attribute):
            if isinstance(node.expr, nodes.Name):
                module = imports.get(node.expr.name, node.expr.name)
                return f"{module}.{node.attrname}"
            return node.attrname
        return None

    def _categorize_pattern(self, pattern: str) -> str:
        """Categorize pattern into threading/multiprocessing/asyncio/celery."""
        pattern_lower = pattern.lower()
        for category, patterns in self.CONCURRENCY_PATTERNS.items():
            if any(p.lower() in pattern_lower for p in patterns):
                return category
        return "threading"  # default

    def _add_pattern(
        self,
        patterns: dict[str, dict[str, list[ConcurrencyUsage]]],
        category: str,
        pattern_type: str,
        usage: ConcurrencyUsage,
    ) -> None:
        """Add pattern to collection."""
        if pattern_type not in patterns[category]:
            patterns[category][pattern_type] = []
        patterns[category][pattern_type].append(usage)

    def _calculate_summary(self, patterns: dict[str, dict[str, list[ConcurrencyUsage]]]) -> ConcurrencyPatternSummary:
        """Calculate summary statistics."""
        by_category: dict[str, int] = {}
        total = 0

        for category, patterns_by_type in patterns.items():
            count = sum(len(usages) for usages in patterns_by_type.values())
            if count > 0:
                by_category[category] = count
                total += count

        files = len({
            usage.file
            for patterns_by_type in patterns.values()
            for usages in patterns_by_type.values()
            for usage in usages
        })

        return ConcurrencyPatternSummary(
            total_count=total,
            files_scanned=files,
            by_category=by_category,
        )
