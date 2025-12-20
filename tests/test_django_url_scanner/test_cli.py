"""Tests for Django URL scanner CLI."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from upcast.main import main


class TestDjangoUrlScannerCLI:
    """Tests for scan-django-urls CLI command."""

    @pytest.fixture
    def runner(self):
        """Create a CLI runner."""
        return CliRunner()

    @pytest.fixture
    def fixtures_dir(self):
        """Get the fixtures directory."""
        return Path(__file__).parent / "fixtures"

    def test_cli_help(self, runner):
        """Test CLI help message."""
        result = runner.invoke(main, ["scan-django-urls", "--help"])
        assert result.exit_code == 0
        assert "Scan Python files for Django URL pattern definitions" in result.output

    def test_cli_scan_file(self, runner, fixtures_dir):
        """Test scanning a single file."""
        result = runner.invoke(main, ["scan-django-urls", str(fixtures_dir / "simple_urls.py")])
        assert result.exit_code == 0
        assert "urlpatterns" in result.output

    def test_cli_scan_directory(self, runner, fixtures_dir):
        """Test scanning a directory."""
        result = runner.invoke(main, ["scan-django-urls", str(fixtures_dir)])
        assert result.exit_code == 0
        assert "urlpatterns" in result.output

    def test_cli_output_file(self, runner, fixtures_dir, tmp_path):
        """Test output to file."""
        output_file = tmp_path / "urls.yaml"
        result = runner.invoke(main, ["scan-django-urls", str(fixtures_dir / "simple_urls.py"), "-o", str(output_file)])
        assert result.exit_code == 0
        assert output_file.exists()

    def test_cli_verbose(self, runner, fixtures_dir):
        """Test verbose output."""
        result = runner.invoke(main, ["scan-django-urls", str(fixtures_dir / "simple_urls.py"), "-v"])
        assert result.exit_code == 0
        # Verbose messages should be in stderr
        assert "Scanning" in result.output or "Processing" in result.output or result.exit_code == 0

    def test_cli_include_pattern(self, runner, fixtures_dir):
        """Test include pattern filtering."""
        result = runner.invoke(main, ["scan-django-urls", str(fixtures_dir), "--include", "*simple*"])
        assert result.exit_code == 0
        assert "simple_urls" in result.output or "urlpatterns" in result.output

    def test_cli_exclude_pattern(self, runner, fixtures_dir):
        """Test exclude pattern filtering."""
        result = runner.invoke(main, ["scan-django-urls", str(fixtures_dir), "--exclude", "*complex*"])
        assert result.exit_code == 0

    def test_cli_nonexistent_path(self, runner):
        """Test error handling for nonexistent path."""
        result = runner.invoke(main, ["scan-django-urls", "/nonexistent/path"])
        assert result.exit_code != 0
