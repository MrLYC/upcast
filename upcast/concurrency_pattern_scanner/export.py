"""YAML export functionality for concurrency patterns."""

from typing import Any

import yaml


def _calculate_summary(patterns: dict[str, dict[str, list[dict[str, Any]]]]) -> dict[str, Any]:
    """Calculate summary statistics for concurrency patterns.

    Args:
        patterns: Dictionary of patterns grouped by category and type

    Returns:
        Summary dictionary with statistics
    """
    total_patterns = 0
    by_category: dict[str, int] = {}

    for category, pattern_types in patterns.items():
        category_count = sum(len(usages) for usages in pattern_types.values())
        if category_count > 0:
            by_category[category] = category_count
            total_patterns += category_count

    return {
        "total_patterns": total_patterns,
        "by_category": by_category,
    }


def format_concurrency_output(patterns: dict[str, dict[str, list[dict[str, Any]]]]) -> str:
    """Format concurrency patterns as YAML output.

    Args:
        patterns: Dictionary of patterns grouped by category and type

    Returns:
        YAML formatted string
    """
    # Calculate summary
    summary = _calculate_summary(patterns)

    # Filter out empty categories
    filtered = {
        category: pattern_types
        for category, pattern_types in patterns.items()
        if any(pattern_types.values())  # At least one pattern type has items
    }

    if not filtered:
        output = {
            "summary": {"total_patterns": 0, "by_category": {}},
            "concurrency_patterns": {},
        }
    else:
        # Build output structure with summary first
        output = {
            "summary": summary,
            "concurrency_patterns": filtered,
        }

    # Use safe_dump with custom settings for readability
    yaml_str = yaml.safe_dump(
        output,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        width=120,
    )

    return yaml_str


def export_to_yaml(patterns: dict[str, dict[str, list[dict[str, Any]]]], output_path: str) -> None:
    """Export concurrency patterns to a YAML file.

    Args:
        patterns: Dictionary of patterns grouped by category and type
        output_path: Path to output YAML file
    """
    yaml_content = format_concurrency_output(patterns)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)
