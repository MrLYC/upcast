"""Common CLI utilities for scanners.

This module provides reusable CLI components for all scanners, including:
- Standard argument definitions
- Common command execution logic
- Output formatting and export
"""

import sys
from pathlib import Path
from typing import Any

import click

from upcast.common.export import export_to_json, export_to_yaml, export_to_yaml_string
from upcast.common.file_utils import collect_python_files
from upcast.common.scanner_base import BaseScanner
from upcast.models.base import ScannerOutput


def add_scanner_arguments(func):
    """Decorator to add standard scanner CLI arguments.

    Adds the following options to a Click command:
    - -o/--output: Output file path
    - --format: Output format (yaml/json/markdown)
    - --markdown-language: Language for markdown output
    - --markdown-title: Title for markdown output
    - --include: File patterns to include (multiple)
    - --exclude: File patterns to exclude (multiple)
    - --no-default-excludes: Disable default exclusions
    - -v/--verbose: Enable verbose output

    Args:
        func: Click command function to decorate

    Returns:
        Decorated function with standard arguments added
    """
    func = click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")(func)
    func = click.option(
        "--no-default-excludes",
        is_flag=True,
        help="Disable default exclusions (venv, migrations, etc.)",
    )(func)
    func = click.option(
        "--exclude",
        multiple=True,
        help="File patterns to exclude (can be specified multiple times)",
    )(func)
    func = click.option(
        "--include",
        multiple=True,
        help="File patterns to include (can be specified multiple times)",
    )(func)
    func = click.option(
        "--markdown-title",
        type=str,
        help="Title for markdown output (only used when format is markdown)",
    )(func)
    func = click.option(
        "--markdown-language",
        type=click.Choice(["en", "zh"], case_sensitive=False),
        default="en",
        help="Language for markdown output (default: en)",
    )(func)

    format_choice = click.Choice(["yaml", "json", "markdown", "html"], case_sensitive=False)
    format_choice.choices = ["yaml", "json", "markdown", "html"]
    func = click.option(
        "--format",
        type=format_choice,
        default="yaml",
        help="Output format (default: yaml)",
    )(func)
    func = click.option("-o", "--output", type=click.Path(), help="Output file path")(func)

    return func


def create_scanner_parser(name: str, description: str, examples: list[str] | None = None) -> click.Command:
    """Create a standard scanner command parser.

    Args:
        name: Scanner name (e.g., "signals", "django-models")
        description: Short description of what the scanner does
        examples: Optional list of usage examples

    Returns:
        Click Command configured with standard arguments
    """

    @click.command(name=name)
    @click.argument("path", type=click.Path(exists=True), required=False, default=".")
    @add_scanner_arguments
    def scanner_command(**kwargs):
        """Scanner command template."""
        pass

    # Update docstring with description and examples
    doc = description
    if examples:
        doc += "\n\n\\b\nExamples:\n"
        for example in examples:
            doc += f"    {example}\n"

    scanner_command.__doc__ = doc
    return scanner_command


def run_scanner_cli(
    scanner: BaseScanner,
    path: str,
    output: str | None = None,
    format: str = "yaml",  # noqa: A002
    include: tuple[str, ...] = (),
    exclude: tuple[str, ...] = (),
    no_default_excludes: bool = False,
    verbose: bool = False,
    markdown_title: str | None = None,
    markdown_language: str = "en",
) -> None:
    """Execute scanner with common CLI logic.

    This function handles:
    - Path validation
    - File collection with include/exclude patterns
    - Scanner execution
    - Result formatting and export
    - Summary display

    Args:
        scanner: Scanner instance (must extend BaseScanner)
        path: Directory or file to scan
        output: Optional output file path
        format: Output format ("yaml", "json", or "markdown")
        include: File patterns to include
        exclude: File patterns to exclude
        no_default_excludes: Whether to disable default exclusions
        verbose: Enable verbose output
        markdown_title: Title for markdown output (only used when format is "markdown")
        markdown_language: Language for markdown output (default: "en")

    Raises:
        SystemExit: If path doesn't exist or no files found
    """
    scan_path = Path(path).resolve()

    # Validate path
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

    # Execute scan
    scanner_output = scanner.scan(scan_path)

    # Validate output type
    if not isinstance(scanner_output, ScannerOutput):
        raise TypeError(f"Scanner must return ScannerOutput, got {type(scanner_output)}")

    # Use Pydantic model serialization
    # Note: Keep None values for critical fields (e.g., view_module, view_name in Django URLs)
    formatted_data = scanner_output.model_dump(mode="json", exclude_none=False)

    if output:
        _write_output_file(
            scanner=scanner,
            scanner_output=scanner_output,
            formatted_data=formatted_data,
            output=output,
            format=format,
            markdown_title=markdown_title,
            markdown_language=markdown_language,
        )
    else:
        _print_output_to_stdout(
            scanner=scanner,
            scanner_output=scanner_output,
            formatted_data=formatted_data,
            format=format,
            markdown_title=markdown_title,
            markdown_language=markdown_language,
        )

    # Print summary
    if verbose:
        _print_summary(scanner_output, verbose)


