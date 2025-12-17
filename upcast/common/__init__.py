"""Common utilities shared across scanners."""

from upcast.common.ast_utils import (
    get_qualified_name,
    infer_type_with_fallback,
    infer_value_with_fallback,
    safe_as_string,
)
from upcast.common.export import export_to_json, export_to_yaml, sort_dict_recursive
from upcast.common.file_utils import collect_python_files, find_package_root, validate_path
from upcast.common.patterns import DEFAULT_EXCLUDES, match_patterns, should_exclude

__all__ = [
    # File utilities
    "validate_path",
    "collect_python_files",
    "find_package_root",
    # Pattern matching
    "match_patterns",
    "should_exclude",
    "DEFAULT_EXCLUDES",
    # AST utilities
    "infer_value_with_fallback",
    "infer_type_with_fallback",
    "get_qualified_name",
    "safe_as_string",
    # Export utilities
    "export_to_yaml",
    "export_to_json",
    "sort_dict_recursive",
]
