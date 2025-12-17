"""Tests for export functions."""

import tempfile
from pathlib import Path

import pytest
import yaml

from upcast.prometheus_metrics_scanner.export import (
    export_to_yaml,
    export_to_yaml_string,
    format_metric_output,
)
from upcast.prometheus_metrics_scanner.metrics_parser import MetricInfo, UsageInfo


@pytest.fixture
def sample_metrics():
    """Create sample metrics for testing."""
    return {
        "test_counter": MetricInfo(
            name="test_counter",
            type="counter",
            help="Test counter",
            labels=["label1", "label2"],
            usages=[
                UsageInfo(
                    location="test.py:10",
                    pattern="instantiation",
                    statement="counter = Counter('test_counter', 'Test counter', ['label1', 'label2'])",
                )
            ],
        ),
        "test_metrics_gauge": MetricInfo(
            name="gauge",
            type="gauge",
            help="Test gauge",
            labels=[],
            namespace="test",
            subsystem="metrics",
            usages=[
                UsageInfo(
                    location="test.py:15",
                    pattern="instantiation",
                    statement="gauge = Gauge('gauge', 'Test gauge', namespace='test', subsystem='metrics')",
                )
            ],
        ),
    }


class TestFormatMetricOutput:
    """Test format_metric_output function."""

    def test_format_basic_metric(self, sample_metrics):
        """Test formatting basic metrics."""
        output = format_metric_output(sample_metrics)

        assert "test_counter" in output
        assert output["test_counter"]["name"] == "test_counter"
        assert output["test_counter"]["type"] == "counter"
        assert output["test_counter"]["help"] == "Test counter"
        assert output["test_counter"]["labels"] == ["label1", "label2"]
        assert len(output["test_counter"]["usages"]) == 1

    def test_format_with_namespace(self, sample_metrics):
        """Test formatting metrics with namespace."""
        output = format_metric_output(sample_metrics)

        assert "test_metrics_gauge" in output
        assert output["test_metrics_gauge"]["name"] == "gauge"
        assert output["test_metrics_gauge"]["namespace"] == "test"
        assert output["test_metrics_gauge"]["subsystem"] == "metrics"

    def test_alphabetical_sorting(self, sample_metrics):
        """Test that metrics are sorted alphabetically."""
        output = format_metric_output(sample_metrics)
        keys = list(output.keys())

        assert keys == sorted(keys)

    def test_full_metric_name_as_key(self, sample_metrics):
        """Test that full metric name (with namespace/subsystem) is used as key."""
        output = format_metric_output(sample_metrics)

        # Metric without namespace/subsystem: key == name
        assert "test_counter" in output
        assert output["test_counter"]["name"] == "test_counter"

        # Metric with namespace and subsystem: key = namespace_subsystem_name
        assert "test_metrics_gauge" in output
        assert output["test_metrics_gauge"]["name"] == "gauge"
        assert output["test_metrics_gauge"]["namespace"] == "test"
        assert output["test_metrics_gauge"]["subsystem"] == "metrics"


class TestExportToYaml:
    """Test export_to_yaml function."""

    def test_export_to_file(self, sample_metrics):
        """Test exporting to a file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.yaml"
            export_to_yaml(sample_metrics, str(output_path))

            assert output_path.exists()

            # Read and verify content
            with output_path.open() as f:
                data = yaml.safe_load(f)

            assert "test_counter" in data
            assert "test_metrics_gauge" in data

    def test_create_parent_directories(self, sample_metrics):
        """Test that parent directories are created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "subdir" / "output.yaml"
            export_to_yaml(sample_metrics, str(output_path))

            assert output_path.exists()


class TestExportToYamlString:
    """Test export_to_yaml_string function."""

    def test_export_to_string(self, sample_metrics):
        """Test exporting to YAML string."""
        yaml_str = export_to_yaml_string(sample_metrics)

        assert isinstance(yaml_str, str)
        assert "test_counter" in yaml_str
        assert "test_metrics_gauge" in yaml_str

        # Verify it's valid YAML
        data = yaml.safe_load(yaml_str)
        assert "test_counter" in data
        assert "test_metrics_gauge" in data

    def test_utf8_support(self, sample_metrics):
        """Test UTF-8 character support."""
        sample_metrics["中文指标"] = MetricInfo(
            name="中文指标",
            type="counter",
            help="中文帮助文本",
            labels=[],
            usages=[],
        )

        yaml_str = export_to_yaml_string(sample_metrics)
        assert "中文指标" in yaml_str
        assert "中文帮助文本" in yaml_str
