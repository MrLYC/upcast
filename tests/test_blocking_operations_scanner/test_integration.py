"""Integration tests for blocking operations scanner."""

import pytest
from pathlib import Path

from upcast.scanners.blocking_operations import BlockingOperationsScanner
from upcast.models.blocking_operations import BlockingOperationsOutput
from tests.fixtures.test_utils import create_test_file


class TestScannerInstantiation:
    """Test scanner instantiation and basic functionality."""

    def test_scanner_instantiation(self, scanner_kwargs):
        """Test that scanner can be instantiated."""
        scanner = BlockingOperationsScanner(**scanner_kwargs)
        assert scanner is not None
        assert isinstance(scanner, BlockingOperationsScanner)

    def test_scanner_has_blocking_patterns(self):
        """Test that scanner has defined blocking patterns."""
        assert hasattr(BlockingOperationsScanner, "BLOCKING_PATTERNS")
        patterns = BlockingOperationsScanner.BLOCKING_PATTERNS

        # Check all expected categories exist
        assert "time_based" in patterns
        assert "database" in patterns
        assert "synchronization" in patterns
        assert "subprocess" in patterns

        # Check patterns are non-empty
        assert len(patterns["time_based"]) > 0
        assert len(patterns["database"]) > 0
        assert len(patterns["synchronization"]) > 0
        assert len(patterns["subprocess"]) > 0


