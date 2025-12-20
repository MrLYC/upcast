"""Code extraction and analysis utilities."""

import io
import tokenize

from astroid import nodes


def extract_function_code(node: nodes.FunctionDef) -> str:
    """Extract complete function source code using astroid.

    Args:
        node: Astroid FunctionDef or AsyncFunctionDef node

    Returns:
        Complete function source code including decorators

    Examples:
        >>> func_node = ...  # astroid FunctionDef
        >>> code = extract_function_code(func_node)
        >>> print(code)
        @decorator
        def my_function(x):
            return x + 1
    """
    try:
        return node.as_string()
    except Exception:
        return ""


def count_comment_lines(source_code: str) -> int:
    """Count comment lines using Python's tokenize module.

    This is more accurate than string matching as it properly handles:
    - Comments inside strings (not counted)
    - Multi-line strings vs actual comments
    - Different comment styles

    Args:
        source_code: Function source code

    Returns:
        Number of comment lines (lines with # comments)

    Examples:
        >>> code = '''
        ... def foo():
        ...     # This is a comment
        ...     x = "# Not a comment"  # This is a comment
        ...     return x
        ... '''
        >>> count_comment_lines(code)
        2
    """
    if not source_code:
        return 0

    comment_count = 0
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source_code).readline)
        comment_lines: set[int] = set()

        for token in tokens:
            if token.type == tokenize.COMMENT:
                comment_lines.add(token.start[0])

        comment_count = len(comment_lines)
    except tokenize.TokenError:
        # Fallback to 0 if tokenization fails
        pass

    return comment_count


def get_code_lines(node: nodes.FunctionDef) -> int:
    """Calculate total function code lines.

    Args:
        node: Astroid FunctionDef or AsyncFunctionDef node

    Returns:
        Total lines including code, comments, and blank lines

    Examples:
        >>> func_node = ...  # function from line 10 to 25
        >>> get_code_lines(func_node)
        16
    """
    if not hasattr(node, "lineno") or not hasattr(node, "end_lineno"):
        return 0

    end_line = node.end_lineno or node.lineno
    return end_line - node.lineno + 1
