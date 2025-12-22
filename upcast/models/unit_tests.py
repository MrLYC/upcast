"""Data models for unit test scanner."""

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class TargetModule(BaseModel):
    """A module targeted by test imports.

    Attributes:
        module: Module path (e.g., 'myapp.models')
        symbols: Imported symbols from the module
    """

    module: str = Field(..., description="Module path")
    symbols: list[str] = Field(default_factory=list, description="Imported symbols")


class UnitTestInfo(BaseModel):
    """Information about a unit test function.

    Attributes:
        name: Test function name
        file: File path
        line_range: (start_line, end_line) tuple
        body_md5: MD5 hash of test body
        assert_count: Number of assertions in test
        targets: List of imported modules/symbols
    """

    name: str = Field(..., description="Test function name")
    file: str = Field(..., description="File path")
    line_range: tuple[int, int] = Field(..., description="(start_line, end_line)")
    body_md5: str = Field(..., description="MD5 hash of test body")
    assert_count: int = Field(..., ge=0, description="Number of assertions")
    targets: list[TargetModule] = Field(default_factory=list, description="Imported modules")


class UnitTestSummary(ScannerSummary):
    """Summary statistics for unit tests.

    Attributes:
        total_tests: Number of test functions
        total_files: Number of test files
        total_assertions: Total assertion count
    """

    total_tests: int = Field(..., ge=0, description="Number of test functions")
    total_files: int = Field(..., ge=0, description="Number of test files")
    total_assertions: int = Field(..., ge=0, description="Total assertions")


class UnitTestOutput(ScannerOutput[dict[str, list[UnitTestInfo]]]):
    """Complete output from unit test scanner.

    Attributes:
        summary: Summary statistics
        results: Tests grouped by file path
    """

    summary: UnitTestSummary
    results: dict[str, list[UnitTestInfo]] = Field(..., description="Tests grouped by file path")
