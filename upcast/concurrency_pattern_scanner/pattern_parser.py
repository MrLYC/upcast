"""Pattern parsing functions for concurrency patterns."""

from typing import Any

from astroid import nodes


def parse_async_function(node: nodes.AsyncFunctionDef, file_path: str) -> dict[str, Any]:
    """Parse an async function definition.

    Args:
        node: AsyncFunctionDef node
        file_path: File path

    Returns:
        Pattern dictionary
    """
    scope_info = _get_scope_info(node)
    return {
        "file": file_path,
        "line": node.lineno,
        "function_name": node.name,
        "parameters": [arg.name for arg in node.args.args],
        **scope_info,
    }


def parse_await_expression(node: nodes.Await, file_path: str) -> dict[str, Any]:
    """Parse an await expression.

    Args:
        node: Await node
        file_path: File path

    Returns:
        Pattern dictionary
    """
    awaited_expr = _get_expression_str(node.value)
    scope_info = _get_scope_info(node)

    return {
        "file": file_path,
        "line": node.lineno,
        "awaited_expression": awaited_expr,
        **scope_info,
    }


def parse_async_context_manager(node: nodes.AsyncWith, file_path: str) -> dict[str, Any]:
    """Parse an async with statement.

    Args:
        node: AsyncWith node
        file_path: File path

    Returns:
        Pattern dictionary
    """
    context_managers = []
    for item in node.items:
        cm_expr = _get_expression_str(item[0])
        context_managers.append(cm_expr)

    scope_info = _get_scope_info(node)

    return {
        "file": file_path,
        "line": node.lineno,
        "context_managers": context_managers,
        **scope_info,
    }


def parse_asyncio_gather(node: nodes.Call, file_path: str) -> dict[str, Any]:
    """Parse asyncio.gather() call.

    Args:
        node: Call node
        file_path: File path

    Returns:
        Pattern dictionary
    """
    tasks = [_get_expression_str(arg) for arg in node.args]
    scope_info = _get_scope_info(node)

    return {
        "file": file_path,
        "line": node.lineno,
        "tasks": tasks,
        "task_count": len(tasks),
        **scope_info,
    }


def parse_asyncio_create_task(node: nodes.Call, file_path: str) -> dict[str, Any]:
    """Parse asyncio.create_task() call.

    Args:
        node: Call node
        file_path: File path

    Returns:
        Pattern dictionary
    """
    coroutine = _get_expression_str(node.args[0]) if node.args else "unknown"
    scope_info = _get_scope_info(node)

    return {
        "file": file_path,
        "line": node.lineno,
        "coroutine": coroutine,
        **scope_info,
    }


def parse_thread_creation(node: nodes.Call, file_path: str) -> dict[str, Any]:
    """Parse threading.Thread() creation.

    Args:
        node: Call node
        file_path: File path

    Returns:
        Pattern dictionary
    """
    target = None
    args_list = []

    # Extract target and args from keywords
    for keyword in node.keywords:
        if keyword.arg == "target":
            target = _get_expression_str(keyword.value)
        elif keyword.arg == "args" and isinstance(keyword.value, (nodes.Tuple, nodes.List)):
            args_list = [_get_expression_str(arg) for arg in keyword.value.elts]

    scope_info = _get_scope_info(node)

    return {
        "file": file_path,
        "line": node.lineno,
        "target": target,
        "args": args_list,
        **scope_info,
    }


def parse_thread_pool_executor(node: nodes.Call, file_path: str) -> dict[str, Any]:
    """Parse ThreadPoolExecutor creation.

    Args:
        node: Call node
        file_path: File path

    Returns:
        Pattern dictionary
    """
    max_workers = None

    # Extract max_workers
    for keyword in node.keywords:
        if keyword.arg == "max_workers":
            if isinstance(keyword.value, nodes.Const):
                max_workers = keyword.value.value
            else:
                max_workers = _get_expression_str(keyword.value)

    scope_info = _get_scope_info(node)

    return {
        "file": file_path,
        "line": node.lineno,
        "max_workers": max_workers,
        **scope_info,
    }


