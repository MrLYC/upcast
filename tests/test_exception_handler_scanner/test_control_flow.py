"""Tests for control flow detection in exception handlers."""

import pytest
from pathlib import Path

from upcast.scanners.exceptions import ExceptionHandlerScanner


class TestControlFlowDetection:
    """Test detection of control flow statements in except clauses."""

    def test_pass_statement(self, tmp_path, scanner):
        """Test detection of pass statements."""
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

    def test_return_statement(self, tmp_path, scanner):
        """Test detection of return statements."""
        code = """
def process():
    try:
        operation()
    except ValueError:
        return None
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        clause = handler.except_clauses[0]
        assert clause.return_count == 1

    def test_raise_statement(self, tmp_path, scanner):
        """Test detection of raise statements."""
        code = """
try:
    operation()
except ValueError:
    raise
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        clause = handler.except_clauses[0]
        assert clause.raise_count == 1

    def test_break_statement(self, tmp_path, scanner):
        """Test detection of break statements."""
        code = """
for item in items:
    try:
        process(item)
    except ValueError:
        break
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        clause = handler.except_clauses[0]
        assert clause.break_count == 1

    def test_continue_statement(self, tmp_path, scanner):
        """Test detection of continue statements."""
        code = """
for item in items:
    try:
        process(item)
    except ValueError:
        continue
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        clause = handler.except_clauses[0]
        assert clause.continue_count == 1

    def test_multiple_control_flow(self, tmp_path, scanner):
        """Test detection of multiple control flow statements."""
        code = """
def process():
    for item in items:
        try:
            handle(item)
        except ValueError:
            pass
            continue
        except KeyError:
            return False
        except Exception:
            raise
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        assert handler.except_clauses[0].pass_count == 1
        assert handler.except_clauses[0].continue_count == 1
        assert handler.except_clauses[1].return_count == 1
        assert handler.except_clauses[2].raise_count == 1

    def test_raise_new_exception(self, tmp_path, scanner):
        """Test detection of raising new exceptions."""
        code = """
try:
    operation()
except ValueError:
    raise CustomError("Wrapped error")
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        clause = handler.except_clauses[0]
        assert clause.raise_count == 1

    def test_raise_from(self, tmp_path, scanner):
        """Test detection of raise...from statements."""
        code = """
try:
    operation()
except ValueError as e:
    raise CustomError("Wrapped") from e
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        clause = handler.except_clauses[0]
        assert clause.raise_count == 1

    def test_return_with_value(self, tmp_path, scanner):
        """Test detection of return with value."""
        code = """
def process():
    try:
        return operation()
    except ValueError:
        return {"error": "failed"}
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        handler = output.results[0]
        # Return in try block
        except_clause = handler.except_clauses[0]
        assert except_clause.return_count == 1
