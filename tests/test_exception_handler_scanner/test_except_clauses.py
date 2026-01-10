"""Tests for except clause detection and parsing."""

import pytest
from pathlib import Path

from upcast.scanners.exceptions import ExceptionHandlerScanner


class TestExceptClauseDetection:
    """Test detection of various except clause patterns."""

    def test_single_exception_type(self, tmp_path, scanner):
        """Test detection of single exception type."""
        code = """
try:
    operation()
except ValueError:
    handle()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        clause = handler.except_clauses[0]
        assert clause.exception_types == ["ValueError"]

    def test_multiple_exception_types_tuple(self, tmp_path, scanner):
        """Test detection of multiple exception types in tuple."""
        code = """
try:
    operation()
except (ValueError, KeyError, TypeError):
    handle()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        clause = handler.except_clauses[0]
        assert len(clause.exception_types) == 3
        assert "ValueError" in clause.exception_types
        assert "KeyError" in clause.exception_types
        assert "TypeError" in clause.exception_types

    def test_builtin_exceptions(self, tmp_path, scanner):
        """Test detection of various builtin exceptions."""
        code = """
try:
    operation()
except IOError:
    pass
except RuntimeError:
    pass
except AttributeError:
    pass
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        assert len(handler.except_clauses) == 3
        assert "IOError" in handler.except_clauses[0].exception_types
        assert "RuntimeError" in handler.except_clauses[1].exception_types
        assert "AttributeError" in handler.except_clauses[2].exception_types

    def test_custom_exception_class(self, tmp_path, scanner):
        """Test detection of custom exception classes."""
        code = """
class CustomError(Exception):
    pass

try:
    operation()
except CustomError:
    handle()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        assert "CustomError" in handler.except_clauses[0].exception_types

    def test_exception_with_as_clause(self, tmp_path, scanner):
        """Test except clause with 'as' variable binding."""
        code = """
try:
    operation()
except ValueError as e:
    handle(e)
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        assert "ValueError" in handler.except_clauses[0].exception_types

    def test_module_qualified_exception(self, tmp_path, scanner):
        """Test detection of module-qualified exceptions."""
        code = """
import requests

try:
    requests.get('http://example.com')
except requests.exceptions.RequestException:
    handle()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        exception_types = handler.except_clauses[0].exception_types
        # Should capture the full qualified name
        assert len(exception_types) == 1
        assert "requests.exceptions.RequestException" in exception_types[0]

    def test_except_clause_line_count(self, tmp_path, scanner):
        """Test that except clause line count is correct."""
        code = """
try:
    operation()
except ValueError:
    line1()
    line2()
    line3()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        clause = handler.except_clauses[0]
        assert clause.lines >= 3  # At least 3 lines of code

    def test_sequential_try_blocks(self, tmp_path, scanner):
        """Test multiple sequential try blocks."""
        code = """
try:
    operation1()
except ValueError:
    handle1()

try:
    operation2()
except KeyError:
    handle2()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert len(output.results) == 2
        assert "ValueError" in output.results[0].except_clauses[0].exception_types
        assert "KeyError" in output.results[1].except_clauses[0].exception_types

    def test_exception_hierarchy(self, tmp_path, scanner):
        """Test detection of exception hierarchy (base before specific)."""
        code = """
try:
    operation()
except Exception:
    handle_generic()
except ValueError:
    handle_specific()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        assert len(handler.except_clauses) == 2
        assert "Exception" in handler.except_clauses[0].exception_types
        assert "ValueError" in handler.except_clauses[1].exception_types

    def test_try_lines_count(self, tmp_path, scanner):
        """Test that try block line count is correct."""
        code = """
try:
    line1()
    line2()
    line3()
    line4()
except ValueError:
    handle()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        assert handler.try_lines >= 4  # At least 4 lines

    def test_empty_except_body(self, tmp_path, scanner):
        """Test except clause with pass statement."""
        code = """
try:
    operation()
except ValueError:
    pass
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        clause = handler.except_clauses[0]
        assert clause.pass_count == 1
