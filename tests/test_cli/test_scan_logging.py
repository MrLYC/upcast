"""Functional tests for the scan-logging command."""

import json

import yaml
from click.testing import CliRunner

from upcast.main import main


def _create_logging_project(tmp_project):
    return tmp_project({
        "app.py": """
import logging


logger = logging.getLogger(__name__)


def log_values(api_endpoint, password):
    logger.info("Endpoint %s", api_endpoint)
    logger.error("Password %s", password)
"""
    })


def test_scan_logging_outputs_yaml(tmp_project):
    """The command should emit YAML logging results to stdout."""
    project_dir = _create_logging_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-logging", str(project_dir)])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_log_calls"] == 2
    assert output["summary"]["sensitive_calls"] == 1
    assert output["summary"]["by_level"] == {"error": 1, "info": 1}

    file_info = output["results"]["app.py"]
    password_call = next(call for call in file_info["logging"] if call["level"] == "error")
    assert "password" in {pattern.lower() for pattern in password_call["sensitive_patterns"]}


def test_scan_logging_writes_json_file(tmp_project, tmp_path):
    """The command should write JSON output when requested."""
    project_dir = _create_logging_project(tmp_project)
    output_file = tmp_path / "logging.json"
    runner = CliRunner()

    result = runner.invoke(
        main,
        ["scan-logging", str(project_dir), "--format", "json", "--output", str(output_file)],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert f"Results written to: {output_file}" in result.output

    output = json.loads(output_file.read_text())
    assert output["summary"]["total_log_calls"] == 2
    assert output["summary"]["by_library"]["logging"] == 2


def test_scan_logging_respects_sensitive_keywords_option(tmp_project):
    """Custom sensitive keywords should change sensitive logging detection."""
    project_dir = _create_logging_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(
        main,
        ["scan-logging", str(project_dir), "--sensitive-keywords", "api_endpoint"],
    )

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["sensitive_calls"] == 1

    file_info = output["results"]["app.py"]
    endpoint_call = next(call for call in file_info["logging"] if call["level"] == "info")
    password_call = next(call for call in file_info["logging"] if call["level"] == "error")
    assert "api_endpoint" in endpoint_call["sensitive_patterns"]
    assert password_call["sensitive_patterns"] == []
