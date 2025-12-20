"""Export complexity results to YAML/JSON formats."""

import json
from dataclasses import asdict
from typing import Any

import yaml

from upcast.cyclomatic_complexity_scanner.complexity_parser import ComplexityResult


def format_results(
    results_by_module: dict[str, list[ComplexityResult]],
    format_type: str = "yaml",
) -> str:
    """Format complexity results for output.

    Args:
        results_by_module: Dictionary mapping module paths to results
        format_type: Output format ('yaml' or 'json')

    Returns:
        Formatted string output

    Examples:
        >>> results = {"app/utils.py": [ComplexityResult(...)]}
        >>> output = format_results(results, format_type="yaml")
        >>> print(output)
        summary:
          total_functions_scanned: 100
          high_complexity_count: 5
          ...
    """
    # Calculate summary statistics
    summary = _calculate_summary(results_by_module)

    # Build output structure
    output: dict[str, Any] = {
        "summary": summary,
        "modules": {},
    }

    # Sort modules alphabetically
    for module_path in sorted(results_by_module.keys()):
        results = results_by_module[module_path]
        module_results = []

        for result in results:
            result_dict = asdict(result)
            module_results.append(result_dict)

        output["modules"][module_path] = module_results

    # Format output
    if format_type == "json":
        return json.dumps(output, indent=2, ensure_ascii=False)
    else:
        # Set width to a very large value to prevent line wrapping
        return yaml.dump(output, allow_unicode=True, sort_keys=False, default_flow_style=False, width=float("inf"))


def _calculate_summary(results_by_module: dict[str, list[ComplexityResult]]) -> dict[str, Any]:
    """Calculate summary statistics.

    Args:
        results_by_module: Dictionary mapping module paths to results

    Returns:
        Summary dictionary
    """
    total_high_complexity = sum(len(results) for results in results_by_module.values())

    # Count by severity
    severity_counts: dict[str, int] = {}
    for results in results_by_module.values():
        for result in results:
            severity_counts[result.severity] = severity_counts.get(result.severity, 0) + 1

    # Only include severity levels that have non-zero counts
    # Exclude 'healthy' and 'acceptable' (below threshold)
    by_severity = {
        severity: count
        for severity, count in severity_counts.items()
        if severity in ("warning", "high_risk", "critical")
    }

    summary: dict[str, Any] = {
        "high_complexity_count": total_high_complexity,
        "files_analyzed": len(results_by_module),
    }

    if by_severity:
        summary["by_severity"] = by_severity

    return summary
