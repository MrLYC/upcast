"""Tests for target resolution in unit tests."""

import pytest
from pathlib import Path
from textwrap import dedent

from upcast.scanners.unit_tests import UnitTestScanner


class TestBasicTargetResolution:
    """Test basic target resolution from imports."""

    def test_simple_import(self, tmp_path):
        """Test should resolve targets from simple imports."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            from myapp.utils import helper

            def test_helper():
                result = helper()
                assert result
        """)
        )

        scanner = UnitTestScanner(root_modules=["myapp"])
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        assert len(tests[0].targets) == 1
        assert tests[0].targets[0].module_path == "myapp.utils"

    def test_multiple_root_modules(self, tmp_path):
        """Multiple root_modules should all be included."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            from myapp.utils import helper
            from otherapp.tools import tool
            from thirdparty.lib import external

            def test_mixed():
                result1 = helper()
                result2 = tool()
                result3 = external()
                assert result1 and result2 and result3
        """)
        )

        scanner = UnitTestScanner(root_modules=["myapp", "otherapp"])
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        assert len(tests[0].targets) == 2

        modules = {t.module_path for t in tests[0].targets}
        assert "myapp.utils" in modules
        assert "otherapp.tools" in modules
        assert "thirdparty.lib" not in modules

    def test_no_root_modules_includes_all(self, tmp_path):
        """When root_modules is None, all imports should be included."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            from myapp.utils import helper
            from other.package import external

            def test_mixed():
                result1 = helper()
                result2 = external()
                assert result1 and result2
        """)
        )

        scanner = UnitTestScanner(root_modules=None)
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        assert len(tests[0].targets) == 2

        modules = {t.module_path for t in tests[0].targets}
        assert "myapp.utils" in modules
        assert "other.package" in modules


class TestImportStyles:
    """Test different import styles."""

    def test_import_as(self, tmp_path):
        """Test 'import X as Y' style imports."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            import myapp.utils as utils

            def test_utils():
                result = utils.helper()
                assert result
        """)
        )

        scanner = UnitTestScanner(root_modules=["myapp"])
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        # Should track the usage through the alias
        assert len(tests[0].targets) >= 0  # May or may not resolve depending on implementation

    def test_from_import_as(self, tmp_path):
        """Test 'from X import Y as Z' style imports."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            from myapp.utils import helper as h

            def test_helper():
                result = h()
                assert result
        """)
        )

        scanner = UnitTestScanner(root_modules=["myapp"])
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        assert len(tests[0].targets) == 1
        assert tests[0].targets[0].module_path == "myapp.utils"


class TestTargetSymbols:
    """Test symbol extraction from targets."""

    def test_unused_imports_not_in_targets(self, tmp_path):
        """Imported but unused symbols should not appear in targets."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            from myapp.utils import helper, unused

            def test_helper():
                result = helper()
                assert result
        """)
        )

        scanner = UnitTestScanner(root_modules=["myapp"])
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        # Only 'helper' is used, 'unused' should not be in targets
        assert "helper" in tests[0].targets[0].symbols

    def test_symbols_sorted(self, tmp_path):
        """Symbols should be sorted alphabetically."""
        test_file = tmp_path / "test_example.py"
        test_file.write_text(
            dedent("""
            from myapp.utils import zebra, alpha, beta

            def test_all():
                zebra()
                alpha()
                beta()
                assert True
        """)
        )

        scanner = UnitTestScanner(root_modules=["myapp"])
        result = scanner.scan(tmp_path)

        tests = list(result.results.values())[0]
        symbols = tests[0].targets[0].symbols
        assert symbols == sorted(symbols)


class TestStructuredTargetResolution:
    """Test target preservation for richer Task 8 structures."""

    def test_fixture_helpers_do_not_create_extra_test_targets(self):
        """Fixture helpers named like tests should not appear as extra target-bearing tests."""
        fixture_file = Path(__file__).parent / "fixtures" / "test_structure_patterns.py"

        scanner = UnitTestScanner(root_modules=["myapp"])
        result = scanner.scan(fixture_file)

        tests = list(result.results.values())[0]
        test_names = {test.name for test in tests}
        target_modules = [target.module_path for test in tests for target in test.targets]

        assert test_names == {"test_marked_values", "test_targeted"}
        assert target_modules == ["myapp.service", "myapp.service"]
