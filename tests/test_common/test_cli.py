"""Tests for common CLI utilities."""

from unittest.mock import MagicMock, patch

import click
import pytest
from click.testing import CliRunner

from upcast.common.cli import (
    add_scanner_arguments,
    create_scanner_parser,
    handle_scan_error,
    run_scanner_cli,
    validate_scanner_arguments,
)
from upcast.models.base import ScannerOutput, ScannerSummary


class TestAddScannerArguments:
    """Tests for add_scanner_arguments decorator."""

    def test_adds_all_standard_options(self):
        """Test that decorator adds all standard CLI options."""

        @click.command()
        @add_scanner_arguments
        def dummy_command(**kwargs):
            pass

        # Get all parameters
        params = {p.name for p in dummy_command.params}

        # Check all expected options are present
        assert "output" in params
        assert "format" in params
        assert "include" in params
        assert "exclude" in params
        assert "no_default_excludes" in params
        assert "verbose" in params

    def test_format_option_has_choices(self):
        """Test that format option restricts to yaml/json/markdown."""

        @click.command()
        @add_scanner_arguments
        def dummy_command(**kwargs):
            pass

        format_param = next(p for p in dummy_command.params if p.name == "format")
        assert isinstance(format_param.type, click.Choice)
        assert format_param.type.choices == ["yaml", "json", "markdown"]

    def test_multiple_patterns_supported(self):
        """Test that include/exclude support multiple values."""

        @click.command()
        @add_scanner_arguments
        def dummy_command(**kwargs):
            pass

        include_param = next(p for p in dummy_command.params if p.name == "include")
        exclude_param = next(p for p in dummy_command.params if p.name == "exclude")

        assert include_param.multiple is True
        assert exclude_param.multiple is True


class TestCreateScannerParser:
    """Tests for create_scanner_parser function."""

    def test_creates_command_with_name(self):
        """Test that command is created with correct name."""
        cmd = create_scanner_parser(name="test-scanner", description="Test scanner description")

        assert cmd.name == "test-scanner"

    def test_includes_description_in_docstring(self):
        """Test that description is included in command docstring."""
        description = "Scans for test patterns"
        cmd = create_scanner_parser(name="test", description=description)

        assert description in cmd.__doc__

    def test_includes_examples_in_docstring(self):
        """Test that examples are included in command docstring."""
        examples = ["upcast test .", "upcast test --verbose"]
        cmd = create_scanner_parser(name="test", description="Test scanner", examples=examples)

        for example in examples:
            assert example in cmd.__doc__

    def test_has_path_argument(self):
        """Test that command has path argument."""
        cmd = create_scanner_parser(name="test", description="Test")

        path_param = next(p for p in cmd.params if p.name == "path")
        assert path_param is not None
        assert path_param.default == "."


