"""Data models for environment variable scanner."""

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class EnvVarLocation(BaseModel):
    """A location where an environment variable is accessed.

    Attributes:
        file: File path
        line: Line number
        column: Column number
        pattern: Access pattern (e.g., os.environ['VAR'], os.getenv('VAR'))
        code: Code snippet
    """

    file: str = Field(..., description="File path")
    line: int = Field(..., ge=1, description="Line number")
    column: int = Field(default=0, ge=0, description="Column number")
    pattern: str = Field(..., description="Access pattern")
    code: str | None = Field(None, description="Code snippet")


class EnvVarInfo(BaseModel):
    """Information about an environment variable.

    Attributes:
        name: Environment variable name
        required: Whether variable is required (no default provided)
        default_value: Default value if provided
        locations: List of access locations
    """

    name: str = Field(..., description="Environment variable name")
    required: bool = Field(..., description="Whether variable is required")
    default_value: str | None = Field(None, description="Default value if provided")
    locations: list[EnvVarLocation] = Field(default_factory=list, description="Access locations")


class EnvVarSummary(ScannerSummary):
    """Summary statistics for environment variables.

    Attributes:
        total_env_vars: Total number of environment variables
        required_count: Number of required variables
        optional_count: Number of optional variables
    """

    total_env_vars: int = Field(ge=0, description="Total environment variables")
    required_count: int = Field(ge=0, description="Required variables")
    optional_count: int = Field(ge=0, description="Optional variables")


class EnvVarOutput(ScannerOutput[dict[str, EnvVarInfo]]):
    """Complete output from environment variable scanner.

    Attributes:
        summary: Summary statistics
        results: Environment variables keyed by name
    """

    summary: EnvVarSummary
    results: dict[str, EnvVarInfo] = Field(..., description="Environment variables")
