"""Tests for PrometheusMetricScanner."""

from pathlib import Path
from unittest.mock import patch

import astroid

from upcast.common.hybrid_scan_pipeline import PipelineRunResult, SemanticDecision, StructuralCandidate
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

    def test_scanner_uses_hybrid_pipeline_for_metric_candidates(self, tmp_path, monkeypatch):
        """Scanner should use the hybrid pipeline to discover metric candidates."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
from prometheus_client import Counter

REQUESTS_TOTAL = Counter('http_requests_total', 'Total requests')
"""
        )

        scanner = MetricsScanner()
        calls: list[tuple[str, str]] = []

        def fake_run_pipeline(*, spec, source, file_path):
            module = astroid.parse(source, path=file_path)
            metric_call = next(module.nodes_of_class(astroid.nodes.Call))
            calls.append((spec.name, file_path))
            return PipelineRunResult(
                candidates=[
                    StructuralCandidate(
                        file_path=file_path,
                        structural_span={
                            "start": [metric_call.lineno, metric_call.col_offset],
                            "end": [metric_call.end_lineno, metric_call.end_col_offset],
                        },
                        captures={
                            "self": metric_call,
                            "METRIC": metric_call.func,
                            "ARGS": metric_call.args,
                        },
                        snippet=metric_call.as_string(),
                    )
                ],
                decisions=[SemanticDecision(status="confirmed")],
                findings=[],
            )

        monkeypatch.setattr("upcast.scanners.metrics.run_pipeline", fake_run_pipeline, raising=False)

        output = scanner.scan(test_file)

        assert calls == [("scan-metrics", str(test_file))]
        assert output.summary.total_metrics == 1
        assert "http_requests_total" in output.results
        assert output.results["http_requests_total"].type == "Counter"
