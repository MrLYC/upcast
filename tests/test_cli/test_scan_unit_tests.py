"""Functional tests for the scan-unit-tests command."""

import json

import yaml
from click.testing import CliRunner

from upcast.main import main


def _create_unit_tests_project(tmp_project):
    return tmp_project({
        "tests/test_users.py": """
from myapp.models import User
from other.lib import Helper


def test_user_creation():
    user = User()
    helper = Helper()
    assert user is not None
    assert helper is not None
""",
        "tests.py": """
def test_legacy_case():
    assert True
""",
    })


def test_scan_unit_tests_outputs_yaml(tmp_project):
    """The command should emit unit test results to stdout by default."""
    project_dir = _create_unit_tests_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-unit-tests", str(project_dir)])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_tests"] == 2
    assert output["summary"]["total_files"] == 2
    assert "tests/test_users.py" in output["results"]
    assert "tests.py" in output["results"]


def test_scan_unit_tests_writes_json_file(tmp_project, tmp_path):
    """The command should write JSON output when requested."""
    project_dir = _create_unit_tests_project(tmp_project)
    output_file = tmp_path / "unit-tests.json"
    runner = CliRunner()

    result = runner.invoke(
        main,
        ["scan-unit-tests", str(project_dir), "--format", "json", "--output", str(output_file)],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert f"Results written to: {output_file}" in result.output

    output = json.loads(output_file.read_text())
    assert output["summary"]["total_tests"] == 2
    assert output["summary"]["total_assertions"] == 3
    assert "tests/test_users.py" in output["results"]


def test_scan_unit_tests_respects_root_modules(tmp_project):
    """The root-modules option should filter detected target modules."""
    project_dir = _create_unit_tests_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-unit-tests", str(project_dir), "--root-modules", "myapp"])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    targets = output["results"]["tests/test_users.py"][0]["targets"]
    assert len(targets) == 1
    assert targets[0]["module_path"] == "myapp.models"
    assert targets[0]["symbols"] == ["User"]


def test_scan_unit_tests_rejects_empty_project(tmp_path):
    """The command should fail when no matching Python files are available."""
    runner = CliRunner()

    result = runner.invoke(main, ["scan-unit-tests", str(tmp_path)])

    assert result.exit_code != 0
    assert "No Python files found to scan" in result.output
