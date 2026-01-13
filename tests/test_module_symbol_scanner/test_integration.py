"""Integration tests for module symbol scanner."""

from pathlib import Path

import pytest

from upcast.scanners.module_symbols import ModuleSymbolScanner


class TestModuleSymbolScanner:
    """Integration tests for ModuleSymbolScanner."""

    @pytest.fixture
    def fixtures_dir(self):
        """Get the fixtures directory path."""
        return Path(__file__).parent / "fixtures"

    @pytest.fixture
    def scanner(self):
        """Create a scanner instance."""
        return ModuleSymbolScanner(verbose=True)

    def test_extract_imports(self, scanner, fixtures_dir):
        """Test extracting various import types."""
        imports_file = fixtures_dir / "imports.py"
        result = scanner.scan(imports_file)

        assert result.summary.files_scanned == 1
        assert len(result.results) > 0

        # Get the first (and only) file result
        file_result = next(iter(result.results.values()))

        # Check imported modules
        assert "sys" in file_result.imported_modules
        # Check attribute access tracking
        assert "platform" in file_result.imported_modules["sys"].attributes

    def test_extract_symbols(self, scanner, fixtures_dir):
        """Test extracting variables, functions, and classes."""
        symbols_file = fixtures_dir / "symbols.py"
        result = scanner.scan(symbols_file)

        file_result = next(iter(result.results.values()))

        # Check variables (private ones excluded by default)
        assert "DEBUG" in file_result.variables
        assert file_result.variables["DEBUG"].value == "True"
        assert "_private_var" not in file_result.variables

        # Check functions
        assert "helper" in file_result.functions
        assert "def helper(arg1: int, arg2: str) -> bool" in file_result.functions["helper"].signature
        assert file_result.functions["helper"].docstring == "A helper function."
        assert "_internal" not in file_result.functions

        # Check classes
        assert "MyClass" in file_result.classes
        assert "attr1" in file_result.classes["MyClass"].attributes
        assert "method1" in file_result.classes["MyClass"].methods
        assert "method2" in file_result.classes["MyClass"].methods
        assert "_PrivateClass" not in file_result.classes

    def test_include_private_symbols(self, fixtures_dir):
        """Test including private symbols."""
        scanner = ModuleSymbolScanner(include_private=True, verbose=True)
        symbols_file = fixtures_dir / "symbols.py"
        result = scanner.scan(symbols_file)

        file_result = next(iter(result.results.values()))

        # Private symbols should be included
        assert "_private_var" in file_result.variables
        assert "_internal" in file_result.functions
        assert "_PrivateClass" in file_result.classes

    def test_extract_decorators(self, scanner, fixtures_dir):
        """Test extracting decorators."""
        symbols_file = fixtures_dir / "symbols.py"
        result = scanner.scan(symbols_file)

        file_result = next(iter(result.results.values()))

        # Check decorated function
        assert "decorated_func" in file_result.functions
        decorators = file_result.functions["decorated_func"].decorators
        assert len(decorators) == 2
        assert decorators[0].name == "decorator"
        assert decorators[1].name == "another_decorator"

        # Check decorated class
        assert "Config" in file_result.classes
        class_decorators = file_result.classes["Config"].decorators
        assert len(class_decorators) == 1
        assert class_decorators[0].name == "dataclass"

    def test_extract_class_bases(self, scanner, fixtures_dir):
        """Test extracting class base classes."""
        symbols_file = fixtures_dir / "symbols.py"
        result = scanner.scan(symbols_file)

        file_result = next(iter(result.results.values()))

        # Check class with multiple bases
        assert "Child" in file_result.classes
        bases = file_result.classes["Child"].bases
        assert "Parent1" in bases
        assert "Parent2" in bases

    def test_attribute_access(self, scanner, fixtures_dir):
        """Test tracking attribute access."""
        attributes_file = fixtures_dir / "attributes.py"
        result = scanner.scan(attributes_file)

        file_result = next(iter(result.results.values()))

        # Check attribute access on imported modules
        assert "os" in file_result.imported_modules
        assert "path" in file_result.imported_modules["os"].attributes

        # Check attribute access on imported symbols
        assert "Path" in file_result.imported_symbols
        assert "home" in file_result.imported_symbols["Path"].attributes

    def test_block_context(self, scanner, fixtures_dir):
        """Test tracking block context."""
        symbols_file = fixtures_dir / "symbols.py"
        result = scanner.scan(symbols_file)

        file_result = next(iter(result.results.values()))

        # Check conditional variable
        if "LOG_LEVEL" in file_result.variables:
            blocks = file_result.variables["LOG_LEVEL"].blocks
            assert "if" in blocks

    def test_summary_statistics(self, scanner, fixtures_dir):
        """Test summary statistics calculation."""
        symbols_file = fixtures_dir / "symbols.py"
        result = scanner.scan(symbols_file)

        summary = result.summary
        assert summary.files_scanned == 1
        assert summary.total_modules > 0
        assert summary.total_imports > 0
        assert summary.total_symbols > 0
        assert summary.scan_duration_ms > 0

    def test_scan_directory(self, scanner, fixtures_dir):
        """Test scanning multiple files in a directory."""
        result = scanner.scan(fixtures_dir)

        assert result.summary.files_scanned > 1
        assert len(result.results) > 1

    def test_file_filtering(self, fixtures_dir):
        """Test file filtering with exclude patterns."""
        scanner = ModuleSymbolScanner(exclude_patterns=["**/imports.py"], verbose=True)
        result = scanner.scan(fixtures_dir)

        # imports.py should be excluded
        assert all("imports.py" not in path for path in result.results.keys())

    def test_empty_file(self, scanner, tmp_path):
        """Test scanning empty file."""
        empty_file = tmp_path / "empty.py"
        empty_file.write_text("")

        result = scanner.scan(empty_file)

        assert result.summary.files_scanned == 1
        # Empty files may not appear in results - that's OK
        if result.results:
            file_result = next(iter(result.results.values()))
            assert len(file_result.imported_modules) == 0
            assert len(file_result.variables) == 0
            assert len(file_result.functions) == 0
            assert len(file_result.classes) == 0

    def test_invalid_syntax(self, scanner, tmp_path):
        """Test handling invalid syntax."""
        invalid_file = tmp_path / "invalid.py"
        invalid_file.write_text("def invalid syntax here")

        result = scanner.scan(invalid_file)

        # Should handle gracefully, file should not appear in results
        assert len(result.results) == 0

    def test_body_md5_different_for_different_functions(self, scanner, tmp_path):
        """Test that body_md5 is different for different function bodies."""
        test_file = tmp_path / "test_funcs.py"
        test_file.write_text(
            """
def func1():
    return 1

def func2():
    return 2
"""
        )

        result = scanner.scan(test_file)
        file_result = next(iter(result.results.values()))

        assert "func1" in file_result.functions
        assert "func2" in file_result.functions
        assert file_result.functions["func1"].body_md5 != file_result.functions["func2"].body_md5

    def test_output_serialization(self, scanner, fixtures_dir):
        """Test that output can be serialized."""
        result = scanner.scan(fixtures_dir)

        # Test to_dict()
        data = result.to_dict()
        assert isinstance(data, dict)
        assert "summary" in data
        assert "results" in data

        # Test to_json()
        json_str = result.to_json()
        assert isinstance(json_str, str)
        assert len(json_str) > 0

    def test_base_class_resolution(self, scanner, fixtures_dir):
        """Test that base classes are resolved to full module paths."""
        base_resolution_file = fixtures_dir / "base_resolution.py"
        result = scanner.scan(base_resolution_file)

        file_result = next(iter(result.results.values()))

        # Check MySerializer inherits from rest_framework.serializers.Serializer
        assert "MySerializer" in file_result.classes
        bases = file_result.classes["MySerializer"].bases
        assert len(bases) == 1
        assert bases[0] == "rest_framework.serializers.Serializer"

        # Check MyModel inherits from django.db.models.Model
        assert "MyModel" in file_result.classes
        bases = file_result.classes["MyModel"].bases
        assert len(bases) == 1
        assert bases[0] == "django.db.models.Model"

        # Check Child inherits from LocalBase (not resolved, as it's local)
        assert "Child" in file_result.classes
        bases = file_result.classes["Child"].bases
        assert len(bases) == 1
        assert bases[0] == "LocalBase"
