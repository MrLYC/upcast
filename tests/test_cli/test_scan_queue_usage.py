"""Functional tests for the scan-queue-usage command."""

import json

import yaml
from click.testing import CliRunner

from upcast.main import main


def _create_queue_project(tmp_project):
    return tmp_project({
        "app.py": """
from queue import Queue

queue = Queue(maxsize=10)
queue.put("item", timeout=2)
""",
    })


def test_scan_queue_usage_outputs_yaml(tmp_project):
    project_dir = _create_queue_project(tmp_project)
    result = CliRunner().invoke(main, ["scan-queue-usage", str(project_dir)])

    assert result.exit_code == 0
    output = yaml.safe_load(result.output)
    assert output["summary"]["total_usages"] == 2
    assert output["results"]["in_process"]


def test_scan_queue_usage_writes_json_file(tmp_project, tmp_path):
    project_dir = _create_queue_project(tmp_project)
    output_file = tmp_path / "queue-usage.json"
    result = CliRunner().invoke(
        main,
        ["scan-queue-usage", str(project_dir), "--format", "json", "--output", str(output_file)],
    )

    assert result.exit_code == 0
    output = json.loads(output_file.read_text())
    assert output["summary"]["total_usages"] == 2


def test_scan_queue_usage_help_describes_supported_scan(tmp_path):
    result = CliRunner().invoke(main, ["scan-queue-usage", "--help"])

    assert result.exit_code == 0
    assert "queue" in result.output.lower()
    assert "--include" in result.output
    assert "--exclude" in result.output
