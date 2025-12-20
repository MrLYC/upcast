"""YAML/JSON output formatting for environment variable results."""

from typing import Any

from upcast.common.export import export_to_json as common_export_json
from upcast.common.export import export_to_yaml_string as common_export_yaml
from upcast.env_var_scanner.env_var_parser import EnvVarInfo


def _calculate_summary(env_vars: dict[str, EnvVarInfo]) -> dict[str, Any]:
    """Calculate summary statistics for environment variables.

    Args:
        env_vars: Dictionary of environment variable information

    Returns:
        Summary dictionary with statistics
    """
    total = len(env_vars)
    required = sum(1 for info in env_vars.values() if info.required)
    optional = total - required

    return {
        "total_env_vars": total,
        "required_count": required,
        "optional_count": optional,
    }


def export_to_yaml(env_vars: dict[str, EnvVarInfo]) -> str:
    """Export environment variable information to YAML format.

    Args:
        env_vars: Dictionary of environment variable information

    Returns:
        YAML string representation (sorted)
    """
    # Calculate summary
    summary = _calculate_summary(env_vars)

    # Build env vars dictionary
    env_vars_dict = {}
    for name, info in env_vars.items():
        env_vars_dict[name] = {
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

    # Build output with summary first
    output = {
        "summary": summary,
        "env_vars": env_vars_dict,
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
    # Calculate summary
    summary = _calculate_summary(env_vars)

    # Build env vars dictionary
    env_vars_dict = {}
    for name, info in env_vars.items():
        env_vars_dict[name] = {
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

    # Build output with summary first
    output = {
        "summary": summary,
        "env_vars": env_vars_dict,
    }

    # Use common export with sorting
    return common_export_json(output)
