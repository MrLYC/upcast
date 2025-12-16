"""Command-line interface for Django model scanner."""

import sys
from pathlib import Path
from typing import Any, Optional

from astroid import MANAGER, nodes

from upcast.django_scanner.checker import DjangoModelChecker
from upcast.django_scanner.export import export_to_yaml, export_to_yaml_string


def scan_django_models(path: str, output: Optional[str] = None, verbose: bool = False) -> str:  # noqa: C901
    """Scan Django models in a Python file or directory.

    Args:
        path: Path to Python file or directory containing Django models
        output: Optional output file path. If None, returns YAML string
        verbose: Enable verbose output for debugging

    Returns:
        YAML string if output is None, otherwise empty string after writing file

    Raises:
        FileNotFoundError: If the input path doesn't exist
        ValueError: If the path is neither a file nor directory
    """
    # Validate input path
    input_path = Path(path)
    if not input_path.exists():
        raise FileNotFoundError(f"Path not found: {path}")

    if not (input_path.is_file() or input_path.is_dir()):
        raise ValueError(f"Path must be a file or directory: {path}")

    # Collect Python files to scan
    python_files = _collect_python_files(input_path)

    if not python_files:
        if verbose:
            print(f"No Python files found in: {path}", file=sys.stderr)
        return ""

    if verbose:
        print(f"Scanning {len(python_files)} Python file(s)...", file=sys.stderr)

    # Create checker
    checker = DjangoModelChecker()

    # Process each file
    for py_file in python_files:
        if verbose:
            print(f"  Processing: {py_file}", file=sys.stderr)

        try:
            _scan_file(py_file, checker, verbose)
        except Exception as e:
            if verbose:
                print(f"  Error processing {py_file}: {e}", file=sys.stderr)

    # Perform second-pass merge of abstract fields
    checker.close()

    # Get collected models
    models = checker.get_models()

    if verbose:
        print(f"Found {len(models)} Django model(s)", file=sys.stderr)

    # Export results
    if output:
        export_to_yaml(models, output)
        if verbose:
            print(f"Wrote output to: {output}", file=sys.stderr)
        return ""
    else:
        return export_to_yaml_string(models)


def _collect_python_files(path: Path) -> list[Path]:
    """Collect Python files from a path.

    Args:
        path: File or directory path

    Returns:
        List of Python file paths
    """
    if path.is_file():
        if path.suffix == ".py":
            return [path]
        return []

    # Recursively find all .py files
    return list(path.rglob("*.py"))


def _scan_file(file_path: Path, checker: DjangoModelChecker, verbose: bool = False) -> None:
    """Scan a single Python file for Django models.

    Args:
        file_path: Path to the Python file
        checker: The DjangoModelChecker instance
        verbose: Enable verbose output
    """
    try:
        # Parse the file with astroid
        module = MANAGER.ast_from_file(str(file_path))

        # Visit all ClassDef nodes in the module
        _visit_module_nodes(module, checker)

    except Exception as e:
        if verbose:
            print(f"Error parsing {file_path}: {e}", file=sys.stderr)
        raise


def _visit_module_nodes(module: Any, checker: DjangoModelChecker) -> None:
    """Visit all ClassDef nodes in a module.

    Args:
        module: The astroid Module node
        checker: The DjangoModelChecker instance
    """
    for node in module.nodes_of_class(nodes.ClassDef):
        checker.visit_classdef(node)


def _visit_node(node: Any, checker: DjangoModelChecker) -> None:
    """Visit an AST node (unused, kept for potential future use).

    Args:
        node: The AST node
        checker: The DjangoModelChecker instance
    """
    pass  # Currently using nodes_of_class which is more efficient
