"""Tests for DjangoSettingsScanner."""

from upcast.models.django_settings import SettingDefinitionItem, SettingInfo, SettingUsageItem
from upcast.scanners.django_settings import DjangoSettingsScanner


class TestDjangoSettingsModels:
    """Tests for Django settings models."""

    def test_valid_setting_definition_item(self):
        """Test creating valid SettingDefinitionItem."""
        item = SettingDefinitionItem(
            file="settings.py",
            value="DEBUG",
            statement="DEBUG = True",
            lineno=10,
            type="bool",
        )
        assert item.file == "settings.py"
        assert item.value == "DEBUG"
        assert item.statement == "DEBUG = True"
        assert item.lineno == 10
        assert item.type == "bool"

    def test_valid_setting_usage_item(self):
        """Test creating valid SettingUsageItem."""
        item = SettingUsageItem(
            file="views.py",
            statement="if settings.DEBUG:",
            lineno=20,
        )
        assert item.file == "views.py"
        assert item.statement == "if settings.DEBUG:"
        assert item.lineno == 20

    def test_valid_setting_info(self):
        """Test creating valid SettingInfo."""
        info = SettingInfo(
            definition_count=1,
            usage_count=2,
            definition_types=["bool"],
            definitions=[],
            usages=[],
        )
        assert info.definition_count == 1
        assert info.usage_count == 2
        assert info.definition_types == ["bool"]


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
        assert "bool" in debug_info.definition_types

        # Check definitions
        assert len(debug_info.definitions) > 0
        debug_def = debug_info.definitions[0]
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
        assert output.results["DEBUG"].definition_types == ["bool"]
        assert output.results["SECRET_KEY"].definition_types == ["str"]
        assert output.results["ALLOWED_HOSTS"].definition_types == ["list"]
        assert output.results["TIMEOUT"].definition_types == ["int"]

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
        usage = debug_info.usages[0]
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

    def test_scanner_extracts_complex_list_values(self, tmp_path):
        """Test scanner extracts complex list values (lists with dicts)."""
        test_file = tmp_path / "settings.py"
        test_file.write_text(
            """
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
]
"""
        )

        scanner = DjangoSettingsScanner()
        output = scanner.scan(test_file)

        assert "AUTH_PASSWORD_VALIDATORS" in output.results
        validator_info = output.results["AUTH_PASSWORD_VALIDATORS"]
        assert validator_info.definition_count == 1
        assert "list" in validator_info.definition_types

        # Check value extraction
        validator_def = validator_info.definitions[0]
        assert validator_def.value is not None
        assert isinstance(validator_def.value, list)
        assert len(validator_def.value) == 2

        # Verify first dict
        assert isinstance(validator_def.value[0], dict)
        assert "NAME" in validator_def.value[0]
        assert (
            validator_def.value[0]["NAME"] == "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        )

        # Verify second dict with nested OPTIONS
        assert isinstance(validator_def.value[1], dict)
        assert "NAME" in validator_def.value[1]
        assert "OPTIONS" in validator_def.value[1]
        assert validator_def.value[1]["OPTIONS"]["min_length"] == 8

    def test_scanner_extracts_nested_structures(self, tmp_path):
        """Test scanner extracts nested data structures."""
        test_file = tmp_path / "settings.py"
        test_file.write_text(
            """
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'OPTIONS': {
            'isolation_level': 'READ COMMITTED',
        },
    }
}

LOGGING_HANDLERS = [
    ('console', {'level': 'INFO'}),
    ('file', {'level': 'ERROR', 'filename': 'app.log'}),
]
"""
        )

        scanner = DjangoSettingsScanner()
        output = scanner.scan(test_file)

        # Test nested dict
        assert "DATABASES" in output.results
        db_info = output.results["DATABASES"]
        db_def = db_info.definitions[0]
        assert db_def.value is not None
        assert isinstance(db_def.value, dict)
        assert "default" in db_def.value
        assert db_def.value["default"]["ENGINE"] == "django.db.backends.postgresql"
        assert db_def.value["default"]["OPTIONS"]["isolation_level"] == "READ COMMITTED"

        # Test list of tuples with dicts
        assert "LOGGING_HANDLERS" in output.results
        log_info = output.results["LOGGING_HANDLERS"]
        log_def = log_info.definitions[0]
        assert log_def.value is not None
        assert isinstance(log_def.value, list)
        assert len(log_def.value) == 2
        assert log_def.value[0] == ("console", {"level": "INFO"})
        assert log_def.value[1][1]["filename"] == "app.log"
