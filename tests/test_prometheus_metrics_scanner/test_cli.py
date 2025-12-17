"""Tests for CLI functions."""

import tempfile
from pathlib import Path

import pytest

from upcast.prometheus_metrics_scanner.cli import scan_prometheus_metrics


@pytest.fixture
def fixtures_dir():
    """Get fixtures directory path."""
    return Path(__file__).parent / "fixtures"


class TestScanPrometheusMetrics:
    """Test scan_prometheus_metrics function."""

    def test_scan_directory(self, fixtures_dir):
        """Test scanning a directory."""
        result = scan_prometheus_metrics(str(fixtures_dir))

        assert isinstance(result, str)
        assert len(result) > 0
        # Should contain some metric names
        assert "http_requests_total" in result

    def test_scan_single_file(self, fixtures_dir):
        """Test scanning a single file."""
        file_path = fixtures_dir / "simple_metrics.py"
        result = scan_prometheus_metrics(str(file_path))

        assert isinstance(result, str)
        assert "http_requests_total" in result

    def test_output_to_file(self, fixtures_dir):
        """Test outputting to a file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.yaml"
            result = scan_prometheus_metrics(str(fixtures_dir), output=str(output_path))

            # Should return empty string when writing to file
            assert result == ""
            # File should exist
            assert output_path.exists()
            # File should contain metrics
            content = output_path.read_text()
            assert "http_requests_total" in content

    def test_nonexistent_path(self):
        """Test error handling for nonexistent path."""
        with pytest.raises(FileNotFoundError):
            scan_prometheus_metrics("/nonexistent/path")

    def test_verbose_mode(self, fixtures_dir, capsys):
        """Test verbose mode output."""
        scan_prometheus_metrics(str(fixtures_dir), verbose=True)

        captured = capsys.readouterr()
        # Should print scanning messages to stderr
        assert "Scanning" in captured.err or "Found" in captured.err

    def test_empty_directory(self):
        """Test scanning an empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = scan_prometheus_metrics(tmpdir)
            # Should return empty string or minimal YAML
            assert isinstance(result, str)
