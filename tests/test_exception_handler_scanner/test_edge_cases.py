"""Tests for edge cases and error handling."""

import pytest
from pathlib import Path

from upcast.scanners.exceptions import ExceptionHandlerScanner


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_deeply_nested_try_blocks(self, tmp_path, scanner):
        """Test deeply nested try blocks."""
        code = """
try:
    try:
        try:
            operation()
        except ValueError:
            handle_inner()
    except KeyError:
        handle_middle()
except Exception:
    handle_outer()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # Should detect all 3 try blocks
        assert output.summary.total_handlers == 3

    def test_try_with_only_finally(self, tmp_path, scanner):
        """Test try block with only finally (no except)."""
        code = """
try:
    operation()
finally:
    cleanup()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_handlers == 1
        handler = output.results[0]
        assert len(handler.exception_blocks) == 0
        assert handler.finally_lineno is not None

    def test_try_in_lambda(self, tmp_path, scanner):
        """Test try block in lambda expression."""
        code = """
# This is not valid Python syntax, but test scanner doesn't crash
handler = lambda: operation() if True else None
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # Should not crash, just return no handlers
        assert output.summary.total_handlers == 0

    def test_try_in_comprehension(self, tmp_path, scanner):
        """Test try blocks are not in comprehensions (Python limitation)."""
        code = """
# Try-except is not allowed in comprehensions
results = [item for item in items]
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_handlers == 0

    def test_except_with_complex_expression(self, tmp_path, scanner):
        """Test except clause with complex exception expression."""
        code = """
try:
    operation()
except getattr(__builtins__, 'ValueError'):
    handle()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # Should handle complex expressions gracefully
        assert output.summary.total_handlers == 1

    def test_empty_try_block(self, tmp_path, scanner):
        """Test try block with pass statement."""
        code = """
try:
    pass
except Exception:
    handle()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_handlers == 1
        handler = output.results[0]
        assert handler.try_lines >= 0

    def test_multiline_exception_tuple(self, tmp_path, scanner):
        """Test except clause with multiline exception tuple."""
        code = """
try:
    operation()
except (
    ValueError,
    KeyError,
    TypeError,
    AttributeError
):
    handle()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        clause = handler.exception_blocks[0]
        assert len(clause.exceptions) == 4

    def test_invalid_syntax_file(self, tmp_path, scanner):
        """Test handling of file with invalid Python syntax."""
        code = """
try:
    operation()
except ValueError
    handle()  # Missing colon
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # Should handle parse errors gracefully
        assert output.summary.total_handlers == 0

    def test_try_with_all_clauses(self, tmp_path, scanner):
        """Test try block with all possible clauses."""
        code = """
try:
    operation()
except ValueError:
    handle_value()
except KeyError:
    handle_key()
else:
    success()
finally:
    cleanup()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        assert len(handler.exception_blocks) == 2
        assert handler.else_lineno is not None
        assert handler.finally_lineno is not None

    def test_exception_in_async_function(self, tmp_path, scanner):
        """Test exception handlers in async functions."""
        code = """
async def process():
    try:
        await operation()
    except ValueError:
        handle()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_handlers == 1

    def test_exception_with_walrus_operator(self, tmp_path, scanner):
        """Test exception handler with walrus operator."""
        code = """
try:
    operation()
except ValueError as e:
    if msg := str(e):
        logger.error(msg)
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_handlers == 1
