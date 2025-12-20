"""YAML export for Django settings usage."""

from upcast.common.export import export_to_yaml as common_export_yaml
from upcast.common.export import export_to_yaml_string as common_export_yaml_string
from upcast.django_settings_scanner.settings_parser import SettingsModule, SettingsVariable


def format_settings_output(settings_dict: dict[str, SettingsVariable]) -> dict:
    """Convert settings dict to YAML-ready structure.

    Args:
        settings_dict: Dictionary of settings variables

    Returns:
        Dictionary ready for YAML serialization
    """
    output = {}

    # Sort variables alphabetically
    for var_name in sorted(settings_dict.keys()):
        var = settings_dict[var_name]

        # Sort locations by (file, line)
        sorted_locations = sorted(var.locations, key=lambda loc: (loc.file, loc.line))

        output[var_name] = {
            "count": var.count,
            "locations": [
                {
                    "file": loc.file,
                    "line": loc.line,
                    "column": loc.column,
                    "pattern": loc.pattern,
                    "code": loc.code,
                }
                for loc in sorted_locations
            ],
        }

    return output


def export_to_yaml(settings_dict: dict[str, SettingsVariable], output_path: str) -> None:
    """Export settings usage to a YAML file.

    Args:
        settings_dict: Dictionary of settings variables
        output_path: Path to output YAML file
    """
    output = format_settings_output(settings_dict)

    # Use common export with sorting
    common_export_yaml(output, output_path)


def export_to_yaml_string(settings_dict: dict[str, SettingsVariable]) -> str:
    """Export settings usage to a YAML string.

    Args:
        settings_dict: Dictionary of settings variables

    Returns:
        YAML formatted string (sorted)
    """
    output = format_settings_output(settings_dict)

    # Use common export with sorting
    return common_export_yaml_string(output)


def format_definitions_output(modules: dict[str, SettingsModule]) -> dict:
    """Convert settings modules to YAML-ready structure.

    Args:
        modules: Dictionary of settings modules by module path

    Returns:
        Dictionary ready for YAML serialization, structured as:
        {
            "module.path": {
                "SETTING_NAME": {
                    "value": <value>,
                    "line": <line_number>,
                    "type": <type_name>,
                    "overrides": "base.module"  # only if present
                },
                "__star_imports__": [<module_paths>],  # only if present
                "__dynamic_imports__": [  # only if present
                    {"pattern": "...", "file": "...", "line": ...}
                ]
            }
        }
    """
    output = {}

    # Sort modules alphabetically
    for module_path in sorted(modules.keys()):
        module = modules[module_path]
        module_output = {}

        # Sort definitions alphabetically
        for setting_name in sorted(module.definitions.keys()):
            definition = module.definitions[setting_name]

            # Check if value is dynamic (wrapped in backticks)
            if (
                isinstance(definition.value, str)
                and definition.value.startswith("`")
                and definition.value.endswith("`")
            ):
                # Dynamic value - use statement field
                setting_data = {
                    "statement": definition.value[1:-1],  # Remove backticks
                    "lineno": definition.line,
                }
            else:
                # Static value - use value field
                setting_data = {
                    "value": definition.value,
                    "lineno": definition.line,
                }

            # Only include overrides if present
            if definition.overrides:
                setting_data["overrides"] = definition.overrides

            module_output[setting_name] = setting_data

        # Add star imports if present
        if module.star_imports:
            module_output["__star_imports__"] = sorted(module.star_imports)

        # Add dynamic imports if present
        if module.dynamic_imports:
            module_output["__dynamic_imports__"] = [
                {
                    "pattern": imp.pattern,
                    "base_module": imp.base_module,
                    "file": imp.file,
                    "line": imp.line,
                }
                for imp in sorted(
                    module.dynamic_imports,
                    key=lambda x: (x.file, x.line),
                )
            ]

        # Only include module if it has any content (definitions, star imports, or dynamic imports)
        if module_output:
            output[module_path] = module_output

    return output


def export_definitions_only(modules: dict[str, SettingsModule], output_path: str) -> None:
    """Export settings definitions to a YAML file.

    Args:
        modules: Dictionary of settings modules by module path
        output_path: Path to output YAML file
    """
    output = {"definitions": format_definitions_output(modules)}
    common_export_yaml(output, output_path)


def export_usages_only(settings_dict: dict[str, SettingsVariable], output_path: str) -> None:
    """Export settings usages to a YAML file (backward compatible format).

    Args:
        settings_dict: Dictionary of settings variables
        output_path: Path to output YAML file
    """
    output = format_settings_output(settings_dict)
    common_export_yaml(output, output_path)


def export_combined(
    modules: dict[str, SettingsModule],
    settings_dict: dict[str, SettingsVariable],
    output_path: str,
) -> None:
    """Export both definitions and usages to a YAML file.

    Args:
        modules: Dictionary of settings modules by module path
        settings_dict: Dictionary of settings variables
        output_path: Path to output YAML file
    """
    output = {
        "definitions": format_definitions_output(modules),
        "usages": format_settings_output(settings_dict),
    }
    common_export_yaml(output, output_path)
