"""YAML export functionality for Django model data."""

from typing import Any

from upcast.common.export import export_to_yaml as common_export_yaml
from upcast.common.export import export_to_yaml_string as common_export_yaml_string


def export_to_yaml(models: dict[str, dict[str, Any]], output_path: str) -> None:
    """Export models to a YAML file.

    Args:
        models: Dictionary of model data keyed by qualified name
        output_path: Path to the output YAML file
    """
    # Format models for output
    formatted_models = format_model_output(models)

    # Use common export with sorting
    common_export_yaml(formatted_models, output_path)


def export_to_yaml_string(models: dict[str, dict[str, Any]]) -> str:
    """Export models to a YAML string.

    Args:
        models: Dictionary of model data keyed by qualified name

    Returns:
        YAML formatted string (sorted)
    """
    # Format models for output
    formatted_models = format_model_output(models)

    # Use common export with sorting
    return common_export_yaml_string(formatted_models)


def format_model_output(models: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Format models dictionary for YAML output.

    Args:
        models: Dictionary of model data keyed by qualified name

    Returns:
        Formatted models dictionary suitable for YAML export
    """
    formatted_models = {}
    for qname, model in models.items():
        formatted_models[qname] = _format_single_model(model)
    return formatted_models


def _format_single_model(model: dict[str, Any]) -> dict[str, Any]:
    """Format a single model dictionary for YAML output.

    Args:
        model: Raw model data dictionary

    Returns:
        Formatted model dictionary suitable for YAML export
    """
    output: dict[str, Any] = {
        "module": model.get("module", ""),
    }

    # Add description from docstring if available
    description = model.get("description")
    if description:
        output["description"] = description

    # Add base classes
    bases = model.get("bases", [])
    if bases:
        output["bases"] = bases

    # Add Meta options (keep abstract in meta, don't move to top level)
    meta = model.get("meta", {})
    if meta:
        output["meta"] = meta

    # Add fields
    fields = model.get("fields", {})
    if fields:
        output["fields"] = {}
        for field_name, field_info in fields.items():
            output["fields"][field_name] = format_field_options(field_info)

    # Add relationships
    relationships = model.get("relationships", {})
    if relationships:
        output["relationships"] = {}
        for rel_name, rel_info in relationships.items():
            output["relationships"][rel_name] = format_field_options(rel_info)

    return output


def format_field_options(field_info: dict[str, Any]) -> dict[str, Any]:
    """Format field options for YAML output.

    Args:
        field_info: Raw field information dictionary

    Returns:
        Formatted field options
    """
    # Start with field type
    output = {"type": field_info.get("type", "Unknown")}

    # Add all other options
    for key, value in field_info.items():
        if key != "type":
            # Normalize value for YAML output
            output[key] = normalize_value(value)

    return output


def normalize_value(value: Any) -> Any:
    """Normalize a value for YAML output.

    Converts AST string representations to more readable forms.

    Args:
        value: Raw value from AST parsing

    Returns:
        Normalized value suitable for YAML
    """
    if isinstance(value, str):
        # Remove unnecessary quotes or module prefixes
        if value.startswith("models."):
            value = value[7:]  # Remove "models." prefix
        # Already a string, return as-is
        return value
    elif isinstance(value, (list, tuple)):
        return [normalize_value(v) for v in value]
    elif isinstance(value, dict):
        return {k: normalize_value(v) for k, v in value.items()}
    else:
        # For numbers, booleans, None, etc.
        return value