class TestBasicScanning:
    """Test basic scanning functionality."""

    def test_scan_empty_file(self, tmp_path, create_scanner):
        """Test scanning an empty file."""
        file_path = create_test_file(tmp_path, "", "empty.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert isinstance(output, BlockingOperationsOutput)
        assert output.summary.total_count == 0
        assert all(len(ops) == 0 for ops in output.results.values())

    def test_scan_file_without_blocking_ops(self, tmp_path, create_scanner):
        """Test scanning a file without blocking operations."""
        code = """
def pure_function():
    x = 1 + 2
    return x * 3

class PureClass:
    def compute(self):
        return 42
"""
        file_path = create_test_file(tmp_path, code, "pure.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert output.summary.total_count == 0
        assert all(len(ops) == 0 for ops in output.results.values())

    def test_scan_single_blocking_operation(self, tmp_path, create_scanner):
        """Test scanning a file with a single blocking operation."""
        code = """
import time

def delayed():
    time.sleep(1)
"""
        file_path = create_test_file(tmp_path, code, "delayed.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert output.summary.total_count == 1
        assert len(output.results["time_based"]) == 1
        assert output.results["time_based"][0].operation == "time.sleep"
        assert output.results["time_based"][0].function == "delayed"

    def test_scan_directory(self, tmp_path, create_scanner):
        """Test scanning a directory with multiple files."""
        # Create multiple files
        file1 = tmp_path / "file1.py"
        file1.write_text("import time\ndef f1(): time.sleep(1)")

        file2 = tmp_path / "file2.py"
        file2.write_text("import subprocess\ndef f2(): subprocess.run(['ls'])")

        scanner = create_scanner(BlockingOperationsScanner)
        output = scanner.scan(tmp_path)

        assert output.summary.total_count == 2
        assert output.summary.files_scanned == 2
        assert len(output.results["time_based"]) == 1
        assert len(output.results["subprocess"]) == 1


class TestCategoryDetection:
    """Test detection of different blocking operation categories."""

    def test_detect_time_based_operations(self, tmp_path, create_scanner):
        """Test detection of time-based blocking operations."""
        code = """
import time
import asyncio

def delays():
    time.sleep(1)
    asyncio.sleep(2)
"""
        file_path = create_test_file(tmp_path, code, "time_ops.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert len(output.results["time_based"]) == 2
        operations = [op.operation for op in output.results["time_based"]]
        assert "time.sleep" in operations
        assert "asyncio.sleep" in operations

    def test_detect_synchronization_operations(self, tmp_path, create_scanner):
        """Test detection of synchronization primitives."""
        code = """
import threading

def use_locks():
    lock = threading.Lock()
    rlock = threading.RLock()
    sem = threading.Semaphore()
"""
        file_path = create_test_file(tmp_path, code, "sync_ops.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert len(output.results["synchronization"]) >= 2
        operations = [op.operation for op in output.results["synchronization"]]
        assert any("Lock" in op for op in operations)

    def test_detect_subprocess_operations(self, tmp_path, create_scanner):
        """Test detection of subprocess operations."""
        code = """
import subprocess
import os

def run_commands():
    subprocess.run(['ls'])
    subprocess.call(['echo', 'test'])
    os.system('pwd')
"""
        file_path = create_test_file(tmp_path, code, "subprocess_ops.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert len(output.results["subprocess"]) == 3
        operations = [op.operation for op in output.results["subprocess"]]
        assert "subprocess.run" in operations
        assert "subprocess.call" in operations
        assert "os.system" in operations

    def test_detect_database_operations(self, tmp_path, create_scanner):
        """Test detection of database blocking operations."""
        code = """
def lock_row(queryset):
    queryset.select_for_update()
"""
        file_path = create_test_file(tmp_path, code, "db_ops.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert len(output.results["database"]) == 1
        # Scanner returns the full qualified name
        assert "select_for_update" in output.results["database"][0].operation


class TestContextCapture:
    """Test that scanner captures proper context information."""

    def test_capture_function_context(self, tmp_path, create_scanner):
        """Test that scanner captures containing function name."""
        code = """
import time

def my_function():
    time.sleep(1)
"""
        file_path = create_test_file(tmp_path, code, "func_context.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert len(output.results["time_based"]) == 1
        assert output.results["time_based"][0].function == "my_function"

    def test_capture_class_context(self, tmp_path, create_scanner):
        """Test that scanner captures containing class name."""
        code = """
import time

class MyClass:
    def method(self):
        time.sleep(1)
"""
        file_path = create_test_file(tmp_path, code, "class_context.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert len(output.results["time_based"]) == 1
        assert output.results["time_based"][0].class_name == "MyClass"
        assert output.results["time_based"][0].function == "method"

    def test_capture_module_level_operation(self, tmp_path, create_scanner):
        """Test that scanner handles module-level operations."""
        code = """
import time

# Module-level operation
time.sleep(1)
"""
        file_path = create_test_file(tmp_path, code, "module_level.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert len(output.results["time_based"]) == 1
        assert output.results["time_based"][0].function is None
        assert output.results["time_based"][0].class_name is None


class TestSummaryGeneration:
    """Test that summary statistics are correctly generated."""

    def test_summary_has_correct_total_count(self, tmp_path, create_scanner):
        """Test that summary total_count matches actual operations."""
        code = """
import time
import subprocess

def multiple_ops():
    time.sleep(1)
    time.sleep(2)
    subprocess.run(['ls'])
"""
        file_path = create_test_file(tmp_path, code, "multi_ops.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        # Count operations in results
        total_in_results = sum(len(ops) for ops in output.results.values())

        assert output.summary.total_count == total_in_results
        assert output.summary.total_count == 3

    def test_summary_by_category_matches_results(self, tmp_path, create_scanner):
        """Test that summary by_category matches actual results."""
        code = """
import time
import threading
import subprocess

def various_ops():
    time.sleep(1)
    time.sleep(2)
    lock = threading.Lock()
    subprocess.run(['ls'])
"""
        file_path = create_test_file(tmp_path, code, "various.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        # Verify by_category matches actual results
        for category, count in output.summary.by_category.items():
            assert count == len(output.results[category])

        # Check specific counts
        assert output.summary.by_category.get("time_based", 0) == 2
        assert output.summary.by_category.get("synchronization", 0) >= 1
        assert output.summary.by_category.get("subprocess", 0) == 1

    def test_summary_scan_duration_is_set(self, tmp_path, create_scanner):
        """Test that scan duration is measured and set."""
        code = """
import time

def test_func():
    time.sleep(1)
"""
        file_path = create_test_file(tmp_path, code, "duration_test.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert output.summary.scan_duration_ms >= 0
        assert isinstance(output.summary.scan_duration_ms, int)


class TestAliasedImports:
    """Test detection with aliased imports."""

    def test_detect_aliased_time_sleep(self, tmp_path, create_scanner):
        """Test detection of time.sleep with import alias."""
        code = """
from time import sleep as tsleep

def delayed():
    tsleep(1)
"""
        file_path = create_test_file(tmp_path, code, "aliased.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert len(output.results["time_based"]) == 1
        # Should detect it regardless of alias
        assert output.results["time_based"][0].category == "time_based"

    def test_detect_module_alias(self, tmp_path, create_scanner):
        """Test detection with module alias."""
        code = """
import time as t

def delayed():
    t.sleep(1)
"""
        file_path = create_test_file(tmp_path, code, "module_alias.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert len(output.results["time_based"]) == 1
        assert "sleep" in output.results["time_based"][0].operation


class TestWithStatements:
    """Test detection of blocking operations in with statements."""

    def test_detect_lock_context_manager(self, tmp_path, create_scanner):
        """Test detection of lock used as context manager."""
        code = """
import threading

def use_lock():
    lock = threading.Lock()
    with lock:
        pass
"""
        file_path = create_test_file(tmp_path, code, "with_lock.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        # Should detect both Lock() instantiation and with statement
        assert len(output.results["synchronization"]) >= 1
        operations = [op.operation for op in output.results["synchronization"]]
        # At least one should be detected
        assert any("Lock" in op for op in operations)
