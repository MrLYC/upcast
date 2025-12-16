"""YAML/JSON output formatting for environment variable results."""

import json

import yaml

from upcast.env_var_scanner.env_var_parser import EnvVarInfo


def export_to_yaml(env_vars: dict[str, EnvVarInfo]) -> str:
    """Export environment variable information to YAML format.

    Args:
        env_vars: Dictionary of environment variable information

    Returns:
        YAML string representation
    """
    output = {}

    for name, info in sorted(env_vars.items()):
        output[name] = {
            "types": info.types,
            "defaults": info.defaults,
            "usages": [
                {
                    "location": usage.location,
                    "statement": usage.statement,
                    "type": usage.type,
                    "default": usage.default,
                    "required": usage.required,
                }
                for usage in sorted(info.usages, key=lambda u: u.location)
            ],
            "required": info.required,
        }

    return yaml.dump(output, default_flow_style=False, sort_keys=False)


def export_to_json(env_vars: dict[str, EnvVarInfo]) -> str:
    """Export environment variable information to JSON format.

    Args:
        env_vars: Dictionary of environment variable information

    Returns:
        JSON string representation
    """
    output = {}

    for name, info in sorted(env_vars.items()):
        output[name] = {
            "types": info.types,
            "defaults": info.defaults,
            "usages": [
                {
                    "location": usage.location,
                    "statement": usage.statement,
                    "type": usage.type,
                    "default": usage.default,
                    "required": usage.required,
                }
                for usage in sorted(info.usages, key=lambda u: u.location)
            ],
            "required": info.required,
        }

    return json.dumps(output, indent=2)
