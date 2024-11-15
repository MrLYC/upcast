import click

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

    if not output:
        exporter = BaseExporter()
    else:
        exporter = MultiExporter.from_paths(output)

    hub = EnvVarHub(
        exporter=exporter,
        additional_patterns=additional_patterns,
        additional_required_patterns=additional_required_patterns,
    )
    hub.run(iter_files())


if __name__ == "__main__":
    main()
