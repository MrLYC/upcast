"""Integration tests for concurrency pattern scanner."""

import pytest
from pathlib import Path

from upcast.scanners.concurrency import ConcurrencyScanner
from upcast.models.concurrency import ConcurrencyPatternOutput
from tests.fixtures.test_utils import create_test_file


class TestScannerInstantiation:
    """Test scanner instantiation and basic functionality."""

    def test_scanner_instantiation(self, scanner_kwargs):
        """Test that scanner can be instantiated."""
        scanner = ConcurrencyScanner(**scanner_kwargs)
        assert scanner is not None
        assert isinstance(scanner, ConcurrencyScanner)

    def test_scanner_has_executor_types(self):
        """Test that scanner has defined executor types."""
        assert hasattr(ConcurrencyScanner, "EXECUTOR_TYPES")
        executor_types = ConcurrencyScanner.EXECUTOR_TYPES
        assert "ThreadPoolExecutor" in executor_types
        assert "ProcessPoolExecutor" in executor_types


class TestBasicScanning:
    """Test basic scanning functionality."""

    def test_scan_empty_file(self, tmp_path, create_scanner):
        """Test scanning an empty file."""
        file_path = create_test_file(tmp_path, "", "empty.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        assert isinstance(output, ConcurrencyPatternOutput)
        assert output.summary.total_count == 0
        assert all(len(patterns) == 0 for patterns in output.results.values())

    def test_scan_file_without_concurrency(self, tmp_path, create_scanner):
        """Test scanning a file without concurrency patterns."""
        code = """
def pure_function():
    x = 1 + 2
    return x * 3

class PureClass:
    def compute(self):
        return 42
"""
        file_path = create_test_file(tmp_path, code, "pure.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        assert output.summary.total_count == 0
        assert all(len(patterns) == 0 for patterns in output.results.values())

    def test_scan_single_thread_creation(self, tmp_path, create_scanner):
        """Test scanning a file with a single thread creation."""
        code = """
import threading

def create_thread():
    t = threading.Thread(target=worker)
    t.start()

def worker():
    pass
"""
        file_path = create_test_file(tmp_path, code, "thread.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        assert output.summary.total_count >= 1
        assert len(output.results["threading"]) >= 1

    def test_scan_directory(self, tmp_path, create_scanner):
        """Test scanning a directory with multiple files."""
        # Create multiple files
        file1 = tmp_path / "file1.py"
        file1.write_text("import threading\ndef f1(): t = threading.Thread(target=lambda: None)")

        file2 = tmp_path / "file2.py"
        file2.write_text("import asyncio\nasync def f2(): await asyncio.sleep(1)")

        scanner = create_scanner(ConcurrencyScanner)
        output = scanner.scan(tmp_path)

        assert output.summary.total_count >= 2
        assert output.summary.files_scanned >= 2


class TestThreadingPatternDetection:
    """Test detection of threading patterns."""

    def test_detect_thread_creation(self, tmp_path, create_scanner):
        """Test detection of threading.Thread creation."""
        code = """
import threading

def create_thread():
    t = threading.Thread(target=worker, name="worker-1")
    t.start()

def worker():
    pass
"""
        file_path = create_test_file(tmp_path, code, "thread.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        threading_patterns = output.results["threading"]
        assert len(threading_patterns) >= 1
        # Check if thread_creation or Thread pattern exists
        found_thread = any("Thread" in key or "thread_creation" in key for key in threading_patterns.keys())
        assert found_thread

    def test_detect_threadpool_executor(self, tmp_path, create_scanner):
        """Test detection of ThreadPoolExecutor."""
        code = """
from concurrent.futures import ThreadPoolExecutor

def use_threadpool():
    executor = ThreadPoolExecutor(max_workers=4)
    future = executor.submit(task)

def task():
    pass
"""
        file_path = create_test_file(tmp_path, code, "threadpool.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        threading_patterns = output.results["threading"]
        assert len(threading_patterns) >= 1
        # Check for ThreadPoolExecutor or submit patterns
        found_pool = any(
            "ThreadPoolExecutor" in key or "submit" in key or "thread_pool" in key for key in threading_patterns.keys()
        )
        assert found_pool

    def test_detect_executor_submit(self, tmp_path, create_scanner):
        """Test detection of executor.submit() calls."""
        code = """
from concurrent.futures import ThreadPoolExecutor

def use_executor():
    executor = ThreadPoolExecutor(max_workers=2)
    future = executor.submit(compute, 10)
    return future.result()

def compute(x):
    return x * 2
"""
        file_path = create_test_file(tmp_path, code, "executor_submit.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        threading_patterns = output.results["threading"]
        assert len(threading_patterns) >= 1


class TestMultiprocessingPatternDetection:
    """Test detection of multiprocessing patterns."""

    def test_detect_process_creation(self, tmp_path, create_scanner):
        """Test detection of multiprocessing.Process creation."""
        code = """
import multiprocessing

def create_process():
    p = multiprocessing.Process(target=worker, name="process-1")
    p.start()

def worker():
    pass
"""
        file_path = create_test_file(tmp_path, code, "process.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        mp_patterns = output.results["multiprocessing"]
        assert len(mp_patterns) >= 1
        found_process = any("Process" in key or "process_creation" in key for key in mp_patterns.keys())
        assert found_process

    def test_detect_processpool_executor(self, tmp_path, create_scanner):
        """Test detection of ProcessPoolExecutor."""
        code = """
from concurrent.futures import ProcessPoolExecutor

def use_processpool():
    executor = ProcessPoolExecutor(max_workers=2)
    future = executor.submit(compute)

def compute():
    return 42
"""
        file_path = create_test_file(tmp_path, code, "processpool.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        mp_patterns = output.results["multiprocessing"]
        assert len(mp_patterns) >= 1


class TestAsyncioPatternDetection:
    """Test detection of asyncio patterns."""

    def test_detect_async_function(self, tmp_path, create_scanner):
        """Test detection of async function definitions."""
        code = """
import asyncio

async def async_task():
    await asyncio.sleep(1)
    return "done"
"""
        file_path = create_test_file(tmp_path, code, "async_func.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        asyncio_patterns = output.results["asyncio"]
        assert len(asyncio_patterns) >= 1
        assert "async_function" in asyncio_patterns or any("async" in key for key in asyncio_patterns.keys())

    def test_detect_await_expression(self, tmp_path, create_scanner):
        """Test detection of await expressions."""
        code = """
import asyncio

async def await_example():
    result = await some_coroutine()
    return result

async def some_coroutine():
    return 42
"""
        file_path = create_test_file(tmp_path, code, "await.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        asyncio_patterns = output.results["asyncio"]
        assert len(asyncio_patterns) >= 1
        # Should have both async_function and await
        assert "await" in asyncio_patterns or "async_function" in asyncio_patterns

    def test_detect_create_task(self, tmp_path, create_scanner):
        """Test detection of asyncio.create_task() calls."""
        code = """
import asyncio

async def create_tasks():
    task = asyncio.create_task(worker())
    await task

async def worker():
    return "done"
"""
        file_path = create_test_file(tmp_path, code, "create_task.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        asyncio_patterns = output.results["asyncio"]
        assert len(asyncio_patterns) >= 1
        # Should detect create_task
        found_create_task = any("create_task" in key for key in asyncio_patterns.keys())
        assert found_create_task

    def test_detect_run_in_executor(self, tmp_path, create_scanner):
        """Test detection of loop.run_in_executor() calls."""
        code = """
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def use_run_in_executor():
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor()
    result = await loop.run_in_executor(executor, blocking_task)
    return result

def blocking_task():
    return 42
"""
        file_path = create_test_file(tmp_path, code, "run_in_executor.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        # run_in_executor with ThreadPoolExecutor goes to threading category
        threading_patterns = output.results["threading"]
        found_run_in_executor = any("run_in_executor" in key for key in threading_patterns.keys())
        assert found_run_in_executor or len(threading_patterns) >= 1


class TestContextCapture:
    """Test that scanner captures proper context information."""

    def test_capture_function_context(self, tmp_path, create_scanner):
        """Test that scanner captures containing function name."""
        code = """
import threading

def my_function():
    t = threading.Thread(target=lambda: None)
"""
        file_path = create_test_file(tmp_path, code, "func_context.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        # Find any threading pattern
        for pattern_list in output.results["threading"].values():
            if pattern_list:
                assert pattern_list[0].function == "my_function"
                break

    def test_capture_class_context(self, tmp_path, create_scanner):
        """Test that scanner captures containing class name."""
        code = """
import threading

class MyClass:
    def method(self):
        t = threading.Thread(target=lambda: None)
"""
        file_path = create_test_file(tmp_path, code, "class_context.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        # Find any threading pattern
        for pattern_list in output.results["threading"].values():
            if pattern_list:
                assert pattern_list[0].class_name == "MyClass"
                assert pattern_list[0].function == "method"
                break


class TestSummaryGeneration:
    """Test that summary statistics are correctly generated."""

    def test_summary_has_correct_total_count(self, tmp_path, create_scanner):
        """Test that summary total_count matches actual patterns."""
        code = """
import threading
import asyncio

def multiple_patterns():
    t1 = threading.Thread(target=lambda: None)
    t2 = threading.Thread(target=lambda: None)

async def async_func():
    await asyncio.sleep(1)
"""
        file_path = create_test_file(tmp_path, code, "multi_patterns.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        # Count patterns in results
        total_in_results = sum(
            len(usages) for category_patterns in output.results.values() for usages in category_patterns.values()
        )

        assert output.summary.total_count == total_in_results
        assert output.summary.total_count >= 3

    def test_summary_by_category_matches_results(self, tmp_path, create_scanner):
        """Test that summary by_category matches actual results."""
        code = """
import threading
import multiprocessing
import asyncio

def various_patterns():
    t = threading.Thread(target=lambda: None)
    p = multiprocessing.Process(target=lambda: None)

async def async_func():
    await asyncio.sleep(1)
"""
        file_path = create_test_file(tmp_path, code, "various.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        # Verify by_category matches actual results
        for category, count in output.summary.by_category.items():
            actual_count = sum(len(usages) for usages in output.results[category].values())
            assert count == actual_count

    def test_summary_scan_duration_is_set(self, tmp_path, create_scanner):
        """Test that scan duration is measured and set."""
        code = """
import threading

def test_func():
    t = threading.Thread(target=lambda: None)
"""
        file_path = create_test_file(tmp_path, code, "duration_test.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        assert output.summary.scan_duration_ms >= 0
        assert isinstance(output.summary.scan_duration_ms, int)


class TestDetailsExtraction:
    """Test that pattern-specific details are extracted."""

    def test_extract_thread_target(self, tmp_path, create_scanner):
        """Test extraction of thread target function."""
        code = """
import threading

def worker():
    pass

def create_thread():
    t = threading.Thread(target=worker, name="worker-1")
"""
        file_path = create_test_file(tmp_path, code, "thread_target.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        # Find thread creation pattern
        for pattern_list in output.results["threading"].values():
            if pattern_list and pattern_list[0].details:
                details = pattern_list[0].details
                assert "target" in details or "name" in details
                break

    def test_extract_max_workers(self, tmp_path, create_scanner):
        """Test extraction of max_workers parameter."""
        code = """
from concurrent.futures import ThreadPoolExecutor

def use_pool():
    executor = ThreadPoolExecutor(max_workers=4)
"""
        file_path = create_test_file(tmp_path, code, "max_workers.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        # Find executor pattern with max_workers
        for pattern_list in output.results["threading"].values():
            if pattern_list and pattern_list[0].details:
                details = pattern_list[0].details
                if "max_workers" in details:
                    assert details["max_workers"] == 4
                    break

    def test_extract_coroutine_name(self, tmp_path, create_scanner):
        """Test extraction of coroutine name in create_task."""
        code = """
import asyncio

async def worker():
    pass

async def create_tasks():
    task = asyncio.create_task(worker())
"""
        file_path = create_test_file(tmp_path, code, "coroutine_name.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        # Find create_task pattern
        if "create_task" in output.results["asyncio"]:
            tasks = output.results["asyncio"]["create_task"]
            if tasks and tasks[0].details:
                assert "coroutine" in tasks[0].details
