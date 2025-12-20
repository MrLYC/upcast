"""CLI interface for signal scanner."""

import sys
from pathlib import Path

import click
import yaml

from upcast.common.file_utils import collect_python_files
from upcast.signal_scanner.checker import SignalChecker
from upcast.signal_scanner.export import export_to_yaml, format_signal_output


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
@click.option(
    "--no-default-excludes",
    is_flag=True,
    help="Disable default exclusions (venv, migrations, etc.)",
)
def scan_signals(
    path: str,
    output: str | None,
    verbose: bool,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan for Django and Celery signal usage.

    Detects signal handlers, custom signal definitions, and signal registrations
    in Python codebases using Django and Celery.

    PATH: Directory or file to scan (defaults to current directory)

    \b
    Examples:
        upcast scan-signals .
        upcast scan-signals /app --include "**/signals/**"
        upcast scan-signals . -o signals.yaml --verbose
        upcast scan-signals /project --exclude "**/tests/**"
    """
    scan_path = Path(path).resolve()

    if not scan_path.exists():
        click.echo(f"Error: Path '{path}' does not exist", err=True)
        sys.exit(1)

    # Collect Python files
    python_files = collect_python_files(
        scan_path,
        include_patterns=list(include) if include else None,
        exclude_patterns=list(exclude) if exclude else None,
        use_default_excludes=not no_default_excludes,
    )

    if not python_files:
        click.echo("No Python files found to scan", err=True)
        sys.exit(1)

    if verbose:
        click.echo(f"Scanning {len(python_files)} Python files...")

    # Initialize checker
    checker = SignalChecker(root_path=str(scan_path), verbose=verbose)

    # Scan files
    for file_path in python_files:
        if verbose:
            click.echo(f"  Analyzing: {file_path}")
        checker.check_file(str(file_path))

    # Get results
    results = checker.get_results()

    if not results:
        click.echo("No signal patterns found")
        sys.exit(0)

    # Output results
    if output:
        export_to_yaml(results, output)
        click.echo(f"Results written to: {output}")
    else:
        # Print to stdout
        formatted = format_signal_output(results)
        click.echo(yaml.dump(formatted, default_flow_style=False, sort_keys=False))

    # Print summary
    summary = checker.get_summary()
    _print_summary(summary, verbose)


def _print_summary(summary: dict, verbose: bool) -> None:
    """Print summary statistics.

    Args:
        summary: Summary dictionary from checker
        verbose: Whether to show detailed summary
    """
    if not summary:
        return

    click.echo("\n" + "=" * 50)
    click.echo("Summary:")
    click.echo("=" * 50)

    if "django_handlers" in summary:
        click.echo(f"Django signal handlers: {summary['django_handlers']}")

    if "celery_handlers" in summary:
        click.echo(f"Celery signal handlers: {summary['celery_handlers']}")

    if "custom_signals_defined" in summary:
        click.echo(f"Custom signals defined: {summary['custom_signals_defined']}")

    if verbose:
        total = summary.get("django_handlers", 0) + summary.get("celery_handlers", 0)
        click.echo(f"Total signal handlers: {total}")
