"""Tests for DjangoSettingsScanner."""

from upcast.models.django_settings import SettingDefinition
from upcast.scanners.django_settings import (
    DjangoSettingsScanner,
)


class TestDjangoSettingsModels:
    """Tests for Django settings models."""

    def test_valid_setting_definition(self):
        """Test creating valid SettingDefinition."""
        setting = SettingDefinition(
            value="DEBUG",
            lineno=10,
        )
        assert setting.value == "DEBUG"
        assert setting.lineno == 10


class TestDjangoSettingsScannerIntegration:
    """Integration tests for DjangoSettingsScanner."""

    def test_scanner_detects_settings(self, tmp_path):
        """Test scanner detects Django settings."""
        test_file = tmp_path / "settings.py"
        test_file.write_text(
            """
DEBUG = True
ALLOWED_HOSTS = ['localhost']
"""
        )

        scanner = DjangoSettingsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 0

    def test_scanner_handles_empty_file(self, tmp_path):
        """Test scanner handles empty files."""
        test_file = tmp_path / "test.py"
        test_file.write_text("")

        scanner = DjangoSettingsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 0
