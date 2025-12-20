"""Integration tests for blocking operation scanner."""

from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from upcast.blocking_operation_scanner.checker import BlockingOperationChecker
from upcast.blocking_operation_scanner.cli import scan_blocking_operations


@pytest.fixture
def sample_project(tmp_path):
    """Create a sample project with blocking operations."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()

    # Create file with mixed operations
    (project_dir / "app.py").write_text(
        """
import time
import threading
import subprocess

async def handler():
    # Anti-pattern: blocking in async
    time.sleep(5)
    threading.Lock().acquire(timeout=10)
    subprocess.run(['ls'], timeout=30)
"""
    )

    # Create file with Django locks
    (project_dir / "models.py").write_text(
        """
def update_user():
    user = User.objects.filter(id=1).select_for_update(timeout=60).first()
    user.save()
"""
    )

    return project_dir


def test_end_to_end_scan(sample_project):
    """Test end-to-end scanning of a project."""
    checker = BlockingOperationChecker()

    all_operations = []
    for file_path in sample_project.glob("*.py"):
        operations = checker.check_file(file_path)
        all_operations.extend(operations)

    assert len(all_operations) > 0

    # Check we found different types
    types = {op.type.value for op in all_operations}
    assert "time_based.sleep" in types
    assert "synchronization.lock_acquire" in types
    assert "subprocess.run" in types


def test_cli_basic_scan(sample_project):
    """Test CLI with basic scan."""
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(
            scan_blocking_operations,
            [str(sample_project)],
        )

        assert result.exit_code == 0
        assert "summary" in result.output


def test_cli_yaml_output(sample_project, tmp_path):
    """Test CLI with YAML output to file."""
    runner = CliRunner()
    output_file = tmp_path / "output.yaml"

    result = runner.invoke(
        scan_blocking_operations,
        [str(sample_project), "-o", str(output_file), "--format", "yaml"],
    )

    assert result.exit_code == 0
    assert output_file.exists()

    data = yaml.safe_load(output_file.read_text())
    assert "summary" in data
    assert "operations" in data


def test_cli_json_output(sample_project, tmp_path):
    """Test CLI with JSON output."""
    runner = CliRunner()
    output_file = tmp_path / "output.json"

    result = runner.invoke(
        scan_blocking_operations,
        [str(sample_project), "-o", str(output_file), "--format", "json"],
    )

    assert result.exit_code == 0
    assert output_file.exists()

    import json

    data = json.loads(output_file.read_text())
    assert "summary" in data


def test_cli_verbose(sample_project):
    """Test CLI with verbose output."""
    runner = CliRunner()

    result = runner.invoke(
        scan_blocking_operations,
        [str(sample_project), "-v"],
    )

    assert result.exit_code == 0


def test_cli_file_filtering(tmp_path):
    """Test CLI with file filtering."""
    # Create files
    (tmp_path / "app.py").write_text("import time\ntime.sleep(1)")
    (tmp_path / "test.py").write_text("import time\ntime.sleep(2)")

    runner = CliRunner()

    # Exclude test files
    result = runner.invoke(
        scan_blocking_operations,
        [str(tmp_path), "--exclude", "test*.py"],
    )

    assert result.exit_code == 0
    # Should not include test.py
    output_data = yaml.safe_load(result.output)
    assert output_data["summary"]["files_analyzed"] == 1


def test_cli_include_pattern(tmp_path):
    """Test CLI with include pattern."""
    # Create subdirectories
    app_dir = tmp_path / "app"
    app_dir.mkdir()
    (app_dir / "main.py").write_text("import time\ntime.sleep(1)")

    test_dir = tmp_path / "tests"
    test_dir.mkdir()
    (test_dir / "test_main.py").write_text("import time\ntime.sleep(2)")

    runner = CliRunner()

    # Only include app directory
    result = runner.invoke(
        scan_blocking_operations,
        [str(tmp_path), "--include", "app/**"],
    )

    assert result.exit_code == 0
    output_data = yaml.safe_load(result.output)
    assert output_data["summary"]["files_analyzed"] == 1


def test_cli_no_files_found(tmp_path):
    """Test CLI when no Python files are found."""
    runner = CliRunner()

    result = runner.invoke(
        scan_blocking_operations,
        [str(tmp_path)],
    )

    # CLI should still succeed and output empty summary
    assert result.exit_code == 0
    assert "total_operations: 0" in result.output


def test_detects_async_anti_patterns(tmp_path):
    """Test detecting blocking operations in async functions."""
    file_path = tmp_path / "async_bad.py"
    file_path.write_text(
        """
import time
import threading

async def bad_async():
    time.sleep(5)  # Anti-pattern
    threading.Lock().acquire()  # Anti-pattern
"""
    )

    checker = BlockingOperationChecker()
    operations = checker.check_file(file_path)

    # Should detect both operations
    assert len(operations) == 2
    # Both should be flagged as in async context
    assert all(op.is_async_context for op in operations)


def test_scan_real_fixture_files():
    """Test scanning the actual fixture files."""
    fixtures_dir = Path(__file__).parent
    sample_file = fixtures_dir / "sample_blocking_ops.py"

    if not sample_file.exists():
        pytest.skip("Fixture file not found")

    checker = BlockingOperationChecker()
    operations = checker.check_file(sample_file)

    # Should find multiple operations
    assert len(operations) > 5

    # Check for specific operation types
    types = {op.type.value for op in operations}
    assert "time_based.sleep" in types
    assert "synchronization.lock_acquire" in types or "synchronization.lock_context" in types
    assert "subprocess.run" in types or "subprocess.wait" in types
