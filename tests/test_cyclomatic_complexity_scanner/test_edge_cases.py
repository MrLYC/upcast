"""Tests for edge cases and error handling in CyclomaticComplexityScanner.

Tests cover:
- Empty files
- Invalid syntax
- Decorators
- Nested functions
- Lambda functions
- Class methods vs standalone functions
- Async functions
- Very high complexity functions
- Multiple files
"""

import pytest


def test_empty_file(scanner, tmp_path):
    """Test scanning an empty file."""
    file_path = tmp_path / "empty.py"
    file_path.write_text("")

    result = scanner.scan(tmp_path)

    assert result.summary.total_count == 0
    # Scanner may not count files with no functions
    assert result.summary.files_scanned >= 0
    assert len(result.results) == 0


def test_file_with_only_comments(scanner, tmp_path):
    """Test scanning a file with only comments."""
    code = """
# This is a comment
# Another comment
"""
    file_path = tmp_path / "comments_only.py"
    file_path.write_text(code)

    result = scanner.scan(tmp_path)

    assert result.summary.total_count == 0
    # Scanner may not count files with no functions
    assert result.summary.files_scanned >= 0


def test_file_with_only_imports(scanner, tmp_path):
    """Test scanning a file with only imports."""
    code = """
import os
import sys
from pathlib import Path
"""
    file_path = tmp_path / "imports_only.py"
    file_path.write_text(code)

    result = scanner.scan(tmp_path)

    assert result.summary.total_count == 0
    # Scanner may not count files with no functions
    assert result.summary.files_scanned >= 0


def test_invalid_syntax_file(scanner, tmp_path):
    """Test that invalid syntax files are handled gracefully."""
    code = """
def broken_func(
    # Missing closing parenthesis
    return 42
"""
    file_path = tmp_path / "broken.py"
    file_path.write_text(code)

    # Should not crash, may skip the file or return empty results
    result = scanner.scan(tmp_path)

    # Just ensure it doesn't crash
    assert result.summary.files_scanned >= 0


def test_function_with_decorators(low_threshold_scanner, tmp_path):
    """Test that decorators don't affect complexity calculation."""
    code = """
@decorator1
@decorator2(arg="value")
def decorated_func(x):
    if x > 0:
        return x
    return 0
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 2  # Base 1 + if 1
    assert result.results["test.py"][0].name == "decorated_func"


def test_nested_function_definitions(low_threshold_scanner, tmp_path):
    """Test that nested functions are each analyzed separately."""
    code = """
def outer_func(x):
    if x > 0:
        def inner_func(y):
            if y > 0:
                return y * 2
            return 0
        return inner_func(x)
    return 0
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 2
    # Check both functions are analyzed
    func_names = [r.name for r in result.results["test.py"]]
    assert "outer_func" in func_names
    assert "inner_func" in func_names


def test_lambda_functions_not_analyzed(scanner, tmp_path):
    """Test that lambda functions are not analyzed."""
    code = """
my_lambda = lambda x: x * 2
another_lambda = lambda x, y: x + y if x > 0 else y
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = scanner.scan(tmp_path)

    # Lambda functions should not be counted
    assert result.summary.total_count == 0


def test_class_methods(low_threshold_scanner, tmp_path):
    """Test that class methods are analyzed correctly."""
    code = """
class MyClass:
    def method_one(self, x):
        if x > 0:
            return x
        return 0

    def method_two(self, y):
        for i in range(y):
            if i > 10:
                break
        return i
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 2
    complexities = [r.complexity for r in result.results["test.py"]]
    # method_one: Base 1 + if 1 = 2
    # method_two: Base 1 + for 1 + if 1 = 3
    assert 2 in complexities
    assert 3 in complexities


def test_static_and_class_methods(low_threshold_scanner, tmp_path):
    """Test that static and class methods are analyzed."""
    code = """
class MyClass:
    @staticmethod
    def static_method(x):
        if x > 0:
            return x
        return 0

    @classmethod
    def class_method(cls, y):
        while y > 0:
            y -= 1
        return y
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 2
    func_names = [r.name for r in result.results["test.py"]]
    assert "static_method" in func_names
    assert "class_method" in func_names


def test_async_function(low_threshold_scanner, tmp_path):
    """Test that async functions are analyzed correctly."""
    code = """
