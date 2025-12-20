"""File scanning and orchestration for environment variable detection."""

from pathlib import Path

from upcast.common.file_utils import collect_python_files, validate_path
from upcast.env_var_scanner.checker import EnvVarChecker


def scan_directory(
    directory: str,
    pattern: str = "**/*.py",
    include_patterns: list[str] | None = None,
    exclude_patterns: list[str] | None = None,
    use_default_excludes: bool = True,
) -> EnvVarChecker:
    """Scan a directory for Python files and detect environment variables.

    Args:
        directory: Path to the directory to scan
        pattern: Glob pattern for matching files (default: **/*.py) - DEPRECATED, use include_patterns
        include_patterns: Glob patterns for files to include
        exclude_patterns: Glob patterns for files to exclude
        use_default_excludes: Whether to apply default exclude patterns (default: True)

    Returns:
        EnvVarChecker with aggregated results
    """
    dir_path = validate_path(directory)
    checker = EnvVarChecker(base_path=str(dir_path))

    # Use common file collection with filtering
    python_files = collect_python_files(
        dir_path,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
        use_default_excludes=use_default_excludes,
    )
    for file_path in python_files:
        checker.check_file(str(file_path))

    return checker


def scan_files(file_paths: list[str]) -> EnvVarChecker:
    """Scan specific Python files for environment variables.

    Args:
        file_paths: List of file paths to scan

    Returns:
        EnvVarChecker with aggregated results
    """
    # Use current working directory as base for relative paths
    checker = EnvVarChecker(base_path=str(Path.cwd()))

    for file_path in file_paths:
        checker.check_file(file_path)

    return checker
