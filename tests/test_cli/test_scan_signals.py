"""Functional tests for the scan-signals command."""

import json

import yaml
from click.testing import CliRunner

from upcast.main import main


def _create_signals_project(tmp_project):
    return tmp_project({
        "signals.py": """
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender='Book')
def on_book_saved(sender, **kwargs):
    return None
""",
        "ignored.py": """
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender='Author')
def on_author_saved(sender, **kwargs):
    return None
""",
    })


def test_scan_signals_outputs_yaml(tmp_project):
    """The command should emit YAML signal results to stdout."""
    project_dir = _create_signals_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-signals", str(project_dir)])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_count"] == 2
    assert output["summary"]["django_receivers"] == 2
    signals = {signal["signal"] for signal in output["results"]}
    assert signals == {"post_save", "pre_save"}


def test_scan_signals_writes_json_file(tmp_project, tmp_path):
    """The command should write JSON output when requested."""
    project_dir = _create_signals_project(tmp_project)
    output_file = tmp_path / "signals.json"
    runner = CliRunner()

    result = runner.invoke(
        main,
        ["scan-signals", str(project_dir), "--format", "json", "--output", str(output_file)],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert f"Results written to: {output_file}" in result.output

    output = json.loads(output_file.read_text())
    assert output["summary"]["total_count"] == 2
    assert len(output["results"]) == 2


def test_scan_signals_honors_exclude_pattern(tmp_project):
    """The command should exclude matching files from scanning."""
    project_dir = _create_signals_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-signals", str(project_dir), "--exclude", "ignored.py"])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_count"] == 1
    assert output["summary"]["django_receivers"] == 1
    assert [signal["signal"] for signal in output["results"]] == ["post_save"]
