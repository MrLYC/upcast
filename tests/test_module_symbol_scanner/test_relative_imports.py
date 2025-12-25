"""Test relative import resolution in module symbol scanner."""

import tempfile
from pathlib import Path

from upcast.scanners.module_symbols import ModuleSymbolScanner


def test_relative_import_resolution():
    """Test that relative imports are resolved to absolute module paths."""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)

        # Create package structure: mypackage/subpackage/__init__.py
        pkg = base / "mypackage" / "subpackage"
        pkg.mkdir(parents=True)

        # Create __init__.py with relative imports
        init_file = pkg / "__init__.py"
        init_file.write_text(
            """
from .module1 import *
from ..other import something
"""
        )

        # Scan the base directory
        scanner = ModuleSymbolScanner(verbose=True)
        result = scanner.scan(base)

        # Debug: print all results
        print("\nAll result paths:")
        for path in result.results:
            print(f"  - {path}")

        # Find results for the __init__.py file
        init_results = None
        for path, symbols in result.results.items():
            if "subpackage" in path and "__init__.py" in path:
                init_results = symbols
                break

        assert init_results is not None, "Could not find subpackage/__init__.py in results"

        # Debug: print what we got
        star_paths = [si.module_path for si in init_results.star_imported]
        print(f"Star import paths: {star_paths}")

        # Check star imports
        assert len(star_paths) == 1
        assert star_paths[0] == "mypackage.subpackage.module1", (
            f"Expected 'mypackage.subpackage.module1', got '{star_paths[0]}'"
        )

        # Check symbol imports
        assert "something" in init_results.imported_symbols
        sym_path = init_results.imported_symbols["something"].module_path
        print(f"Symbol import path: {sym_path}")
        assert sym_path == "mypackage.other.something", f"Expected 'mypackage.other.something', got '{sym_path}'"
