"""Functional tests for the scan-complexity-patterns command."""

import json

import yaml
from click.testing import CliRunner

from upcast.main import main


def _create_complexity_project(tmp_project):
    return tmp_project({
        "app.py": """
def complex_enough(value):
    if value > 0:
        value += 1
    if value % 2:
        value += 2
    for _ in range(2):
        value += 3
    return value


def simple():
    return 1
"""
    })


def test_scan_complexity_patterns_outputs_yaml(tmp_project):
    """The command should emit YAML results for functions above the threshold."""
    project_dir = _create_complexity_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-complexity-patterns", str(project_dir), "--threshold", "4"])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_count"] == 1
    assert output["summary"]["high_complexity_count"] == 1
    assert output["results"]["app.py"][0]["name"] == "complex_enough"
    assert output["results"]["app.py"][0]["complexity"] == 4


def test_scan_complexity_patterns_writes_json_file(tmp_project, tmp_path):
    """The command should write JSON output when requested."""
    project_dir = _create_complexity_project(tmp_project)
    output_file = tmp_path / "complexity.json"
    runner = CliRunner()

    result = runner.invoke(
        main,
        [
            "scan-complexity-patterns",
            str(project_dir),
            "--threshold",
            "4",
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
    assert output["summary"]["total_count"] == 1
    assert output["results"]["app.py"][0]["name"] == "complex_enough"


def test_scan_complexity_patterns_respects_threshold(tmp_project):
    """The threshold option should change which functions are reported."""
    project_dir = _create_complexity_project(tmp_project)
    runner = CliRunner()

    threshold_four = runner.invoke(main, ["scan-complexity-patterns", str(project_dir), "--threshold", "4"])
    threshold_five = runner.invoke(main, ["scan-complexity-patterns", str(project_dir), "--threshold", "5"])

    assert threshold_four.exit_code == 0
    assert threshold_five.exit_code == 0

    output_four = yaml.safe_load(threshold_four.output)
    output_five = yaml.safe_load(threshold_five.output)
    assert output_four["summary"]["total_count"] == 1
    assert output_five["summary"]["total_count"] == 0
    assert output_five["results"] == {}
