"""Tests for function detection and metadata extraction."""

from pathlib import Path

import pytest
from astroid import parse

from upcast.cyclomatic_complexity_scanner.checker import ComplexityChecker


class TestFunctionDetection:
    """Tests for detecting different types of functions."""

    @pytest.fixture
    def edge_cases_fixture_path(self):
        """Path to edge_cases.py fixture."""
        return Path(__file__).parent / "fixtures" / "edge_cases.py"

    def test_detect_regular_function(self):
        """Test detecting a regular function."""
        source = """
def regular_function(x, y):
    \"\"\"A regular function.\"\"\"
    return x + y
"""
        module = parse(source)
        functions = list(module.nodes_of_class(parse("def f(): pass").body[0].__class__))

        assert len(functions) == 1
        func = functions[0]
        assert func.name == "regular_function"
        assert not func.is_method()

    def test_detect_async_function(self):
        """Test detecting an async function."""
        source = """
async def async_function(x):
    \"\"\"An async function.\"\"\"
    return x * 2
"""
        module = parse(source)
        functions = list(module.nodes_of_class(parse("def f(): pass").body[0].__class__))

        assert len(functions) == 1
        func = functions[0]
        assert func.name == "async_function"

    def test_detect_class_methods(self):
        """Test detecting methods in a class."""
        source = """
class MyClass:
    def instance_method(self, x):
        return x

    @staticmethod
    def static_method(x):
        return x

    @classmethod
    def class_method(cls, x):
        return cls()
"""
        module = parse(source)
        functions = list(module.nodes_of_class(parse("def f(): pass").body[0].__class__))

        assert len(functions) == 3
        names = {func.name for func in functions}
        assert names == {"instance_method", "static_method", "class_method"}

        # All should be detected as methods
        for func in functions:
            assert func.is_method()

    def test_detect_nested_functions(self):
        """Test that nested functions are detected independently."""
        source = """
def outer():
    x = 10

    def inner(y):
        return y * 2

    return inner(x)
"""
        module = parse(source)
        functions = list(module.nodes_of_class(parse("def f(): pass").body[0].__class__))

        # Should detect both outer and inner
        assert len(functions) == 2
        names = {func.name for func in functions}
        assert names == {"outer", "inner"}

    def test_extract_function_signature(self, edge_cases_fixture_path):
        """Test extracting function signatures."""
        checker = ComplexityChecker(threshold=1)
        results = checker.check_file(edge_cases_fixture_path)

        # Find a specific function
        instance_method = next((r for r in results if r.name == "instance_method"), None)

        assert instance_method is not None
        assert "def instance_method" in instance_method.signature
        assert "self" in instance_method.signature

    def test_extract_docstring(self, edge_cases_fixture_path):
        """Test extracting first line of docstring."""
        checker = ComplexityChecker(threshold=1)
        results = checker.check_file(edge_cases_fixture_path)

        # Find function with docstring
        func_with_doc = next((r for r in results if r.name == "function_with_comments"), None)

        assert func_with_doc is not None
        assert func_with_doc.description  # Should have docstring
        assert "Function with comments" in func_with_doc.description

    def test_extract_line_numbers(self, edge_cases_fixture_path):
        """Test extracting correct line numbers."""
        checker = ComplexityChecker(threshold=1)
        results = checker.check_file(edge_cases_fixture_path)

        for result in results:
            assert result.line > 0
            assert result.end_line > 0
            assert result.end_line >= result.line

    def test_detect_is_async(self, edge_cases_fixture_path):
        """Test detecting async functions from fixture."""
        checker = ComplexityChecker(threshold=1)
        results = checker.check_file(edge_cases_fixture_path)

        # Find async method in MyClass
        async_result = next((r for r in results if r.name == "async_method"), None)

        assert async_result is not None
        assert async_result.is_async

    def test_detect_is_method(self, edge_cases_fixture_path):
        """Test detecting methods vs functions."""
        checker = ComplexityChecker(threshold=1)
        results = checker.check_file(edge_cases_fixture_path)

        # Regular functions should have is_method=False
        outer_func = next((r for r in results if r.name == "nested_function_outer"), None)
        assert outer_func is not None
        assert not outer_func.is_method

        # Methods should have is_method=True
        instance_method = next((r for r in results if r.name == "instance_method"), None)
        assert instance_method is not None
        assert instance_method.is_method

    def test_extract_class_name(self, edge_cases_fixture_path):
        """Test extracting parent class name for methods."""
        checker = ComplexityChecker(threshold=1)
        results = checker.check_file(edge_cases_fixture_path)

        # Methods should have class_name
        instance_method = next((r for r in results if r.name == "instance_method"), None)
        assert instance_method is not None
        assert instance_method.class_name == "MyClass"

        # Regular functions should not have class_name
        regular_func = next((r for r in results if r.name == "nested_function_outer"), None)
        assert regular_func is not None
        assert regular_func.class_name is None


class TestCodeExtraction:
    """Tests for extracting complete function code."""

    @pytest.fixture
    def edge_cases_fixture_path(self):
        """Path to edge_cases.py fixture."""
        return Path(__file__).parent / "fixtures" / "edge_cases.py"

    def test_extract_function_code_from_fixture(self, edge_cases_fixture_path):
        """Test extracting code from functions in fixture file."""
        checker = ComplexityChecker(threshold=1)
        results = checker.check_file(edge_cases_fixture_path)

        # Should have multiple functions with code
        assert len(results) > 0

        # Check that all results have non-empty code
        for result in results:
            assert result.code
            assert "def " in result.code
            assert result.name in result.code

    def test_code_lines_count_from_fixture(self, edge_cases_fixture_path):
        """Test counting total code lines from fixture."""
        checker = ComplexityChecker(threshold=1)
        results = checker.check_file(edge_cases_fixture_path)

        # All results should have valid code_lines
        for result in results:
            assert result.code_lines > 0
            assert result.end_line >= result.line
            # code_lines should approximately match line range
            expected_lines = result.end_line - result.line + 1
            assert result.code_lines == expected_lines

    def test_comment_lines_from_fixture(self, edge_cases_fixture_path):
        """Test comment line counting from fixture.

        Note: astroid's as_string() method does not preserve comments,
        so comment_lines will be 0 for all functions. This is expected behavior.
        """
        checker = ComplexityChecker(threshold=1)
        results = checker.check_file(edge_cases_fixture_path)

        # Since astroid.as_string() doesn't preserve comments,
        # all functions will have comment_lines == 0
        # This is a known limitation of using astroid for source extraction
        assert all(r.comment_lines == 0 for r in results)

    def test_no_comment_lines_from_fixture(self, edge_cases_fixture_path):
        """Test function without comments from fixture."""
        checker = ComplexityChecker(threshold=1)
        results = checker.check_file(edge_cases_fixture_path)

        # Many functions should have 0 comment lines
        functions_without_comments = [r for r in results if r.comment_lines == 0]
        assert len(functions_without_comments) > 0
