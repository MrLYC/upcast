"""Parse blocking operations from Python AST."""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import astroid


class OperationType(str, Enum):
    """Types of blocking operations."""

    TIME_SLEEP = "time_based.sleep"
    DB_SELECT_FOR_UPDATE = "database.select_for_update"
    LOCK_ACQUIRE = "synchronization.lock_acquire"
    LOCK_CONTEXT = "synchronization.lock_context"
    SUBPROCESS_RUN = "subprocess.run"
    SUBPROCESS_WAIT = "subprocess.wait"
    SUBPROCESS_COMMUNICATE = "subprocess.communicate"


@dataclass
class BlockingOperation:
    """Represents a detected blocking operation."""

    type: OperationType
    file: str
    line: int
    column: int
    statement: str
    function: str | None = None
    class_name: str | None = None
    is_async_context: bool = False
    duration: Any | None = None  # For sleep operations
    timeout: Any | None = None  # For operations with timeout parameter
    parameters: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for export."""
        result = {
            "type": self.type.value,
            "location": f"{self.file}:{self.line}:{self.column}",
            "statement": self.statement,
        }

        if self.function:
            result["function"] = self.function
        if self.class_name:
            result["class"] = self.class_name
        if self.is_async_context:
            result["async_context"] = True
        if self.duration is not None:
            result["duration"] = self.duration
        if self.timeout is not None:
            result["timeout"] = self.timeout
        if self.parameters:
            result["parameters"] = self.parameters

        return result


def get_statement_code(node: astroid.NodeNG) -> str:
    """Extract source code for a statement."""
    try:
        return node.as_string()
    except Exception:
        return "<source unavailable>"


def extract_literal_value(node: astroid.NodeNG) -> Any | None:
    """Extract literal value from AST node."""
    if isinstance(node, astroid.Const):
        return node.value
    return None


def extract_function_context(node: astroid.NodeNG) -> tuple[str | None, str | None, bool]:
    """Extract function and class context for a node.

    Returns:
        Tuple of (function_name, class_name, is_async)
    """
    current = node
    function_name = None
    class_name = None
    is_async = False

    while current:
        if isinstance(current, (astroid.FunctionDef, astroid.AsyncFunctionDef)):
            if function_name is None:
                function_name = current.name
                # Check if it's an AsyncFunctionDef
                is_async = isinstance(current, astroid.AsyncFunctionDef)
        elif isinstance(current, astroid.ClassDef) and class_name is None:
            class_name = current.name

        current = current.parent

    return function_name, class_name, is_async


def parse_sleep_operation(
    node: astroid.Call,
    file_path: Path,
    module_imports: dict[str, str],
) -> BlockingOperation | None:
    """Parse time.sleep() operations."""
    # Check if this is a sleep call
    is_sleep = False
    if isinstance(node.func, astroid.Attribute) and node.func.attrname == "sleep":
        # time.sleep()
        if isinstance(node.func.expr, astroid.Name) and node.func.expr.name == "time":
            is_sleep = True
    elif isinstance(node.func, astroid.Name) and node.func.name == "sleep" and module_imports.get("sleep") == "time":
        # from time import sleep
        is_sleep = True

    if not is_sleep:
        return None

    # Extract duration if available
    duration = None
    if node.args:
        duration = extract_literal_value(node.args[0])
        if duration is None:
            # Variable duration - get expression
            duration = get_statement_code(node.args[0])

    function_name, class_name, is_async = extract_function_context(node)

    return BlockingOperation(
        type=OperationType.TIME_SLEEP,
        file=str(file_path),
        line=node.lineno,
        column=node.col_offset,
        statement=get_statement_code(node),
        function=function_name,
        class_name=class_name,
        is_async_context=is_async,
        duration=duration,
    )


def parse_select_for_update(
    node: astroid.Call,
    file_path: Path,
) -> BlockingOperation | None:
    """Parse Django ORM select_for_update() operations."""
    if not isinstance(node.func, astroid.Attribute):
        return None

    if node.func.attrname != "select_for_update":
        return None

    # Extract timeout and other parameters
    parameters = {}
    timeout = None

    for keyword in node.keywords:
        if keyword.arg == "timeout":
            timeout = extract_literal_value(keyword.value)
            if timeout is None:
                timeout = get_statement_code(keyword.value)
        elif keyword.arg:
            parameters[keyword.arg] = extract_literal_value(keyword.value) or get_statement_code(keyword.value)

    function_name, class_name, is_async = extract_function_context(node)

    return BlockingOperation(
        type=OperationType.DB_SELECT_FOR_UPDATE,
        file=str(file_path),
        line=node.lineno,
        column=node.col_offset,
        statement=get_statement_code(node),
        function=function_name,
        class_name=class_name,
        is_async_context=is_async,
        timeout=timeout,
        parameters=parameters,
    )


def parse_lock_acquire(  # noqa: C901
    node: astroid.Call,
    file_path: Path,
    module_imports: dict[str, str],
) -> BlockingOperation | None:
    """Parse threading lock acquire() operations."""
    if not isinstance(node.func, astroid.Attribute):
        return None

    if node.func.attrname != "acquire":
        return None

    # Check if this is a threading lock/rlock/semaphore
    is_lock = False
    expr = node.func.expr

    # Handle Lock().acquire(), RLock().acquire(), etc.
    if isinstance(expr, astroid.Call) and isinstance(expr.func, astroid.Attribute):
        lock_types = ["Lock", "RLock", "Semaphore", "BoundedSemaphore"]
        if expr.func.attrname in lock_types:
            if isinstance(expr.func.expr, astroid.Name) and expr.func.expr.name == "threading":
                is_lock = True
            # Check for imported lock types
            elif isinstance(expr.func.expr, astroid.Name):
                imported_from = module_imports.get(expr.func.expr.name)
                if imported_from == "threading":
                    is_lock = True

    # Also try to infer the type of the expression (for lock = threading.Lock(); lock.acquire())
    if not is_lock:
        try:
            inferred = next(expr.infer(), None)
            if inferred and hasattr(inferred, "pytype"):
                pytype_str = inferred.pytype()
                # Check if it's a threading lock type
                if "threading" in pytype_str and any(
                    lock_type in pytype_str for lock_type in ["Lock", "RLock", "Semaphore", "BoundedSemaphore"]
                ):
                    is_lock = True
        except Exception:  # noqa: S110
            pass

    if not is_lock:
        return None

    # Extract timeout and blocking parameters
    parameters = {}
    timeout = None

    for keyword in node.keywords:
        if keyword.arg == "timeout":
            timeout = extract_literal_value(keyword.value)
            if timeout is None:
                timeout = get_statement_code(keyword.value)
        elif keyword.arg:
            parameters[keyword.arg] = extract_literal_value(keyword.value) or get_statement_code(keyword.value)

    function_name, class_name, is_async = extract_function_context(node)

    return BlockingOperation(
        type=OperationType.LOCK_ACQUIRE,
        file=str(file_path),
        line=node.lineno,
        column=node.col_offset,
        statement=get_statement_code(node),
        function=function_name,
        class_name=class_name,
        is_async_context=is_async,
        timeout=timeout,
        parameters=parameters,
    )


def parse_lock_context(
    node: astroid.With,
    file_path: Path,
    module_imports: dict[str, str],
) -> list[BlockingOperation]:
    """Parse threading lock context manager usage."""
    operations = []

    for item in node.items:
        context_expr = item[0]

        # Check if this is Lock(), RLock(), etc.
        is_lock = False
        if isinstance(context_expr, astroid.Call) and isinstance(context_expr.func, astroid.Attribute):
            lock_types = ["Lock", "RLock", "Semaphore", "BoundedSemaphore"]
            if (
                context_expr.func.attrname in lock_types
                and isinstance(context_expr.func.expr, astroid.Name)
                and (
                    context_expr.func.expr.name == "threading"
                    or module_imports.get(context_expr.func.expr.name) == "threading"
                )
            ):
                is_lock = True

        if is_lock:
            function_name, class_name, is_async = extract_function_context(node)

            operations.append(
                BlockingOperation(
                    type=OperationType.LOCK_CONTEXT,
                    file=str(file_path),
                    line=node.lineno,
                    column=node.col_offset,
                    statement=get_statement_code(context_expr),
                    function=function_name,
                    class_name=class_name,
                    is_async_context=is_async,
                )
            )

    return operations


def parse_subprocess_operation(  # noqa: C901
    node: astroid.Call,
    file_path: Path,
    module_imports: dict[str, str],
) -> BlockingOperation | None:
    """Parse subprocess operations (run, wait, communicate)."""
    operation_type = None

    # Check for subprocess.run()
    if isinstance(node.func, astroid.Attribute):
        if node.func.attrname == "run":
            if isinstance(node.func.expr, astroid.Name) and node.func.expr.name == "subprocess":
                operation_type = OperationType.SUBPROCESS_RUN
        elif node.func.attrname in ["wait", "communicate"]:
            # Could be Popen.wait() or proc.wait()
            operation_type = (
                OperationType.SUBPROCESS_WAIT if node.func.attrname == "wait" else OperationType.SUBPROCESS_COMMUNICATE
            )
    elif isinstance(node.func, astroid.Name) and node.func.name == "run" and module_imports.get("run") == "subprocess":
        # from subprocess import run
        operation_type = OperationType.SUBPROCESS_RUN

    if operation_type is None:
        return None

    # Extract timeout parameter
    parameters = {}
    timeout = None

    for keyword in node.keywords:
        if keyword.arg == "timeout":
            timeout = extract_literal_value(keyword.value)
            if timeout is None:
                timeout = get_statement_code(keyword.value)
        elif keyword.arg:
            parameters[keyword.arg] = extract_literal_value(keyword.value) or get_statement_code(keyword.value)

    # Extract command for subprocess.run
    if operation_type == OperationType.SUBPROCESS_RUN and node.args:
        cmd = extract_literal_value(node.args[0])
        if cmd is None:
            cmd = get_statement_code(node.args[0])
        parameters["command"] = cmd

    function_name, class_name, is_async = extract_function_context(node)

    return BlockingOperation(
        type=operation_type,
        file=str(file_path),
        line=node.lineno,
        column=node.col_offset,
        statement=get_statement_code(node),
        function=function_name,
        class_name=class_name,
        is_async_context=is_async,
        timeout=timeout,
        parameters=parameters,
    )


def extract_imports(module: astroid.Module) -> dict[str, str]:
    """Extract import mappings from a module.

    Returns a dict mapping names to their source modules.
    """
    imports = {}

    for node in module.body:
        if isinstance(node, astroid.Import):
            for name, alias in node.names:
                # For 'import time', map both 'time' -> 'time'
                imported_name = alias or name
                # Handle multi-level imports like 'import os.path'
                base_module = name.split(".")[0]
                imports[imported_name] = base_module
        elif isinstance(node, astroid.ImportFrom):
            module_name = node.modname
            for name, alias in node.names:
                imports[alias or name] = module_name

    return imports
