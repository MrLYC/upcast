"""Tests for exception handler models."""

import pytest
from pydantic import ValidationError

from upcast.models.exceptions import (
    ExceptionBlock,
    ExceptionHandler,
    ExceptionHandlerSummary,
    ExceptionHandlerOutput,
)


class TestExceptionBlockModel:
    """Test ExceptionBlock model validation."""

    def test_exception_block_valid(self):
        """Test valid ExceptionBlock creation."""
        block = ExceptionBlock(
            lineno=10,
            exceptions=["ValueError"],
            lines=3,
            log_error_count=1,
            pass_count=0,
        )
        assert block.lineno == 10
        assert block.exceptions == ["ValueError"]
        assert block.lines == 3
        assert block.log_error_count == 1

    def test_exception_block_multiple_exceptions(self):
        """Test ExceptionBlock with multiple exception types."""
        block = ExceptionBlock(
            lineno=10,
            exceptions=["ValueError", "KeyError", "TypeError"],
            lines=5,
        )
        assert len(block.exceptions) == 3
        assert "ValueError" in block.exceptions

    def test_exception_block_bare_except(self):
        """Test ExceptionBlock for bare except (empty exceptions)."""
        block = ExceptionBlock(
            lineno=10,
            exceptions=[],
            lines=2,
        )
        assert block.exceptions == []
        assert block.lines == 2

    def test_exception_block_with_logging(self):
        """Test ExceptionBlock with logging counts."""
        block = ExceptionBlock(
            lineno=10,
            exceptions=["Exception"],
            lines=5,
            log_error_count=2,
            log_exception_count=1,
            log_warning_count=1,
        )
        assert block.log_error_count == 2
        assert block.log_exception_count == 1
        assert block.log_warning_count == 1
        assert block.log_debug_count == 0

    def test_exception_block_with_control_flow(self):
        """Test ExceptionBlock with control flow counts."""
        block = ExceptionBlock(
            lineno=10,
            exceptions=["ValueError"],
            lines=3,
            return_count=1,
            raise_count=1,
            pass_count=0,
        )
        assert block.return_count == 1
        assert block.raise_count == 1
        assert block.break_count == 0


class TestExceptionHandlerModel:
    """Test ExceptionHandler model validation."""

    def test_exception_handler_valid(self):
        """Test valid ExceptionHandler creation."""
        handler = ExceptionHandler(
            file="test.py",
            try_lineno=10,
            try_lines=3,
            else_lineno=None,
            else_lines=None,
            finally_lineno=None,
            finally_lines=None,
            exception_blocks=[ExceptionBlock(lineno=13, exceptions=["ValueError"], lines=2)],
        )
        assert handler.file == "test.py"
        assert handler.try_lineno == 10
        assert handler.try_lines == 3
        assert len(handler.exception_blocks) == 1

    def test_exception_handler_with_else_finally(self):
        """Test ExceptionHandler with else and finally clauses."""
        handler = ExceptionHandler(
            file="test.py",
            try_lineno=10,
            try_lines=3,
            else_lineno=15,
            else_lines=2,
            finally_lineno=17,
            finally_lines=3,
            exception_blocks=[ExceptionBlock(lineno=13, exceptions=["ValueError"], lines=2)],
        )
        assert handler.else_lineno == 15
        assert handler.else_lines == 2
        assert handler.finally_lineno == 17
        assert handler.finally_lines == 3

    def test_exception_handler_multiple_blocks(self):
        """Test ExceptionHandler with multiple exception blocks."""
        handler = ExceptionHandler(
            file="test.py",
            try_lineno=10,
            try_lines=3,
            else_lineno=None,
            else_lines=None,
            finally_lineno=None,
            finally_lines=None,
            exception_blocks=[
                ExceptionBlock(lineno=13, exceptions=["ValueError"], lines=2),
                ExceptionBlock(lineno=15, exceptions=["KeyError"], lines=2),
                ExceptionBlock(lineno=17, exceptions=["Exception"], lines=2),
            ],
        )
        assert len(handler.exception_blocks) == 3
        assert handler.exception_blocks[0].exceptions == ["ValueError"]
        assert handler.exception_blocks[1].exceptions == ["KeyError"]

    def test_exception_handler_nested(self):
        """Test ExceptionHandler with nested flag."""
        handler = ExceptionHandler(
            file="test.py",
            try_lineno=10,
            try_lines=3,
            else_lineno=None,
            else_lines=None,
            finally_lineno=None,
            finally_lines=None,
            nested_exceptions=True,
            exception_blocks=[ExceptionBlock(lineno=13, exceptions=["ValueError"], lines=2)],
        )
        assert handler.nested_exceptions is True


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
                    try_lineno=10,
                    try_lines=3,
                    else_lineno=None,
                    else_lines=None,
                    finally_lineno=None,
                    finally_lines=None,
                    exception_blocks=[ExceptionBlock(lineno=13, exceptions=["ValueError"], lines=2)],
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
                    try_lineno=10,
                    try_lines=3,
                    else_lineno=None,
                    else_lines=None,
                    finally_lineno=None,
                    finally_lines=None,
                    exception_blocks=[ExceptionBlock(lineno=13, exceptions=["ValueError"], lines=2)],
                )
            ],
        )
        data = output.model_dump()
        assert "summary" in data
        assert "results" in data
        assert data["summary"]["total_handlers"] == 1
