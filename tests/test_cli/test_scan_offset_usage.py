"""Functional tests for the scan-offset-usage command."""

import json

import yaml
from click.testing import CliRunner

from upcast.main import main


def _create_offset_project(tmp_project):
    return tmp_project({
        "views.py": """
from app.models import User

page = request.GET.get("page")
page_size = 25
users = User.objects.order_by("id")
result = users[(page - 1) * page_size : page * page_size]
""",
        "ignored.py": """
from app.models import User
result = User.objects.all()[100:150]
""",
    })


def test_scan_offset_usage_outputs_yaml(tmp_project):
    project_dir = _create_offset_project(tmp_project)
    result = CliRunner().invoke(main, ["scan-offset-usage", str(project_dir)])

    assert result.exit_code == 0
    output = yaml.safe_load(result.output)
    assert output["summary"]["total_count"] == 2
    assert output["results"]["queryset_slice"]


def test_scan_offset_usage_writes_json_and_honors_exclude(tmp_project, tmp_path):
    project_dir = _create_offset_project(tmp_project)
    output_file = tmp_path / "offset-usage.json"
    result = CliRunner().invoke(
        main,
        [
            "scan-offset-usage",
            str(project_dir),
            "--format",
            "json",
            "--output",
            str(output_file),
            "--exclude",
            "ignored.py",
        ],
    )

    assert result.exit_code == 0
    output = json.loads(output_file.read_text())
    assert output["summary"]["total_count"] == 1


def test_scan_offset_usage_help_describes_supported_patterns():
    result = CliRunner().invoke(main, ["scan-offset-usage", "--help"])

    assert result.exit_code == 0
    assert "QuerySet" in result.output
    assert "Paginator" in result.output
    assert "--include" in result.output
    assert "--exclude" in result.output
