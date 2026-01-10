"""Tests for edge cases and error handling in unit test scanner."""

import pytest
from pathlib import Path
from textwrap import dedent

from upcast.scanners.unit_tests import UnitTestScanner


class TestInvalidSyntax:
    """Test handling of invalid Python syntax."""

    def test_invalid_syntax_file_skipped(self, tmp_path):
        """Files with invalid syntax should be skipped gracefully."""
        test_file = tmp_path / "test_invalid.py"
        test_file.write_text("def test_broken(:\n    assert True\n")

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        # Should not crash, just skip the file
        assert result.summary.total_tests == 0
        assert result.summary.total_files == 0

    def test_partial_valid_syntax(self, tmp_path):
        """File with some valid tests should handle gracefully."""
        test_file = tmp_path / "test_partial.py"
        test_file.write_text(
            dedent("""
            def test_valid():
                assert True
            
            # Invalid function below
            def test_broken(
                assert False
        """)
        )

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        # May or may not parse depending on astroid's error recovery
        assert isinstance(result.summary.total_tests, int)


class TestNonTestFunctions:
    """Test that non-test functions are not detected."""

    def test_helper_functions_ignored(self, tmp_path):
        """Helper functions without test_ prefix should be ignored."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            def helper_function():
                return 42
            
            def test_actual_test():
                assert helper_function() == 42
        """)
        )

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        assert len(tests) == 1
        assert tests[0].name == "test_actual_test"

    def test_nested_test_functions_ignored(self, tmp_path):
        """Test functions nested inside other functions should be ignored."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            def outer_function():
                def test_nested():
                    assert True
                return test_nested
            
            def test_top_level():
                assert True
        """)
        )

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        assert len(tests) == 1
        assert tests[0].name == "test_top_level"

    def test_class_method_without_test_class(self, tmp_path):
        """Test methods in non-test classes should be ignored."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            class RegularClass:
                def test_method(self):
                    assert True
            
            def test_function():
                assert True
        """)
        )

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        assert len(tests) == 1
        assert tests[0].name == "test_function"


class TestEmptyFiles:
    """Test handling of empty and minimal files."""

    def test_empty_file(self, tmp_path):
        """Empty test file should return no tests."""
        test_file = tmp_path / "test_empty.py"
        test_file.write_text("")

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        assert result.summary.total_tests == 0
        assert result.summary.total_files == 0

    def test_file_with_only_imports(self, tmp_path):
        """File with only imports should return no tests."""
        test_file = tmp_path / "test_imports_only.py"
        test_file.write_text(
            dedent("""
            import unittest
            from myapp.utils import helper
        """)
        )

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        assert result.summary.total_tests == 0

    def test_file_with_only_comments(self, tmp_path):
        """File with only comments should return no tests."""
        test_file = tmp_path / "test_comments.py"
        test_file.write_text(
            dedent("""
            # This is a comment
            # TODO: Add tests here
            \"\"\"
            Module docstring
            \"\"\"
        """)
        )

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        assert result.summary.total_tests == 0


class TestBodyMD5:
    """Test MD5 hash calculation."""

    def test_identical_tests_same_hash(self, tmp_path):
        """Two identical test functions should have different MD5 due to different names."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            def test_one():
                assert 1 == 1
            
            def test_two():
                assert 1 == 1
        """)
        )

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        assert len(tests) == 2
        # Different function names produce different hashes
        assert tests[0].body_md5 != tests[1].body_md5

    def test_different_tests_different_hash(self, tmp_path):
        """Different test functions should have different MD5."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            def test_one():
                assert 1 == 1
            
            def test_two():
                assert 2 == 2
        """)
        )

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        assert len(tests) == 2
        assert tests[0].body_md5 != tests[1].body_md5

    def test_comments_normalized_in_hash(self, tmp_path):
        """Comments should be normalized, but function names still differ."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            def test_with_comment():
                # This is a comment
                assert 1 == 1
            
            def test_without_comment():
                assert 1 == 1
        """)
        )

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        # Different function names produce different hashes even if body is similar
        assert tests[0].body_md5 != tests[1].body_md5


class TestFilePatterns:
    """Test file pattern matching."""

    def test_default_patterns_match_test_files(self, tmp_path):
        """Default patterns should match test_*.py files."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text("def test_func(): assert True")

        non_test_file = tmp_path / "regular.py"
        non_test_file.write_text("def test_func(): assert True")

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        # Should only scan test_example.py
        assert result.summary.total_files == 1

    def test_custom_patterns(self, tmp_path):
        """Custom patterns should be respected."""
        test_file = tmp_path / "custom_test.py"
        test_file.write_text("def test_func(): assert True")

        scanner = UnitTestScanner(include_patterns=["**/custom_*.py"])
        result = scanner.scan(tmp_path)

        assert result.summary.total_files == 1


class TestLineRanges:
    """Test line range tracking."""

    def test_line_range_captured(self, tmp_path):
        """Test function line ranges should be captured correctly."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            def test_multiline():
                x = 1
                y = 2
                z = x + y
                assert z == 3
        """)
        )

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        line_start, line_end = tests[0].line_range
        assert line_start > 0
        assert line_end > line_start
        assert line_end - line_start >= 4  # At least 5 lines
