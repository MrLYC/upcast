"""YAML export functions."""

from pathlib import Path
from typing import Any

import yaml

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

    # Create parent directories if needed
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Write YAML file
    with Path(output_path).open("w", encoding="utf-8") as f:
        yaml.dump(
            output,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            indent=2,
        )


def export_to_yaml_string(metrics: dict[str, MetricInfo]) -> str:
    """Convert metrics to YAML string.

    Args:
        metrics: Dictionary of metric names to MetricInfo

    Returns:
        YAML formatted string
    """
    output = format_metric_output(metrics)

    return yaml.dump(
        output,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        indent=2,
    )
