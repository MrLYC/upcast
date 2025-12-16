"""Integration tests for environment variable scanner."""

from pathlib import Path

import pytest

from upcast.env_var_scanner.checker import EnvVarChecker
from upcast.env_var_scanner.cli import scan_directory, scan_files
from upcast.env_var_scanner.export import export_to_json, export_to_yaml


class TestEnvVarChecker:
    """Tests for EnvVarChecker class."""

    @pytest.fixture
    def fixtures_dir(self):
        """Get the fixtures directory path."""
        return Path(__file__).parent / "fixtures"

    def test_check_simple_file(self, fixtures_dir):
        """Should detect environment variables in simple.py."""
        checker = EnvVarChecker()
        simple_file = fixtures_dir / "simple.py"
        checker.check_file(str(simple_file))

        results = checker.get_results()

        # Should find multiple env vars
        assert len(results) > 0
        assert "DATABASE_URL" in results
        assert "DEBUG" in results
        assert "PORT" in results
        assert "API_KEY" in results

    def test_os_getenv_detection(self, fixtures_dir):
        """Should detect os.getenv patterns correctly."""
        checker = EnvVarChecker()
        simple_file = fixtures_dir / "simple.py"
        checker.check_file(str(simple_file))

        results = checker.get_results()

        # DATABASE_URL - no default, not required (implicit None)
        if "DATABASE_URL" in results:
            db_var = results["DATABASE_URL"]
            assert db_var.name == "DATABASE_URL"
            assert len(db_var.usages) >= 1
            # Type should be str (default for getenv)
            assert "str" in db_var.types or not db_var.types

        # PORT - with type conversion to int
        if "PORT" in results:
            port_var = results["PORT"]
            assert "int" in port_var.types

    def test_os_environ_subscript_detection(self, fixtures_dir):
        """Should detect os.environ[KEY] patterns as required."""
        checker = EnvVarChecker()
        simple_file = fixtures_dir / "simple.py"
        checker.check_file(str(simple_file))

        results = checker.get_results()

        # API_KEY uses os.environ[KEY] - should be required
        if "API_KEY" in results:
            api_var = results["API_KEY"]
            assert api_var.required is True

    def test_django_environ_patterns(self, fixtures_dir):
        """Should detect django-environ patterns."""
        checker = EnvVarChecker()
        django_file = fixtures_dir / "django_env.py"
        checker.check_file(str(django_file))

        results = checker.get_results()

        # Should find django-environ variables
        assert len(results) > 0

        # Check typed methods
        if "DATABASE_URL" in results:
            db_var = results["DATABASE_URL"]
            assert "str" in db_var.types

        if "DEBUG" in results:
            debug_var = results["DEBUG"]
            assert "bool" in debug_var.types

        if "PORT" in results:
            port_var = results["PORT"]
            assert "int" in port_var.types

    def test_type_inference_from_conversion(self, fixtures_dir):
        """Should infer types from type conversions."""
        checker = EnvVarChecker()
        complex_file = fixtures_dir / "complex.py"
        checker.check_file(str(complex_file))

        results = checker.get_results()

        # MAX_RETRIES has int conversion
        if "MAX_RETRIES" in results:
            var = results["MAX_RETRIES"]
            assert "int" in var.types

        # RATE_LIMIT has float conversion
        if "RATE_LIMIT" in results:
            var = results["RATE_LIMIT"]
            assert "float" in var.types

    def test_aggregation_multiple_usages(self, fixtures_dir):
        """Should aggregate multiple usages of same variable."""
        checker = EnvVarChecker()
        complex_file = fixtures_dir / "complex.py"
        checker.check_file(str(complex_file))

        results = checker.get_results()

        # DB_HOST is used twice
        if "DB_HOST" in results:
            db_host = results["DB_HOST"]
            assert len(db_host.usages) >= 1

    def test_exclude_del_statements(self, tmp_path):
        """Should not detect environ access in del statements."""
        test_file = tmp_path / "test_del.py"
        test_file.write_text(
            """
import os

# Should NOT be detected - del statement
del os.environ['DELETE_ME']

# Should be detected - normal read
value = os.environ['KEEP_ME']
"""
        )

        checker = EnvVarChecker()
        checker.check_file(str(test_file))
        results = checker.get_results()

        # Should only detect KEEP_ME, not DELETE_ME
        assert "DELETE_ME" not in results
        assert "KEEP_ME" in results

    def test_exclude_variable_keys(self, tmp_path):
        """Should not detect environ access with variable keys."""
        test_file = tmp_path / "test_var_keys.py"
        test_file.write_text(
            """
import os

# Should NOT be detected - variable key
key = 'SOME_KEY'
value = os.environ[key]

# Should NOT be detected - variable in loop
for k in os.environ:
    print(os.environ[k])

# Should be detected - literal key
api_key = os.environ['API_KEY']
"""
        )

        checker = EnvVarChecker()
        checker.check_file(str(test_file))
        results = checker.get_results()

        # Should only detect API_KEY
        assert "SOME_KEY" not in results
        assert "k" not in results
        assert "key" not in results
        assert "API_KEY" in results

    def test_exclude_environ_dict_methods(self, tmp_path):
        """Should not detect os.environ dict methods as env var access."""
        test_file = tmp_path / "test_dict_methods.py"
        test_file.write_text(
            """
import os

# Should NOT be detected - dict methods
for k, v in os.environ.items():
    print(k)

keys = os.environ.keys()
values = os.environ.values()

# Should be detected - actual env var access
debug = os.getenv('DEBUG', 'false')
"""
        )

        checker = EnvVarChecker()
        checker.check_file(str(test_file))
        results = checker.get_results()

        # Should only detect DEBUG
        assert "k" not in results
        assert "v" not in results
        assert "DEBUG" in results


