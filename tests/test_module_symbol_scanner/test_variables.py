"""Tests for variable detection in module symbol scanner."""

from pathlib import Path

import pytest

from upcast.scanners.module_symbols import ModuleSymbolScanner


class TestBasicVariables:
    """Test basic variable detection."""

    def test_simple_variable(self, tmp_path: Path) -> None:
        """Test detection of simple variable assignment."""
        code = """
x = 42
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert "x" in result.variables
        assert result.variables["x"].value == "42"
        assert "x = 42" in result.variables["x"].statement

    def test_string_variable(self, tmp_path: Path) -> None:
        """Test detection of string variable."""
        code = """
name = "test"
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert "name" in result.variables
        assert result.variables["name"].value == "test"

    def test_multiple_variables(self, tmp_path: Path) -> None:
        """Test detection of multiple variables."""
        code = """
x = 1
y = 2
z = 3
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert len(result.variables) == 3
        assert "x" in result.variables
        assert "y" in result.variables
        assert "z" in result.variables


class TestComplexVariables:
    """Test complex variable types."""

    def test_list_variable(self, tmp_path: Path) -> None:
        """Test detection of list variable."""
        code = """
items = [1, 2, 3]
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert "items" in result.variables

    def test_dict_variable(self, tmp_path: Path) -> None:
        """Test detection of dict variable."""
        code = """
config = {"key": "value"}
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert "config" in result.variables

    def test_function_call_variable(self, tmp_path: Path) -> None:
        """Test variable assigned from function call."""
        code = """
result = some_function()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert "result" in result.variables


class TestPrivateVariables:
    """Test private variable handling."""

    def test_private_variable_excluded_by_default(self, tmp_path: Path) -> None:
        """Test that private variables are excluded by default."""
        code = """
_private = 42
public = 10
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner(include_private=False)
        result = scanner.scan_file(file_path)

        assert result is not None
        assert "_private" not in result.variables
        assert "public" in result.variables

    def test_private_variable_included_when_enabled(self, tmp_path: Path) -> None:
        """Test that private variables are included when enabled."""
        code = """
_private = 42
public = 10
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner(include_private=True)
        result = scanner.scan_file(file_path)

        assert result is not None
        assert "_private" in result.variables
        assert "public" in result.variables


class TestVariableBlocks:
    """Test variable detection in different block contexts."""

    def test_module_level_variable(self, tmp_path: Path) -> None:
        """Test module-level variable block context."""
        code = """
x = 42
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert "x" in result.variables
        assert result.variables["x"].blocks == ["module"]

    def test_variable_in_if_block(self, tmp_path: Path) -> None:
        """Test variable in if block."""
        code = """
if True:
    x = 42
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert "x" in result.variables
        assert result.variables["x"].blocks == ["module", "if"]

    def test_variable_in_try_block(self, tmp_path: Path) -> None:
        """Test variable in try block."""
        code = """
try:
    x = 42
except:
    pass
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert "x" in result.variables
        assert result.variables["x"].blocks == ["module", "try"]


class TestVariableAttributeAccess:
    """Test attribute access tracking for variables."""

    def test_variable_attribute_access(self, tmp_path: Path) -> None:
        """Test tracking attribute access on variables."""
        code = """
obj = Object()
x = obj.attribute
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert "obj" in result.variables
        assert "attribute" in result.variables["obj"].attributes

    def test_variable_method_call(self, tmp_path: Path) -> None:
        """Test tracking method calls on variables."""
        code = """
obj = Object()
obj.method()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert "obj" in result.variables
        assert "method" in result.variables["obj"].attributes
