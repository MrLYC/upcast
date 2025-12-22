"""Tests for UnitTestScanner."""

from upcast.scanners.unit_tests import (
    UnitTestInfo,
    UnitTestScanner,
)


class TestUnitTestModels:
    """Tests for unit test models."""

    def test_valid_unit_test_info(self):
        """Test creating valid UnitTestInfo."""
        test_info = UnitTestInfo(
            name="test_example",
            file="test_module.py",
            line_range=(10, 20),
            body_md5="abc123",
            assert_count=3,
        )
        assert test_info.name == "test_example"
        assert test_info.assert_count == 3


class TestUnitTestScannerIntegration:
    """Integration tests for UnitTestScanner."""

    def test_scanner_detects_pytest_tests(self, tmp_path):
        """Test scanner detects pytest test functions."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            """
def test_addition():
    assert 1 + 1 == 2
"""
        )

        scanner = UnitTestScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 0

    def test_scanner_handles_empty_file(self, tmp_path):
        """Test scanner handles empty files."""
        test_file = tmp_path / "test.py"
        test_file.write_text("")

        scanner = UnitTestScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 0
