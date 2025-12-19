"""Tests for AST utilities in django_settings_scanner."""

from pathlib import Path
from textwrap import dedent

from astroid import MANAGER, nodes

from upcast.django_settings_scanner.ast_utils import (
    extract_getattr_default,
    extract_setting_name,
    is_django_settings,
    is_settings_attribute_access,
    is_settings_getattr_call,
    is_settings_hasattr_call,
)


class TestIsDjangoSettings:
    """Test is_django_settings function."""

    def test_direct_settings_import(self, tmp_path: Path) -> None:
        """Test detecting django.conf.settings import."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent(
                """
                from django.conf import settings

                value = settings.DEBUG
                """
            )
        )

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.nodes_of_class(nodes.Attribute):
            if node.attrname == "DEBUG":
                assert is_django_settings(node.expr) is True

    def test_aliased_settings_import(self, tmp_path: Path) -> None:
        """Test detecting aliased settings import."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent(
                """
                from django.conf import settings as config

                value = config.DEBUG
                """
            )
        )

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.nodes_of_class(nodes.Attribute):
            if node.attrname == "DEBUG":
                assert is_django_settings(node.expr) is True

    def test_non_django_settings(self, tmp_path: Path) -> None:
        """Test non-Django settings is not detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent(
                """
                settings = {"DEBUG": True}

                value = settings["DEBUG"]
                """
            )
        )

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.nodes_of_class(nodes.Name):
            if node.name == "settings":
                assert is_django_settings(node) is False


class TestIsSettingsAttributeAccess:
    """Test is_settings_attribute_access function."""

    def test_simple_attribute_access(self, tmp_path: Path) -> None:
        """Test detecting simple settings.KEY pattern."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent(
                """
                from django.conf import settings

                value = settings.DEBUG
                """
            )
        )

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.nodes_of_class(nodes.Attribute):
            if node.attrname == "DEBUG":
                assert is_settings_attribute_access(node) is True

    def test_non_settings_attribute(self, tmp_path: Path) -> None:
        """Test non-settings attribute is not detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent(
                """
                obj = object()
                value = obj.attr
                """
            )
        )

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.nodes_of_class(nodes.Attribute):
            if node.attrname == "attr":
                assert is_settings_attribute_access(node) is False


class TestIsSettingsGetattrCall:
    """Test is_settings_getattr_call function."""

    def test_getattr_with_default(self, tmp_path: Path) -> None:
        """Test detecting getattr(settings, 'KEY', default)."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent(
                """
                from django.conf import settings

                value = getattr(settings, 'API_KEY', 'default')
                """
            )
        )

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.nodes_of_class(nodes.Call):
            if isinstance(node.func, nodes.Name) and node.func.name == "getattr":
                assert is_settings_getattr_call(node) is True

    def test_getattr_without_default(self, tmp_path: Path) -> None:
        """Test detecting getattr(settings, 'KEY')."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent(
                """
                from django.conf import settings

                value = getattr(settings, 'API_KEY')
                """
            )
        )

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.nodes_of_class(nodes.Call):
            if isinstance(node.func, nodes.Name) and node.func.name == "getattr":
                assert is_settings_getattr_call(node) is True

    def test_non_settings_getattr(self, tmp_path: Path) -> None:
        """Test getattr on non-settings object is not detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent(
                """
                obj = object()
                value = getattr(obj, 'attr')
                """
            )
        )

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.nodes_of_class(nodes.Call):
            if isinstance(node.func, nodes.Name) and node.func.name == "getattr":
                assert is_settings_getattr_call(node) is False


class TestIsSettingsHasattrCall:
    """Test is_settings_hasattr_call function."""

    def test_hasattr_call(self, tmp_path: Path) -> None:
        """Test detecting hasattr(settings, 'KEY')."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent(
                """
                from django.conf import settings

                has_feature = hasattr(settings, 'FEATURE_ENABLED')
                """
            )
        )

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.nodes_of_class(nodes.Call):
            if isinstance(node.func, nodes.Name) and node.func.name == "hasattr":
                assert is_settings_hasattr_call(node) is True

    def test_non_settings_hasattr(self, tmp_path: Path) -> None:
        """Test hasattr on non-settings object is not detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent(
                """
                obj = object()
                has_attr = hasattr(obj, 'attr')
                """
            )
        )

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.nodes_of_class(nodes.Call):
            if isinstance(node.func, nodes.Name) and node.func.name == "hasattr":
                assert is_settings_hasattr_call(node) is False


