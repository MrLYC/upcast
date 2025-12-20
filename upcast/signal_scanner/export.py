"""YAML export for signal scan results."""

from pathlib import Path
from typing import Any

import yaml


def format_signal_output(results: dict[str, Any]) -> dict[str, Any]:  # noqa: C901
    """Format signal results for YAML export using flat list structure.

    Args:
        results: Raw results from SignalChecker

    Returns:
        Formatted dictionary with flat list of signals
    """
    signals_list = []

    # Process Django signals
    if "django" in results:
        for category, signals in results["django"].items():
            if category == "unused_custom_signals":
                # Handle unused signals separately
                for signal_def in signals:
                    signals_list.append({
                        "signal": signal_def.get("name", "unknown"),
                        "type": "django",
                        "category": "unused_custom_signals",
                        "file": signal_def.get("file", ""),
                        "line": signal_def.get("line", 0),
                        "status": "unused",
                    })
                continue

            # Process regular signals
            for signal_name, signal_data in signals.items():
                if isinstance(signal_data, dict) and "receivers" in signal_data:
                    receivers = []
                    for handler in signal_data["receivers"]:
                        handler_entry = {
                            "handler": handler["handler"],
                            "file": handler["file"],
                            "line": handler["line"],
                        }
                        if "sender" in handler:
                            handler_entry["sender"] = handler["sender"]
                        if "context" in handler:
                            handler_entry["context"] = handler["context"]
                        receivers.append(handler_entry)

                    signals_list.append({
                        "signal": signal_name,
                        "type": "django",
                        "category": category,
                        "receivers": receivers,
                    })

    # Process Celery signals
    if "celery" in results:
        for category, signals in results["celery"].items():
            for signal_name, signal_data in signals.items():
                if isinstance(signal_data, dict) and "receivers" in signal_data:
                    receivers = []
                    for handler in signal_data["receivers"]:
                        handler_entry = {
                            "handler": handler["handler"],
                            "file": handler["file"],
                            "line": handler["line"],
                        }
                        if "context" in handler:
                            handler_entry["context"] = handler["context"]
                        receivers.append(handler_entry)

                    signals_list.append({
                        "signal": signal_name,
                        "type": "celery",
                        "category": category,
                        "receivers": receivers,
                    })

    return {"signals": signals_list}


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
