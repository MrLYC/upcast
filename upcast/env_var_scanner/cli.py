"""File scanning and orchestration for environment variable detection."""

from pathlib import Path

from upcast.common.file_utils import collect_python_files, validate_path
from upcast.env_var_scanner.checker import EnvVarChecker


def scan_directory(directory: str, pattern: str = "**/*.py") -> EnvVarChecker:
    """Scan a directory for Python files and detect environment variables.

    Args:
        directory: Path to the directory to scan
        pattern: Glob pattern for matching files (default: **/*.py)

    Returns:
        EnvVarChecker with aggregated results
    """
    dir_path = validate_path(directory)
    checker = EnvVarChecker(base_path=str(dir_path))

    # Use common file collection
    python_files = collect_python_files(dir_path)
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
