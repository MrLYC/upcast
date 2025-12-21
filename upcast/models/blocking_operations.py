"""Data models for blocking operations scanner."""

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class BlockingOperation(BaseModel):
    """A single blocking operation detected.

    Attributes:
        file: File path where operation was found
        line: Line number
        column: Column number
        category: Operation category (time_based, database, synchronization, subprocess)
        operation: Operation name (e.g., time.sleep, requests.get)
        statement: Code statement containing the operation
        function: Containing function name if applicable
        class_name: Containing class name if applicable
    """

    file: str = Field(..., description="File path")
    line: int = Field(..., ge=1, description="Line number")
    column: int = Field(default=0, ge=0, description="Column number")
    category: str = Field(..., description="Operation category")
    operation: str = Field(..., description="Operation name")
    statement: str | None = Field(None, description="Code statement")
    function: str | None = Field(None, description="Containing function")
    class_name: str | None = Field(None, description="Containing class")


class BlockingOperationsSummary(ScannerSummary):
    """Summary statistics for blocking operations.

    Attributes:
        by_category: Count by category (time_based, database, synchronization, subprocess)
    """

    by_category: dict[str, int] = Field(
        default_factory=dict,
        description="Count by category (time_based, database, synchronization, subprocess)",
    )


class BlockingOperationsOutput(ScannerOutput[dict[str, list[BlockingOperation]]]):
    """Complete output from blocking operations scanner.

    Attributes:
        summary: Summary statistics
        results: Operations grouped by category
    """

    summary: BlockingOperationsSummary
    results: dict[str, list[BlockingOperation]] = Field(
        ..., alias="operations", description="Operations grouped by category"
    )
