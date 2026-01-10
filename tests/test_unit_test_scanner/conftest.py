"""Pytest fixtures for unit test scanner tests."""

import pytest
from pathlib import Path

from upcast.scanners.unit_tests import UnitTestScanner


@pytest.fixture
def scanner():
    """Create a UnitTestScanner instance."""
    return UnitTestScanner(verbose=False)


@pytest.fixture
def simple_test_function():
    """Simple pytest test function."""
    return """
def test_addition():
    assert 1 + 1 == 2
"""


@pytest.fixture
def test_class_fixture():
    """Pytest test class."""
    return """
class TestMath:
    def test_addition(self):
        assert 1 + 1 == 2
    
    def test_subtraction(self):
        assert 2 - 1 == 1
"""


@pytest.fixture
def unittest_fixture():
    """Unittest TestCase."""
    return """
import unittest

class TestMath(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)
    
    def test_subtraction(self):
        self.assertEqual(2 - 1, 1)
"""


@pytest.fixture
def test_with_imports():
    """Test with imports."""
    return """
from myapp.math_utils import add, subtract

def test_add_function():
    result = add(1, 2)
    assert result == 3

def test_subtract_function():
    result = subtract(5, 3)
    assert result == 2
"""


@pytest.fixture
def test_with_multiple_assertions():
    """Test with multiple assertions."""
    return """
def test_multiple_checks():
    assert 1 + 1 == 2
    assert 2 + 2 == 4
    assert 3 + 3 == 6
"""
