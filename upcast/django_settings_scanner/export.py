"""YAML export for Django settings usage."""

from upcast.common.export import export_to_yaml as common_export_yaml
from upcast.common.export import export_to_yaml_string as common_export_yaml_string
from upcast.django_settings_scanner.settings_parser import SettingsVariable


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
