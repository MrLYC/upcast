"""Functional tests for the scan-env-vars command."""

import json

import yaml
from click.testing import CliRunner

from upcast.main import main


def _create_env_var_project(tmp_project):
    return tmp_project({
        "app.py": """
import os

gateway = os.getenv('AIDEV_GATEWAY_NAME')
secret = os.environ['AIDEV_SECRET']
""",
        "ignored.py": """
import os

ignored = os.getenv('IGNORED_ENV')
""",
    })


def test_scan_env_vars_outputs_yaml(tmp_project):
    """The command should emit YAML results to stdout by default."""
    project_dir = _create_env_var_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-env-vars", str(project_dir)])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_count"] == 3
    assert "AIDEV_GATEWAY_NAME" in output["results"]
    assert output["results"]["AIDEV_GATEWAY_NAME"]["types"] == ["str"]
    assert output["results"]["AIDEV_SECRET"]["required"] is True


def test_scan_env_vars_writes_json_file(tmp_project, tmp_path):
    """The command should write JSON output when requested."""
    project_dir = _create_env_var_project(tmp_project)
    output_file = tmp_path / "env-vars.json"
    runner = CliRunner()

    result = runner.invoke(
        main,
        ["scan-env-vars", str(project_dir), "--format", "json", "--output", str(output_file)],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert f"Results written to: {output_file}" in result.output

    output = json.loads(output_file.read_text())
    assert output["summary"]["total_count"] == 3
    assert "AIDEV_GATEWAY_NAME" in output["results"]
    assert output["results"]["AIDEV_SECRET"]["types"] == ["str"]


def test_scan_env_vars_honors_exclude_pattern(tmp_project):
    """The command should exclude matching files from scanning."""
    project_dir = _create_env_var_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-env-vars", str(project_dir), "--exclude", "ignored.py"])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_count"] == 2
    assert "AIDEV_GATEWAY_NAME" in output["results"]
    assert "AIDEV_SECRET" in output["results"]
    assert "IGNORED_ENV" not in output["results"]


def test_scan_env_vars_rejects_empty_project(tmp_path):
    """The command should fail when no Python files are available."""
    runner = CliRunner()

    result = runner.invoke(main, ["scan-env-vars", str(tmp_path)])

    assert result.exit_code != 0
    assert "No Python files found to scan" in result.output


def test_scan_env_vars_rejects_invalid_path():
    """The command should fail fast when the scan path does not exist."""
    runner = CliRunner()

    result = runner.invoke(main, ["scan-env-vars", "/path/that/does/not/exist"])

    assert result.exit_code != 0
    assert "Path '/path/that/does/not/exist' does not exist" in result.output
