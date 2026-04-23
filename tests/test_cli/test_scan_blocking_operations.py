"""Functional tests for the scan-blocking-operations command."""

import json

import yaml
from click.testing import CliRunner

from upcast.main import main


def _create_blocking_operations_project(tmp_project):
    return tmp_project({
        "app.py": """
import time

def wait_for_data():
    time.sleep(1)
""",
        "ignored.py": """
import subprocess

def run_shell():
    subprocess.run(['ls'], timeout=3)
""",
    })


def test_scan_blocking_operations_outputs_yaml(tmp_project):
    """The command should emit YAML results to stdout by default."""
    project_dir = _create_blocking_operations_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-blocking-operations", str(project_dir)])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_count"] == 2
    assert output["summary"]["by_category"]["time_based"] == 1
    assert output["summary"]["by_category"]["subprocess"] == 1
    assert output["results"]["time_based"][0]["operation"] == "time.sleep"


def test_scan_blocking_operations_writes_json_file(tmp_project, tmp_path):
    """The command should write JSON output when requested."""
    project_dir = _create_blocking_operations_project(tmp_project)
    output_file = tmp_path / "blocking-operations.json"
    runner = CliRunner()

    result = runner.invoke(
        main,
        [
            "scan-blocking-operations",
            str(project_dir),
            "--format",
            "json",
            "--output",
            str(output_file),
        ],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert f"Results written to: {output_file}" in result.output

    output = json.loads(output_file.read_text())
    assert output["summary"]["total_count"] == 2
    assert output["results"]["subprocess"][0]["operation"] == "subprocess.run"


def test_scan_blocking_operations_honors_exclude_pattern(tmp_project):
    """The command should exclude matching files from scanning."""
    project_dir = _create_blocking_operations_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(
        main,
        ["scan-blocking-operations", str(project_dir), "--exclude", "ignored.py"],
    )

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_count"] == 1
    assert output["summary"]["by_category"] == {"time_based": 1}
    assert output["results"]["subprocess"] == []
