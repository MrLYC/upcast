import json
import sys
from contextlib import nullcontext
from typing import Optional

import click

from upcast.django_model.core import Runner
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
@click.argument("path", nargs=-1)
def analyze_django_models(output: Optional[str], path: list[str]):
    def iter_files():
        for i in path:
            with open(i) as f:
                yield f

    output_file = open(output, "w") if output else nullcontext(sys.stdout)

    with output_file as f:
        runner = Runner()
        runner.run(iter_files())

        f.write(
            json.dumps(
                {k: v.model_dump() for k, v in runner.context.resolved_models.items()},
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
