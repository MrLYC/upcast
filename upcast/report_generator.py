"""Generate deterministic Markdown reports from saved scanner results."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

import yaml


class ReportGenerator:
    """Aggregate scanner YAML files without importing or executing target code."""

    def __init__(self, scan_results_dir: str | Path):
        self.scan_results_dir = Path(scan_results_dir)
        self.results: dict[str, dict[str, Any]] = {}
        self._loaded = False

    def load_results(self) -> dict[str, dict[str, Any]]:
        """Load top-level YAML scanner results in filename order."""
        if not self.scan_results_dir.exists():
            raise FileNotFoundError(f"Directory not found: {self.scan_results_dir}")
        if not self.scan_results_dir.is_dir():
            raise NotADirectoryError(f"Scan results path is not a directory: {self.scan_results_dir}")

        results: dict[str, dict[str, Any]] = {}
        for yaml_file in sorted(self.scan_results_dir.glob("*.yaml")):
            with yaml_file.open(encoding="utf-8") as stream:
                payload = yaml.safe_load(stream) or {}
            if isinstance(payload, Mapping):
                results[yaml_file.stem] = dict(payload)
        self.results = results
        self._loaded = True
        return self.results

    def generate_report(self) -> str:
        """Return a stable Markdown report for the loaded scanner results."""
        if not self._loaded:
            self.load_results()

        sections = [
            self._header(),
            self._executive_summary(),
            self._code_quality_section(),
            self._architecture_section(),
            self._infrastructure_section(),
            self._testing_section(),
            self._dependencies_section(),
            self._recommendations_section(),
        ]
        return "\n\n".join(section for section in sections if section)

    def _header(self) -> str:
        return "# Project Analysis Report\n\nGenerated from static code analysis scan results."

    def _executive_summary(self) -> str:
        total_files = sum(self._summary_int(data, "files_scanned") for data in self.results.values())
        total_findings = sum(self._summary_int(data, "total_count") for data in self.results.values())
        lines = [
            "## Executive Summary",
            "",
            f"- **Total Files Scanned**: {total_files}",
            f"- **Total Findings**: {total_findings}",
            f"- **Scan Types**: {len(self.results)}",
        ]
        return "\n".join(lines)

    def _code_quality_section(self) -> str:
        sections: list[str] = []
        complexity = self.results.get("complexity-patterns")
        if complexity is not None:
            summary = self._summary(complexity)
            lines = [
                "## Code Quality Analysis",
                "",
                "### Cyclomatic Complexity",
                "",
                f"- **High Complexity Functions**: {self._value(summary, 'high_complexity_count')}",
                f"- **Files Analyzed**: {self._value(summary, 'files_scanned')}",
            ]
            severity = self._mapping(summary.get("by_severity"))
            if severity:
                lines.extend(["", "**Distribution by Severity:**", "", "| Severity | Count |", "|---|---:|"])
                lines.extend(f"| {self._cell(key)} | {self._cell(value)} |" for key, value in sorted(severity.items()))
            records = self._flatten_records(complexity.get("results"))
            if records:
                lines.extend([
                    "",
                    "#### Top Complexity Findings",
                    "",
                    "| Function | Complexity | File | Line |",
                    "|---|---:|---|---:|",
                ])
                ranked = sorted(records, key=lambda record: self._number(record.get("complexity")), reverse=True)
                for record in ranked[:10]:
                    lines.append(
                        "| {} | {} | {} | {} |".format(
                            self._cell(record.get("name", "unknown")),
                            self._cell(record.get("complexity", "?")),
                            self._cell(record.get("file", "unknown")),
                            self._cell(record.get("line", "?")),
                        )
                    )
            sections.append("\n".join(lines))

        blocking = self.results.get("blocking-operations")
        if blocking is not None:
            summary = self._summary(blocking)
            lines = [
                "### Blocking Operations",
                "",
                f"- **Total Operations**: {self._value(summary, 'total_count')}",
                f"- **Files Scanned**: {self._value(summary, 'files_scanned')}",
            ]
            categories = self._mapping(summary.get("by_category"))
            if categories:
                lines.extend(["", "| Category | Count |", "|---|---:|"])
                lines.extend(
                    f"| {self._cell(key)} | {self._cell(value)} |" for key, value in sorted(categories.items())
                )
            sections.append("\n".join(lines))

        return "\n\n".join(sections)

    def _architecture_section(self) -> str:
        scanner_names = ("django-models", "django-urls", "concurrency-patterns", "signals")
        present = [name for name in scanner_names if name in self.results]
        if not present:
            return ""

        lines = ["## Architecture & Patterns"]
        for name in present:
            summary = self._summary(self.results[name])
            title = name.replace("-", " ").title()
            lines.extend(["", f"### {title}"])
            for key in self._preferred_summary_keys(summary):
                lines.append(f"- **{key.replace('_', ' ').title()}**: {self._cell(summary[key])}")
        return "\n".join(lines)

    def _infrastructure_section(self) -> str:
        scanner_names = ("env-vars", "django-settings", "redis-usage", "metrics")
        present = [name for name in scanner_names if name in self.results]
        if not present:
            return ""

        lines = ["## Infrastructure"]
        for name in present:
            summary = self._summary(self.results[name])
            title = name.replace("-", " ").title()
            lines.extend(["", f"### {title}"])
            for key in self._preferred_summary_keys(summary):
                lines.append(f"- **{key.replace('_', ' ').title()}**: {self._cell(summary[key])}")
        return "\n".join(lines)

    def _testing_section(self) -> str:
        scanner_names = ("unit-tests", "exception-handlers")
        present = [name for name in scanner_names if name in self.results]
        if not present:
            return ""

        lines = ["## Testing & Reliability"]
        for name in present:
            summary = self._summary(self.results[name])
            title = name.replace("-", " ").title()
            lines.extend(["", f"### {title}"])
            for key in self._preferred_summary_keys(summary):
                lines.append(f"- **{key.replace('_', ' ').title()}**: {self._cell(summary[key])}")
        return "\n".join(lines)

    def _dependencies_section(self) -> str:
        data = self.results.get("http-requests")
        if data is None:
            return ""
        summary = self._summary(data)
        lines = [
            "## External Dependencies",
            "",
            "### HTTP Requests",
            "",
            f"- **Total Requests**: {self._value(summary, 'total_count')}",
            f"- **Files Scanned**: {self._value(summary, 'files_scanned')}",
        ]
        libraries = self._mapping(summary.get("by_library"))
        if libraries:
            lines.extend(["", "| Library | Count |", "|---|---:|"])
            lines.extend(f"| {self._cell(key)} | {self._cell(value)} |" for key, value in sorted(libraries.items()))
        requests = data.get("results")
        if isinstance(requests, Mapping):
            rows = []
            for url, info in sorted(requests.items(), key=lambda item: str(item[0])):
                if isinstance(info, Mapping):
                    rows.append((url, info.get("method", "?"), info.get("library", "?")))
            if rows:
                lines.extend(["", "**Request Patterns:**", "", "| URL | Method | Library |", "|---|---|---|"])
                lines.extend(
                    f"| {self._cell(url)} | {self._cell(method)} | {self._cell(library)} |"
                    for url, method, library in rows[:20]
                )
        return "\n".join(lines)

    def _recommendations_section(self) -> str:
        if not self.results:
            return ""
        complexity = self._summary(self.results.get("complexity-patterns", {}))
        blocking = self._summary(self.results.get("blocking-operations", {}))
        exceptions = self._summary(self.results.get("exception-handlers", {}))
        lines = [
            "## Summary & Key Recommendations",
            "",
            "### Key Findings",
            "",
            f"- **High Complexity**: {self._value(complexity, 'high_complexity_count')}",
            f"- **Blocking Operations**: {self._value(blocking, 'total_count')}",
            f"- **Exception Handlers**: {self._value(exceptions, 'total_count')}",
            "",
            "Review scanner-specific YAML for source locations before making changes.",
        ]
        return "\n".join(lines)

    def _summary(self, data: Mapping[str, Any]) -> dict[str, Any]:
        summary = data.get("summary")
        return dict(summary) if isinstance(summary, Mapping) else {}

    def _summary_int(self, data: Mapping[str, Any], key: str) -> int:
        value = self._summary(data).get(key, 0)
        return self._number(value)

    def _preferred_summary_keys(self, summary: Mapping[str, Any]) -> list[str]:
        keys = ("total_count", "total_models", "total_fields", "total_relationships", "total_patterns", "files_scanned")
        return [key for key in keys if key in summary]

    def _value(self, mapping: Mapping[str, Any], key: str) -> Any:
        return mapping.get(key, 0)

    def _mapping(self, value: Any) -> dict[str, Any]:
        return dict(value) if isinstance(value, Mapping) else {}

    def _flatten_records(self, value: Any) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        if isinstance(value, Mapping):
            for file_name, entries in value.items():
                if isinstance(entries, Mapping):
                    record = dict(entries)
                    record.setdefault("file", file_name)
                    records.append(record)
                elif isinstance(entries, Iterable) and not isinstance(entries, (str, bytes)):
                    for entry in entries:
                        if isinstance(entry, Mapping):
                            record = dict(entry)
                            record.setdefault("file", file_name)
                            records.append(record)
        elif isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
            records.extend(dict(entry) for entry in value if isinstance(entry, Mapping))
        return records

    def _cell(self, value: Any) -> str:
        return str(value).replace("|", r"\|").replace("\n", " ").replace("`", r"\`")

    def _number(self, value: Any) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0
