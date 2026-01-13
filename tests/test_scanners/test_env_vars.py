"""Tests for EnvVarScanner models and implementation."""

import pytest
from pydantic import ValidationError

from upcast.scanners.env_vars import (
    EnvVarInfo,
    EnvVarLocation,
    EnvVarOutput,
    EnvVarScanner,
    EnvVarSummary,
)


class TestEnvVarLocationModel:
    """Tests for EnvVarLocation Pydantic model."""

    def test_valid_location(self):
        """Test creating valid EnvVarLocation."""
        location = EnvVarLocation(
            file="app/config.py",
            line=10,
            statement="os.getenv('DATABASE_URL')",
        )

        assert location.file == "app/config.py"
        assert location.line == 10
        assert "DATABASE_URL" in location.statement

    def test_location_validates_line_number(self):
        """Test that line number must be >= 1."""
        with pytest.raises(ValidationError):
            EnvVarLocation(file="test.py", line=0, statement="test")

    def test_location_statement_required(self):
        """Test that statement is required."""
        location = EnvVarLocation(file="test.py", line=1, statement="test")
        assert location.statement == "test"

    def test_location_with_optional_fields(self):
        """Test EnvVarLocation with only required fields."""
        location = EnvVarLocation(file="test.py", line=1, statement="test_pattern")

        assert location.file == "test.py"
        assert location.line == 1


class TestEnvVarInfoModel:
    """Tests for EnvVarInfo Pydantic model."""

    def test_valid_env_var_info_required(self):
        """Test creating required env var."""
        info = EnvVarInfo(
            name="API_KEY",
            required=True,
            default_value="",
            locations=[EnvVarLocation(file="api.py", line=5, statement="os.getenv('API_KEY')")],
        )

        assert info.name == "API_KEY"
        assert info.required is True
        assert info.default_value == ""
        assert len(info.locations) == 1

    def test_valid_env_var_info_optional(self):
        """Test creating optional env var with default."""
        info = EnvVarInfo(
            name="DEBUG",
            required=False,
            default_value="False",
            locations=[EnvVarLocation(file="settings.py", line=10, statement="os.getenv('DEBUG')")],
        )

        assert info.required is False
        assert info.default_value == "False"

    def test_env_var_info_multiple_locations(self):
        """Test env var with multiple usage locations."""
        info = EnvVarInfo(
            name="DATABASE_URL",
            required=True,
            locations=[
                EnvVarLocation(file="db.py", line=10, statement="os.environ['DATABASE_URL']"),
                EnvVarLocation(file="migrations.py", line=20, statement="os.getenv('DATABASE_URL')"),
            ],
        )

        assert len(info.locations) == 2
        assert info.locations[0].file == "db.py"
        assert info.locations[1].file == "migrations.py"

    def test_env_var_info_empty_locations(self):
        """Test env var with empty locations list."""
        info = EnvVarInfo(
            name="UNUSED_VAR",
            required=False,
            locations=[],
        )

        assert len(info.locations) == 0


class TestEnvVarSummaryModel:
    """Tests for EnvVarSummary Pydantic model."""

    def test_valid_summary(self):
        """Test creating valid EnvVarSummary."""
        summary = EnvVarSummary(
            total_count=10,
            files_scanned=5,
            scan_duration_ms=1200,
            total_env_vars=10,
            required_count=6,
            optional_count=4,
        )

        assert summary.total_count == 10
        assert summary.total_env_vars == 10
        assert summary.required_count == 6
        assert summary.optional_count == 4

    def test_summary_validates_negative_counts(self):
        """Test that negative counts are rejected."""
        with pytest.raises(ValidationError):
            EnvVarSummary(
                total_count=5,
                files_scanned=2,
                required_count=-1,  # invalid
            )

    def test_summary_with_defaults(self):
        """Test EnvVarSummary with minimal fields."""
        summary = EnvVarSummary(
            total_count=3,
            files_scanned=1,
            total_env_vars=3,
            required_count=2,
            optional_count=1,
        )

        assert summary.total_env_vars == 3
        assert summary.required_count == 2
        assert summary.optional_count == 1


class TestEnvVarOutputModel:
    """Tests for EnvVarOutput Pydantic model."""

    def test_valid_output(self):
        """Test creating valid EnvVarOutput."""
        summary = EnvVarSummary(
            total_count=2,
            files_scanned=1,
            total_env_vars=2,
            required_count=1,
            optional_count=1,
        )

        results = {
            "API_KEY": EnvVarInfo(
                name="API_KEY",
                required=True,
                locations=[EnvVarLocation(file="api.py", line=10, statement="os.getenv('API_KEY')")],
            ),
            "DEBUG": EnvVarInfo(
                name="DEBUG",
                required=False,
                default_value="False",
                locations=[EnvVarLocation(file="settings.py", line=20, statement="os.getenv('DEBUG')")],
            ),
        }

        output = EnvVarOutput(summary=summary, results=results, metadata={})

        assert output.summary.total_count == 2
        assert len(output.results) == 2
        assert "API_KEY" in output.results
        assert output.results["API_KEY"].required is True

    def test_output_serialization(self):
        """Test EnvVarOutput can be serialized to dict."""
        summary = EnvVarSummary(total_count=1, files_scanned=1, total_env_vars=1, required_count=1, optional_count=0)
        results = {
            "TEST": EnvVarInfo(name="TEST", required=True, locations=[]),
        }

        output = EnvVarOutput(summary=summary, results=results, metadata={})
        data = output.model_dump()

        assert data["summary"]["total_count"] == 1
        assert "TEST" in data["results"]

    def test_output_json_serialization(self):
        """Test EnvVarOutput can be serialized to JSON."""
        summary = EnvVarSummary(total_count=1, files_scanned=1, total_env_vars=1, required_count=0, optional_count=1)
        results = {"VAR": EnvVarInfo(name="VAR", required=False, locations=[])}

        output = EnvVarOutput(summary=summary, results=results, metadata={})
        json_str = output.model_dump_json()

        assert "VAR" in json_str
        assert "summary" in json_str


