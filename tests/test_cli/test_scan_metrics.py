"""Functional tests for the scan-metrics command."""

import json

import yaml
from click.testing import CliRunner

from upcast.main import main


def _create_metrics_project(tmp_project):
    return tmp_project({
        "app.py": """
from prometheus_client import Counter

HTTP_REQUESTS = Counter('http_requests_total', 'Total HTTP requests')
""",
        "ignored.py": """
from prometheus_client import Gauge

IGNORED_METRIC = Gauge('ignored_metric', 'Ignored metric')
""",
    })


def test_scan_metrics_outputs_yaml(tmp_project):
    """The command should emit YAML results to stdout by default."""
    project_dir = _create_metrics_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-metrics", str(project_dir)])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_metrics"] == 2
    assert "http_requests_total" in output["results"]
    assert output["results"]["http_requests_total"]["type"] == "Counter"


def test_scan_metrics_writes_json_file(tmp_project, tmp_path):
    """The command should write JSON output when requested."""
    project_dir = _create_metrics_project(tmp_project)
    output_file = tmp_path / "metrics.json"
    runner = CliRunner()

    result = runner.invoke(
        main,
        ["scan-metrics", str(project_dir), "--format", "json", "--output", str(output_file)],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert f"Results written to: {output_file}" in result.output

    output = json.loads(output_file.read_text())
    assert output["summary"]["total_metrics"] == 2
    assert output["results"]["ignored_metric"]["type"] == "Gauge"


def test_scan_metrics_honors_exclude_pattern(tmp_project):
    """The command should exclude matching files from scanning."""
    project_dir = _create_metrics_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-metrics", str(project_dir), "--exclude", "ignored.py"])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_metrics"] == 1
    assert "http_requests_total" in output["results"]
    assert "ignored_metric" not in output["results"]
