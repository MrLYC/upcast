"""Tests for export functions."""

from pathlib import Path

from upcast.exception_handler_scanner.checker import ExceptionHandlerChecker
from upcast.exception_handler_scanner.export import format_handler_output


def test_format_handler_output():
    """Test formatting handler output."""
    fixture_dir = Path(__file__).parent / "fixtures"
    simple_file = fixture_dir / "simple.py"

    checker = ExceptionHandlerChecker(fixture_dir)
    checker.check_file(simple_file)

    handlers = checker.get_handlers()
    summary = checker.get_summary()

    output = format_handler_output(handlers, summary)

    # Check structure
    assert "exception_handlers" in output
    assert "summary" in output
    assert isinstance(output["exception_handlers"], list)
    assert isinstance(output["summary"], dict)


def test_format_handler_fields():
    """Test that all required fields are present in formatted output."""
    fixture_dir = Path(__file__).parent / "fixtures"
    complex_file = fixture_dir / "complex.py"

    checker = ExceptionHandlerChecker(fixture_dir)
    checker.check_file(complex_file)

    handlers = checker.get_handlers()
    summary = checker.get_summary()

    output = format_handler_output(handlers, summary)

    # Check first handler structure
    if output["exception_handlers"]:
        handler = output["exception_handlers"][0]
        assert "location" in handler
        assert "try_lines" in handler
        assert "except_clauses" in handler
        assert "else_clause" in handler
        assert "finally_clause" in handler

        # Check except clause structure
        if handler["except_clauses"]:
            clause = handler["except_clauses"][0]
            assert "line" in clause
            assert "exception_types" in clause
            assert "lines" in clause
            # Logging counts
            assert "log_debug_count" in clause
            assert "log_info_count" in clause
            assert "log_warning_count" in clause
            assert "log_error_count" in clause
            assert "log_exception_count" in clause
            assert "log_critical_count" in clause
            # Control flow counts
            assert "pass_count" in clause
            assert "return_count" in clause
            assert "break_count" in clause
            assert "continue_count" in clause
            assert "raise_count" in clause


def test_format_handler_null_clauses():
    """Test that null else/finally clauses are handled correctly."""
    fixture_dir = Path(__file__).parent / "fixtures"
    simple_file = fixture_dir / "simple.py"

    checker = ExceptionHandlerChecker(fixture_dir)
    checker.check_file(simple_file)

    handlers = checker.get_handlers()
    summary = checker.get_summary()

    output = format_handler_output(handlers, summary)

    # Find handlers without else/finally
    handlers_without_else = [h for h in output["exception_handlers"] if h["else_clause"] is None]
    assert len(handlers_without_else) > 0


def test_format_summary_structure():
    """Test summary statistics structure."""
    fixture_dir = Path(__file__).parent / "fixtures"
    logging_file = fixture_dir / "logging.py"

    checker = ExceptionHandlerChecker(fixture_dir)
    checker.check_file(logging_file)

    handlers = checker.get_handlers()
    summary = checker.get_summary()

    output = format_handler_output(handlers, summary)

    # Check summary fields
    summary_data = output["summary"]
    assert "total_try_blocks" in summary_data
    assert "total_except_clauses" in summary_data
    assert "bare_excepts" in summary_data
    assert "except_with_pass" in summary_data
    assert "except_with_return" in summary_data
    assert "except_with_raise" in summary_data
    assert "total_log_calls" in summary_data
    assert "except_without_logging" in summary_data
