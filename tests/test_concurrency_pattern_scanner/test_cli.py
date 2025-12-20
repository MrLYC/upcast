"""Tests for CLI interface."""

import tempfile
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from upcast.concurrency_pattern_scanner.cli import scan_concurrency_patterns


@pytest.fixture
def runner():
    """Create CLI runner."""
    return CliRunner()


@pytest.fixture
def fixtures_dir():
    """Get fixtures directory path."""
    return Path(__file__).parent / "fixtures"


def test_scan_current_directory(runner, fixtures_dir):
    """Test scanning current directory."""
    result = runner.invoke(scan_concurrency_patterns, [str(fixtures_dir)])

    assert result.exit_code == 0
    # Output should contain YAML with concurrency_patterns
    assert "concurrency_patterns:" in result.output


def test_scan_with_output_file(runner, fixtures_dir):
    """Test scanning with output file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        output_file = f.name

    try:
        result = runner.invoke(scan_concurrency_patterns, [str(fixtures_dir), "-o", output_file])

        assert result.exit_code == 0

        # Check output file exists and contains valid YAML
        assert Path(output_file).exists()
        with open(output_file) as f:
            data = yaml.safe_load(f)
            assert "concurrency_patterns" in data
    finally:
        Path(output_file).unlink(missing_ok=True)


def test_scan_with_verbose(runner, fixtures_dir):
    """Test scanning with verbose output."""
    result = runner.invoke(scan_concurrency_patterns, [str(fixtures_dir), "-v"])

    assert result.exit_code == 0
    # Verbose output should show scanning info
    assert "Scanning" in result.output or "Summary" in result.output


def test_scan_with_include_pattern(runner, fixtures_dir):
    """Test scanning with include pattern."""
    result = runner.invoke(scan_concurrency_patterns, [str(fixtures_dir), "--include", "**/asyncio_*.py"])

    assert result.exit_code == 0
    # Should only scan asyncio files
    output_data = yaml.safe_load(result.output)
    assert "concurrency_patterns" in output_data


def test_scan_with_exclude_pattern(runner, fixtures_dir):
    """Test scanning with exclude pattern."""
    result = runner.invoke(scan_concurrency_patterns, [str(fixtures_dir), "--exclude", "**/threading_*.py"])

    assert result.exit_code == 0
    # Should exclude threading files
    output_data = yaml.safe_load(result.output)
    assert "concurrency_patterns" in output_data


def test_scan_single_file(runner, fixtures_dir):
    """Test scanning a single file."""
    asyncio_file = fixtures_dir / "asyncio_patterns.py"
    result = runner.invoke(scan_concurrency_patterns, [str(asyncio_file)])

    assert result.exit_code == 0
    output_data = yaml.safe_load(result.output)
    assert "concurrency_patterns" in output_data
    # Should only have asyncio patterns
    assert "asyncio" in output_data["concurrency_patterns"]


def test_scan_nonexistent_path(runner):
    """Test scanning nonexistent path."""
    result = runner.invoke(scan_concurrency_patterns, ["/nonexistent/path"])

    assert result.exit_code != 0  # Should fail (exit code can be 1 or 2)
    assert "does not exist" in result.output


def test_scan_with_multiple_include(runner, fixtures_dir):
    """Test scanning with multiple include patterns."""
    result = runner.invoke(
        scan_concurrency_patterns,
        [
            str(fixtures_dir),
            "--include",
            "**/asyncio_*.py",
            "--include",
            "**/threading_*.py",
        ],
    )

    assert result.exit_code == 0
    output_data = yaml.safe_load(result.output)
    assert "concurrency_patterns" in output_data


def test_scan_empty_directory(runner):
    """Test scanning empty directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = runner.invoke(scan_concurrency_patterns, [tmpdir])

        # Should exit with error (no Python files)
        assert result.exit_code == 1
        assert "No Python files found" in result.output


def test_scan_output_format(runner, fixtures_dir):
    """Test that output is valid YAML."""
    result = runner.invoke(scan_concurrency_patterns, [str(fixtures_dir)])

    assert result.exit_code == 0

    # Parse YAML and verify structure
    data = yaml.safe_load(result.output)
    assert isinstance(data, dict)
    assert "concurrency_patterns" in data

    patterns = data["concurrency_patterns"]
    # Should have category keys
    assert any(key in patterns for key in ["asyncio", "threading", "multiprocessing"])


def test_verbose_with_output_file(runner, fixtures_dir):
    """Test verbose mode with output file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        output_file = f.name

    try:
        result = runner.invoke(scan_concurrency_patterns, [str(fixtures_dir), "-o", output_file, "-v"])

        assert result.exit_code == 0
        # Verbose output should show scanning info
        assert "Scanning" in result.output or "Results written to" in result.output
        # YAML should be in file, not stdout
        assert Path(output_file).exists()
    finally:
        Path(output_file).unlink(missing_ok=True)
