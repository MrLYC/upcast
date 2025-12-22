"""Data models for cyclomatic complexity scanner."""

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class ComplexityResult(BaseModel):
    """Complexity result for a single function.

    Attributes:
        name: Function name
        line: Start line number
        end_line: End line number
        complexity: Cyclomatic complexity score
        severity: Severity level (warning, high_risk, critical)
        message: Optional message about the complexity
    """

    name: str = Field(..., description="Function name")
    line: int = Field(..., ge=1, description="Start line number")
    end_line: int = Field(..., ge=1, description="End line number")
    complexity: int = Field(..., ge=0, description="Cyclomatic complexity score")
    severity: str = Field(..., description="Severity level (warning, high_risk, critical)")
    message: str | None = Field(None, description="Optional message")


class ComplexitySummary(ScannerSummary):
    """Summary statistics for complexity analysis.

    Attributes:
        high_complexity_count: Functions above threshold
        by_severity: Count by severity level
    """

    high_complexity_count: int = Field(ge=0, description="Functions above threshold")
    by_severity: dict[str, int] = Field(default_factory=dict, description="Count by severity level")


class ComplexityOutput(ScannerOutput[dict[str, list[ComplexityResult]]]):
    """Complete output from complexity scanner.

    Attributes:
        summary: Summary statistics
        results: Results grouped by module path
    """

    summary: ComplexitySummary
    results: dict[str, list[ComplexityResult]] = Field(..., description="Results grouped by module path")
