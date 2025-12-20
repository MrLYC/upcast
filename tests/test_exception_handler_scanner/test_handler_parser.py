"""Tests for exception handler parser."""

from astroid import nodes, parse

from upcast.exception_handler_scanner.handler_parser import (
    count_control_flow,
    count_logging_calls,
    extract_exception_types,
    parse_try_block,
)


def test_extract_exception_types_single():
    """Test extraction of single exception type."""
    code = """
try:
    pass
except ValueError:
    pass
"""
    tree = parse(code)
    try_node = next(iter(tree.nodes_of_class(nodes.Try)))
    handler = try_node.handlers[0]

    types = extract_exception_types(handler)
    assert types == ["ValueError"]


def test_extract_exception_types_multiple():
    """Test extraction of multiple exception types."""
    code = """
try:
    pass
except (ValueError, KeyError):
    pass
"""
    tree = parse(code)
    try_node = next(iter(tree.nodes_of_class(nodes.Try)))
    handler = try_node.handlers[0]

    types = extract_exception_types(handler)
    assert set(types) == {"ValueError", "KeyError"}


def test_extract_exception_types_bare():
    """Test bare except clause."""
    code = """
try:
    pass
except:
    pass
"""
    tree = parse(code)
    try_node = next(iter(tree.nodes_of_class(nodes.Try)))
    handler = try_node.handlers[0]

    types = extract_exception_types(handler)
    assert types == []


def test_count_logging_calls_error():
    """Test counting error level logging."""
    code = """
import logging
logger = logging.getLogger(__name__)

try:
    x = 1 / 0
except ZeroDivisionError:
    logger.error("Error message")
"""
    tree = parse(code)
    try_node = next(iter(tree.nodes_of_class(nodes.Try)))
    handler = try_node.handlers[0]

    counts = count_logging_calls(handler.body)
    assert counts["error"] == 1
    assert counts["debug"] == 0
    assert counts["info"] == 0


def test_count_logging_calls_multiple_levels():
    """Test counting multiple log levels."""
    code = """
import logging
logger = logging.getLogger(__name__)

try:
    x = 1 / 0
except ZeroDivisionError:
    logger.debug("Debug")
    logger.info("Info")
    logger.error("Error")
"""
    tree = parse(code)
    try_node = next(iter(tree.nodes_of_class(nodes.Try)))
    handler = try_node.handlers[0]

    counts = count_logging_calls(handler.body)
    assert counts["debug"] == 1
    assert counts["info"] == 1
    assert counts["error"] == 1
    assert counts["warning"] == 0


def test_count_control_flow_pass():
    """Test counting pass statements."""
    code = """
try:
    x = 1 / 0
except ZeroDivisionError:
    pass
"""
    tree = parse(code)
    try_node = next(iter(tree.nodes_of_class(nodes.Try)))
    handler = try_node.handlers[0]

    counts = count_control_flow(handler.body)
    assert counts["pass"] == 1
    assert counts["return"] == 0


def test_count_control_flow_return():
    """Test counting return statements."""
    code = """
try:
    x = 1 / 0
except ZeroDivisionError:
    return None
"""
    tree = parse(code)
    try_node = next(iter(tree.nodes_of_class(nodes.Try)))
    handler = try_node.handlers[0]

    counts = count_control_flow(handler.body)
    assert counts["return"] == 1
    assert counts["pass"] == 0


def test_count_control_flow_raise():
    """Test counting raise statements."""
    code = """
try:
    x = 1 / 0
except ZeroDivisionError:
    raise ValueError("Error")
"""
    tree = parse(code)
    try_node = next(iter(tree.nodes_of_class(nodes.Try)))
    handler = try_node.handlers[0]

    counts = count_control_flow(handler.body)
    assert counts["raise"] == 1


def test_parse_try_block_basic():
    """Test parsing basic try/except block."""
    code = """
try:
    x = 1 / 0
except ZeroDivisionError:
    pass
"""
    tree = parse(code)
    try_node = next(iter(tree.nodes_of_class(nodes.Try)))

    handler = parse_try_block(try_node, "test.py")

    assert handler.file == "test.py"
    assert handler.try_lines > 0
    assert len(handler.except_clauses) == 1
    assert handler.else_clause is None
    assert handler.finally_clause is None


def test_parse_try_block_with_else():
    """Test parsing try/except/else block."""
    code = """
try:
    x = 1 / 2
except ZeroDivisionError:
    pass
else:
    print("Success")
"""
    tree = parse(code)
    try_node = next(iter(tree.nodes_of_class(nodes.Try)))

    handler = parse_try_block(try_node, "test.py")

    assert handler.else_clause is not None
    assert handler.else_clause.lines > 0


def test_parse_try_block_with_finally():
    """Test parsing try/except/finally block."""
    code = """
try:
    x = 1 / 0
except ZeroDivisionError:
    pass
finally:
    print("Cleanup")
"""
    tree = parse(code)
    try_node = next(iter(tree.nodes_of_class(nodes.Try)))

    handler = parse_try_block(try_node, "test.py")

    assert handler.finally_clause is not None
    assert handler.finally_clause.lines > 0


def test_parse_try_block_complete():
    """Test parsing complete try/except/else/finally block."""
    code = """
try:
    x = 1 / 2
except ZeroDivisionError:
    pass
else:
    print("Success")
finally:
    print("Cleanup")
"""
    tree = parse(code)
    try_node = next(iter(tree.nodes_of_class(nodes.Try)))

    handler = parse_try_block(try_node, "test.py")

    assert len(handler.except_clauses) == 1
    assert handler.else_clause is not None
    assert handler.finally_clause is not None


def test_parse_try_block_multiple_except():
    """Test parsing try block with multiple except clauses."""
    code = """
import logging
logger = logging.getLogger(__name__)

try:
    data = {}
    value = data["key"]
except KeyError:
    logger.error("Key error")
except ValueError:
    logger.warning("Value error")
except Exception:
    logger.exception("Unexpected")
    raise
"""
    tree = parse(code)
    try_node = next(iter(tree.nodes_of_class(nodes.Try)))

    handler = parse_try_block(try_node, "test.py")

    assert len(handler.except_clauses) == 3
    assert handler.except_clauses[0].exception_types == ["KeyError"]
    assert handler.except_clauses[1].exception_types == ["ValueError"]
    assert handler.except_clauses[2].exception_types == ["Exception"]

    # Check logging counts
    assert handler.except_clauses[0].log_error_count == 1
    assert handler.except_clauses[1].log_warning_count == 1
    assert handler.except_clauses[2].log_exception_count == 1

    # Check control flow
    assert handler.except_clauses[2].raise_count == 1
