"""Functional tests for the scan-django-views command."""

import yaml
from click.testing import CliRunner

from upcast.main import main


def test_scan_django_views_outputs_yaml(tmp_path):
    views_file = tmp_path / "app" / "views.py"
    views_file.parent.mkdir()
    views_file.write_text(
        """
from rest_framework.decorators import api_view

@api_view(["GET"])
def health(request):
    return None
"""
    )

    result = CliRunner().invoke(main, ["scan-django-views", str(tmp_path)])

    assert result.exit_code == 0, result.output
    output = yaml.safe_load(result.output)
    assert output["summary"]["total_count"] == 1
    assert output["results"]["app.views"][0]["name"] == "health"


def test_scan_django_views_outputs_markdown(tmp_path):
    views_file = tmp_path / "app" / "views.py"
    views_file.parent.mkdir()
    views_file.write_text(
        """
from rest_framework.decorators import api_view

@api_view(["GET"])
def health(request):
    return None
"""
    )
    output_file = tmp_path / "views.md"

    result = CliRunner().invoke(
        main,
        ["scan-django-views", str(tmp_path), "--format", "markdown", "--output", str(output_file)],
    )

    assert result.exit_code == 0, result.output
    assert "View Module: app.views" in output_file.read_text()
