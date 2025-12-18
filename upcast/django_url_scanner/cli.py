"""Command-line interface for Django URL scanner."""

import sys
from pathlib import Path

from astroid import MANAGER

from upcast.common.file_utils import collect_python_files, validate_path
from upcast.django_url_scanner.checker import UrlPatternChecker
from upcast.django_url_scanner.export import export_to_yaml, export_to_yaml_string


def scan_django_urls(  # noqa: C901
    path: str,
    output: str | None = None,
    verbose: bool = False,
    include_patterns: list[str] | None = None,
    exclude_patterns: list[str] | None = None,
    use_default_excludes: bool = True,
) -> str:
    """Scan Django URL patterns in a Python file or directory.

    Args:
        path: Path to Python file or directory containing URL configurations
        output: Optional output file path. If None, returns YAML string
        verbose: Enable verbose output for debugging
        include_patterns: Optional list of patterns to include
        exclude_patterns: Optional list of patterns to exclude
        use_default_excludes: Whether to use default exclusion patterns

    Returns:
        YAML string if output is None, otherwise empty string after writing file

    Raises:
        FileNotFoundError: If the input path doesn't exist
        ValueError: If the path is neither a file nor directory
    """
    # Validate and normalize input path
    input_path = validate_path(path)

    # Collect Python files to scan
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
    root_path = _find_project_root(input_path, verbose)

    # Create checker with root path
    checker = UrlPatternChecker(root_path=root_path, verbose=verbose)

    # Process each file
    for py_file in python_files:
        if verbose:
            print(f"  Processing: {py_file}", file=sys.stderr)

        try:
            _scan_file(py_file, checker, root_path, verbose)
        except Exception as e:
            if verbose:
                print(f"  Error processing {py_file}: {e}", file=sys.stderr)

    # Get collected URL patterns
    url_modules = checker.get_url_patterns()

    if verbose:
        total_patterns = sum(len(patterns) for patterns in url_modules.values())
        print(f"Found {total_patterns} URL pattern(s) in {len(url_modules)} module(s)", file=sys.stderr)

    # Export results
    if output:
        export_to_yaml(url_modules, output)
        if verbose:
            print(f"Wrote output to: {output}", file=sys.stderr)
        return ""
    else:
        return export_to_yaml_string(url_modules)


def _find_project_root(start_path: Path, verbose: bool = False) -> str:
    """Find the Python package root directory.

    For projects with src/ layout, returns the src/ directory.
    Otherwise returns the start_path itself.

    Args:
        start_path: Starting path (file or directory)
        verbose: Enable verbose output

    Returns:
        Absolute path to the Python package root directory
    """
    search_path = start_path if start_path.is_dir() else start_path.parent
    search_path = search_path.resolve()

    # Check if current path is inside a src/ directory
    current = search_path
    while current.parent != current:
        if current.name == "src":
            has_python_packages = any(current.rglob("__init__.py"))
            if has_python_packages:
                if verbose:
                    print(f"Found Python packages in src/, using: {current}", file=sys.stderr)
                return str(current)
        current = current.parent

    # Check if there's a src/ subdirectory
    src_dir = search_path / "src"
    if src_dir.is_dir():
        has_python_packages = any(src_dir.rglob("__init__.py"))
        if has_python_packages:
            if verbose:
                print(f"Found Python packages in src/, using: {src_dir}", file=sys.stderr)
            return str(src_dir)

    if verbose:
        print(f"Using directory as Python root: {search_path}", file=sys.stderr)
    return str(search_path)


def _scan_file(file_path: Path, checker: UrlPatternChecker, root_path: str, verbose: bool = False) -> None:
    """Scan a single Python file for URL patterns.

    Args:
        file_path: Path to the Python file
        checker: The UrlPatternChecker instance
        root_path: Root path for module name calculation
        verbose: Enable verbose output
    """
    try:
        # Calculate module name from file path relative to root
        modname = None
        if root_path:
            try:
                root_p = Path(root_path).resolve()
                file_p = file_path.resolve()
                if file_p.is_relative_to(root_p):
                    rel_path = file_p.relative_to(root_p)
                    if rel_path.name == "__init__.py":
                        if rel_path.parent.parts:
                            modname = ".".join(rel_path.parent.parts)
                    else:
                        modname = ".".join(rel_path.with_suffix("").parts)
            except (ValueError, OSError):
                pass

        # Parse the file with astroid
        if modname:
            module = MANAGER.ast_from_file(str(file_path), modname=modname)
        else:
            module = MANAGER.ast_from_file(str(file_path))

        # Scan for urlpatterns
        checker.visit_module(module)

    except Exception as e:
        if verbose:
            print(f"Error parsing {file_path}: {e}", file=sys.stderr)
        raise