class TestExtractSettingName:
    """Test extract_setting_name function."""

    def test_extract_from_attribute(self, tmp_path: Path) -> None:
        """Test extracting name from attribute access."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent(
                """
                from django.conf import settings

                value = settings.DEBUG
                """
            )
        )

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.nodes_of_class(nodes.Attribute):
            if node.attrname == "DEBUG":
                assert extract_setting_name(node) == "DEBUG"

    def test_extract_from_getattr(self, tmp_path: Path) -> None:
        """Test extracting name from getattr call."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent(
                """
                from django.conf import settings

                value = getattr(settings, 'API_KEY')
                """
            )
        )

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.nodes_of_class(nodes.Call):
            if isinstance(node.func, nodes.Name) and node.func.name == "getattr":
                assert extract_setting_name(node) == "API_KEY"

    def test_extract_from_hasattr(self, tmp_path: Path) -> None:
        """Test extracting name from hasattr call."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent(
                """
                from django.conf import settings

                has_feature = hasattr(settings, 'FEATURE_ENABLED')
                """
            )
        )

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.nodes_of_class(nodes.Call):
            if isinstance(node.func, nodes.Name) and node.func.name == "hasattr":
                assert extract_setting_name(node) == "FEATURE_ENABLED"

    def test_extract_dynamic_name(self, tmp_path: Path) -> None:
        """Test extracting dynamic variable name."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent(
                """
                from django.conf import settings

                key = "DEBUG"
                value = getattr(settings, key)
                """
            )
        )

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.nodes_of_class(nodes.Call):
            if isinstance(node.func, nodes.Name) and node.func.name == "getattr":
                assert extract_setting_name(node) == "DYNAMIC"

    def test_filter_lowercase_attribute(self, tmp_path: Path) -> None:
        """Test that lowercase attributes are filtered out."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent(
                """
                from django.conf import settings

                # These should be filtered out (lowercase)
                settings.configure()
                value1 = settings.configured

                # These should be captured (uppercase)
                value2 = settings.DEBUG
                """
            )
        )

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.nodes_of_class(nodes.Attribute):
            if node.attrname == "configure" or node.attrname == "configured":
                assert extract_setting_name(node) is None
            elif node.attrname == "DEBUG":
                assert extract_setting_name(node) == "DEBUG"

    def test_filter_lowercase_getattr(self, tmp_path: Path) -> None:
        """Test that lowercase names in getattr are filtered out."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent(
                """
                from django.conf import settings

                # Should be filtered out (lowercase)
                value1 = getattr(settings, 'configured')

                # Should be captured (uppercase)
                value2 = getattr(settings, 'DEBUG')
                """
            )
        )

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.nodes_of_class(nodes.Call):
            if isinstance(node.func, nodes.Name) and node.func.name == "getattr" and len(node.args) >= 2:
                key_arg = node.args[1]
                if isinstance(key_arg, nodes.Const):
                    if key_arg.value == "configured":
                        assert extract_setting_name(node) is None
                    elif key_arg.value == "DEBUG":
                        assert extract_setting_name(node) == "DEBUG"


class TestExtractGetattrDefault:
    """Test extract_getattr_default function."""

    def test_extract_string_default(self, tmp_path: Path) -> None:
        """Test extracting string default value."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent(
                """
                from django.conf import settings

                value = getattr(settings, 'API_KEY', 'default')
                """
            )
        )

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.nodes_of_class(nodes.Call):
            if isinstance(node.func, nodes.Name) and node.func.name == "getattr":
                # Now returns the actual value, not string representation
                assert extract_getattr_default(node) == "default"

    def test_extract_none_default(self, tmp_path: Path) -> None:
        """Test extracting None default value."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent(
                """
                from django.conf import settings

                value = getattr(settings, 'API_KEY', None)
                """
            )
        )

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.nodes_of_class(nodes.Call):
            if isinstance(node.func, nodes.Name) and node.func.name == "getattr":
                # Now returns None value, not string "None"
                assert extract_getattr_default(node) is None

    def test_no_default(self, tmp_path: Path) -> None:
        """Test getattr without default value."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent(
                """
                from django.conf import settings

                value = getattr(settings, 'API_KEY')
                """
            )
        )

        module = MANAGER.ast_from_file(str(test_file), modname="test")

        for node in module.nodes_of_class(nodes.Call):
            if isinstance(node.func, nodes.Name) and node.func.name == "getattr":
                assert extract_getattr_default(node) is None
