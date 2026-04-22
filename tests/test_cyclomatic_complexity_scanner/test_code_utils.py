"""Tests for code utilities in upcast/common/code_utils.py."""

from pathlib import Path

import pytest
from astroid import parse

from upcast.common.code_utils import (
    count_comment_lines,
    extract_function_code,
    get_code_lines,
)


class TestExtractFunctionCode:
    """Tests for extract_function_code function."""

    def test_simple_function(self):
        """Test extracting code from a simple function."""
        source = """
def simple():
    return 42
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        code = extract_function_code(func)

        assert "def simple():" in code
        assert "return 42" in code

    def test_function_with_decorator(self):
        """Test extracting code from a decorated function."""
        source = """
@decorator
def decorated():
    return True
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        code = extract_function_code(func)

        assert "def decorated():" in code
        assert "return True" in code

    def test_function_with_docstring(self):
        """Test extracting code with docstring."""
        source = '''
def with_doc():
    """This is a docstring."""
    return "value"
'''
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        code = extract_function_code(func)

        assert "def with_doc():" in code
        assert "This is a docstring" in code
        # astroid may normalize quotes
        assert "return" in code and "value" in code

    def test_multiline_function(self):
        """Test extracting code from multiline function."""
        source = """
def multiline(x, y):
    result = x + y
    if result > 0:
        return result
    return 0
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        code = extract_function_code(func)

        assert "def multiline(x, y):" in code
        assert "result = x + y" in code
        assert "if result > 0:" in code
        assert "return result" in code

    def test_falls_back_to_as_string_when_source_file_read_fails(self, monkeypatch, tmp_path):
        """Expected file read failures should still fall back to astroid rendering."""
        test_file = tmp_path / "module.py"
        test_file.write_text("def sample():\n    return 42\n")
        module = parse(test_file.read_text())
        module.file = str(test_file)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))

        def fake_read_text(self, encoding=None):
            raise OSError("cannot read source")

        monkeypatch.setattr(Path, "read_text", fake_read_text)

        code = extract_function_code(func)

        assert "def sample():" in code
        assert "return 42" in code

    def test_unexpected_read_errors_are_not_silently_swallowed(self, monkeypatch, tmp_path):
        """Unexpected read failures should surface instead of being silently ignored."""
        test_file = tmp_path / "module.py"
        test_file.write_text("def sample():\n    return 42\n")
        module = parse(test_file.read_text())
        module.file = str(test_file)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))

        def fake_read_text(self, encoding=None):
            raise RuntimeError("boom")

        monkeypatch.setattr(Path, "read_text", fake_read_text)

        with pytest.raises(RuntimeError, match="boom"):
            extract_function_code(func)


class TestCountCommentLines:
    """Tests for count_comment_lines function."""

    def test_no_comments(self):
        """Test code without comments."""
        source = """
def simple():
    return 42
"""
        count = count_comment_lines(source)
        assert count == 0

    def test_single_line_comment(self):
        """Test single line comment."""
        source = """
# This is a comment
def simple():
    return 42
"""
        count = count_comment_lines(source)
        assert count == 1

    def test_multiple_comments(self):
        """Test multiple comments."""
        source = """
# Comment 1
def simple():
    # Comment 2
    x = 10  # Inline comment
    # Comment 3
    return x
"""
        count = count_comment_lines(source)
        assert count == 4  # All 4 comment lines

    def test_hash_in_string_not_counted(self):
        """Test that # in strings is not counted as comment."""
        source = """
def func():
    msg = "This is #not a comment"
    code = "# Also not a comment"
    return msg
"""
        count = count_comment_lines(source)
        assert count == 0

    def test_multiline_string_not_counted(self):
        """Test that multiline strings with # are not counted."""
        source = '''
def func():
    text = """
    # This looks like a comment
    But it's inside a string
    """
    return text
'''
        count = count_comment_lines(source)
        assert count == 0

    def test_docstring_not_counted(self):
        """Test that docstrings are not counted as comments."""
        source = '''
def func():
    """This is a docstring, not a comment."""
    return 42
'''
        count = count_comment_lines(source)
        assert count == 0

    def test_mixed_comments_and_strings(self):
        """Test mixing comments and strings with #."""
        source = """
# Real comment
def func():
    msg = "This has a # in it"  # Real comment
    # Another real comment
    return msg
"""
        count = count_comment_lines(source)
        assert count == 3


class TestGetCodeLines:
    """Tests for get_code_lines function."""

    def test_single_line_function(self):
        """Test counting lines for single-line function."""
        source = """
def simple(): return 42
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        lines = get_code_lines(func)

        assert lines == 1

    def test_multiline_function(self):
        """Test counting lines for multiline function."""
        source = """
def multiline():
    x = 10
    y = 20
    return x + y
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        lines = get_code_lines(func)

        assert lines == 4  # def line + 3 body lines

    def test_function_with_decorator(self):
        """Test counting lines includes decorator."""
        source = """
@decorator
def decorated():
    return True
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        lines = get_code_lines(func)

        # Decorators are part of the function node
        assert lines >= 2

    def test_function_with_empty_lines(self):
        """Test that empty lines within function are counted."""
        source = """
def with_empty():
    x = 10

    y = 20

    return x + y
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        lines = get_code_lines(func)

        # Should count all lines from def to last return
        assert lines == 6
