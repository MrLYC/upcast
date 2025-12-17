"""Unified export utilities for YAML and JSON with sorted output."""

import json
from pathlib import Path
from typing import Any, Optional

import yaml


def sort_dict_recursive(obj: Any) -> Any:
    """Recursively sort dictionary keys and nested structures.

    Args:
        obj: Object to sort (dict, list, or primitive)

    Returns:
        Sorted version of the object
    """
    if isinstance(obj, dict):
        # Sort dictionary keys alphabetically
        return {k: sort_dict_recursive(v) for k, v in sorted(obj.items())}
    elif isinstance(obj, list):
        # Sort lists if they contain dictionaries with common sortable keys
        # Otherwise, preserve order
        if obj and all(isinstance(item, dict) for item in obj):
            # Try to sort by common keys like 'file', 'line', 'name'
            try:
                # Try sorting by 'file' first, then 'line'
                if all("file" in item for item in obj):
                    sorted_list = sorted(
                        obj,
                        key=lambda x: (x.get("file", ""), x.get("line", 0), x.get("column", 0)),
                    )
                # Try sorting by 'name'
                elif all("name" in item for item in obj):
                    sorted_list = sorted(obj, key=lambda x: x.get("name", ""))
                else:
                    sorted_list = obj  # Keep original order
            except (TypeError, KeyError):
                sorted_list = obj  # Keep original order if sorting fails

            # Recursively sort each item
            return [sort_dict_recursive(item) for item in sorted_list]
        else:
            # For non-dict lists, just recursively sort elements
            return [sort_dict_recursive(item) for item in obj]
    else:
        return obj


def export_to_yaml(data: Any, output_path: str) -> None:
    """Export data to YAML file with sorted keys.

    Args:
        data: Data structure to export
        output_path: Path to output file

    Raises:
        OSError: If file cannot be written
    """
    # Sort data recursively
    sorted_data = sort_dict_recursive(data)

    # Create parent directory if needed
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Write YAML with UTF-8 encoding
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(
            sorted_data,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,  # We already sorted
            indent=2,
        )


def export_to_yaml_string(data: Any) -> str:
    """Export data to YAML string with sorted keys.

    Args:
        data: Data structure to export

    Returns:
        YAML string representation
    """
    # Sort data recursively
    sorted_data = sort_dict_recursive(data)

    return yaml.dump(
        sorted_data,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,  # We already sorted
        indent=2,
    )


def export_to_json(data: Any, output_path: Optional[str] = None) -> str:
    """Export data to JSON with sorted keys.

    Args:
        data: Data structure to export
        output_path: Optional path to output file

    Returns:
        JSON string representation if output_path is None,
        otherwise the output_path
    """
    # Sort data recursively
    sorted_data = sort_dict_recursive(data)

    json_str = json.dumps(sorted_data, ensure_ascii=False, indent=2, sort_keys=True)

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json_str)
        return output_path

    return json_str


# Type alias for Optional import
from typing import Optional  # noqa: E402
