"""CLI interface for concurrency pattern scanner."""

import sys
from pathlib import Path

import click

from upcast.concurrency_pattern_scanner.checker import ConcurrencyChecker
from upcast.concurrency_pattern_scanner.export import export_to_yaml, format_concurrency_output


@click.command()
@click.argument("path", type=click.Path(exists=True), required=False, default=".")
@click.option("-o", "--output", type=click.Path(), help="Output YAML file path")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option(
    "--include",
    multiple=True,
    help="File patterns to include (can be specified multiple times)",
)
@click.option(
    "--exclude",
    multiple=True,
    help="File patterns to exclude (can be specified multiple times)",
)
def scan_concurrency_patterns(
    path: str,
    output: str | None,
    verbose: bool,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
) -> None:
    """Scan Python code for concurrency patterns.

    Detects asyncio, threading, and multiprocessing patterns in Python files.

    PATH: Directory or file to scan (defaults to current directory)
    """
    scan_path = Path(path).resolve()

    if not scan_path.exists():
        click.echo(f"Error: Path '{path}' does not exist", err=True)
        sys.exit(1)

    # Collect Python files
    python_files = _collect_python_files(scan_path, include, exclude)

    if not python_files:
        click.echo("No Python files found to scan", err=True)
        sys.exit(1)

    if verbose:
        click.echo(f"Scanning {len(python_files)} Python files...")

    # Initialize checker
    checker = ConcurrencyChecker(root_path=str(scan_path), verbose=verbose)

    # Scan files
    for file_path in python_files:
        if verbose:
            click.echo(f"  Analyzing: {file_path}")
        checker.check_file(str(file_path))

    # Get patterns
    patterns = checker.get_patterns()

    # Output results
    if output:
        export_to_yaml(patterns, output)
        if verbose:
            click.echo(f"Results written to: {output}")
    else:
        # Print to stdout
        yaml_output = format_concurrency_output(patterns)
        click.echo(yaml_output)

    # Print summary
    if verbose:
        _print_summary(patterns)


def _collect_python_files(path: Path, include: tuple[str, ...], exclude: tuple[str, ...]) -> list[Path]:
    """Collect Python files to scan.

    Args:
        path: Root path to scan
        include: Patterns to include
        exclude: Patterns to exclude

    Returns:
        List of Python file paths
    """
    if path.is_file():
        return [path] if path.suffix == ".py" else []

    # Default patterns
    include_patterns = list(include) if include else ["**/*.py"]
    exclude_patterns = list(exclude) if exclude else []

    # Add common excludes
    default_excludes = [
        "**/.*",
        "**/__pycache__",
        "**/venv",
        "**/env",
        "**/node_modules",
        "**/build",
        "**/dist",
        "**/*.egg-info",
    ]
    exclude_patterns.extend(default_excludes)

    python_files = []

    # Collect files matching include patterns
    for pattern in include_patterns:
        for file_path in path.glob(pattern):
            if file_path.is_file():
                # Check if excluded
                excluded = False
                for exclude_pattern in exclude_patterns:
                    if file_path.match(exclude_pattern):
                        excluded = True
                        break

                if not excluded:
                    python_files.append(file_path)

    return sorted(set(python_files))


def _print_summary(patterns: dict) -> None:
    """Print summary statistics.

    Args:
        patterns: Patterns dictionary
    """
    click.echo("\nSummary:")

    for category, pattern_types in patterns.items():
        total = sum(len(items) for items in pattern_types.values())
        if total > 0:
            click.echo(f"  {category}: {total} patterns")
            for pattern_type, items in pattern_types.items():
                if items:
                    click.echo(f"    - {pattern_type}: {len(items)}")


if __name__ == "__main__":
    scan_concurrency_patterns()
