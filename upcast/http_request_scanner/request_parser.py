"""HTTP request parsing and extraction logic."""

import logging
from dataclasses import dataclass, field

from astroid import nodes

from upcast.common.ast_utils import infer_value_with_fallback

logger = logging.getLogger(__name__)


@dataclass
class HttpRequest:
    """Represents a single HTTP request call."""

    location: str  # "file.py:line"
    statement: str  # Original code statement
    library: str  # "requests" | "httpx" | "aiohttp" | etc.
    url: str  # Extracted or inferred URL
    method: str  # "GET" | "POST" | etc.
    params: dict = field(default_factory=dict)  # Query parameters
    headers: dict = field(default_factory=dict)  # HTTP headers
    json_body: dict | None = None  # JSON request body
    data: dict | None = None  # Form data
    timeout: int | float | None = None  # Timeout value
    session_based: bool = False  # Whether called via session
    is_async: bool = False  # Whether using async/await


def _is_http_method(method_name: str) -> bool:
    """Check if method name is an HTTP method."""
    http_methods = ["get", "post", "put", "delete", "patch", "head", "options", "request"]
    return method_name in http_methods


def _get_original_module_name(name_node: nodes.Name) -> str | None:
    """Get the original module name from an import, handling aliases.

    Args:
        name_node: Name node to trace

    Returns:
        Original module name if it's an import, None otherwise
    """
    try:
        scope = name_node.scope()
        var_name = name_node.name

        if var_name in scope.locals:
            for local_node in scope.locals[var_name]:
                # Check if it's from an import statement
                if isinstance(local_node, nodes.Import):
                    # Direct import: import requests [as req]
                    for module_name, alias in local_node.names:
                        if alias == var_name or (alias is None and module_name == var_name):
                            return module_name
                elif isinstance(local_node, nodes.ImportFrom):
                    # From import: from requests import Session [as S]
                    # Return the module name
                    return local_node.modname
    except Exception as e:
        logger.debug(f"Failed to get original module name: {e}")
    return None


def _infer_session_type(node: nodes.Name) -> str | None:
    """Infer the library type from a session/client variable.

    Args:
        node: Name node representing session/client variable

    Returns:
        Library name or None
    """
    try:
        for inferred in node.infer():
            if hasattr(inferred, "qname"):
                qname = inferred.qname()
                if "requests" in qname:
                    return "requests"
                elif "httpx" in qname:
                    return "httpx"
                elif "aiohttp" in qname:
                    return "aiohttp"
    except Exception as e:
        logger.debug(f"Failed to infer type: {e}")
    return None


def _check_inferred_type(inferred, base_name: str, method_name: str) -> str | None:
    """Check inferred type and return library name if valid.

    Args:
        inferred: Inferred astroid node
        base_name: Variable name being checked
        method_name: HTTP method name

    Returns:
        Library name if valid, None if should be rejected or continue checking
    """
    if not hasattr(inferred, "qname"):
        return None

    qname = inferred.qname()

    # REJECT built-in types - these are definitely not HTTP libraries
    if qname in [
        "builtins.dict",
        "builtins.list",
        "builtins.tuple",
        "builtins.set",
        "builtins.str",
        "builtins.int",
        "builtins.float",
    ]:
        logger.debug(f"Rejecting {base_name}.{method_name}() - base is {qname}")
        return "REJECT"

    # REJECT local classes/functions (qname starts with '.')
    if isinstance(qname, str) and qname.startswith("."):
        logger.debug(f"Rejecting {base_name}.{method_name}() - base is local class/function")
        return "REJECT"

    # ACCEPT if qname contains library name
    if isinstance(qname, str):
        qname_lower = qname.lower()
        if "requests" in qname_lower:
            return "requests"
        elif "httpx" in qname_lower:
            return "httpx"
        elif "aiohttp" in qname_lower:
            return "aiohttp"
        elif "urllib3" in qname_lower:
            return "urllib3"

    return None


def _handle_uninferable(name_node: nodes.Name, base_name: str) -> str | None:
    """Handle Uninferable case by checking imports and name.

    Args:
        name_node: Name node to check
        base_name: Variable name

    Returns:
        Library name if detected, None otherwise
    """
    # Try to get original module name from imports (for aliases)
    original_module = _get_original_module_name(name_node)
    if original_module in ["requests", "httpx", "aiohttp", "urllib3"]:
        return original_module
    # Fall back to name-based detection for known library names
    if base_name in ["requests", "httpx", "aiohttp", "urllib3"]:
        return base_name
    # Check for common session/client variable names
    if base_name in ["session", "s", "client"]:
        return _infer_session_type(name_node)
    return None


