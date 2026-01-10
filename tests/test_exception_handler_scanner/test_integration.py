"""Integration tests for exception handler scanner."""

import pytest
from pathlib import Path

from upcast.scanners.exceptions import ExceptionHandlerScanner
from upcast.models.exceptions import ExceptionHandlerOutput


class TestScannerInstantiation:
    """Test scanner instantiation and basic functionality."""

    def test_scanner_instantiation(self, scanner):
        """Test that scanner can be instantiated."""
        assert scanner is not None
        assert isinstance(scanner, ExceptionHandlerScanner)

    def test_scanner_verbose_mode(self):
        """Test that scanner can be instantiated with verbose mode."""
        scanner = ExceptionHandlerScanner(verbose=True)
        assert scanner.verbose is True

    def test_scanner_custom_patterns(self):
        """Test scanner with custom include/exclude patterns."""
        scanner = ExceptionHandlerScanner(
            include_patterns=["**/handlers.py"],
            exclude_patterns=["**/tests/**"],
        )
        assert scanner.include_patterns == ["**/handlers.py"]
        assert scanner.exclude_patterns == ["**/tests/**"]


class TestBasicScanning:
    """Test basic scanning functionality."""

    def test_scan_empty_file(self, tmp_path, scanner):
        """Test scanning an empty file."""
        file_path = tmp_path / "empty.py"
        file_path.write_text("")

        output = scanner.scan(file_path)

        assert isinstance(output, ExceptionHandlerOutput)
        assert output.summary.total_handlers == 0
        assert output.summary.total_except_clauses == 0
        assert len(output.results) == 0

    def test_scan_file_without_exceptions(self, tmp_path, scanner):
        """Test scanning a file without exception handlers."""
        code = """
def pure_function():
    x = 1 + 2
    return x * 3

class PureClass:
    def compute(self):
        return 42
"""
        file_path = tmp_path / "pure.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_handlers == 0
        assert len(output.results) == 0

    def test_scan_simple_try_except(self, tmp_path, scanner, simple_try_except):
        """Test scanning a simple try-except block."""
        file_path = tmp_path / "test.py"
        file_path.write_text(simple_try_except)

        output = scanner.scan(file_path)

        assert output.summary.total_handlers == 1
        assert output.summary.total_except_clauses == 1
        assert len(output.results) == 1

        handler = output.results[0]
        assert handler.lineno is not None
        assert len(handler.except_clauses) == 1
        assert "ValueError" in handler.except_clauses[0].exception_types

    def test_scan_multiple_except_clauses(self, tmp_path, scanner, multiple_except_clauses):
        """Test scanning try block with multiple except clauses."""
        file_path = tmp_path / "test.py"
        file_path.write_text(multiple_except_clauses)

        output = scanner.scan(file_path)

        assert output.summary.total_handlers == 1
        assert output.summary.total_except_clauses == 3

        handler = output.results[0]
        assert len(handler.except_clauses) == 3
        assert "ValueError" in handler.except_clauses[0].exception_types
        assert "KeyError" in handler.except_clauses[1].exception_types
        assert "Exception" in handler.except_clauses[2].exception_types

    def test_scan_try_except_else(self, tmp_path, scanner, try_except_else):
        """Test scanning try-except with else clause."""
        file_path = tmp_path / "test.py"
        file_path.write_text(try_except_else)

        output = scanner.scan(file_path)

        assert output.summary.total_handlers == 1
        handler = output.results[0]
        assert handler.else_clause is not None
        assert handler.else_clause.line is not None
        assert handler.else_clause.lines > 0

    def test_scan_try_except_finally(self, tmp_path, scanner, try_except_finally):
        """Test scanning try-except with finally clause."""
        file_path = tmp_path / "test.py"
        file_path.write_text(try_except_finally)

        output = scanner.scan(file_path)

        assert output.summary.total_handlers == 1
        handler = output.results[0]
        assert handler.finally_clause is not None
        assert handler.finally_clause.line is not None
        assert handler.finally_clause.lines > 0

    def test_scan_try_except_else_finally(self, tmp_path, scanner, try_except_else_finally):
        """Test scanning try-except with both else and finally."""
        file_path = tmp_path / "test.py"
        file_path.write_text(try_except_else_finally)

        output = scanner.scan(file_path)

        assert output.summary.total_handlers == 1
        handler = output.results[0]
        assert handler.else_clause is not None
        assert handler.finally_clause is not None

    def test_scan_bare_except(self, tmp_path, scanner, bare_except):
        """Test scanning bare except clause."""
        file_path = tmp_path / "test.py"
        file_path.write_text(bare_except)

        output = scanner.scan(file_path)

        assert output.summary.total_handlers == 1
        handler = output.results[0]
        # Bare except has empty exception_types list
        assert handler.except_clauses[0].exception_types == []

    def test_scan_multiple_exception_types(self, tmp_path, scanner, multiple_exception_types):
        """Test scanning except clause with multiple exception types."""
        file_path = tmp_path / "test.py"
        file_path.write_text(multiple_exception_types)

        output = scanner.scan(file_path)

        assert output.summary.total_handlers == 1
        handler = output.results[0]
        exception_types = handler.except_clauses[0].exception_types
        assert len(exception_types) == 3
        assert "ValueError" in exception_types
        assert "KeyError" in exception_types
        assert "TypeError" in exception_types

    def test_scan_directory(self, tmp_path, scanner):
        """Test scanning a directory with multiple files."""
        # Create multiple files
        file1 = tmp_path / "file1.py"
        file1.write_text("""
try:
    operation1()
except ValueError:
    handle1()
""")

        file2 = tmp_path / "file2.py"
        file2.write_text("""
try:
    operation2()
except KeyError:
    handle2()
except Exception:
    handle_all()
""")

        output = scanner.scan(tmp_path)

        assert output.summary.total_handlers == 2
        assert output.summary.total_except_clauses == 3
        assert output.summary.files_scanned == 2

    def test_scan_nested_try_blocks(self, tmp_path, scanner):
        """Test scanning nested try blocks."""
        code = """
try:
    outer_operation()
    try:
        inner_operation()
    except ValueError:
        handle_inner()
except KeyError:
    handle_outer()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # Should detect both outer and inner try blocks
        assert output.summary.total_handlers == 2
        assert output.summary.total_except_clauses == 2

    def test_scan_try_in_function(self, tmp_path, scanner):
        """Test scanning try blocks inside functions."""
        code = """
