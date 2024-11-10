import csv
from dataclasses import dataclass
from typing import TextIO, List, Dict

from black.cache import field
from pydantic import BaseModel

from upcast.core import EnvVar


class BaseExporter(BaseModel):
    def begin(self):
        pass

    def handle(self, env_var: EnvVar):
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
            fieldnames=["name", "cast", "value", "required", "location", "statement"],
        )

    def begin(self):
        self.writer.writeheader()

    def handle(self, env_var: EnvVar):
        self.writer.writerow(
            {
                "name": env_var.name,
                "cast": env_var.cast,
                "value": env_var.value,
                "required": "*" if env_var.required else "",
                "location": env_var.location(),
                "statement": env_var.statement(),
            }
        )

    def end(self):
        self.file.close()


class ConsoleExporter(BaseExporter):
    def handle(self, env_var: EnvVar):
        prefix = ""
        if env_var.required:
            prefix = "*"

        if env_var.value:
            print(f"{prefix}{env_var.name}={env_var.value} at {env_var.location()}")
        else:
            print(f"{prefix}{env_var.name} at {env_var.location()}")


class CollectionExporter(BaseExporter):
    collected_vars: List[EnvVar] = field(default_factory=list)

    def handle(self, env_var: EnvVar):
        self.collected_vars.append(env_var)

    def get_merged_vars(self) -> Dict[str, EnvVar]:
        merged_vars: Dict[str, EnvVar] = {}
        for i in self.collected_vars:
            if i.name in merged_vars:
                merged_vars[i.name].merge_from(i, False)
            else:
                merged_vars[i.name] = i

        return merged_vars
