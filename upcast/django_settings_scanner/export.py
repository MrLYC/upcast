"""YAML export for Django settings usage."""

from pathlib import Path

import yaml

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

    # Create parent directories if needed
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Write YAML with proper formatting
    with Path(output_path).open("w", encoding="utf-8") as f:
        yaml.dump(
            output,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,  # We already sorted in format_settings_output
            indent=2,
        )


def export_to_yaml_string(settings_dict: dict[str, SettingsVariable]) -> str:
    """Export settings usage to a YAML string.

    Args:
        settings_dict: Dictionary of settings variables

    Returns:
        YAML formatted string
    """
    output = format_settings_output(settings_dict)

    return yaml.dump(
        output,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        indent=2,
    )