def _get_markdown_title(scanner: BaseScanner, markdown_title: str | None) -> str:
    if markdown_title is not None:
        return markdown_title

    scanner_name = scanner.__class__.__name__.replace("Scanner", "")
    return f"{scanner_name} Analysis"


def _write_output_file(
    *,
    scanner: BaseScanner,
    scanner_output: ScannerOutput,
    formatted_data: dict[str, Any],
    output: str,
    format: str,  # noqa: A002
    markdown_title: str | None,
    markdown_language: str,
) -> None:
    fmt = format.lower()
    if fmt == "json":
        export_to_json(formatted_data, output)
        click.echo(f"Results written to: {output}")
        return

    if fmt == "markdown":
        from upcast.render import render_to_file

        render_to_file(
            scanner_output,
            output,
            language=markdown_language,
            title=_get_markdown_title(scanner, markdown_title),
            format="markdown",
        )
        click.echo(f"Markdown report written to: {output}")
        return

    if fmt == "html":
        from upcast.render import render_to_file

        render_to_file(
            scanner_output,
            output,
            language=markdown_language,
            title=_get_markdown_title(scanner, markdown_title),
            format="html",
        )
        click.echo(f"HTML report written to: {output}")
        return

    export_to_yaml(formatted_data, output)
    click.echo(f"Results written to: {output}")


def _print_output_to_stdout(
    *,
    scanner: BaseScanner,
    scanner_output: ScannerOutput,
    formatted_data: dict[str, Any],
    format: str,  # noqa: A002
    markdown_title: str | None,
    markdown_language: str,
) -> None:
    fmt = format.lower()
    if fmt == "json":
        import json

        click.echo(json.dumps(formatted_data, indent=2))
        return

    if fmt == "markdown":
        from upcast.render import render_to_markdown

        markdown_output = render_to_markdown(
            scanner_output,
            language=markdown_language,
            title=_get_markdown_title(scanner, markdown_title),
        )
        click.echo(markdown_output)
        return

    if fmt == "html":
        from upcast.render import render_to_html

        html_output = render_to_html(
            scanner_output,
            language=markdown_language,
            title=_get_markdown_title(scanner, markdown_title),
        )
        click.echo(html_output)
        return

    click.echo(export_to_yaml_string(formatted_data))


def _print_summary(scanner_output: ScannerOutput, verbose: bool) -> None:
    """Print summary statistics.

    Args:
        scanner_output: Scanner output containing summary
        verbose: Whether to show detailed summary
    """
    summary = scanner_output.summary

    click.echo("\n" + "=" * 50)
    click.echo("Summary:")
    click.echo("=" * 50)
    click.echo(f"Total items found: {summary.total_count}")
    click.echo(f"Files scanned: {summary.files_scanned}")

    if summary.scan_duration_ms is not None:
        duration_sec = summary.scan_duration_ms / 1000.0
        click.echo(f"Scan duration: {duration_sec:.2f}s")

    # Print scanner-specific metadata if available
    if verbose and scanner_output.metadata:
        click.echo("\nMetadata:")
        for key, value in scanner_output.metadata.items():
            click.echo(f"  {key}: {value}")


def handle_scan_error(error: Exception, verbose: bool = False) -> None:
    """Handle scanner errors with consistent formatting.

    Args:
        error: Exception that occurred
        verbose: Whether to show detailed error information
    """
    click.echo(f"Error during scan: {error}", err=True)
    if verbose:
        import traceback

        click.echo("\nFull traceback:", err=True)
        click.echo(traceback.format_exc(), err=True)
    sys.exit(1)


def validate_scanner_arguments(
    include: tuple[str, ...] | None = None,
    exclude: tuple[str, ...] | None = None,
    format: str = "yaml",  # noqa: A002
) -> dict[str, Any]:
    """Validate and normalize scanner CLI arguments.

    Args:
        include: File patterns to include
        exclude: File patterns to exclude
        format: Output format

    Returns:
        Dictionary of validated arguments

    Raises:
        click.BadParameter: If arguments are invalid
    """
    validated = {}

    # Validate format
    if format.lower() not in ["yaml", "json", "markdown", "html"]:
        raise click.BadParameter(
            f"Invalid format '{format}'. Must be 'yaml', 'json', 'markdown', or 'html'.",
            param_hint="--format",
        )
    validated["format"] = format.lower()

    # Normalize patterns
    validated["include_patterns"] = list(include) if include else None
    validated["exclude_patterns"] = list(exclude) if exclude else None

    return validated
