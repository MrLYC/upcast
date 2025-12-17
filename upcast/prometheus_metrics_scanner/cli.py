"""Command-line interface for Prometheus metrics scanner."""

import sys
from pathlib import Path
from typing import Optional

from upcast.prometheus_metrics_scanner.checker import PrometheusMetricsChecker
from upcast.prometheus_metrics_scanner.export import export_to_yaml, export_to_yaml_string


def _validate_path(path_str: str) -> Path:
    """Validate and return input path.

    Args:
        path_str: Path string to validate

    Returns:
        Validated Path object

    Raises:
        FileNotFoundError: If path doesn't exist
        ValueError: If path is neither file nor directory
    """
    input_path = Path(path_str)
    if not input_path.exists():
        raise FileNotFoundError(f"Path not found: {path_str}")

    if not (input_path.is_file() or input_path.is_dir()):
        raise ValueError(f"Path must be a file or directory: {path_str}")

    return input_path


def _process_files(python_files: list[Path], base_path: Path, verbose: bool) -> dict:
    """Process Python files and collect metrics.

    Args:
        python_files: List of Python files to process
        base_path: Base path for relative paths
        verbose: Enable verbose logging

    Returns:
        Dictionary of collected metrics
    """
    if verbose:
        print(f"Scanning {len(python_files)} Python file(s)...", file=sys.stderr)

    checker = PrometheusMetricsChecker(str(base_path))

    for py_file in python_files:
        if verbose:
            print(f"  Processing: {py_file}", file=sys.stderr)

        try:
            checker.check_file(str(py_file))
        except Exception as e:
            if verbose:
                print(f"  Error processing {py_file}: {e}", file=sys.stderr)

    return checker.get_metrics()


def scan_prometheus_metrics(path: str, output: Optional[str] = None, verbose: bool = False) -> str:
    """Scan Prometheus metrics in Python files or directories.

    Args:
        path: Path to Python file or directory
        output: Optional output file path. If None, returns YAML string
        verbose: Enable verbose output for debugging

    Returns:
        YAML string if output is None, otherwise empty string after writing file

    Raises:
        FileNotFoundError: If the input path doesn't exist
        ValueError: If the path is neither a file nor directory
    """
    input_path = _validate_path(path)

    python_files = _collect_python_files(input_path)

    if not python_files:
        if verbose:
            print(f"No Python files found in: {path}", file=sys.stderr)
        return ""

    base_path = input_path if input_path.is_dir() else input_path.parent
    metrics = _process_files(python_files, base_path, verbose)

    if verbose:
        print(f"Found {len(metrics)} Prometheus metric(s)", file=sys.stderr)

    if output:
        export_to_yaml(metrics, output)
        if verbose:
            print(f"Wrote output to: {output}", file=sys.stderr)
        return ""

    return export_to_yaml_string(metrics)


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

    # Recursively find all .py files, excluding common directories
    exclude_dirs = {
        "venv",
        ".venv",
        "env",
        "build",
        "dist",
        ".eggs",
        "__pycache__",
        ".pytest_cache",
        ".tox",
        ".git",
    }

    python_files = []
    for py_file in path.rglob("*.py"):
        # Check if file is in an excluded directory
        if any(excluded in py_file.parts for excluded in exclude_dirs):
            continue
        python_files.append(py_file)

    return python_files
