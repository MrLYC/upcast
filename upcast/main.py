import sys
from typing import Optional

import click

from upcast.concurrency_scanner.cli import scan_concurrency
from upcast.django_model_scanner import scan_django_models
from upcast.django_settings_scanner import scan_django_settings
from upcast.django_url_scanner import scan_django_urls
from upcast.env_var_scanner.cli import scan_directory, scan_files
from upcast.env_var_scanner.export import export_to_json, export_to_yaml
from upcast.prometheus_metrics_scanner import scan_prometheus_metrics


@click.group()
def main():
    pass


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
@click.argument("path", type=click.Path(exists=True))
def scan_django_settings_cmd(
    output: Optional[str],
    verbose: bool,
    path: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """Scan Django project for settings usage.

    PATH can be a Python file or directory containing Django code.
    Results are aggregated by settings variable name and exported to YAML format.
    """
    try:
        scan_django_settings(
            path,
            output=output,
            verbose=verbose,
            include_patterns=list(include) if include else None,
            exclude_patterns=list(exclude) if exclude else None,
            use_default_excludes=not no_default_excludes,
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


@main.command(name="scan-concurrency")
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
def scan_concurrency_cmd(
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
        upcast scan-concurrency

        \b
        # Scan specific directory with verbose output
        upcast scan-concurrency ./src -v

        \b
        # Save results to file
        upcast scan-concurrency ./src -o concurrency.yaml

        \b
        # Include only specific files
        upcast scan-concurrency ./src --include "**/*_async.py"

        \b
        # Exclude test files
        upcast scan-concurrency ./src --exclude "**/test_*.py"
    """
    try:
        # Call scan_concurrency directly using its context
        ctx = click.Context(scan_concurrency)
        ctx.params = {
            "path": path,
            "output": output,
            "verbose": verbose,
            "include": include,
            "exclude": exclude,
        }
        scan_concurrency.invoke(ctx)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
