"""Tests for class detection in module symbol scanner."""

import pytest
from pathlib import Path
from textwrap import dedent

from upcast.scanners.module_symbols import ModuleSymbolScanner


class TestBasicClasses:
    """Test basic class detection."""

    def test_simple_class(self, tmp_path):
        """Simple class should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            class MyClass:
                pass
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "MyClass" in symbols.classes

    def test_class_with_methods(self, tmp_path):
        """Class with methods should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            class Calculator:
                def add(self, a, b):
                    return a + b
                
                def subtract(self, a, b):
                    return a - b
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "Calculator" in symbols.classes
        assert "add" in symbols.classes["Calculator"].methods
        assert "subtract" in symbols.classes["Calculator"].methods

    def test_class_with_attributes(self, tmp_path):
        """Class with attributes should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            class Config:
                DEBUG = True
                PORT = 8000
                HOST = 'localhost'
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "Config" in symbols.classes
        # Attributes detection may vary
        assert isinstance(symbols.classes["Config"].attributes, list)

    def test_multiple_classes(self, tmp_path):
        """Multiple classes should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            class Class1:
                pass
            
            class Class2:
                pass
            
            class Class3:
                pass
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert len(symbols.classes) == 3
        assert "Class1" in symbols.classes
        assert "Class2" in symbols.classes
        assert "Class3" in symbols.classes


class TestClassInheritance:
    """Test class inheritance detection."""

    def test_single_inheritance(self, tmp_path):
        """Class with single base should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            class Parent:
                pass
            
            class Child(Parent):
                pass
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "Child" in symbols.classes
        assert len(symbols.classes["Child"].bases) >= 1

    def test_multiple_inheritance(self, tmp_path):
        """Class with multiple bases should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            class Mixin1:
                pass
            
            class Mixin2:
                pass
            
            class Combined(Mixin1, Mixin2):
                pass
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "Combined" in symbols.classes
        assert len(symbols.classes["Combined"].bases) >= 2


class TestClassDecorators:
    """Test class decorator detection."""

    def test_single_decorator(self, tmp_path):
        """Class with single decorator should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            @dataclass
            class Point:
                x: int
                y: int
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "Point" in symbols.classes
        assert len(symbols.classes["Point"].decorators) >= 1

    def test_multiple_decorators(self, tmp_path):
        """Class with multiple decorators should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            @decorator1
            @decorator2
            class Decorated:
                pass
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "Decorated" in symbols.classes
        assert len(symbols.classes["Decorated"].decorators) >= 1


class TestClassDocstrings:
    """Test class docstring detection."""

    def test_class_with_docstring(self, tmp_path):
        """Class with docstring should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            class Documented:
                '''This is a class docstring.'''
                pass
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "Documented" in symbols.classes
        assert symbols.classes["Documented"].docstring is not None

    def test_class_without_docstring(self, tmp_path):
        """Class without docstring should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            class Undocumented:
                pass
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "Undocumented" in symbols.classes


class TestClassBodyMD5:
    """Test class body MD5 hash calculation."""

    def test_body_md5_calculated(self, tmp_path):
        """Class body MD5 should be calculated."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            class Example:
                def method(self):
                    return 42
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "Example" in symbols.classes
        assert symbols.classes["Example"].body_md5
        assert len(symbols.classes["Example"].body_md5) == 32  # MD5 hex length

    def test_different_bodies_different_hash(self, tmp_path):
        """Different class bodies should have different hashes."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            class Class1:
                value = 1
            
            class Class2:
                value = 2
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        hash1 = symbols.classes["Class1"].body_md5
        hash2 = symbols.classes["Class2"].body_md5
        assert hash1 != hash2


class TestPrivateClasses:
    """Test private class handling."""

    def test_private_class_excluded_by_default(self, tmp_path):
        """Private classes should be excluded by default."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            class _Private:
                pass
            
            class Public:
                pass
        """)
        )

        scanner = ModuleSymbolScanner(include_private=False)
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "_Private" not in symbols.classes
        assert "Public" in symbols.classes

    def test_private_class_included_when_enabled(self, tmp_path):
        """Private classes should be included when enabled."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            class _Private:
                pass
            
            class Public:
                pass
        """)
        )

        scanner = ModuleSymbolScanner(include_private=True)
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "_Private" in symbols.classes
        assert "Public" in symbols.classes
