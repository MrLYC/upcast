"""CLI interface for exception handler scanner."""

from pathlib import Path

import click

from upcast.common.file_utils import collect_python_files
from upcast.exception_handler_scanner.checker import ExceptionHandlerChecker
from upcast.exception_handler_scanner.export import export_exception_handlers


@click.command()
@click.argument("path", type=click.Path(exists=True), required=False, default=".")
@click.option("-o", "--output", type=click.Path(), help="Output file path (YAML or JSON)")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option("--include", multiple=True, help="File patterns to include (can be used multiple times)")
@click.option("--exclude", multiple=True, help="File patterns to exclude (can be used multiple times)")
def scan_exception_handlers(
    path: str, output: str | None, verbose: bool, include: tuple[str, ...], exclude: tuple[str, ...]
) -> None:
    """Scan Python code for exception handling patterns.

    Detects try/except/else/finally blocks and analyzes:
    - Exception types caught in each except clause
    - Logging practices (counts by log level)
    - Control flow patterns (pass, return, raise, etc.)
    - Line counts for try/except/else/finally sections

    Examples:

        upcast scan-exception-handlers .

        upcast scan-exception-handlers src/ -o handlers.yaml

        upcast scan-exception-handlers . --include "**/*.py" --exclude "**/tests/**"
    """
    # Convert to Path and resolve
    target_path = Path(path).resolve()

    if verbose:
        click.echo(f"Scanning: {target_path}")

    # Collect Python files
    python_files = collect_python_files(
        target_path,
        include_patterns=include if include else None,
        exclude_patterns=exclude if exclude else None,
    )

    if verbose:
        click.echo(f"Found {len(python_files)} Python files")

    # Create checker and process files
    checker = ExceptionHandlerChecker(target_path)

    for file_path in python_files:
        if verbose:
            click.echo(f"Checking: {file_path.relative_to(target_path)}")
        checker.check_file(file_path)

    # Get results
    handlers = checker.get_handlers()
    summary = checker.get_summary()

    if verbose:
        click.echo(f"\nFound {len(handlers)} exception handlers")
        click.echo(f"Total except clauses: {summary['total_except_clauses']}")

    # Export results
    format_type = "json" if output and output.endswith(".json") else "yaml"
    result = export_exception_handlers(handlers, summary, output, format_type)

    # Print to stdout if no output file specified
    if not output:
        click.echo(result)
    elif verbose:
        click.echo(f"\nOutput written to: {output}")
