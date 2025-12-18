"""AST checker for blocking operations."""

import logging
from pathlib import Path

import astroid

from upcast.blocking_operation_scanner.operation_parser import (
    BlockingOperation,
    extract_imports,
    parse_lock_acquire,
    parse_lock_context,
    parse_select_for_update,
    parse_sleep_operation,
    parse_subprocess_operation,
)

logger = logging.getLogger(__name__)


class BlockingOperationChecker:
    """Check Python files for blocking operations."""

    def __init__(self) -> None:
        """Initialize the checker."""
        self.operations: list[BlockingOperation] = []

    def _check_call(
        self,
        node: astroid.Call,
        file_path: Path,
        module_imports: dict[str, str],
    ) -> None:
        """Check a function call for blocking operations."""
        # Try each parser
        operation = parse_sleep_operation(node, file_path, module_imports)
        if operation:
            self.operations.append(operation)
            return

        operation = parse_select_for_update(node, file_path)
        if operation:
            self.operations.append(operation)
            return

        operation = parse_lock_acquire(node, file_path, module_imports)
        if operation:
            self.operations.append(operation)
            return

        operation = parse_subprocess_operation(node, file_path, module_imports)
        if operation:
            self.operations.append(operation)

    def _check_with(
        self,
        node: astroid.With,
        file_path: Path,
        module_imports: dict[str, str],
    ) -> None:
        """Check with statement for lock context managers."""
        operations = parse_lock_context(node, file_path, module_imports)
        self.operations.extend(operations)

    def _traverse(
        self,
        node: astroid.NodeNG,
        file_path: Path,
        module_imports: dict[str, str],
    ) -> None:
        """Recursively traverse AST nodes."""
        if isinstance(node, astroid.Call):
            self._check_call(node, file_path, module_imports)
        elif isinstance(node, astroid.With):
            self._check_with(node, file_path, module_imports)

        # Traverse children
        for child in node.get_children():
            self._traverse(child, file_path, module_imports)

    def check_file(self, file_path: Path) -> list[BlockingOperation]:
        """Check a Python file for blocking operations.

        Args:
            file_path: Path to the Python file to check

        Returns:
            List of blocking operations found in the file
        """
        self.operations = []

        try:
            module = astroid.parse(file_path.read_text(), path=str(file_path))
            module_imports = extract_imports(module)
            self._traverse(module, file_path, module_imports)
        except Exception as e:
            logger.warning("Failed to parse %s: %s", file_path, e)

        return self.operations

    def check_module(self, module: astroid.Module, file_path: Path) -> list[BlockingOperation]:
        """Check an astroid module for blocking operations.

        Args:
            module: Parsed astroid module
            file_path: Path to the source file

        Returns:
            List of blocking operations found in the module
        """
        self.operations = []
        module_imports = extract_imports(module)
        self._traverse(module, file_path, module_imports)
        return self.operations
