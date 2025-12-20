"""Parser for exception handler patterns in Python code."""

from dataclasses import dataclass, field

from astroid import nodes


@dataclass
class BlockInfo:
    """Information about an else or finally block."""

    line: int
    lines: int


@dataclass
class ExceptionClause:
    """Information about a single except clause."""

    line: int
    exception_types: list[str]
    lines: int
    # Logging counts by level
    log_debug_count: int = 0
    log_info_count: int = 0
    log_warning_count: int = 0
    log_error_count: int = 0
    log_exception_count: int = 0
    log_critical_count: int = 0
    # Control flow counts
    pass_count: int = 0
    return_count: int = 0
    break_count: int = 0
    continue_count: int = 0
    raise_count: int = 0


@dataclass
class ExceptionHandler:
    """Information about a complete try/except block."""

    location: str
    file: str
    start_line: int
    end_line: int
    try_lines: int
    except_clauses: list[ExceptionClause] = field(default_factory=list)
    else_clause: BlockInfo | None = None
    finally_clause: BlockInfo | None = None


def extract_exception_types(handler: nodes.ExceptHandler) -> list[str]:
    """Extract exception type names from an except handler.

    Args:
        handler: The except handler node

    Returns:
        List of exception type names (empty list for bare except)
    """
    if handler.type is None:
        # Bare except: except:
        return []

    exception_types = []

    if isinstance(handler.type, nodes.Tuple):
        # Multiple exceptions: except (ValueError, KeyError):
        for elt in handler.type.elts:
            if isinstance(elt, (nodes.Name, nodes.Attribute)):
                exception_types.append(elt.as_string())
    elif isinstance(handler.type, (nodes.Name, nodes.Attribute)):
        # Single exception: except ValueError:
        exception_types.append(handler.type.as_string())

    return exception_types


def count_logging_calls(body: list[nodes.NodeNG]) -> dict[str, int]:
    """Count logging calls by level in a code block.

    Args:
        body: List of AST nodes to analyze

    Returns:
        Dictionary with counts for each log level
    """
    counts = {
        "debug": 0,
        "info": 0,
        "warning": 0,
        "error": 0,
        "exception": 0,
        "critical": 0,
    }

    for node in body:
        for subnode in node.nodes_of_class(nodes.Call):
            if isinstance(subnode.func, nodes.Attribute):
                method_name = subnode.func.attrname
                if method_name in counts:
                    # Check if it's likely a logger call
                    # Accept common logger variable names
                    if isinstance(subnode.func.expr, nodes.Name):
                        var_name = subnode.func.expr.name
                        if var_name.lower() in {"logger", "log", "_logger"} or var_name in {
                            "LOG",
                            "LOGGER",
                        }:
                            counts[method_name] += 1
                    elif isinstance(subnode.func.expr, nodes.Attribute):
                        # Handle self.logger.error() or cls.logger.error()
                        if subnode.func.expr.attrname in {"logger", "log"}:
                            counts[method_name] += 1

    return counts


def _count_node_type(node: nodes.NodeNG) -> dict[str, int]:
    """Count the type of a single node.

    Args:
        node: AST node to count

    Returns:
        Dictionary with count for the node type
    """
    counts = {
        "pass": 0,
        "return": 0,
        "break": 0,
        "continue": 0,
        "raise": 0,
    }

    if isinstance(node, nodes.Pass):
        counts["pass"] = 1
    elif isinstance(node, nodes.Return):
        counts["return"] = 1
    elif isinstance(node, nodes.Break):
        counts["break"] = 1
    elif isinstance(node, nodes.Continue):
        counts["continue"] = 1
    elif isinstance(node, nodes.Raise):
        counts["raise"] = 1

    return counts


