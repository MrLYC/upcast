import csv
from dataclasses import dataclass
from typing import TextIO, List

from black.cache import field
from pydantic import BaseModel

from p_ast.core import Var


class BaseExporter(BaseModel):
    def begin(self):
        pass

    def handle(self, env_var: Var):
        raise NotImplementedError()

    def end(self):
        pass


@dataclass
class CSVExporter:
    path: str
    file: TextIO = field(init=False)
    writer: csv.DictWriter = field(init=False)

    def __post_init__(self):
        self.file = open(self.path, "w", encoding="utf-8-sig")
        self.writer = csv.DictWriter(
            self.file,
            fieldnames=["name", "cast", "value", "location", "statement"],
        )

    def begin(self):
        self.writer.writeheader()

    def handle(self, env_var: Var):
        self.writer.writerow(
            {
                "name": env_var.name,
                "cast": env_var.cast,
                "value": env_var.value,
                "location": env_var.location(),
                "statement": env_var.statement(),
            }
        )

    def end(self):
        self.file.close()


class ConsoleExporter(BaseExporter):
    def handle(self, env_var: Var):
        if env_var.value:
            print(f"{env_var.name}={env_var.value} at {env_var.location()}")
        else:
            print(f"{env_var.name} at {env_var.position}")


class CollectionExporter(BaseExporter):
    collected_vars: List[Var]

    def handle(self, env_var: Var):
        self.vars.append(env_var)

    def get_vars(self):
        return self.collected_vars
