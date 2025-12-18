"""CLI for blocking operation scanner."""

import logging
from pathlib import Path

import click

from upcast.blocking_operation_scanner.checker import BlockingOperationChecker
from upcast.blocking_operation_scanner.export import export_to_json, export_to_yaml
from upcast.common.file_utils import collect_python_files, find_package_root

logger = logging.getLogger(__name__)


@click.command(name="scan-blocking-operations")
@click.argument("path", type=click.Path(exists=True), nargs=-1, required=True)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    help="Output file path (default: stdout)",
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["yaml", "json"]),
    default="yaml",
    help="Output format",
)
@click.option(
    "--include",
    multiple=True,
    help="Include files matching glob pattern (can be used multiple times)",
)
@click.option(
    "--exclude",
    multiple=True,
    help="Exclude files matching glob pattern (can be used multiple times)",
)
@click.option(
    "--no-default-excludes",
    is_flag=True,
    help="Disable default exclusion of common directories",
)
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
def scan_blocking_operations(
    path: tuple[str],
    output: str | None,
    output_format: str,
    include: tuple[str],
    exclude: tuple[str],
    no_default_excludes: bool,
    verbose: bool,
) -> int:
    """Scan Python files for blocking operations.

    Detects blocking operations that may cause performance issues:
    - time.sleep() calls
    - Django ORM select_for_update()
    - threading.Lock().acquire()
    - subprocess.run(), Popen.wait(), Popen.communicate()

    Examples:

        # Scan current directory
        upcast scan-blocking-operations .

        # Scan specific files
        upcast scan-blocking-operations app.py utils.py

        # Save to file
        upcast scan-blocking-operations /path/to/project -o blocking.yaml

        # JSON output
        upcast scan-blocking-operations /path/to/project --format json

        # Filter files
        upcast scan-blocking-operations /path/to/project --include "app/**" --exclude "tests/**"

        # Verbose output
        upcast scan-blocking-operations /path/to/project -v
    """
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Collect Python files
    paths = [Path(p) for p in path]
    all_files = []

    for p in paths:
        files = collect_python_files(
            p,
            include_patterns=list(include) if include else None,
            exclude_patterns=list(exclude) if exclude else None,
            use_default_excludes=not no_default_excludes,
        )
        all_files.extend(files)

    # Remove duplicates and sort
    files = sorted(set(all_files))

    if not files:
        logger.warning("No Python files found to scan")
        # Output empty result instead of error
        result = export_to_yaml([], Path.cwd()) if output_format == "yaml" else export_to_json([], Path.cwd())
        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(result)
        else:
            click.echo(result)
        return 0

    logger.info("Scanning %d files for blocking operations", len(files))

    # Scan files
    checker = BlockingOperationChecker()
    all_operations = []

    for file_path in files:
        logger.debug("Scanning %s", file_path)
        operations = checker.check_file(file_path)
        all_operations.extend(operations)
        if operations:
            logger.debug("Found %d operations in %s", len(operations), file_path)

    logger.info("Found %d blocking operations", len(all_operations))

    # Determine base path for relative paths
    if len(paths) == 1 and paths[0].is_dir():
        base_path = paths[0]
    else:
        # Find common package root
        base_path = find_package_root(paths[0]) if paths else Path.cwd()

    # Export results
    if output_format == "yaml":
        result = export_to_yaml(all_operations, base_path)
    else:
        result = export_to_json(all_operations, base_path)

    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result)
        logger.info("Results written to %s", output)
    else:
        click.echo(result)

    return 0
