"""File discovery and path utilities."""

import os
from pathlib import Path
from typing import Optional

from pathspec import GitIgnoreSpec


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
    from upcast.common.patterns import match_patterns, should_exclude

    if path.is_file():
        return [path] if path.suffix == ".py" else []

    gitignore_spec = _load_gitignore_spec(path)
    python_files = []

    for root, dirnames, filenames in os.walk(path, topdown=True):
        root_path = Path(root)

        dirnames[:] = [
            dirname
            for dirname in dirnames
            if not _should_skip_directory(
                (root_path / dirname).relative_to(path),
                gitignore_spec=gitignore_spec,
                exclude_patterns=exclude_patterns,
                use_default_excludes=use_default_excludes,
            )
        ]

        for filename in filenames:
            py_file = root_path / filename
            relative_path = py_file.relative_to(path)

            if py_file.suffix == ".py" or (
                py_file.suffix == ".pyi" and include_patterns and match_patterns(relative_path, include_patterns)
            ):
                pass
            else:
                continue

            if _matches_gitignore(relative_path, gitignore_spec):
                continue

            if should_exclude(
                relative_path,
                include_patterns=include_patterns,
                exclude_patterns=exclude_patterns,
                use_default_excludes=use_default_excludes,
            ):
                continue

            python_files.append(py_file)

    return sorted(python_files)


def _load_gitignore_spec(path: Path) -> GitIgnoreSpec | None:
    """Load .gitignore rules from the target directory root."""
    gitignore_path = path / ".gitignore"
    if not gitignore_path.is_file():
        return None

    lines = gitignore_path.read_text(encoding="utf-8").splitlines()
    if not lines:
        return None

    return GitIgnoreSpec.from_lines(lines)


def _matches_gitignore(relative_path: Path, gitignore_spec: GitIgnoreSpec | None, *, is_dir: bool = False) -> bool:
    """Check whether a relative path matches target .gitignore rules."""
    if gitignore_spec is None:
        return False

    path_str = relative_path.as_posix()
    if not path_str or path_str == ".":
        return False

    if is_dir:
        path_str = f"{path_str}/"

    return gitignore_spec.match_file(path_str)


def _should_skip_directory(
    relative_path: Path,
    *,
    gitignore_spec: GitIgnoreSpec | None,
    exclude_patterns: Optional[list[str]],
    use_default_excludes: bool,
) -> bool:
    """Check whether a directory should be pruned during discovery."""
    from upcast.common.patterns import should_exclude

    return should_exclude(
        relative_path,
        exclude_patterns=exclude_patterns,
        use_default_excludes=use_default_excludes,
    ) or _matches_gitignore(relative_path, gitignore_spec, is_dir=True)


def get_relative_path_str(file_path: Path, base_path: Path) -> str:
    """Get relative path as string, with fallback to absolute if not relative.

    Args:
        file_path: File path (absolute or relative)
        base_path: Base directory path

    Returns:
        Relative path string if file is under base_path, otherwise absolute path string

    Examples:
        >>> get_relative_path_str(Path("/project/src/app.py"), Path("/project"))
        'src/app.py'
        >>> get_relative_path_str(Path("/other/file.py"), Path("/project"))
        '/other/file.py'
    """
    try:
        return str(file_path.relative_to(base_path))
    except ValueError:
        # If file_path is not relative to base_path, return absolute path
        return str(file_path)


def is_test_file(file_path: Path) -> bool:
    """Check if a file is a test file based on common naming patterns.

    Args:
        file_path: Path to check

    Returns:
        True if file matches test file patterns

    Examples:
        >>> is_test_file(Path("tests/test_app.py"))
        True
        >>> is_test_file(Path("src/app.py"))
        False
        >>> is_test_file(Path("app_test.py"))
        True
    """
    # Common test file patterns
    test_patterns = [
        "tests/**",
        "**/tests/**",
        "test_*.py",
        "*_test.py",
        "**/test_*.py",
        "**/*_test.py",
    ]

    # Check if path matches any test pattern
    return any(file_path.match(pattern) for pattern in test_patterns)
