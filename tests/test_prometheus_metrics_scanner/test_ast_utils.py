"""Tests for AST utilities."""

from pathlib import Path

import pytest
from astroid import MANAGER, nodes

from upcast.prometheus_metrics_scanner.ast_utils import (
    extract_help_text,
    extract_labels,
    extract_metric_name,
    is_custom_collector_class,
    is_metric_family_call,
    is_prometheus_metric_call,
)


@pytest.fixture
def simple_metrics_module():
    """Load simple_metrics fixture as astroid module."""
    fixture_path = Path(__file__).parent / "fixtures" / "simple_metrics.py"
    return MANAGER.ast_from_file(str(fixture_path))


@pytest.fixture
def non_prometheus_module():
    """Load non_prometheus fixture as astroid module."""
    fixture_path = Path(__file__).parent / "fixtures" / "non_prometheus.py"
    return MANAGER.ast_from_file(str(fixture_path))


@pytest.fixture
def mixed_counters_module():
    """Load mixed_counters fixture as astroid module."""
    fixture_path = Path(__file__).parent / "fixtures" / "mixed_counters.py"
    return MANAGER.ast_from_file(str(fixture_path))


class TestMetricDetection:
    """Test metric type detection."""

    def test_counter_detection(self, simple_metrics_module):
        """Test Counter metric detection."""
        # Find the http_requests_total assignment
        for assign in simple_metrics_module.nodes_of_class(nodes.Assign):
            if assign.targets[0].name == "http_requests_total":
                assert isinstance(assign.value, nodes.Call)
                metric_type = is_prometheus_metric_call(assign.value)
                assert metric_type == "counter"
                break
        else:
            pytest.fail("http_requests_total not found")

    def test_gauge_detection(self, simple_metrics_module):
        """Test Gauge metric detection."""
        for assign in simple_metrics_module.nodes_of_class(nodes.Assign):
            if assign.targets[0].name == "memory_usage_bytes":
                assert isinstance(assign.value, nodes.Call)
                metric_type = is_prometheus_metric_call(assign.value)
                assert metric_type == "gauge"
                break
        else:
            pytest.fail("memory_usage_bytes not found")

    def test_histogram_detection(self, simple_metrics_module):
        """Test Histogram metric detection."""
        for assign in simple_metrics_module.nodes_of_class(nodes.Assign):
            if assign.targets[0].name == "request_duration_seconds":
                assert isinstance(assign.value, nodes.Call)
                metric_type = is_prometheus_metric_call(assign.value)
                assert metric_type == "histogram"
                break
        else:
            pytest.fail("request_duration_seconds not found")

    def test_summary_detection(self, simple_metrics_module):
        """Test Summary metric detection."""
        for assign in simple_metrics_module.nodes_of_class(nodes.Assign):
            if assign.targets[0].name == "response_size_bytes":
                assert isinstance(assign.value, nodes.Call)
                metric_type = is_prometheus_metric_call(assign.value)
                assert metric_type == "summary"
                break
        else:
            pytest.fail("response_size_bytes not found")

    def test_module_import_style(self, simple_metrics_module):
        """Test detection with module.Counter style."""
        for assign in simple_metrics_module.nodes_of_class(nodes.Assign):
            if assign.targets[0].name == "module_style_counter":
                assert isinstance(assign.value, nodes.Call)
                metric_type = is_prometheus_metric_call(assign.value)
                assert metric_type == "counter"
                break
        else:
            pytest.fail("module_style_counter not found")

    def test_non_prometheus_counter_not_detected(self, non_prometheus_module):
        """Test that collections.Counter is NOT detected as Prometheus metric."""
        for assign in non_prometheus_module.nodes_of_class(nodes.Assign):
            if assign.targets[0].name in ("word_counts", "letter_frequency"):
                assert isinstance(assign.value, nodes.Call)
                metric_type = is_prometheus_metric_call(assign.value)
                # Should NOT detect collections.Counter as prometheus metric
                assert metric_type is None

    def test_mixed_counters_only_prometheus_detected(self, mixed_counters_module):
        """Test that only Prometheus Counter is detected when mixed with collections.Counter."""
        prometheus_detected = False
        collections_detected = False

        for assign in mixed_counters_module.nodes_of_class(nodes.Assign):
            if assign.targets[0].name == "http_requests":
                assert isinstance(assign.value, nodes.Call)
                metric_type = is_prometheus_metric_call(assign.value)
                assert metric_type == "counter"
                prometheus_detected = True
            elif assign.targets[0].name in ("word_counts", "char_frequency"):
                assert isinstance(assign.value, nodes.Call)
                metric_type = is_prometheus_metric_call(assign.value)
                assert metric_type is None
                collections_detected = True

        assert prometheus_detected, "Prometheus Counter should be detected"
        assert collections_detected, "collections.Counter should be checked"


