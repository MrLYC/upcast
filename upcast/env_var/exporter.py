import csv
import os
from dataclasses import dataclass, field
from typing import TextIO

from pydantic import BaseModel

from upcast.env_var.core import EnvVar, EnvVarExporter


class BaseExporter(BaseModel):
    collected_vars: list[EnvVar] = field(default_factory=list)

    def begin(self):
        pass

    def handle(self, env_var: EnvVar):
        self.collected_vars.append(env_var)

    def get_merged_vars(self) -> dict[str, EnvVar]:
        merged_vars: dict[str, EnvVar] = {}
        for i in self.collected_vars:
            if i.name in merged_vars:
                merged_vars[i.name].merge_from(i, False)
            else:
                merged_vars[i.name] = i

        return merged_vars

    def end(self):
        pass


@dataclass
class MultiExporter:
    exporters: list[EnvVarExporter] = field(default_factory=list)

    @classmethod
    def from_paths(cls, paths: list[str]):
        exporters = []
        for i in paths:
            _, ext = os.path.splitext(i)
            if ext == ".csv":
                exporters.append(CSVExporter(path=i))
            elif ext == ".html":
                exporters.append(HTMLExporter(path=i))
            else:
                raise ValueError(f"Output format not supported: {ext}")

        return cls(exporters=exporters)

    def begin(self):
        for i in self.exporters:
            i.begin()

    def handle(self, env_var: EnvVar):
        for i in self.exporters:
            i.handle(env_var)

    def end(self):
        for i in self.exporters:
            i.end()


@dataclass
class CSVExporter:
    path: str
    file: TextIO = field(init=False)
    writer: csv.DictWriter = field(init=False)

    def __post_init__(self):
        self.file = open(self.path, "w", encoding="utf-8-sig")
        self.writer = csv.DictWriter(
            self.file,
            fieldnames=["name", "cast", "value", "required", "statement", "location"],
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


@dataclass
class HTMLExporter:
    path: str
    file: TextIO = field(init=False)

    def __post_init__(self):
        self.file = open(self.path, "w", encoding="utf-8")

    def begin(self):
        self.file.write("<html><head><title>Env Vars</title></head><body><table>")
        self.file.write(
            "\n".join(
                [
                    "<tr><th>Name</th>",
                    "<th>Value</th>",
                    "<th>Cast</th>",
                    "<th>Required</th>",
                    "<th>Statement</th></tr>" "<th>Location</th>",
                ]
            )
        )

    def handle(self, env_var: EnvVar):
        self.file.write(
            "\n".join(
                [
                    "<tr>",
                    f"<td>{env_var.name}</td>",
                    f"<td>{env_var.value}</td>",
                    f"<td>{env_var.cast}</td>",
                    f"<td>{'Yes' if env_var.required else ''}</td>",
                    f"<td>{env_var.statement()}</td>",
                    f"<td>{env_var.location()}</td>",
                    "</tr>",
                ]
            )
        )

    def end(self):
        self.file.write("</table></body></html>")
        self.file.close()
