"""Tests for Django settings Pydantic models."""

import pytest

from upcast.models.django_settings import (
    DjangoSettingsOutput,
    DjangoSettingsSummary,
    SettingDefinitionItem,
    SettingInfo,
    SettingUsageItem,
)


class TestSettingDefinitionItem:
    """Test SettingDefinitionItem model."""

    def test_basic_definition(self) -> None:
        """Test creating a basic definition."""
        defn = SettingDefinitionItem(
            value="localhost",
            statement="DEBUG = True",
            lineno=10,
            type="str",
        )
        assert defn.value == "localhost"
        assert defn.statement == "DEBUG = True"
        assert defn.lineno == 10
        assert defn.type == "str"

    def test_definition_without_value(self) -> None:
        """Test definition without inferred value."""
        defn = SettingDefinitionItem(
            value=None,
            statement="DATABASES = {...}",
            lineno=15,
            type="dict",
        )
        assert defn.value is None
        assert defn.type == "dict"


class TestSettingUsageItem:
    """Test SettingUsageItem model."""

    def test_basic_usage(self) -> None:
        """Test creating a basic usage."""
        usage = SettingUsageItem(
            statement="if settings.DEBUG:",
            lineno=25,
        )
        assert usage.statement == "if settings.DEBUG:"
        assert usage.lineno == 25

    def test_usage_validation(self) -> None:
        """Test that line number must be >= 1."""
        with pytest.raises(ValueError):
            SettingUsageItem(
                statement="settings.DEBUG",
                lineno=0,
            )


class TestSettingInfo:
    """Test SettingInfo model."""

    def test_basic_info(self) -> None:
        """Test creating basic setting info."""
        info = SettingInfo(
            definition_count=1,
            usage_count=5,
            type_list=["bool"],
            definitions={},
            usages={},
        )
        assert info.definition_count == 1
        assert info.usage_count == 5
        assert info.type_list == ["bool"]

    def test_info_with_data(self) -> None:
        """Test setting info with definitions and usages."""
        defn = SettingDefinitionItem(
            value=True,
            statement="DEBUG = True",
            lineno=1,
            type="bool",
        )
        usage = SettingUsageItem(
            statement="if settings.DEBUG:",
            lineno=10,
        )
        info = SettingInfo(
            definition_count=1,
            usage_count=1,
            type_list=["bool"],
            definitions={"settings.py": [defn]},
            usages={"views.py": [usage]},
        )
        assert len(info.definitions) == 1
        assert len(info.usages) == 1


class TestDjangoSettingsSummary:
    """Test DjangoSettingsSummary model."""

    def test_summary(self) -> None:
        """Test creating a summary."""
        summary = DjangoSettingsSummary(
            total_count=10,
            files_scanned=5,
            scan_duration_ms=100,
            total_settings=10,
            total_definitions=15,
            total_usages=50,
        )
        assert summary.total_settings == 10
        assert summary.total_definitions == 15
        assert summary.total_usages == 50

    def test_summary_validation(self) -> None:
        """Test that negative values are rejected."""
        with pytest.raises(ValueError):
            DjangoSettingsSummary(
                total_count=-1,
                files_scanned=0,
                scan_duration_ms=0,
                total_settings=0,
                total_definitions=0,
                total_usages=0,
            )


class TestDjangoSettingsOutput:
    """Test DjangoSettingsOutput model."""

    def test_output_structure(self) -> None:
        """Test output structure."""
        info = SettingInfo(
            definition_count=1,
            usage_count=2,
            type_list=["bool"],
            definitions={},
            usages={},
        )
        summary = DjangoSettingsSummary(
            total_count=1,
            files_scanned=1,
            scan_duration_ms=50,
            total_settings=1,
            total_definitions=1,
            total_usages=2,
        )
        output = DjangoSettingsOutput(
            summary=summary,
            results={"DEBUG": info},
        )
        assert len(output.results) == 1
        assert "DEBUG" in output.results

    def test_output_serialization(self) -> None:
        """Test that output can be serialized."""
        info = SettingInfo(
            definition_count=1,
            usage_count=0,
            type_list=["str"],
            definitions={},
            usages={},
        )
        summary = DjangoSettingsSummary(
            total_count=1,
            files_scanned=1,
            scan_duration_ms=50,
            total_settings=1,
            total_definitions=1,
            total_usages=0,
        )
        output = DjangoSettingsOutput(
            summary=summary,
            results={"SECRET_KEY": info},
        )
        data = output.model_dump()
        assert "summary" in data
        assert "results" in data