def parse_process_creation(node: nodes.Call, file_path: str) -> dict[str, Any]:
    """Parse multiprocessing.Process() creation.

    Args:
        node: Call node
        file_path: File path

    Returns:
        Pattern dictionary
    """
    target = None
    args_list = []

    # Extract target and args from keywords
    for keyword in node.keywords:
        if keyword.arg == "target":
            target = _get_expression_str(keyword.value)
        elif keyword.arg == "args" and isinstance(keyword.value, (nodes.Tuple, nodes.List)):
            args_list = [_get_expression_str(arg) for arg in keyword.value.elts]

    scope_info = _get_scope_info(node)

    return {
        "file": file_path,
        "line": node.lineno,
        "target": target,
        "args": args_list,
        **scope_info,
    }


def parse_process_pool_executor(node: nodes.Call, file_path: str) -> dict[str, Any]:
    """Parse ProcessPoolExecutor creation.

    Args:
        node: Call node
        file_path: File path

    Returns:
        Pattern dictionary
    """
    max_workers = None

    # Extract max_workers
    for keyword in node.keywords:
        if keyword.arg == "max_workers":
            if isinstance(keyword.value, nodes.Const):
                max_workers = keyword.value.value
            else:
                max_workers = _get_expression_str(keyword.value)

    scope_info = _get_scope_info(node)

    return {
        "file": file_path,
        "line": node.lineno,
        "max_workers": max_workers,
        **scope_info,
    }


def parse_run_in_executor(node: nodes.Call, file_path: str, executor_types: dict[str, str]) -> dict[str, Any]:
    """Parse loop.run_in_executor() call.

    Args:
        node: Call node
        file_path: File path
        executor_types: Mapping of executor variable names to types

    Returns:
        Pattern dictionary with _category key
    """
    executor_name = None
    func = None
    args_list = []

    # Extract executor, function, and args
    if len(node.args) >= 2:
        # First arg is executor (or None for default)
        if isinstance(node.args[0], nodes.Const) and node.args[0].value is None:
            executor_name = "default_thread_executor"
        else:
            executor_name = _get_expression_str(node.args[0])

        # Second arg is function
        func = _get_expression_str(node.args[1])

        # Remaining args are function arguments
        args_list = [_get_expression_str(arg) for arg in node.args[2:]]

    # Determine category based on executor type
    category = "threading"  # Default to threading
    if executor_name and executor_name in executor_types:
        executor_type = executor_types[executor_name]
        if "Process" in executor_type:
            category = "multiprocessing"

    scope_info = _get_scope_info(node)

    return {
        "file": file_path,
        "line": node.lineno,
        "executor": executor_name,
        "function": func,
        "args": args_list,
        "_category": category,  # Internal marker for categorization
        **scope_info,
    }


def _get_expression_str(node: nodes.NodeNG) -> str:
    """Get string representation of an expression.

    Args:
        node: Expression node

    Returns:
        String representation
    """
    if isinstance(node, nodes.Name):
        return node.name
    elif isinstance(node, nodes.Attribute):
        # Recursively build attribute chain
        base = _get_expression_str(node.expr)
        return f"{base}.{node.attrname}"
    elif isinstance(node, nodes.Call):
        # Get function name
        func_name = _get_expression_str(node.func)
        return f"{func_name}(...)"
    elif isinstance(node, nodes.Const):
        return repr(node.value)
    else:
        # Fallback: use as_string() but truncate if too long
        try:
            result = node.as_string()
            if len(result) > 50:
                return result[:47] + "..."
            else:
                return result
        except Exception:
            return "<expression>"


def _get_scope_info(node: nodes.NodeNG) -> dict[str, str | None]:
    """Extract scope information (function and class) from a node.

    Args:
        node: AST node

    Returns:
        Dictionary with function_context and class_context keys
    """
    function_context = None
    class_context = None

    # Walk up the parent chain to find enclosing function and class
    current = node.parent
    while current is not None:
        if isinstance(current, (nodes.FunctionDef, nodes.AsyncFunctionDef)) and function_context is None:
            function_context = current.name
        elif isinstance(current, nodes.ClassDef) and class_context is None:
            class_context = current.name
        current = current.parent

    return {
        "function_context": function_context,
        "class_context": class_context,
    }
