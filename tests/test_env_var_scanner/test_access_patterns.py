"""Tests for environment variable access patterns."""

import pytest

from upcast.scanners.env_vars import EnvVarScanner


class TestAccessPatterns:
    """Test various environment variable access patterns."""

    def test_os_getenv_simple(self, scanner: EnvVarScanner, tmp_path):
        """Test os.getenv() without default."""
        code = """
import os
api_key = os.getenv('API_KEY')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "API_KEY" in result.results
        assert result.results["API_KEY"].required is True
        assert result.results["API_KEY"].default_value is None
        assert len(result.results["API_KEY"].locations) == 1
        assert "os.getenv" in result.results["API_KEY"].locations[0].pattern

    def test_os_getenv_with_default(self, scanner: EnvVarScanner, tmp_path):
        """Test os.getenv() with default value."""
        code = """
import os
host = os.getenv('HOST', 'localhost')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "HOST" in result.results
        assert result.results["HOST"].required is False
        assert result.results["HOST"].default_value == "localhost"

    def test_os_getenv_with_keyword_default(self, scanner: EnvVarScanner, tmp_path):
        """Test os.getenv() with keyword default."""
        code = """
import os
port = os.getenv('PORT', default='8080')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "PORT" in result.results
        assert result.results["PORT"].required is False
        assert result.results["PORT"].default_value == "8080"

    def test_os_environ_subscript(self, scanner: EnvVarScanner, tmp_path):
        """Test os.environ['KEY'] subscript access."""
        code = """
import os
secret = os.environ['SECRET_KEY']
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "SECRET_KEY" in result.results
        assert result.results["SECRET_KEY"].required is True
        assert result.results["SECRET_KEY"].default_value is None
        assert "os.environ['SECRET_KEY']" in result.results["SECRET_KEY"].locations[0].pattern

    def test_os_environ_get_method(self, scanner: EnvVarScanner, tmp_path):
        """Test os.environ.get() method."""
        code = """
import os
timeout = os.environ.get('TIMEOUT')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "TIMEOUT" in result.results
        assert result.results["TIMEOUT"].required is True
        assert result.results["TIMEOUT"].default_value is None

    def test_os_environ_get_with_default(self, scanner: EnvVarScanner, tmp_path):
        """Test os.environ.get() with default value."""
        code = """
import os
debug = os.environ.get('DEBUG', 'False')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "DEBUG" in result.results
        assert result.results["DEBUG"].required is False
        assert result.results["DEBUG"].default_value == "False"

    def test_from_os_import_getenv(self, scanner: EnvVarScanner, tmp_path):
        """Test 'from os import getenv' pattern."""
        code = """
from os import getenv
token = getenv('TOKEN')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "TOKEN" in result.results
        assert result.results["TOKEN"].required is True

    def test_from_os_import_environ(self, scanner: EnvVarScanner, tmp_path):
        """Test 'from os import environ' with subscript."""
        code = """
from os import environ
user = environ['USERNAME']
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "USERNAME" in result.results
        assert result.results["USERNAME"].required is True
        assert "environ['USERNAME']" in result.results["USERNAME"].locations[0].pattern

    def test_from_os_import_environ_get(self, scanner: EnvVarScanner, tmp_path):
        """Test 'from os import environ' with .get()."""
        code = """
from os import environ
path = environ.get('PATH', '/usr/bin')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "PATH" in result.results
        assert result.results["PATH"].required is False
        assert result.results["PATH"].default_value == "/usr/bin"

    def test_mixed_access_patterns_same_variable(self, scanner: EnvVarScanner, tmp_path):
        """Test same variable accessed with different patterns."""
        code = """
import os

# First access - required
key1 = os.getenv('API_KEY')

# Second access - with default
key2 = os.getenv('API_KEY', 'default')

# Third access - subscript
key3 = os.environ['API_KEY']
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "API_KEY" in result.results
        # Should be marked as required because at least one access is required
        assert result.results["API_KEY"].required is True
        # Should have default value from the second access
        assert result.results["API_KEY"].default_value == "default"
        # Should have all 3 locations
        assert len(result.results["API_KEY"].locations) == 3

    def test_chained_getenv_calls(self, scanner: EnvVarScanner, tmp_path):
        """Test chained getenv calls."""
        code = """
import os
config = os.getenv('PRIMARY') or os.getenv('SECONDARY', 'fallback')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "PRIMARY" in result.results
        assert "SECONDARY" in result.results
        assert result.results["PRIMARY"].required is True
        assert result.results["SECONDARY"].required is False

    def test_nested_function_calls(self, scanner: EnvVarScanner, tmp_path):
        """Test env vars in nested function calls."""
        code = """
import os
port = int(os.getenv('PORT', '8080'))
url = f"http://{os.getenv('HOST')}"
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "PORT" in result.results
        assert "HOST" in result.results
        assert result.results["PORT"].required is False
        assert result.results["HOST"].required is True

    def test_os_environ_in_function_def(self, scanner: EnvVarScanner, tmp_path):
        """Test os.environ in function definition."""
        code = """
import os

def get_config():
    return os.getenv('CONFIG')

def get_secret():
    return os.environ['SECRET']
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "CONFIG" in result.results
        assert "SECRET" in result.results
        assert len(result.results) == 2

    def test_os_environ_in_class(self, scanner: EnvVarScanner, tmp_path):
        """Test os.environ in class definition."""
        code = """
import os

class Config:
    HOST = os.getenv('HOST', 'localhost')
    PORT = os.environ['PORT']
    
    def get_url(self):
        return os.getenv('URL')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "HOST" in result.results
        assert "PORT" in result.results
        assert "URL" in result.results
        assert result.results["HOST"].required is False
        assert result.results["PORT"].required is True
        assert result.results["URL"].required is True
