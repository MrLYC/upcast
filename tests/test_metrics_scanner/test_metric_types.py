"""Tests for different metric types."""

import pytest
from pathlib import Path

from upcast.scanners.metrics import MetricsScanner


class TestMetricTypes:
    """Test detection of different metric types."""

    def test_counter_from_direct_import(self, tmp_path, scanner):
        """Test Counter with direct import."""
        code = """
from prometheus_client import Counter

http_requests = Counter('http_requests_total', 'Total HTTP requests')
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_metrics == 1
        metric = output.results["http_requests_total"]
        assert metric.type == "Counter"

    def test_gauge_from_direct_import(self, tmp_path, scanner):
        """Test Gauge with direct import."""
        code = """
from prometheus_client import Gauge

temperature = Gauge('temperature_celsius', 'Current temperature')
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        metric = output.results["temperature_celsius"]
        assert metric.type == "Gauge"

    def test_histogram_from_direct_import(self, tmp_path, scanner):
        """Test Histogram with direct import."""
        code = """
from prometheus_client import Histogram

request_latency = Histogram('request_latency_seconds', 'Request latency')
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        metric = output.results["request_latency_seconds"]
        assert metric.type == "Histogram"

    def test_summary_from_direct_import(self, tmp_path, scanner):
        """Test Summary with direct import."""
        code = """
from prometheus_client import Summary

response_size = Summary('response_size_bytes', 'Response size')
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        metric = output.results["response_size_bytes"]
        assert metric.type == "Summary"

    def test_counter_from_module_import(self, tmp_path, scanner):
        """Test Counter with module import."""
        code = """
import prometheus_client

http_requests = prometheus_client.Counter('http_requests_total', 'Total requests')
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_metrics == 1
        metric = output.results["http_requests_total"]
        assert metric.type == "Counter"

    def test_gauge_from_module_import(self, tmp_path, scanner):
        """Test Gauge with module import."""
        code = """
import prometheus_client as prom

connections = prom.Gauge('active_connections', 'Active connections')
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        metric = output.results["active_connections"]
        assert metric.type == "Gauge"

    def test_mixed_import_styles(self, tmp_path, scanner):
        """Test mixed import styles."""
        code = """
from prometheus_client import Counter, Gauge
import prometheus_client

counter1 = Counter('counter1', 'First counter')
gauge1 = Gauge('gauge1', 'First gauge')
counter2 = prometheus_client.Counter('counter2', 'Second counter')
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_metrics == 3
        assert output.summary.by_type["Counter"] == 2
        assert output.summary.by_type["Gauge"] == 1

    def test_all_metric_types_together(self, tmp_path, scanner):
        """Test all metric types in one file."""
        code = """
from prometheus_client import Counter, Gauge, Histogram, Summary

counter = Counter('my_counter', 'A counter')
gauge = Gauge('my_gauge', 'A gauge')
histogram = Histogram('my_histogram', 'A histogram')
summary = Summary('my_summary', 'A summary')
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_metrics == 4
        assert output.summary.by_type["Counter"] == 1
        assert output.summary.by_type["Gauge"] == 1
        assert output.summary.by_type["Histogram"] == 1
        assert output.summary.by_type["Summary"] == 1

    def test_counter_with_keyword_args(self, tmp_path, scanner):
        """Test Counter with keyword arguments."""
        code = """
from prometheus_client import Counter

requests = Counter(
    name='http_requests_total',
    documentation='Total HTTP requests'
)
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_metrics == 1
        metric = output.results["http_requests_total"]
        assert metric.type == "Counter"
        assert metric.help == "Total HTTP requests"

    def test_metric_type_case_sensitivity(self, tmp_path, scanner):
        """Test that metric types are case-sensitive."""
        code = """
from prometheus_client import Counter

# Standard case
counter1 = Counter('counter1', 'First')
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_metrics == 1
        assert output.results["counter1"].type == "Counter"

    def test_metric_with_multiline_definition(self, tmp_path, scanner):
        """Test metric with multiline definition."""
        code = """
from prometheus_client import Counter

requests = Counter(
    'http_requests_total',
    'Total HTTP requests made to the API',
)
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_metrics == 1
        metric = output.results["http_requests_total"]
        assert metric.type == "Counter"
