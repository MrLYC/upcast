"""Tests for asyncio concurrency patterns."""

import pytest

from upcast.scanners.concurrency import ConcurrencyScanner
from tests.fixtures.test_utils import create_test_file


class TestAsyncFunctions:
    """Test detection of async function definitions."""

    def test_simple_async_function(self, tmp_path, create_scanner):
        """Test detection of basic async function."""
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
        assert "async_function" in asyncio_patterns

    def test_async_method_in_class(self, tmp_path, create_scanner):
        """Test detection of async methods in classes."""
        code = """
import asyncio

class AsyncClass:
    async def async_method(self):
        await asyncio.sleep(1)
        return "done"
"""
        file_path = create_test_file(tmp_path, code, "async_class.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        asyncio_patterns = output.results["asyncio"]
        assert len(asyncio_patterns) >= 1


class TestAwaitExpressions:
    """Test detection of await expressions."""

    def test_simple_await(self, tmp_path, create_scanner):
        """Test detection of basic await expression."""
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
        assert "await" in asyncio_patterns
        assert len(asyncio_patterns["await"]) >= 1

    def test_await_in_loop(self, tmp_path, create_scanner):
        """Test detection of await in loop."""
        code = """
import asyncio

async def await_in_loop():
    for i in range(5):
        await asyncio.sleep(0.1)
"""
        file_path = create_test_file(tmp_path, code, "await_loop.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        asyncio_patterns = output.results["asyncio"]
        assert "await" in asyncio_patterns

    def test_await_in_with(self, tmp_path, create_scanner):
        """Test detection of await in with statement."""
        code = """
import asyncio

async def await_in_with():
    async with some_context() as ctx:
        result = await ctx.process()
    return result

async def some_context():
    pass
"""
        file_path = create_test_file(tmp_path, code, "await_with.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        asyncio_patterns = output.results["asyncio"]
        assert len(asyncio_patterns) >= 1


class TestCreateTask:
    """Test detection of asyncio.create_task() patterns."""

    def test_basic_create_task(self, tmp_path, create_scanner):
        """Test detection of basic create_task."""
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
        assert "create_task" in asyncio_patterns
        assert len(asyncio_patterns["create_task"]) >= 1

    def test_multiple_create_task(self, tmp_path, create_scanner):
        """Test detection of multiple create_task calls."""
        code = """
import asyncio

async def create_multiple_tasks():
    task1 = asyncio.create_task(worker(1))
    task2 = asyncio.create_task(worker(2))
    task3 = asyncio.create_task(worker(3))
    await asyncio.gather(task1, task2, task3)

async def worker(n):
    return n * 2
"""
        file_path = create_test_file(tmp_path, code, "multiple_tasks.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        asyncio_patterns = output.results["asyncio"]
        assert "create_task" in asyncio_patterns
        assert len(asyncio_patterns["create_task"]) >= 3


class TestRunInExecutor:
    """Test detection of loop.run_in_executor() patterns."""

    def test_run_in_executor_with_threadpool(self, tmp_path, create_scanner):
        """Test detection of run_in_executor with ThreadPoolExecutor."""
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
        file_path = create_test_file(tmp_path, code, "run_in_executor_thread.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        # run_in_executor with ThreadPoolExecutor should be in threading category
        threading_patterns = output.results["threading"]
        found = any("run_in_executor" in key for key in threading_patterns.keys())
        assert found

    def test_run_in_executor_with_processpool(self, tmp_path, create_scanner):
        """Test detection of run_in_executor with ProcessPoolExecutor."""
        code = """
import asyncio
from concurrent.futures import ProcessPoolExecutor

async def use_run_in_executor():
    loop = asyncio.get_event_loop()
    executor = ProcessPoolExecutor()
    result = await loop.run_in_executor(executor, compute)
    return result

def compute():
    return 42
"""
        file_path = create_test_file(tmp_path, code, "run_in_executor_process.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        # run_in_executor with ProcessPoolExecutor should be in multiprocessing category
        mp_patterns = output.results["multiprocessing"]
        found = any("run_in_executor" in key for key in mp_patterns.keys())
        assert found

    def test_run_in_executor_with_none(self, tmp_path, create_scanner):
        """Test detection of run_in_executor with None executor (default thread pool)."""
        code = """
import asyncio

async def use_run_in_executor():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_task)
    return result

def blocking_task():
    return 42
"""
        file_path = create_test_file(tmp_path, code, "run_in_executor_none.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        # None executor should default to threading
        threading_patterns = output.results["threading"]
        found = any("run_in_executor" in key for key in threading_patterns.keys())
        assert found


class TestAsyncioGather:
    """Test scenarios with asyncio.gather()."""

    def test_gather_multiple_tasks(self, tmp_path, create_scanner):
        """Test gather with multiple tasks."""
        code = """
import asyncio

async def use_gather():
    results = await asyncio.gather(
        task1(),
        task2(),
        task3()
    )
    return results

async def task1():
    return 1

async def task2():
    return 2

async def task3():
    return 3
"""
        file_path = create_test_file(tmp_path, code, "gather.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        asyncio_patterns = output.results["asyncio"]
        # Should detect async functions and await
        assert len(asyncio_patterns) >= 1


class TestAsyncioInClass:
    """Test detection of asyncio patterns in class methods."""

    def test_async_method_in_class(self, tmp_path, create_scanner):
        """Test async method inside class."""
        code = """
import asyncio

class AsyncWorker:
    async def process(self):
        task = asyncio.create_task(self.worker())
        await task
    
    async def worker(self):
        await asyncio.sleep(1)
        return "done"
"""
        file_path = create_test_file(tmp_path, code, "async_class.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        asyncio_patterns = output.results["asyncio"]
        assert len(asyncio_patterns) >= 1

        # Check context capture
        for pattern_list in asyncio_patterns.values():
            if pattern_list and pattern_list[0].class_name:
                assert pattern_list[0].class_name == "AsyncWorker"
                break
