"""Tests for threading concurrency patterns."""

import pytest

from upcast.scanners.concurrency import ConcurrencyScanner
from tests.fixtures.test_utils import create_test_file


class TestThreadCreation:
    """Test detection of threading.Thread patterns."""

    def test_basic_thread_creation(self, tmp_path, create_scanner):
        """Test detection of basic Thread creation."""
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

        threading_patterns = output.results["threading"]
        assert len(threading_patterns) >= 1

    def test_thread_with_args(self, tmp_path, create_scanner):
        """Test detection of Thread with arguments."""
        code = """
import threading

def create_thread():
    t = threading.Thread(target=worker, args=(10, 20), kwargs={'name': 'test'})
    t.start()

def worker(a, b, name):
    pass
"""
        file_path = create_test_file(tmp_path, code, "thread_args.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        threading_patterns = output.results["threading"]
        assert len(threading_patterns) >= 1

    def test_thread_with_name(self, tmp_path, create_scanner):
        """Test detection of Thread with name parameter."""
        code = """
import threading

def create_thread():
    t = threading.Thread(target=worker, name="worker-thread")
    t.start()

def worker():
    pass
"""
        file_path = create_test_file(tmp_path, code, "thread_name.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        threading_patterns = output.results["threading"]
        assert len(threading_patterns) >= 1


class TestThreadPoolExecutor:
    """Test detection of ThreadPoolExecutor patterns."""

    def test_threadpool_creation(self, tmp_path, create_scanner):
        """Test detection of ThreadPoolExecutor instantiation."""
        code = """
from concurrent.futures import ThreadPoolExecutor

def create_pool():
    executor = ThreadPoolExecutor(max_workers=4)
"""
        file_path = create_test_file(tmp_path, code, "pool.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        threading_patterns = output.results["threading"]
        assert len(threading_patterns) >= 1

    def test_threadpool_submit(self, tmp_path, create_scanner):
        """Test detection of executor.submit() method."""
        code = """
from concurrent.futures import ThreadPoolExecutor

def use_submit():
    executor = ThreadPoolExecutor(max_workers=2)
    future = executor.submit(task, 10)
    return future.result()

def task(x):
    return x * 2
"""
        file_path = create_test_file(tmp_path, code, "submit.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        threading_patterns = output.results["threading"]
        # Should detect both ThreadPoolExecutor and submit
        assert len(threading_patterns) >= 1

    def test_threadpool_map(self, tmp_path, create_scanner):
        """Test ThreadPoolExecutor with map method."""
        code = """
from concurrent.futures import ThreadPoolExecutor

def use_map():
    executor = ThreadPoolExecutor(max_workers=3)
    results = executor.map(process_item, [1, 2, 3, 4, 5])
    return list(results)

def process_item(item):
    return item * 2
"""
        file_path = create_test_file(tmp_path, code, "map.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        threading_patterns = output.results["threading"]
        assert len(threading_patterns) >= 1

    def test_threadpool_context_manager(self, tmp_path, create_scanner):
        """Test ThreadPoolExecutor as context manager."""
        code = """
from concurrent.futures import ThreadPoolExecutor

def use_context_manager():
    with ThreadPoolExecutor(max_workers=4) as executor:
        future = executor.submit(task)
        return future.result()

def task():
    return 42
"""
        file_path = create_test_file(tmp_path, code, "context.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        threading_patterns = output.results["threading"]
        assert len(threading_patterns) >= 1


class TestThreadingInClass:
    """Test detection of threading patterns in class methods."""

    def test_thread_in_class_method(self, tmp_path, create_scanner):
        """Test Thread creation inside class method."""
        code = """
import threading

class ThreadManager:
    def create_thread(self):
        t = threading.Thread(target=self.worker)
        t.start()
    
    def worker(self):
        pass
"""
        file_path = create_test_file(tmp_path, code, "class_thread.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        threading_patterns = output.results["threading"]
        assert len(threading_patterns) >= 1

        # Check context capture
        for pattern_list in threading_patterns.values():
            if pattern_list:
                assert pattern_list[0].class_name == "ThreadManager"
                break
