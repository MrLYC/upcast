"""File discovery and path utilities."""

from pathlib import Path
from typing import Optional


def validate_path(path_str: str) -> Path:
    """Validate that a path exists and is either a file or directory.

    Args:
        path_str: Path string to validate

    Returns:
        Validated Path object

    Raises:
        FileNotFoundError: If path doesn't exist
        ValueError: If path is neither file nor directory
    """
    path = Path(path_str)

    if not path.exists():
        raise FileNotFoundError(f"Path not found: {path_str}")

    if not (path.is_file() or path.is_dir()):
        raise ValueError(f"Path must be a file or directory: {path_str}")

    return path


def find_package_root(start_path: Path) -> Path:
    """Find Python package root by locating __init__.py files.

    Walks up the directory tree to find the outermost directory
    containing __init__.py.

    Args:
        start_path: Starting path (file or directory)

    Returns:
        Package root path, or original path if no __init__.py found
    """
    current = start_path if start_path.is_dir() else start_path.parent

    # Find the outermost directory with __init__.py
    package_root = None

    while current.parent != current:  # Not at filesystem root
        if (current / "__init__.py").exists():
            package_root = current
        current = current.parent

    return package_root if package_root else start_path


def collect_python_files(
    path: Path,
    include_patterns: Optional[list[str]] = None,
    exclude_patterns: Optional[list[str]] = None,
    use_default_excludes: bool = True,
) -> list[Path]:
    """Recursively collect Python files with pattern filtering.

    Args:
        path: Root path to search (file or directory)
        include_patterns: Glob patterns for files to include (default: all .py files)
        exclude_patterns: Glob patterns for files to exclude
        use_default_excludes: Whether to apply default exclude patterns

    Returns:
        Sorted list of Python file paths
    """
    from upcast.common.patterns import should_exclude

    if path.is_file():
        return [path] if path.suffix == ".py" else []

    python_files = []

    for py_file in path.rglob("*.py"):
        # Apply filtering
        relative_path = py_file.relative_to(path)

        if should_exclude(
            relative_path,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            use_default_excludes=use_default_excludes,
        ):
            continue

        python_files.append(py_file)

    return sorted(python_files)
