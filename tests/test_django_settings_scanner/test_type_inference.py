"""Tests for settings type inference."""

from pathlib import Path

import pytest

from upcast.scanners.django_settings import DjangoSettingsScanner


class TestBooleanSettings:
    """Test boolean setting detection."""

    def test_true_value(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test True boolean value."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("DEBUG = True")

        result = scanner.scan(tmp_path)

        assert "DEBUG" in result.results
        debug_info = result.results["DEBUG"]
        assert "bool" in debug_info.definition_types

    def test_false_value(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test False boolean value."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("DEBUG = False")

        result = scanner.scan(tmp_path)

        assert "DEBUG" in result.results


class TestStringSettings:
    """Test string setting detection."""

    def test_simple_string(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test simple string value."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("SECRET_KEY = 'my-secret'")

        result = scanner.scan(tmp_path)

        assert "SECRET_KEY" in result.results
        secret_info = result.results["SECRET_KEY"]
        assert "str" in secret_info.definition_types

    def test_multiline_string(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test multiline string value."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text('''
DESCRIPTION = """
This is a multiline
description
"""
''')

        result = scanner.scan(tmp_path)

        assert "DESCRIPTION" in result.results


class TestNumericSettings:
    """Test numeric setting detection."""

    def test_integer_value(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test integer value."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("MAX_CONNECTIONS = 100")

        result = scanner.scan(tmp_path)

        assert "MAX_CONNECTIONS" in result.results
        info = result.results["MAX_CONNECTIONS"]
        assert "int" in info.definition_types

    def test_float_value(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test float value."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("TIMEOUT = 30.5")

        result = scanner.scan(tmp_path)

        assert "TIMEOUT" in result.results


class TestListSettings:
    """Test list setting detection."""

    def test_simple_list(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test simple list."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("ALLOWED_HOSTS = ['localhost', '127.0.0.1']")

        result = scanner.scan(tmp_path)

        assert "ALLOWED_HOSTS" in result.results
        info = result.results["ALLOWED_HOSTS"]
        assert "list" in info.definition_types

    def test_empty_list(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test empty list."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("CUSTOM_LIST = []")

        result = scanner.scan(tmp_path)

        assert "CUSTOM_LIST" in result.results


class TestDictSettings:
    """Test dict setting detection."""

    def test_simple_dict(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test simple dictionary."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("""
CONFIG = {
    'key1': 'value1',
    'key2': 'value2',
}
""")

        result = scanner.scan(tmp_path)

        assert "CONFIG" in result.results
        info = result.results["CONFIG"]
        assert "dict" in info.definition_types

    def test_nested_dict(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test nested dictionary."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
""")

        result = scanner.scan(tmp_path)

        assert "DATABASES" in result.results


class TestTupleSettings:
    """Test tuple setting detection."""

    def test_simple_tuple(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test simple tuple."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("ADMINS = (('John', 'john@example.com'),)")

        result = scanner.scan(tmp_path)

        assert "ADMINS" in result.results
        info = result.results["ADMINS"]
        assert "tuple" in info.definition_types


class TestDynamicSettings:
    """Test dynamic/complex setting detection."""

    def test_environment_variable(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test setting from environment variable."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("""
import os
SECRET_KEY = os.environ.get('SECRET_KEY', 'default')
""")

        result = scanner.scan(tmp_path)

        assert "SECRET_KEY" in result.results
        info = result.results["SECRET_KEY"]
        assert "dynamic" in info.definition_types

    def test_computed_value(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test computed setting value."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("""
BASE_DIR = '/path/to/base'
STATIC_ROOT = BASE_DIR + '/static'
""")

        result = scanner.scan(tmp_path)

        assert "STATIC_ROOT" in result.results
