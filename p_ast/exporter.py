import csv
from dataclasses import dataclass
from typing import TextIO

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
            fieldnames=["name", "value_type", "value", "file", "line"],
        )

    def begin(self):
        self.writer.writeheader()

    def handle(self, env_var: Var):
        self.writer.writerow(
            {
                "name": env_var.name,
                "value_type": env_var.value_type,
                "value": env_var.value,
                "line": env_var.line_range(),
                "file": env_var.file,
            }
        )

    def end(self):
        self.file.close()


class ConsoleExporter(BaseExporter):
    def handle(self, env_var: Var):
        line = f"{env_var.file}:{env_var.line_range()}"

        if env_var.value:
            print(f"{env_var.name}={env_var.value} in {line}")
        else:
            print(f"{env_var.name} in {line}")
