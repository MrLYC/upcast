"""AST visitor for detecting concurrency patterns."""

from pathlib import Path
from typing import Any

from astroid import MANAGER, nodes

from upcast.concurrency_pattern_scanner.pattern_parser import (
    parse_async_context_manager,
    parse_async_function,
    parse_asyncio_create_task,
    parse_asyncio_gather,
    parse_await_expression,
    parse_process_creation,
    parse_process_pool_executor,
    parse_run_in_executor,
    parse_thread_creation,
    parse_thread_pool_executor,
)


class ConcurrencyChecker:
    """AST visitor that detects concurrency patterns in Python modules."""

    def __init__(self, root_path: str | None = None, verbose: bool = False):
        """Initialize the checker.

        Args:
            root_path: Root path for calculating module names
            verbose: Enable verbose output
        """
        self.root_path = Path(root_path) if root_path else Path.cwd()
        self.verbose = verbose

        # Pattern collections grouped by type
        self.patterns: dict[str, dict[str, list[dict[str, Any]]]] = {
            "asyncio": {},
            "threading": {},
            "multiprocessing": {},
        }

        # Executor type mapping (variable name -> executor type)
        self.executor_types: dict[str, str] = {}

        # Current file context
        self.current_file: str = ""

    def visit_module(self, module: nodes.Module) -> None:
        """Visit a module and extract concurrency patterns.

        Args:
            module: The astroid Module node to visit
        """
        # First pass: collect executor definitions
        self._collect_executors(module)

        # Second pass: collect patterns
        self._collect_patterns(module)

    def _collect_executors(self, module: nodes.Module) -> None:
        """First pass: collect executor variable definitions.

        Args:
            module: The module to scan
        """
        for assign_node in module.nodes_of_class(nodes.Assign):
            if not isinstance(assign_node.value, nodes.Call):
                continue

            func_name = self._get_function_name(assign_node.value.func)
            if func_name in ("ThreadPoolExecutor", "ProcessPoolExecutor"):
                # Get the variable name being assigned
                for target in assign_node.targets:
                    if isinstance(target, nodes.AssignName):
                        self.executor_types[target.name] = func_name

    def _collect_patterns(self, module: nodes.Module) -> None:
        """Second pass: collect concurrency patterns.

        Args:
            module: The module to scan
        """
        # Async function definitions
        self._collect_async_functions(module)
        # Await expressions
        self._collect_await_expressions(module)
        # Async context managers
        self._collect_async_context_managers(module)
        # Function calls (gather, create_task, executors, etc.)
        self._collect_function_call_patterns(module)

    def _collect_async_functions(self, module: nodes.Module) -> None:
        """Collect async function definitions."""
        for func_node in module.nodes_of_class(nodes.AsyncFunctionDef):
            pattern = parse_async_function(func_node, self.current_file)
            if pattern:
                self._add_pattern("asyncio", "async_functions", pattern)

    def _collect_await_expressions(self, module: nodes.Module) -> None:
        """Collect await expressions."""
        for await_node in module.nodes_of_class(nodes.Await):
            pattern = parse_await_expression(await_node, self.current_file)
            if pattern:
                self._add_pattern("asyncio", "await_expressions", pattern)

    def _collect_async_context_managers(self, module: nodes.Module) -> None:
        """Collect async context managers."""
        for with_node in module.nodes_of_class(nodes.AsyncWith):
            pattern = parse_async_context_manager(with_node, self.current_file)
            if pattern:
                self._add_pattern("asyncio", "async_context_managers", pattern)

    def _collect_function_call_patterns(self, module: nodes.Module) -> None:
        """Collect patterns from function calls."""
        for call_node in module.nodes_of_class(nodes.Call):
            func_name = self._get_function_name(call_node.func)

            # Collect patterns by type
            self._collect_asyncio_call_patterns(call_node, func_name)
            self._collect_threading_call_patterns(call_node, func_name)
            self._collect_multiprocessing_call_patterns(call_node, func_name)
            self._collect_run_in_executor_pattern(call_node)

    def _collect_asyncio_call_patterns(self, call_node: nodes.Call, func_name: str | None) -> None:
        """Collect asyncio call patterns."""
        if self._is_gather_call(call_node, func_name):
            pattern = parse_asyncio_gather(call_node, self.current_file)
            if pattern:
                self._add_pattern("asyncio", "gather_patterns", pattern)
        elif self._is_create_task_call(call_node, func_name):
            pattern = parse_asyncio_create_task(call_node, self.current_file)
            if pattern:
                self._add_pattern("asyncio", "task_creation", pattern)

    def _collect_threading_call_patterns(self, call_node: nodes.Call, func_name: str | None) -> None:
        """Collect threading call patterns."""
        if func_name == "Thread":
            pattern = parse_thread_creation(call_node, self.current_file)
            if pattern:
                self._add_pattern("threading", "thread_creation", pattern)
        elif func_name == "ThreadPoolExecutor":
            pattern = parse_thread_pool_executor(call_node, self.current_file)
            if pattern:
                self._add_pattern("threading", "thread_pool_executors", pattern)

    def _collect_multiprocessing_call_patterns(self, call_node: nodes.Call, func_name: str | None) -> None:
        """Collect multiprocessing call patterns."""
        if func_name == "Process":
            pattern = parse_process_creation(call_node, self.current_file)
            if pattern:
                self._add_pattern("multiprocessing", "process_creation", pattern)
        elif func_name == "ProcessPoolExecutor":
            pattern = parse_process_pool_executor(call_node, self.current_file)
            if pattern:
                self._add_pattern("multiprocessing", "process_pool_executors", pattern)

    def _collect_run_in_executor_pattern(self, call_node: nodes.Call) -> None:
        """Collect run_in_executor pattern."""
        if isinstance(call_node.func, nodes.Attribute) and call_node.func.attrname == "run_in_executor":
            pattern = parse_run_in_executor(call_node, self.current_file, self.executor_types)
            if pattern:
                category = pattern.pop("_category", "threading")
                self._add_pattern(category, "run_in_executor", pattern)

    def _is_gather_call(self, call_node: nodes.Call, func_name: str | None) -> bool:
        """Check if call is asyncio.gather."""
        return func_name == "gather" or (
            isinstance(call_node.func, nodes.Attribute) and call_node.func.attrname == "gather"
        )

    def _is_create_task_call(self, call_node: nodes.Call, func_name: str | None) -> bool:
        """Check if call is asyncio.create_task."""
        return func_name == "create_task" or (
            isinstance(call_node.func, nodes.Attribute) and call_node.func.attrname == "create_task"
        )

    def _get_function_name(self, func_node: nodes.NodeNG) -> str | None:
        """Extract function name from various node types.

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

    def _add_pattern(self, category: str, pattern_type: str, pattern: dict[str, Any]) -> None:
        """Add a pattern to the collection.

        Args:
            category: asyncio, threading, or multiprocessing
            pattern_type: Specific pattern type within category
            pattern: Pattern data dictionary
        """
        if pattern_type not in self.patterns[category]:
            self.patterns[category][pattern_type] = []
        self.patterns[category][pattern_type].append(pattern)

    def get_patterns(self) -> dict[str, dict[str, list[dict[str, Any]]]]:
        """Get all collected patterns.

        Returns:
            Dictionary mapping categories to pattern types to pattern lists
        """
        return self.patterns

    def check_file(self, file_path: str) -> None:
        """Analyze a Python file for concurrency patterns.

        Args:
            file_path: Path to the Python file to analyze
        """
        # Store relative path
        try:
            self.current_file = str(Path(file_path).relative_to(self.root_path))
        except ValueError:
            self.current_file = file_path

        try:
            module = MANAGER.ast_from_file(file_path)
            self.visit_module(module)
        except Exception:
            # Silently skip files with parsing errors
            if self.verbose:
                import sys

                print(f"Warning: Failed to parse {file_path}", file=sys.stderr)
