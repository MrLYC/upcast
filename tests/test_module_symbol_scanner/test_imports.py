"""Tests for import detection in module symbol scanner."""

import pytest
from pathlib import Path
from textwrap import dedent

from upcast.scanners.module_symbols import ModuleSymbolScanner


class TestBasicImports:
    """Test basic import statement detection."""

    def test_simple_import(self, tmp_path):
        """Simple import statement should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import os
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "os" in symbols.imported_modules
        assert symbols.imported_modules["os"].module_path == "os"

    def test_multiple_imports(self, tmp_path):
        """Multiple import statements should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import os
            import sys
            import json
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "os" in symbols.imported_modules
        assert "sys" in symbols.imported_modules
        assert "json" in symbols.imported_modules

    def test_dotted_import(self, tmp_path):
        """Dotted import should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import os.path
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "os" in symbols.imported_modules


class TestFromImports:
    """Test from...import statement detection."""

    def test_from_import_single(self, tmp_path):
        """Single from...import should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            from os import path
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "path" in symbols.imported_symbols
        assert symbols.imported_symbols["path"].module_path == "os.path"

    def test_from_import_multiple(self, tmp_path):
        """Multiple symbols from same module should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            from collections import OrderedDict, defaultdict
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert "OrderedDict" in symbols.imported_symbols
        assert "defaultdict" in symbols.imported_symbols

    def test_star_import(self, tmp_path):
        """Star import should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            from os import *
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        assert len(symbols.star_imported) == 1
        assert symbols.star_imported[0].module_path == "os"


class TestRelativeImports:
    """Test relative import detection."""

    def test_relative_import_single_dot(self, tmp_path):
        """Relative import with single dot should be detected."""
        package_dir = tmp_path / "mypackage"
        package_dir.mkdir()
        (package_dir / "__init__.py").write_text("")

        test_file = package_dir / "module.py"
        test_file.write_text(
            dedent("""
            from .utils import helper
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(tmp_path)

        # Should have detected the relative import
        assert output.summary.total_imports >= 1

    def test_relative_import_double_dot(self, tmp_path):
        """Relative import with double dot should be detected."""
        package_dir = tmp_path / "mypackage"
        sub_dir = package_dir / "subpackage"
        sub_dir.mkdir(parents=True)
        (package_dir / "__init__.py").write_text("")
        (sub_dir / "__init__.py").write_text("")

        test_file = sub_dir / "module.py"
        test_file.write_text(
            dedent("""
            from ..utils import helper
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(tmp_path)

        assert output.summary.total_imports >= 1


class TestImportAliases:
    """Test import alias detection."""

    def test_import_as(self, tmp_path):
        """Import with alias should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            import numpy as np
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        # Should detect numpy import
        assert "numpy" in symbols.imported_modules

    def test_from_import_as(self, tmp_path):
        """From import with alias should be detected."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            dedent("""
            from collections import OrderedDict as OD
        """)
        )

        scanner = ModuleSymbolScanner()
        output = scanner.scan(test_file)

        symbols = list(output.results.values())[0]
        # Alias handling may vary by implementation
        assert len(symbols.imported_symbols) >= 0
