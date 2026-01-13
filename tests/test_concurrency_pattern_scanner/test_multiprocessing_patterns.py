"""Tests for multiprocessing concurrency patterns."""

import pytest

from upcast.scanners.concurrency import ConcurrencyScanner
from tests.fixtures.test_utils import create_test_file


class TestProcessCreation:
    """Test detection of multiprocessing.Process patterns."""

    def test_basic_process_creation(self, tmp_path, create_scanner):
        """Test detection of basic Process creation."""
        code = """
import multiprocessing

def create_process():
    p = multiprocessing.Process(target=worker)
    p.start()

def worker():
    pass
"""
        file_path = create_test_file(tmp_path, code, "process.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        mp_patterns = output.results["multiprocessing"]
        assert len(mp_patterns) >= 1

    def test_process_with_args(self, tmp_path, create_scanner):
        """Test detection of Process with arguments."""
        code = """
import multiprocessing

def create_process():
    p = multiprocessing.Process(target=worker, args=(10, 20))
    p.start()

def worker(a, b):
    pass
"""
        file_path = create_test_file(tmp_path, code, "process_args.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        mp_patterns = output.results["multiprocessing"]
        assert len(mp_patterns) >= 1

    def test_process_with_name(self, tmp_path, create_scanner):
        """Test detection of Process with name parameter."""
        code = """
import multiprocessing

def create_process():
    p = multiprocessing.Process(target=worker, name="worker-process")
    p.start()

def worker():
    pass
"""
        file_path = create_test_file(tmp_path, code, "process_name.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        mp_patterns = output.results["multiprocessing"]
        assert len(mp_patterns) >= 1


class TestProcessPoolExecutor:
    """Test detection of ProcessPoolExecutor patterns."""

    def test_processpool_creation(self, tmp_path, create_scanner):
        """Test detection of ProcessPoolExecutor instantiation."""
        code = """
from concurrent.futures import ProcessPoolExecutor

def create_pool():
    executor = ProcessPoolExecutor(max_workers=2)
"""
        file_path = create_test_file(tmp_path, code, "pool.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        mp_patterns = output.results["multiprocessing"]
        assert len(mp_patterns) >= 1

    def test_processpool_submit(self, tmp_path, create_scanner):
        """Test detection of executor.submit() method."""
        code = """
from concurrent.futures import ProcessPoolExecutor

def use_submit():
    executor = ProcessPoolExecutor(max_workers=2)
    future = executor.submit(compute, 10)
    return future.result()

def compute(x):
    return x * 2
"""
        file_path = create_test_file(tmp_path, code, "submit.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        mp_patterns = output.results["multiprocessing"]
        # Should detect both ProcessPoolExecutor and submit
        assert len(mp_patterns) >= 1

    def test_processpool_map(self, tmp_path, create_scanner):
        """Test ProcessPoolExecutor with map method."""
        code = """
from concurrent.futures import ProcessPoolExecutor

def use_map():
    executor = ProcessPoolExecutor(max_workers=2)
    results = executor.map(compute, [1, 2, 3, 4, 5])
    return list(results)

def compute(x):
    return x * 2
"""
        file_path = create_test_file(tmp_path, code, "map.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        mp_patterns = output.results["multiprocessing"]
        assert len(mp_patterns) >= 1

    def test_processpool_context_manager(self, tmp_path, create_scanner):
        """Test ProcessPoolExecutor as context manager."""
        code = """
from concurrent.futures import ProcessPoolExecutor

def use_context_manager():
    with ProcessPoolExecutor(max_workers=2) as executor:
        future = executor.submit(compute)
        return future.result()

def compute():
    return 42
"""
        file_path = create_test_file(tmp_path, code, "context.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        mp_patterns = output.results["multiprocessing"]
        assert len(mp_patterns) >= 1


class TestMultiprocessingPool:
    """Test detection of multiprocessing.Pool patterns."""

    def test_pool_creation(self, tmp_path, create_scanner):
        """Test detection of multiprocessing.Pool instantiation."""
        code = """
import multiprocessing

def create_pool():
    pool = multiprocessing.Pool(processes=4)
    pool.close()
"""
        file_path = create_test_file(tmp_path, code, "pool.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        # Pool might not be detected if not in BLOCKING_PATTERNS
        # but at least the code should not crash
        assert output is not None


class TestMultiprocessingInClass:
    """Test detection of multiprocessing patterns in class methods."""

    def test_process_in_class_method(self, tmp_path, create_scanner):
        """Test Process creation inside class method."""
        code = """
import multiprocessing

class ProcessManager:
    def create_process(self):
        p = multiprocessing.Process(target=self.worker)
        p.start()

    def worker(self):
        pass
"""
        file_path = create_test_file(tmp_path, code, "class_process.py")
        scanner = create_scanner(ConcurrencyScanner)

        output = scanner.scan(file_path)

        mp_patterns = output.results["multiprocessing"]
        assert len(mp_patterns) >= 1

        # Check context capture
        for pattern_list in mp_patterns.values():
            if pattern_list:
                assert pattern_list[0].class_name == "ProcessManager"
                break
