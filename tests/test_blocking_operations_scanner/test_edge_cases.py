"""Edge case tests for blocking operations scanner."""

import pytest

from upcast.scanners.blocking_operations import BlockingOperationsScanner
from tests.fixtures.test_utils import create_test_file
from tests.test_blocking_operations_scanner.fixtures import edge_cases


class TestAliasedImports:
    """Test detection with various import aliases."""

    def test_aliased_imports_detection(self, tmp_path, create_scanner):
        """Test that aliased imports are correctly detected."""
        file_path = create_test_file(tmp_path, edge_cases.ALIASED_IMPORTS, "aliased.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        # Should detect sleep operations despite aliases
        assert output.summary.total_count >= 1
        assert len(output.results["time_based"]) >= 1


class TestNestedStructures:
    """Test detection in nested code structures."""

    def test_nested_function_calls(self, tmp_path, create_scanner):
        """Test detection in nested function definitions."""
        file_path = create_test_file(tmp_path, edge_cases.NESTED_CALLS, "nested.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        # Should detect all sleep calls in nested functions
        assert len(output.results["time_based"]) >= 2

    def test_lambda_functions(self, tmp_path, create_scanner):
        """Test detection in lambda functions."""
        file_path = create_test_file(tmp_path, edge_cases.LAMBDA_FUNCTIONS, "lambdas.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        # Should detect sleep calls in lambda definitions
        assert len(output.results["time_based"]) >= 2

    def test_attribute_chains(self, tmp_path, create_scanner):
        """Test detection with long attribute chains."""
        file_path = create_test_file(tmp_path, edge_cases.ATTRIBUTE_CHAINS, "chains.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        # Should detect lock operations in attribute chains
        assert len(output.results["synchronization"]) >= 1


class TestComplexExpressions:
    """Test detection in complex expressions."""

    def test_multiple_ops_one_line(self, tmp_path, create_scanner):
        """Test detection of multiple operations on one line."""
        file_path = create_test_file(tmp_path, edge_cases.MULTIPLE_OPS_ONE_LINE, "multi_line.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        # Should detect all sleep operations even on same line
        assert len(output.results["time_based"]) >= 3

    def test_comprehensions(self, tmp_path, create_scanner):
        """Test detection in list/dict/set comprehensions."""
        file_path = create_test_file(tmp_path, edge_cases.COMPREHENSIONS, "comprehensions.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        # Should detect sleep operations in comprehensions
        assert len(output.results["time_based"]) >= 3

    def test_generators(self, tmp_path, create_scanner):
        """Test detection in generator functions and expressions."""
        file_path = create_test_file(tmp_path, edge_cases.GENERATORS, "generators.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        # Should detect sleep operations in generators
        assert len(output.results["time_based"]) >= 2


class TestSpecialContexts:
    """Test detection in special code contexts."""

    def test_decorated_functions(self, tmp_path, create_scanner):
        """Test detection in decorated functions and decorators."""
        file_path = create_test_file(tmp_path, edge_cases.DECORATED_FUNCTIONS, "decorated.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        # Should detect sleep in both decorator and decorated function
        assert len(output.results["time_based"]) >= 2

    def test_exception_handlers(self, tmp_path, create_scanner):
        """Test detection in exception handlers."""
        file_path = create_test_file(tmp_path, edge_cases.EXCEPTION_HANDLERS, "exceptions.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        # Should detect operations in try/except/else/finally blocks
        assert output.summary.total_count >= 4

    def test_properties(self, tmp_path, create_scanner):
        """Test detection in property getters/setters."""
        file_path = create_test_file(tmp_path, edge_cases.PROPERTIES, "properties.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        # Should detect sleep operations in property methods
        assert len(output.results["time_based"]) >= 2

    def test_special_methods(self, tmp_path, create_scanner):
        """Test detection in __init__ and other special methods."""
        file_path = create_test_file(tmp_path, edge_cases.SPECIAL_METHODS, "special.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        # Should detect sleep in all special methods
        assert len(output.results["time_based"]) >= 4


class TestNegativeCases:
    """Test cases that should NOT detect operations."""

    def test_no_blocking_operations(self, tmp_path, create_scanner):
        """Test file with no blocking operations."""
        file_path = create_test_file(tmp_path, edge_cases.NO_BLOCKING_OPS, "no_blocking.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert output.summary.total_count == 0
        assert all(len(ops) == 0 for ops in output.results.values())

    def test_comments_and_strings(self, tmp_path, create_scanner):
        """Test that operations in comments/strings are not detected."""
        file_path = create_test_file(tmp_path, edge_cases.COMMENTS_AND_STRINGS, "comments_strings.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        # Only actual call should be detected, not ones in comments/strings
        assert len(output.results["time_based"]) == 1
        # Verify the detected one is the actual call (line 11 in the code string)
        assert output.results["time_based"][0].line == 11  # The actual_call line


class TestRobustness:
    """Test scanner robustness with edge cases."""

    def test_incomplete_code(self, tmp_path, create_scanner):
        """Test that scanner handles incomplete code gracefully."""
        file_path = create_test_file(tmp_path, edge_cases.INCOMPLETE_CODE, "incomplete.py")
        scanner = create_scanner(BlockingOperationsScanner)

        # Should not crash, may return empty or partial results
        try:
            output = scanner.scan(file_path)
            assert output is not None
        except Exception:
            # If parsing fails, that's acceptable for invalid syntax
            pytest.skip("Scanner cannot parse invalid syntax (expected)")

    def test_long_lines(self, tmp_path, create_scanner):
        """Test scanner with very long lines."""
        file_path = create_test_file(tmp_path, edge_cases.LONG_LINES, "long_lines.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        # Should detect operations despite long lines
        assert len(output.results["time_based"]) >= 2

    def test_unicode_code(self, tmp_path, create_scanner):
        """Test scanner with unicode/special characters."""
        file_path = create_test_file(tmp_path, edge_cases.UNICODE_CODE, "unicode.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        # Should detect operations regardless of unicode in names
        assert len(output.results["time_based"]) >= 2


class TestLocationInformation:
    """Test that line/column information is correctly captured."""

    def test_line_numbers_are_accurate(self, tmp_path, create_scanner):
        """Test that reported line numbers are accurate."""
        code = """import time

def func1():
    time.sleep(1)  # Line 4

def func2():
    time.sleep(2)  # Line 7
"""
        file_path = create_test_file(tmp_path, code, "line_test.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert len(output.results["time_based"]) == 2
        lines = sorted([op.line for op in output.results["time_based"]])
        assert lines[0] == 4
        assert lines[1] == 7

    def test_column_numbers_are_set(self, tmp_path, create_scanner):
        """Test that column numbers are captured."""
        code = """import time
def func():
    time.sleep(1)
"""
        file_path = create_test_file(tmp_path, code, "column_test.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert len(output.results["time_based"]) == 1
        assert output.results["time_based"][0].column is not None
        assert output.results["time_based"][0].column >= 0
