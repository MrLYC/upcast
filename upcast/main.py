import sys
from typing import Optional

import click

from upcast.django_scanner import scan_django_models
from upcast.env_var.exporter import BaseExporter, MultiExporter
from upcast.env_var.plugin import EnvVarHub


@click.group()
def main():
    pass


@main.command()
@click.option("-o", "--output", default=[], type=click.Path(), multiple=True)
@click.option("--additional-patterns", default=[], multiple=True)
@click.option("--additional-required-patterns", default=[], multiple=True)
@click.argument("path", nargs=-1)
def find_env_vars(
    output: list[str],
    path: list[str],
    additional_patterns: list[str],
    additional_required_patterns: list[str],
):
    def iter_files():
        for i in path:
            with open(i) as f:
                yield f

    exporter = MultiExporter.from_paths(output) if output else BaseExporter()

    hub = EnvVarHub(
        exporter=exporter,
        additional_patterns=additional_patterns,
        additional_required_patterns=additional_required_patterns,
    )
    hub.run(iter_files())


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