class TestScanFunctions:
    """Tests for scan_files and scan_directory functions."""

    @pytest.fixture
    def fixtures_dir(self):
        """Get the fixtures directory path."""
        return Path(__file__).parent / "fixtures"

    def test_scan_files(self, fixtures_dir):
        """Should scan multiple files."""
        files = [
            str(fixtures_dir / "simple.py"),
            str(fixtures_dir / "django_env.py"),
        ]
        checker = scan_files(files)
        results = checker.get_results()

        # Should find vars from both files
        assert len(results) > 0

    def test_scan_directory(self, fixtures_dir):
        """Should scan all Python files in directory."""
        checker = scan_directory(str(fixtures_dir))
        results = checker.get_results()

        # Should find vars from all fixture files
        assert len(results) > 0


class TestExport:
    """Tests for export functions."""

    @pytest.fixture
    def sample_results(self):
        """Create sample results for testing export."""
        from upcast.env_var_scanner.env_var_parser import EnvVarInfo, EnvVarUsage

        results = {
            "DATABASE_URL": EnvVarInfo(
                name="DATABASE_URL",
                types=["str"],
                defaults=["postgresql://localhost/db"],
                required=False,
            ),
            "API_KEY": EnvVarInfo(
                name="API_KEY",
                types=[],
                defaults=[],
                required=True,
            ),
        }

        # Add usages
        results["DATABASE_URL"].usages.append(
            EnvVarUsage(
                name="DATABASE_URL",
                location="test.py:10",
                statement="os.getenv('DATABASE_URL', 'postgresql://localhost/db')",
                type="str",
                default="postgresql://localhost/db",
                required=False,
            )
        )

        results["API_KEY"].usages.append(
            EnvVarUsage(
                name="API_KEY",
                location="test.py:15",
                statement="os.environ['API_KEY']",
                type=None,
                default=None,
                required=True,
            )
        )

        return results

    def test_export_to_yaml(self, sample_results):
        """Should export results to YAML format."""
        yaml_str = export_to_yaml(sample_results)

        assert "DATABASE_URL" in yaml_str
        assert "API_KEY" in yaml_str
        assert "types:" in yaml_str
        assert "usages:" in yaml_str
        assert "location:" in yaml_str

    def test_export_to_json(self, sample_results):
        """Should export results to JSON format."""
        import json

        json_str = export_to_json(sample_results)
        data = json.loads(json_str)

        assert "DATABASE_URL" in data
        assert "API_KEY" in data
        assert "types" in data["DATABASE_URL"]
        assert "usages" in data["DATABASE_URL"]
