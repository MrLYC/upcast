"""Tests for ExceptionHandlerChecker."""

from pathlib import Path

from upcast.exception_handler_scanner.checker import ExceptionHandlerChecker


def test_checker_simple_file():
    """Test checker with simple fixture file."""
    fixture_dir = Path(__file__).parent / "fixtures"
    simple_file = fixture_dir / "simple.py"

    checker = ExceptionHandlerChecker(fixture_dir)
    checker.check_file(simple_file)

    handlers = checker.get_handlers()
    assert len(handlers) > 0

    # Check that we found try blocks
    summary = checker.get_summary()
    assert summary["total_try_blocks"] > 0


def test_checker_control_flow_file():
    """Test checker with control flow fixture file."""
    fixture_dir = Path(__file__).parent / "fixtures"
    control_file = fixture_dir / "control_flow.py"

    checker = ExceptionHandlerChecker(fixture_dir)
    checker.check_file(control_file)

    summary = checker.get_summary()
    assert summary["except_with_pass"] > 0
    assert summary["except_with_return"] > 0
    assert summary["except_with_raise"] > 0


def test_checker_logging_file():
    """Test checker with logging fixture file."""
    fixture_dir = Path(__file__).parent / "fixtures"
    logging_file = fixture_dir / "logging.py"

    checker = ExceptionHandlerChecker(fixture_dir)
    checker.check_file(logging_file)

    summary = checker.get_summary()
    assert summary["total_log_calls"] > 0


def test_checker_complex_file():
    """Test checker with complex fixture file."""
    fixture_dir = Path(__file__).parent / "fixtures"
    complex_file = fixture_dir / "complex.py"

    checker = ExceptionHandlerChecker(fixture_dir)
    checker.check_file(complex_file)

    handlers = checker.get_handlers()
    assert len(handlers) > 0

    # Find handler with multiple except clauses
    multi_except = [h for h in handlers if len(h.except_clauses) > 1]
    assert len(multi_except) > 0


def test_checker_multiple_files():
    """Test checker with multiple fixture files."""
    fixture_dir = Path(__file__).parent / "fixtures"

    checker = ExceptionHandlerChecker(fixture_dir)
    checker.check_file(fixture_dir / "simple.py")
    checker.check_file(fixture_dir / "control_flow.py")
    checker.check_file(fixture_dir / "logging.py")

    handlers = checker.get_handlers()
    assert len(handlers) > 5

    summary = checker.get_summary()
    assert summary["total_try_blocks"] > 5
    assert summary["total_except_clauses"] > 5


def test_checker_bare_except():
    """Test detection of bare except clauses."""
    fixture_dir = Path(__file__).parent / "fixtures"
    simple_file = fixture_dir / "simple.py"

    checker = ExceptionHandlerChecker(fixture_dir)
    checker.check_file(simple_file)

    summary = checker.get_summary()
    # simple.py has one bare except
    assert summary["bare_excepts"] >= 1


def test_checker_summary_statistics():
    """Test summary statistics calculation."""
    fixture_dir = Path(__file__).parent / "fixtures"
    logging_file = fixture_dir / "logging.py"

    checker = ExceptionHandlerChecker(fixture_dir)
    checker.check_file(logging_file)

    summary = checker.get_summary()

    # Verify all summary fields exist
    assert "total_try_blocks" in summary
    assert "total_except_clauses" in summary
    assert "bare_excepts" in summary
    assert "except_with_pass" in summary
    assert "except_with_return" in summary
    assert "except_with_raise" in summary
    assert "total_log_calls" in summary
    assert "except_without_logging" in summary

    # All values should be non-negative
    assert all(v >= 0 for v in summary.values())
