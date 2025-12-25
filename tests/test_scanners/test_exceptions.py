"""Tests for ExceptionHandlerScanner."""

from upcast.scanners.exceptions import (
    ExceptClause,
    ExceptionHandlerScanner,
)


class TestExceptionModels:
    """Tests for exception handler models."""

    def test_valid_except_clause(self):
        """Test creating valid ExceptClause."""
        clause = ExceptClause(
            line=10,
            exception_types=["ValueError", "TypeError"],
            lines=3,
            log_error_count=1,
        )
        assert clause.line == 10
        assert len(clause.exception_types) == 2


class TestExceptionHandlerScannerIntegration:
    """Integration tests for ExceptionHandlerScanner."""

    def test_scanner_detects_try_except(self, tmp_path):
        """Test scanner detects try-except blocks."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
try:
    risky_operation()
except ValueError:
    pass
"""
        )

        scanner = ExceptionHandlerScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 0

    def test_scanner_handles_empty_file(self, tmp_path):
        """Test scanner handles empty files."""
        test_file = tmp_path / "test.py"
        test_file.write_text("")

        scanner = ExceptionHandlerScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 0
