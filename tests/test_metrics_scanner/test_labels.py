"""Tests for metric labels detection."""

import pytest
from pathlib import Path

from upcast.scanners.metrics import MetricsScanner


class TestLabels:
    """Test detection of metric labels."""

    def test_metric_without_labels(self, tmp_path, scanner):
        """Test metric without labels."""
        code = """
from prometheus_client import Counter

requests = Counter('requests_total', 'Total requests')
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        metric = output.results["requests_total"]
        assert len(metric.labels) == 0

    def test_metric_with_single_label(self, tmp_path, scanner):
        """Test metric with single label."""
        code = """
from prometheus_client import Counter

requests = Counter('requests_total', 'Total requests', labelnames=['method'])
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        metric = output.results["requests_total"]
        assert len(metric.labels) == 1
        assert "method" in metric.labels

    def test_metric_with_multiple_labels(self, tmp_path, scanner):
        """Test metric with multiple labels."""
        code = """
from prometheus_client import Counter

requests = Counter(
    'requests_total',
    'Total requests',
    labelnames=['method', 'endpoint', 'status', 'region']
)
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        metric = output.results["requests_total"]
        assert len(metric.labels) == 4
        assert "method" in metric.labels
        assert "endpoint" in metric.labels
        assert "status" in metric.labels
        assert "region" in metric.labels

    def test_metric_with_labels_keyword(self, tmp_path, scanner):
        """Test metric with 'labels' keyword instead of 'labelnames'."""
        code = """
from prometheus_client import Counter

requests = Counter('requests_total', 'Total requests', labels=['method', 'status'])
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        metric = output.results["requests_total"]
        assert len(metric.labels) == 2
        assert "method" in metric.labels
        assert "status" in metric.labels

    def test_metric_with_tuple_labels(self, tmp_path, scanner):
        """Test metric with labels as tuple."""
        code = """
from prometheus_client import Counter

requests = Counter('requests_total', 'Total requests', labelnames=('method', 'status'))
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        metric = output.results["requests_total"]
        assert len(metric.labels) >= 2

    def test_different_metrics_different_labels(self, tmp_path, scanner):
        """Test different metrics with different labels."""
        code = """
from prometheus_client import Counter, Gauge

requests = Counter('requests_total', 'Total requests', labelnames=['method', 'status'])
connections = Gauge('active_connections', 'Active connections', labelnames=['protocol'])
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        requests_metric = output.results["requests_total"]
        connections_metric = output.results["active_connections"]

        assert len(requests_metric.labels) == 2
        assert "method" in requests_metric.labels

        assert len(connections_metric.labels) == 1
        assert "protocol" in connections_metric.labels
