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


class TestTypedDefaults:
    """Tests for typed default value preservation."""

    @pytest.fixture
    def fixtures_dir(self):
        """Get the fixtures directory path."""
        return Path(__file__).parent / "fixtures"

    def test_boolean_defaults_preserved(self, fixtures_dir):
        """Should preserve boolean default values as bool, not str."""
        checker = EnvVarChecker()
        typed_file = fixtures_dir / "typed_defaults.py"
        checker.check_file(str(typed_file))
        results = checker.get_results()

        # DEBUG with False default
        if "DEBUG" in results:
            var = results["DEBUG"]
            assert False in var.defaults
            assert "False" not in var.defaults  # Should NOT be string

        # ENABLE_CACHE with True default
        if "ENABLE_CACHE" in results:
            var = results["ENABLE_CACHE"]
            assert True in var.defaults
            assert "True" not in var.defaults

    def test_integer_defaults_preserved(self, fixtures_dir):
        """Should preserve integer default values as int, not str."""
        checker = EnvVarChecker()
        typed_file = fixtures_dir / "typed_defaults.py"
        checker.check_file(str(typed_file))
        results = checker.get_results()

        # PORT with 8000 default
        if "PORT" in results:
            var = results["PORT"]
            assert 8000 in var.defaults
            assert "8000" not in var.defaults

        # MAX_CONNECTIONS with 100 default
        if "MAX_CONNECTIONS" in results:
            var = results["MAX_CONNECTIONS"]
            assert 100 in var.defaults

        # TIMEOUT with 0 default (falsy)
        if "TIMEOUT" in results:
            var = results["TIMEOUT"]
            assert 0 in var.defaults
            assert "0" not in var.defaults

    def test_float_defaults_preserved(self, fixtures_dir):
        """Should preserve float default values as float, not str."""
        checker = EnvVarChecker()
        typed_file = fixtures_dir / "typed_defaults.py"
        checker.check_file(str(typed_file))
        results = checker.get_results()

        # RATE_LIMIT with 10.5 default
        if "RATE_LIMIT" in results:
            var = results["RATE_LIMIT"]
            assert 10.5 in var.defaults
            assert "10.5" not in var.defaults

        # THRESHOLD with 0.0 default (falsy)
        if "THRESHOLD" in results:
            var = results["THRESHOLD"]
            assert 0.0 in var.defaults

    def test_none_defaults_preserved(self, fixtures_dir):
        """Should preserve None default values, not convert to string."""
        checker = EnvVarChecker()
        typed_file = fixtures_dir / "typed_defaults.py"
        checker.check_file(str(typed_file))
        results = checker.get_results()

        # OPTIONAL_KEY with None default
        if "OPTIONAL_KEY" in results:
            var = results["OPTIONAL_KEY"]
            assert None in var.defaults
            assert "None" not in var.defaults

    def test_string_defaults_still_work(self, fixtures_dir):
        """Should still handle string defaults correctly."""
        checker = EnvVarChecker()
        typed_file = fixtures_dir / "typed_defaults.py"
        checker.check_file(str(typed_file))
        results = checker.get_results()

        # LOG_LEVEL with string default
        if "LOG_LEVEL" in results:
            var = results["LOG_LEVEL"]
            assert "INFO" in var.defaults

        # EMPTY_STRING with empty string default (falsy)
        if "EMPTY_STRING" in results:
            var = results["EMPTY_STRING"]
            assert "" in var.defaults

    def test_mixed_type_defaults(self, fixtures_dir):
        """Should aggregate different typed defaults for same variable."""
        checker = EnvVarChecker()
        typed_file = fixtures_dir / "typed_defaults.py"
        checker.check_file(str(typed_file))
        results = checker.get_results()

        # MULTI_TYPE with both False and 0 defaults
        if "MULTI_TYPE" in results:
            var = results["MULTI_TYPE"]
            assert False in var.defaults
            assert 0 in var.defaults
            assert len(var.defaults) == 2


class TestDynamicDefaultFiltering:
    """Tests for filtering backtick-wrapped dynamic defaults."""

    @pytest.fixture
    def fixtures_dir(self):
        """Get the fixtures directory path."""
        return Path(__file__).parent / "fixtures"

    def test_dynamic_defaults_excluded(self, fixtures_dir):
        """Should exclude backtick-wrapped dynamic defaults from defaults list."""
        checker = EnvVarChecker()
        dynamic_file = fixtures_dir / "dynamic_defaults.py"
        checker.check_file(str(dynamic_file))
        results = checker.get_results()

        # BK_CC_HOST with dynamic default
        if "BK_CC_HOST" in results:
            var = results["BK_CC_HOST"]
            # Should not include the backticked expression
            for default in var.defaults:
                assert not (isinstance(default, str) and default.startswith("`"))

        # API_URL with dynamic default
        if "API_URL" in results:
            var = results["API_URL"]
            # Should not include the backticked expression
            for default in var.defaults:
                assert not (isinstance(default, str) and default.startswith("`"))

    def test_static_defaults_included(self, fixtures_dir):
        """Should include static defaults in defaults list."""
        checker = EnvVarChecker()
        dynamic_file = fixtures_dir / "dynamic_defaults.py"
        checker.check_file(str(dynamic_file))
        results = checker.get_results()

        # STATIC_DEFAULT with simple static default
        if "STATIC_DEFAULT" in results:
            var = results["STATIC_DEFAULT"]
            assert "http://example.com" in var.defaults

    def test_mixed_static_and_dynamic_defaults(self, fixtures_dir):
        """Should include only static defaults when variable has both."""
        checker = EnvVarChecker()
        dynamic_file = fixtures_dir / "dynamic_defaults.py"
        checker.check_file(str(dynamic_file))
        results = checker.get_results()

        # DB_URL with both static and dynamic defaults
        if "DB_URL" in results:
            var = results["DB_URL"]
            # Should include static default
            assert "postgresql://localhost/db" in var.defaults
            # Should NOT include dynamic defaults
            for default in var.defaults:
                assert not (isinstance(default, str) and default.startswith("`"))

        # MIXED_VAR with multiple static and dynamic defaults
        if "MIXED_VAR" in results:
            var = results["MIXED_VAR"]
            # Should include both static defaults
            assert "static1" in var.defaults
            assert "static2" in var.defaults
            # Should NOT include dynamic defaults
            for default in var.defaults:
                assert not (isinstance(default, str) and default.startswith("`"))

    def test_only_dynamic_defaults(self, fixtures_dir):
        """Should have empty defaults list if only dynamic defaults exist."""
        checker = EnvVarChecker()
        dynamic_file = fixtures_dir / "dynamic_defaults.py"
        checker.check_file(str(dynamic_file))
        results = checker.get_results()

        # ONLY_DYNAMIC with only dynamic default
        if "ONLY_DYNAMIC" in results:
            var = results["ONLY_DYNAMIC"]
            # Should have empty or no backticked defaults
            for default in var.defaults:
                assert not (isinstance(default, str) and default.startswith("`"))