class TestMetadataExtraction:
    """Test metadata extraction from metric calls."""

    def test_extract_metric_name(self, simple_metrics_module):
        """Test metric name extraction."""
        for assign in simple_metrics_module.nodes_of_class(nodes.Assign):
            if assign.targets[0].name == "http_requests_total":
                assert isinstance(assign.value, nodes.Call)
                name = extract_metric_name(assign.value)
                assert name == "http_requests_total"
                break
        else:
            pytest.fail("http_requests_total not found")

    def test_extract_help_text(self, simple_metrics_module):
        """Test help text extraction."""
        for assign in simple_metrics_module.nodes_of_class(nodes.Assign):
            if assign.targets[0].name == "http_requests_total":
                assert isinstance(assign.value, nodes.Call)
                help_text = extract_help_text(assign.value)
                assert help_text == "HTTP 请求总数"
                break
        else:
            pytest.fail("http_requests_total not found")

    def test_extract_help_text_missing(self, simple_metrics_module):
        """Test help text extraction when missing."""
        for assign in simple_metrics_module.nodes_of_class(nodes.Assign):
            if assign.targets[0].name == "simple_counter":
                assert isinstance(assign.value, nodes.Call)
                help_text = extract_help_text(assign.value)
                assert help_text is None
                break
        else:
            pytest.fail("simple_counter not found")

    def test_extract_labels_with_values(self, simple_metrics_module):
        """Test label extraction from list."""
        for assign in simple_metrics_module.nodes_of_class(nodes.Assign):
            if assign.targets[0].name == "http_requests_total":
                assert isinstance(assign.value, nodes.Call)
                labels = extract_labels(assign.value)
                assert labels == ["method", "path", "status"]
                break
        else:
            pytest.fail("http_requests_total not found")

    def test_extract_labels_empty(self, simple_metrics_module):
        """Test label extraction when no labels."""
        for assign in simple_metrics_module.nodes_of_class(nodes.Assign):
            if assign.targets[0].name == "memory_usage_bytes":
                assert isinstance(assign.value, nodes.Call)
                labels = extract_labels(assign.value)
                assert labels == []
                break
        else:
            pytest.fail("memory_usage_bytes not found")

    def test_extract_labels_from_keyword(self, simple_metrics_module):
        """Test label extraction from keyword argument."""
        for assign in simple_metrics_module.nodes_of_class(nodes.Assign):
            if assign.targets[0].name == "api_errors":
                assert isinstance(assign.value, nodes.Call)
                labels = extract_labels(assign.value)
                assert labels == ["error_type"]
                break
        else:
            pytest.fail("api_errors not found")


class TestCustomCollector:
    """Test custom collector detection."""

    def test_is_custom_collector_class_false(self, simple_metrics_module):
        """Test that regular classes are not detected as collectors."""
        # simple_metrics doesn't have custom collectors
        for classdef in simple_metrics_module.nodes_of_class(nodes.ClassDef):
            assert not is_custom_collector_class(classdef)


class TestMetricFamilyDetection:
    """Test MetricFamily detection."""

    def test_metric_family_call_not_in_simple(self, simple_metrics_module):
        """Test that simple metrics don't use MetricFamily."""
        for assign in simple_metrics_module.nodes_of_class(nodes.Assign):
            if isinstance(assign.value, nodes.Call):
                # Simple metrics use Counter/Gauge/etc, not MetricFamily
                # Call is_metric_family_call to ensure it doesn't crash
                is_metric_family_call(assign.value)
                # The key is we can detect both patterns
                pass