def _detect_attribute_call(node: nodes.Call) -> str | None:
    """Detect HTTP request from attribute call like requests.get()."""
    method_name = node.func.attrname

    # Check if method name matches HTTP methods
    if not _is_http_method(method_name):
        return None

    # Try to infer the base object
    if not isinstance(node.func.expr, nodes.Name):
        return None

    base_name = node.func.expr.name

    # Step 1: Infer what the name ACTUALLY points to at this specific location
    # This is the most reliable way to prevent false positives
    try:
        for inferred in node.func.expr.infer():
            # Check the inferred type
            result = _check_inferred_type(inferred, base_name, method_name)
            if result == "REJECT":
                return None
            if result:  # Found a library
                return result

            # Handle Uninferable case (external modules)
            if type(inferred).__name__ == "UninferableBase":
                return _handle_uninferable(node.func.expr, base_name)
    except Exception as e:
        logger.debug(f"Failed to infer base object type: {e}")
        # Last resort: conservative name-based check
        if base_name in ["requests", "httpx", "aiohttp", "urllib3"]:
            return base_name

    return None


def _detect_name_call(node: nodes.Call) -> str | None:
    """Detect HTTP request from direct function call like get()."""
    func_name = node.func.name
    http_methods = ["get", "post", "put", "delete", "patch", "head", "options"]

    if func_name not in http_methods and func_name != "urlopen":
        return None

    # Try to infer where it comes from
    try:
        for inferred in node.func.infer():
            if hasattr(inferred, "qname"):
                qname = inferred.qname()
                if "requests" in qname:
                    return "requests"
                elif "httpx" in qname:
                    return "httpx"
                elif "urllib.request" in qname:
                    return "urllib.request"
    except Exception as e:
        logger.debug(f"Failed to infer import: {e}")

    return None


def detect_request_call(node: nodes.Call) -> str | None:
    """Detect if this call is an HTTP request and return the library name.

    Args:
        node: astroid Call node to check

    Returns:
        Library name if detected, None otherwise
    """
    # Check if it's an attribute access (e.g., requests.get, session.post)
    if isinstance(node.func, nodes.Attribute):
        return _detect_attribute_call(node)

    # Check for direct function calls (e.g., from requests import get)
    if isinstance(node.func, nodes.Name):
        return _detect_name_call(node)

    return None


def _extract_format_string_template(call_node: nodes.Call) -> str | None:
    """Extract URL template from str.format() call.

    Args:
        call_node: Call node for .format() method

    Returns:
        URL template with {} replaced by ..., or None if cannot extract
    """
    try:
        # Get the string being formatted (the object .format() is called on)
        if isinstance(call_node.func, nodes.Attribute):
            format_string_node = call_node.func.expr

            # Try to get the string literal
            if isinstance(format_string_node, nodes.Const):
                template = str(format_string_node.value)
                # Replace {} placeholders with ...
                # Handle both {} and {name} patterns
                import re

                result = re.sub(r"\{[^}]*\}", "...", template)
                return result
    except Exception as e:
        logger.debug(f"Failed to extract format string template: {e}")
    return None


