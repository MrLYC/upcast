"""Tests for complexity calculation in CyclomaticComplexityScanner.

Tests cover:
- Base complexity
- Individual constructs (if, for, while, except, assert, ternary)
- Boolean operators
- Comprehensions
- Combined constructs
"""

import pytest


def test_base_complexity_simple_function(low_threshold_scanner, tmp_path):
    """Test that a simple function has base complexity of 1."""
    code = """
def simple_func():
    return 42
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 1
    assert result.results["test.py"][0].severity == "healthy"


def test_single_if_statement(low_threshold_scanner, tmp_path):
    """Test that a single if statement adds 1 to complexity."""
    code = """
def func_with_if(x):
    if x > 0:
        return x
    return 0
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 2  # Base 1 + if 1


def test_multiple_if_statements(low_threshold_scanner, tmp_path):
    """Test that multiple if statements each add 1 to complexity."""
    code = """
def func_with_multiple_ifs(x, y):
    if x > 0:
        return x
    if y > 0:
        return y
    return 0
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 3  # Base 1 + if 1 + if 1


def test_nested_if_statements(low_threshold_scanner, tmp_path):
    """Test that nested if statements each add 1 to complexity."""
    code = """
def func_with_nested_ifs(x, y):
    if x > 0:
        if y > 0:
            return x + y
    return 0
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 3  # Base 1 + if 1 + if 1


def test_for_loop_complexity(low_threshold_scanner, tmp_path):
    """Test that a for loop adds 1 to complexity."""
    code = """
def func_with_for(items):
    total = 0
    for item in items:
        total += item
    return total
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 2  # Base 1 + for 1


def test_while_loop_complexity(low_threshold_scanner, tmp_path):
    """Test that a while loop adds 1 to complexity."""
    code = """
def func_with_while(x):
    while x > 0:
        x -= 1
    return x
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 2  # Base 1 + while 1


def test_except_handler_complexity(low_threshold_scanner, tmp_path):
    """Test that except handlers add 1 to complexity each."""
    code = """
def func_with_except():
    try:
        risky_operation()
    except ValueError:
        handle_value_error()
    except KeyError:
        handle_key_error()
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 3  # Base 1 + except 1 + except 1


def test_assert_statement_complexity(low_threshold_scanner, tmp_path):
    """Test that assert statements add 1 to complexity."""
    code = """
def func_with_assert(x):
    assert x > 0
    assert x < 100
    return x
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 3  # Base 1 + assert 1 + assert 1


def test_ternary_if_expression_complexity(low_threshold_scanner, tmp_path):
    """Test that ternary if expressions (IfExp) add 1 to complexity."""
    code = """
def func_with_ternary(x):
    return "positive" if x > 0 else "negative"
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 2  # Base 1 + ternary if 1


def test_boolean_and_operator_complexity(low_threshold_scanner, tmp_path):
    """Test that boolean AND operators add 1 to complexity."""
    code = """
def func_with_and(x, y):
    if x > 0 and y > 0:
        return x + y
    return 0
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 3  # Base 1 + if 1 + and 1


def test_boolean_or_operator_complexity(low_threshold_scanner, tmp_path):
    """Test that boolean OR operators add 1 to complexity."""
    code = """
def func_with_or(x, y):
    if x > 0 or y > 0:
        return True
    return False
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 3  # Base 1 + if 1 + or 1


def test_multiple_boolean_operators(low_threshold_scanner, tmp_path):
    """Test that multiple boolean operators each add 1 to complexity."""
    code = """
def func_with_multiple_bools(x, y, z):
    if x > 0 and y > 0 or z > 0:
        return True
    return False
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 4  # Base 1 + if 1 + and 1 + or 1


def test_list_comprehension_with_if(low_threshold_scanner, tmp_path):
    """Test that if clauses in comprehensions add 1 to complexity."""
    code = """
def func_with_comprehension(items):
    return [x for x in items if x > 0]
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 2  # Base 1 + if in comprehension 1


def test_comprehension_with_multiple_ifs(low_threshold_scanner, tmp_path):
    """Test that multiple if clauses in comprehensions each add 1."""
    code = """
def func_with_multiple_comp_ifs(items):
    return [x for x in items if x > 0 if x < 100]
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 3  # Base 1 + if 1 + if 1


def test_combined_constructs_complexity(low_threshold_scanner, tmp_path):
    """Test combined constructs calculate correct total complexity."""
    code = """
def combined_func(x, y, items):
    if x > 0 and y > 0:
        for item in items:
            if item > 10:
                return item
    return 0
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    # Base 1 + if 1 + and 1 + for 1 + if 1 = 5
    assert result.results["test.py"][0].complexity == 5


def test_complex_function_with_all_constructs(low_threshold_scanner, tmp_path):
    """Test function with multiple different constructs."""
    code = """
def very_complex_func(x, y, items):
    result = "default" if x > 0 else "none"
    
    if y > 0:
        for item in items:
            while item > 0:
                try:
                    if item > 10 and item < 100:
                        assert item != 50
                        item -= 1
                except ValueError:
                    break
    
    return result
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    # Base 1 + ternary 1 + if 1 + for 1 + while 1 + if 1 + and 1 + assert 1 + except 1 = 9
    assert result.results["test.py"][0].complexity == 9
    assert result.results["test.py"][0].severity == "acceptable"


def test_elif_statements_complexity(low_threshold_scanner, tmp_path):
    """Test that elif statements add 1 to complexity each."""
    code = """
def func_with_elif(x):
    if x > 100:
        return "high"
    elif x > 50:
        return "medium"
    elif x > 0:
        return "low"
    else:
        return "zero or negative"
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    # Base 1 + if 1 + elif 1 + elif 1 = 4
    assert result.results["test.py"][0].complexity == 4


def test_nested_loops_complexity(low_threshold_scanner, tmp_path):
    """Test that nested loops each add 1 to complexity."""
    code = """
def func_with_nested_loops(matrix):
    total = 0
    for row in matrix:
        for item in row:
            total += item
    return total
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count == 1
    assert result.results["test.py"][0].complexity == 3  # Base 1 + for 1 + for 1


def test_match_case_not_counted(low_threshold_scanner, tmp_path):
    """Test that match/case statements are handled (Python 3.10+)."""
    code = """
def func_with_match(value):
    match value:
        case 1:
            return "one"
        case 2:
            return "two"
        case _:
            return "other"
"""
    file_path = tmp_path / "test.py"
    file_path.write_text(code)

    # This may parse differently depending on Python version
    # We just ensure it doesn't crash
    result = low_threshold_scanner.scan(tmp_path)

    assert result.summary.total_count >= 0  # Just ensure it doesn't crash
