"""Integration tests for concurrency pattern scanner."""

from pathlib import Path

import pytest

from upcast.concurrency_pattern_scanner.checker import ConcurrencyChecker


@pytest.fixture
def fixtures_dir():
    """Get fixtures directory path."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def asyncio_fixture(fixtures_dir):
    """Get asyncio fixture file path."""
    return str(fixtures_dir / "asyncio_patterns.py")


@pytest.fixture
def threading_fixture(fixtures_dir):
    """Get threading fixture file path."""
    return str(fixtures_dir / "threading_patterns.py")


@pytest.fixture
def multiprocessing_fixture(fixtures_dir):
    """Get multiprocessing fixture file path."""
    return str(fixtures_dir / "multiprocessing_patterns.py")


@pytest.fixture
def run_in_executor_fixture(fixtures_dir):
    """Get run_in_executor fixture file path."""
    return str(fixtures_dir / "run_in_executor_patterns.py")


@pytest.fixture
def mixed_fixture(fixtures_dir):
    """Get mixed patterns fixture file path."""
    return str(fixtures_dir / "mixed_patterns.py")


@pytest.fixture
def complex_fixture(fixtures_dir):
    """Get complex patterns fixture file path."""
    return str(fixtures_dir / "complex_patterns.py")


def test_check_asyncio_patterns(asyncio_fixture):
    """Test detecting asyncio patterns."""
    checker = ConcurrencyChecker(verbose=False)
    checker.check_file(asyncio_fixture)

    patterns = checker.get_patterns()

    # Should have asyncio patterns
    assert "asyncio" in patterns
    asyncio_patterns = patterns["asyncio"]

    # Should detect async functions
    assert "async_functions" in asyncio_patterns
    assert len(asyncio_patterns["async_functions"]) >= 4  # At least 4 async functions in fixture

    # Should detect await expressions
    assert "await_expressions" in asyncio_patterns
    assert len(asyncio_patterns["await_expressions"]) > 0

    # Should detect gather
    assert "gather_patterns" in asyncio_patterns
    assert len(asyncio_patterns["gather_patterns"]) >= 1

    # Should detect create_task
    assert "task_creation" in asyncio_patterns
    assert len(asyncio_patterns["task_creation"]) >= 1


def test_check_threading_patterns(threading_fixture):
    """Test detecting threading patterns."""
    checker = ConcurrencyChecker(verbose=False)
    checker.check_file(threading_fixture)

    patterns = checker.get_patterns()

    # Should have threading patterns
    assert "threading" in patterns
    threading_patterns = patterns["threading"]

    # Should detect Thread creation
    assert "thread_creation" in threading_patterns
    assert len(threading_patterns["thread_creation"]) >= 3  # Multiple threads created in fixture

    # Should detect ThreadPoolExecutor
    assert "thread_pool_executors" in threading_patterns
    assert len(threading_patterns["thread_pool_executors"]) >= 2


def test_check_multiprocessing_patterns(multiprocessing_fixture):
    """Test detecting multiprocessing patterns."""
    checker = ConcurrencyChecker(verbose=False)
    checker.check_file(multiprocessing_fixture)

    patterns = checker.get_patterns()

    # Should have multiprocessing patterns
    assert "multiprocessing" in patterns
    mp_patterns = patterns["multiprocessing"]

    # Should detect Process creation
    assert "process_creation" in mp_patterns
    assert len(mp_patterns["process_creation"]) >= 3  # Multiple processes created in fixture

    # Should detect ProcessPoolExecutor
    assert "process_pool_executors" in mp_patterns
    assert len(mp_patterns["process_pool_executors"]) >= 2


def test_check_run_in_executor_patterns(run_in_executor_fixture):
    """Test detecting run_in_executor patterns."""
    checker = ConcurrencyChecker(verbose=False)
    checker.check_file(run_in_executor_fixture)

    patterns = checker.get_patterns()

    # Should have run_in_executor in threading and multiprocessing
    # Default executor goes to threading
    if "threading" in patterns and "run_in_executor" in patterns["threading"]:
        assert len(patterns["threading"]["run_in_executor"]) >= 1

    # Process executor goes to multiprocessing
    if "multiprocessing" in patterns and "run_in_executor" in patterns["multiprocessing"]:
        assert len(patterns["multiprocessing"]["run_in_executor"]) >= 1


def test_check_multiple_files(asyncio_fixture, threading_fixture):
    """Test checking multiple files."""
    checker = ConcurrencyChecker(verbose=False)
    checker.check_file(asyncio_fixture)
    checker.check_file(threading_fixture)

    patterns = checker.get_patterns()

    # Should have both asyncio and threading patterns
    assert "asyncio" in patterns
    assert "threading" in patterns

    # Should aggregate patterns from both files
    assert len(patterns["asyncio"]) > 0
    assert len(patterns["threading"]) > 0


def test_pattern_context_extraction(asyncio_fixture):
    """Test that context information is extracted correctly."""
    checker = ConcurrencyChecker(verbose=False)
    checker.check_file(asyncio_fixture)

    patterns = checker.get_patterns()
    asyncio_patterns = patterns["asyncio"]

    # Check async functions have proper context
    if "async_functions" in asyncio_patterns:
        for pattern in asyncio_patterns["async_functions"]:
            assert "file" in pattern
            assert "line" in pattern
            # Function context should be None at top level
            # or have a value if nested
            assert "function_context" in pattern
            assert "class_context" in pattern


def test_empty_file_detection():
    """Test that empty pattern collections are handled correctly."""
    checker = ConcurrencyChecker(verbose=False)

    # No files checked, should have empty pattern collections
    patterns = checker.get_patterns()

    assert "asyncio" in patterns
    assert "threading" in patterns
    assert "multiprocessing" in patterns

    # All should be empty dicts
    assert patterns["asyncio"] == {}
    assert patterns["threading"] == {}
    assert patterns["multiprocessing"] == {}


def test_checker_with_root_path(asyncio_fixture, fixtures_dir):
    """Test checker with custom root path."""
    checker = ConcurrencyChecker(root_path=str(fixtures_dir), verbose=False)
    checker.check_file(asyncio_fixture)

    patterns = checker.get_patterns()

    # Should still detect patterns
    assert "asyncio" in patterns
    assert len(patterns["asyncio"]) > 0


def test_check_mixed_patterns(mixed_fixture):
    """Test detecting mixed concurrency patterns in one file."""
    checker = ConcurrencyChecker(verbose=False)
    checker.check_file(mixed_fixture)

    patterns = checker.get_patterns()

    # Should have all three types
    assert "asyncio" in patterns
    assert "threading" in patterns
    assert "multiprocessing" in patterns

    # Should have multiple pattern types
    if "asyncio" in patterns:
        asyncio_patterns = patterns["asyncio"]
        # Should have async functions, gather, create_task, await, run_in_executor
        assert len([k for k in asyncio_patterns if asyncio_patterns[k]]) >= 3


def test_check_complex_patterns(complex_fixture):
    """Test detecting complex edge case patterns."""
    checker = ConcurrencyChecker(verbose=False)
    checker.check_file(complex_fixture)

    patterns = checker.get_patterns()

    # Should detect patterns even in complex scenarios
    assert any(patterns.values())

    # Should detect nested async functions
    if "asyncio" in patterns and "async_functions" in patterns["asyncio"]:
        assert len(patterns["asyncio"]["async_functions"]) > 0

    # Should detect threading in nested contexts
    if "threading" in patterns and "thread_creation" in patterns["threading"]:
        assert len(patterns["threading"]["thread_creation"]) >= 1
