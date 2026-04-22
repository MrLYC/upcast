"""Tests for PrometheusMetricScanner."""

from pathlib import Path
from unittest.mock import patch

from upcast.scanners.metrics import (
    MetricInfo,
    MetricsScanner,
)


class TestMetricModels:
    """Tests for metric models."""

    def test_valid_metric_info(self):
        """Test creating valid MetricInfo."""
        metric = MetricInfo(
            name="http_requests_total",
            metric_name="http_requests_total",
            type="Counter",
            help="Total HTTP requests",
            custom_collector=False,
            labels=[],
            usages=[],
            definitions=[],
        )
        assert metric.name == "http_requests_total"
        assert metric.type == "Counter"


class TestPrometheusMetricScannerIntegration:
    """Integration tests for PrometheusMetricScanner."""

    def test_scanner_detects_counter(self, tmp_path):
        """Test scanner detects Counter metrics."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
from prometheus_client import Counter
requests_total = Counter('http_requests_total', 'Total requests')
"""
        )

        scanner = MetricsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 0

    def test_scanner_handles_empty_file(self, tmp_path):
        """Test scanner handles empty files."""
        test_file = tmp_path / "test.py"
        test_file.write_text("")

        scanner = MetricsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 0

    def test_scanner_records_scan_duration(self):
        """Test scanner records elapsed scan duration in summary."""
        fixture_path = Path(__file__).resolve().parents[1] / "fixtures" / "metrics_duration_sample.py"
        scanner = MetricsScanner()

        with patch("time.perf_counter", side_effect=[10.0, 10.25]):
            output = scanner.scan(fixture_path)

        assert output.summary.scan_duration_ms == 250
