"""YAML export functionality for Django URL pattern data."""

from typing import Any

from upcast.common.export import export_to_yaml as common_export_yaml
from upcast.common.export import export_to_yaml_string as common_export_yaml_string


def export_to_yaml(url_modules: dict[str, list[dict[str, Any]]], output_path: str) -> None:
    """Export URL patterns to a YAML file.

    Args:
        url_modules: Dictionary mapping module paths to lists of URL patterns
        output_path: Path to the output YAML file
    """
    # Format for output
    formatted = format_url_output(url_modules)

    # Use common export with sorting
    common_export_yaml(formatted, output_path)


def export_to_yaml_string(url_modules: dict[str, list[dict[str, Any]]]) -> str:
    """Export URL patterns to a YAML string.

    Args:
        url_modules: Dictionary mapping module paths to lists of URL patterns

    Returns:
        YAML formatted string (sorted)
    """
    # Format for output
    formatted = format_url_output(url_modules)

    # Use common export with sorting
    return common_export_yaml_string(formatted)


def format_url_output(url_modules: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Format URL patterns dictionary for YAML output.

    Args:
        url_modules: Dictionary mapping module paths to lists of URL patterns

    Returns:
        Formatted dictionary suitable for YAML export
    """
    output = {}

    for module_path, patterns in url_modules.items():
        output[module_path] = {"urlpatterns": [_format_single_pattern(pattern) for pattern in patterns]}

    return output


def _format_single_pattern(pattern: dict[str, Any]) -> dict[str, Any]:  # noqa: C901
    """Format a single URL pattern for YAML output.

    Args:
        pattern: Raw pattern data dictionary

    Returns:
        Formatted pattern dictionary
    """
    output: dict[str, Any] = {}

    # Always include type
    if "type" in pattern:
        output["type"] = pattern["type"]

    # Always include pattern with clear indication for empty/missing patterns
    if "pattern" in pattern:
        pattern_value = pattern["pattern"]
        if pattern_value is None:
            output["pattern"] = "<not-detected>"
        elif pattern_value == "":
            output["pattern"] = "<root>"
        else:
            output["pattern"] = pattern_value

    # Check if this is a dynamic pattern
    if pattern.get("type") == "dynamic":
        if pattern.get("note"):
            output["note"] = pattern["note"]
        return output

    # Check if this is an include
    if pattern.get("include_module"):
        output["include_module"] = pattern["include_module"]
        if pattern.get("namespace"):
            output["namespace"] = pattern["namespace"]
    # Check if this is a router registration
    elif pattern.get("type") == "router_registration":
        if pattern.get("viewset_module"):
            output["viewset_module"] = pattern["viewset_module"]
        if pattern.get("viewset_name"):
            output["viewset_name"] = pattern["viewset_name"]
        if pattern.get("basename"):
            output["basename"] = pattern["basename"]
        if pattern.get("router_type"):
            output["router_type"] = pattern["router_type"]
    else:
        # Regular view pattern
        if pattern.get("view_module"):
            output["view_module"] = pattern["view_module"]
        if pattern.get("view_name"):
            output["view_name"] = pattern["view_name"]

    # Add name if present
    if pattern.get("name"):
        output["name"] = pattern["name"]

    # Add description if present
    if pattern.get("description"):
        output["description"] = pattern["description"]

    # Add converters if present
    if pattern.get("converters"):
        output["converters"] = pattern["converters"]

    # Add named groups if present (for regex patterns)
    if pattern.get("named_groups"):
        output["named_groups"] = pattern["named_groups"]

    # Mark special view types
    if pattern.get("is_partial"):
        output["is_partial"] = True
    if pattern.get("is_conditional"):
        output["is_conditional"] = True

    return output
