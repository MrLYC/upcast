"""YAML export for signal scan results."""

from pathlib import Path
from typing import Any

import yaml


def format_signal_output(results: dict[str, Any]) -> dict[str, Any]:  # noqa: C901
    """Format signal results for YAML export.

    Args:
        results: Raw results from SignalChecker

    Returns:
        Formatted dictionary ready for YAML export
    """
    output: dict[str, Any] = {}

    # Format Django signals
    if "django" in results:
        django_output: dict[str, Any] = {}

        for category, signals in results["django"].items():
            if category == "unused_custom_signals":
                # Special handling for unused signals
                django_output[category] = signals
                continue

            category_output: dict[str, Any] = {}

            for signal_name, signal_data in signals.items():
                # Handle new structure: {receivers: [], senders: [], usages: []}
                if isinstance(signal_data, dict) and "receivers" in signal_data:
                    # Format the nested structure
                    formatted_signal: dict[str, Any] = {}

                    # Format receivers
                    if "receivers" in signal_data:
                        formatted_receivers = []
                        for handler in signal_data["receivers"]:
                            handler_entry: dict[str, Any] = {
                                "handler": handler["handler"],
                                "file": handler["file"],
                                "line": handler["line"],
                            }
                            # Add sender if present
                            if "sender" in handler:
                                handler_entry["sender"] = handler["sender"]
                            # Add context if present
                            if "context" in handler:
                                handler_entry["context"] = handler["context"]
                            formatted_receivers.append(handler_entry)
                        formatted_signal["receivers"] = formatted_receivers

                    category_output[signal_name] = formatted_signal
                else:
                    # Shouldn't happen, but handle gracefully
                    category_output[signal_name] = {"receivers": []}

            if category_output:
                django_output[category] = category_output

        if django_output:
            output["django"] = django_output

    # Format Celery signals
    if "celery" in results:
        celery_output: dict[str, Any] = {}

        for category, signals in results["celery"].items():
            category_output: dict[str, Any] = {}

            for signal_name, signal_data in signals.items():
                # Handle new structure: {receivers: [], senders: [], usages: []}
                if isinstance(signal_data, dict) and "receivers" in signal_data:
                    # Format the nested structure
                    formatted_signal: dict[str, Any] = {}

                    # Format receivers
                    if "receivers" in signal_data:
                        formatted_receivers = []
                        for handler in signal_data["receivers"]:
                            handler_entry: dict[str, Any] = {
                                "handler": handler["handler"],
                                "file": handler["file"],
                                "line": handler["line"],
                            }
                            # Add context if present
                            if "context" in handler:
                                handler_entry["context"] = handler["context"]
                            formatted_receivers.append(handler_entry)
                        formatted_signal["receivers"] = formatted_receivers

                    category_output[signal_name] = formatted_signal
                else:
                    # Shouldn't happen, but handle gracefully
                    category_output[signal_name] = {"receivers": []}

            if category_output:
                celery_output[category] = category_output

        if celery_output:
            output["celery"] = celery_output

    return output


def export_to_yaml(results: dict[str, Any], output_path: str) -> None:
    """Export signal results to YAML file.

    Args:
        results: Signal scan results
        output_path: Path to write YAML file
    """
    formatted_output = format_signal_output(results)

    # Ensure parent directory exists
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Write YAML with nice formatting
    with output_file.open("w") as f:
        yaml.dump(
            formatted_output,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )
