"""Export blocking operations to YAML/JSON formats."""

import json
from pathlib import Path
from typing import Any

from upcast.blocking_operation_scanner.operation_parser import BlockingOperation
from upcast.common.export import export_to_yaml_string, sort_dict_recursive


def format_operations_output(
    operations: list[BlockingOperation],
    base_path: Path | None = None,
) -> dict[str, Any]:
    """Format blocking operations for export.

    Groups operations by category and converts file paths to relative paths.

    Args:
        operations: List of blocking operations
        base_path: Base path for converting to relative paths

    Returns:
        Dictionary with categorized operations and summary
    """
    # Convert to relative paths if base_path provided
    if base_path:
        base_path = base_path.resolve()
        for op in operations:
            try:
                file_path = Path(op.file).resolve()
                op.file = str(file_path.relative_to(base_path))
            except ValueError:
                # File is outside base_path, keep absolute
                pass

    # Group by category
    categories: dict[str, list[dict[str, Any]]] = {
        "time_based": [],
        "database": [],
        "synchronization": [],
        "subprocess": [],
    }

    for op in operations:
        op_dict = op.to_dict()
        category_key = op.type.value.split(".")[0]
        if category_key in categories:
            categories[category_key].append(op_dict)

    # Sort operations within each category by file and line
    for category in categories.values():
        category.sort(key=lambda x: (x["location"], x["type"]))

    # Add summary
    total_count = len(operations)
    category_counts = {cat: len(ops) for cat, ops in categories.items() if ops}

    # Get unique files
    files = sorted({op.file for op in operations})

    result = {
        "summary": {
            "total_operations": total_count,
            "by_category": category_counts,
            "files_analyzed": len(files),
        },
        "operations": {k: v for k, v in categories.items() if v},
    }

    return sort_dict_recursive(result)


def export_to_yaml(operations: list[BlockingOperation], base_path: Path | None = None) -> str:
    """Export blocking operations to YAML format.

    Args:
        operations: List of blocking operations
        base_path: Base path for converting to relative paths

    Returns:
        YAML string
    """
    data = format_operations_output(operations, base_path)
    return export_to_yaml_string(data)


def export_to_json(
    operations: list[BlockingOperation],
    base_path: Path | None = None,
) -> str:
    """Export blocking operations to JSON format.

    Args:
        operations: List of blocking operations
        base_path: Base path for converting to relative paths

    Returns:
        JSON string
    """
    data = format_operations_output(operations, base_path)
    return json.dumps(data, indent=2, ensure_ascii=False)
