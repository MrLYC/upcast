from typing import List

import click

from upcast.exporter import CSVExporter, BaseExporter, HTMLExporter
from upcast.plugins.env_var import EnvVarHub
import os


@click.group()
def main():
    pass


@main.command()
@click.option("-o", "--output", default="", type=click.Path())
@click.argument("path", nargs=-1)
def find_env_vars(output: str, path: List[str]):
    def iter_files():
        for i in path:
            with open(i, "r") as f:
                yield f

    _, output_ext = os.path.splitext(output)

    if not output:
        exporter = BaseExporter()
    elif output_ext == ".csv":
        exporter = CSVExporter(path=output)
    elif output_ext == ".html":
        exporter = HTMLExporter(path=output)
    else:
        raise click.UsageError("Output format not supported")

    hub = EnvVarHub(exporter=exporter)
    hub.run(iter_files())


if __name__ == "__main__":
    main()
