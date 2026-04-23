"""Functional tests for the scan-exception-handlers command."""

import json

import yaml
from click.testing import CliRunner

from upcast.main import main


def _create_exception_handler_project(tmp_project):
    return tmp_project({
        "app.py": """
def parse_value(raw):
    try:
        return int(raw)
    except ValueError:
        return 0
""",
        "ignored.py": """
def read_mapping(data):
    try:
        return data['name']
    except KeyError:
        return 'missing'
""",
    })


def test_scan_exception_handlers_outputs_yaml(tmp_project):
    """The command should emit YAML results to stdout by default."""
    project_dir = _create_exception_handler_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-exception-handlers", str(project_dir)])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_handlers"] == 2
    assert output["summary"]["total_except_clauses"] == 2
    assert output["results"][0]["exception_blocks"][0]["exceptions"] == ["ValueError"]


def test_scan_exception_handlers_writes_json_file(tmp_project, tmp_path):
    """The command should write JSON output when requested."""
    project_dir = _create_exception_handler_project(tmp_project)
    output_file = tmp_path / "exception-handlers.json"
    runner = CliRunner()

    result = runner.invoke(
        main,
        [
            "scan-exception-handlers",
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
    assert output["summary"]["total_handlers"] == 2
    all_exceptions = [block["exceptions"] for item in output["results"] for block in item["exception_blocks"]]
    assert ["KeyError"] in all_exceptions


def test_scan_exception_handlers_honors_exclude_pattern(tmp_project):
    """The command should exclude matching files from scanning."""
    project_dir = _create_exception_handler_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-exception-handlers", str(project_dir), "--exclude", "ignored.py"])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_handlers"] == 1
    assert output["summary"]["total_except_clauses"] == 1
    assert output["results"][0]["exception_blocks"][0]["exceptions"] == ["ValueError"]
