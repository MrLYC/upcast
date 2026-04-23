"""Functional tests for the scan-concurrency-patterns command."""

import json

import yaml
from click.testing import CliRunner

from upcast.main import main


def _create_concurrency_project(tmp_project):
    return tmp_project({
        "app.py": """
import threading

def worker():
    return None

def create_thread():
    thread = threading.Thread(target=worker)
    thread.start()
""",
        "ignored.py": """
import multiprocessing

def worker():
    return None

def create_process():
    process = multiprocessing.Process(target=worker)
    process.start()
""",
    })


def _usage_count(patterns):
    return sum(len(usages) for usages in patterns.values())


def test_scan_concurrency_patterns_outputs_yaml(tmp_project):
    """The command should emit YAML results to stdout by default."""
    project_dir = _create_concurrency_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-concurrency-patterns", str(project_dir)])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_count"] == 2
    assert output["summary"]["by_category"]["threading"] >= 1
    assert _usage_count(output["results"]["threading"]) >= 1


def test_scan_concurrency_patterns_writes_json_file(tmp_project, tmp_path):
    """The command should write JSON output when requested."""
    project_dir = _create_concurrency_project(tmp_project)
    output_file = tmp_path / "concurrency-patterns.json"
    runner = CliRunner()

    result = runner.invoke(
        main,
        [
            "scan-concurrency-patterns",
            str(project_dir),
            "--format",
            "json",
            "--output",
            str(output_file),
        ],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    assert f"Results written to: {output_file}" in result.output

    output = json.loads(output_file.read_text())
    assert output["summary"]["total_count"] == 2
    assert _usage_count(output["results"]["multiprocessing"]) >= 1


def test_scan_concurrency_patterns_honors_exclude_pattern(tmp_project):
    """The command should exclude matching files from scanning."""
    project_dir = _create_concurrency_project(tmp_project)
    runner = CliRunner()

    result = runner.invoke(main, ["scan-concurrency-patterns", str(project_dir), "--exclude", "ignored.py"])

    assert result.exit_code == 0

    output = yaml.safe_load(result.output)
    assert output["summary"]["total_count"] == 1
    assert output["summary"]["by_category"] == {"threading": 1}
    assert _usage_count(output["results"]["multiprocessing"]) == 0
