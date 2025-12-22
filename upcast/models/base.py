"""Base Pydantic models for scanner outputs.

This module provides base models that all scanners extend to ensure
consistent structure, type safety, and validation across all scanner outputs.
"""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ScannerSummary(BaseModel):
    """Base summary model for all scanners.

    All scanner-specific summary models must extend this class and include
    these required fields.

    Attributes:
        total_count: Total number of items found by the scanner
        files_scanned: Number of files that were scanned
        scan_duration_ms: Duration of the scan in milliseconds (optional)
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    total_count: int = Field(..., ge=0, description="Total items found")
    files_scanned: int = Field(..., ge=0, description="Number of files scanned")
    scan_duration_ms: int | None = Field(None, ge=0, description="Scan duration in milliseconds")


class ScannerOutput(BaseModel, Generic[T]):
    """Base output model for all scanners.

    All scanner outputs must follow this structure with summary, results,
    and metadata fields.

    Type Parameters:
        T: The type of the results field (scanner-specific)

    Attributes:
        summary: Summary information about the scan
        results: Scanner-specific results (type varies by scanner)
        metadata: Additional metadata about the scan
    """

    model_config = ConfigDict(extra="allow")  # Allow scanner-specific metadata

    summary: ScannerSummary
    results: T
    metadata: dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for export.

        Returns:
            Dictionary representation with None values excluded
        """
        return self.model_dump(mode="python", exclude_none=True)

    def to_json(self, **kwargs: Any) -> str:
        """Export as JSON string.

        Args:
            **kwargs: Additional arguments passed to model_dump_json

        Returns:
            JSON string representation
        """
        return self.model_dump_json(**kwargs)