def _extract_url_from_node(url_node: nodes.NodeNG) -> str | None:  # noqa: C901
    """Extract URL from node with variable placeholder support.

    For unresolvable variables, uses { variable_name } format.
    Returns None if URL is entirely a single variable.

    Args:
        url_node: AST node containing URL

    Returns:
        URL string with placeholders, or None to skip
    """
    # Handle f-strings (JoinedStr nodes)
    if isinstance(url_node, nodes.JoinedStr):
        # Check if it's a single variable
        if len(url_node.values) == 1 and isinstance(url_node.values[0], nodes.FormattedValue):
            # Single variable like f"{url}" - skip this request
            return None

        # Build URL with variable placeholders
        parts = []
        for value in url_node.values:
            if isinstance(value, nodes.Const):
                # Static string part
                parts.append(str(value.value))
            elif isinstance(value, nodes.FormattedValue):
                # Variable part - try to infer first
                try:
                    inferred_list = list(value.value.infer())
                    if inferred_list and len(inferred_list) == 1:
                        inferred = inferred_list[0]
                        if isinstance(inferred, nodes.Const):
                            const_value = str(inferred.value)
                            if const_value and const_value.strip() and "Uninferable" not in const_value:
                                # Successfully inferred to a valid constant - use the value
                                parts.append(const_value)
                                continue

                    # Cannot infer to constant - check if it's a simple Name (variable)
                    if isinstance(value.value, nodes.Name):
                        # Simple variable reference - use ... to indicate unknown
                        parts.append("...")
                    elif isinstance(value.value, (nodes.Call, nodes.Attribute)):
                        # Complex expression - use ... to indicate omitted
                        parts.append("...")
                    else:
                        # Other cases - try to show the expression
                        var_name = value.value.as_string()
                        parts.append(f"{{ {var_name} }}")
                except Exception as e:
                    # Inference failed - use ... for unknown parts
                    logger.debug(f"URL variable inference failed: {e}")
                    parts.append("...")
        return "".join(parts)

    # Handle simple Name nodes (single variable)
    if isinstance(url_node, nodes.Name):
        # Try to infer the value first
        try:
            inferred_list = list(url_node.infer())
            if inferred_list and len(inferred_list) == 1:
                inferred = inferred_list[0]
                if isinstance(inferred, nodes.Const):
                    # Successfully inferred to a constant - return it
                    value_str = str(inferred.value)
                    if value_str and value_str.strip() and "Uninferable" not in value_str:
                        return value_str
        except Exception as e:
            logger.debug(f"URL variable inference failed: {e}")
        # Cannot infer - this is likely a function parameter or unresolvable variable
        # Return None to skip collecting this request
        return None

    # Handle string concatenation (BinOp with + operator)
    if isinstance(url_node, nodes.BinOp) and url_node.op == "+":
        # First try to infer the whole expression
        try:
            value, success = infer_value_with_fallback(url_node)
            if success and isinstance(value, str):
                return value
        except Exception as e:
            logger.debug(f"BinOp inference failed: {e}")

        # Recursively extract left and right parts
        left = _extract_url_from_node(url_node.left)
        right = _extract_url_from_node(url_node.right)

        # If either side is None (completely unresolvable), use ...
        if left is None:
            left = "..."
        if right is None:
            right = "..."

        # Concatenate the parts (may contain ... placeholders)
        return left + right

    # Handle Call nodes (e.g., str.format(), urljoin())
    if isinstance(url_node, nodes.Call):
        # Check if it's a .format() call on a string
        if isinstance(url_node.func, nodes.Attribute) and url_node.func.attrname == "format":
            # Try to extract the format string template
            format_result = _extract_format_string_template(url_node)
            if format_result:
                return format_result

        # For other calls, try inference
        value, success = infer_value_with_fallback(url_node)
        if success and isinstance(value, str) and value.strip():
            # Successfully inferred to a non-empty string
            return value
        # Cannot resolve - use ... to indicate complex expression
        return "..."

    # Fallback: try standard inference
    value, success = infer_value_with_fallback(url_node)
    if success and isinstance(value, str) and "Uninferable" not in value:
        return value

    # Last resort: mark as dynamic
    return None


def _find_assignment_value(url_node: nodes.Name) -> nodes.NodeNG | None:
    """Find the assignment value for a Name node.

    Args:
        url_node: Name node to find assignment for

    Returns:
        The value node from the assignment, or None if not found
    """
    try:
        for parent in url_node.node_ancestors():
            if hasattr(parent, "body"):
                for stmt in parent.body:
                    if isinstance(stmt, nodes.Assign):
                        for target in stmt.targets:
                            if isinstance(target, nodes.AssignName) and target.name == url_node.name:
                                return stmt.value
    except Exception as e:
        logger.debug(f"Failed to find assignment: {e}")
    return None


def _extract_url_from_name_node(url_node: nodes.Name) -> str | None:
    """Extract URL from a Name node by inferring its value.

    Args:
        url_node: Name node representing a variable

    Returns:
        Extracted URL, or None if completely unresolvable (e.g., function parameter)
    """
    try:
        inferred_list = list(url_node.infer())
        if inferred_list and len(inferred_list) == 1:
            inferred = inferred_list[0]

            # If it's a simple constant, check if it's valid
            if isinstance(inferred, nodes.Const):
                value_str = str(inferred.value)
                # Reject empty strings or strings containing "Uninferable"
                if value_str and value_str.strip() and "Uninferable" not in value_str:
                    return value_str
                # Invalid inference - try to get original assignment
                assignment_value = _find_assignment_value(url_node)
                if assignment_value:
                    url = _extract_url_from_node(assignment_value)
                    if url is not None:
                        return url
                # Couldn't find or process assignment - unresolvable
                return None

            # If it's a complex expression (JoinedStr, Call, etc.), process it
            if isinstance(inferred, (nodes.JoinedStr, nodes.Call, nodes.BinOp)):
                url = _extract_url_from_node(inferred)
                return url  # May be None if completely unresolvable
    except Exception as e:
        logger.debug(f"URL variable inference failed: {e}")
    # Cannot infer - completely unresolvable (likely function parameter)
    return None


def extract_url(node: nodes.Call) -> str:
    """Extract URL from HTTP request call.

    Args:
        node: astroid Call node

    Returns:
        Extracted URL or backtick-wrapped expression if unresolvable
    """
    # Get first positional argument or url= kwarg
    if node.args:
        url_node = node.args[0]
    else:
        for keyword in node.keywords or []:
            if keyword.arg == "url":
                url_node = keyword.value
                break
        else:
            return "`<unknown>`"

    # Special case: single variable URL (Name node)
    if isinstance(url_node, nodes.Name):
        url = _extract_url_from_name_node(url_node)
        # If completely unresolvable, return None to skip this request
        return url

    # Extract URL with variable placeholder support
    url = _extract_url_from_node(url_node)

    # Return url (may be None if completely unresolvable, causing request to be skipped)
    return url


