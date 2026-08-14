"""Functional tests for the scan-django-views command."""

import json

import yaml
from click.testing import CliRunner

from upcast.main import main


def _create_django_views_project(tmp_project):
    return tmp_project(
        {
            "app/views.py": '''
from rest_framework.decorators import api_view


@api_view(["GET"])
def health(request):
    return None
''',
            "app/other.py": '''
from rest_framework.decorators import api_view


@api_view(["GET"])
def ignored_by_include(request):
    return None
''',
            "app/urls.py": '''
from django.urls import path
from .views import health

urlpatterns = [path("health/", health)]
urlpatterns.append(path("dynamic/", build_callback()))
''',
        }
    )


def test_scan_django_views_outputs_yaml(tmp_project):
    """The command emits view records as YAML by default."""
    project_dir = _create_django_views_project(tmp_project)
    result = CliRunner().invoke(main, ["scan-django-views", str(project_dir)])

    assert result.exit_code == 0
    output = yaml.safe_load(result.output)
    assert output["summary"]["total_views"] == 2
    assert output["results"]["app.views.health"]["route_refs"][0]["pattern"] == "health/"
    assert len(output["unresolved_route_references"]) == 1


def test_scan_django_views_writes_json_and_honors_include_pattern(tmp_project, tmp_path):
    """JSON output and explicit all-file filters follow standard scanner conventions."""
    project_dir = _create_django_views_project(tmp_project)
    output_file = tmp_path / "django-views.json"
    runner = CliRunner()

    result = runner.invoke(
        main,
        [
            "scan-django-views",
            str(project_dir),
            "--include",
            "**/views.py",
            "--format",
            "json",
            "--output",
            str(output_file),
        ],
    )

    assert result.exit_code == 0
    assert f"Results written to: {output_file}" in result.output
    output = json.loads(output_file.read_text())
    assert output["summary"]["total_views"] == 1
    assert list(output["results"]) == ["app.views.health"]


def test_scan_django_views_renders_markdown(tmp_project):
    """The command supports the project-standard Markdown output mode."""
    project_dir = _create_django_views_project(tmp_project)
    result = CliRunner().invoke(main, ["scan-django-views", str(project_dir), "--format", "markdown"])

    assert result.exit_code == 0
    assert "Django View Analysis" in result.output
    assert "app.views.health" in result.output
    assert "Unresolved route references" in result.output
    assert "build_callback()" in result.output


def test_scan_django_views_rejects_empty_projects_and_explains_semantic_discovery(tmp_path):
    """The command reports empty inputs and help avoids a filename-based promise."""
    runner = CliRunner()

    empty_result = runner.invoke(main, ["scan-django-views", str(tmp_path)])
    help_result = runner.invoke(main, ["scan-django-views", "--help"])

    assert empty_result.exit_code != 0
    assert "No Python files found to scan" in empty_result.output
    assert help_result.exit_code == 0
    assert "semantic" in help_result.output.lower()
    assert "--include" in help_result.output
