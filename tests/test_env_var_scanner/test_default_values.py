"""Tests for environment variable default value handling."""

import pytest

from upcast.scanners.env_vars import EnvVarScanner


class TestDefaultValues:
    """Test default value extraction and handling."""

    def test_string_default(self, scanner: EnvVarScanner, tmp_path):
        """Test string default value."""
        code = """
import os
host = os.getenv('HOST', 'localhost')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.results["HOST"].default_value == "localhost"
        assert result.results["HOST"].required is False

    def test_numeric_default(self, scanner: EnvVarScanner, tmp_path):
        """Test numeric default value (as string)."""
        code = """
import os
port = os.getenv('PORT', '8080')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.results["PORT"].default_value == "8080"

    def test_empty_string_default(self, scanner: EnvVarScanner, tmp_path):
        """Test empty string as default value."""
        code = """
import os
prefix = os.getenv('PREFIX', '')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.results["PREFIX"].default_value == ""
        assert result.results["PREFIX"].required is False

    def test_none_default(self, scanner: EnvVarScanner, tmp_path):
        """Test None as explicit default value."""
        code = """
import os
optional = os.getenv('OPTIONAL', None)
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        # None is not stored as a string, but the var is still optional
        assert result.results["OPTIONAL"].default_value is None
        assert result.results["OPTIONAL"].required is False

    def test_boolean_default(self, scanner: EnvVarScanner, tmp_path):
        """Test boolean default value (as string)."""
        code = """
import os
debug = os.getenv('DEBUG', 'False')
enabled = os.getenv('ENABLED', 'True')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.results["DEBUG"].default_value == "False"
        assert result.results["ENABLED"].default_value == "True"

    def test_dynamic_default_value(self, scanner: EnvVarScanner, tmp_path):
        """Test dynamic/computed default values."""
        code = """
import os
config_path = os.getenv('CONFIG', get_default_path())
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        # Dynamic values should be marked as "<dynamic>"
        assert result.results["CONFIG"].default_value == "<dynamic>"
        assert result.results["CONFIG"].required is False

    def test_variable_as_default(self, scanner: EnvVarScanner, tmp_path):
        """Test variable as default value."""
        code = """
import os
default_host = 'localhost'
host = os.getenv('HOST', default_host)
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        # The scanner can infer the value if it's a simple variable
        assert result.results["HOST"].default_value == "localhost"

    def test_multiple_defaults_same_variable(self, scanner: EnvVarScanner, tmp_path):
        """Test same variable with different defaults (first one wins)."""
        code = """
import os
# First access with default 'foo'
val1 = os.getenv('VAR', 'foo')
# Second access with default 'bar'
val2 = os.getenv('VAR', 'bar')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        # First default value should be recorded
        assert result.results["VAR"].default_value == "foo"

    def test_required_then_optional(self, scanner: EnvVarScanner, tmp_path):
        """Test variable accessed first without default, then with default."""
        code = """
import os
# First: required
val1 = os.getenv('KEY')
# Second: optional
val2 = os.getenv('KEY', 'default')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        # Should be marked as required (most strict)
        assert result.results["KEY"].required is True
        # Should still capture default value
        assert result.results["KEY"].default_value == "default"

    def test_optional_then_required(self, scanner: EnvVarScanner, tmp_path):
        """Test variable accessed first with default, then without."""
        code = """
import os
# First: optional
val1 = os.getenv('KEY', 'default')
# Second: required
val2 = os.getenv('KEY')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        # Should be marked as required (most strict)
        assert result.results["KEY"].required is True
        assert result.results["KEY"].default_value == "default"

    def test_environ_get_with_default(self, scanner: EnvVarScanner, tmp_path):
        """Test os.environ.get() with default value."""
        code = """
import os
timeout = os.environ.get('TIMEOUT', '30')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.results["TIMEOUT"].default_value == "30"
        assert result.results["TIMEOUT"].required is False

    def test_subscript_no_default(self, scanner: EnvVarScanner, tmp_path):
        """Test os.environ[] subscript has no default."""
        code = """
import os
key = os.environ['API_KEY']
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.results["API_KEY"].default_value is None
        assert result.results["API_KEY"].required is True

    def test_keyword_default_argument(self, scanner: EnvVarScanner, tmp_path):
        """Test keyword argument for default."""
        code = """
import os
host = os.getenv('HOST', default='0.0.0.0')
port = os.environ.get('PORT', default='9000')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.results["HOST"].default_value == "0.0.0.0"
        assert result.results["PORT"].default_value == "9000"
