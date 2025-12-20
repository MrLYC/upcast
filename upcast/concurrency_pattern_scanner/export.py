"""YAML export functionality for concurrency patterns."""

from typing import Any

import yaml


def format_concurrency_output(patterns: dict[str, dict[str, list[dict[str, Any]]]]) -> str:
    """Format concurrency patterns as YAML output.

    Args:
        patterns: Dictionary of patterns grouped by category and type

    Returns:
        YAML formatted string
    """
    # Filter out empty categories
    filtered = {
        category: pattern_types
        for category, pattern_types in patterns.items()
        if any(pattern_types.values())  # At least one pattern type has items
    }

    if not filtered:
        return "concurrency_patterns: {}\n"

    # Build output structure
    output = {"concurrency_patterns": filtered}

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
