"""Integration tests for unit test scanner."""

from pathlib import Path

from upcast.unit_test_scanner.checker import check_file
from upcast.unit_test_scanner.cli import scan_unit_tests


class TestIntegration:
    """Integration tests."""

    def test_scan_fixtures_directory(self):
        """Test scanning the fixtures directory."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        pytest_file = fixtures_dir / "sample_pytest_tests.py"

        # Use check_file directly since CLI filters by filename pattern
        tests = check_file(pytest_file, ["app"])

        # Should find tests from pytest file
        assert len(tests) == 3

        # Check test names
        test_names = [t.name for t in tests]
        assert "test_add_and_even" in test_names
        assert "test_add" in test_names
        assert "test_exceptions" in test_names

    def test_scan_with_output_file(self, tmp_path):
        """Test scanning with output file using CLI."""
        fixtures_dir = Path(__file__).parent / "fixtures"

        # Rename fixture to test_ pattern temporarily for CLI
        pytest_file = fixtures_dir / "sample_pytest_tests.py"
        test_file = fixtures_dir / "test_sample.py"

        # Copy fixture to test_ filename
        test_file.write_text(pytest_file.read_text())

        try:
            output_file = tmp_path / "results.yaml"

            _ = scan_unit_tests(
                path=str(test_file),
                root_modules=["app"],
                output=str(output_file),
                verbose=False,
            )
        finally:
            # Clean up temporary file
            if test_file.exists():
                test_file.unlink()

        assert output_file.exists()
        content = output_file.read_text()
        assert "test_add_and_even" in content
        assert "body_md5:" in content
        assert "assert_count:" in content

    def test_scan_with_json_format(self, tmp_path):
        """Test scanning with JSON output using CLI."""
        fixtures_dir = Path(__file__).parent / "fixtures"

        # Rename fixture to test_ pattern temporarily for CLI
        pytest_file = fixtures_dir / "sample_pytest_tests.py"
        test_file = fixtures_dir / "test_sample.py"

        # Copy fixture to test_ filename
        test_file.write_text(pytest_file.read_text())

        try:
            output_file = tmp_path / "results.json"

            _ = scan_unit_tests(
                path=str(test_file),
                root_modules=["app"],
                output=str(output_file),
                output_format="json",
                verbose=False,
            )
        finally:
            # Clean up temporary file
            if test_file.exists():
                test_file.unlink()

        assert output_file.exists()
        content = output_file.read_text()
        assert '"test_add_and_even"' in content

    def test_example_from_product_context(self):
        """Test with the exact example from product context."""
        # Create a temporary test file matching the product context example
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            # Create app module structure
            app_dir = tmpdir_path / "app"
            app_dir.mkdir()
            (app_dir / "__init__.py").write_text("")

            # Create math_utils module
            (app_dir / "math_utils.py").write_text("""
def add(a, b):
    return a + b

def is_even(n):
    return n % 2 == 0
""")

            # Create test file
            tests_dir = tmpdir_path / "tests"
            tests_dir.mkdir()
            (tests_dir / "__init__.py").write_text("")

            test_file = tests_dir / "test_math_utils.py"
            test_file.write_text("""
import pytest
from app.math_utils import add, is_even


def test_add_and_even():
    \"\"\"
    测试 add 和 is_even 的基本行为
    \"\"\"

    result = add(2, 3)
    assert result == 5

    assert is_even(result) is False
    assert is_even(4) is True
""")

            # Scan the tests
            tests = scan_unit_tests(
                path=str(tests_dir),
                root_modules=["app"],
                verbose=False,
            )

            assert len(tests) == 1
            test = tests[0]

            assert test.name == "test_add_and_even"
            assert len(test.body_md5) == 32
            assert test.assert_count == 3

            # Check targets
            assert len(test.targets) == 1
            assert test.targets[0].module == "app.math_utils"
            assert "add" in test.targets[0].symbols
            assert "is_even" in test.targets[0].symbols

    def test_multiple_root_modules(self):
        """Test with multiple root modules."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        pytest_file = fixtures_dir / "sample_pytest_tests.py"

        # Use check_file directly since CLI filters by filename pattern
        tests = check_file(pytest_file, ["app", "mylib"])

        assert len(tests) >= 3
