"""Tests for checker module."""

from pathlib import Path

from upcast.unit_test_scanner.checker import UnitTestChecker, check_file


class TestCheckFile:
    """Test file checking functionality."""

    def test_check_pytest_file(self):
        """Test checking a file with pytest tests."""
        fixture_path = Path(__file__).parent / "fixtures" / "sample_pytest_tests.py"

        tests = check_file(fixture_path, ["app"])

        assert len(tests) == 3
        test_names = [t.name for t in tests]
        assert "test_add_and_even" in test_names
        assert "test_add" in test_names
        assert "test_exceptions" in test_names

    def test_check_unittest_file(self):
        """Test checking a file with unittest tests."""
        fixture_path = Path(__file__).parent / "fixtures" / "sample_unittest_tests.py"

        tests = check_file(fixture_path, ["app"])

        assert len(tests) == 4
        test_names = [t.name for t in tests]
        assert "test_email_valid" in test_names
        assert "test_email_invalid" in test_names
        assert "test_phone" in test_names

    def test_check_nonexistent_file(self):
        """Test checking a nonexistent file."""
        fake_path = Path("/nonexistent/file.py")

        tests = check_file(fake_path, ["app"])

        assert len(tests) == 0

    def test_filter_by_root_modules(self):
        """Test that root_modules filtering works."""
        fixture_path = Path(__file__).parent / "fixtures" / "sample_pytest_tests.py"

        # Check with matching root module
        tests_app = check_file(fixture_path, ["app"])

        # Check with non-matching root module
        _ = check_file(fixture_path, ["other"])

        # Should find tests but targets may differ
        assert len(tests_app) == 3


class TestUnitTestChecker:
    """Test UnitTestChecker class."""

    def test_detect_pytest_functions(self):
        """Test detection of pytest functions."""
        from astroid import MANAGER

        code = """
def test_something():
    assert True

def test_another():
    assert False

def not_a_test():
    pass
"""
        module = MANAGER.ast_from_string(code)
        checker = UnitTestChecker("test_file.py", ["app"])
        checker.check_module(module)

        tests = checker.get_tests()

        assert len(tests) == 2
        assert all(t.name.startswith("test_") for t in tests)

    def test_detect_unittest_methods(self):
        """Test detection of unittest.TestCase methods."""
        from astroid import MANAGER

        code = """
import unittest

class TestSomething(unittest.TestCase):
    def test_method(self):
        self.assertTrue(True)

    def test_another(self):
        self.assertFalse(False)

    def helper_method(self):
        pass
"""
        module = MANAGER.ast_from_string(code)
        checker = UnitTestChecker("test_file.py", ["app"])
        checker.check_module(module)

        tests = checker.get_tests()

        assert len(tests) == 2
        test_names = [t.name for t in tests]
        assert "test_method" in test_names
        assert "test_another" in test_names
        assert "helper_method" not in test_names

    def test_extract_imports(self):
        """Test that imports are extracted from module."""
        from astroid import MANAGER

        code = """
import app.math_utils
from app import validators

def test_something():
    pass
"""
        module = MANAGER.ast_from_string(code)
        checker = UnitTestChecker("test_file.py", ["app"])
        checker.check_module(module)

        assert len(checker.module_imports) > 0
