"""Data models for Django settings scanner."""

from typing import Any

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class SettingsLocation(BaseModel):
    """A location where a setting is used.

    Attributes:
        file: File path
        line: Line number
        column: Column number
        pattern: Usage pattern (e.g., settings.DEBUG)
        code: Code snippet
    """

    file: str = Field(..., description="File path")
    line: int = Field(..., ge=1, description="Line number")
    column: int = Field(..., ge=0, description="Column number")
    pattern: str = Field(..., description="Usage pattern")
    code: str | None = Field(None, description="Code snippet")


class SettingsUsage(BaseModel):
    """Usage information for a setting variable.

    Attributes:
        count: Number of usages
        locations: List of usage locations
    """

    count: int = Field(..., ge=0, description="Number of usages")
    locations: list[SettingsLocation] = Field(default_factory=list, description="Usage locations")


class SettingDefinition(BaseModel):
    """A setting definition in a settings module.

    Attributes:
        value: Static value if determinable
        statement: Dynamic assignment statement if value is not static
        lineno: Line number
        overrides: Module path this overrides (for multiple settings files)
    """

    value: Any | None = Field(None, description="Static value")
    statement: str | None = Field(None, description="Dynamic assignment statement")
    lineno: int = Field(..., ge=1, description="Line number")
    overrides: str | None = Field(None, description="Module path this overrides")


class DynamicImport(BaseModel):
    """A dynamic import in settings module.

    Attributes:
        pattern: Import pattern
        base_module: Base module if determinable
        file: File path
        line: Line number
    """

    pattern: str = Field(..., description="Import pattern")
    base_module: str | None = Field(None, description="Base module")
    file: str = Field(..., description="File path")
    line: int = Field(..., ge=1, description="Line number")


class SettingsModule(BaseModel):
    """A Django settings module.

    Attributes:
        definitions: Setting definitions keyed by setting name
        star_imports: List of 'from X import *' statements
        dynamic_imports: List of dynamic import patterns
    """

    definitions: dict[str, SettingDefinition] = Field(default_factory=dict, description="Setting definitions")
    star_imports: list[str] = Field(default_factory=list, description="From X import * statements")
    dynamic_imports: list[DynamicImport] = Field(default_factory=list, description="Dynamic imports")


class DjangoSettingsSummary(ScannerSummary):
    """Summary statistics for Django settings.

    Attributes:
        total_settings: Number of unique settings
        total_usages: Total usage count
    """

    total_settings: int = Field(..., ge=0, description="Number of unique settings")
    total_usages: int = Field(..., ge=0, description="Total usage count")


class DjangoSettingsUsageOutput(ScannerOutput[dict[str, SettingsUsage]]):
    """Output for settings usage scan.

    Attributes:
        summary: Summary statistics
        results: Settings usages keyed by setting name
    """

    summary: DjangoSettingsSummary
    results: dict[str, SettingsUsage] = Field(..., description="Settings usages")


class DjangoSettingsDefinitionOutput(ScannerOutput[dict[str, SettingsModule]]):
    """Output for settings definition scan.

    Attributes:
        summary: Summary statistics
        results: Settings modules keyed by module path
    """

    summary: DjangoSettingsSummary
    results: dict[str, SettingsModule] = Field(..., description="Settings definitions")


class DjangoSettingsCombinedOutput(BaseModel):
    """Combined output for both definitions and usages.

    Attributes:
        definitions: Settings modules keyed by module path
        usages: Settings usages keyed by setting name
    """

    definitions: dict[str, SettingsModule] = Field(..., description="Settings definitions")
    usages: dict[str, SettingsUsage] = Field(..., description="Settings usages")
