"""Integration tests for metrics scanner."""

import pytest
from pathlib import Path

from upcast.scanners.metrics import MetricsScanner
from upcast.models.metrics import PrometheusMetricOutput


class TestScannerInstantiation:
    """Test scanner instantiation and basic functionality."""

    def test_scanner_instantiation(self, scanner):
        """Test that scanner can be instantiated."""
        assert scanner is not None
        assert isinstance(scanner, MetricsScanner)

    def test_scanner_has_metric_types(self):
        """Test that scanner has defined metric types."""
        assert hasattr(MetricsScanner, "METRIC_TYPES")
        assert "Counter" in MetricsScanner.METRIC_TYPES
        assert "Gauge" in MetricsScanner.METRIC_TYPES
        assert "Histogram" in MetricsScanner.METRIC_TYPES
        assert "Summary" in MetricsScanner.METRIC_TYPES

    def test_scanner_verbose_mode(self):
        """Test scanner with verbose mode."""
        scanner = MetricsScanner(verbose=True)
        assert scanner.verbose is True


class TestBasicScanning:
    """Test basic scanning functionality."""

    def test_scan_empty_file(self, tmp_path, scanner):
        """Test scanning an empty file."""
        file_path = tmp_path / "metrics.py"
        file_path.write_text("")

        output = scanner.scan(file_path)

        assert isinstance(output, PrometheusMetricOutput)
        assert output.summary.total_metrics == 0
        assert len(output.results) == 0

    def test_scan_file_without_metrics(self, tmp_path, scanner):
        """Test scanning a file without metrics."""
        code = """
def process_request():
    return "Hello"

class Handler:
    def handle(self):
        pass
"""
        file_path = tmp_path / "app.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_metrics == 0

    def test_scan_counter_metric(self, tmp_path, scanner, counter_metric):
        """Test scanning a Counter metric."""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(counter_metric)

        output = scanner.scan(file_path)

        assert output.summary.total_metrics == 1
        assert "http_requests_total" in output.results
        metric = output.results["http_requests_total"]
        assert metric.type == "Counter"
        assert metric.help == "Total HTTP requests"

    def test_scan_gauge_metric(self, tmp_path, scanner, gauge_metric):
        """Test scanning a Gauge metric."""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(gauge_metric)

        output = scanner.scan(file_path)

        assert output.summary.total_metrics == 1
        assert "active_users" in output.results
        metric = output.results["active_users"]
        assert metric.type == "Gauge"

    def test_scan_histogram_metric(self, tmp_path, scanner, histogram_metric):
        """Test scanning a Histogram metric."""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(histogram_metric)

        output = scanner.scan(file_path)

        assert output.summary.total_metrics == 1
        assert "request_duration_seconds" in output.results
        metric = output.results["request_duration_seconds"]
        assert metric.type == "Histogram"

    def test_scan_summary_metric(self, tmp_path, scanner, summary_metric):
        """Test scanning a Summary metric."""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(summary_metric)

        output = scanner.scan(file_path)

        assert output.summary.total_metrics == 1
        assert "response_size_bytes" in output.results
        metric = output.results["response_size_bytes"]
        assert metric.type == "Summary"

    def test_scan_metric_with_labels(self, tmp_path, scanner, metric_with_labels):
        """Test scanning a metric with labels."""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(metric_with_labels)

        output = scanner.scan(file_path)

        assert output.summary.total_metrics == 1
        metric = output.results["http_requests_total"]
        assert len(metric.labels) == 3
        assert "method" in metric.labels
        assert "endpoint" in metric.labels
        assert "status" in metric.labels

    def test_scan_multiple_metrics(self, tmp_path, scanner, multiple_metrics):
        """Test scanning multiple metrics in one file."""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(multiple_metrics)

        output = scanner.scan(file_path)

        assert output.summary.total_metrics == 3
        assert "http_requests_total" in output.results
        assert "active_connections" in output.results
        assert "request_duration_seconds" in output.results

    def test_scan_directory(self, tmp_path, scanner):
        """Test scanning a directory with multiple files."""
        file1 = tmp_path / "metrics1.py"
        file1.write_text("""
from prometheus_client import Counter

requests = Counter('requests_total', 'Total requests')
""")

        file2 = tmp_path / "metrics2.py"
        file2.write_text("""
from prometheus_client import Gauge

connections = Gauge('active_connections', 'Active connections')
""")

        output = scanner.scan(tmp_path)

        assert output.summary.total_metrics == 2
        assert output.summary.files_scanned == 2

    def test_scan_summary_by_type(self, tmp_path, scanner, multiple_metrics):
        """Test that summary counts metrics by type."""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(multiple_metrics)

        output = scanner.scan(file_path)

        assert output.summary.by_type["Counter"] == 1
        assert output.summary.by_type["Gauge"] == 1
        assert output.summary.by_type["Histogram"] == 1

    def test_scan_metric_usage_tracking(self, tmp_path, scanner, counter_metric):
        """Test that metric definitions are tracked."""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(counter_metric)

        output = scanner.scan(file_path)

        metric = output.results["http_requests_total"]
        assert len(metric.definitions) == 1
        definition = metric.definitions[0]
        assert definition.file is not None
        assert definition.line is not None
        assert "Counter" in definition.statement

    def test_scan_metric_name_extraction(self, tmp_path, scanner):
        """Test that metric names are correctly extracted."""
        code = """
from prometheus_client import Counter

my_counter = Counter('custom_metric_name', 'Help text')
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert "custom_metric_name" in output.results

    def test_scan_metric_help_extraction(self, tmp_path, scanner):
        """Test that help text is correctly extracted."""
        code = """
from prometheus_client import Counter

counter = Counter('test_metric', 'This is the help text')
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        metric = output.results["test_metric"]
        assert metric.help == "This is the help text"

    def test_scan_file_path_tracking(self, tmp_path, scanner, counter_metric):
        """Test that file paths are correctly tracked in definitions."""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(counter_metric)

        output = scanner.scan(file_path)

        metric = output.results["http_requests_total"]
        definition = metric.definitions[0]
        assert "metrics.py" in definition.file
