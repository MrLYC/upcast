"""Tests for metrics parser."""

from pathlib import Path

import pytest
from astroid import MANAGER, nodes

from upcast.prometheus_metrics_scanner.metrics_parser import (
    MetricInfo,
    UsageInfo,
    parse_metric_instantiation,
)


@pytest.fixture
def simple_metrics_module():
    """Load simple_metrics fixture as astroid module."""
    fixture_path = Path(__file__).parent / "fixtures" / "simple_metrics.py"
    return MANAGER.ast_from_file(str(fixture_path))


class TestMetricInstantiationParsing:
    """Test parsing metric instantiation."""

    def test_parse_counter_with_labels(self, simple_metrics_module):
        """Test parsing Counter with all metadata."""
        for assign in simple_metrics_module.nodes_of_class(nodes.Assign):
            if assign.targets[0].name == "http_requests_total":
                metric = parse_metric_instantiation(assign, "test.py", assign.lineno)
                assert metric is not None
                assert metric.name == "http_requests_total"
                assert metric.type == "counter"
                assert metric.help == "HTTP 请求总数"
                assert metric.labels == ["method", "path", "status"]
                assert len(metric.usages) == 1
                assert metric.usages[0].pattern == "instantiation"
                assert metric.usages[0].location == f"test.py:{assign.lineno}"
                break
        else:
            pytest.fail("http_requests_total not found")

    def test_parse_gauge_without_labels(self, simple_metrics_module):
        """Test parsing Gauge without labels."""
        for assign in simple_metrics_module.nodes_of_class(nodes.Assign):
            if assign.targets[0].name == "memory_usage_bytes":
                metric = parse_metric_instantiation(assign, "test.py", assign.lineno)
                assert metric is not None
                assert metric.name == "memory_usage_bytes"
                assert metric.type == "gauge"
                assert metric.help == "Memory usage in bytes"
                assert metric.labels == []
                break
        else:
            pytest.fail("memory_usage_bytes not found")

    def test_parse_histogram_with_buckets(self, simple_metrics_module):
        """Test parsing Histogram with buckets."""
        for assign in simple_metrics_module.nodes_of_class(nodes.Assign):
            if assign.targets[0].name == "request_duration_seconds":
                metric = parse_metric_instantiation(assign, "test.py", assign.lineno)
                assert metric is not None
                assert metric.name == "request_duration_seconds"
                assert metric.type == "histogram"
                assert metric.buckets == [0.1, 0.5, 1.0, 2.5, 5.0]
                break
        else:
            pytest.fail("request_duration_seconds not found")

    def test_parse_summary(self, simple_metrics_module):
        """Test parsing Summary."""
        for assign in simple_metrics_module.nodes_of_class(nodes.Assign):
            if assign.targets[0].name == "response_size_bytes":
                metric = parse_metric_instantiation(assign, "test.py", assign.lineno)
                assert metric is not None
                assert metric.name == "response_size_bytes"
                assert metric.type == "summary"
                break
        else:
            pytest.fail("response_size_bytes not found")

    def test_parse_with_namespace_subsystem(self, simple_metrics_module):
        """Test parsing with namespace and subsystem."""
        for assign in simple_metrics_module.nodes_of_class(nodes.Assign):
            if assign.targets[0].name == "api_errors":
                metric = parse_metric_instantiation(assign, "test.py", assign.lineno)
                assert metric is not None
                assert metric.name == "errors"
                assert metric.namespace == "api"
                assert metric.subsystem == "http"
                assert metric.labels == ["error_type"]
                break
        else:
            pytest.fail("api_errors not found")

    def test_parse_without_help(self, simple_metrics_module):
        """Test parsing metric without help text."""
        for assign in simple_metrics_module.nodes_of_class(nodes.Assign):
            if assign.targets[0].name == "simple_counter":
                metric = parse_metric_instantiation(assign, "test.py", assign.lineno)
                assert metric is not None
                assert metric.name == "simple_counter"
                assert metric.help is None
                break
        else:
            pytest.fail("simple_counter not found")


class TestDataStructures:
    """Test data structures."""

    def test_usage_info_creation(self):
        """Test UsageInfo dataclass."""
        usage = UsageInfo(location="test.py:10", pattern="instantiation", statement="counter = Counter(...)")
        assert usage.location == "test.py:10"
        assert usage.pattern == "instantiation"
        assert usage.statement == "counter = Counter(...)"

    def test_metric_info_creation(self):
        """Test MetricInfo dataclass."""
        metric = MetricInfo(
            name="test_metric",
            type="counter",
            help="Test metric",
            labels=["label1"],
            namespace="test",
        )
        assert metric.name == "test_metric"
        assert metric.type == "counter"
        assert metric.help == "Test metric"
        assert metric.labels == ["label1"]

    def test_get_full_name_without_namespace(self):
        """Test get_full_name() without namespace/subsystem."""
        metric = MetricInfo(
            name="simple_counter",
            type="counter",
            help="Simple counter",
            labels=[],
        )
        assert metric.get_full_name() == "simple_counter"

    def test_get_full_name_with_namespace(self):
        """Test get_full_name() with namespace only."""
        metric = MetricInfo(
            name="requests_total",
            type="counter",
            help="Total requests",
            labels=[],
            namespace="api",
        )
        assert metric.get_full_name() == "api_requests_total"

    def test_get_full_name_with_namespace_and_subsystem(self):
        """Test get_full_name() with namespace and subsystem."""
        metric = MetricInfo(
            name="errors",
            type="counter",
            help="API errors",
            labels=[],
            namespace="api",
            subsystem="http",
        )
        assert metric.get_full_name() == "api_http_errors"

    def test_get_full_name_with_subsystem_only(self):
        """Test get_full_name() with subsystem only."""
        metric = MetricInfo(
            name="latency_seconds",
            type="histogram",
            help="Request latency",
            labels=[],
            subsystem="http",
        )
        assert metric.get_full_name() == "http_latency_seconds"
