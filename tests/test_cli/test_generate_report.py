"""CLI tests for project analysis report generation."""

from pathlib import Path

import yaml
from click.testing import CliRunner

from upcast.main import main


def _write_result(directory: Path, name: str, payload: dict) -> None:
    (directory / f"{name}.yaml").write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def test_generate_report_writes_markdown_to_requested_output(tmp_path):
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    _write_result(results_dir, "complexity-patterns", {"summary": {"total_count": 1, "files_scanned": 1}})
    output_file = tmp_path / "reports" / "analysis.md"

    result = CliRunner().invoke(main, ["generate-report", str(results_dir), "--output", str(output_file)])

    assert result.exit_code == 0, result.output
    assert output_file.exists()
    assert "Report saved to:" in result.output
    assert "# Project Analysis Report" in output_file.read_text(encoding="utf-8")
    assert "# Project Analysis Report" not in result.output


def test_generate_report_prints_markdown_and_help_describes_input(tmp_path):
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    _write_result(results_dir, "unit-tests", {"summary": {"total_count": 2, "files_scanned": 1}})

    result = CliRunner().invoke(main, ["generate-report", str(results_dir)])
    help_result = CliRunner().invoke(main, ["generate-report", "--help"])

    assert result.exit_code == 0, result.output
    assert "# Project Analysis Report" in result.output
    assert help_result.exit_code == 0
    assert "scan results" in help_result.output.lower()
    assert "--output" in help_result.output
