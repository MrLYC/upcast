"""Tests for checker module integration with definition parsing."""

import tempfile
from pathlib import Path

from upcast.django_settings_scanner.checker import DjangoSettingsChecker


class TestCheckerDefinitionScanning:
    """Test definition scanning in DjangoSettingsChecker."""

    def test_scan_definitions_finds_settings_modules(self):
        """Test that scan_definitions finds settings modules."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a settings directory structure
            settings_dir = Path(tmpdir) / "myproject" / "settings"
            settings_dir.mkdir(parents=True)

            # Create base.py
            base_file = settings_dir / "base.py"
            base_file.write_text(
                """
DEBUG = True
SECRET_KEY = "base-secret"
ALLOWED_HOSTS = []
"""
            )

            # Create dev.py
            dev_file = settings_dir / "dev.py"
            dev_file.write_text(
                """
from .base import *

DEBUG = False
ALLOWED_HOSTS = ["localhost"]
"""
            )

            # Initialize checker and scan
            checker = DjangoSettingsChecker(tmpdir)
            checker.scan_definitions(tmpdir)

            # Should find both modules
            definitions = checker.get_definitions_by_module()
            assert len(definitions) >= 2

            # Check that modules are keyed by their module paths
            module_paths = list(definitions.keys())
            assert any("settings.base" in path for path in module_paths)
            assert any("settings.dev" in path for path in module_paths)

    def test_parse_settings_module_extracts_definitions(self):
        """Test that settings definitions are correctly extracted."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create settings module
            settings_dir = Path(tmpdir) / "config"
            settings_dir.mkdir(parents=True)

            settings_file = settings_dir / "base.py"
            settings_file.write_text(
                """
DEBUG = True
SECRET_KEY = "test-key"
PORT = 8000
ALLOWED_HOSTS = ["example.com"]
"""
            )

            # Scan definitions
            checker = DjangoSettingsChecker(tmpdir)
            checker.scan_definitions(tmpdir)

            definitions = checker.get_definitions_by_module()
            assert len(definitions) > 0

            # Get the module
            module = next(iter(definitions.values()))

            # Check definitions
            assert "DEBUG" in module.definitions
            assert "SECRET_KEY" in module.definitions
            assert "PORT" in module.definitions
            assert "ALLOWED_HOSTS" in module.definitions

            # Check values
            assert module.definitions["DEBUG"].value is True
            assert module.definitions["SECRET_KEY"].value == "test-key"
            assert module.definitions["PORT"].value == 8000
            assert module.definitions["ALLOWED_HOSTS"].value == ["example.com"]

    def test_override_tracking_across_modules(self):
        """Test that overrides are correctly tracked."""
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_dir = Path(tmpdir) / "settings"
            settings_dir.mkdir(parents=True)

            # Create base module
            base_file = settings_dir / "base.py"
            base_file.write_text(
                """
DEBUG = True
SECRET_KEY = "base"
DATABASE_NAME = "base_db"
"""
            )

            # Create dev module that overrides DEBUG
            dev_file = settings_dir / "dev.py"
            dev_file.write_text(
                """
from .base import *

DEBUG = False
DEV_MODE = True
"""
            )

            # Scan definitions
            checker = DjangoSettingsChecker(tmpdir)
            checker.scan_definitions(tmpdir)

            definitions = checker.get_definitions_by_module()

            # Find dev module
            dev_module = None
            for module in definitions.values():
                if "dev" in module.module_path:
                    dev_module = module
                    break

            assert dev_module is not None

            # DEBUG should be marked as override
            assert "DEBUG" in dev_module.definitions
            debug_def = dev_module.definitions["DEBUG"]
            assert debug_def.overrides is not None
            assert "base" in debug_def.overrides

            # DEV_MODE should not be marked as override (new setting)
            assert "DEV_MODE" in dev_module.definitions
            dev_mode_def = dev_module.definitions["DEV_MODE"]
            assert dev_mode_def.overrides is None

    def test_get_all_defined_settings(self):
        """Test getting unique settings across all modules."""
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_dir = Path(tmpdir) / "settings"
            settings_dir.mkdir(parents=True)

            # Base module
            base_file = settings_dir / "base.py"
            base_file.write_text(
                """
DEBUG = True
SECRET_KEY = "key"
"""
            )

            # Dev module
            dev_file = settings_dir / "dev.py"
            dev_file.write_text(
                """
from .base import *

DEBUG = False
DEV_SETTING = "dev"
"""
            )

            # Prod module
            prod_file = settings_dir / "prod.py"
            prod_file.write_text(
                """
from .base import *

PROD_SETTING = "prod"
"""
            )

            checker = DjangoSettingsChecker(tmpdir)
            checker.scan_definitions(tmpdir)

            all_settings = checker.get_all_defined_settings()

            # Should have unique settings across all modules
            expected_settings = {"DEBUG", "SECRET_KEY", "DEV_SETTING", "PROD_SETTING"}
            assert all_settings == expected_settings

    def test_integration_with_usage_tracking(self):
        """Test that definitions and usages can coexist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create settings directory
            settings_dir = Path(tmpdir) / "settings"
            settings_dir.mkdir(parents=True)

            settings_file = settings_dir / "base.py"
            settings_file.write_text("DEBUG = True\n")

            # Create app file that uses settings
            app_dir = Path(tmpdir) / "myapp"
            app_dir.mkdir(parents=True)

            app_file = app_dir / "views.py"
            app_file.write_text(
                """
from django.conf import settings

if settings.DEBUG:
    print("Debug mode")
"""
            )

            # Initialize checker
            checker = DjangoSettingsChecker(tmpdir)

            # Scan definitions
            checker.scan_definitions(tmpdir)

            # Check usages
            checker.check_file(str(app_file))

            # Should have definitions
            definitions = checker.get_definitions_by_module()
            assert len(definitions) > 0

            # Should have usages
            assert len(checker.settings) > 0
            assert "DEBUG" in checker.settings

    def test_empty_settings_module(self):
        """Test handling of empty settings module."""
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_dir = Path(tmpdir) / "settings"
            settings_dir.mkdir(parents=True)

            # Create empty settings file
            settings_file = settings_dir / "base.py"
            settings_file.write_text("# Empty settings\n")

            checker = DjangoSettingsChecker(tmpdir)
            checker.scan_definitions(tmpdir)

            definitions = checker.get_definitions_by_module()

            # Should still create a module entry, just with no definitions
            assert len(definitions) > 0
            module = next(iter(definitions.values()))
            assert len(module.definitions) == 0

    def test_settings_with_lowercase_variables(self):
        """Test that lowercase variables are not included."""
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_dir = Path(tmpdir) / "settings"
            settings_dir.mkdir(parents=True)

            settings_file = settings_dir / "base.py"
            settings_file.write_text(
                """
DEBUG = True
secret_key = "should not be included"
_private = "also not included"
"""
            )

            checker = DjangoSettingsChecker(tmpdir)
            checker.scan_definitions(tmpdir)

            definitions = checker.get_definitions_by_module()
            module = next(iter(definitions.values()))

            # Should only include DEBUG
            assert "DEBUG" in module.definitions
            assert "secret_key" not in module.definitions
            assert "_private" not in module.definitions
