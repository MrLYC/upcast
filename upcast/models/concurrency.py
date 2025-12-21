"""Data models for concurrency pattern scanner."""

from typing import Any

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class ConcurrencyUsage(BaseModel):
    """A single usage of a concurrency pattern.

    Attributes:
        file: File path where pattern was used
        line: Line number
        column: Column number
        pattern: Pattern type (e.g., threading.Thread, asyncio.create_task)
        statement: Code statement
        context: Additional context information
    """

    file: str = Field(..., description="File path")
    line: int = Field(..., ge=1, description="Line number")
    column: int = Field(default=0, ge=0, description="Column number")
    pattern: str = Field(..., description="Pattern type")
    statement: str | None = Field(None, description="Code statement")
    context: dict[str, Any] | None = Field(None, description="Additional context")


class ConcurrencyPatternSummary(ScannerSummary):
    """Summary statistics for concurrency patterns.

    Attributes:
        by_category: Count by category (threading, multiprocessing, asyncio, celery)
    """

    by_category: dict[str, int] = Field(
        default_factory=dict,
        description="Count by category (threading, multiprocessing, asyncio, celery)",
    )


class ConcurrencyPatternOutput(ScannerOutput[dict[str, dict[str, list[ConcurrencyUsage]]]]):
    """Complete output from concurrency pattern scanner.

    Attributes:
        summary: Summary statistics
        results: Patterns grouped by category and type
    """

    summary: ConcurrencyPatternSummary
    results: dict[str, dict[str, list[ConcurrencyUsage]]] = Field(
        ...,
        alias="concurrency_patterns",
        description="Patterns grouped by category and type",
    )
