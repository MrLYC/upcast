"""Tests for the current-main project analysis report generator."""

from pathlib import Path

import pytest
import yaml

from upcast.report_generator import ReportGenerator


def _write_result(directory: Path, name: str, payload: dict) -> None:
    (directory / f"{name}.yaml").write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def test_report_generator_loads_results_and_emits_deterministic_summary(tmp_path):
    _write_result(
        tmp_path,
        "unit-tests",
        {
            "summary": {"files_scanned": 2, "total_count": 3, "total_tests": 3},
            "results": {"tests|module.py": [{"name": "test_login", "line": 10}]},
        },
    )
    _write_result(
        tmp_path,
        "complexity-patterns",
        {
            "summary": {
                "files_scanned": 1,
                "total_count": 2,
                "high_complexity_count": 1,
                "by_severity": {"critical": 1, "warning": 1},
            },
            "results": {"module.py": [{"name": "build|plan", "complexity": 21, "line": 4}]},
        },
    )

    generator = ReportGenerator(tmp_path)
    generator.load_results()
    first = generator.generate_report()
    second = ReportGenerator(tmp_path).generate_report()

    assert first == second
    assert "# Project Analysis Report" in first
    assert "**Scan Types**: 2" in first
    assert "**Total Files Scanned**: 3" in first
    assert "**Total Findings**: 5" in first
    assert "## Code Quality Analysis" in first
    assert "build\\|plan" in first
    assert "## Testing & Reliability" in first


def test_report_generator_tolerates_partial_results_and_escapes_table_cells(tmp_path):
    _write_result(
        tmp_path,
        "http-requests",
        {
            "summary": {"total_count": 1, "files_scanned": 1},
            "results": {"https://example.test/a|b": {"method": "GET", "library": "requests"}},
        },
    )
    _write_result(tmp_path, "future-scanner", {"new_field": {"nested": True}})

    report = ReportGenerator(tmp_path).generate_report()

    assert "## External Dependencies" in report
    assert "https://example.test/a\\|b" in report
    assert "future-scanner" not in report


def test_report_generator_rejects_missing_input_directory(tmp_path):
    with pytest.raises(FileNotFoundError):
        ReportGenerator(tmp_path / "missing").load_results()
