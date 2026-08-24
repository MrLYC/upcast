"""Data models for static Django offset usage findings."""

from typing import Any

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class OffsetParameter(BaseModel):
    """A pagination parameter and its static-analysis evidence."""

    name: str = Field(description="Canonical parameter name")
    expression: str | None = Field(None, description="Source expression for the parameter")
    value: Any = Field(None, description="Best-effort static value")
    source_kind: str = Field(description="literal, static_constant, configuration, runtime, expression, or unknown")
    hardcoded: bool | None = Field(
        None,
        description="Whether the parameter is hardcoded; None means static analysis cannot decide",
    )


class OffsetUsage(BaseModel):
    """One statically detected statement that can produce SQL offset pagination."""

    pattern: str = Field(description="Finding pattern such as queryset_slice or raw_sql")
    framework: str = Field(description="Framework or API family")
    operation: str = Field(description="Operation such as slice, paginate, or execute")
    file: str = Field(description="Relative source file path")
    line: int = Field(gt=0, description="Source line")
    column: int = Field(ge=0, description="Source column")
    statement: str | None = Field(None, description="Source statement")
    function: str | None = Field(None, description="Enclosing function name")
    class_name: str | None = Field(None, description="Enclosing class name")
    parameters: list[OffsetParameter] = Field(default_factory=list, description="Pagination parameters")
    offset: OffsetParameter | None = Field(None, description="Offset evidence")
    limit: OffsetParameter | None = Field(None, description="Limit evidence")
    page: OffsetParameter | None = Field(None, description="Page-number evidence")
    page_size: OffsetParameter | None = Field(None, description="Page-size evidence")
    hardcoding_status: str = Field(description="Aggregate parameter status")
    warning: str | None = Field(None, description="Static-analysis warning")


class OffsetUsageSummary(ScannerSummary):
    """Summary statistics for an offset usage scan."""

    by_pattern: dict[str, int] = Field(default_factory=dict, description="Finding count by pattern")
    by_framework: dict[str, int] = Field(default_factory=dict, description="Finding count by framework")
    direct_offset_count: int = Field(ge=0, default=0, description="Findings with direct offset evidence")
    indirect_pagination_count: int = Field(ge=0, default=0, description="Findings with indirect pagination evidence")
    dynamic_count: int = Field(ge=0, default=0, description="Findings with dynamic offset-related parameters")


class OffsetUsageOutput(ScannerOutput[OffsetUsageSummary, dict[str, list[OffsetUsage]]]):
    """Complete offset usage scanner output."""

    summary: OffsetUsageSummary = Field(description="Summary statistics")
    results: dict[str, list[OffsetUsage]] = Field(default_factory=dict, description="Findings grouped by pattern")
