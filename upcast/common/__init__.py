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
    "DEFAULT_EXCLUDES",
    "collect_python_files",
    "export_to_json",
    # Export utilities
    "export_to_yaml",
    "find_package_root",
    "get_qualified_name",
    "infer_type_with_fallback",
    # AST utilities
    "infer_value_with_fallback",
    # Pattern matching
    "match_patterns",
    "safe_as_string",
    "should_exclude",
    "sort_dict_recursive",
    # File utilities
    "validate_path",
]