class TestEnvVarScannerIntegration:
    """Integration tests for EnvVarScanner."""

    def test_scanner_detects_getenv(self, tmp_path):
        """Test scanner detects os.getenv() calls."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import os

api_key = os.getenv('API_KEY')
debug = os.getenv('DEBUG', 'False')
"""
        )

        scanner = EnvVarScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_env_vars == 2
        assert "API_KEY" in output.results
        assert "DEBUG" in output.results
        assert output.results["API_KEY"].required is True
        assert output.results["DEBUG"].required is False
        assert output.results["DEBUG"].default_value == "False"

    def test_scanner_detects_environ_subscript(self, tmp_path):
        """Test scanner detects os.environ['KEY'] patterns."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import os

database_url = os.environ['DATABASE_URL']
secret_key = os.environ['SECRET_KEY']
"""
        )

        scanner = EnvVarScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_env_vars == 2
        assert "DATABASE_URL" in output.results
        assert "SECRET_KEY" in output.results
        assert output.results["DATABASE_URL"].required is True
        assert output.results["SECRET_KEY"].required is True

    def test_scanner_detects_environ_get(self, tmp_path):
        """Test scanner detects os.environ.get() patterns."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import os

host = os.environ.get('HOST', 'localhost')
port = os.environ.get('PORT', 8000)
"""
        )

        scanner = EnvVarScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_env_vars == 2
        assert "HOST" in output.results
        assert output.results["HOST"].required is False
        assert output.results["HOST"].default_value == "localhost"
        assert output.results["PORT"].required is False
        assert output.results["PORT"].default_value == "8000"

    def test_scanner_handles_multiple_locations(self, tmp_path):
        """Test scanner tracks multiple usages of same env var."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import os

api_key1 = os.getenv('API_KEY')
api_key2 = os.environ['API_KEY']
api_key3 = os.environ.get('API_KEY', 'default')
"""
        )

        scanner = EnvVarScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_env_vars == 1
        assert "API_KEY" in output.results
        assert len(output.results["API_KEY"].locations) == 3
        # Should be marked required because of os.environ[] usage
        assert output.results["API_KEY"].required is True

    def test_scanner_handles_empty_file(self, tmp_path):
        """Test scanner handles files with no env vars."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
def hello():
    return "Hello, World!"
"""
        )

        scanner = EnvVarScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_env_vars == 0
        assert len(output.results) == 0
        assert output.summary.files_scanned == 1

    def test_scanner_with_invalid_syntax(self, tmp_path):
        """Test scanner handles files with syntax errors."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import os
def broken(
    # Missing closing parenthesis
"""
        )

        scanner = EnvVarScanner()
        output = scanner.scan(test_file)

        # Should handle gracefully, return empty results
        assert output.summary.total_env_vars == 0

    def test_scanner_with_directory(self, tmp_path):
        """Test scanner can scan entire directory."""
        (tmp_path / "file1.py").write_text("import os\nval1 = os.getenv('VAR1')")
        (tmp_path / "file2.py").write_text("import os\nval2 = os.getenv('VAR2')")

        scanner = EnvVarScanner()
        output = scanner.scan(tmp_path)

        assert output.summary.total_env_vars == 2
        assert "VAR1" in output.results
        assert "VAR2" in output.results
        assert output.summary.files_scanned == 2

    def test_scanner_respects_patterns(self, tmp_path):
        """Test scanner respects include/exclude patterns."""
        (tmp_path / "include.py").write_text("import os\nval = os.getenv('INCLUDED')")
        (tmp_path / "exclude.py").write_text("import os\nval = os.getenv('EXCLUDED')")

        scanner = EnvVarScanner(include_patterns=["**/include.py"])
        output = scanner.scan(tmp_path)

        assert output.summary.total_env_vars == 1
        assert "INCLUDED" in output.results
        assert "EXCLUDED" not in output.results

    def test_scanner_calculates_summary_correctly(self, tmp_path):
        """Test scanner calculates summary statistics correctly."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import os

required = os.environ['REQUIRED']
optional1 = os.getenv('OPTIONAL1', 'default1')
optional2 = os.getenv('OPTIONAL2', 'default2')
"""
        )

        scanner = EnvVarScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 3
        assert output.summary.total_env_vars == 3
        assert output.summary.required_count == 1
        assert output.summary.optional_count == 2
        assert output.summary.files_scanned == 1
        assert output.summary.scan_duration_ms >= 0
