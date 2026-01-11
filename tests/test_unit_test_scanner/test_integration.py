"""Integration tests for unit test scanner."""

import pytest
from pathlib import Path

from upcast.scanners.unit_tests import UnitTestScanner
from upcast.models.unit_tests import UnitTestOutput


class TestScannerInstantiation:
    """Test scanner instantiation."""

    def test_scanner_instantiation(self, scanner):
        """Test scanner can be instantiated."""
        assert scanner is not None
        assert isinstance(scanner, UnitTestScanner)

    def test_scanner_default_patterns(self):
        """Test default file patterns."""
        scanner = UnitTestScanner()
        assert "**/test_*.py" in scanner.include_patterns
        assert "**/*_test.py" in scanner.include_patterns


class TestBasicScanning:
    """Test basic scanning functionality."""

    def test_scan_empty_file(self, tmp_path, scanner):
        """Test scanning empty file."""
        file_path = tmp_path / "test_empty.py"
        file_path.write_text("")

        output = scanner.scan(file_path)

        assert isinstance(output, UnitTestOutput)
        assert output.summary.total_tests == 0

    def test_scan_simple_pytest_test(self, tmp_path, scanner, simple_test_function):
        """Test scanning simple pytest test."""
        file_path = tmp_path / "test_math.py"
        file_path.write_text(simple_test_function)

        output = scanner.scan(file_path)

        assert output.summary.total_tests == 1
        assert len(output.results) == 1
        test = list(output.results.values())[0][0]
        assert test.name == "test_addition"
        assert test.assert_count == 1

    def test_scan_pytest_test_class(self, tmp_path, scanner, test_class_fixture):
        """Test scanning pytest test class."""
        file_path = tmp_path / "test_math.py"
        file_path.write_text(test_class_fixture)

        output = scanner.scan(file_path)

        assert output.summary.total_tests == 2

    def test_scan_unittest_test(self, tmp_path, scanner, unittest_fixture):
        """Test scanning unittest TestCase."""
        file_path = tmp_path / "test_math.py"
        file_path.write_text(unittest_fixture)

        output = scanner.scan(file_path)

        assert output.summary.total_tests == 2

    def test_scan_test_with_imports(self, tmp_path, scanner, test_with_imports):
        """Test scanning test with imports."""
        file_path = tmp_path / "test_math.py"
        file_path.write_text(test_with_imports)

        output = scanner.scan(file_path)

        assert output.summary.total_tests == 2
        test = list(output.results.values())[0][0]
        assert len(test.targets) > 0

    def test_scan_multiple_assertions(self, tmp_path, scanner, test_with_multiple_assertions):
        """Test scanning test with multiple assertions."""
        file_path = tmp_path / "test_checks.py"
        file_path.write_text(test_with_multiple_assertions)

        output = scanner.scan(file_path)

        test = list(output.results.values())[0][0]
        assert test.assert_count == 3

    def test_scan_directory(self, tmp_path, scanner):
        """Test scanning directory with multiple test files."""
        file1 = tmp_path / "test_one.py"
        file1.write_text("def test_a(): assert True")

        file2 = tmp_path / "test_two.py"
        file2.write_text("def test_b(): assert True")

        output = scanner.scan(tmp_path)

        assert output.summary.total_tests == 2
        assert output.summary.total_files == 2

    def test_body_md5_calculation(self, tmp_path, scanner):
        """Test that body MD5 is calculated."""
        file_path = tmp_path / "test_hash.py"
        file_path.write_text("def test_example(): assert True")

        output = scanner.scan(file_path)

        test = list(output.results.values())[0][0]
        assert test.body_md5 is not None
        assert len(test.body_md5) == 32  # MD5 hex string

    def test_line_range_tracking(self, tmp_path, scanner):
        """Test line range tracking."""
        code = """
def test_first():
    assert 1 == 1

def test_second():
    assert 2 == 2
"""
        file_path = tmp_path / "test_lines.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        tests = list(output.results.values())[0]
        assert tests[0].line_range[0] < tests[0].line_range[1]

    def test_skip_non_test_functions(self, tmp_path, scanner):
        """Test that non-test functions are skipped."""
        code = """
def helper_function():
    return 42

def test_real_test():
    assert helper_function() == 42
"""
        file_path = tmp_path / "test_skip.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_tests == 1

    def test_skip_nested_test_functions(self, tmp_path, scanner):
        """Test that nested test functions are skipped."""
        code = """
def outer_function():
    def test_nested():
        assert True
    test_nested()

def test_valid():
    assert True
"""
        file_path = tmp_path / "test_nested.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_tests == 1

    def test_summary_statistics(self, tmp_path, scanner):
        """Test summary statistics calculation."""
        code = """
def test_one():
    assert True

def test_two():
    assert True
    assert True
"""
        file_path = tmp_path / "test_stats.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_tests == 2
        assert output.summary.total_assertions == 3
        assert output.summary.scan_duration_ms >= 0

    def test_pytest_raises_counted(self, tmp_path, scanner):
        """Test that pytest.raises is counted as assertion."""
        code = """
import pytest

def test_exception():
    with pytest.raises(ValueError):
        raise ValueError("test")
"""
        file_path = tmp_path / "test_raises.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        test = list(output.results.values())[0][0]
        assert test.assert_count >= 1

    def test_root_modules_filtering(self, tmp_path):
        """Test root_modules filtering."""
        scanner = UnitTestScanner(root_modules=["myapp"])

        code = """
from myapp.models import User
from other.lib import Helper

def test_user():
    user = User()
    helper = Helper()
    assert user is not None
"""
        file_path = tmp_path / "test_filter.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        test = list(output.results.values())[0][0]
        # Should only include myapp targets
        target_modules = [t.module_path for t in test.targets]
        assert all("myapp" in m for m in target_modules)
