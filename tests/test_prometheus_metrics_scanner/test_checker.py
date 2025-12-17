"""Tests for checker."""

from pathlib import Path

import pytest

from upcast.prometheus_metrics_scanner.checker import PrometheusMetricsChecker


@pytest.fixture
def fixtures_dir():
    """Get fixtures directory path."""
    return Path(__file__).parent / "fixtures"


class TestChecker:
    """Test PrometheusMetricsChecker."""

    def test_check_simple_metrics_file(self, fixtures_dir):
        """Test checking simple metrics file."""
        checker = PrometheusMetricsChecker(str(fixtures_dir))
        checker.check_file(str(fixtures_dir / "simple_metrics.py"))

        metrics = checker.get_metrics()
        assert len(metrics) > 0

        # Check that http_requests_total was found
        assert "http_requests_total" in metrics
        metric = metrics["http_requests_total"]
        assert metric.type == "counter"
        assert metric.help == "HTTP 请求总数"
        assert metric.labels == ["method", "path", "status"]

    def test_check_custom_collectors(self, fixtures_dir):
        """Test checking custom collectors."""
        checker = PrometheusMetricsChecker(str(fixtures_dir))
        checker.check_file(str(fixtures_dir / "custom_collectors.py"))

        metrics = checker.get_metrics()

        # Check custom collector metrics
        if "my_dynamic_metric" in metrics:
            metric = metrics["my_dynamic_metric"]
            assert metric.custom_collector is True
            assert metric.type == "gauge"

    def test_multiple_files(self, fixtures_dir):
        """Test checking multiple files."""
        checker = PrometheusMetricsChecker(str(fixtures_dir))
        checker.check_file(str(fixtures_dir / "simple_metrics.py"))
        checker.check_file(str(fixtures_dir / "decorators.py"))

        metrics = checker.get_metrics()
        assert len(metrics) > 0

    def test_aggregation(self, fixtures_dir):
        """Test that usages are aggregated correctly."""
        checker = PrometheusMetricsChecker(str(fixtures_dir))
        checker.check_file(str(fixtures_dir / "simple_metrics.py"))

        metrics = checker.get_metrics()
        # Each metric should have at least one usage
        for metric in metrics.values():
            assert len(metric.usages) > 0
            # Check usage structure
            for usage in metric.usages:
                assert usage.location
                assert usage.pattern
                assert usage.statement
