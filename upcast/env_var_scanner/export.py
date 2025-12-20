"""YAML/JSON output formatting for environment variable results."""

from upcast.common.export import export_to_json as common_export_json
from upcast.common.export import export_to_yaml_string as common_export_yaml
from upcast.env_var_scanner.env_var_parser import EnvVarInfo


def export_to_yaml(env_vars: dict[str, EnvVarInfo]) -> str:
    """Export environment variable information to YAML format.

    Args:
        env_vars: Dictionary of environment variable information

    Returns:
        YAML string representation (sorted)
    """
    output = {}

    for name, info in env_vars.items():
        output[name] = {
            "types": info.types,
            "defaults": info.defaults,
            "usages": [
                {
                    "location": usage.location,
                    "statement": usage.statement,
                }
                for usage in info.usages
            ],
            "required": info.required,
        }

    # Use common export with sorting
    return common_export_yaml(output)


def export_to_json(env_vars: dict[str, EnvVarInfo]) -> str:
    """Export environment variable information to JSON format.

    Args:
        env_vars: Dictionary of environment variable information

    Returns:
        JSON string representation (sorted)
    """
    output = {}

    for name, info in env_vars.items():
        output[name] = {
            "types": info.types,
            "defaults": info.defaults,
            "usages": [
                {
                    "location": usage.location,
                    "statement": usage.statement,
                }
                for usage in info.usages
            ],
            "required": info.required,
        }

    # Use common export with sorting
    return common_export_json(output)
