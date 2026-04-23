"""Functional tests for the scan-django-settings command."""

import json

import yaml
from click.testing import CliRunner

from upcast.main import main


def _create_django_settings_project(tmp_project):
    return tmp_project({
        "settings.py": """
DEBUG = True
SECRET_KEY = 'test-secret'
""",
        "views.py": """
from django.conf import settings


enabled = settings.DEBUG
""",
    })


def test_scan_django_settings_outputs_yaml(tmp_project):
    """The command should emit YAML settings results to stdout."""
    project_dir = _create_django_settings_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-django-settings", str(project_dir)])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_settings"] == 2
    assert output["summary"]["total_definitions"] == 2
    assert output["summary"]["total_usages"] == 1
    assert "DEBUG" in output["results"]
    assert output["results"]["DEBUG"]["usage_count"] == 1


def test_scan_django_settings_writes_json_file(tmp_project, tmp_path):
    """The command should write JSON output when requested."""
    project_dir = _create_django_settings_project(tmp_project)
    output_file = tmp_path / "django-settings.json"
    runner = CliRunner()

    result = runner.invoke(
        main,
        ["scan-django-settings", str(project_dir), "--format", "json", "--output", str(output_file)],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert f"Results written to: {output_file}" in result.output

    output = json.loads(output_file.read_text())
    assert output["summary"]["total_settings"] == 2
    assert output["results"]["SECRET_KEY"]["definition_count"] == 1


def test_scan_django_settings_verbose_reports_completion(tmp_project):
    """Verbose mode should print the command-specific completion message."""
    project_dir = _create_django_settings_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-django-settings", str(project_dir), "--verbose"])

    assert result.exit_code == 0
    assert "Scan complete!" in result.stderr
