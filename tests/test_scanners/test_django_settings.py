"""Tests for DjangoSettingsScanner."""

from upcast.models.django_settings import SettingDefinitionItem, SettingInfo, SettingUsageItem
from upcast.scanners.django_settings import DjangoSettingsScanner


class TestDjangoSettingsModels:
    """Tests for Django settings models."""

    def test_valid_setting_definition_item(self):
        """Test creating valid SettingDefinitionItem."""
        item = SettingDefinitionItem(
            value="DEBUG",
            statement="DEBUG = True",
            lineno=10,
            type="bool",
        )
        assert item.value == "DEBUG"
        assert item.statement == "DEBUG = True"
        assert item.lineno == 10
        assert item.type == "bool"

    def test_valid_setting_usage_item(self):
        """Test creating valid SettingUsageItem."""
        item = SettingUsageItem(
            statement="if settings.DEBUG:",
            lineno=20,
        )
        assert item.statement == "if settings.DEBUG:"
        assert item.lineno == 20

    def test_valid_setting_info(self):
        """Test creating valid SettingInfo."""
        info = SettingInfo(
            definition_count=1,
            usage_count=2,
            type_list=["bool"],
            definitions={"settings.py": []},
            usages={"views.py": []},
        )
        assert info.definition_count == 1
        assert info.usage_count == 2
        assert info.type_list == ["bool"]


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

        assert output.summary.total_count == 2
        assert "DEBUG" in output.results
        assert "ALLOWED_HOSTS" in output.results

        # Check DEBUG setting
        debug_info = output.results["DEBUG"]
        assert debug_info.definition_count == 1
        assert debug_info.usage_count == 0
        assert "bool" in debug_info.type_list

        # Check definitions
        assert len(debug_info.definitions) > 0
        first_file = next(iter(debug_info.definitions.keys()))
        assert len(debug_info.definitions[first_file]) == 1
        debug_def = debug_info.definitions[first_file][0]
        assert debug_def.value is True
        assert debug_def.type == "bool"

    def test_scanner_handles_empty_file(self, tmp_path):
        """Test scanner handles empty files."""
        test_file = tmp_path / "test.py"
        test_file.write_text("")

        scanner = DjangoSettingsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 0
        assert len(output.results) == 0

    def test_scanner_detects_multiple_types(self, tmp_path):
        """Test scanner detects different setting types."""
        test_file = tmp_path / "settings.py"
        test_file.write_text(
            """
DEBUG = True
SECRET_KEY = 'my-secret'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
TIMEOUT = 30
"""
        )

        scanner = DjangoSettingsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 4

        # Check types
        assert output.results["DEBUG"].type_list == ["bool"]
        assert output.results["SECRET_KEY"].type_list == ["str"]
        assert output.results["ALLOWED_HOSTS"].type_list == ["list"]
        assert output.results["TIMEOUT"].type_list == ["int"]

    def test_scanner_detects_usages(self, tmp_path):
        """Test scanner detects settings usages."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("DEBUG = True\n")

        views_file = tmp_path / "views.py"
        views_file.write_text(
            """
from django.conf import settings

if settings.DEBUG:
    print("Debug mode")
"""
        )

        scanner = DjangoSettingsScanner()
        output = scanner.scan(tmp_path)

        assert "DEBUG" in output.results
        debug_info = output.results["DEBUG"]
        assert debug_info.definition_count == 1
        assert debug_info.usage_count == 1

        # Check usage details
        assert len(debug_info.usages) > 0
        usage_file = next(iter(debug_info.usages.keys()))
        assert len(debug_info.usages[usage_file]) == 1
        usage = debug_info.usages[usage_file][0]
        assert "settings.DEBUG" in usage.statement

    def test_scanner_summary_statistics(self, tmp_path):
        """Test scanner generates correct summary statistics."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text(
            """
DEBUG = True
SECRET_KEY = 'test'
"""
        )

        scanner = DjangoSettingsScanner()
        output = scanner.scan(settings_file)

        # Check summary
        assert output.summary.total_settings == 2
        assert output.summary.total_definitions == 2
        assert output.summary.total_usages == 0
        assert output.summary.files_scanned > 0
