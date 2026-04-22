"""Concurrency patterns scanner implementation with Pydantic models."""

import time
from pathlib import Path
from typing import Any, ClassVar

from astroid import nodes

from upcast.common.ast_utils import get_import_info, safe_as_string
from upcast.common.file_utils import get_relative_path_str
from upcast.common.inference import infer_value
from upcast.common.scanner_base import BaseScanner
from upcast.models.concurrency import ConcurrencyPatternOutput, ConcurrencyPatternSummary, ConcurrencyUsage


class ConcurrencyScanner(BaseScanner[ConcurrencyPatternOutput]):
    """Scanner for concurrency patterns (threading, multiprocessing, asyncio, celery)."""

    # Executor types for resolution
    EXECUTOR_TYPES: ClassVar[set[str]] = {
        "ThreadPoolExecutor",
        "ProcessPoolExecutor",
    }

    CELERY_TASK_DECORATORS: ClassVar[set[str]] = {"celery.shared_task"}
    CELERY_TASK_CALLS: ClassVar[set[str]] = {"delay", "apply_async"}

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
            self._scan_file_patterns(file_path, base_path, patterns)

        scan_duration_ms = int((time.time() - start_time) * 1000)
        summary = self._calculate_summary(patterns, scan_duration_ms)
        return ConcurrencyPatternOutput(
            summary=summary, results=patterns, metadata={"scanner_name": "concurrency-patterns"}
        )

    def _scan_file_patterns(
        self,
        file_path: Path,
        base_path: Path,
        patterns: dict[str, dict[str, list[ConcurrencyUsage]]],
    ) -> None:
        """Scan a single file and merge detected concurrency patterns."""
        module = self.parse_file(file_path)
        if not module:
            return

        imports = get_import_info(module)
        rel_path = get_relative_path_str(file_path, base_path)
        celery_app_names = self._build_celery_app_mapping(module, imports)
        celery_task_names = self._collect_celery_task_names(module, imports, celery_app_names)
        executor_mapping = self._build_executor_mapping(module, imports)

        self._collect_decorator_patterns(module, rel_path, imports, celery_app_names, patterns)
        self._collect_async_patterns(module, rel_path, imports, celery_app_names, patterns)
        self._collect_await_patterns(module, rel_path, patterns)
        self._collect_call_patterns(module, rel_path, imports, executor_mapping, celery_task_names, patterns)

    def _collect_decorator_patterns(
        self,
        module: nodes.Module,
        rel_path: str,
        imports: dict[str, str],
        celery_app_names: set[str],
        patterns: dict[str, dict[str, list[ConcurrencyUsage]]],
    ) -> None:
        """Collect Celery task decorator patterns from synchronous functions."""
        for node in module.nodes_of_class(nodes.FunctionDef):
            celery_usage = self._detect_celery_task_decorator(node, rel_path, imports, celery_app_names)
            if celery_usage:
                self._add_pattern(patterns, "celery", celery_usage.pattern, celery_usage)

    def _collect_async_patterns(
        self,
        module: nodes.Module,
        rel_path: str,
        imports: dict[str, str],
        celery_app_names: set[str],
        patterns: dict[str, dict[str, list[ConcurrencyUsage]]],
    ) -> None:
        """Collect patterns emitted by async function definitions."""
        for node in module.nodes_of_class(nodes.AsyncFunctionDef):
            celery_usage = self._detect_celery_task_decorator(node, rel_path, imports, celery_app_names)
            if celery_usage:
                self._add_pattern(patterns, "celery", celery_usage.pattern, celery_usage)

            function, class_name = self._extract_context(node)
            usage = ConcurrencyUsage(
                file=rel_path,
                line=node.lineno,
                column=node.col_offset,
                pattern="async_function",
                statement=f"async def {node.name}",
                function=function,
                class_name=class_name,
                block=self._get_block_name(node),
                details=None,
                api_call=None,
            )
            self._add_pattern(patterns, "asyncio", "async_function", usage)

    def _collect_await_patterns(
        self,
        module: nodes.Module,
        rel_path: str,
        patterns: dict[str, dict[str, list[ConcurrencyUsage]]],
    ) -> None:
        """Collect await-expression patterns."""
        for node in module.nodes_of_class(nodes.Await):
            usage = self._detect_await(node, rel_path)
            if usage:
                self._add_pattern(patterns, "asyncio", "await", usage)

    def _collect_call_patterns(
        self,
        module: nodes.Module,
        rel_path: str,
        imports: dict[str, str],
        executor_mapping: dict[str, str],
        celery_task_names: set[str],
        patterns: dict[str, dict[str, list[ConcurrencyUsage]]],
    ) -> None:
        """Collect call-driven concurrency patterns."""
        for node in module.nodes_of_class(nodes.Call):
            usage = self._detect_call_pattern(node, rel_path, imports, executor_mapping, celery_task_names)
            if usage:
                category = self._get_category_from_pattern(usage.pattern)
                pattern_type = usage.api_call or usage.pattern
                self._add_pattern(patterns, category, pattern_type, usage)

    def _detect_call_pattern(
        self,
        node: nodes.Call,
        rel_path: str,
        imports: dict[str, str],
        executor_mapping: dict[str, str],
        celery_task_names: set[str],
    ) -> ConcurrencyUsage | None:
        """Detect a concurrency pattern from a call node using existing detector order."""
        return (
            self._detect_thread_creation(node, rel_path, imports)
            or self._detect_threadpool_executor(node, rel_path, imports)
            or self._detect_process_creation(node, rel_path, imports)
            or self._detect_processpool_executor(node, rel_path, imports)
            or self._detect_executor_submit(node, rel_path, imports, executor_mapping)
            or self._detect_create_task(node, rel_path, imports)
            or self._detect_run_in_executor(node, rel_path, imports, executor_mapping)
            or self._detect_celery_task_call(node, rel_path, celery_task_names)
        )

    def _build_celery_app_mapping(self, module: nodes.Module, imports: dict[str, str]) -> set[str]:
        """Collect variable names bound to Celery app instances."""
        app_names: set[str] = set()

        for node in module.nodes_of_class(nodes.Assign):
            if not isinstance(node.value, nodes.Call):
                continue

            func_name = self._get_qualified_name(node.value.func, imports)
            if func_name != "celery.Celery":
                continue

            for target in node.targets:
                if isinstance(target, nodes.AssignName):
                    app_names.add(target.name)

        return app_names

    def _collect_celery_task_names(
        self, module: nodes.Module, imports: dict[str, str], celery_app_names: set[str]
    ) -> set[str]:
        """Collect function names declared as Celery tasks."""
        task_names: set[str] = set()

        for node in module.nodes_of_class((nodes.FunctionDef, nodes.AsyncFunctionDef)):
            if self._get_celery_decorator_pattern(node, imports, celery_app_names):
                task_names.add(node.name)

        return task_names

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
            block=self._get_block_name(node),
            details=None,
            api_call=None,
        )

    def _detect_thread_creation(
        self, node: nodes.Call, file_path: str, imports: dict[str, str]
    ) -> ConcurrencyUsage | None:
        """Detect threading.Thread() creation."""
        func_name = self._get_qualified_name(node.func, imports)
        if not func_name or "Thread" not in func_name or "ThreadPool" in func_name:
            return None

        # Only accept threading.Thread, reject custom Thread classes
        if func_name != "threading.Thread":
            return None

        # Extract target and name
        details: dict[str, Any] = {}
        for keyword in node.keywords or []:
            if keyword.arg == "target":
                target_value = infer_value(keyword.value).get_exact()
                if target_value:
                    details["target"] = str(target_value)
                else:
                    details["target"] = safe_as_string(keyword.value)
            elif keyword.arg == "name":
                name_value = infer_value(keyword.value).get_exact()
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
            block=self._get_block_name(node),
            details=details if details else None,
            api_call=None,
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
                max_workers = infer_value(keyword.value).get_if_type(int)
                if max_workers is not None:
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
            block=self._get_block_name(node),
            details=details if details else None,
            api_call=None,
        )

    def _detect_process_creation(
        self, node: nodes.Call, file_path: str, imports: dict[str, str]
    ) -> ConcurrencyUsage | None:
        """Detect multiprocessing.Process() creation."""
        func_name = self._get_qualified_name(node.func, imports)
        if not func_name or "Process" not in func_name or "ProcessPool" in func_name:
            return None

        # Only accept multiprocessing.Process, reject dataclasses and custom Process classes
        if func_name != "multiprocessing.Process":
            return None

        # Extract target and name
        details: dict[str, Any] = {}
        for keyword in node.keywords or []:
            if keyword.arg == "target":
                target_value = infer_value(keyword.value).get_exact()
                if target_value:
                    details["target"] = str(target_value)
                else:
                    details["target"] = safe_as_string(keyword.value)
            elif keyword.arg == "name":
                name_value = infer_value(keyword.value).get_exact()
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
            block=self._get_block_name(node),
            details=details if details else None,
            api_call=None,
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
                max_workers = infer_value(keyword.value).get_if_type(int)
                if max_workers is not None:
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
            block=self._get_block_name(node),
            details=details if details else None,
            api_call=None,
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
                func_value = infer_value(func_arg).get_exact()
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
                block=self._get_block_name(node),
                details=details if details else None,
                api_call="submit",
            )

        return None

    def _detect_create_task(self, node: nodes.Call, file_path: str, imports: dict[str, str]) -> ConcurrencyUsage | None:
        """Detect asyncio.create_task() calls."""
        func_name = self._get_qualified_name(node.func, imports)
        if func_name not in {"asyncio.create_task", "create_task"}:
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
            coro_value = infer_value(coro_arg).get_exact()
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
            block=self._get_block_name(node),
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
            func_value = infer_value(func_arg).get_exact()
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
            block=self._get_block_name(node),
            details=details,
            api_call="run_in_executor",
        )

    def _get_celery_decorator_pattern(
        self,
        node: nodes.FunctionDef | nodes.AsyncFunctionDef,
        imports: dict[str, str],
        celery_app_names: set[str],
    ) -> str | None:
        """Return the Celery pattern name for a task decorator."""
        if not node.decorators:
            return None

        for decorator in node.decorators.nodes:
            decorator_func = decorator.func if isinstance(decorator, nodes.Call) else decorator
            qualified_name = self._get_qualified_name(decorator_func, imports)

            if qualified_name in self.CELERY_TASK_DECORATORS:
                return "celery_shared_task"

            if (
                isinstance(decorator_func, nodes.Attribute)
                and decorator_func.attrname == "task"
                and isinstance(decorator_func.expr, nodes.Name)
                and decorator_func.expr.name in celery_app_names
            ):
                return "celery_app_task"

        return None

    def _detect_celery_task_decorator(
        self,
        node: nodes.FunctionDef | nodes.AsyncFunctionDef,
        file_path: str,
        imports: dict[str, str],
        celery_app_names: set[str],
    ) -> ConcurrencyUsage | None:
        """Detect Celery task decorators on functions."""
        pattern = self._get_celery_decorator_pattern(node, imports, celery_app_names)
        if not pattern:
            return None

        function, class_name = self._extract_context(node)
        statement_prefix = "async def" if isinstance(node, nodes.AsyncFunctionDef) else "def"
        return ConcurrencyUsage(
            file=file_path,
            line=node.lineno,
            column=node.col_offset,
            pattern=pattern,
            statement=f"{statement_prefix} {node.name}",
            function=function,
            class_name=class_name,
            block=self._get_block_name(node),
            details=None,
            api_call=None,
        )

    def _detect_celery_task_call(
        self, node: nodes.Call, file_path: str, celery_task_names: set[str]
    ) -> ConcurrencyUsage | None:
        """Detect Celery task invocation calls like .delay() and .apply_async()."""
        if not isinstance(node.func, nodes.Attribute):
            return None
        if node.func.attrname not in self.CELERY_TASK_CALLS:
            return None
        if not isinstance(node.func.expr, nodes.Name):
            return None
        if node.func.expr.name not in celery_task_names:
            return None
        if self._is_shadowed_in_scope(node, node.func.expr.name):
            return None
        function, class_name = self._extract_context(node)
        return ConcurrencyUsage(
            file=file_path,
            line=node.lineno,
            column=node.col_offset,
            pattern=f"celery_{node.func.attrname}",
            statement=safe_as_string(node),
            function=function,
            class_name=class_name,
            block=self._get_block_name(node),
            details={"task": node.func.expr.name},
            api_call=node.func.attrname,
        )

    def _is_shadowed_in_scope(self, node: nodes.NodeNG, name: str) -> bool:
        """Return True when a local scope shadows a module-level Celery task name."""
        scope = node.scope()
        if not isinstance(scope, (nodes.FunctionDef, nodes.AsyncFunctionDef)):
            return False

        return self._scope_has_shadowing_argument(scope, name) or self._scope_has_shadowing_binding(scope, node, name)

    def _scope_has_shadowing_argument(
        self,
        scope: nodes.FunctionDef | nodes.AsyncFunctionDef,
        name: str,
    ) -> bool:
        """Return True when a function argument shadows a Celery task name."""
        if any(arg.name == name for arg in scope.args.arguments):
            return True
        if scope.args.vararg and scope.args.vararg == name:
            return True
        if scope.args.kwarg and scope.args.kwarg == name:
            return True
        if any(arg.name == name for arg in getattr(scope.args, "posonlyargs", [])):
            return True
        return any(arg.name == name for arg in scope.args.kwonlyargs)

    def _scope_has_shadowing_binding(
        self,
        scope: nodes.FunctionDef | nodes.AsyncFunctionDef,
        node: nodes.NodeNG,
        name: str,
    ) -> bool:
        """Return True when an earlier binding in scope shadows a Celery task name."""
        for child in scope.body:
            if child.fromlineno >= node.lineno:
                break
            if self._child_contains_shadowing_binding(child, name):
                return True
        return False

    def _child_contains_shadowing_binding(self, child: nodes.NodeNG, name: str) -> bool:
        """Return True when a scope child contains a binding for the given name."""
        binding_node_types = (
            nodes.AssignName,
            nodes.AnnAssign,
            nodes.ExceptHandler,
            nodes.With,
            nodes.For,
            nodes.AsyncFor,
        )
        return any(self._binding_shadows_name(assign, name) for assign in child.nodes_of_class(binding_node_types))

    def _binding_shadows_name(self, binding: nodes.NodeNG, name: str) -> bool:
        """Return True when a binding node assigns the target name."""
        if isinstance(binding, nodes.AssignName):
            return binding.name == name
        if isinstance(binding, nodes.AnnAssign):
            return isinstance(binding.target, nodes.AssignName) and binding.target.name == name
        if isinstance(binding, nodes.ExceptHandler):
            return binding.name == name
        if isinstance(binding, (nodes.For, nodes.AsyncFor)):
            return isinstance(binding.target, nodes.AssignName) and binding.target.name == name
        if isinstance(binding, nodes.With):
            return any(isinstance(alias, nodes.AssignName) and alias.name == name for _ctx, alias in binding.items)
        return False

    def _get_block_name(self, node: nodes.NodeNG) -> str | None:
        """Get immediate containing block name (if, for, while, etc.)."""
        parent = node.parent
        if isinstance(parent, nodes.If):
            return "if"
        elif isinstance(parent, nodes.For):
            return "for"
        elif isinstance(parent, nodes.While):
            return "while"
        elif isinstance(parent, nodes.With):
            return "with"
        elif isinstance(parent, nodes.Try):
            return "try"
        elif isinstance(parent, nodes.ExceptHandler):
            return "except"
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

    def _get_category_from_pattern(self, pattern: str) -> str:
        """Determine category from pattern name."""
        if "thread" in pattern.lower():
            return "threading"
        elif "process" in pattern.lower():
            return "multiprocessing"
        elif "celery" in pattern.lower():
            return "celery"
        elif "async" in pattern.lower() or pattern in ("await", "create_task"):
            return "asyncio"
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
