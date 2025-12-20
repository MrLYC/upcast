"""Tests for complexity calculation in complexity_parser.py."""

from pathlib import Path

import pytest
from astroid import parse

from upcast.cyclomatic_complexity_scanner.complexity_parser import (
    calculate_complexity,
)


class TestComplexityCalculation:
    """Tests for basic complexity calculation."""

    def test_simple_function(self):
        """Test that a simple function has complexity 1."""
        source = """
def simple():
    return 42
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        complexity = calculate_complexity(func)

        assert complexity == 1

    def test_function_with_if(self):
        """Test that if statement adds 1 to complexity."""
        source = """
def with_if(x):
    if x > 0:
        return x
    return -x
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        complexity = calculate_complexity(func)

        assert complexity == 2  # 1 base + 1 if

    def test_function_with_if_elif(self):
        """Test that if-elif adds complexity."""
        source = """
def with_elif(x):
    if x > 0:
        return "positive"
    elif x < 0:
        return "negative"
    return "zero"
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        complexity = calculate_complexity(func)

        assert complexity == 3  # 1 base + 1 if + 1 elif

    def test_function_with_if_elif_else(self):
        """Test that else doesn't add complexity."""
        source = """
def with_else(x):
    if x > 0:
        return "positive"
    elif x < 0:
        return "negative"
    else:
        return "zero"
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        complexity = calculate_complexity(func)

        assert complexity == 3  # 1 base + 1 if + 1 elif (else doesn't count)

    def test_function_with_for_loop(self):
        """Test that for loop adds 1 to complexity."""
        source = """
def with_loop(items):
    total = 0
    for item in items:
        total += item
    return total
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        complexity = calculate_complexity(func)

        assert complexity == 2  # 1 base + 1 for

    def test_function_with_while_loop(self):
        """Test that while loop adds 1 to complexity."""
        source = """
def with_while(n):
    count = 0
    while n > 0:
        count += 1
        n -= 1
    return count
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        complexity = calculate_complexity(func)

        assert complexity == 2  # 1 base + 1 while

    def test_function_with_exception_handler(self):
        """Test that exception handlers add to complexity."""
        source = """
def with_except(value):
    try:
        return int(value)
    except ValueError:
        return 0
    except TypeError:
        return -1
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        complexity = calculate_complexity(func)

        assert complexity == 3  # 1 base + 1 ValueError + 1 TypeError

    def test_function_with_and_operator(self):
        """Test that 'and' operator adds to complexity."""
        source = """
def with_and(x, y):
    if x > 0 and y > 0:
        return x + y
    return 0
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        complexity = calculate_complexity(func)

        assert complexity == 3  # 1 base + 1 if + 1 and

    def test_function_with_or_operator(self):
        """Test that 'or' operator adds to complexity."""
        source = """
def with_or(x, y):
    if x > 0 or y > 0:
        return max(x, y)
    return 0
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        complexity = calculate_complexity(func)

        assert complexity == 3  # 1 base + 1 if + 1 or

    def test_function_with_multiple_bool_ops(self):
        """Test that multiple boolean operators add to complexity."""
        source = """
def with_multiple_ops(x, y, z):
    if x > 0 and y > 0 and z > 0:
        return x + y + z
    return 0
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        complexity = calculate_complexity(func)

        assert complexity == 4  # 1 base + 1 if + 2 and operators

    def test_function_with_ternary(self):
        """Test that ternary expression adds to complexity."""
        source = """
def with_ternary(x):
    return x if x > 0 else 0
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        complexity = calculate_complexity(func)

        assert complexity == 2  # 1 base + 1 ternary

    def test_function_with_list_comprehension(self):
        """Test that list comprehension with if adds to complexity."""
        source = """
def with_comprehension(items):
    return [x for x in items if x > 0]
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        complexity = calculate_complexity(func)

        assert complexity == 2  # 1 base + 1 comprehension if

    def test_function_with_multiple_comprehension_ifs(self):
        """Test that multiple if clauses in comprehension add complexity."""
        source = """
def with_multiple_ifs(items):
    return [x for x in items if x > 0 if x % 2 == 0]
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        complexity = calculate_complexity(func)

        assert complexity == 3  # 1 base + 2 comprehension ifs

    def test_function_with_assert(self):
        """Test that assert with condition adds to complexity."""
        source = """
def with_assert(value):
    assert value > 0
    return value * 2
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        complexity = calculate_complexity(func)

        assert complexity == 2  # 1 base + 1 assert

    def test_nested_conditions(self):
        """Test nested if statements."""
        source = """
def nested(x, y):
    if x > 0:
        if y > 0:
            return x + y
        return x
    return 0
"""
        module = parse(source)
        func = next(iter(module.nodes_of_class(parse("def f(): pass").body[0].__class__)))
        complexity = calculate_complexity(func)

        assert complexity == 3  # 1 base + 2 if statements


class TestComplexFixtures:
    """Test complexity calculation using fixture files."""

    @pytest.fixture
    def simple_fixture_path(self):
        """Path to simple.py fixture."""
        return Path(__file__).parent / "fixtures" / "simple.py"

    @pytest.fixture
    def complex_fixture_path(self):
        """Path to complex.py fixture."""
        return Path(__file__).parent / "fixtures" / "complex.py"

    def test_simple_fixture_complexities(self, simple_fixture_path):
        """Test expected complexities from simple.py fixture."""
        with open(simple_fixture_path, encoding="utf-8") as f:
            source = f.read()

        module = parse(source)
        functions = list(module.nodes_of_class(parse("def f(): pass").body[0].__class__))

        expected = {
            "simple_function": 1,
            "function_with_if": 2,
            "function_with_if_elif": 3,
            "function_with_loop": 2,
            "function_with_while": 2,
        }

        for func in functions:
            if func.name in expected:
                complexity = calculate_complexity(func)
                assert complexity == expected[func.name], (
                    f"{func.name}: expected {expected[func.name]}, got {complexity}"
                )

    def test_complex_fixture_complexities(self, complex_fixture_path):
        """Test expected complexities from complex.py fixture."""
        with open(complex_fixture_path, encoding="utf-8") as f:
            source = f.read()

        module = parse(source)
        functions = list(module.nodes_of_class(parse("def f(): pass").body[0].__class__))

        # Note: These are minimum expected values
        expected_min = {
            "complex_function": 7,  # Multiple conditions and loops
            "function_with_try_except": 3,  # 1 base + 1 if + 2 except
            "function_with_ternary": 3,  # 1 base + 2 ternary
            "function_with_comprehension": 3,  # 1 base + comprehension ifs
            "async_function_complex": 5,  # Multiple conditions
            "complex_method": 6,  # Complex method in class
        }

        for func in functions:
            if func.name in expected_min:
                complexity = calculate_complexity(func)
                assert complexity >= expected_min[func.name], (
                    f"{func.name}: expected at least {expected_min[func.name]}, got {complexity}"
                )
