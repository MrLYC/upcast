import sys
from typing import Optional

import click

from upcast.django_model_scanner import scan_django_models
from upcast.env_var_scanner.cli import scan_directory, scan_files
from upcast.env_var_scanner.export import export_to_json, export_to_yaml


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
@click.argument("path", type=click.Path(exists=True), nargs=-1, required=True)
def scan_env_vars(  # noqa: C901
    output: Optional[str],
    verbose: bool,
    format: str,  # noqa: A002
    path: tuple[str, ...],
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


@main.command()
@click.option("-o", "--output", default=None, type=click.Path())
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.argument("path", type=click.Path(exists=True))
def analyze_django_models(output: Optional[str], verbose: bool, path: str) -> None:
    """Analyze Django models in Python files and export to YAML.

    PATH can be a Python file or directory containing Django models.
    """
    try:
        result = scan_django_models(path, output=output, verbose=verbose)

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


if __name__ == "__main__":
    main()
