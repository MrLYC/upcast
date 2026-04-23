"""Functional tests for the scan-redis-usage command."""

import json

import yaml
from click.testing import CliRunner

from upcast.main import main


def _create_redis_usage_project(tmp_project):
    return tmp_project({
        "app.py": """
from django.core.cache import cache


def use_cache():
    cache.get('user:1')
""",
        "ignored.py": """
from django.core.cache import cache


def update_cache():
    cache.set('user:2', 'value', 300)
""",
    })


def test_scan_redis_usage_outputs_yaml(tmp_project):
    """The command should emit YAML Redis usage results to stdout."""
    project_dir = _create_redis_usage_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-redis-usage", str(project_dir)])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_usages"] == 2
    assert output["summary"]["categories"]["direct_client"] == 2
    operations = {usage["operation"] for usage in output["results"]["direct_client"]}
    assert operations == {"get", "set"}


def test_scan_redis_usage_writes_json_file(tmp_project, tmp_path):
    """The command should write JSON output when requested."""
    project_dir = _create_redis_usage_project(tmp_project)
    output_file = tmp_path / "redis-usage.json"
    runner = CliRunner()

    result = runner.invoke(
        main,
        ["scan-redis-usage", str(project_dir), "--format", "json", "--output", str(output_file)],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert f"Results written to: {output_file}" in result.output

    output = json.loads(output_file.read_text())
    assert output["summary"]["total_usages"] == 2
    assert len(output["results"]["direct_client"]) == 2


def test_scan_redis_usage_verbose_reports_progress(tmp_project):
    """Verbose mode should print the command-specific start and completion messages."""
    project_dir = _create_redis_usage_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-redis-usage", str(project_dir), "--verbose"])

    assert result.exit_code == 0
    assert f"Scanning for Redis usage in: {project_dir}" in result.stderr
    assert "Scan complete!" in result.stderr
