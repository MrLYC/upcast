"""Parsing functions for signal patterns."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from astroid import nodes

from upcast.common.ast_utils import safe_as_string


@dataclass
class SignalUsage:
    """Represents a single usage of a signal (send or receive)."""

    file: str  # Relative path from project root
    line: int  # Line number (1-based)
    column: int  # Column number (0-based)
    pattern: str  # Usage pattern type
    code: str  # Source code snippet
    sender: str | None = None  # Sender if specified


def _get_scope_context(node: nodes.NodeNG) -> dict[str, Any]:
    """Extract scope context (enclosing class/function) for a node.

    Args:
        node: AST node to get context for

    Returns:
        Dictionary containing context type and names
    """
    context: dict[str, Any] = {"type": "function", "class": None, "enclosing_function": None}

    parent = node.parent
    while parent:
        if isinstance(parent, nodes.ClassDef):
            context["type"] = "method"
            context["class"] = parent.name
            break
        elif isinstance(parent, nodes.FunctionDef):
            if context["enclosing_function"] is None and parent != node:
                context["enclosing_function"] = parent.name
        parent = parent.parent

    if context["enclosing_function"] and not context["class"]:
        context["type"] = "nested"

    return context


def _get_relative_path(file_path: str, root_path: str | None) -> str:
    """Get relative path from root.

    Args:
        file_path: Absolute file path
        root_path: Root path for relativity

    Returns:
        Relative path string
    """
    if not root_path:
        return file_path

    try:
        return str(Path(file_path).relative_to(Path(root_path)))
    except ValueError:
        return file_path


def _extract_code_snippet(node: nodes.NodeNG, max_length: int = 100) -> str:
    """Extract source code snippet from an AST node.

    Args:
        node: The AST node
        max_length: Maximum length of snippet

    Returns:
        Source code string, truncated if needed
    """
    try:
        code = node.as_string()
        if len(code) > max_length:
            code = code[:max_length] + "..."
        else:
            return code
    except Exception:
        return "<unknown>"


def _extract_signal_name_from_call(node: nodes.Call) -> str | None:
    """Extract signal name from a .send() or .connect() call node.

    Args:
        node: Call node (e.g., post_save.send(...))

    Returns:
        Signal name or None if cannot extract
    """
    if not isinstance(node.func, nodes.Attribute):
        return None

    # Get the object calling the method (e.g., 'post_save' from 'post_save.send()')
    if isinstance(node.func.expr, nodes.Name):
        return node.func.expr.name

    return None


def _extract_signal_names_from_decorator(decorator: nodes.NodeNG) -> list[str]:
    """Extract signal names from @receiver or @signal.connect decorator.

    Args:
        decorator: Decorator node

    Returns:
        List of signal names
    """
    signal_names = []

    # Handle @receiver(signal_name) or @receiver([signal1, signal2])
    if isinstance(decorator, nodes.Call):
        if decorator.args:
            first_arg = decorator.args[0]

            # Single signal: @receiver(post_save)
            if isinstance(first_arg, nodes.Name):
                signal_names.append(first_arg.name)

            # Multiple signals: @receiver([post_save, pre_delete])
            elif isinstance(first_arg, (nodes.List, nodes.Tuple)):
                for elem in first_arg.elts:
                    if isinstance(elem, nodes.Name):
                        signal_names.append(elem.name)

            # Attribute access: @receiver(signals.post_save)
            elif isinstance(first_arg, nodes.Attribute):
                signal_names.append(first_arg.attrname)

    # Handle @signal.connect (Attribute node)
    elif isinstance(decorator, nodes.Attribute):
        signal_names.append(decorator.attrname)

    return signal_names


def _extract_sender_from_decorator(decorator: nodes.Call) -> str | None:
    """Extract sender argument from decorator.

    Args:
        decorator: Call decorator node

    Returns:
        Sender class name if found, None otherwise
    """
    # Check keyword arguments for sender
    for keyword in decorator.keywords:
        if keyword.arg == "sender":
            value = keyword.value
            if isinstance(value, nodes.Name):
                return value.name
            elif isinstance(value, nodes.Attribute):
                return value.attrname
            elif isinstance(value, nodes.Const):
                # Handle string literals like sender="Order"
                return value.value if isinstance(value.value, str) else safe_as_string(value)
            else:
                return safe_as_string(value)

    return None


def parse_receiver_decorator(func_node: nodes.FunctionDef, root_path: str | None = None) -> list[dict[str, Any]]:
    """Parse @receiver decorator pattern for Django signals.

    Args:
        func_node: Function node with @receiver decorator
        root_path: Root path for relative file paths

    Returns:
        List of handler dictionaries (one per signal if multiple)
    """
    handlers = []

    for decorator in func_node.decorators.nodes if func_node.decorators else []:
        # Check if this is a receiver decorator
        is_receiver = False

        if isinstance(decorator, nodes.Call):
            func_name = decorator.func
            if isinstance(func_name, nodes.Name) and func_name.name == "receiver":
                is_receiver = True

        if not is_receiver:
            continue

        # Extract signal names
        signal_names = _extract_signal_names_from_decorator(decorator)
        sender = _extract_sender_from_decorator(decorator)

        # Create handler entry for each signal
        for signal_name in signal_names:
            file_path = func_node.root().file if hasattr(func_node.root(), "file") else ""
            context = _get_scope_context(func_node)

            handler: dict[str, Any] = {
                "signal": signal_name,
                "handler": func_node.name,
                "file": _get_relative_path(file_path, root_path),
                "line": func_node.lineno,
                "context": context,
            }

            if sender:
                handler["sender"] = sender

            handlers.append(handler)

    return handlers


def parse_celery_connect_decorator(func_node: nodes.FunctionDef, root_path: str | None = None) -> list[dict[str, Any]]:
    """Parse @signal.connect decorator pattern for Celery signals.

    Args:
        func_node: Function node with @signal.connect decorator
        root_path: Root path for relative file paths

    Returns:
        List of handler dictionaries
    """
    handlers = []

    for decorator in func_node.decorators.nodes if func_node.decorators else []:
        # Check if this is signal.connect pattern
        is_connect = False
        signal_name = None

        if (
            isinstance(decorator, nodes.Attribute)
            and decorator.attrname == "connect"
            and isinstance(decorator.expr, nodes.Name)
        ):
            # @task_prerun.connect
            is_connect = True
            signal_name = decorator.expr.name

        if not is_connect or not signal_name:
            continue

        file_path = func_node.root().file if hasattr(func_node.root(), "file") else ""
        context = _get_scope_context(func_node)

        handler: dict[str, Any] = {
            "signal": signal_name,
            "handler": func_node.name,
            "file": _get_relative_path(file_path, root_path),
            "line": func_node.lineno,
            "context": context,
        }

        handlers.append(handler)

    return handlers


def parse_signal_connect_method(  # noqa: C901
    call_node: nodes.Call, root_path: str | None = None
) -> dict[str, Any] | None:
    """Parse signal.connect(handler) method call pattern.

    Args:
        call_node: Call node for .connect() method
        root_path: Root path for relative file paths

    Returns:
        Handler dictionary or None
    """
    # Check if this is a .connect() call
    if not isinstance(call_node.func, nodes.Attribute):
        return None

    if call_node.func.attrname != "connect":
        return None

    # Extract signal name
    signal_name = None
    if isinstance(call_node.func.expr, nodes.Name):
        signal_name = call_node.func.expr.name
    elif isinstance(call_node.func.expr, nodes.Attribute):
        signal_name = call_node.func.expr.attrname

    if not signal_name:
        return None

    # Extract handler function name
    handler_name = None
    if call_node.args:
        handler_arg = call_node.args[0]
        if isinstance(handler_arg, nodes.Name):
            handler_name = handler_arg.name
        elif isinstance(handler_arg, nodes.Attribute):
            handler_name = handler_arg.attrname
        else:
            handler_name = safe_as_string(handler_arg)

    if not handler_name:
        return None

    # Extract sender if present (Django signals)
    sender = None
    for keyword in call_node.keywords:
        if keyword.arg == "sender":
            value = keyword.value
            if isinstance(value, nodes.Name):
                sender = value.name
            elif isinstance(value, nodes.Attribute):
                sender = value.attrname
            elif isinstance(value, nodes.Const):
                # Handle string literals like sender="Order"
                sender = value.value if isinstance(value.value, str) else safe_as_string(value)
            else:
                sender = safe_as_string(value)

    file_path = call_node.root().file if hasattr(call_node.root(), "file") else ""

    handler: dict[str, Any] = {
        "signal": signal_name,
        "handler": handler_name,
        "file": _get_relative_path(file_path, root_path),
        "line": call_node.lineno,
    }

    if sender:
        handler["sender"] = sender

    return handler


def parse_custom_signal_definition(  # noqa: C901
    assign_node: nodes.Assign, root_path: str | None = None
) -> dict[str, Any] | None:
    """Parse custom Signal() definition.

    Args:
        assign_node: Assignment node with Signal() call
        root_path: Root path for relative file paths

    Returns:
        Signal definition dictionary or None
    """
    # Check if RHS is a Call to Signal()
    if not isinstance(assign_node.value, nodes.Call):
        return None

    func = assign_node.value.func
    is_signal_call = False

    if (isinstance(func, nodes.Name) and func.name == "Signal") or (
        isinstance(func, nodes.Attribute) and func.attrname == "Signal"
    ):
        is_signal_call = True

    if not is_signal_call:
        return None

    # Extract signal variable name
    signal_name = None
    if assign_node.targets:
        target = assign_node.targets[0]
        if isinstance(target, nodes.AssignName):
            signal_name = target.name

    if not signal_name:
        return None

    file_path = assign_node.root().file if hasattr(assign_node.root(), "file") else ""

    signal_def: dict[str, Any] = {
        "name": signal_name,
        "file": _get_relative_path(file_path, root_path),
        "line": assign_node.lineno,
    }

    # Extract providing_args if present (Django < 4.0)
    for keyword in assign_node.value.keywords:
        if keyword.arg == "providing_args":
            value = keyword.value
            if isinstance(value, (nodes.List, nodes.Tuple)):
                args = []
                for elem in value.elts:
                    if isinstance(elem, nodes.Const):
                        args.append(elem.value)
                    else:
                        args.append(safe_as_string(elem))
                if args:
                    signal_def["providing_args"] = args

    return signal_def


def categorize_django_signal(signal_name: str) -> str:
    """Categorize Django signal by type.

    Args:
        signal_name: Signal name

    Returns:
        Category string
    """
    model_signals = {
        "pre_init",
        "post_init",
        "pre_save",
        "post_save",
        "pre_delete",
        "post_delete",
        "m2m_changed",
        "class_prepared",
    }

    request_signals = {
        "request_started",
        "request_finished",
        "got_request_exception",
    }

    management_signals = {
        "pre_migrate",
        "post_migrate",
    }

    if signal_name in model_signals:
        return "model_signals"
    elif signal_name in request_signals:
        return "request_signals"
    elif signal_name in management_signals:
        return "management_signals"
    else:
        return "other_signals"


def categorize_celery_signal(signal_name: str) -> str:
    """Categorize Celery signal by type.

    Args:
        signal_name: Signal name

    Returns:
        Category string
    """
    task_signals = {
        "task_prerun",
        "task_postrun",
        "task_retry",
        "task_success",
        "task_failure",
        "task_revoked",
        "task_rejected",
        "task_unknown",
        "task_internal_error",
    }

    worker_signals = {
        "worker_init",
        "worker_ready",
        "worker_process_init",
        "worker_process_shutdown",
        "worker_shutdown",
        "worker_shutting_down",
    }

    beat_signals = {
        "beat_init",
        "beat_embedded_init",
    }

    if signal_name in task_signals:
        return "task_signals"
    elif signal_name in worker_signals:
        return "worker_signals"
    elif signal_name in beat_signals:
        return "beat_signals"
    else:
        return "other_signals"


def _is_signal_send_call(
    node: nodes.Call,
    django_imports: set[str],
    celery_imports: set[str],
    custom_signals: dict[str, Any],
    known_signal_names: set[str],
) -> tuple[str, str] | None:
    """Check if a Call node is a signal send.

    Validates that the object calling .send() is a known signal to avoid
    false positives like mail.send(), message.send(), etc.

    Args:
        node: The Call AST node
        django_imports: Django signal names from imports
        celery_imports: Celery signal names from imports
        custom_signals: Custom signal definitions
        known_signal_names: Signal names extracted from receivers

    Returns:
        (signal_name, method_type) tuple or None
        method_type is "send" or "send_robust"
        Returns None if not a valid signal send
    """
    # Must be method call (attribute access)
    if not isinstance(node.func, nodes.Attribute):
        return None

    # Extract method name
    method = node.func.attrname
    if method not in ("send", "send_robust"):
        return None

    # Extract signal name from node.func.expr
    signal_name = _extract_signal_name_from_call(node)
    if not signal_name:
        return None

    # Validate against known signals whitelist
    if (
        signal_name not in django_imports
        and signal_name not in celery_imports
        and signal_name not in custom_signals
        and signal_name not in known_signal_names
    ):
        # Not a known signal - likely mail.send(), etc.
        return None

    return (signal_name, method)


def parse_signal_send(
    node: nodes.Call,
    django_imports: set[str],
    celery_imports: set[str],
    custom_signals: dict[str, Any],
    known_signal_names: set[str],
    root_path: str | None,
    file_path: str,
) -> tuple[str, SignalUsage] | None:
    """Parse signal.send() or signal.send_robust() call.

    Args:
        node: Call node
        django_imports: Django signal names
        celery_imports: Celery signal names
        custom_signals: Custom signals dict
        known_signal_names: Signals with receivers
        root_path: Project root path
        file_path: Current file path

    Returns:
        (signal_name, SignalUsage) tuple or None
    """
    # Validate this is a signal send
    result = _is_signal_send_call(node, django_imports, celery_imports, custom_signals, known_signal_names)
    if not result:
        return None

    signal_name, method_type = result

    # Extract sender parameter
    sender = None
    if node.keywords:
        for keyword in node.keywords:
            if keyword.arg == "sender":
                value = keyword.value
                if isinstance(value, nodes.Name):
                    sender = value.name
                elif isinstance(value, nodes.Const):
                    sender = value.value if isinstance(value.value, str) else safe_as_string(value)
                else:
                    sender = safe_as_string(value)

    # Create SignalUsage
    pattern = "send_robust_method" if method_type == "send_robust" else "send_method"
    usage = SignalUsage(
        file=_get_relative_path(file_path, root_path),
        line=node.lineno,
        column=node.col_offset,
        pattern=pattern,
        code=_extract_code_snippet(node),
        sender=sender,
    )

    return (signal_name, usage)
