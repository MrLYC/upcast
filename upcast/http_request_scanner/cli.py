"""CLI interface for HTTP request scanner."""

from pathlib import Path

import click

from upcast.common.export import export_to_json, export_to_yaml
from upcast.common.file_utils import collect_python_files, validate_path
from upcast.http_request_scanner.checker import HttpRequestChecker
from upcast.http_request_scanner.export import format_request_output


@click.command()
@click.argument("path", type=str, default=".")
@click.option("-o", "--output", type=str, help="Output file path")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option("--include", multiple=True, help="File patterns to include (glob)")
@click.option("--exclude", multiple=True, help="File patterns to exclude (glob)")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["yaml", "json"]),
    default="yaml",
    help="Output format",
)
def scan_http_requests(
    path: str,
    output: str | None,
    verbose: bool,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    output_format: str,
) -> None:
    """Scan Python code for HTTP/API requests.

    Detects requests made via requests, httpx, aiohttp, urllib3, urllib.request,
    and http.client libraries.

    Examples:

        upcast scan-http-requests .

        upcast scan-http-requests src/ -o requests.yaml

        upcast scan-http-requests . --include "*/api/*.py" --format json
    """
    # Validate and resolve path
    scan_path = validate_path(Path(path).resolve())

    # Collect Python files
    if scan_path.is_file():
        files = [scan_path]
    else:
        files = collect_python_files(
            scan_path,
            include_patterns=list(include) if include else None,
            exclude_patterns=list(exclude) if exclude else None,
        )

    if verbose:
        click.echo(f"Scanning {len(files)} files...")

    # Process files
    checker = HttpRequestChecker(scan_path if scan_path.is_dir() else scan_path.parent)
    for file_path in files:
        if verbose:
            click.echo(f"Processing {file_path}")
        checker.check_file(file_path)

    # Get results
    requests_by_url = checker.get_requests_by_url()
    summary = checker.get_summary()

    # Format output
    result = format_request_output(requests_by_url, summary)

    # Export
    if output:
        output_path = Path(output)
        if output_format == "yaml":
            export_to_yaml(result, output_path)
        else:
            export_to_json(result, output_path)
        if verbose:
            click.echo(f"Results written to {output}")
    else:
        # Print to stdout
        if output_format == "yaml":
            import yaml

            click.echo(yaml.dump(result, allow_unicode=True, default_flow_style=False, indent=2))
        else:
            import json

            click.echo(json.dumps(result, indent=2, ensure_ascii=False))
