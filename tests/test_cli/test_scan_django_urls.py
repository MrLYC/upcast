"""Functional tests for the scan-django-urls command."""

import json

import yaml
from click.testing import CliRunner

from upcast.main import main


def _create_django_urls_project(tmp_project):
    return tmp_project({
        "myapp/urls.py": """
from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book-list'),
]
""",
        "ignored_urls.py": """
from django.urls import path
from . import views

urlpatterns = [
    path('ignored/', views.ignored, name='ignored'),
]
""",
    })


def test_scan_django_urls_outputs_yaml(tmp_project):
    """The command should emit Django URL results to stdout by default."""
    project_dir = _create_django_urls_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-django-urls", str(project_dir)])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_modules"] == 2
    assert output["summary"]["total_patterns"] == 2
    assert "ignored_urls" in output["results"]
    assert "myapp.urls" in output["results"]
    pattern = output["results"]["myapp.urls"]["urlpatterns"][0]
    assert pattern["pattern"] == "books/"
    assert pattern["name"] == "book-list"


def test_scan_django_urls_writes_json_file(tmp_project, tmp_path):
    """The command should write JSON output when requested."""
    project_dir = _create_django_urls_project(tmp_project)
    output_file = tmp_path / "django-urls.json"
    runner = CliRunner()

    result = runner.invoke(
        main,
        ["scan-django-urls", str(project_dir), "--format", "json", "--output", str(output_file)],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert f"Results written to: {output_file}" in result.output

    output = json.loads(output_file.read_text())
    assert output["summary"]["total_modules"] == 2
    assert output["summary"]["total_patterns"] == 2
    assert "myapp.urls" in output["results"]
    assert "ignored_urls" in output["results"]


def test_scan_django_urls_honors_include_pattern(tmp_project):
    """The include option currently expands matching URL file patterns without narrowing defaults."""
    project_dir = _create_django_urls_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-django-urls", str(project_dir), "--include", "**/*_urls.py"])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_modules"] == 2
    assert output["summary"]["total_patterns"] == 2
    assert "ignored_urls" in output["results"]
    assert "myapp.urls" in output["results"]


def test_scan_django_urls_rejects_empty_project(tmp_path):
    """The command should fail when no matching Python files are available."""
    runner = CliRunner()

    result = runner.invoke(main, ["scan-django-urls", str(tmp_path)])

    assert result.exit_code != 0
    assert "No Python files found to scan" in result.output
