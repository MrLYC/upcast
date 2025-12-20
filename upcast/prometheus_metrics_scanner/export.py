"""YAML export functions."""

from typing import Any

from upcast.common.export import export_to_yaml as common_export_yaml
from upcast.common.export import export_to_yaml_string as common_export_yaml_string
from upcast.prometheus_metrics_scanner.metrics_parser import MetricInfo


def format_metric_output(metrics: dict[str, MetricInfo]) -> dict[str, Any]:
    """Convert MetricInfo dict to output structure.

    Args:
        metrics: Dictionary of metric names to MetricInfo

    Returns:
        Dictionary ready for YAML serialization
    """
    output = {}

    # Sort metrics alphabetically by name
    for name in sorted(metrics.keys()):
        metric = metrics[name]

        metric_dict: dict[str, Any] = {
            "name": metric.name,  # Original name from definition
            "type": metric.type,
            "help": metric.help,
            "labels": metric.labels,
        }

        # Add optional fields
        if metric.namespace:
            metric_dict["namespace"] = metric.namespace
        if metric.subsystem:
            metric_dict["subsystem"] = metric.subsystem
        if metric.unit:
            metric_dict["unit"] = metric.unit
        if metric.custom_collector:
            metric_dict["custom_collector"] = True
        if metric.buckets:
            metric_dict["buckets"] = metric.buckets

        # Add usages
        metric_dict["usages"] = [
            {
                "location": usage.location,
                "pattern": usage.pattern,
                "statement": usage.statement,
            }
            for usage in metric.usages
        ]

        output[name] = metric_dict

    return output


def export_to_yaml(metrics: dict[str, MetricInfo], output_path: str) -> None:
    """Write metrics to a YAML file.

    Args:
        metrics: Dictionary of metric names to MetricInfo
        output_path: Path to output file
    """
    output = format_metric_output(metrics)
    common_export_yaml(output, output_path)


def export_to_yaml_string(metrics: dict[str, MetricInfo]) -> str:
    """Convert metrics to YAML string.

    Args:
        metrics: Dictionary of metric names to MetricInfo

    Returns:
        YAML formatted string
    """
    output = format_metric_output(metrics)
    return common_export_yaml_string(output)
