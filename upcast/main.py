import os

import click

from tests.test_plugins_env_var import exporter
from upcast.exporter import BaseExporter, MultiExporter
from upcast.plugins.env_var import EnvVarHub


@click.group()
def main():
    pass


@main.command()
@click.option("-o", "--output", default=[], type=click.Path(), multiple=True)
@click.argument("path", nargs=-1)
def find_env_vars(output: list[str], path: list[str]):
    def iter_files():
        for i in path:
            with open(i) as f:
                yield f

    if not output:
        exporter = BaseExporter()
    else:
        exporter = MultiExporter.from_paths(output)

    hub = EnvVarHub(exporter=exporter)
    hub.run(iter_files())


if __name__ == "__main__":
    main()