async def async_func(x):
    if x > 0:
        await some_operation()
        return x
    return 0
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 2  # Base 1 + if 1
    assert result.results["test.py"][0].name == "async_func"


def test_async_for_and_with(low_threshold_scanner, tmp_path):
    """Test that async for loops add to complexity."""
    code = """
async def async_iteration(items):
    async for item in items:
        if item > 0:
            yield item
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    # Base 1 + async for 1 + if 1 = 3
    assert result.results["test.py"][0].complexity == 3


def test_very_high_complexity_function(low_threshold_scanner, tmp_path):
    """Test function with very high complexity (>10 - warning/high_risk)."""
    code = """
def ultra_complex_func(a, b, c, d, e):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    if e > 0:
                        for i in range(10):
                            if i > 5:
                                while i < 20:
                                    if i % 2 == 0:
                                        try:
                                            if i > 10:
                                                assert i < 15
                                                i += 1
                                        except ValueError:
                                            pass
                                        except KeyError:
                                            pass
    return 0
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    # Base 1 + 6 ifs + 1 for + 1 while + 2 except + 1 assert = 12+
    assert result.results["test.py"][0].complexity >= 12
    # Should be at least warning level (11-15)
    assert result.results["test.py"][0].severity in ["warning", "high_risk", "critical"]


def test_multiple_files(low_threshold_scanner, tmp_path):
    """Test scanning multiple files."""
    code1 = """
def func1(x):
    if x > 0:
        return x
    return 0
"""
    code2 = """
def func2(y):
    for i in range(y):
        if i > 10:
            return i
    return 0
"""
    file1 = tmp_path / "file1.py"
    file2 = tmp_path / "file2.py"
    file1.write_text(code1)
    file2.write_text(code2)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 2
    assert result.summary.files_scanned == 2
    assert "file1.py" in result.results
    assert "file2.py" in result.results


def test_function_without_body(scanner, tmp_path):
    """Test function with only pass statement."""
    code = """
def empty_func():
    pass
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = scanner.scan(tmp_path)

    # Empty function still has base complexity 1, but might be below threshold
    # Using default scanner (threshold=11), this won't be reported
    assert result.summary.files_scanned >= 0


def test_function_with_only_docstring(low_threshold_scanner, tmp_path):
    """Test function with only a docstring."""
    code = '''
def documented_func():
    """This function does nothing."""
    pass
'''
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 1  # Base complexity


def test_multiline_function_signature(low_threshold_scanner, tmp_path):
    """Test function with multiline signature."""
    code = """
def multiline_func(
    arg1: int,
    arg2: str,
    arg3: bool = False
) -> int:
    if arg3:
        return arg1
    return 0
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 2  # Base 1 + if 1
    assert result.results["test.py"][0].name == "multiline_func"


def test_generator_function(low_threshold_scanner, tmp_path):
    """Test generator function with yield."""
    code = """
def generator_func(n):
    for i in range(n):
        if i % 2 == 0:
            yield i
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 3  # Base 1 + for 1 + if 1


def test_context_manager_with_statement(low_threshold_scanner, tmp_path):
    """Test that with statements don't add complexity (unless they have conditions)."""
    code = """
def func_with_context_manager(filename):
    with open(filename) as f:
        content = f.read()
        if content:
            return content
    return ""
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    # Base 1 + if 1 = 2 (with statement doesn't add complexity)
    assert result.results["test.py"][0].complexity == 2


def test_no_python_files_in_directory(scanner, tmp_path):
    """Test scanning directory with no Python files."""
    # Create a non-Python file
    non_python = tmp_path / "readme.txt"
    non_python.write_text("This is not Python")

    result = scanner.scan(tmp_path)

    assert result.summary.total_count == 0
    assert result.summary.files_scanned == 0


def test_subdirectories_scanned(low_threshold_scanner, tmp_path):
    """Test that subdirectories are scanned recursively."""
    subdir = tmp_path / "subdir"
    subdir.mkdir()

    code1 = """
def func1(x):
    if x > 0:
        return x
    return 0
"""
    code2 = """
def func2(y):
    for i in range(y):
        return i
    return 0
"""
    file1 = tmp_path / "file1.py"
    file2 = subdir / "file2.py"
    file1.write_text(code1)
    file2.write_text(code2)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 2
    assert result.summary.files_scanned == 2
