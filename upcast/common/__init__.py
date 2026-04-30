"""Common utilities shared across scanners."""

from upcast.common.ast_utils import (
    get_qualified_name,
    safe_as_string,
)
from upcast.common.astroid_matcher import MatchResult, find_matches, match

# CSTASTMapper depends on the optional extra 'ast-grep-py'.
# The class is always importable; an ImportError is raised only at instantiation
# time when the dependency is missing (see cst_ast_mapper module for details).
from upcast.common.cst_ast_mapper import CSTASTMapper
from upcast.common.export import export_to_json, export_to_yaml, sort_dict_recursive
from upcast.common.file_utils import collect_python_files, find_package_root, validate_path
from upcast.common.hybrid_scan_pipeline import (
    Finding,
    LocateStage,
    MapStage,
    PipelineRunResult,
    PipelineSpec,
    ProjectStage,
    SemanticDecision,
    SemanticFilterStage,
    StructuralCandidate,
    run_pipeline,
)
from upcast.common.inference import InferenceResult, StringPattern, infer_string_pattern, infer_type, infer_value
from upcast.common.patterns import DEFAULT_EXCLUDES, match_patterns, should_exclude

__all__ = [
    "DEFAULT_EXCLUDES",
    "CSTASTMapper",
    "Finding",
    "InferenceResult",
    "LocateStage",
    "MapStage",
    "MatchResult",
    "PipelineRunResult",
    "PipelineSpec",
    "ProjectStage",
    "SemanticDecision",
    "SemanticFilterStage",
    "StringPattern",
    "StructuralCandidate",
    "collect_python_files",
    "export_to_json",
    "export_to_yaml",
    "find_matches",
    "find_package_root",
    "get_qualified_name",
    "infer_string_pattern",
    "infer_type",
    "infer_value",
    "match",
    "match_patterns",
    "run_pipeline",
    "safe_as_string",
    "should_exclude",
    "sort_dict_recursive",
    "validate_path",
]
