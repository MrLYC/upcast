"""Edge case tests for concurrency pattern scanner."""

import pytest

from upcast.scanners.concurrency import ConcurrencyScanner
from tests.fixtures.test_utils import create_test_file


class TestAliasedImports:
    """Test detection with aliased imports."""

    def test_threading_alias(self, tmp_path, create_scanner):
        """Test detection with threading module alias."""
        code = """
import threading as t

def create_thread():
    thread = t.Thread(target=worker)
    thread.start()

def worker():
    pass
"""
        file_path = create_test_file(tmp_path, code, "alias.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        threading_patterns = output.results["threading"]
        assert len(threading_patterns) >= 1

    def test_asyncio_alias(self, tmp_path, create_scanner):
        """Test detection with asyncio alias."""
        code = """
import asyncio as aio

async def async_task():
    await aio.sleep(1)
    return "done"
"""
        file_path = create_test_file(tmp_path, code, "asyncio_alias.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        asyncio_patterns = output.results["asyncio"]
        assert len(asyncio_patterns) >= 1


class TestMixedPatterns:
    """Test files with multiple concurrency patterns."""

    def test_threading_and_asyncio(self, tmp_path, create_scanner):
        """Test file with both threading and asyncio."""
        code = """
import threading
import asyncio

def create_thread():
    t = threading.Thread(target=worker)
    t.start()

def worker():
    pass

async def async_task():
    await asyncio.sleep(1)
"""
        file_path = create_test_file(tmp_path, code, "mixed.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        assert len(output.results["threading"]) >= 1
        assert len(output.results["asyncio"]) >= 1
        assert output.summary.total_count >= 2

    def test_all_categories(self, tmp_path, create_scanner):
        """Test file with patterns from all categories."""
        code = """
import threading
import multiprocessing
import asyncio

def thread_example():
    t = threading.Thread(target=lambda: None)

def process_example():
    p = multiprocessing.Process(target=lambda: None)

async def async_example():
    await asyncio.sleep(1)
"""
        file_path = create_test_file(tmp_path, code, "all_categories.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        assert len(output.results["threading"]) >= 1
        assert len(output.results["multiprocessing"]) >= 1
        assert len(output.results["asyncio"]) >= 1


class TestNegativeCases:
    """Test cases that should NOT detect patterns."""

    def test_no_concurrency_patterns(self, tmp_path, create_scanner):
        """Test file with no concurrency patterns."""
        code = """
def pure_function():
    x = 1 + 2
    return x * 3

class PureClass:
    def compute(self):
        return 42
"""
        file_path = create_test_file(tmp_path, code, "no_concurrency.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        assert output.summary.total_count == 0
        assert all(len(patterns) == 0 for patterns in output.results.values())

    def test_custom_thread_class(self, tmp_path, create_scanner):
        """Test that custom Thread classes are not detected."""
        code = """
class Thread:
    def __init__(self, target):
        self.target = target
    
    def start(self):
        self.target()

def create_custom_thread():
    t = Thread(target=lambda: None)
    t.start()
"""
        file_path = create_test_file(tmp_path, code, "custom_thread.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        # Should NOT detect custom Thread class
        threading_patterns = output.results["threading"]
        assert len(threading_patterns) == 0


class TestEdgeCases:
    """Test edge cases and corner scenarios."""

    def test_nested_async_functions(self, tmp_path, create_scanner):
        """Test nested async function definitions."""
        code = """
import asyncio

async def outer():
    async def inner():
        await asyncio.sleep(1)
    await inner()
"""
        file_path = create_test_file(tmp_path, code, "nested_async.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        asyncio_patterns = output.results["asyncio"]
        # Should detect both async functions
        assert "async_function" in asyncio_patterns
        assert len(asyncio_patterns["async_function"]) >= 2

    def test_lambda_as_target(self, tmp_path, create_scanner):
        """Test thread with lambda as target."""
        code = """
import threading

def create_thread():
    t = threading.Thread(target=lambda: print("hello"))
    t.start()
"""
        file_path = create_test_file(tmp_path, code, "lambda_target.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        threading_patterns = output.results["threading"]
        assert len(threading_patterns) >= 1

    def test_executor_not_tracked(self, tmp_path, create_scanner):
        """Test executor.submit() when executor is not tracked."""
        code = """
def use_unknown_executor(executor):
    # executor is passed as parameter, not created locally
    future = executor.submit(task)
    return future.result()

def task():
    return 42
"""
        file_path = create_test_file(tmp_path, code, "unknown_executor.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        # Should not crash, but won't detect the submit call
        assert output is not None

    def test_create_task_with_unknown_coroutine(self, tmp_path, create_scanner):
        """Test create_task with unknown coroutine."""
        code = """
import asyncio

async def create_task_unknown(coro):
    # coroutine is passed as parameter
    task = asyncio.create_task(coro)
    await task
"""
        file_path = create_test_file(tmp_path, code, "unknown_coro.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        # Should detect async function, but might not detect create_task
        # (per spec, skip if coroutine is unknown)
        asyncio_patterns = output.results["asyncio"]
        assert len(asyncio_patterns) >= 1


class TestLocationInformation:
    """Test that line/column information is correctly captured."""

    def test_line_numbers_are_accurate(self, tmp_path, create_scanner):
        """Test that reported line numbers are accurate."""
        code = """import threading

def func1():
    t = threading.Thread(target=lambda: None)  # Line 4

def func2():
    t = threading.Thread(target=lambda: None)  # Line 7
"""
        file_path = create_test_file(tmp_path, code, "line_test.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        # Find threading patterns and check line numbers
        for pattern_list in output.results["threading"].values():
            if len(pattern_list) >= 2:
                lines = sorted([usage.line for usage in pattern_list])
                assert lines[0] == 4
                assert lines[1] == 7
                break

    def test_column_numbers_are_set(self, tmp_path, create_scanner):
        """Test that column numbers are captured."""
        code = """import threading
def func():
    t = threading.Thread(target=lambda: None)
"""
        file_path = create_test_file(tmp_path, code, "column_test.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        # Check that column is set
        for pattern_list in output.results["threading"].values():
            if pattern_list:
                assert pattern_list[0].column is not None
                assert pattern_list[0].column >= 0
                break