class TestRunScannerCli:
    """Tests for run_scanner_cli function."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
        self.mock_scanner = MagicMock()
        self.mock_scanner.scan.return_value = ScannerOutput(
            summary=ScannerSummary(total_count=5, files_scanned=2),
            results={"items": [{"name": "test1"}, {"name": "test2"}]},
            metadata={},
        )

    def test_validates_path_exists(self):
        """Test that non-existent path raises error."""
        with pytest.raises(SystemExit):
            run_scanner_cli(
                scanner=self.mock_scanner,
                path="/nonexistent/path",
            )

    def test_collects_python_files(self, tmp_path):
        """Test that Python files are collected correctly."""
        # Create test files
        (tmp_path / "test1.py").write_text("# test")
        (tmp_path / "test2.py").write_text("# test")

        with patch("upcast.common.cli.collect_python_files") as mock_collect:
            mock_collect.return_value = [
                tmp_path / "test1.py",
                tmp_path / "test2.py",
            ]

            # This will fail on scan, but we just want to test file collection
            from contextlib import suppress

            with suppress(Exception):
                run_scanner_cli(scanner=self.mock_scanner, path=str(tmp_path))

            mock_collect.assert_called_once()

    def test_exits_if_no_files_found(self, tmp_path):
        """Test that error is raised if no Python files found."""
        with patch("upcast.common.cli.collect_python_files") as mock_collect:
            mock_collect.return_value = []

            with pytest.raises(SystemExit):
                run_scanner_cli(scanner=self.mock_scanner, path=str(tmp_path))

    def test_calls_scanner_scan_method(self, tmp_path):
        """Test that scanner.scan() is called."""
        (tmp_path / "test.py").write_text("# test")

        with patch("upcast.common.cli.collect_python_files") as mock_collect:
            mock_collect.return_value = [tmp_path / "test.py"]

            with patch("upcast.common.cli.click.echo"):
                run_scanner_cli(scanner=self.mock_scanner, path=str(tmp_path))

            self.mock_scanner.scan.assert_called_once()

    def test_outputs_to_file_yaml(self, tmp_path):
        """Test that output is written to YAML file."""
        scan_dir = tmp_path / "scan"
        scan_dir.mkdir()
        (scan_dir / "test.py").write_text("# test")
        output_file = tmp_path / "output.yaml"

        with patch("upcast.common.cli.collect_python_files") as mock_collect:
            mock_collect.return_value = [scan_dir / "test.py"]

            with patch("upcast.common.cli.export_to_yaml") as mock_export:
                with patch("upcast.common.cli.click.echo"):
                    run_scanner_cli(
                        scanner=self.mock_scanner,
                        path=str(scan_dir),
                        output=str(output_file),
                        format="yaml",
                    )

                mock_export.assert_called_once()

    def test_outputs_to_file_json(self, tmp_path):
        """Test that output is written to JSON file."""
        scan_dir = tmp_path / "scan"
        scan_dir.mkdir()
        (scan_dir / "test.py").write_text("# test")
        output_file = tmp_path / "output.json"

        with patch("upcast.common.cli.collect_python_files") as mock_collect:
            mock_collect.return_value = [scan_dir / "test.py"]

            with patch("upcast.common.cli.export_to_json") as mock_export:
                with patch("upcast.common.cli.click.echo"):
                    run_scanner_cli(
                        scanner=self.mock_scanner,
                        path=str(scan_dir),
                        output=str(output_file),
                        format="json",
                    )

                mock_export.assert_called_once()

    def test_verbose_mode_prints_progress(self, tmp_path):
        """Test that verbose mode prints progress messages."""
        (tmp_path / "test.py").write_text("# test")

        with patch("upcast.common.cli.collect_python_files") as mock_collect:
            mock_collect.return_value = [tmp_path / "test.py"]

            with patch("upcast.common.cli.click.echo") as mock_echo:
                run_scanner_cli(scanner=self.mock_scanner, path=str(tmp_path), verbose=True)

                # Should print at least scanning message and summary
                assert mock_echo.call_count >= 2

    def test_raises_type_error_for_invalid_output(self, tmp_path):
        """Test that TypeError is raised if scanner doesn't return ScannerOutput."""
        (tmp_path / "test.py").write_text("# test")
        bad_scanner = MagicMock()
        bad_scanner.scan.return_value = {"not": "a scanner output"}

        with patch("upcast.common.cli.collect_python_files") as mock_collect:
            mock_collect.return_value = [tmp_path / "test.py"]

            with pytest.raises(TypeError, match="must return ScannerOutput"):
                run_scanner_cli(scanner=bad_scanner, path=str(tmp_path))


class TestValidateScannerArguments:
    """Tests for validate_scanner_arguments function."""

    def test_validates_yaml_format(self):
        """Test that yaml format is accepted."""
        result = validate_scanner_arguments(format="yaml")
        assert result["format"] == "yaml"

    def test_validates_json_format(self):
        """Test that json format is accepted."""
        result = validate_scanner_arguments(format="json")
        assert result["format"] == "json"

    def test_rejects_invalid_format(self):
        """Test that invalid format raises error."""
        with pytest.raises(click.BadParameter, match="Invalid format"):
            validate_scanner_arguments(format="xml")

    def test_normalizes_include_patterns(self):
        """Test that include patterns are normalized to list."""
        result = validate_scanner_arguments(include=("*.py", "*.pyi"))
        assert result["include_patterns"] == ["*.py", "*.pyi"]

    def test_normalizes_exclude_patterns(self):
        """Test that exclude patterns are normalized to list."""
        result = validate_scanner_arguments(exclude=("test_*", "*_test.py"))
        assert result["exclude_patterns"] == ["test_*", "*_test.py"]

    def test_handles_empty_patterns(self):
        """Test that empty patterns are converted to None."""
        result = validate_scanner_arguments(include=(), exclude=())
        assert result["include_patterns"] is None
        assert result["exclude_patterns"] is None


class TestHandleScanError:
    """Tests for handle_scan_error function."""

    def test_prints_error_message(self):
        """Test that error message is printed."""
        error = ValueError("Test error")

        with patch("upcast.common.cli.click.echo") as mock_echo:
            with pytest.raises(SystemExit):
                handle_scan_error(error)

            # Should print error message
            assert mock_echo.call_count >= 1
            call_args = str(mock_echo.call_args_list[0])
            assert "Test error" in call_args

    def test_verbose_mode_prints_traceback(self):
        """Test that verbose mode prints full traceback."""
        error = ValueError("Test error")

        with patch("upcast.common.cli.click.echo") as mock_echo:
            with pytest.raises(SystemExit):
                handle_scan_error(error, verbose=True)

            # Should print error and traceback
            assert mock_echo.call_count >= 2
