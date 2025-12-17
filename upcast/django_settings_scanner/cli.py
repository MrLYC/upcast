"""Command-line interface for Django settings scanner."""

from pathlib import Path

import click

from upcast.common.file_utils import collect_python_files, validate_path
from upcast.django_settings_scanner.checker import DjangoSettingsChecker
from upcast.django_settings_scanner.export import export_to_yaml, export_to_yaml_string


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


def scan_django_settings(
    path: str,
    output: str | None = None,
    verbose: bool = False,
    include_patterns: list[str] | None = None,
    exclude_patterns: list[str] | None = None,
    use_default_excludes: bool = True,
) -> dict:
    """Scan Django project for settings usage.

    Args:
        path: Path to scan (file or directory)
        output: Optional output file path for YAML
        verbose: Enable verbose output

    Returns:
        Dictionary of settings variables and their usages
    """
    try:
        # Validate path using common utilities
        root_path = validate_path(path)
    except (FileNotFoundError, ValueError) as e:
        raise click.ClickException(str(e)) from e

    # Determine base path for relative path calculation
    base_path = root_path if root_path.is_dir() else root_path.parent

    # Initialize checker
    checker = DjangoSettingsChecker(str(base_path))

    # Collect Python files using common utilities
    if verbose:
        click.echo(f"Collecting Python files from {root_path}...")
    python_files = collect_python_files(
        root_path,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
        use_default_excludes=use_default_excludes,
    )

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
