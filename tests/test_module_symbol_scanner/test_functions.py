"""Tests for function detection in module symbol scanner."""

import pytest
from pathlib import Path
from textwrap import dedent

from upcast.scanners.module_symbols import ModuleSymbolScanner


class TestBasicFunctions:
    """Test basic function detection."""

    def test_simple_function(self, tmp_path):
        """Simple function should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            def hello():
                pass
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "hello" in symbols.functions
        assert "def hello()" in symbols.functions["hello"].signature

    def test_function_with_params(self, tmp_path):
        """Function with parameters should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            def add(a, b):
                return a + b
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "add" in symbols.functions
        assert "a" in symbols.functions["add"].signature
        assert "b" in symbols.functions["add"].signature

    def test_function_with_type_hints(self, tmp_path):
        """Function with type hints should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            def multiply(x: int, y: int) -> int:
                return x * y
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "multiply" in symbols.functions

    def test_multiple_functions(self, tmp_path):
        """Multiple functions should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            def func1():
                pass
            
            def func2():
                pass
            
            def func3():
                pass
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert len(symbols.functions) == 3
        assert "func1" in symbols.functions
        assert "func2" in symbols.functions
        assert "func3" in symbols.functions


class TestFunctionDecorators:
    """Test function decorator detection."""

    def test_single_decorator(self, tmp_path):
        """Function with single decorator should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            @property
            def value(self):
                return self._value
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "value" in symbols.functions
        assert len(symbols.functions["value"].decorators) >= 1

    def test_multiple_decorators(self, tmp_path):
        """Function with multiple decorators should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            @staticmethod
            @lru_cache
            def cached_func():
                return expensive_computation()
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "cached_func" in symbols.functions
        assert len(symbols.functions["cached_func"].decorators) >= 1


class TestFunctionDocstrings:
    """Test function docstring detection."""

    def test_function_with_docstring(self, tmp_path):
        """Function with docstring should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            def documented():
                '''This is a docstring.'''
                pass
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "documented" in symbols.functions
        assert symbols.functions["documented"].docstring is not None

    def test_function_without_docstring(self, tmp_path):
        """Function without docstring should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            def undocumented():
                pass
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "undocumented" in symbols.functions


class TestFunctionBodyMD5:
    """Test function body MD5 hash calculation."""

    def test_body_md5_calculated(self, tmp_path):
        """Function body MD5 should be calculated."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            def compute():
                result = 1 + 1
                return result
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "compute" in symbols.functions
        assert symbols.functions["compute"].body_md5
        assert len(symbols.functions["compute"].body_md5) == 32  # MD5 hex length

    def test_different_bodies_different_hash(self, tmp_path):
        """Different function bodies should have different hashes."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            def func1():
                return 1
            
            def func2():
                return 2
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        hash1 = symbols.functions["func1"].body_md5
        hash2 = symbols.functions["func2"].body_md5
        assert hash1 != hash2


class TestPrivateFunctions:
    """Test private function handling."""

    def test_private_function_excluded_by_default(self, tmp_path):
        """Private functions should be excluded by default."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            def _private():
                pass
            
            def public():
                pass
        """)
        )

        scanner = ModuleSymbolScanner(include_private=False)
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "_private" not in symbols.functions
        assert "public" in symbols.functions

    def test_private_function_included_when_enabled(self, tmp_path):
        """Private functions should be included when enabled."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            def _private():
                pass
            
            def public():
                pass
        """)
        )

        scanner = ModuleSymbolScanner(include_private=True)
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "_private" in symbols.functions
        assert "public" in symbols.functions
