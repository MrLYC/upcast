"""Data models for concurrency pattern scanner."""

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

    file: str = Field(description="File path")
    line: int | None = Field(ge=1, description="Line number")
    column: int | None = Field(ge=0, description="Column number")
    pattern: str = Field(description="Pattern type")
    statement: str | None = Field(None, description="Code statement")


class ConcurrencyPatternSummary(ScannerSummary):
    """Summary statistics for concurrency patterns.

    Attributes:
        by_category: Count by category (threading, multiprocessing, asyncio, celery)
    """

    by_category: dict[str, int] = Field(
        ...,
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
        description="Patterns grouped by category and type",
    )
