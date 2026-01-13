"""Integration tests for environment variable scanner."""

from pathlib import Path

import pytest

from upcast.scanners.env_vars import EnvVarScanner


class TestEnvVarScanner:
    """Test EnvVarScanner integration."""

    def test_scan_os_getenv(self, tmp_path: Path, scanner: EnvVarScanner) -> None:
        """Test scanning os.getenv()."""
        code_file = tmp_path / "config.py"
        code_file.write_text("""
import os

api_key = os.getenv('API_KEY')
""")

        result = scanner.scan(tmp_path)

        assert "API_KEY" in result.results
        assert result.results["API_KEY"].required is True

    def test_scan_os_getenv_with_default(self, tmp_path: Path, scanner: EnvVarScanner) -> None:
        """Test scanning os.getenv() with default value."""
        code_file = tmp_path / "config.py"
        code_file.write_text("""
import os

debug = os.getenv('DEBUG', 'False')
""")

        result = scanner.scan(tmp_path)

        assert "DEBUG" in result.results
        assert result.results["DEBUG"].required is False
        assert result.results["DEBUG"].default_value == "False"

    def test_scan_os_environ_subscript(self, tmp_path: Path, scanner: EnvVarScanner) -> None:
        """Test scanning os.environ['VAR']."""
        code_file = tmp_path / "settings.py"
        code_file.write_text("""
import os

secret = os.environ['SECRET_KEY']
""")

        result = scanner.scan(tmp_path)

        assert "SECRET_KEY" in result.results
        assert result.results["SECRET_KEY"].required is True

    def test_scan_os_environ_get(self, tmp_path: Path, scanner: EnvVarScanner) -> None:
        """Test scanning os.environ.get()."""
        code_file = tmp_path / "config.py"
        code_file.write_text("""
import os

host = os.environ.get('DATABASE_HOST', 'localhost')
""")

        result = scanner.scan(tmp_path)

        assert "DATABASE_HOST" in result.results
        assert result.results["DATABASE_HOST"].required is False

    def test_scan_multiple_variables(self, tmp_path: Path, scanner: EnvVarScanner) -> None:
        """Test scanning multiple environment variables."""
        code_file = tmp_path / "config.py"
        code_file.write_text("""
import os

api_key = os.getenv('API_KEY')
debug = os.getenv('DEBUG', 'False')
secret = os.environ['SECRET_KEY']
""")

        result = scanner.scan(tmp_path)

        assert len(result.results) >= 3
        assert "API_KEY" in result.results
        assert "DEBUG" in result.results
        assert "SECRET_KEY" in result.results

    def test_scan_duplicate_variable(self, tmp_path: Path, scanner: EnvVarScanner) -> None:
        """Test scanning same variable multiple times."""
        code_file = tmp_path / "config.py"
        code_file.write_text("""
import os

api_key1 = os.getenv('API_KEY')
api_key2 = os.getenv('API_KEY')
""")

        result = scanner.scan(tmp_path)

        assert "API_KEY" in result.results
        # Should have 2 locations
        assert len(result.results["API_KEY"].locations) == 2

    def test_scan_multiple_files(self, tmp_path: Path, scanner: EnvVarScanner) -> None:
        """Test scanning multiple files."""
        (tmp_path / "config.py").write_text("""
import os
api_key = os.getenv('API_KEY')
""")
        (tmp_path / "settings.py").write_text("""
import os
api_key = os.getenv('API_KEY')
""")

        result = scanner.scan(tmp_path)

        assert "API_KEY" in result.results
        assert len(result.results["API_KEY"].locations) == 2

    def test_scan_empty_directory(self, tmp_path: Path, scanner: EnvVarScanner) -> None:
        """Test scanning empty directory."""
        result = scanner.scan(tmp_path)

        assert result.summary.total_env_vars == 0
        assert len(result.results) == 0

    def test_scan_no_env_vars(self, tmp_path: Path, scanner: EnvVarScanner) -> None:
        """Test scanning file without environment variables."""
        code_file = tmp_path / "utils.py"
        code_file.write_text("""
def hello():
    return "world"
""")

        result = scanner.scan(tmp_path)

        assert result.summary.total_env_vars == 0

    def test_scan_summary_statistics(self, tmp_path: Path, scanner: EnvVarScanner) -> None:
        """Test summary statistics."""
        code_file = tmp_path / "config.py"
        code_file.write_text("""
import os

required1 = os.getenv('REQUIRED1')
required2 = os.environ['REQUIRED2']
optional1 = os.getenv('OPTIONAL1', 'default1')
optional2 = os.environ.get('OPTIONAL2', 'default2')
""")

        result = scanner.scan(tmp_path)

        assert result.summary.total_env_vars == 4
        assert result.summary.required_count == 2
        assert result.summary.optional_count == 2
        assert result.summary.files_scanned >= 1
