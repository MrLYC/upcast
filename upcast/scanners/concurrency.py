"""Concurrency patterns scanner implementation with Pydantic models."""

import time
from pathlib import Path
from typing import Any, ClassVar

from astroid import nodes

from upcast.common.ast_utils import get_import_info, safe_as_string, safe_infer_value
from upcast.common.file_utils import get_relative_path_str
from upcast.common.scanner_base import BaseScanner
from upcast.models.concurrency import ConcurrencyPatternOutput, ConcurrencyPatternSummary, ConcurrencyUsage


class ConcurrencyScanner(BaseScanner[ConcurrencyPatternOutput]):
    """Scanner for concurrency patterns (threading, multiprocessing, asyncio, celery)."""

    # Executor types for resolution
    EXECUTOR_TYPES: ClassVar[set[str]] = {
        "ThreadPoolExecutor",
        "ProcessPoolExecutor",
    }

    def scan(self, path: Path) -> ConcurrencyPatternOutput:
        """Scan for concurrency patterns."""
        start_time = time.time()
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

            # Pass 1: Build executor mapping
            executor_mapping = self._build_executor_mapping(module, imports)

            # Pass 2: Detect patterns
            # Check async functions
            for node in module.nodes_of_class(nodes.AsyncFunctionDef):
                function, class_name = self._extract_context(node)
                usage = ConcurrencyUsage(
                    file=rel_path,
                    line=node.lineno,
                    column=node.col_offset,
                    pattern="async_function",
                    statement=f"async def {node.name}",
                    function=function,
                    class_name=class_name,
                )
                self._add_pattern(patterns, "asyncio", "async_function", usage)

            # Check await expressions
            for node in module.nodes_of_class(nodes.Await):
                usage = self._detect_await(node, rel_path)
                if usage:
                    self._add_pattern(patterns, "asyncio", "await", usage)

            # Check all Call nodes for specific patterns
            for node in module.nodes_of_class(nodes.Call):
                # Try each detector
                usage = (
                    self._detect_thread_creation(node, rel_path, imports)
                    or self._detect_threadpool_executor(node, rel_path, imports)
                    or self._detect_process_creation(node, rel_path, imports)
                    or self._detect_processpool_executor(node, rel_path, imports)
                    or self._detect_executor_submit(node, rel_path, imports, executor_mapping)
                    or self._detect_create_task(node, rel_path, imports)
                    or self._detect_run_in_executor(node, rel_path, imports, executor_mapping)
                )
                if usage:
                    # Determine category from pattern
                    category = self._get_category_from_pattern(usage.pattern)
                    pattern_type = usage.api_call or usage.pattern
                    self._add_pattern(patterns, category, pattern_type, usage)

        scan_duration_ms = int((time.time() - start_time) * 1000)
        summary = self._calculate_summary(patterns, scan_duration_ms)
        return ConcurrencyPatternOutput(summary=summary, results=patterns)

    def _build_executor_mapping(self, module: nodes.Module, imports: dict[str, str]) -> dict[str, str]:
        """Build mapping of variable names to executor types.

        Returns:
            Dict mapping variable name to executor type (ThreadPoolExecutor or ProcessPoolExecutor)
        """
        mapping: dict[str, str] = {}

        for node in module.nodes_of_class(nodes.Assign):
            # Check if this is an executor assignment
            if not isinstance(node.value, nodes.Call):
                continue

            func_name = self._get_qualified_name(node.value.func, imports)
            if not func_name:
                continue

            # Check if it's an executor type
            executor_type = None
            if "ThreadPoolExecutor" in func_name:
                executor_type = "ThreadPoolExecutor"
            elif "ProcessPoolExecutor" in func_name:
                executor_type = "ProcessPoolExecutor"

            if executor_type:
                # Extract variable name from assignment target
                for target in node.targets:
                    if isinstance(target, nodes.AssignName):
                        mapping[target.name] = executor_type

        return mapping

    def _extract_context(self, node: nodes.NodeNG) -> tuple[str | None, str | None]:
        """Extract function and class context for a node.

        Returns:
            Tuple of (function_name, class_name)
        """
        function_name = None
        class_name = None

        # Get enclosing scope
        scope = node.scope()

        # Check if inside a function
        if isinstance(scope, (nodes.FunctionDef, nodes.AsyncFunctionDef)):
            function_name = scope.name

            # Check if function is inside a class
            parent = scope.parent
            while parent:
                if isinstance(parent, nodes.ClassDef):
                    class_name = parent.name
                    break
                parent = parent.parent if hasattr(parent, "parent") else None

        return function_name, class_name

    def _detect_await(self, node: nodes.Await, file_path: str) -> ConcurrencyUsage | None:
        """Detect await expressions."""
        function, class_name = self._extract_context(node)
        return ConcurrencyUsage(
            file=file_path,
            line=node.lineno,
            column=node.col_offset,
            pattern="await",
            statement=safe_as_string(node),
            function=function,
            class_name=class_name,
        )

    def _detect_thread_creation(
        self, node: nodes.Call, file_path: str, imports: dict[str, str]
    ) -> ConcurrencyUsage | None:
        """Detect threading.Thread() creation."""
        func_name = self._get_qualified_name(node.func, imports)
        if not func_name or "Thread" not in func_name or "ThreadPool" in func_name:
            return None

        if not ("threading.Thread" in func_name or func_name.endswith("Thread")):
            return None

        # Extract target and name
        details: dict[str, Any] = {}
        for keyword in node.keywords or []:
            if keyword.arg == "target":
                target_value = safe_infer_value(keyword.value)
                if target_value:
                    details["target"] = str(target_value)
                else:
                    details["target"] = safe_as_string(keyword.value)
            elif keyword.arg == "name":
                name_value = safe_infer_value(keyword.value)
                if name_value:
                    details["name"] = name_value

        function, class_name = self._extract_context(node)
        return ConcurrencyUsage(
            file=file_path,
            line=node.lineno,
            column=node.col_offset,
            pattern="thread_creation",
            statement=safe_as_string(node),
            function=function,
            class_name=class_name,
            details=details if details else None,
        )

    def _detect_threadpool_executor(
        self, node: nodes.Call, file_path: str, imports: dict[str, str]
    ) -> ConcurrencyUsage | None:
        """Detect ThreadPoolExecutor() creation."""
        func_name = self._get_qualified_name(node.func, imports)
        if not func_name or "ThreadPoolExecutor" not in func_name:
            return None

        # Extract max_workers
        details: dict[str, Any] = {}
        for keyword in node.keywords or []:
            if keyword.arg == "max_workers":
                max_workers = safe_infer_value(keyword.value)
                if isinstance(max_workers, int):
                    details["max_workers"] = max_workers

        function, class_name = self._extract_context(node)
        return ConcurrencyUsage(
            file=file_path,
            line=node.lineno,
            column=node.col_offset,
            pattern="thread_pool_executor",
            statement=safe_as_string(node),
            function=function,
            class_name=class_name,
            details=details if details else None,
        )

    def _detect_process_creation(
        self, node: nodes.Call, file_path: str, imports: dict[str, str]
    ) -> ConcurrencyUsage | None:
        """Detect multiprocessing.Process() creation."""
        func_name = self._get_qualified_name(node.func, imports)
        if not func_name or "Process" not in func_name or "ProcessPool" in func_name:
            return None

        if not ("multiprocessing.Process" in func_name or func_name.endswith("Process")):
            return None

        # Extract target and name
        details: dict[str, Any] = {}
        for keyword in node.keywords or []:
            if keyword.arg == "target":
                target_value = safe_infer_value(keyword.value)
                if target_value:
                    details["target"] = str(target_value)
                else:
                    details["target"] = safe_as_string(keyword.value)
            elif keyword.arg == "name":
                name_value = safe_infer_value(keyword.value)
                if name_value:
                    details["name"] = name_value

        function, class_name = self._extract_context(node)
        return ConcurrencyUsage(
            file=file_path,
            line=node.lineno,
            column=node.col_offset,
            pattern="process_creation",
            statement=safe_as_string(node),
            function=function,
            class_name=class_name,
            details=details if details else None,
        )

    def _detect_processpool_executor(
        self, node: nodes.Call, file_path: str, imports: dict[str, str]
    ) -> ConcurrencyUsage | None:
        """Detect ProcessPoolExecutor() creation."""
        func_name = self._get_qualified_name(node.func, imports)
        if not func_name or "ProcessPoolExecutor" not in func_name:
            return None

        # Extract max_workers
        details: dict[str, Any] = {}
        for keyword in node.keywords or []:
            if keyword.arg == "max_workers":
                max_workers = safe_infer_value(keyword.value)
                if isinstance(max_workers, int):
                    details["max_workers"] = max_workers

        function, class_name = self._extract_context(node)
        return ConcurrencyUsage(
            file=file_path,
            line=node.lineno,
            column=node.col_offset,
            pattern="process_pool_executor",
            statement=safe_as_string(node),
            function=function,
            class_name=class_name,
            details=details if details else None,
        )

    def _detect_executor_submit(
        self, node: nodes.Call, file_path: str, imports: dict[str, str], executor_mapping: dict[str, str]
    ) -> ConcurrencyUsage | None:
        """Detect executor.submit() calls."""
        if not isinstance(node.func, nodes.Attribute):
            return None
        if node.func.attrname != "submit":
            return None

        # Try to resolve executor variable
        if isinstance(node.func.expr, nodes.Name):
            var_name = node.func.expr.name
            executor_type = executor_mapping.get(var_name)
            if not executor_type:
                # Not a tracked executor
                return None

            # Extract submitted function
            details: dict[str, Any] = {}
            if node.args:
                func_arg = node.args[0]
                func_value = safe_infer_value(func_arg)
                if func_value:
                    details["function"] = str(func_value)
                else:
                    details["function"] = safe_as_string(func_arg)

            function, class_name = self._extract_context(node)

            # Determine pattern based on executor type
            pattern = "executor_submit_thread" if executor_type == "ThreadPoolExecutor" else "executor_submit_process"

            return ConcurrencyUsage(
                file=file_path,
                line=node.lineno,
                column=node.col_offset,
                pattern=pattern,
                statement=safe_as_string(node),
                function=function,
                class_name=class_name,
                details=details if details else None,
                api_call="submit",
            )

        return None

    def _detect_create_task(self, node: nodes.Call, file_path: str, imports: dict[str, str]) -> ConcurrencyUsage | None:
        """Detect asyncio.create_task() calls."""
        func_name = self._get_qualified_name(node.func, imports)
        if not func_name or "create_task" not in func_name:
            return None

        # Try to resolve coroutine
        if not node.args:
            return None

        coro_arg = node.args[0]
        coro_name = None

        # Try to get coroutine name
        if isinstance(coro_arg, nodes.Call):
            coro_name = self._get_qualified_name(coro_arg.func, imports)
        else:
            coro_value = safe_infer_value(coro_arg)
            if coro_value:
                coro_name = str(coro_value)

        # Skip if coroutine is unknown (per spec)
        if not coro_name or coro_name == "unknown":
            return None

        details = {"coroutine": coro_name}
        function, class_name = self._extract_context(node)

        return ConcurrencyUsage(
            file=file_path,
            line=node.lineno,
            column=node.col_offset,
            pattern="create_task",
            statement=safe_as_string(node),
            function=function,
            class_name=class_name,
            details=details,
            api_call="create_task",
        )

    def _detect_run_in_executor(
        self, node: nodes.Call, file_path: str, imports: dict[str, str], executor_mapping: dict[str, str]
    ) -> ConcurrencyUsage | None:
        """Detect loop.run_in_executor() calls."""
        if not isinstance(node.func, nodes.Attribute):
            return None
        if node.func.attrname != "run_in_executor":
            return None

        # Extract executor and function arguments
        executor_type = "<unknown-executor>"
        func_name = None

        if len(node.args) >= 2:
            # First arg is executor
            executor_arg = node.args[0]
            if isinstance(executor_arg, nodes.Name):
                executor_type = executor_mapping.get(executor_arg.name, "<unknown-executor>")
            elif isinstance(executor_arg, nodes.Const) and executor_arg.value is None:
                executor_type = "ThreadPoolExecutor"  # None means default thread pool

            # Second arg is function
            func_arg = node.args[1]
            func_value = safe_infer_value(func_arg)
            func_name = str(func_value) if func_value else safe_as_string(func_arg)

        details = {
            "executor_type": executor_type,
            "function": func_name if func_name else "unknown",
        }

        function, class_name = self._extract_context(node)

        # Determine pattern based on executor type
        pattern = "run_in_executor_process" if executor_type == "ProcessPoolExecutor" else "run_in_executor_thread"

        return ConcurrencyUsage(
            file=file_path,
            line=node.lineno,
            column=node.col_offset,
            pattern=pattern,
            statement=safe_as_string(node),
            function=function,
            class_name=class_name,
            details=details,
            api_call="run_in_executor",
        )

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

    def _get_category_from_pattern(self, pattern: str) -> str:
        """Determine category from pattern name."""
        if "thread" in pattern.lower():
            return "threading"
        elif "process" in pattern.lower():
            return "multiprocessing"
        elif "async" in pattern.lower() or pattern in ("await", "create_task"):
            return "asyncio"
        elif "celery" in pattern.lower():
            return "celery"
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

    def _calculate_summary(
        self, patterns: dict[str, dict[str, list[ConcurrencyUsage]]], scan_duration_ms: int
    ) -> ConcurrencyPatternSummary:
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
            scan_duration_ms=scan_duration_ms,
            by_category=by_category,
        )
