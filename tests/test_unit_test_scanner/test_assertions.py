"""Tests for assertion counting in unit tests."""

import pytest
from pathlib import Path
from textwrap import dedent

from upcast.scanners.unit_tests import UnitTestScanner


class TestPytestAssertions:
    """Test pytest assert statement counting."""

    def test_single_assert(self, tmp_path):
        """Single assert statement should be counted."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            def test_simple():
                assert 1 == 1
        """)
        )

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        assert len(result.results) == 1
        tests = list(result.results.values())[0]
        assert len(tests) == 1
        assert tests[0].assert_count == 1

    def test_multiple_asserts(self, tmp_path):
        """Multiple assert statements should all be counted."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            def test_multiple():
                assert 1 == 1
                assert 2 == 2
                assert 3 == 3
        """)
        )

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        assert tests[0].assert_count == 3

    def test_no_assertions(self, tmp_path):
        """Test with no assertions should have count of 0."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            def test_no_assert():
                x = 1 + 1
                print(x)
        """)
        )

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        assert tests[0].assert_count == 0


class TestUnittestAssertions:
    """Test unittest assertion method counting."""

    def test_unittest_assertions(self, tmp_path):
        """Unittest assertion methods should be counted."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            import unittest

            class TestMath(unittest.TestCase):
                def test_equality(self):
                    self.assertEqual(1, 1)
                    self.assertTrue(True)
                    self.assertFalse(False)
        """)
        )

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        assert tests[0].assert_count == 3

    def test_various_unittest_methods(self, tmp_path):
        """Various unittest assertion methods should all be counted."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            import unittest

            class TestVariousAsserts(unittest.TestCase):
                def test_all_types(self):
                    self.assertEqual(1, 1)
                    self.assertNotEqual(1, 2)
                    self.assertTrue(True)
                    self.assertFalse(False)
                    self.assertIs(None, None)
                    self.assertIsNot(1, 2)
                    self.assertIsNone(None)
                    self.assertIsNotNone(1)
                    self.assertIn(1, [1, 2, 3])
                    self.assertNotIn(4, [1, 2, 3])
        """)
        )

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        assert tests[0].assert_count == 10


class TestPytestRaises:
    """Test pytest.raises context manager counting."""

    def test_pytest_raises(self, tmp_path):
        """pytest.raises should be counted as an assertion."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            import pytest

            def test_exception():
                with pytest.raises(ValueError):
                    raise ValueError("error")
        """)
        )

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        assert tests[0].assert_count == 1

    def test_pytest_raises_with_match(self, tmp_path):
        """pytest.raises with match parameter should be counted."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            import pytest

            def test_exception_message():
                with pytest.raises(ValueError, match="error"):
                    raise ValueError("error")
        """)
        )

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        assert tests[0].assert_count == 1


class TestMixedAssertions:
    """Test mixed assertion types."""

    def test_mixed_pytest_and_raises(self, tmp_path):
        """Mix of pytest assert and pytest.raises should all be counted."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            import pytest

            def test_mixed():
                assert 1 == 1
                with pytest.raises(ValueError):
                    raise ValueError("error")
                assert 2 == 2
        """)
        )

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        assert tests[0].assert_count == 3

    def test_summary_total_assertions(self, tmp_path):
        """Summary should count total assertions across all tests."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            def test_one():
                assert 1 == 1
                assert 2 == 2

            def test_two():
                assert 3 == 3
        """)
        )

        scanner = UnitTestScanner()
        result = scanner.scan(tmp_path)

        assert result.summary.total_assertions == 3
        assert result.summary.total_tests == 2
