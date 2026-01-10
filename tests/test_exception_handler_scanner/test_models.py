"""Tests for exception handler models."""

import pytest
from pydantic import ValidationError

from upcast.models.exceptions import (
    ExceptClause,
    ElseClause,
    FinallyClause,
    ExceptionHandler,
    ExceptionHandlerSummary,
    ExceptionHandlerOutput,
)


class TestExceptClauseModel:
    """Test ExceptClause model validation."""

    def test_except_clause_valid(self):
        """Test valid ExceptClause creation."""
        clause = ExceptClause(
            line=10,
            exception_types=["ValueError"],
            lines=3,
            log_error_count=1,
            pass_count=0,
        )
        assert clause.line == 10
        assert clause.exception_types == ["ValueError"]
        assert clause.lines == 3
        assert clause.log_error_count == 1

    def test_except_clause_multiple_exception_types(self):
        """Test ExceptClause with multiple exception types."""
        clause = ExceptClause(
            line=10,
            exception_types=["ValueError", "KeyError", "TypeError"],
            lines=5,
        )
        assert len(clause.exception_types) == 3
        assert "ValueError" in clause.exception_types

    def test_except_clause_bare_except(self):
        """Test ExceptClause for bare except (empty exception_types)."""
        clause = ExceptClause(
            line=10,
            exception_types=[],
            lines=2,
        )
        assert clause.exception_types == []
        assert clause.lines == 2

    def test_except_clause_with_logging(self):
        """Test ExceptClause with logging counts."""
        clause = ExceptClause(
            line=10,
            exception_types=["Exception"],
            lines=5,
            log_error_count=2,
            log_exception_count=1,
            log_warning_count=1,
        )
        assert clause.log_error_count == 2
        assert clause.log_exception_count == 1
        assert clause.log_warning_count == 1
        assert clause.log_debug_count == 0  # Default

    def test_except_clause_with_control_flow(self):
        """Test ExceptClause with control flow counts."""
        clause = ExceptClause(
            line=10,
            exception_types=["ValueError"],
            lines=3,
            return_count=1,
            raise_count=1,
            pass_count=0,
        )
        assert clause.return_count == 1
        assert clause.raise_count == 1
        assert clause.break_count == 0  # Default


class TestElseClauseModel:
    """Test ElseClause model validation."""

    def test_else_clause_valid(self):
        """Test valid ElseClause creation."""
        clause = ElseClause(line=15, lines=3)
        assert clause.line == 15
        assert clause.lines == 3

    def test_else_clause_negative_line(self):
        """Test that negative line number is rejected."""
        with pytest.raises(ValidationError):
            ElseClause(line=-1, lines=3)


class TestFinallyClauseModel:
    """Test FinallyClause model validation."""

    def test_finally_clause_valid(self):
        """Test valid FinallyClause creation."""
        clause = FinallyClause(line=20, lines=2)
        assert clause.line == 20
        assert clause.lines == 2

    def test_finally_clause_zero_lines(self):
        """Test FinallyClause with zero lines."""
        clause = FinallyClause(line=20, lines=0)
        assert clause.lines == 0


class TestExceptionHandlerModel:
    """Test ExceptionHandler model validation."""

    def test_exception_handler_valid(self):
        """Test valid ExceptionHandler creation."""
        handler = ExceptionHandler(
            file="test.py",
            lineno=10,
            end_lineno=15,
            try_lines=3,
            except_clauses=[ExceptClause(line=13, exception_types=["ValueError"], lines=2)],
        )
        assert handler.file == "test.py"
        assert handler.lineno == 10
        assert handler.end_lineno == 15
        assert len(handler.except_clauses) == 1

    def test_exception_handler_with_else_finally(self):
        """Test ExceptionHandler with else and finally clauses."""
        handler = ExceptionHandler(
            file="test.py",
            lineno=10,
            end_lineno=20,
            try_lines=3,
            except_clauses=[ExceptClause(line=13, exception_types=["ValueError"], lines=2)],
            else_clause=ElseClause(line=15, lines=2),
            finally_clause=FinallyClause(line=17, lines=3),
        )
        assert handler.else_clause is not None
        assert handler.finally_clause is not None
        assert handler.else_clause.line == 15
        assert handler.finally_clause.line == 17

    def test_exception_handler_multiple_except_clauses(self):
        """Test ExceptionHandler with multiple except clauses."""
        handler = ExceptionHandler(
            file="test.py",
            lineno=10,
            end_lineno=20,
            try_lines=3,
            except_clauses=[
                ExceptClause(line=13, exception_types=["ValueError"], lines=2),
                ExceptClause(line=15, exception_types=["KeyError"], lines=2),
                ExceptClause(line=17, exception_types=["Exception"], lines=2),
            ],
        )
        assert len(handler.except_clauses) == 3
        assert handler.except_clauses[0].exception_types == ["ValueError"]
        assert handler.except_clauses[1].exception_types == ["KeyError"]


class TestExceptionHandlerSummaryModel:
    """Test ExceptionHandlerSummary model validation."""

    def test_summary_valid(self):
        """Test valid ExceptionHandlerSummary creation."""
        summary = ExceptionHandlerSummary(
            total_count=5,
            files_scanned=2,
            scan_duration_ms=100,
            total_handlers=3,
            total_except_clauses=5,
        )
        assert summary.total_count == 5
        assert summary.total_handlers == 3
        assert summary.total_except_clauses == 5

    def test_summary_zero_values(self):
        """Test summary with zero values."""
        summary = ExceptionHandlerSummary(
            total_count=0,
            files_scanned=0,
            scan_duration_ms=50,
            total_handlers=0,
            total_except_clauses=0,
        )
        assert summary.total_handlers == 0
        assert summary.total_except_clauses == 0


class TestExceptionHandlerOutputModel:
    """Test ExceptionHandlerOutput model validation."""

    def test_output_valid(self):
        """Test valid ExceptionHandlerOutput creation."""
        output = ExceptionHandlerOutput(
            summary=ExceptionHandlerSummary(
                total_count=1,
                files_scanned=1,
                scan_duration_ms=100,
                total_handlers=1,
                total_except_clauses=1,
            ),
            results=[
                ExceptionHandler(
                    file="test.py",
                    lineno=10,
                    end_lineno=15,
                    try_lines=3,
                    except_clauses=[ExceptClause(line=13, exception_types=["ValueError"], lines=2)],
                )
            ],
        )
        assert len(output.results) == 1
        assert output.summary.total_handlers == 1

    def test_output_empty_results(self):
        """Test output with empty results."""
        output = ExceptionHandlerOutput(
            summary=ExceptionHandlerSummary(
                total_count=0,
                files_scanned=0,
                scan_duration_ms=50,
                total_handlers=0,
                total_except_clauses=0,
            ),
            results=[],
        )
        assert len(output.results) == 0
        assert output.summary.total_handlers == 0

    def test_output_serialization(self):
        """Test that output can be serialized to dict/JSON."""
        output = ExceptionHandlerOutput(
            summary=ExceptionHandlerSummary(
                total_count=1,
                files_scanned=1,
                scan_duration_ms=100,
                total_handlers=1,
                total_except_clauses=1,
            ),
            results=[
                ExceptionHandler(
                    file="test.py",
                    lineno=10,
                    end_lineno=15,
                    try_lines=3,
                    except_clauses=[ExceptClause(line=13, exception_types=["ValueError"], lines=2)],
                )
            ],
        )
        data = output.model_dump()
        assert "summary" in data
        assert "results" in data
        assert data["summary"]["total_handlers"] == 1
