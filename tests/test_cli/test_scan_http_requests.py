"""Functional tests for the scan-http-requests command."""

import json

import yaml
from click.testing import CliRunner

from upcast.main import main


def _create_http_requests_project(tmp_project):
    return tmp_project({
        "app.py": """
import requests

response = requests.get('https://api.example.com/users')
""",
        "ignored.py": """
import requests

response = requests.post('https://ignored.example.com/users')
""",
    })


def test_scan_http_requests_outputs_yaml(tmp_project):
    """The command should emit YAML results to stdout by default."""
    project_dir = _create_http_requests_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-http-requests", str(project_dir)])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_requests"] == 2
    assert "https://api.example.com/users" in output["results"]
    assert output["results"]["https://api.example.com/users"]["method"] == "GET"


def test_scan_http_requests_writes_json_file(tmp_project, tmp_path):
    """The command should write JSON output when requested."""
    project_dir = _create_http_requests_project(tmp_project)
    output_file = tmp_path / "http-requests.json"
    runner = CliRunner()

    result = runner.invoke(
        main,
        ["scan-http-requests", str(project_dir), "--format", "json", "--output", str(output_file)],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert f"Results written to: {output_file}" in result.output

    output = json.loads(output_file.read_text())
    assert output["summary"]["total_requests"] == 2
    assert output["results"]["https://ignored.example.com/users"]["method"] == "POST"


def test_scan_http_requests_honors_exclude_pattern(tmp_project):
    """The command should exclude matching files from scanning."""
    project_dir = _create_http_requests_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-http-requests", str(project_dir), "--exclude", "ignored.py"])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_requests"] == 1
    assert "https://api.example.com/users" in output["results"]
    assert "https://ignored.example.com/users" not in output["results"]
