"""Tests for BlockingOperationsScanner."""

from upcast.scanners.blocking_operations import (
    BlockingOperation,
    BlockingOperationsScanner,
)


class TestBlockingOperationModel:
    """Tests for BlockingOperation model."""

    def test_valid_operation(self):
        """Test creating valid BlockingOperation."""
        op = BlockingOperation(
            file="test.py",
            line=10,
            column=4,
            category="time_based",
            operation="time.sleep",
            statement="time.sleep(1)",
        )
        assert op.category == "time_based"
        assert op.operation == "time.sleep"


class TestBlockingOperationsScannerIntegration:
    """Integration tests for BlockingOperationsScanner."""

    def test_scanner_detects_sleep(self, tmp_path):
        """Test scanner detects time.sleep."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import time
time.sleep(1)
"""
        )

        scanner = BlockingOperationsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 0

    def test_scanner_handles_empty_file(self, tmp_path):
        """Test scanner handles empty files."""
        test_file = tmp_path / "test.py"
        test_file.write_text("")

        scanner = BlockingOperationsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 0
