import sys
from typing import Optional

import click

from upcast.common.cli import run_scanner_cli
from upcast.scanners import (
    BlockingOperationsScanner,
    ComplexityScanner,
    ConcurrencyScanner,
    DjangoModelScanner,
    DjangoSettingsScanner,
    DjangoUrlScanner,
    EnvVarScanner,
    ExceptionHandlerScanner,
    HttpRequestsScanner,
    MetricsScanner,
    ModuleSymbolScanner,
    RedisUsageScanner,
    UnitTestScanner,
)


@click.group()
def main():
    pass


@main.command(name="scan-complexity-patterns")
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
def scan_complexity_patterns_cmd(
    output: Optional[str],
    verbose: bool,
    format: str,  # noqa: A002
    threshold: int,
    path: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan Python files for cyclomatic complexity patterns.

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


@main.command(name="scan-concurrency-patterns")
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
def scan_concurrency_patterns_cmd(
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
    "output_format",
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
def scan_unit_tests_cmd(
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


@main.command(name="scan-django-urls")
@click.option("-o", "--output", type=click.Path(), help="Output file path (YAML or JSON)")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["yaml", "json"], case_sensitive=False),
    default="yaml",
    help="Output format (default: yaml)",
)
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging")
@click.option("--include", multiple=True, help="File patterns to include (e.g., '**/urls.py')")
@click.option("--exclude", multiple=True, help="File patterns to exclude")
@click.option("--no-default-excludes", is_flag=True, help="Disable default exclude patterns")
@click.argument("path", type=click.Path(exists=True), default=".")
def scan_django_urls_cmd(
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
        upcast scan-django-urls ./myproject

        \b
        # Scan specific urls.py file
        upcast scan-django-urls myapp/urls.py

        \b
        # Save results to JSON file
        upcast scan-django-urls ./myproject --output urls.json --format json
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
@click.option("-o", "--output", type=click.Path(), help="Output file path (YAML or JSON)")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["yaml", "json"], case_sensitive=False),
    default="yaml",
    help="Output format (default: yaml)",
)
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging")
@click.option("--include", multiple=True, help="File patterns to include (e.g., '**/models.py')")
@click.option("--exclude", multiple=True, help="File patterns to exclude")
@click.option("--no-default-excludes", is_flag=True, help="Disable default exclude patterns")
@click.argument("path", type=click.Path(exists=True), default=".")
def scan_django_models_cmd(
    path: str,
    output: str | None,
    output_format: str,
    verbose: bool,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan Django model files for model definitions.

    Extracts model classes, fields, relationships, and Meta options.

    PATH: Directory or file to scan (defaults to current directory)

    Examples:

        \b
        # Scan for Django models
        upcast scan-django-models ./myproject

        \b
        # Scan specific models.py file
        upcast scan-django-models myapp/models.py

        \b
        # Save results to JSON file
        upcast scan-django-models ./myproject --output models.json --format json
    """

    try:
        scanner = DjangoModelScanner(
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


@main.command(name="scan-django-settings")
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
def scan_django_settings_cmd(
    output: Optional[str],
    verbose: bool,
    format: str,  # noqa: A002
    path: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan Django code for settings definitions and usages.

    This command scans for both settings definitions and usages, producing
    comprehensive output for each setting variable.

    PATH: Directory or file to scan (defaults to current directory)

    Examples:

        \b
        # Scan for settings
        upcast scan-django-settings .

        \b
        # Save results to file
        upcast scan-django-settings . -o settings.yaml

        \b
        # Output as JSON
        upcast scan-django-settings . --format json
    """
    try:
        scanner = DjangoSettingsScanner(verbose=verbose)
        output_format_str = format
        run_scanner_cli(scanner, path, output, output_format_str, include, exclude, no_default_excludes, verbose)

        if verbose:
            click.echo("Scan complete!", err=True)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


@main.command(name="scan-redis-usage")
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
def scan_redis_usage_cmd(
    output: Optional[str],
    verbose: bool,
    format: str,  # noqa: A002
    path: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan for Redis usage patterns in Django projects.

    Detects:
    - Cache backend configurations (django-redis)
    - Session storage using Redis
    - Celery broker and result backend
    - Django Channels
    - Distributed locks
    - Direct redis-py usage
    - Rate limiting configurations
    - Feature flags
    """
    try:
        if verbose:
            click.echo(f"Scanning for Redis usage in: {path}", err=True)

        scanner = RedisUsageScanner(
            include_patterns=list(include) if include else None,
            exclude_patterns=list(exclude) if exclude else None,
            verbose=verbose,
        )

        run_scanner_cli(
            scanner=scanner,
            path=path,
            output=output,
            format=format,
            verbose=verbose,
            include=include,
            exclude=exclude,
            no_default_excludes=no_default_excludes,
        )

        if verbose:
            click.echo("Scan complete!", err=True)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


@main.command(name="scan-module-symbols")
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
@click.option("--include-private", is_flag=True, help="Include private symbols (starting with _)")
@click.argument("path", type=click.Path(exists=True), default=".", required=False)
def scan_module_symbols_cmd(
    output: Optional[str],
    verbose: bool,
    format: str,  # noqa: A002
    path: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
    include_private: bool,
) -> None:
    """Scan Python modules for imports and symbol definitions.

    Extracts:
    - Import statements (import, from...import, from...import *)
    - Module-level variables, functions, and classes
    - Decorators, docstrings, and signatures
    - Attribute access patterns
    - Block context (module, if, try, except)

    PATH can be a Python file or directory.
    """
    try:
        scanner = ModuleSymbolScanner(
            include_patterns=list(include) if include else None,
            exclude_patterns=list(exclude) if exclude else None,
            verbose=verbose,
            include_private=include_private,
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


@main.command(name="render-markdown")
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="Output markdown file path (default: <input>-<lang>.md)")
@click.option(
    "-l",
    "--language",
    type=click.Choice(["en", "zh"], case_sensitive=False),
    default="en",
    help="Output language (default: en)",
)
@click.option("-t", "--title", type=str, help="Document title (auto-generated if not provided)")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
def render_markdown_cmd(
    input_file: str,
    output: str | None,
    language: str,
    title: str | None,
    verbose: bool,
) -> None:
    """Render scanner output (YAML/JSON) to markdown format.

    Converts scanner output files to readable markdown documentation with support
    for multiple languages.

    INPUT_FILE: Path to scanner output file (YAML or JSON format)

    Examples:

        \b
        # Render to English markdown
        upcast render-markdown results.yaml

        \b
        # Render to Chinese markdown
        upcast render-markdown results.yaml --language zh

        \b
        # Specify output file and title
        upcast render-markdown results.yaml -o report.md --title "Analysis Report"

        \b
        # Render JSON input to markdown
        upcast render-markdown results.json -o report.md
    """
    import json
    from pathlib import Path

    import yaml

    from upcast.models.base import ScannerOutput
    from upcast.models.blocking_operations import BlockingOperationsOutput
    from upcast.models.complexity import ComplexityOutput
    from upcast.models.concurrency import ConcurrencyPatternOutput
    from upcast.models.django_models import DjangoModelOutput
    from upcast.models.django_settings import DjangoSettingsOutput
    from upcast.models.django_urls import DjangoUrlOutput
    from upcast.models.env_vars import EnvVarOutput
    from upcast.models.exceptions import ExceptionHandlerOutput
    from upcast.models.http_requests import HttpRequestOutput
    from upcast.models.metrics import PrometheusMetricOutput
    from upcast.models.redis_usage import RedisUsageOutput
    from upcast.models.signals import SignalOutput
    from upcast.models.unit_tests import UnitTestOutput
    from upcast.render import render_to_file

    try:
        input_path = Path(input_file)

        if verbose:
            click.echo(f"Reading input file: {input_path}", err=True)

        # Load input data
        with open(input_path) as f:
            if input_path.suffix.lower() in [".yaml", ".yml"]:
                data = yaml.safe_load(f)
            elif input_path.suffix.lower() == ".json":
                data = json.load(f)
            else:
                raise ValueError(f"Unsupported file format: {input_path.suffix}. Use .yaml, .yml, or .json")

        # Try to detect the model type and create appropriate instance
        model_classes = [
            HttpRequestOutput,
            DjangoModelOutput,
            ComplexityOutput,
            EnvVarOutput,
            SignalOutput,
            BlockingOperationsOutput,
            ConcurrencyPatternOutput,
            DjangoSettingsOutput,
            DjangoUrlOutput,
            ExceptionHandlerOutput,
            PrometheusMetricOutput,
            RedisUsageOutput,
            UnitTestOutput,
        ]

        scanner_output: ScannerOutput | None = None
        for model_class in model_classes:
            try:
                scanner_output = model_class(**data)
                if verbose:
                    click.echo(f"Detected model type: {model_class.__name__}", err=True)
                break
            except (TypeError, ValueError, KeyError):
                # Expected exceptions during model instantiation
                continue

        if scanner_output is None:
            raise ValueError(
                "Could not determine scanner output type. "
                "Please ensure the input file is a valid scanner output."
            )

        # Generate output filename if not provided
        if output is None:
            output = str(input_path.with_suffix("")) + f"-{language}.md"

        # Generate title if not provided
        if title is None:
            # Use filename without extension as title
            title = input_path.stem.replace("-", " ").replace("_", " ").title()

        if verbose:
            click.echo(f"Rendering to markdown: {output}", err=True)
            click.echo(f"Language: {language}", err=True)
            click.echo(f"Title: {title}", err=True)

        # Render to markdown
        render_to_file(scanner_output, output, language=language, title=title)

        click.echo(f"✓ Successfully rendered markdown to: {output}")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
