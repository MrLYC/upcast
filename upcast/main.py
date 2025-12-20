import sys
from typing import Optional

import click

from upcast.blocking_operation_scanner.cli import scan_blocking_operations
from upcast.concurrency_pattern_scanner.cli import scan_concurrency_patterns
from upcast.cyclomatic_complexity_scanner.cli import scan_complexity
from upcast.django_model_scanner import scan_django_models
from upcast.django_settings_scanner import scan_django_settings
from upcast.django_url_scanner import scan_django_urls
from upcast.env_var_scanner.cli import scan_directory, scan_files
from upcast.env_var_scanner.export import export_to_json, export_to_yaml
from upcast.exception_handler_scanner.cli import scan_exception_handlers
from upcast.http_request_scanner.cli import scan_http_requests
from upcast.prometheus_metrics_scanner import scan_prometheus_metrics
from upcast.signal_scanner.cli import scan_signals
from upcast.unit_test_scanner.cli import scan_unit_tests


@click.group()
def main():
    pass


# Register scan-complexity command
main.add_command(scan_complexity)


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
@click.argument("path", type=click.Path(exists=True), nargs=-1, required=True)
def scan_env_vars_cmd(  # noqa: C901
    output: Optional[str],
    verbose: bool,
    format: str,  # noqa: A002
    path: tuple[str, ...],
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan Python files for environment variable usage.

    PATH can be one or more Python files or directories.
    Results are aggregated by environment variable name.
    """
    from pathlib import Path as PathLib

    def _export_results(results: dict, output_format: str) -> str:
        """Export results to the specified format."""
        return export_to_json(results) if output_format.lower() == "json" else export_to_yaml(results)

    def _write_output(result_str: str, output_path: Optional[str], verbose: bool) -> None:
        """Write results to file or stdout."""
        if output_path:
            with open(output_path, "w") as f:
                f.write(result_str)
            if verbose:
                click.echo(f"Results written to {output_path}", err=True)
        else:
            click.echo(result_str)

    try:
        # Prepare filtering parameters
        include_patterns = list(include) if include else None
        exclude_patterns = list(exclude) if exclude else None
        use_default_excludes = not no_default_excludes

        # Separate files and directories
        all_files = []
        for p in path:
            p_obj = PathLib(p)
            if p_obj.is_file():
                all_files.append(str(p))
            elif p_obj.is_dir():
                # Scan directory for Python files with filtering
                checker = scan_directory(
                    str(p),
                    include_patterns=include_patterns,
                    exclude_patterns=exclude_patterns,
                    use_default_excludes=use_default_excludes,
                )
                results = checker.get_results()
                if verbose:
                    click.echo(f"Found {len(results)} environment variables", err=True)

                result_str = _export_results(results, format)
                _write_output(result_str, output, verbose)
                return

        # Scan specific files
        if all_files:
            checker = scan_files(all_files)
            results = checker.get_results()
            if verbose:
                click.echo(f"Found {len(results)} environment variables", err=True)

            result_str = _export_results(results, format)
            _write_output(result_str, output, verbose)

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


@main.command(name="scan-prometheus-metrics")
@click.option("-o", "--output", default=None, type=click.Path(), help="Output file path")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option("--include", multiple=True, help="Glob patterns for files to include")
@click.option("--exclude", multiple=True, help="Glob patterns for files to exclude")
@click.option("--no-default-excludes", is_flag=True, help="Disable default exclude patterns")
@click.argument("path", type=click.Path(exists=True))
def scan_prometheus_metrics_cmd(
    output: Optional[str],
    verbose: bool,
    path: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan Python files for Prometheus metrics usage.

    PATH can be a Python file or directory containing Prometheus metrics.
    Results are aggregated by metric name and exported to YAML format.
    """
    try:
        result = scan_prometheus_metrics(
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
    except ValueError as e:
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


@main.command(name="scan-concurrency-patterns")
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
def scan_concurrency_patterns_cmd(
    path: str,
    output: Optional[str],
    verbose: bool,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
) -> None:
    """Scan Python code for concurrency patterns.

    Detects asyncio, threading, and multiprocessing patterns in Python files.
    Results are grouped by concurrency type and exported to YAML format.

    PATH: Directory or file to scan (defaults to current directory)

    Examples:

        \b
        # Scan current directory
        upcast scan-concurrency-patterns

        \b
        # Scan specific directory with verbose output
        upcast scan-concurrency-patterns ./src -v

        \b
        # Save results to file
        upcast scan-concurrency-patterns ./src -o concurrency.yaml

        \b
        # Include only specific files
        upcast scan-concurrency-patterns ./src --include "**/*_async.py"

        \b
        # Exclude test files
        upcast scan-concurrency-patterns ./src --exclude "**/test_*.py"
    """
    try:
        # Call scan_concurrency_patterns directly using its context
        ctx = click.Context(scan_concurrency_patterns)
        ctx.params = {
            "path": path,
            "output": output,
            "verbose": verbose,
            "include": include,
            "exclude": exclude,
        }
        scan_concurrency_patterns.invoke(ctx)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


@main.command(name="scan-signals")
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
def scan_signals_cmd(
    path: str,
    output: Optional[str],
    verbose: bool,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan for Django and Celery signal usage.

    Detects signal handlers, custom signal definitions, and signal registrations
    in Python codebases using Django and Celery. Results are grouped by framework
    (django/celery) and signal type, exported to YAML format.

    PATH: Directory or file to scan (defaults to current directory)

    Examples:

        \b
        # Scan current directory
        upcast scan-signals

        \b
        # Scan specific directory with verbose output
        upcast scan-signals ./src -v

        \b
        # Save results to file
        upcast scan-signals ./src -o signals.yaml

        \b
        # Include only signal files
        upcast scan-signals ./src --include "**/signals/**"

        \b
        # Exclude test files
        upcast scan-signals ./src --exclude "**/tests/**"
    """
    try:
        # Call scan_signals directly using its context
        ctx = click.Context(scan_signals)
        ctx.params = {
            "path": path,
            "output": output,
            "verbose": verbose,
            "include": include,
            "exclude": exclude,
            "no_default_excludes": no_default_excludes,
        }
        scan_signals.invoke(ctx)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


@main.command(name="scan-exception-handlers")
@click.argument("path", type=click.Path(exists=True), required=False, default=".")
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
def scan_exception_handlers_cmd(
    path: str,
    output: Optional[str],
    verbose: bool,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
) -> None:
    """Scan Python code for exception handling patterns.

    Detects try/except/else/finally blocks and analyzes exception types,
    logging practices, and control flow patterns. Results are exported
    to YAML format with detailed statistics.

    PATH: Directory or file to scan (defaults to current directory)

    Examples:

        \b
        # Scan current directory
        upcast scan-exception-handlers

        \b
        # Scan specific directory with verbose output
        upcast scan-exception-handlers ./src -v

        \b
        # Save results to file
        upcast scan-exception-handlers ./src -o handlers.yaml

        \b
        # Include only specific files
        upcast scan-exception-handlers ./src --include "**/*.py"

        \b
        # Exclude test files
        upcast scan-exception-handlers ./src --exclude "**/test_*.py"
    """
    try:
        # Call scan_exception_handlers directly using its context
        ctx = click.Context(scan_exception_handlers)
        ctx.params = {
            "path": path,
            "output": output,
            "verbose": verbose,
            "include": include,
            "exclude": exclude,
        }
        scan_exception_handlers.invoke(ctx)

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


@main.command(name="scan-blocking-operations")
@click.argument("path", type=click.Path(exists=True), required=False, nargs=-1)
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
def scan_blocking_operations_cmd(
    path: tuple[str, ...],
    output: Optional[str],
    verbose: bool,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
    output_format: str,
) -> None:
    """Scan Python code for blocking operations.

    Detects blocking operations that may cause performance issues:
    - time.sleep() calls
    - Django ORM select_for_update()
    - threading.Lock().acquire()
    - subprocess.run(), Popen.wait(), Popen.communicate()

    PATH: One or more directories or files to scan (defaults to current directory)

    Examples:

        \b
        # Scan current directory
        upcast scan-blocking-operations

        \b
        # Scan specific directory with verbose output
        upcast scan-blocking-operations ./src -v

        \b
        # Save results to file
        upcast scan-blocking-operations ./src -o blocking.yaml

        \b
        # Output as JSON
        upcast scan-blocking-operations ./src --format json

        \b
        # Include only specific files
        upcast scan-blocking-operations ./src --include "**/*.py"

        \b
        # Exclude test files
        upcast scan-blocking-operations ./src --exclude "**/test_*.py"
    """
    try:
        # Default to current directory if no path provided
        paths_to_scan = path if path else (".",)

        # Call scan_blocking_operations
        ctx = click.Context(scan_blocking_operations)
        ctx.params = {
            "path": paths_to_scan,
            "output": output,
            "output_format": output_format,
            "include": include,
            "exclude": exclude,
            "no_default_excludes": no_default_excludes,
            "verbose": verbose,
        }
        scan_blocking_operations.invoke(ctx)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


@main.command(name="scan-http-requests")
@click.argument("path", type=click.Path(exists=True), required=False, default=".")
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
    "--format",
    "output_format",
    type=click.Choice(["yaml", "json"]),
    default="yaml",
    help="Output format (yaml or json)",
)
def scan_http_requests_cmd(
    path: str,
    output: Optional[str],
    verbose: bool,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    output_format: str,
) -> None:
    """Scan Python code for HTTP/API requests.

    Detects requests made via requests, httpx, aiohttp, urllib3, urllib.request,
    and http.client libraries. Results are grouped by URL with detailed usage
    information and exported to YAML or JSON format.

    PATH: Directory or file to scan (defaults to current directory)

    Examples:

        \b
        # Scan current directory
        upcast scan-http-requests

        \b
        # Scan specific directory with verbose output
        upcast scan-http-requests ./src -v

        \b
        # Save results to file
        upcast scan-http-requests ./src -o requests.yaml

        \b
        # Output as JSON
        upcast scan-http-requests ./src --format json

        \b
        # Include only API client files
        upcast scan-http-requests ./src --include "*/api/*.py"

        \b
        # Exclude test files
        upcast scan-http-requests ./src --exclude "**/test_*.py"
    """
    try:
        # Call scan_http_requests directly using its context
        ctx = click.Context(scan_http_requests)
        ctx.params = {
            "path": path,
            "output": output,
            "verbose": verbose,
            "include": include,
            "exclude": exclude,
            "output_format": output_format,
        }
        scan_http_requests.invoke(ctx)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
