"""URL pattern parsing utilities."""

import re
from typing import Any


def parse_url_pattern(pattern: str) -> dict[str, Any]:
    """Parse a Django URL pattern string.

    Extracts converters from path() style patterns and named groups from regex patterns.

    Args:
        pattern: URL pattern string (e.g., "post/<int:id>/" or "^post/(?P<id>\\d+)/$")

    Returns:
        Dictionary with:
        - converters: Dict of parameter names to converter types
        - named_groups: List of regex named group names
        - is_regex: Whether this appears to be a regex pattern
    """
    result: dict[str, Any] = {
        "converters": {},
        "named_groups": [],
        "is_regex": False,
    }

    # Check if it's a regex pattern (contains regex special chars)
    regex_chars = ["^", "$", "(?", "[", "]", "*", "+", "?", "|"]
    if any(char in pattern for char in regex_chars):
        result["is_regex"] = True
        # Extract named groups from regex
        result["named_groups"] = extract_regex_named_groups(pattern)
    else:
        # Extract path converters
        result["converters"] = extract_path_converters(pattern)

    return result


def extract_path_converters(pattern: str) -> dict[str, str]:
    """Extract path converters from Django path() pattern.

    Args:
        pattern: Path pattern string (e.g., "post/<int:id>/edit/")

    Returns:
        Dictionary mapping parameter names to converter types
        (e.g., {"id": "int"})
    """
    converters = {}

    # Match <converter:name> or <name> (default str converter)
    converter_pattern = r"<(?:(\w+):)?(\w+)>"

    for match in re.finditer(converter_pattern, pattern):
        converter_type = match.group(1) or "str"  # Default to str if no type specified
        param_name = match.group(2)
        converters[param_name] = converter_type

    return converters


def extract_regex_named_groups(pattern: str) -> list[str]:
    """Extract named groups from regex pattern.

    Args:
        pattern: Regex pattern string (e.g., "^post/(?P<id>\\d+)/$")

    Returns:
        List of named group names (e.g., ["id"])
    """
    # Match (?P<name>...) named groups
    named_group_pattern = r"\(\?P<(\w+)>"
    return re.findall(named_group_pattern, pattern)
