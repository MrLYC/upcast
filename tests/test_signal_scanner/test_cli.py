"""CLI tests for signal scanner."""

from pathlib import Path

import yaml
from click.testing import CliRunner

from upcast.signal_scanner.cli import scan_signals

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_scan_current_directory():
    """Test scanning fixtures directory."""
    runner = CliRunner()
    result = runner.invoke(scan_signals, [str(FIXTURES_DIR)])

    assert result.exit_code == 0
    assert "django" in result.output or "celery" in result.output


def test_scan_with_output_file(tmp_path):
    """Test writing output to file."""
    output_file = tmp_path / "signals.yaml"
    runner = CliRunner()
    result = runner.invoke(scan_signals, [str(FIXTURES_DIR), "-o", str(output_file)])

    assert result.exit_code == 0
    assert output_file.exists()

    # Verify YAML is valid
    with output_file.open() as f:
        data = yaml.safe_load(f)
        assert data is not None


def test_scan_with_verbose(tmp_path):
    """Test verbose output."""
    runner = CliRunner()
    result = runner.invoke(scan_signals, [str(FIXTURES_DIR), "-v"])

    assert result.exit_code == 0
    assert "Scanning" in result.output
    assert "Summary" in result.output


def test_scan_single_file():
    """Test scanning single file."""
    runner = CliRunner()
    result = runner.invoke(scan_signals, [str(FIXTURES_DIR / "django_signals.py")])

    assert result.exit_code == 0
    assert "django" in result.output


def test_scan_with_include_pattern():
    """Test --include pattern filtering."""
    runner = CliRunner()
    result = runner.invoke(scan_signals, [str(FIXTURES_DIR), "--include", "django_*.py", "-v"])

    assert result.exit_code == 0
    assert "django" in result.output.lower()


def test_scan_with_exclude_pattern():
    """Test --exclude pattern filtering."""
    runner = CliRunner()
    result = runner.invoke(scan_signals, [str(FIXTURES_DIR), "--exclude", "**/celery_*.py", "-v"])

    assert result.exit_code == 0
    # Should have Django signals but not Celery
    output_lower = result.output.lower()
    assert "django" in output_lower


def test_scan_nonexistent_path():
    """Test error handling for nonexistent path."""
    runner = CliRunner()
    result = runner.invoke(scan_signals, ["/nonexistent/path"])

    assert result.exit_code != 0
    assert "does not exist" in result.output


def test_scan_output_yaml_format(tmp_path):
    """Test YAML output format structure."""
    output_file = tmp_path / "signals.yaml"
    runner = CliRunner()
    result = runner.invoke(
        scan_signals,
        [str(FIXTURES_DIR / "django_signals.py"), "-o", str(output_file)],
    )

    assert result.exit_code == 0

    with output_file.open() as f:
        data = yaml.safe_load(f)
        assert "django" in data
        # Check hierarchical structure
        assert "model_signals" in data["django"]
        model_signals = data["django"]["model_signals"]
        assert isinstance(model_signals, dict)
        # Check signal has correct structure with receivers, senders, usages
        for _signal_name, signal_data in model_signals.items():
            assert isinstance(signal_data, dict)
            assert "receivers" in signal_data
            assert isinstance(signal_data["receivers"], list)
            for receiver in signal_data["receivers"]:
                assert "handler" in receiver
                assert "file" in receiver
                assert "line" in receiver


def test_scan_no_signals_found(tmp_path):
    """Test scanning file with no signals."""
    # Create Python file without signals
    test_file = tmp_path / "no_signals.py"
    test_file.write_text("def regular_function():\n    pass\n")

    runner = CliRunner()
    result = runner.invoke(scan_signals, [str(test_file)])

    assert result.exit_code == 0
    assert "No signal patterns found" in result.output


def test_scan_with_multiple_include_patterns():
    """Test multiple --include patterns."""
    runner = CliRunner()
    result = runner.invoke(
        scan_signals,
        [
            str(FIXTURES_DIR),
            "--include",
            "django_*.py",
            "--include",
            "celery_*.py",
            "-v",
        ],
    )

    assert result.exit_code == 0


def test_scan_with_no_default_excludes():
    """Test --no-default-excludes flag."""
    runner = CliRunner()
    result = runner.invoke(scan_signals, [str(FIXTURES_DIR), "--no-default-excludes", "-v"])

    assert result.exit_code == 0


def test_verbose_with_output_file(tmp_path):
    """Test verbose mode with output file."""
    output_file = tmp_path / "signals.yaml"
    runner = CliRunner()
    result = runner.invoke(scan_signals, [str(FIXTURES_DIR), "-o", str(output_file), "-v"])

    assert result.exit_code == 0
    assert "Results written to" in result.output
    assert "Summary" in result.output
    assert output_file.exists()
