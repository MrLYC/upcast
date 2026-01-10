"""Tests for metrics scanner models."""

import pytest
from pydantic import ValidationError

from upcast.models.metrics import (
    MetricUsage,
    MetricInfo,
    PrometheusMetricSummary,
    PrometheusMetricOutput,
)


class TestMetricUsageModel:
    """Test MetricUsage model validation."""

    def test_metric_usage_valid(self):
        """Test valid MetricUsage creation."""
        usage = MetricUsage(
            file="metrics.py",
            line=10,
            pattern="Counter.inc()",
            statement="requests_total.inc()",
        )
        assert usage.file == "metrics.py"
        assert usage.line == 10
        assert usage.pattern == "Counter.inc()"

    def test_metric_usage_without_line(self):
        """Test MetricUsage without line number."""
        usage = MetricUsage(
            file="metrics.py",
            line=None,
            pattern="Counter definition",
            statement="Counter('test', 'help')",
        )
        assert usage.line is None


class TestMetricInfoModel:
    """Test MetricInfo model validation."""

    def test_metric_info_counter(self):
        """Test MetricInfo for Counter."""
        metric = MetricInfo(
            name="http_requests_total",
            type="Counter",
            help="Total HTTP requests",
            labels=[],
            namespace=None,
            subsystem=None,
            unit=None,
            custom_collector=False,
            buckets=None,
            usages=[],
        )
        assert metric.name == "http_requests_total"
        assert metric.type == "Counter"

    def test_metric_info_with_labels(self):
        """Test MetricInfo with labels."""
        metric = MetricInfo(
            name="http_requests_total",
            type="Counter",
            help="Total requests",
            labels=["method", "endpoint", "status"],
            namespace=None,
            subsystem=None,
            unit=None,
            custom_collector=False,
            buckets=None,
            usages=[],
        )
        assert len(metric.labels) == 3
        assert "method" in metric.labels

    def test_metric_info_with_namespace_subsystem(self):
        """Test MetricInfo with namespace and subsystem."""
        metric = MetricInfo(
            name="http_requests_total",
            type="Counter",
            help="Total requests",
            labels=[],
            namespace="myapp",
            subsystem="api",
            unit="seconds",
            custom_collector=False,
            buckets=None,
            usages=[],
        )
        assert metric.namespace == "myapp"
        assert metric.subsystem == "api"
        assert metric.unit == "seconds"

    def test_metric_info_histogram_with_buckets(self):
        """Test MetricInfo for Histogram with buckets."""
        metric = MetricInfo(
            name="request_duration_seconds",
            type="Histogram",
            help="Request duration",
            labels=[],
            namespace=None,
            subsystem=None,
            unit=None,
            custom_collector=False,
            buckets=[0.1, 0.5, 1.0, 5.0],
            usages=[],
        )
        assert metric.type == "Histogram"
        assert metric.buckets == [0.1, 0.5, 1.0, 5.0]

    def test_metric_info_with_usages(self):
        """Test MetricInfo with usages."""
        usage1 = MetricUsage(
            file="api.py",
            line=10,
            pattern="Counter.inc()",
            statement="requests_total.inc()",
        )
        usage2 = MetricUsage(
            file="handlers.py",
            line=20,
            pattern="Counter.inc()",
            statement="requests_total.inc()",
        )

        metric = MetricInfo(
            name="http_requests_total",
            type="Counter",
            help="Total requests",
            labels=[],
            namespace=None,
            subsystem=None,
            unit=None,
            custom_collector=False,
            buckets=None,
            usages=[usage1, usage2],
        )
        assert len(metric.usages) == 2


class TestPrometheusMetricSummaryModel:
    """Test PrometheusMetricSummary model validation."""

    def test_summary_valid(self):
        """Test valid PrometheusMetricSummary creation."""
        summary = PrometheusMetricSummary(
            total_count=10,
            files_scanned=3,
            scan_duration_ms=100,
            total_metrics=5,
            by_type={"Counter": 3, "Gauge": 2},
        )
        assert summary.total_metrics == 5
        assert summary.by_type["Counter"] == 3

    def test_summary_empty(self):
        """Test summary with no metrics."""
        summary = PrometheusMetricSummary(
            total_count=0,
            files_scanned=0,
            scan_duration_ms=50,
            total_metrics=0,
            by_type={},
        )
        assert summary.total_metrics == 0
        assert len(summary.by_type) == 0

    def test_summary_all_metric_types(self):
        """Test summary with all metric types."""
        summary = PrometheusMetricSummary(
            total_count=10,
            files_scanned=2,
            scan_duration_ms=100,
            total_metrics=10,
            by_type={
                "Counter": 3,
                "Gauge": 2,
                "Histogram": 3,
                "Summary": 2,
            },
        )
        assert len(summary.by_type) == 4
        assert summary.by_type["Histogram"] == 3


class TestPrometheusMetricOutputModel:
    """Test PrometheusMetricOutput model validation."""

    def test_output_valid(self):
        """Test valid PrometheusMetricOutput creation."""
        metric = MetricInfo(
            name="http_requests_total",
            type="Counter",
            help="Total requests",
            labels=[],
            namespace=None,
            subsystem=None,
            unit=None,
            custom_collector=False,
            buckets=None,
            usages=[],
        )

        output = PrometheusMetricOutput(
            summary=PrometheusMetricSummary(
                total_count=1,
                files_scanned=1,
                scan_duration_ms=100,
                total_metrics=1,
                by_type={"Counter": 1},
            ),
            results={"http_requests_total": metric},
        )
        assert len(output.results) == 1
        assert "http_requests_total" in output.results

    def test_output_empty(self):
        """Test output with no metrics."""
        output = PrometheusMetricOutput(
            summary=PrometheusMetricSummary(
                total_count=0,
                files_scanned=0,
                scan_duration_ms=50,
                total_metrics=0,
                by_type={},
            ),
            results={},
        )
        assert len(output.results) == 0

    def test_output_multiple_metrics(self):
        """Test output with multiple metrics."""
        metric1 = MetricInfo(
            name="http_requests_total",
            type="Counter",
            help="Total requests",
            labels=[],
            namespace=None,
            subsystem=None,
            unit=None,
            custom_collector=False,
            buckets=None,
            usages=[],
        )
        metric2 = MetricInfo(
            name="active_connections",
            type="Gauge",
            help="Active connections",
            labels=[],
            namespace=None,
            subsystem=None,
            unit=None,
            custom_collector=False,
            buckets=None,
            usages=[],
        )

        output = PrometheusMetricOutput(
            summary=PrometheusMetricSummary(
                total_count=2,
                files_scanned=1,
                scan_duration_ms=100,
                total_metrics=2,
                by_type={"Counter": 1, "Gauge": 1},
            ),
            results={
                "http_requests_total": metric1,
                "active_connections": metric2,
            },
        )
        assert len(output.results) == 2

    def test_output_serialization(self):
        """Test that output can be serialized to dict/JSON."""
        metric = MetricInfo(
            name="http_requests_total",
            type="Counter",
            help="Total requests",
            labels=[],
            namespace=None,
            subsystem=None,
            unit=None,
            custom_collector=False,
            buckets=None,
            usages=[],
        )

        output = PrometheusMetricOutput(
            summary=PrometheusMetricSummary(
                total_count=1,
                files_scanned=1,
                scan_duration_ms=100,
                total_metrics=1,
                by_type={"Counter": 1},
            ),
            results={"http_requests_total": metric},
        )

        data = output.model_dump()
        assert "summary" in data
        assert "results" in data
        assert data["summary"]["total_metrics"] == 1
