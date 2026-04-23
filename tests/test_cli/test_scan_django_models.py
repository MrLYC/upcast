"""Functional tests for the scan-django-models command."""

import json

import yaml
from click.testing import CliRunner

from upcast.main import main


def _create_django_models_project(tmp_project):
    return tmp_project({
        "blog/models.py": """
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=100)
""",
        "ignored_models.py": """
from django.db import models


class IgnoredRecord(models.Model):
    code = models.CharField(max_length=20)
""",
    })


def test_scan_django_models_outputs_yaml(tmp_project):
    """The command should emit Django model results to stdout by default."""
    project_dir = _create_django_models_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-django-models", str(project_dir)])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_models"] == 2
    assert output["summary"]["total_fields"] == 2
    model_names = {model["name"] for model in output["results"].values()}
    assert model_names == {"Article", "IgnoredRecord"}


def test_scan_django_models_writes_json_file(tmp_project, tmp_path):
    """The command should write JSON output when requested."""
    project_dir = _create_django_models_project(tmp_project)
    output_file = tmp_path / "django-models.json"
    runner = CliRunner()

    result = runner.invoke(
        main,
        ["scan-django-models", str(project_dir), "--format", "json", "--output", str(output_file)],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert f"Results written to: {output_file}" in result.output

    output = json.loads(output_file.read_text())
    assert output["summary"]["total_models"] == 2
    assert output["summary"]["total_fields"] == 2
    model_names = {model["name"] for model in output["results"].values()}
    assert model_names == {"Article", "IgnoredRecord"}


def test_scan_django_models_honors_include_pattern(tmp_project):
    """The include option currently expands matching model file patterns without narrowing defaults."""
    project_dir = _create_django_models_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-django-models", str(project_dir), "--include", "**/*_models.py"])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_models"] == 2
    model_names = {model["name"] for model in output["results"].values()}
    assert model_names == {"Article", "IgnoredRecord"}


def test_scan_django_models_rejects_empty_project(tmp_path):
    """The command should fail when no matching Python files are available."""
    runner = CliRunner()

    result = runner.invoke(main, ["scan-django-models", str(tmp_path)])

    assert result.exit_code != 0
    assert "No Python files found to scan" in result.output
