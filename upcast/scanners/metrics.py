"""Prometheus metrics scanner implementation with Pydantic models."""

from pathlib import Path
from typing import ClassVar

from astroid import nodes

from upcast.common.ast_utils import get_import_info, safe_as_string, safe_infer_value
from upcast.common.file_utils import get_relative_path_str
from upcast.common.scanner_base import BaseScanner
from upcast.models.metrics import MetricInfo, MetricUsage, PrometheusMetricOutput, PrometheusMetricSummary


class MetricsScanner(BaseScanner[PrometheusMetricOutput]):
    """Scanner for Prometheus metrics (Counter, Gauge, Histogram, Summary)."""

    METRIC_TYPES: ClassVar[list[str]] = ["Counter", "Gauge", "Histogram", "Summary"]

    def scan(self, path: Path) -> PrometheusMetricOutput:
        """Scan for Prometheus metrics."""
        files = self.get_files_to_scan(path)
        base_path = path if path.is_dir() else path.parent

        metrics: dict[str, MetricInfo] = {}

        for file_path in files:
            module = self.parse_file(file_path)
            if not module:
                continue

            imports = get_import_info(module)
            rel_path = get_relative_path_str(file_path, base_path)

            # Find metric definitions (assignments)
            for node in module.nodes_of_class(nodes.Assign):
                metric = self._parse_metric_definition(node, rel_path, imports)
                if metric:
                    metrics[metric.name] = metric

        summary = self._calculate_summary(metrics)
        return PrometheusMetricOutput(summary=summary, results=metrics)

    def _parse_metric_definition(
        self, node: nodes.Assign, file_path: str, imports: dict[str, str]
    ) -> MetricInfo | None:
        """Parse metric definition from assignment."""
        if not isinstance(node.value, nodes.Call):
            return None

        func = node.value.func
        metric_type = self._get_metric_type(func, imports)
        if not metric_type:
            return None

        # Extract metric name
        name = self._extract_string_arg(node.value, 0, "name")
        if not name:
            return None

        # Extract help text
        help_text = self._extract_string_arg(node.value, 1, "documentation")

        # Extract labels
        labels = self._extract_labels(node.value)

        usage = MetricUsage(
            file=file_path,
            line=node.lineno if hasattr(node, "lineno") else None,
            pattern=f"{metric_type} definition",
            statement=safe_as_string(node),
        )

        return MetricInfo(
            name=name,
            type=metric_type,
            help=help_text,
            labels=labels,
            usages=[usage],
            namespace=None,
            subsystem=None,
            unit=None,
            custom_collector=False,
            buckets=None,
        )

    def _get_metric_type(self, func_node: nodes.NodeNG, imports: dict[str, str]) -> str | None:
        """Get metric type from function call."""
        if isinstance(func_node, nodes.Attribute):
            if func_node.attrname in self.METRIC_TYPES:
                return func_node.attrname
        elif isinstance(func_node, nodes.Name):
            name = func_node.name
            qualified = imports.get(name, name)
            for metric_type in self.METRIC_TYPES:
                if metric_type in qualified or name == metric_type:
                    return metric_type
        return None

    def _extract_string_arg(self, call_node: nodes.Call, pos: int, kwarg_name: str | None = None) -> str | None:
        """Extract string argument by position or keyword."""
        # Try positional
        if len(call_node.args) > pos:
            value = safe_infer_value(call_node.args[pos])
            if isinstance(value, str):
                return value

        # Try keyword
        if kwarg_name:
            for keyword in call_node.keywords or []:
                if keyword.arg == kwarg_name:
                    value = safe_infer_value(keyword.value)
                    if isinstance(value, str):
                        return value

        return None

    def _extract_labels(self, call_node: nodes.Call) -> list[str]:
        """Extract label names from metric definition."""
        for keyword in call_node.keywords or []:
            if keyword.arg in ("labelnames", "labels"):
                value = safe_infer_value(keyword.value)
                if isinstance(value, (list, tuple)):
                    return [str(v) for v in value if isinstance(v, str)]
        return []

    def _calculate_summary(self, metrics: dict[str, MetricInfo]) -> PrometheusMetricSummary:
        """Calculate summary statistics."""
        by_type: dict[str, int] = {}
        for metric in metrics.values():
            by_type[metric.type] = by_type.get(metric.type, 0) + 1

        total_usages = sum(len(m.usages) for m in metrics.values())

        return PrometheusMetricSummary(
            total_count=total_usages,
            files_scanned=len({u.file for m in metrics.values() for u in m.usages}),
            total_metrics=len(metrics),
            by_type=by_type,
            scan_duration_ms=0,  # TODO: Add timing
        )
