"""Tests for environment variable Pydantic models."""

import pytest

from upcast.models.env_vars import EnvVarInfo, EnvVarLocation, EnvVarOutput, EnvVarSummary


class TestEnvVarLocation:
    """Test EnvVarLocation model."""

    def test_basic_location(self) -> None:
        """Test creating basic location."""
        loc = EnvVarLocation(
            file="config.py",
            line=10,
            column=4,
            pattern="os.getenv",
            code='os.getenv("API_KEY")',
        )
        assert loc.file == "config.py"
        assert loc.line == 10
        assert loc.pattern == "os.getenv"

    def test_location_without_code(self) -> None:
        """Test location without code snippet."""
        loc = EnvVarLocation(
            file="settings.py",
            line=5,
            column=0,
            pattern="os.environ",
        )
        assert loc.code is None


class TestEnvVarInfo:
    """Test EnvVarInfo model."""

    def test_required_variable(self) -> None:
        """Test required environment variable."""
        info = EnvVarInfo(
            name="API_KEY",
            required=True,
            locations=[],
        )
        assert info.name == "API_KEY"
        assert info.required is True
        assert info.default_value is None

    def test_optional_variable(self) -> None:
        """Test optional environment variable with default."""
        info = EnvVarInfo(
            name="DEBUG",
            required=False,
            default_value="False",
            locations=[],
        )
        assert info.required is False
        assert info.default_value == "False"

    def test_variable_with_locations(self) -> None:
        """Test variable with multiple locations."""
        loc1 = EnvVarLocation(file="a.py", line=1, column=0, pattern="os.getenv")
        loc2 = EnvVarLocation(file="b.py", line=5, column=0, pattern="os.environ")
        info = EnvVarInfo(
            name="DATABASE_URL",
            required=True,
            locations=[loc1, loc2],
        )
        assert len(info.locations) == 2


class TestEnvVarSummary:
    """Test EnvVarSummary model."""

    def test_summary(self) -> None:
        """Test creating summary."""
        summary = EnvVarSummary(
            total_count=10,
            files_scanned=5,
            scan_duration_ms=100,
            total_env_vars=10,
            required_count=7,
            optional_count=3,
        )
        assert summary.total_env_vars == 10
        assert summary.required_count == 7
        assert summary.optional_count == 3

    def test_summary_validation(self) -> None:
        """Test that negative values are rejected."""
        with pytest.raises(ValueError):
            EnvVarSummary(
                total_count=-1,
                files_scanned=0,
                scan_duration_ms=0,
                total_env_vars=0,
                required_count=0,
                optional_count=0,
            )


class TestEnvVarOutput:
    """Test EnvVarOutput model."""

    def test_output_structure(self) -> None:
        """Test output structure."""
        info = EnvVarInfo(name="API_KEY", required=True, locations=[])
        summary = EnvVarSummary(
            total_count=1,
            files_scanned=1,
            scan_duration_ms=50,
            total_env_vars=1,
            required_count=1,
            optional_count=0,
        )
        output = EnvVarOutput(summary=summary, results={"API_KEY": info})
        assert len(output.results) == 1
        assert "API_KEY" in output.results

    def test_output_serialization(self) -> None:
        """Test that output can be serialized."""
        info = EnvVarInfo(name="SECRET", required=True, locations=[])
        summary = EnvVarSummary(
            total_count=1,
            files_scanned=1,
            scan_duration_ms=50,
            total_env_vars=1,
            required_count=1,
            optional_count=0,
        )
        output = EnvVarOutput(summary=summary, results={"SECRET": info})
        data = output.model_dump()
        assert "summary" in data
        assert "results" in data
