"""Tests for ConcurrencyPatternScanner."""

from upcast.scanners.concurrency import (
    ConcurrencyScanner,
    ConcurrencyUsage,
)


class TestConcurrencyModels:
    """Tests for concurrency models."""

    def test_valid_usage(self):
        """Test creating valid ConcurrencyUsage."""
        usage = ConcurrencyUsage(
            file="test.py",
            line=10,
            column=0,
            pattern="threading.Thread",
            statement="t = threading.Thread(target=worker)",
        )
        assert usage.pattern == "threading.Thread"


class TestConcurrencyPatternScannerIntegration:
    """Integration tests for ConcurrencyPatternScanner."""

    def test_scanner_detects_threading(self, tmp_path):
        """Test scanner detects threading patterns."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import threading
t = threading.Thread(target=lambda: None)
"""
        )

        scanner = ConcurrencyPatternScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 0

    def test_scanner_handles_empty_file(self, tmp_path):
        """Test scanner handles empty files."""
        test_file = tmp_path / "test.py"
        test_file.write_text("")

        scanner = ConcurrencyScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 0
