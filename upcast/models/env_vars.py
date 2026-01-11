"""Data models for environment variable scanner."""

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class EnvVarLocation(BaseModel):
    """A location where an environment variable is accessed.

    Attributes:
        file: File path
        line: Line number
        statement: Code snippet containing the env var access
        type: Inferred type (string, int, bool, etc.) or 'unknown'
    """

    file: str = Field(description="File path")
    line: int | None = Field(ge=1, description="Line number")
    statement: str | None = Field(None, description="Code snippet")
    type: str = Field(default="unknown", description="Inferred type")


class EnvVarInfo(BaseModel):
    """Information about an environment variable.

    Attributes:
        name: Environment variable name
        required: Whether variable is required (no default provided)
        default_value: Default value if provided
        types: Aggregated types from all locations
        locations: List of access locations
    """

    name: str = Field(description="Environment variable name")
    required: bool = Field(description="Whether variable is required")
    default_value: str | None = Field(None, description="Default value if provided")
    types: list[str] = Field(default_factory=list, description="Aggregated types")
    locations: list[EnvVarLocation] = Field(description="Access locations")


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
    results: dict[str, EnvVarInfo] = Field(description="Environment variables")
