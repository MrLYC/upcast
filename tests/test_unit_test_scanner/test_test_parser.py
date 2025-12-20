"""Tests for test_parser module."""

from astroid import MANAGER, nodes

from upcast.unit_test_scanner.test_parser import (
    calculate_body_md5,
    count_assertions,
    extract_imports,
    normalize_code,
    parse_test_function,
    resolve_targets,
)


class TestNormalizeCode:
    """Test code normalization."""

    def test_remove_comments(self):
        """Test comment removal."""
        code = """
def test_something():
    # This is a comment
    x = 1  # Inline comment
    assert x == 1
"""
        normalized = normalize_code(code)
        assert "#" not in normalized
        assert "x = 1" in normalized
        assert "assert x == 1" in normalized

    def test_remove_empty_lines(self):
        """Test empty line removal."""
        code = """
def test_something():

    x = 1

    assert x == 1

"""
        normalized = normalize_code(code)
        lines = normalized.split("\n")
        assert "" not in lines

    def test_strip_whitespace(self):
        """Test whitespace stripping."""
        code = "    def test():    \n        x = 1    \n"
        normalized = normalize_code(code)
        assert not any(line.endswith(" ") for line in normalized.split("\n"))


class TestCountAssertions:
    """Test assertion counting."""

    def test_count_pytest_asserts(self):
        """Test counting pytest assert statements."""
        code = """
def test_something():
    assert 1 == 1
    assert True
    assert 2 + 2 == 4
"""
        module = MANAGER.ast_from_string(code)
        func = next(module.nodes_of_class(nodes.FunctionDef))
        count = count_assertions(func)
        assert count == 3

    def test_count_unittest_asserts(self):
        """Test counting unittest assert methods."""
        code = """
class TestSomething:
    def test_method(self):
        self.assertEqual(1, 1)
        self.assertTrue(True)
        self.assertFalse(False)
"""
        module = MANAGER.ast_from_string(code)
        func = next(module.nodes_of_class(nodes.FunctionDef))
        count = count_assertions(func)
        assert count == 3

    def test_count_pytest_raises(self):
        """Test counting pytest.raises."""
        code = """
import pytest

def test_exception():
    with pytest.raises(ValueError):
        raise ValueError()
"""
        module = MANAGER.ast_from_string(code)
        func = next(module.nodes_of_class(nodes.FunctionDef))
        count = count_assertions(func)
        assert count == 1

    def test_mixed_assertions(self):
        """Test counting mixed assertion styles."""
        code = """
import pytest

def test_mixed():
    assert 1 == 1
    with pytest.raises(ValueError):
        raise ValueError()
    assert True
"""
        module = MANAGER.ast_from_string(code)
        func = next(module.nodes_of_class(nodes.FunctionDef))
        count = count_assertions(func)
        assert count == 3


class TestExtractImports:
    """Test import extraction."""

    def test_simple_import(self):
        """Test simple import extraction."""
        code = """
import app.math_utils
from app import validators
"""
        module = MANAGER.ast_from_string(code)
        imports = extract_imports(module)
        assert "app.math_utils" in imports.values()
        assert "app.validators" in imports.values()

    def test_import_with_alias(self):
        """Test import with alias."""
        code = """
import app.math_utils as math
from app import validators as val
"""
        module = MANAGER.ast_from_string(code)
        imports = extract_imports(module)
        assert "math" in imports
        assert imports["math"] == "app.math_utils"
        assert "val" in imports
        assert imports["val"] == "app.validators"

    def test_from_import(self):
        """Test from import extraction."""
        code = """
from app.math_utils import add, is_even
"""
        module = MANAGER.ast_from_string(code)
        imports = extract_imports(module)
        assert "add" in imports
        assert imports["add"] == "app.math_utils.add"
        assert "is_even" in imports
        assert imports["is_even"] == "app.math_utils.is_even"

    def test_wildcard_import(self):
        """Test wildcard import."""
        code = """
from app.math_utils import *
"""
        module = MANAGER.ast_from_string(code)
        imports = extract_imports(module)
        assert "*from:app.math_utils" in imports


class TestResolveTargets:
    """Test target resolution."""

    def test_resolve_single_target(self):
        """Test resolving single target."""
        code = """
from app.math_utils import add

def test_add():
    result = add(1, 2)
    assert result == 3
"""
        module = MANAGER.ast_from_string(code)
        func = next(module.nodes_of_class(nodes.FunctionDef))
        imports = extract_imports(module)

        targets = resolve_targets(func, imports, ["app"])

        assert len(targets) == 1
        assert targets[0].module == "app.math_utils"
        assert "add" in targets[0].symbols

    def test_resolve_multiple_targets(self):
        """Test resolving multiple targets from same module."""
        code = """
from app.math_utils import add, subtract

def test_math():
    assert add(1, 2) == 3
    assert subtract(5, 3) == 2
"""
        module = MANAGER.ast_from_string(code)
        func = next(module.nodes_of_class(nodes.FunctionDef))
        imports = extract_imports(module)

        targets = resolve_targets(func, imports, ["app"])

        assert len(targets) == 1
        assert targets[0].module == "app.math_utils"
        assert "add" in targets[0].symbols
        assert "subtract" in targets[0].symbols

    def test_no_matching_targets(self):
        """Test when no targets match root modules."""
        code = """
import os

def test_something():
    path = os.path.join("a", "b")
    assert path
"""
        module = MANAGER.ast_from_string(code)
        func = next(module.nodes_of_class(nodes.FunctionDef))
        imports = extract_imports(module)

        targets = resolve_targets(func, imports, ["myapp"])

        assert len(targets) == 0


class TestCalculateBodyMD5:
    """Test MD5 calculation."""

    def test_md5_consistent(self):
        """Test MD5 is consistent for same code."""
        code = """
def test_something():
    assert 1 == 1
"""
        module = MANAGER.ast_from_string(code)
        func = next(module.nodes_of_class(nodes.FunctionDef))

        md5_1 = calculate_body_md5(func)
        md5_2 = calculate_body_md5(func)

        assert md5_1 == md5_2
        assert len(md5_1) == 32  # MD5 is 32 hex chars

    def test_md5_different_for_different_code(self):
        """Test MD5 differs for different code."""
        code1 = "def test_1(): assert 1 == 1"
        code2 = "def test_2(): assert 2 == 2"

        module1 = MANAGER.ast_from_string(code1)
        module2 = MANAGER.ast_from_string(code2)

        func1 = next(module1.nodes_of_class(nodes.FunctionDef))
        func2 = next(module2.nodes_of_class(nodes.FunctionDef))

        md5_1 = calculate_body_md5(func1)
        md5_2 = calculate_body_md5(func2)

        assert md5_1 != md5_2


class TestParseTestFunction:
    """Test test function parsing."""

    def test_parse_complete_test(self):
        """Test parsing a complete test function."""
        code = """
from app.math_utils import add

def test_add():
    result = add(2, 3)
    assert result == 5
"""
        module = MANAGER.ast_from_string(code)
        func = next(module.nodes_of_class(nodes.FunctionDef))
        imports = extract_imports(module)

        test = parse_test_function(func, "test_file.py", imports, ["app"])

        assert test.name == "test_add"
        assert test.file == "test_file.py"
        assert test.line == func.lineno
        assert test.location == f"test_file.py:{func.lineno}"
        assert len(test.body_md5) == 32
        assert test.assert_count == 1
        assert len(test.targets) == 1
        assert test.targets[0].module == "app.math_utils"
