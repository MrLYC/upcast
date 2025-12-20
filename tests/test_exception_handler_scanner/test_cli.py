"""Tests for CLI interface."""

from pathlib import Path

from click.testing import CliRunner

from upcast.exception_handler_scanner.cli import scan_exception_handlers


def test_cli_basic_scan():
    """Test basic CLI scanning."""
    runner = CliRunner()
    fixture_dir = Path(__file__).parent / "fixtures"

    result = runner.invoke(scan_exception_handlers, [str(fixture_dir)])

    if result.exit_code != 0:
        print(f"Output: {result.output}")
        if result.exception:
            import traceback

            traceback.print_exception(type(result.exception), result.exception, result.exception.__traceback__)
    assert result.exit_code == 0
    assert "exception_handlers" in result.output


def test_cli_verbose_output():
    """Test CLI with verbose flag."""
    runner = CliRunner()
    fixture_dir = Path(__file__).parent / "fixtures"

    result = runner.invoke(scan_exception_handlers, [str(fixture_dir), "-v"])

    assert result.exit_code == 0
    assert "Scanning:" in result.output or "Found" in result.output


def test_cli_output_to_file():
    """Test CLI with output file."""
    runner = CliRunner()
    fixture_dir = Path(__file__).parent / "fixtures"

    with runner.isolated_filesystem():
        result = runner.invoke(
            scan_exception_handlers,
            [str(fixture_dir), "-o", "output.yaml"],
        )

        assert result.exit_code == 0
        assert Path("output.yaml").exists()


def test_cli_single_file():
    """Test scanning a single file."""
    runner = CliRunner()
    fixture_file = Path(__file__).parent / "fixtures" / "simple.py"

    result = runner.invoke(scan_exception_handlers, [str(fixture_file)])

    assert result.exit_code == 0
    assert "exception_handlers" in result.output


def test_cli_include_pattern():
    """Test CLI with include pattern."""
    runner = CliRunner()
    fixture_dir = Path(__file__).parent / "fixtures"

    result = runner.invoke(
        scan_exception_handlers,
        [str(fixture_dir), "--include", "**/simple.py"],
    )

    assert result.exit_code == 0


def test_cli_exclude_pattern():
    """Test CLI with exclude pattern."""
    runner = CliRunner()
    fixture_dir = Path(__file__).parent / "fixtures"

    result = runner.invoke(
        scan_exception_handlers,
        [str(fixture_dir), "--exclude", "**/complex.py"],
    )

    assert result.exit_code == 0


def test_cli_json_output():
    """Test CLI with JSON output format."""
    runner = CliRunner()
    fixture_dir = Path(__file__).parent / "fixtures"

    with runner.isolated_filesystem():
        result = runner.invoke(
            scan_exception_handlers,
            [str(fixture_dir), "-o", "output.json"],
        )

        assert result.exit_code == 0
        assert Path("output.json").exists()

        # Check it's valid JSON
        import json

        with open("output.json") as f:
            data = json.load(f)
            assert "exception_handlers" in data


def test_cli_default_path():
    """Test CLI with default path (current directory)."""
    runner = CliRunner()

    with runner.isolated_filesystem():
        # Create a simple Python file
        Path("test.py").write_text(
            """
try:
    pass
except Exception:
    pass
"""
        )

        result = runner.invoke(scan_exception_handlers, [])

        assert result.exit_code == 0
        assert "exception_handlers" in result.output
