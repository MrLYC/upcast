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


def extract_function_signature(node: nodes.FunctionDef) -> str | None:  # noqa: C901
    """Extract complete function signature with type hints and defaults.

    Args:
        node: Astroid FunctionDef or AsyncFunctionDef node

    Returns:
        Function signature string or None if extraction fails

    Examples:
        >>> func_node = ...  # def foo(x: int, y: str = "default") -> bool:
        >>> extract_function_signature(func_node)
        'def foo(x: int, y: str = "default") -> bool:'
    """
    try:
        parts = []

        # Handle async functions
        if isinstance(node, nodes.AsyncFunctionDef):
            parts.append("async")

        parts.append("def")
        parts.append(node.name)
        parts.append("(")

        # Build parameter list
        params = []
        if node.args:
            args_list = node.args.args or []
            defaults = node.args.defaults or []
            annotations = node.args.annotations or []

            # Calculate where defaults start
            num_without_defaults = len(args_list) - len(defaults)

            for i, arg in enumerate(args_list):
                param_str = arg.name

                # Add type annotation if available
                if i < len(annotations) and annotations[i]:
                    param_str += f": {annotations[i].as_string()}"

                # Add default value if available
                if i >= num_without_defaults:
                    default_idx = i - num_without_defaults
                    if default_idx < len(defaults):
                        param_str += f" = {defaults[default_idx].as_string()}"

                params.append(param_str)

            # *args
            if node.args.vararg:
                vararg_str = f"*{node.args.vararg}"
                if node.args.varargannotation:
                    vararg_str += f": {node.args.varargannotation.as_string()}"
                params.append(vararg_str)

            # **kwargs
            if node.args.kwarg:
                kwarg_str = f"**{node.args.kwarg}"
                if node.args.kwargannotation:
                    kwarg_str += f": {node.args.kwargannotation.as_string()}"
                params.append(kwarg_str)

        parts.append(", ".join(params))
        parts.append(")")

        # Return type annotation
        if node.returns:
            parts.append("->")
            parts.append(node.returns.as_string())

        parts.append(":")

        return " ".join(parts)
    except Exception:
        return None


def extract_description(node: nodes.FunctionDef | nodes.ClassDef) -> str | None:
    """Extract first line of docstring as description.

    Args:
        node: Astroid FunctionDef, AsyncFunctionDef, or ClassDef node

    Returns:
        First line of docstring or None if no docstring

    Examples:
        >>> func_node = ...  # def foo():
        ...                  #     '''First line.
        ...                  #     Second line.'''
        >>> extract_description(func_node)
        'First line.'
    """
    try:
        doc = node.doc_node
        if not doc:
            return None

        docstring = doc.value
        if not docstring:
            return None

        # Extract first line
        first_line = docstring.split("\n")[0].strip()
    except Exception:
        return None
    else:
        return first_line if first_line else None
