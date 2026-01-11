"""Data models for Django settings scanner."""

from typing import Any

from pydantic import Field

from upcast.models.base import BaseModel, ScannerOutput, ScannerSummary


class SettingDefinitionItem(BaseModel):
    """A single definition of a setting.

    Attributes:
        file: File path
        value: Inferred static value, None if cannot infer
        statement: Code statement
        lineno: Line number
        type: Inferred type (e.g., 'str', 'int', 'bool', 'dict', 'list', 'dynamic')
    """

    file: str = Field(description="File path")
    value: Any | None = Field(None, description="Inferred static value")
    statement: str = Field(description="Code statement")
    lineno: int = Field(ge=1, description="Line number")
    type: str = Field(description="Inferred type")


class SettingUsageItem(BaseModel):
    """A single usage of a setting.

    Attributes:
        file: File path
        statement: Code statement
        lineno: Line number
    """

    file: str = Field(description="File path")
    statement: str = Field(description="Code statement")
    lineno: int = Field(ge=1, description="Line number")


class SettingInfo(BaseModel):
    """Comprehensive information about a setting variable.

    Attributes:
        definition_count: Number of definitions
        usage_count: Number of usages
        definition_types: List of possible types inferred from definitions
        definitions: List of definitions
        usages: List of usages
    """

    definition_count: int = Field(ge=0, description="Number of definitions")
    usage_count: int = Field(ge=0, description="Number of usages")
    definition_types: list[str] = Field(description="List of possible types")
    definitions: list[SettingDefinitionItem] = Field(description="Definitions")
    usages: list[SettingUsageItem] = Field(description="Usages")


class DjangoSettingsSummary(ScannerSummary):
    """Summary statistics for Django settings.

    Attributes:
        total_settings: Number of unique settings
        total_definitions: Total definition count
        total_usages: Total usage count
    """

    total_settings: int = Field(ge=0, description="Number of unique settings")
    total_definitions: int = Field(ge=0, description="Total definition count")
    total_usages: int = Field(ge=0, description="Total usage count")


class DjangoSettingsOutput(ScannerOutput[dict[str, SettingInfo]]):
    """Output for Django settings scan.

    Attributes:
        summary: Summary statistics
        results: Settings information keyed by setting name
    """

    summary: DjangoSettingsSummary
    results: dict[str, SettingInfo] = Field(description="Settings information")