def extract_method(node: nodes.Call) -> str:
    """Extract HTTP method from request call.

    Args:
        node: astroid Call node

    Returns:
        HTTP method (GET, POST, etc.)
    """
    # Extract method from function name (e.g., requests.get -> GET)
    if isinstance(node.func, nodes.Attribute):
        method_name = node.func.attrname
        return method_name.upper()
    return "GET"  # Default


def extract_params(node: nodes.Call) -> dict:
    """Extract query parameters from request call.

    Args:
        node: astroid Call node

    Returns:
        Dictionary of query parameters
    """
    for keyword in node.keywords or []:
        if keyword.arg == "params":
            value, inferred = infer_value_with_fallback(keyword.value)
            if inferred and isinstance(value, dict):
                return value
    return {}


def extract_headers(node: nodes.Call) -> dict:
    """Extract HTTP headers from request call.

    Args:
        node: astroid Call node

    Returns:
        Dictionary of headers
    """
    for keyword in node.keywords or []:
        if keyword.arg == "headers":
            value, inferred = infer_value_with_fallback(keyword.value)
            if inferred and isinstance(value, dict):
                return value
    return {}


def extract_json_body(node: nodes.Call) -> dict | None:
    """Extract JSON body from request call.

    Args:
        node: astroid Call node

    Returns:
        JSON body dict or None
    """
    for keyword in node.keywords or []:
        if keyword.arg == "json":
            value, inferred = infer_value_with_fallback(keyword.value)
            if inferred and isinstance(value, dict):
                return value
    return None


def extract_data(node: nodes.Call) -> dict | None:
    """Extract form data from request call.

    Args:
        node: astroid Call node

    Returns:
        Form data dict or None
    """
    for keyword in node.keywords or []:
        if keyword.arg == "data":
            value, inferred = infer_value_with_fallback(keyword.value)
            if inferred and isinstance(value, dict):
                return value
    return None


def extract_timeout(node: nodes.Call) -> int | float | None:
    """Extract timeout value from request call.

    Args:
        node: astroid Call node

    Returns:
        Timeout value or None
    """
    for keyword in node.keywords or []:
        if keyword.arg == "timeout":
            value, inferred = infer_value_with_fallback(keyword.value)
            if inferred and isinstance(value, (int, float)):
                return value
    return None


def is_session_based(node: nodes.Call) -> bool:
    """Check if this is a session-based request call.

    Args:
        node: astroid Call node

    Returns:
        True if session-based, False otherwise
    """
    if not isinstance(node.func, nodes.Attribute):
        return False

    # Check if the base is a session/client object
    if isinstance(node.func.expr, nodes.Name):
        base_name = node.func.expr.name

        # Common session variable names
        if base_name in ["session", "s", "client", "c"]:
            try:
                for inferred in node.func.expr.infer():
                    if hasattr(inferred, "qname"):
                        qname = inferred.qname()
                        # Check if it's a Session or Client type
                        if any(x in qname for x in ["Session", "Client", "ClientSession", "PoolManager"]):
                            return True
            except Exception:
                # If we can't infer, assume session based on name
                return base_name in ["session", "client"]

    return False


def is_async_call(node: nodes.Call) -> bool:
    """Check if this call is inside an async function.

    Args:
        node: astroid Call node

    Returns:
        True if async, False otherwise
    """
    # Traverse up to find enclosing function
    parent = node.parent
    while parent:
        # Check if it's an AsyncFunctionDef (async def)
        if isinstance(parent, nodes.AsyncFunctionDef):
            return True
        # Regular FunctionDef is not async
        if isinstance(parent, nodes.FunctionDef):
            return False
        parent = parent.parent
    return False


def parse_request(node: nodes.Call, file_path: str, library: str) -> HttpRequest:
    """Parse a complete HTTP request from a Call node.

    Args:
        node: astroid Call node
        file_path: Relative file path
        library: Detected library name

    Returns:
        HttpRequest object
    """
    location = f"{file_path}:{node.lineno}"
    statement = node.as_string()

    url = extract_url(node)
    method = extract_method(node)
    params = extract_params(node)
    headers = extract_headers(node)
    json_body = extract_json_body(node)
    data = extract_data(node)
    timeout = extract_timeout(node)
    session_based = is_session_based(node)
    is_async = is_async_call(node)

    return HttpRequest(
        location=location,
        statement=statement,
        library=library,
        url=url,
        method=method,
        params=params,
        headers=headers,
        json_body=json_body,
        data=data,
        timeout=timeout,
        session_based=session_based,
        is_async=is_async,
    )
