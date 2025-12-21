import sys
from typing import Optional

import click

from upcast.common.cli import run_scanner_cli
from upcast.django_model_scanner import scan_django_models
from upcast.django_settings_scanner import scan_django_settings
from upcast.django_url_scanner import scan_django_urls
from upcast.scanners import (
    BlockingOperationsScanner,
    ComplexityScanner,
    ConcurrencyScanner,
    DjangoUrlScanner,
    EnvVarScanner,
    ExceptionHandlerScanner,
    HttpRequestsScanner,
    MetricsScanner,
    UnitTestScanner,
)
from upcast.unit_test_scanner.cli import scan_unit_tests


@click.group()
def main():
    pass


@main.command(name="scan-complexity")
@click.option("-o", "--output", default=None, type=click.Path(), help="Output file path")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option(
    "--format",
    type=click.Choice(["yaml", "json"], case_sensitive=False),
    default="yaml",
    help="Output format (yaml or json)",
)
@click.option("--threshold", type=int, default=11, help="Minimum complexity to report (default: 11)")
@click.option("--include", multiple=True, help="Glob patterns for files to include")
@click.option("--exclude", multiple=True, help="Glob patterns for files to exclude")
@click.option("--no-default-excludes", is_flag=True, help="Disable default exclude patterns")
@click.argument("path", type=click.Path(exists=True), default=".", required=False)
def scan_complexity_cmd(
    output: Optional[str],
    verbose: bool,
    format: str,  # noqa: A002
    threshold: int,
    path: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan Python files for high cyclomatic complexity.

    Analyzes functions to identify code that may need refactoring.
    """
    try:
        scanner = ComplexityScanner(
            threshold=threshold,
            include_patterns=list(include) if include else None,
            exclude_patterns=list(exclude) if exclude else None,
            verbose=verbose,
        )
        run_scanner_cli(
            scanner=scanner,
            path=path,
            output=output,
            format=format,
            include=include,
            exclude=exclude,
            no_default_excludes=no_default_excludes,
            verbose=verbose,
        )
    except Exception as e:
        from upcast.common.cli import handle_scan_error

        handle_scan_error(e, verbose=verbose)


@main.command(name="scan-env-vars")
@click.option("-o", "--output", default=None, type=click.Path(), help="Output file path")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option(
    "--format",
    type=click.Choice(["yaml", "json"], case_sensitive=False),
    default="yaml",
    help="Output format (yaml or json)",
)
@click.option("--include", multiple=True, help="Glob patterns for files to include")
@click.option("--exclude", multiple=True, help="Glob patterns for files to exclude")
@click.option("--no-default-excludes", is_flag=True, help="Disable default exclude patterns")
@click.argument("path", type=click.Path(exists=True), default=".", required=False)
def scan_env_vars_cmd(
    output: Optional[str],
    verbose: bool,
    format: str,  # noqa: A002
    path: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan Python files for environment variable usage.

    PATH can be a Python file or directory.
    Results are aggregated by environment variable name.
    """
    try:
        scanner = EnvVarScanner(
            include_patterns=list(include) if include else None,
            exclude_patterns=list(exclude) if exclude else None,
            verbose=verbose,
        )
        run_scanner_cli(
            scanner=scanner,
            path=path,
            output=output,
            format=format,
            include=include,
            exclude=exclude,
            no_default_excludes=no_default_excludes,
            verbose=verbose,
        )
    except Exception as e:
        from upcast.common.cli import handle_scan_error

        handle_scan_error(e, verbose=verbose)


@main.command(name="scan-blocking-operations")
@click.option("-o", "--output", default=None, type=click.Path(), help="Output file path")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option(
    "--format",
    type=click.Choice(["yaml", "json"], case_sensitive=False),
    default="yaml",
    help="Output format (yaml or json)",
)
@click.option("--include", multiple=True, help="Glob patterns for files to include")
@click.option("--exclude", multiple=True, help="Glob patterns for files to exclude")
@click.option("--no-default-excludes", is_flag=True, help="Disable default exclude patterns")
@click.argument("path", type=click.Path(exists=True), default=".", required=False)
def scan_blocking_operations_cmd(
    output: Optional[str],
    verbose: bool,
    format: str,  # noqa: A002
    path: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan for blocking operations (sleep, locks, subprocess, DB queries)."""
    try:
        scanner = BlockingOperationsScanner(
            include_patterns=list(include) if include else None,
            exclude_patterns=list(exclude) if exclude else None,
            verbose=verbose,
        )
        run_scanner_cli(
            scanner=scanner,
            path=path,
            output=output,
            format=format,
            include=include,
            exclude=exclude,
            no_default_excludes=no_default_excludes,
            verbose=verbose,
        )
    except Exception as e:
        from upcast.common.cli import handle_scan_error

        handle_scan_error(e, verbose=verbose)


@main.command(name="scan-http-requests")
@click.option("-o", "--output", default=None, type=click.Path(), help="Output file path")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option(
    "--format",
    type=click.Choice(["yaml", "json"], case_sensitive=False),
    default="yaml",
    help="Output format (yaml or json)",
)
@click.option("--include", multiple=True, help="Glob patterns for files to include")
@click.option("--exclude", multiple=True, help="Glob patterns for files to exclude")
@click.option("--no-default-excludes", is_flag=True, help="Disable default exclude patterns")
@click.argument("path", type=click.Path(exists=True), default=".", required=False)
def scan_http_requests_cmd(
    output: Optional[str],
    verbose: bool,
    format: str,  # noqa: A002
    path: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan for HTTP request patterns (requests, httpx, aiohttp)."""
    try:
        scanner = HttpRequestsScanner(
            include_patterns=list(include) if include else None,
            exclude_patterns=list(exclude) if exclude else None,
            verbose=verbose,
        )
        run_scanner_cli(
            scanner=scanner,
            path=path,
            output=output,
            format=format,
            include=include,
            exclude=exclude,
            no_default_excludes=no_default_excludes,
            verbose=verbose,
        )
    except Exception as e:
        from upcast.common.cli import handle_scan_error

        handle_scan_error(e, verbose=verbose)


@main.command(name="scan-metrics")
@click.option("-o", "--output", default=None, type=click.Path(), help="Output file path")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option(
    "--format",
    type=click.Choice(["yaml", "json"], case_sensitive=False),
    default="yaml",
    help="Output format (yaml or json)",
)
@click.option("--include", multiple=True, help="Glob patterns for files to include")
@click.option("--exclude", multiple=True, help="Glob patterns for files to exclude")
@click.option("--no-default-excludes", is_flag=True, help="Disable default exclude patterns")
@click.argument("path", type=click.Path(exists=True), default=".", required=False)
def scan_metrics_cmd(
    output: Optional[str],
    verbose: bool,
    format: str,  # noqa: A002
    path: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan for Prometheus metrics (Counter, Gauge, Histogram, Summary)."""
    try:
        scanner = MetricsScanner(
            include_patterns=list(include) if include else None,
            exclude_patterns=list(exclude) if exclude else None,
            verbose=verbose,
        )
        run_scanner_cli(
            scanner=scanner,
            path=path,
            output=output,
            format=format,
            include=include,
            exclude=exclude,
            no_default_excludes=no_default_excludes,
            verbose=verbose,
        )
    except Exception as e:
        from upcast.common.cli import handle_scan_error

        handle_scan_error(e, verbose=verbose)


@main.command(name="scan-concurrency")
@click.option("-o", "--output", default=None, type=click.Path(), help="Output file path")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option(
    "--format",
    type=click.Choice(["yaml", "json"], case_sensitive=False),
    default="yaml",
    help="Output format (yaml or json)",
)
@click.option("--include", multiple=True, help="Glob patterns for files to include")
@click.option("--exclude", multiple=True, help="Glob patterns for files to exclude")
@click.option("--no-default-excludes", is_flag=True, help="Disable default exclude patterns")
@click.argument("path", type=click.Path(exists=True), default=".", required=False)
def scan_concurrency_cmd(
    output: Optional[str],
    verbose: bool,
    format: str,  # noqa: A002
    path: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan for concurrency patterns (threading, multiprocessing, asyncio)."""
    try:
        scanner = ConcurrencyScanner(
            include_patterns=list(include) if include else None,
            exclude_patterns=list(exclude) if exclude else None,
            verbose=verbose,
        )
        run_scanner_cli(
            scanner=scanner,
            path=path,
            output=output,
            format=format,
            include=include,
            exclude=exclude,
            no_default_excludes=no_default_excludes,
            verbose=verbose,
        )
    except Exception as e:
        from upcast.common.cli import handle_scan_error

        handle_scan_error(e, verbose=verbose)


@main.command(name="scan-exception-handlers")
@click.option("-o", "--output", default=None, type=click.Path(), help="Output file path")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option(
    "--format",
    type=click.Choice(["yaml", "json"], case_sensitive=False),
    default="yaml",
    help="Output format (yaml or json)",
)
@click.option("--include", multiple=True, help="Glob patterns for files to include")
@click.option("--exclude", multiple=True, help="Glob patterns for files to exclude")
@click.option("--no-default-excludes", is_flag=True, help="Disable default exclude patterns")
@click.argument("path", type=click.Path(exists=True), default=".", required=False)
def scan_exception_handlers_cmd(
    output: Optional[str],
    verbose: bool,
    format: str,  # noqa: A002
    path: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan for exception handlers (try/except/else/finally)."""
    try:
        scanner = ExceptionHandlerScanner(
            include_patterns=list(include) if include else None,
            exclude_patterns=list(exclude) if exclude else None,
            verbose=verbose,
        )
        run_scanner_cli(
            scanner=scanner,
            path=path,
            output=output,
            format=format,
            include=include,
            exclude=exclude,
            no_default_excludes=no_default_excludes,
            verbose=verbose,
        )
    except Exception as e:
        from upcast.common.cli import handle_scan_error

        handle_scan_error(e, verbose=verbose)


@main.command(name="scan-unit-tests")
@click.option("-o", "--output", type=click.Path(), help="Output file path (YAML or JSON)")
@click.option(
    "--format",
    type=click.Choice(["yaml", "json"], case_sensitive=False),
    default="yaml",
    help="Output format (default: yaml)",
)
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging")
@click.option("--include", multiple=True, help="File patterns to include (e.g., 'test_*.py')")
@click.option("--exclude", multiple=True, help="File patterns to exclude (e.g., '__pycache__/**')")
@click.option("--no-default-excludes", is_flag=True, help="Disable default exclude patterns")
@click.option(
    "-r",
    "--root-modules",
    multiple=True,
    help="Root module prefixes for target resolution (e.g., 'app', 'mylib')",
)
@click.argument("path", type=click.Path(exists=True), default=".")
def scan_unit_tests_new_cmd(
    path: str,
    root_modules: tuple[str, ...],
    output: str | None,
    output_format: str,
    verbose: bool,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan Python code for unit tests.

    Detects pytest and unittest test functions, calculates MD5 hashes,
    counts assertions, and resolves test targets based on root modules.

    PATH: Directory or file to scan (defaults to current directory)

    Examples:

        \b
        # Scan tests directory
        upcast scan-unit-tests ./tests

        \b
        # Scan with specific root module
        upcast scan-unit-tests ./tests --root-modules app

        \b
        # Scan with multiple root modules
        upcast scan-unit-tests ./tests -r app -r mylib -v

        \b
        # Save results to JSON file
        upcast scan-unit-tests ./tests --output results.json --format json
    """

    try:
        scanner = UnitTestScanner(
            root_modules=list(root_modules) if root_modules else None,
            include_patterns=list(include) if include else None,
            exclude_patterns=list(exclude) if exclude else None,
            verbose=verbose,
        )

        run_scanner_cli(
            scanner=scanner,
            path=path,
            output=output,
            format=output_format,
            verbose=verbose,
        )

    except Exception as e:
        from upcast.common.cli import handle_scan_error

        handle_scan_error(e, verbose=verbose)


@main.command(name="scan-django-urls-new")
@click.option("-o", "--output", type=click.Path(), help="Output file path (YAML or JSON)")
@click.option(
    "--format",
    type=click.Choice(["yaml", "json"], case_sensitive=False),
    default="yaml",
    help="Output format (default: yaml)",
)
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging")
@click.option("--include", multiple=True, help="File patterns to include (e.g., '**/urls.py')")
@click.option("--exclude", multiple=True, help="File patterns to exclude")
@click.option("--no-default-excludes", is_flag=True, help="Disable default exclude patterns")
@click.argument("path", type=click.Path(exists=True), default=".")
def scan_django_urls_new_cmd(
    path: str,
    output: str | None,
    output_format: str,
    verbose: bool,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan Django URLconf files for URL patterns.

    Detects path(), re_path(), include(), and DRF router registrations.

    PATH: Directory or file to scan (defaults to current directory)

    Examples:

        \b
        # Scan for Django URLs
        upcast scan-django-urls-new ./myproject

        \b
        # Scan specific urls.py file
        upcast scan-django-urls-new myapp/urls.py

        \b
        # Save results to JSON file
        upcast scan-django-urls-new ./myproject --output urls.json --format json
    """

    try:
        scanner = DjangoUrlScanner(
            include_patterns=list(include) if include else None,
            exclude_patterns=list(exclude) if exclude else None,
            verbose=verbose,
        )

        run_scanner_cli(
            scanner=scanner,
            path=path,
            output=output,
            format=output_format,
            verbose=verbose,
        )

    except Exception as e:
        from upcast.common.cli import handle_scan_error

        handle_scan_error(e, verbose=verbose)


@main.command(name="scan-django-models")
@click.option("-o", "--output", default=None, type=click.Path())
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option("--include", multiple=True, help="Glob patterns for files to include")
@click.option("--exclude", multiple=True, help="Glob patterns for files to exclude")
@click.option("--no-default-excludes", is_flag=True, help="Disable default exclude patterns")
@click.argument("path", type=click.Path(exists=True))
def scan_django_models_cmd(
    output: Optional[str],
    verbose: bool,
    path: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan Python files for Django model definitions.

    PATH can be a Python file or directory containing Django models.
    """
    try:
        result = scan_django_models(
            path,
            output=output,
            verbose=verbose,
            include_patterns=list(include) if include else None,
            exclude_patterns=list(exclude) if exclude else None,
            use_default_excludes=not no_default_excludes,
        )

        # If no output file specified, print to stdout
        if not output and result:
            click.echo(result)

        if verbose:
            click.echo("Analysis complete!", err=True)

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


@main.command(name="scan-django-urls")
@click.option("-o", "--output", default=None, type=click.Path(), help="Output file path")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option("--include", multiple=True, help="Glob patterns for files to include")
@click.option("--exclude", multiple=True, help="Glob patterns for files to exclude")
@click.option("--no-default-excludes", is_flag=True, help="Disable default exclude patterns")
@click.argument("path", type=click.Path(exists=True))
def scan_django_urls_cmd(
    output: Optional[str],
    verbose: bool,
    path: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan Python files for Django URL pattern definitions.

    PATH can be a Python file or directory containing Django URL configurations.
    Results are grouped by module and exported to YAML format.
    """
    try:
        result = scan_django_urls(
            path,
            output=output,
            verbose=verbose,
            include_patterns=list(include) if include else None,
            exclude_patterns=list(exclude) if exclude else None,
            use_default_excludes=not no_default_excludes,
        )

        # If no output file specified, print to stdout
        if not output and result:
            click.echo(result)

        if verbose:
            click.echo("Scan complete!", err=True)

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


@main.command(name="scan-django-settings")
@click.option("-o", "--output", default=None, type=click.Path(), help="Output file path")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option("--include", multiple=True, help="Glob patterns for files to include")
@click.option("--exclude", multiple=True, help="Glob patterns for files to exclude")
@click.option("--no-default-excludes", is_flag=True, help="Disable default exclude patterns")
@click.option("--definitions-only", is_flag=True, help="Only scan and output settings definitions")
@click.option("--usages-only", is_flag=True, help="Only scan and output settings usages (default)")
@click.option("--combined", "combined_output", is_flag=True, help="Output both definitions and usages")
@click.option("--no-usages", is_flag=True, help="Skip usage scanning (only scan definitions, faster)")
@click.option("--no-definitions", is_flag=True, help="Skip definition scanning (only scan usages, default behavior)")
@click.argument("path", type=click.Path(exists=True))
def scan_django_settings_cmd(  # noqa: C901
    output: Optional[str],
    verbose: bool,
    path: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
    definitions_only: bool,
    usages_only: bool,
    combined_output: bool,
    no_usages: bool,
    no_definitions: bool,
) -> None:
    """Scan Django project for settings usage and/or definitions.

    PATH can be a Python file or directory containing Django code.
    Results are aggregated by settings variable name and exported to YAML format.

    Output modes:

    - Default: Scan and output both definitions and usages (combined mode)

    - --definitions-only: Scan and output only settings definitions

    - --usages-only: Scan and output only settings usages

    - --combined: Explicitly request combined output (same as default)

    - --no-usages: Skip usage scanning (only scan definitions)

    - --no-definitions: Skip definition scanning (only scan usages)
    """
    try:
        # Determine what to scan
        # Default: scan both definitions and usages (combined mode)
        scan_defs = True
        scan_uses = True

        if definitions_only:
            scan_defs = True
            scan_uses = False
        elif usages_only:
            scan_defs = False
            scan_uses = True
        elif no_usages:
            scan_defs = True
            scan_uses = False
        elif no_definitions:
            scan_defs = False
            scan_uses = True
        # else: keep default (both True)

        # Determine output mode
        output_mode = "auto"
        if definitions_only:
            output_mode = "definitions"
        elif usages_only:
            output_mode = "usages"
        else:
            # Default or explicit combined
            output_mode = "combined"

        scan_django_settings(
            path,
            output=output,
            verbose=verbose,
            include_patterns=list(include) if include else None,
            exclude_patterns=list(exclude) if exclude else None,
            use_default_excludes=not no_default_excludes,
            scan_definitions=scan_defs,
            scan_usages=scan_uses,
            output_mode=output_mode,
        )

        if verbose:
            click.echo("Scan complete!", err=True)

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


@main.command(name="scan-signals")
@click.argument("path", type=click.Path(exists=True), required=False, default=".")
@click.option("-o", "--output", type=click.Path(), help="Output file path (YAML or JSON)")
@click.option(
    "--format",
    type=click.Choice(["yaml", "json"], case_sensitive=False),
    default="yaml",
    help="Output format (yaml or json)",
)
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
def scan_signals_cmd(
    path: str,
    output: Optional[str],
    format: str,  # noqa: A002
    verbose: bool,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan for Django and Celery signal usage.

    Detects signal handlers, custom signal definitions, and signal sends
    in Python codebases using Django and Celery. Results are grouped by framework
    (django/celery) and signal type, exported to YAML or JSON format.

    PATH: Directory or file to scan (defaults to current directory)

    Examples:

        \b
        # Scan current directory
        upcast scan-signals

        \b
        # Scan specific directory with verbose output
        upcast scan-signals ./src -v

        \b
        # Save results to YAML file
        upcast scan-signals ./src -o signals.yaml

        \b
        # Save results to JSON file
        upcast scan-signals ./src -o signals.json --format json

        \b
        # Include only signal files
        upcast scan-signals ./src --include "**/signals/**"

        \b
        # Exclude test files
        upcast scan-signals ./src --exclude "**/tests/**"
    """
    try:
        # Import new scanner
        from upcast.common.cli import run_scanner_cli
        from upcast.scanners.signals import SignalScanner

        # Create scanner
        scanner = SignalScanner(
            include_patterns=list(include) if include else None,
            exclude_patterns=list(exclude) if exclude else None,
            verbose=verbose,
        )

        # Run scanner with common CLI logic
        run_scanner_cli(
            scanner=scanner,
            path=path,
            output=output,
            format=format,
            include=include,
            exclude=exclude,
            no_default_excludes=no_default_excludes,
            verbose=verbose,
        )

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


@main.command(name="scan-unit-tests")
@click.argument("path", type=click.Path(exists=True), required=False, default=".")
@click.option(
    "-r",
    "--root-modules",
    multiple=True,
    help="Root modules to match (can be specified multiple times, default: collect all imports)",
)
@click.option("-o", "--output", type=click.Path(), help="Output file path (YAML or JSON)")
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
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["yaml", "json"]),
    default="yaml",
    help="Output format (yaml or json)",
)
def scan_unit_tests_cmd(
    path: str,
    root_modules: tuple[str, ...],
    output: Optional[str],
    verbose: bool,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
    output_format: str,
) -> None:
    """Scan Python code for unit tests.

    Detects pytest and unittest test functions, calculates MD5 hashes,
    counts assertions, and resolves test targets based on root modules.
    Results are exported to YAML or JSON format with relative file paths.

    PATH: Directory or file to scan (defaults to current directory)

    Examples:

        \b
        # Scan tests directory (collect all imports)
        upcast scan-unit-tests ./tests

        \b
        # Scan with specific root module
        upcast scan-unit-tests ./tests --root-modules app

        \b
        # Scan with multiple root modules
        upcast scan-unit-tests ./tests -r app -r mylib -r utils -v

        \b
        # Save results to file
        upcast scan-unit-tests ./tests --root-modules app -o tests.yaml

        \b
        # Output as JSON
        upcast scan-unit-tests ./tests --root-modules app --format json

        \b
        # Include only specific test files
        upcast scan-unit-tests ./tests --root-modules app --include "test_*.py"

        \b
        # Exclude integration tests
        upcast scan-unit-tests ./tests --root-modules app --exclude "**/integration/**"
    """
    try:
        # Convert root_modules tuple to list (None if empty)
        root_modules_list = list(root_modules) if root_modules else None

        # Call scan_unit_tests
        scan_unit_tests(
            path=path,
            root_modules=root_modules_list,
            output=output,
            output_format=output_format,
            include=list(include) if include else None,
            exclude=list(exclude) if exclude else None,
            no_default_excludes=no_default_excludes,
            verbose=verbose,
        )

        if verbose:
            click.echo("Scan complete!", err=True)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
