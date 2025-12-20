"""Checker for Prometheus metrics scanning."""

from pathlib import Path
from typing import Any

from astroid import MANAGER, nodes

from upcast.prometheus_metrics_scanner.metrics_parser import (
    MetricInfo,
    parse_custom_collector,
    parse_metric_decorator,
    parse_metric_instantiation,
)


class PrometheusMetricsChecker:
    """Checker that scans Prometheus metrics using AST analysis."""

    def __init__(self, base_path: str):
        """Initialize the checker.

        Args:
            base_path: Base directory path for calculating relative paths
        """
        self.metrics: dict[str, MetricInfo] = {}
        self.base_path = Path(base_path)

    def check_file(self, file_path: str) -> None:
        """Process a single file.

        Args:
            file_path: Path to the file to check
        """
        try:
            module = MANAGER.ast_from_file(file_path)
            rel_path = self._get_relative_path(file_path)

            # First pass: Find metric instantiations
            for assign in module.nodes_of_class(nodes.Assign):
                metric_info = parse_metric_instantiation(assign, rel_path, assign.lineno)
                if metric_info:
                    self._register_metric(metric_info)

            # Second pass: Find decorators
            for funcdef in module.nodes_of_class(nodes.FunctionDef):
                usages = parse_metric_decorator(funcdef, rel_path)
                for _usage in usages:
                    # Decorators are tracked but simplified for initial implementation
                    pass

            # Third pass: Find custom collectors
            for classdef in module.nodes_of_class(nodes.ClassDef):
                collector_metrics = parse_custom_collector(classdef, rel_path)
                for metric_info in collector_metrics:
                    self._register_metric(metric_info)

        except Exception:  # noqa: S110
            pass

    def _get_relative_path(self, file_path: str) -> str:
        """Get path relative to base_path.

        Args:
            file_path: Absolute file path

        Returns:
            Relative path string
        """
        try:
            return str(Path(file_path).relative_to(self.base_path))
        except ValueError:
            return file_path

    def _register_metric(self, metric_info: MetricInfo) -> None:
        """Register a metric, aggregating if it already exists.

        Args:
            metric_info: The metric to register
        """
        full_name = metric_info.get_full_name()
        if full_name in self.metrics:
            # Aggregate usages
            existing = self.metrics[full_name]
            existing.usages.extend(metric_info.usages)
            # Sort usages by location
            existing.usages.sort(key=lambda u: u.location)
        else:
            self.metrics[full_name] = metric_info

    def get_metrics(self) -> dict[str, Any]:
        """Get all collected metrics.

        Returns:
            Dictionary of metric names to MetricInfo
        """
        return self.metrics
