"""Data models for static queue usage findings."""

from typing import Any

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class QueueParameter(BaseModel):
    """A queue-related argument and its static-analysis evidence."""

    name: str = Field(description="Canonical parameter name")
    expression: str | None = Field(None, description="Source expression for the parameter")
    value: Any = Field(None, description="Best-effort static value, or a redaction marker")
    source_kind: str = Field(description="literal, static_constant, configuration, runtime, expression, or unknown")
    hardcoded: bool | None = Field(
        None,
        description="Whether the parameter is hardcoded; None means static analysis cannot decide",
    )


class QueueUsage(BaseModel):
    """One statically detected queue construction or operation."""

    category: str = Field(description="Queue category")
    framework: str = Field(description="Concrete library or framework")
    operation: str = Field(description="Operation such as construct, publish, consume, or configure")
    file: str = Field(description="Relative source file path")
    line: int = Field(gt=0, description="Source line")
    column: int = Field(ge=0, description="Source column")
    statement: str | None = Field(None, description="Redacted source statement")
    function: str | None = Field(None, description="Enclosing function name")
    class_name: str | None = Field(None, description="Enclosing class name")
    parameters: list[QueueParameter] = Field(default_factory=list, description="Relevant queue parameters")
    hardcoding_status: str = Field(description="Aggregate parameter status")


class QueueUsageSummary(ScannerSummary):
    """Summary statistics for queue usage findings."""

    total_usages: int = Field(ge=0, description="Total queue findings")
    by_category: dict[str, int] = Field(default_factory=dict, description="Findings grouped by queue category")
    by_framework: dict[str, int] = Field(default_factory=dict, description="Findings grouped by framework")
    hardcoded_parameters: int = Field(ge=0, description="Parameters classified as hardcoded")
    dynamic_parameters: int = Field(ge=0, description="Parameters classified as dynamic")
    unknown_parameters: int = Field(ge=0, description="Parameters whose hardcoding status is unknown")


class QueueUsageOutput(ScannerOutput[QueueUsageSummary, dict[str, list[QueueUsage]]]):
    """Complete output from the queue usage scanner."""

    summary: QueueUsageSummary = Field(description="Summary statistics")
    results: dict[str, list[QueueUsage]] = Field(default_factory=dict, description="Findings grouped by category")
