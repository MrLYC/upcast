"""Data models for unit test scanner."""

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class TargetModule(BaseModel):
    """A module targeted by test imports.

    Attributes:
        module_path: Module path (e.g., 'myapp.models')
        symbols: Imported symbols from the module
    """

    module_path: str = Field(description="Module path")
    symbols: list[str] = Field(description="Imported symbols")


class UnitTestInfo(BaseModel):
    """Information about a unit test function.

    Attributes:
        name: Test function name
        file: File path
        line_range: (start_line, end_line) tuple
        body_md5: MD5 hash of test body
        assert_count: Number of assertions in test
        targets: List of imported modules/symbols
        class_name: Parent test class name if any
        fixtures: Fixture-like parameters used by the test
        markers: Pytest marker names applied to the test
        parametrize: Compact pytest parametrize metadata
        expanded_count: Expanded case count for parametrized tests
    """

    name: str = Field(description="Test function name")
    file: str = Field(description="File path")
    line_range: tuple[int, int] = Field(description="(start_line, end_line)")
    body_md5: str = Field(description="MD5 hash of test body")
    assert_count: int = Field(ge=0, description="Number of assertions")
    targets: list[TargetModule] = Field(description="Imported modules")
    class_name: str | None = Field(default=None, description="Parent test class name if any")
    fixtures: list[str] = Field(default_factory=list, description="Fixture-like parameters excluding self/cls")
    markers: list[str] = Field(default_factory=list, description="Pytest marker names excluding parametrize")
    parametrize: list[dict[str, str | int]] = Field(
        default_factory=list, description="Compact pytest parametrize metadata"
    )
    expanded_count: int = Field(default=1, ge=1, description="Expanded case count for parametrized tests")


class UnitTestSummary(ScannerSummary):
    """Summary statistics for unit tests.

    Attributes:
        total_tests: Number of test functions
        total_files: Number of test files
        total_assertions: Total assertion count
    """

    total_tests: int = Field(ge=0, description="Number of test functions")
    total_files: int = Field(ge=0, description="Number of test files")
    total_assertions: int = Field(ge=0, description="Total assertions")


class UnitTestOutput(ScannerOutput[UnitTestSummary, dict[str, list[UnitTestInfo]]]):
    """Complete output from unit test scanner.

    Attributes:
        summary: Summary statistics
        results: Tests grouped by file path
    """

    summary: UnitTestSummary
    results: dict[str, list[UnitTestInfo]] = Field(description="Tests grouped by file path")
