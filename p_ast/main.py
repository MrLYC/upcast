from typing import List

import click

from p_ast.exporter import CSVExporter, ConsoleExporter
from p_ast.plugins.env_var import EnvVarHub


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

    if not output:
        exporter = ConsoleExporter()
    elif output.endswith(".csv"):
        exporter = CSVExporter(path=output)
    else:
        raise click.UsageError("Output format not supported")

    hub = EnvVarHub(exporter=exporter)
    hub.run(iter_files())


if __name__ == "__main__":
    main()
