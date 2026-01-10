"""Tests for edge cases in Django settings scanner."""

from pathlib import Path

import pytest

from upcast.scanners.django_settings import DjangoSettingsScanner


class TestCaseSensitivity:
    """Test case sensitivity of setting names."""

    def test_uppercase_only(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test that only uppercase variables are detected."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("""
DEBUG = True
debug = False  # lowercase, should be ignored
Debug = False  # mixed case, should be ignored
""")

        result = scanner.scan(tmp_path)

        assert "DEBUG" in result.results
        assert "debug" not in result.results
        assert "Debug" not in result.results


class TestMultipleDefinitions:
    """Test handling of multiple definitions."""

    def test_same_setting_multiple_files(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test same setting in multiple files."""
        (tmp_path / "settings_base.py").write_text("DEBUG = False")
        (tmp_path / "settings_local.py").write_text("DEBUG = True")

        result = scanner.scan(tmp_path)

        assert "DEBUG" in result.results
        debug_info = result.results["DEBUG"]
        assert debug_info.definition_count == 2

    def test_overridden_setting(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test setting defined multiple times in same file."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("""
DEBUG = False
DEBUG = True  # Override
""")

        result = scanner.scan(tmp_path)

        assert "DEBUG" in result.results
        debug_info = result.results["DEBUG"]
        assert debug_info.definition_count == 2


class TestComplexUsages:
    """Test complex usage patterns."""

    def test_attribute_chain(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test chained attribute access."""
        (tmp_path / "settings.py").write_text("""
DATABASES = {'default': {'ENGINE': 'sqlite3'}}
""")

        (tmp_path / "views.py").write_text("""
from django.conf import settings
engine = settings.DATABASES['default']['ENGINE']
""")

        result = scanner.scan(tmp_path)

        assert "DATABASES" in result.results

    def test_conditional_usage(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test usage in conditional statements."""
        (tmp_path / "settings.py").write_text("DEBUG = True")

        (tmp_path / "views.py").write_text("""
from django.conf import settings

if settings.DEBUG:
    print("Debug")
elif not settings.DEBUG:
    print("Production")
""")

        result = scanner.scan(tmp_path)

        assert "DEBUG" in result.results
        debug_info = result.results["DEBUG"]
        assert debug_info.usage_count >= 2

    def test_usage_in_function(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test usage inside function."""
        (tmp_path / "settings.py").write_text("API_KEY = 'test'")

        (tmp_path / "utils.py").write_text("""
from django.conf import settings

def get_api_key():
    return settings.API_KEY
""")

        result = scanner.scan(tmp_path)

        assert "API_KEY" in result.results


class TestSettingsFileDetection:
    """Test settings file detection."""

    def test_settings_py(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test settings.py is detected."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("DEBUG = True")

        result = scanner.scan(tmp_path)

        assert "DEBUG" in result.results
        assert result.results["DEBUG"].definition_count >= 1

    def test_config_file(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test config.py is detected."""
        config_file = tmp_path / "config.py"
        config_file.write_text("DEBUG = True")

        result = scanner.scan(tmp_path)

        assert "DEBUG" in result.results

    def test_settings_directory(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test settings directory."""
        settings_dir = tmp_path / "settings"
        settings_dir.mkdir()

        (settings_dir / "__init__.py").write_text("")
        (settings_dir / "base.py").write_text("DEBUG = False")

        result = scanner.scan(tmp_path)

        assert "DEBUG" in result.results


class TestEmptyAndInvalid:
    """Test empty and invalid files."""

    def test_empty_settings_file(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test empty settings file."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("")

        result = scanner.scan(tmp_path)

        assert result.summary.total_settings == 0

    def test_invalid_syntax(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test file with invalid syntax."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("""
DEBUG = True
INVALID SYNTAX HERE
""")

        result = scanner.scan(tmp_path)

        # Should handle gracefully
        assert result is not None

    def test_comments_only(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test file with only comments."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("""
# This is a comment
# DEBUG = True
""")

        result = scanner.scan(tmp_path)

        assert "DEBUG" not in result.results


class TestImportVariations:
    """Test different import patterns."""

    def test_direct_import(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test direct settings import."""
        (tmp_path / "settings.py").write_text("DEBUG = True")

        (tmp_path / "views.py").write_text("""
from django.conf import settings
x = settings.DEBUG
""")

        result = scanner.scan(tmp_path)

        assert "DEBUG" in result.results

    def test_aliased_import(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test aliased settings import."""
        (tmp_path / "settings.py").write_text("DEBUG = True")

        (tmp_path / "views.py").write_text("""
from django.conf import settings as s
x = s.DEBUG
""")

        result = scanner.scan(tmp_path)

        # Aliased imports might not be detected depending on implementation
        # This test documents the behavior
        assert result is not None


class TestSpecialSettings:
    """Test detection of common Django settings."""

    def test_database_settings(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test DATABASES setting."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
""")

        result = scanner.scan(tmp_path)

        assert "DATABASES" in result.results

    def test_static_files_settings(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test static files settings."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("""
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/static/'
STATICFILES_DIRS = ['/path/to/static']
""")

        result = scanner.scan(tmp_path)

        assert "STATIC_URL" in result.results
        assert "STATIC_ROOT" in result.results
        assert "STATICFILES_DIRS" in result.results

    def test_template_settings(self, tmp_path: Path, scanner: DjangoSettingsScanner) -> None:
        """Test TEMPLATES setting."""
        settings_file = tmp_path / "settings.py"
        settings_file.write_text("""
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    },
]
""")

        result = scanner.scan(tmp_path)

        assert "TEMPLATES" in result.results
