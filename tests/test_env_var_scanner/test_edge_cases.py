"""Tests for environment variable scanner edge cases."""

import pytest

from upcast.scanners.env_vars import EnvVarScanner


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_file(self, scanner: EnvVarScanner, tmp_path):
        """Test scanning empty file."""
        file_path = tmp_path / "empty.py"
        file_path.write_text("")

        result = scanner.scan(tmp_path)

        assert len(result.results) == 0
        assert result.summary.total_env_vars == 0

    def test_file_without_env_vars(self, scanner: EnvVarScanner, tmp_path):
        """Test file without any environment variables."""
        code = """
def hello():
    return "Hello, World!"

class MyClass:
    pass
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert len(result.results) == 0

    def test_invalid_syntax_file(self, scanner: EnvVarScanner, tmp_path):
        """Test file with invalid Python syntax."""
        code = """
import os
this is not valid python syntax!!!
api_key = os.getenv('API_KEY')
"""
        file_path = tmp_path / "invalid.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        # Scanner should handle parse errors gracefully
        assert isinstance(result.results, dict)

    def test_getenv_without_arguments(self, scanner: EnvVarScanner, tmp_path):
        """Test getenv() called without arguments."""
        code = """
import os
# Invalid call - no arguments
val = os.getenv()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        # Should not crash, but also should not detect any variables
        assert len(result.results) == 0

    def test_getenv_with_non_string_literal(self, scanner: EnvVarScanner, tmp_path):
        """Test getenv() with variable instead of string literal."""
        code = """
import os
key_name = 'API_KEY'
val = os.getenv(key_name)
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        # The scanner can infer simple variable references
        assert len(result.results) == 1
        assert "API_KEY" in result.results

    def test_environ_subscript_non_string(self, scanner: EnvVarScanner, tmp_path):
        """Test os.environ[] with non-string index."""
        code = """
import os
idx = 0
val = os.environ[idx]  # Invalid - must be string literal
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert len(result.results) == 0

    def test_environ_del_statement(self, scanner: EnvVarScanner, tmp_path):
        """Test os.environ in delete statement (should be ignored)."""
        code = """
import os
del os.environ['TEMP_VAR']
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        # Delete statements should be ignored
        assert len(result.results) == 0

    def test_non_os_environ_subscript(self, scanner: EnvVarScanner, tmp_path):
        """Test subscript on non-os.environ objects."""
        code = """
data = {'key': 'value'}
val = data['key']  # Should not be detected

api = get_api()
result = api.environ['KEY']  # Should not be detected
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        # Should not detect non-os.environ subscripts
        assert len(result.results) == 0

    def test_non_os_getenv_calls(self, scanner: EnvVarScanner, tmp_path):
        """Test getenv calls on non-os modules."""
        code = """
import custom_module

val = custom_module.getenv('KEY')
result = obj.getenv('VAR')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        # The scanner detects any getenv() call containing 'getenv' in the name
        # This is a limitation of the current implementation
        assert len(result.results) == 2
        assert "KEY" in result.results
        assert "VAR" in result.results

    def test_commented_out_env_vars(self, scanner: EnvVarScanner, tmp_path):
        """Test commented out environment variable usage."""
        code = """
import os
# api_key = os.getenv('API_KEY')
# secret = os.environ['SECRET']
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        # Comments should be ignored
        assert len(result.results) == 0

    def test_env_var_in_string(self, scanner: EnvVarScanner, tmp_path):
        """Test environment variable mentioned in string."""
        code = """
import os
message = "Please set the API_KEY environment variable"
doc = '''
Use os.getenv('SECRET') to get the secret
'''
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        # String literals should not be detected as env var usage
        assert len(result.results) == 0

    def test_extremely_long_variable_name(self, scanner: EnvVarScanner, tmp_path):
        """Test very long environment variable name."""
        code = f"""
import os
val = os.getenv('{"A" * 1000}')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "A" * 1000 in result.results
        assert len(result.results["A" * 1000].name) == 1000

    def test_unicode_variable_name(self, scanner: EnvVarScanner, tmp_path):
        """Test environment variable with unicode characters."""
        code = """
import os
val = os.getenv('API_KEY_日本語')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "API_KEY_日本語" in result.results

    def test_special_characters_in_name(self, scanner: EnvVarScanner, tmp_path):
        """Test environment variable with special characters."""
        code = """
import os
val1 = os.getenv('MY-VAR')
val2 = os.getenv('MY.VAR')
val3 = os.getenv('MY:VAR')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "MY-VAR" in result.results
        assert "MY.VAR" in result.results
        assert "MY:VAR" in result.results

    def test_nested_subscripts(self, scanner: EnvVarScanner, tmp_path):
        """Test nested subscript expressions."""
        code = """
import os
configs = {'prod': os.environ}
val = configs['prod']['API_KEY']  # Should not be detected
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        # Nested subscripts should not be detected
        assert len(result.results) == 0

    def test_environ_in_list_comprehension(self, scanner: EnvVarScanner, tmp_path):
        """Test environment variable in list comprehension."""
        code = """
import os
keys = [os.getenv(k) for k in ['KEY1', 'KEY2']]
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        # Dynamic key names in comprehension
        assert len(result.results) == 0

    def test_environ_in_dict_comprehension(self, scanner: EnvVarScanner, tmp_path):
        """Test environment variable in dict comprehension."""
        code = """
import os
config = {k: os.getenv(k) for k in ['HOST', 'PORT']}
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        # Dynamic key names
        assert len(result.results) == 0

    def test_multiple_files_same_directory(self, scanner: EnvVarScanner, tmp_path):
        """Test scanning multiple files in same directory."""
        file1 = tmp_path / "file1.py"
        file1.write_text("import os\nkey1 = os.getenv('KEY1')")

        file2 = tmp_path / "file2.py"
        file2.write_text("import os\nkey2 = os.getenv('KEY2')")

        result = scanner.scan(tmp_path)

        assert len(result.results) == 2
        assert "KEY1" in result.results
        assert "KEY2" in result.results
        assert result.summary.files_scanned == 2

    def test_non_python_files_ignored(self, scanner: EnvVarScanner, tmp_path):
        """Test that non-Python files are ignored."""
        python_file = tmp_path / "test.py"
        python_file.write_text("import os\nval = os.getenv('KEY')")

        txt_file = tmp_path / "readme.txt"
        txt_file.write_text("os.getenv('IGNORED')")

        result = scanner.scan(tmp_path)

        assert len(result.results) == 1
        assert "KEY" in result.results
        assert "IGNORED" not in result.results
