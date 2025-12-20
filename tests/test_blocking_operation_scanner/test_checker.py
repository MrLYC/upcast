"""Tests for checker module."""

import pytest

from upcast.blocking_operation_scanner.checker import BlockingOperationChecker
from upcast.blocking_operation_scanner.operation_parser import OperationType


@pytest.fixture
def checker():
    """Create a checker instance."""
    return BlockingOperationChecker()


@pytest.fixture
def sample_file(tmp_path):
    """Create a sample Python file with blocking operations."""
    file_path = tmp_path / "test_file.py"
    file_path.write_text(
        """
import time
import threading
import subprocess

def test_func():
    time.sleep(5)
    threading.Lock().acquire()
    subprocess.run(['ls'])
"""
    )
    return file_path


def test_check_file(checker, sample_file):
    """Test checking a file for blocking operations."""
    operations = checker.check_file(sample_file)

    assert len(operations) == 3
    types = {op.type for op in operations}
    assert OperationType.TIME_SLEEP in types
    assert OperationType.LOCK_ACQUIRE in types
    assert OperationType.SUBPROCESS_RUN in types


def test_check_file_with_sleep(checker, tmp_path):
    """Test detecting sleep operations."""
    file_path = tmp_path / "test.py"
    file_path.write_text(
        """
import time

def func():
    time.sleep(10)
"""
    )

    operations = checker.check_file(file_path)

    assert len(operations) == 1
    assert operations[0].type == OperationType.TIME_SLEEP
    assert operations[0].duration == 10
    assert operations[0].function == "func"


def test_check_file_async_context(checker, tmp_path):
    """Test detecting operations in async context."""
    file_path = tmp_path / "test.py"
    file_path.write_text(
        """
import time

async def async_func():
    time.sleep(1)
"""
    )

    operations = checker.check_file(file_path)

    assert len(operations) == 1
    assert operations[0].is_async_context is True


def test_check_file_with_locks(checker, tmp_path):
    """Test detecting lock operations."""
    file_path = tmp_path / "test.py"
    file_path.write_text(
        """
import threading

def func():
    threading.Lock().acquire(timeout=5)

    with threading.RLock():
        pass
"""
    )

    operations = checker.check_file(file_path)

    assert len(operations) == 2
    assert any(op.type == OperationType.LOCK_ACQUIRE for op in operations)
    assert any(op.type == OperationType.LOCK_CONTEXT for op in operations)


def test_check_file_with_subprocess(checker, tmp_path):
    """Test detecting subprocess operations."""
    file_path = tmp_path / "test.py"
    file_path.write_text(
        """
import subprocess
from subprocess import Popen

def func():
    subprocess.run(['ls'], timeout=30)
    proc = Popen(['echo'])
    proc.wait()
    proc.communicate()
"""
    )

    operations = checker.check_file(file_path)

    assert len(operations) == 3
    types = {op.type for op in operations}
    assert OperationType.SUBPROCESS_RUN in types
    assert OperationType.SUBPROCESS_WAIT in types
    assert OperationType.SUBPROCESS_COMMUNICATE in types


def test_check_file_with_django_locks(checker, tmp_path):
    """Test detecting Django select_for_update operations."""
    file_path = tmp_path / "test.py"
    file_path.write_text(
        """
def func():
    users = User.objects.filter(active=True).select_for_update(timeout=30).all()
"""
    )

    operations = checker.check_file(file_path)

    assert len(operations) == 1
    assert operations[0].type == OperationType.DB_SELECT_FOR_UPDATE
    assert operations[0].timeout == 30


def test_check_file_invalid_syntax(checker, tmp_path):
    """Test handling files with invalid syntax."""
    file_path = tmp_path / "test.py"
    file_path.write_text("def func( invalid syntax")

    operations = checker.check_file(file_path)

    assert operations == []


def test_check_file_class_methods(checker, tmp_path):
    """Test detecting operations in class methods."""
    file_path = tmp_path / "test.py"
    file_path.write_text(
        """
import time

class MyClass:
    def method(self):
        time.sleep(2)
"""
    )

    operations = checker.check_file(file_path)

    assert len(operations) == 1
    assert operations[0].function == "method"
    assert operations[0].class_name == "MyClass"
