import sys
from typing import Optional

import click

from upcast.django_model_scanner import scan_django_models
from upcast.django_settings_scanner import scan_django_settings
from upcast.env_var_scanner.cli import scan_directory, scan_files
from upcast.env_var_scanner.export import export_to_json, export_to_yaml
from upcast.prometheus_metrics_scanner import scan_prometheus_metrics


@click.group()
def main():
    pass


@main.command()
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
def scan_env_vars(  # noqa: C901
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
        # Separate files and directories
        all_files = []
        for p in path:
            p_obj = PathLib(p)
            if p_obj.is_file():
                all_files.append(str(p))
            elif p_obj.is_dir():
                # Scan directory for Python files
                checker = scan_directory(str(p))
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
def scan_django_models_command(
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
def scan_prometheus_metrics_command(
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


@main.command(name="scan-django-settings")
@click.option("-o", "--output", default=None, type=click.Path(), help="Output file path")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option("--include", multiple=True, help="Glob patterns for files to include")
@click.option("--exclude", multiple=True, help="Glob patterns for files to exclude")
@click.option("--no-default-excludes", is_flag=True, help="Disable default exclude patterns")
@click.argument("path", type=click.Path(exists=True))
def scan_django_settings_command(
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


# Deprecated command aliases with warnings
@main.command(name="analyze-django-models", hidden=True)
@click.option("-o", "--output", default=None, type=click.Path())
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option("--include", multiple=True, help="Glob patterns for files to include")
@click.option("--exclude", multiple=True, help="Glob patterns for files to exclude")
@click.option("--no-default-excludes", is_flag=True, help="Disable default exclude patterns")
@click.argument("path", type=click.Path(exists=True))
def analyze_django_models_deprecated(
    output: Optional[str],
    verbose: bool,
    path: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """DEPRECATED: Use 'scan-django-models' instead."""
    click.echo(
        "Warning: 'analyze-django-models' is deprecated. Use 'scan-django-models' instead.",
        err=True,
    )
    ctx = click.get_current_context()
    ctx.invoke(
        scan_django_models_command,
        output=output,
        verbose=verbose,
        path=path,
        include=include,
        exclude=exclude,
        no_default_excludes=no_default_excludes,
    )


@main.command(name="scan-prometheus-metrics-cmd", hidden=True)
@click.option("-o", "--output", default=None, type=click.Path(), help="Output file path")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option("--include", multiple=True, help="Glob patterns for files to include")
@click.option("--exclude", multiple=True, help="Glob patterns for files to exclude")
@click.option("--no-default-excludes", is_flag=True, help="Disable default exclude patterns")
@click.argument("path", type=click.Path(exists=True))
def scan_prometheus_metrics_cmd_deprecated(
    output: Optional[str],
    verbose: bool,
    path: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """DEPRECATED: Use 'scan-prometheus-metrics' instead."""
    click.echo(
        "Warning: 'scan-prometheus-metrics-cmd' is deprecated. Use 'scan-prometheus-metrics' instead.",
        err=True,
    )
    ctx = click.get_current_context()
    ctx.invoke(
        scan_prometheus_metrics_command,
        output=output,
        verbose=verbose,
        path=path,
        include=include,
        exclude=exclude,
        no_default_excludes=no_default_excludes,
    )


@main.command(name="scan-django-settings-cmd", hidden=True)
@click.option("-o", "--output", default=None, type=click.Path(), help="Output file path")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option("--include", multiple=True, help="Glob patterns for files to include")
@click.option("--exclude", multiple=True, help="Glob patterns for files to exclude")
@click.option("--no-default-excludes", is_flag=True, help="Disable default exclude patterns")
@click.argument("path", type=click.Path(exists=True))
def scan_django_settings_cmd_deprecated(
    output: Optional[str],
    verbose: bool,
    path: str,
    include: tuple[str, ...],
    exclude: tuple[str, ...],
    no_default_excludes: bool,
) -> None:
    """DEPRECATED: Use 'scan-django-settings' instead."""
    click.echo(
        "Warning: 'scan-django-settings-cmd' is deprecated. Use 'scan-django-settings' instead.",
        err=True,
    )
    ctx = click.get_current_context()
    ctx.invoke(
        scan_django_settings_command,
        output=output,
        verbose=verbose,
        path=path,
        include=include,
        exclude=exclude,
        no_default_excludes=no_default_excludes,
    )


if __name__ == "__main__":
    main()
