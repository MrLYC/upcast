"""CLI for cyclomatic complexity scanner."""

from pathlib import Path

import click

from upcast.common.file_utils import collect_python_files, validate_path
from upcast.cyclomatic_complexity_scanner.checker import ComplexityChecker
from upcast.cyclomatic_complexity_scanner.export import format_results


@click.command(name="scan-complexity")
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--threshold",
    type=int,
    default=11,
    help="Minimum complexity to report (default: 11)",
)
@click.option(
    "--include-tests",
    is_flag=True,
    help="Include test files (default: excluded)",
)
@click.option(
    "--include",
    multiple=True,
    help="Include file patterns (glob)",
)
@click.option(
    "--exclude",
    multiple=True,
    help="Exclude file patterns (glob)",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    help="Output file path (default: stdout)",
)
@click.option(
    "--format",
    "format_type",
    type=click.Choice(["yaml", "json"]),
    default="yaml",
    help="Output format (default: yaml)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Verbose output",
)
def scan_complexity(
    path: str,
    threshold: int,
    include_tests: bool,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    output: str | None,
    format_type: str,
    verbose: bool,
) -> None:
    """Scan Python files for high cyclomatic complexity.

    Analyzes functions and methods to identify code that may need refactoring
    based on cyclomatic complexity metrics.

    PATH: File or directory to scan

    Examples:

        # Scan current directory with default threshold
        upcast scan-complexity .

        # Scan with custom threshold
        upcast scan-complexity . --threshold 15

        # Include test files
        upcast scan-complexity . --include-tests

        # Save results to file
        upcast scan-complexity . -o complexity-report.yaml

        # Output JSON format
        upcast scan-complexity . --format json
    """
    try:
        # Validate path
        scan_path = validate_path(path)

        # Collect Python files
        include_patterns = list(include) if include else None
        exclude_patterns = list(exclude) if exclude else None

        python_files = collect_python_files(
            scan_path,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            use_default_excludes=not include_tests,
        )

        if verbose:
            click.echo(f"Found {len(python_files)} Python files to analyze", err=True)

        # Create checker
        checker = ComplexityChecker(
            threshold=threshold,
            include_tests=include_tests,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
        )

        # Determine base path for relative paths
        base_path = str(scan_path) if scan_path.is_dir() else str(scan_path.parent)

        # Check files
        file_paths = [str(f) for f in python_files]
        results = checker.check_files(file_paths, base_path=base_path)

        if verbose:
            total_high_complexity = sum(len(r) for r in results.values())
            click.echo(
                f"Found {total_high_complexity} functions with complexity >= {threshold}",
                err=True,
            )

        # Format results
        formatted_output = format_results(results, format_type=format_type)

        # Output results
        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(formatted_output, encoding="utf-8")
            if verbose:
                click.echo(f"Results written to {output}", err=True)
        else:
            click.echo(formatted_output)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort() from e


if __name__ == "__main__":
    scan_complexity()