def count_control_flow(body: list[nodes.NodeNG]) -> dict[str, int]:
    """Count control flow statements in a code block.

    Args:
        body: List of AST nodes to analyze

    Returns:
        Dictionary with counts for each control flow type
    """
    counts = {
        "pass": 0,
        "return": 0,
        "break": 0,
        "continue": 0,
        "raise": 0,
    }

    for node in body:
        # Count at top level of except block
        node_counts = _count_node_type(node)
        for key, value in node_counts.items():
            counts[key] += value

        # Also check nested structures (if, for, while, etc.)
        for subnode in node.nodes_of_class((nodes.Pass, nodes.Return, nodes.Break, nodes.Continue, nodes.Raise)):
            if subnode is node:
                continue  # Skip the node we already counted
            subnode_counts = _count_node_type(subnode)
            for key, value in subnode_counts.items():
                counts[key] += value

    return counts


def parse_except_clause(handler: nodes.ExceptHandler) -> ExceptionClause:
    """Parse an except clause into an ExceptionClause object.

    Args:
        handler: The except handler node

    Returns:
        ExceptionClause with extracted information
    """
    exception_types = extract_exception_types(handler)

    # Count lines in except block
    lines = handler.body[-1].lineno - handler.lineno + 1 if handler.body else 1

    # Count logging calls
    log_counts = count_logging_calls(handler.body)

    # Count control flow statements
    flow_counts = count_control_flow(handler.body)

    return ExceptionClause(
        line=handler.lineno,
        exception_types=exception_types,
        lines=lines,
        log_debug_count=log_counts["debug"],
        log_info_count=log_counts["info"],
        log_warning_count=log_counts["warning"],
        log_error_count=log_counts["error"],
        log_exception_count=log_counts["exception"],
        log_critical_count=log_counts["critical"],
        pass_count=flow_counts["pass"],
        return_count=flow_counts["return"],
        break_count=flow_counts["break"],
        continue_count=flow_counts["continue"],
        raise_count=flow_counts["raise"],
    )


def parse_else_clause(node: nodes.Try) -> BlockInfo | None:
    """Parse the else clause of a try block if present.

    Args:
        node: The try block node

    Returns:
        BlockInfo if else clause exists, None otherwise
    """
    if not node.orelse:
        return None

    line = node.orelse[0].lineno
    lines = node.orelse[-1].lineno - line + 1

    return BlockInfo(line=line, lines=lines)


def parse_finally_clause(node: nodes.Try) -> BlockInfo | None:
    """Parse the finally clause of a try block if present.

    Args:
        node: The try block node

    Returns:
        BlockInfo if finally clause exists, None otherwise
    """
    if not node.finalbody:
        return None

    line = node.finalbody[0].lineno
    lines = node.finalbody[-1].lineno - line + 1

    return BlockInfo(line=line, lines=lines)


def parse_try_block(node: nodes.Try, file_path: str) -> ExceptionHandler:
    """Parse a try block into an ExceptionHandler object.

    Args:
        node: The try block node
        file_path: Path to the file containing this try block

    Returns:
        ExceptionHandler with all extracted information
    """
    # Calculate try block line count
    try_lines = node.body[-1].lineno - node.lineno + 1 if node.body else 1

    # Parse all except clauses
    except_clauses = [parse_except_clause(handler) for handler in node.handlers]

    # Determine end line (last line of finally, else, or last except)
    if node.finalbody:
        end_line = node.finalbody[-1].lineno
    elif node.orelse:
        end_line = node.orelse[-1].lineno
    elif node.handlers:
        end_line = node.handlers[-1].body[-1].lineno if node.handlers[-1].body else node.handlers[-1].lineno
    else:
        end_line = node.body[-1].lineno if node.body else node.lineno

    # Parse else and finally clauses
    else_clause = parse_else_clause(node)
    finally_clause = parse_finally_clause(node)

    location = f"{file_path}:{node.lineno}-{end_line}"

    return ExceptionHandler(
        location=location,
        file=file_path,
        start_line=node.lineno,
        end_line=end_line,
        try_lines=try_lines,
        except_clauses=except_clauses,
        else_clause=else_clause,
        finally_clause=finally_clause,
    )
