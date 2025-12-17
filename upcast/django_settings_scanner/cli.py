"""Command-line interface for Django settings scanner."""

from pathlib import Path

import click

from upcast.django_settings_scanner.checker import DjangoSettingsChecker
from upcast.django_settings_scanner.export import export_to_yaml, export_to_yaml_string


def _validate_path(path: str) -> Path:
    """Validate that the input path exists.

    Args:
        path: Path to validate

    Returns:
        Path object

    Raises:
        click.ClickException: If path does not exist
    """
    p = Path(path)
    if not p.exists():
        raise click.ClickException(f"Path does not exist: {path}")
    return p


def _collect_python_files(path: Path) -> list[Path]:
    """Recursively collect Python files, excluding common directories.

    Args:
        path: Root path to search

    Returns:
        List of Python file paths
    """
    if path.is_file():
        return [path] if path.suffix == ".py" else []

    # Directories to exclude
    exclude_dirs = {
        "venv",
        "env",
        ".venv",
        "virtualenv",
        "site-packages",
        "__pycache__",
        "build",
        "dist",
        ".egg-info",
        ".tox",
        ".pytest_cache",
        "node_modules",
    }

    python_files = []
    for item in path.rglob("*.py"):
        # Check if any parent directory should be excluded
        if any(part in exclude_dirs for part in item.parts):
            continue
        python_files.append(item)

    return python_files


def _process_files(checker: DjangoSettingsChecker, files: list[Path], verbose: bool) -> None:
    """Process Python files with the checker.

    Args:
        checker: DjangoSettingsChecker instance
        files: List of files to process
        verbose: Enable verbose output
    """
    for file_path in files:
        if verbose:
            click.echo(f"Scanning: {file_path}")
        try:
            checker.check_file(str(file_path))
        except Exception as e:
            click.echo(f"Error scanning {file_path}: {e!s}", err=True)


def scan_django_settings(path: str, output: str | None = None, verbose: bool = False) -> dict:
    """Scan Django project for settings usage.

    Args:
        path: Path to scan (file or directory)
        output: Optional output file path for YAML
        verbose: Enable verbose output

    Returns:
        Dictionary of settings variables and their usages
    """
    # Validate path
    root_path = _validate_path(path)

    # Determine base path for relative path calculation
    base_path = root_path if root_path.is_dir() else root_path.parent

    # Initialize checker
    checker = DjangoSettingsChecker(str(base_path))

    # Collect Python files
    if verbose:
        click.echo(f"Collecting Python files from {root_path}...")
    python_files = _collect_python_files(root_path)

    if not python_files:
        click.echo("No Python files found.")
        return {}

    if verbose:
        click.echo(f"Found {len(python_files)} Python files.")

    # Process files
    _process_files(checker, python_files, verbose)

    # Output results
    if checker.settings:
        total_usages = sum(var.count for var in checker.settings.values())
        click.echo(f"\nFound {len(checker.settings)} unique settings " f"with {total_usages} total usages.")

        if output:
            export_to_yaml(checker.settings, output)
            click.echo(f"Results written to {output}")
        else:
            # Print to stdout
            yaml_output = export_to_yaml_string(checker.settings)
            click.echo("\n" + yaml_output)
    else:
        click.echo("No Django settings usage found.")

    return checker.settings
