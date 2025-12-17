"""Command-line interface for Django model scanner."""

import sys
from pathlib import Path
from typing import Any, Optional

from astroid import MANAGER, nodes

from upcast.common.file_utils import collect_python_files, validate_path
from upcast.django_model_scanner.checker import DjangoModelChecker
from upcast.django_model_scanner.export import export_to_yaml, export_to_yaml_string


def scan_django_models(  # noqa: C901
    path: str,
    output: Optional[str] = None,
    verbose: bool = False,
    include_patterns: Optional[list[str]] = None,
    exclude_patterns: Optional[list[str]] = None,
    use_default_excludes: bool = True,
) -> str:
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
    # Validate and normalize input path
    input_path = validate_path(path)

    # Collect Python files to scan using common utilities
    python_files = collect_python_files(
        input_path,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
        use_default_excludes=use_default_excludes,
    )

    if not python_files:
        if verbose:
            print(f"No Python files found in: {path}", file=sys.stderr)
        return ""

    if verbose:
        print(f"Scanning {len(python_files)} Python file(s)...", file=sys.stderr)

    # Determine root path for module path calculation
    # Try to find the project root by looking for marker files
    root_path = _find_project_root(input_path, verbose)

    # Create checker with root path
    checker = DjangoModelChecker(root_path=root_path)

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


def _find_project_root(start_path: Path, verbose: bool = False) -> str:
    """Find the Python package root directory.

    For projects with src/ layout, returns the src/ directory.
    Otherwise returns the start_path itself.

    Args:
        start_path: Starting path (file or directory) - typically the repository root
        verbose: Enable verbose output

    Returns:
        Absolute path to the Python package root directory
    """
    # Start from the directory
    search_path = start_path if start_path.is_dir() else start_path.parent
    search_path = search_path.resolve()

    # First check if current path is inside a src/ directory
    current = search_path
    while current.parent != current:  # Stop at filesystem root
        if current.name == "src":
            # Check if this src/ contains Python packages
            has_python_packages = any(current.rglob("__init__.py"))
            if has_python_packages:
                if verbose:
                    print(f"Found Python packages in src/, using: {current}", file=sys.stderr)
                return str(current)
        current = current.parent

    # Check if there's a src/ subdirectory with Python packages
    src_dir = search_path / "src"
    if src_dir.is_dir():
        # Check if src/ contains Python packages (has __init__.py files)
        has_python_packages = any(src_dir.rglob("__init__.py"))
        if has_python_packages:
            if verbose:
                print(f"Found Python packages in src/, using: {src_dir}", file=sys.stderr)
            return str(src_dir)

    # Otherwise use the search path itself as root
    if verbose:
        print(f"Using directory as Python root: {search_path}", file=sys.stderr)
    return str(search_path)


def _scan_file(file_path: Path, checker: DjangoModelChecker, verbose: bool = False) -> None:
    """Scan a single Python file for Django models.

    Args:
        file_path: Path to the Python file
        checker: The DjangoModelChecker instance
        verbose: Enable verbose output
    """
    try:
        # Calculate module name from file path relative to root
        modname = None
        if checker.root_path:
            try:
                root_p = Path(checker.root_path).resolve()
                file_p = file_path.resolve()
                if file_p.is_relative_to(root_p):
                    rel_path = file_p.relative_to(root_p)
                    # Convert to module path
                    if rel_path.name == "__init__.py":
                        # For __init__.py, use parent directory as module
                        if rel_path.parent.parts:
                            modname = ".".join(rel_path.parent.parts)
                    else:
                        # Remove .py extension
                        modname = ".".join(rel_path.with_suffix("").parts)
            except (ValueError, OSError):
                pass

        # Parse the file with astroid, providing module name if available
        if modname:
            module = MANAGER.ast_from_file(str(file_path), modname=modname)
        else:
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