def process_data():
    try:
        risky_operation()
    except ValueError:
        handle_error()
    except KeyError:
        handle_key_error()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_handlers == 1
        assert output.summary.total_except_clauses == 2

    def test_scan_try_in_class(self, tmp_path, scanner):
        """Test scanning try blocks inside class methods."""
        code = """
class DataProcessor:
    def process(self):
        try:
            self.risky_method()
        except ValueError:
            self.handle_error()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_handlers == 1

    def test_scan_summary_statistics(self, tmp_path, scanner):
        """Test that summary statistics are calculated correctly."""
        code = """
try:
    operation1()
except ValueError:
    handle1()

try:
    operation2()
except KeyError:
    handle2()
except TypeError:
    handle3()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_handlers == 2
        assert output.summary.total_except_clauses == 3
        assert output.summary.files_scanned == 1
        assert output.summary.scan_duration_ms >= 0

    def test_scan_duration_measurement(self, tmp_path, scanner):
        """Test that scan duration is measured."""
        file_path = tmp_path / "test.py"
        file_path.write_text("""
try:
    operation()
except Exception:
    pass
""")

        output = scanner.scan(file_path)

        assert output.summary.scan_duration_ms >= 0
        assert isinstance(output.summary.scan_duration_ms, int)

    def test_scan_file_path_tracking(self, tmp_path, scanner):
        """Test that file paths are correctly tracked."""
        file_path = tmp_path / "test.py"
        file_path.write_text("""
try:
    operation()
except Exception:
    pass
""")

        output = scanner.scan(file_path)

        assert len(output.results) == 1
        handler = output.results[0]
        assert handler.file is not None
        assert "test.py" in handler.file
