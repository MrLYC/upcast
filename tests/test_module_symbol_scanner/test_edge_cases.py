"""Tests for edge cases in module symbol scanner."""

from pathlib import Path

import pytest

from upcast.scanners.module_symbols import ModuleSymbolScanner


class TestInvalidSyntax:
    """Test handling of invalid syntax."""

    def test_invalid_python_syntax(self, tmp_path: Path) -> None:
        """Test that invalid Python syntax is handled gracefully."""
        code = """
def incomplete_function(
    # Missing closing paren and colon
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        # Should return None for unparseable files
        assert result is None


class TestEmptyFiles:
    """Test handling of empty files."""

    def test_empty_file(self, tmp_path: Path) -> None:
        """Test scanning an empty file."""
        file_path = tmp_path / "empty.py"
        file_path.write_text("")

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert len(result.imported_modules) == 0
        assert len(result.imported_symbols) == 0
        assert len(result.variables) == 0
        assert len(result.functions) == 0
        assert len(result.classes) == 0

    def test_whitespace_only_file(self, tmp_path: Path) -> None:
        """Test scanning a file with only whitespace."""
        file_path = tmp_path / "whitespace.py"
        file_path.write_text("   \n\n   \n")

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert len(result.imported_modules) == 0
        assert len(result.functions) == 0


class TestNestedStructures:
    """Test handling of nested structures."""

    def test_nested_classes(self, tmp_path: Path) -> None:
        """Test detection of nested classes (only outer class detected at module level)."""
        code = """
class Outer:
    class Inner:
        pass
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert "Outer" in result.classes
        # Inner classes are not extracted as module-level symbols
        assert "Inner" not in result.classes

    def test_nested_functions(self, tmp_path: Path) -> None:
        """Test detection of nested functions (only outer function detected)."""
        code = """
def outer():
    def inner():
        pass
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert "outer" in result.functions
        # Nested functions are not extracted as module-level symbols
        assert "inner" not in result.functions


class TestSpecialCases:
    """Test special cases."""

    def test_module_with_only_docstring(self, tmp_path: Path) -> None:
        """Test module with only a docstring."""
        code = '''"""Module docstring."""'''
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert len(result.functions) == 0
        assert len(result.classes) == 0

    def test_module_with_only_comments(self, tmp_path: Path) -> None:
        """Test module with only comments."""
        code = """# This is a comment
# Another comment
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert len(result.functions) == 0
        assert len(result.classes) == 0

    def test_module_with_main_guard(self, tmp_path: Path) -> None:
        """Test module with if __name__ == '__main__' guard."""
        code = """
def main():
    pass

if __name__ == '__main__':
    main()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert "main" in result.functions


class TestComplexDecorators:
    """Test complex decorator patterns."""

    def test_decorator_with_complex_args(self, tmp_path: Path) -> None:
        """Test decorator with complex arguments."""
        code = """
@decorator(arg1=1, arg2="value", arg3=[1, 2, 3])
def func():
    pass
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert "func" in result.functions
        assert len(result.functions["func"].decorators) == 1

    def test_chained_decorators(self, tmp_path: Path) -> None:
        """Test multiple chained decorators."""
        code = """
@decorator1
@decorator2
@decorator3
def func():
    pass
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert "func" in result.functions
        assert len(result.functions["func"].decorators) == 3


class TestComplexInheritance:
    """Test complex inheritance patterns."""

    def test_multiple_base_classes(self, tmp_path: Path) -> None:
        """Test class with multiple base classes."""
        code = """
class Base1:
    pass

class Base2:
    pass

class Child(Base1, Base2):
    pass
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert "Child" in result.classes
        assert len(result.classes["Child"].bases) == 2

    def test_class_with_imported_base(self, tmp_path: Path) -> None:
        """Test class inheriting from imported base."""
        code = """
from django.db import models

class MyModel(models.Model):
    pass
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        scanner = ModuleSymbolScanner()
        result = scanner.scan_file(file_path)

        assert result is not None
        assert "MyModel" in result.classes
        # Base should be resolved to full module path
        assert "django.db.models.Model" in result.classes["MyModel"].bases


class TestModulePath:
    """Test module path resolution."""

    def test_init_file_module_path(self, tmp_path: Path) -> None:
        """Test module path for __init__.py file."""
        package_dir = tmp_path / "mypackage"
        package_dir.mkdir()
        init_file = package_dir / "__init__.py"
        init_file.write_text("x = 1")

        scanner = ModuleSymbolScanner()
        scanner.base_path = tmp_path
        result = scanner.scan_file(init_file)

        assert result is not None
        assert "x" in result.variables
        # Module path should be the package path
        assert result.variables["x"].module_path == "mypackage"

    def test_regular_file_module_path(self, tmp_path: Path) -> None:
        """Test module path for regular Python file."""
        package_dir = tmp_path / "mypackage"
        package_dir.mkdir()
        module_file = package_dir / "mymodule.py"
        module_file.write_text("x = 1")

        scanner = ModuleSymbolScanner()
        scanner.base_path = tmp_path
        result = scanner.scan_file(module_file)

        assert result is not None
        assert "x" in result.variables
        assert result.variables["x"].module_path == "mypackage.mymodule"
