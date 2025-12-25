"""Unified export utilities for YAML and JSON with sorted output."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import yaml

from upcast.models.base import ScannerOutput


# Configure YAML to output None values as 'null'
def represent_none(self, _):
    """Represent None as 'null' in YAML output."""
    return self.represent_scalar("tag:yaml.org,2002:null", "null")


yaml.add_representer(type(None), represent_none)


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


def export_scanner_output(
    output: ScannerOutput | dict[str, Any],
    file_path: str,
    format: str = "yaml",  # noqa: A002
    scanner_name: str | None = None,
    scanner_version: str | None = None,
    include_metadata: bool = True,
) -> None:
    """Export scanner output with optional metadata injection.

    This is the main export function for all scanners. It handles both
    Pydantic ScannerOutput models and legacy dict outputs.

    Args:
        output: Scanner output (ScannerOutput or dict)
        file_path: Path to output file
        format: Output format ("yaml" or "json")
        scanner_name: Optional scanner name to inject in metadata
        scanner_version: Optional scanner version to inject
        include_metadata: Whether to include metadata in output

    Raises:
        ValueError: If format is invalid
        OSError: If file cannot be written
    """
    # Convert ScannerOutput to dict
    # Note: Keep None values for critical fields like view_module and view_name
    data = output.model_dump(mode="json", exclude_none=False) if isinstance(output, ScannerOutput) else dict(output)

    # Inject metadata if requested
    if include_metadata:
        metadata = data.setdefault("metadata", {})

        if scanner_name:
            metadata["scanner_name"] = scanner_name

        if scanner_version:
            metadata["scanner_version"] = scanner_version

        # Always add timestamp
        metadata["scan_timestamp"] = datetime.now().isoformat()

    # Export based on format
    if format.lower() == "json":
        export_to_json(data, file_path)
    elif format.lower() == "yaml":
        export_to_yaml(data, file_path)
    else:
        raise ValueError(f"Invalid format: {format}. Must be 'yaml' or 'json'.")
