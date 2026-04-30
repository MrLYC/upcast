"""Typed core contracts for the hybrid structural + semantic scan pipeline."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Literal

import astroid

from upcast.common.ast_utils import get_qualified_name
from upcast.common.cst_ast_mapper import CSTASTMapper

try:
    from ast_grep_py import SgRoot
except ImportError:  # pragma: no cover - exercised through CSTASTMapper usage
    SgRoot = None  # type: ignore[assignment]


DecisionStatus = Literal["confirmed", "rejected", "unknown"]
_SINGLE_CAPTURE_PATTERN = re.compile(r"\$([A-Z][A-Z0-9_]*)")
_MULTI_CAPTURE_PATTERN = re.compile(r"\$\$\$([A-Z][A-Z0-9_]*)")


@dataclass(frozen=True)
class LocateStage:
    """Structural locate stage configuration for v1."""

    pattern: str


@dataclass(frozen=True)
class MapStage:
    """Marker config for CST-to-astroid mapping stage."""


@dataclass(frozen=True)
class SemanticFilterStage:
    """Semantic filter stage configuration for v1."""

    predicate: str
    target: str = "self"
    rule: dict[str, Any] | None = None


@dataclass(frozen=True)
class ProjectStage:
    """Projection stage configuration for final findings."""

    kind: str


@dataclass(frozen=True)
class PipelineSpec:
    """Typed single-round pipeline specification for v1."""

    name: str
    locate: LocateStage
    map: MapStage
    semantic_filters: list[SemanticFilterStage]
    project: ProjectStage


@dataclass(frozen=True)
class StructuralCandidate:
    """Intermediate artifact produced by the structural stage."""

    file_path: str
    structural_span: dict[str, list[int]]
    captures: dict[str, Any] = field(default_factory=dict)
    missing_captures: list[str] = field(default_factory=list)
    snippet: str = ""
    stage_name: str = "locate"


@dataclass(frozen=True)
class SemanticDecision:
    """Semantic verification result preserving three-state outcomes."""

    status: DecisionStatus
    reason_codes: list[str] = field(default_factory=list)
    facts: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        allowed_statuses = {"confirmed", "rejected", "unknown"}
        if self.status not in allowed_statuses:
            allowed = ", ".join(sorted(allowed_statuses))
            raise ValueError(f"SemanticDecision.status must be one of: {allowed}")


@dataclass(frozen=True)
class Finding:
    """Final shaped finding emitted by the pipeline."""

    kind: str
    primary_span: dict[str, list[int]]
    evidence_chain: list[str] = field(default_factory=list)
    fields: dict[str, Any] = field(default_factory=dict)
    related_spans: list[dict[str, list[int]]] = field(default_factory=list)


@dataclass(frozen=True)
class PipelineRunResult:
    """Result bundle produced by one single-round pipeline execution."""

    candidates: list[StructuralCandidate]
    decisions: list[SemanticDecision]
    findings: list[Finding]


def run_pipeline(*, spec: PipelineSpec, source: str, file_path: str) -> PipelineRunResult:
    """Execute the minimal v1 single-round pipeline contract."""
    mapper = _build_mapper(source, file_path)
    candidates = _locate_candidates(mapper=mapper, pattern=spec.locate.pattern, file_path=file_path)
    decisions = [_evaluate_candidate(candidate=candidate, filters=spec.semantic_filters) for candidate in candidates]
    findings = _project_findings(spec=spec, candidates=candidates, decisions=decisions)
    return PipelineRunResult(candidates=candidates, decisions=decisions, findings=findings)


def _build_mapper(source: str, file_path: str) -> CSTASTMapper:
    if SgRoot is None:
        raise ImportError("run_pipeline requires the optional dependency 'ast-grep-py'")
    return CSTASTMapper(SgRoot(source, "python"), astroid.parse(source, path=file_path))


def _locate_candidates(*, mapper: CSTASTMapper, pattern: str, file_path: str) -> list[StructuralCandidate]:
    single_capture_names = _extract_single_capture_names(pattern)
    multi_capture_names = _extract_multi_capture_names(pattern)
    candidates: list[StructuralCandidate] = []

    for sg_node in mapper.search_cst(pattern):
        single_capture_matches = mapper.cst_to_ast_by_matches(sg_node, *single_capture_names)
        multi_capture_matches = mapper.cst_to_ast_by_multiple_matches(sg_node, *multi_capture_names)
        ast_node = mapper.cst_to_ast(sg_node)
        if ast_node is None:
            missing_captures = [
                "self",
                *[name for name in single_capture_names if name not in single_capture_matches],
                *[name for name in multi_capture_names if name not in multi_capture_matches],
            ]
            candidates.append(
                StructuralCandidate(
                    file_path=file_path,
                    structural_span=_sg_node_span(sg_node),
                    captures={**single_capture_matches, **multi_capture_matches},
                    missing_captures=missing_captures,
                    snippet=_sg_node_text(sg_node),
                    stage_name="map",
                )
            )
            continue

        captures: dict[str, Any] = {}
        captures.update(single_capture_matches)
        captures.update(multi_capture_matches)
        captures["self"] = ast_node
        missing_captures = [
            *[name for name in single_capture_names if name not in single_capture_matches],
            *[name for name in multi_capture_names if name not in multi_capture_matches],
        ]

        candidates.append(
            StructuralCandidate(
                file_path=file_path,
                structural_span=_node_span(ast_node),
                captures=captures,
                missing_captures=missing_captures,
                snippet=ast_node.as_string(),
                stage_name="locate",
            )
        )

    return candidates


def _evaluate_candidate(
    *, candidate: StructuralCandidate, filters: list[SemanticFilterStage]
) -> SemanticDecision:
    class_node = candidate.captures.get("NAME") or candidate.captures.get("self")
    class_name = getattr(class_node, "name", candidate.snippet)
    facts: dict[str, Any] = {"class_name": class_name}
    reason_codes: list[str] = []

    if "self" in candidate.missing_captures:
        return SemanticDecision(
            status="unknown",
            reason_codes=["map-failure"],
            facts=facts,
            errors=["primary CST-to-astroid mapping failed"],
        )

    status: DecisionStatus = "confirmed"
    for filter_stage in filters:
        filter_status, filter_reason_codes, filter_facts = _evaluate_filter(candidate=candidate, filter_stage=filter_stage)
        reason_codes.extend(filter_reason_codes)
        facts.update(filter_facts)

        if filter_status == "rejected":
            return SemanticDecision(status="rejected", reason_codes=reason_codes, facts=facts)
        if filter_status == "unknown":
            status = "unknown"

    return SemanticDecision(status=status, reason_codes=reason_codes, facts=facts)


def _evaluate_filter(*, candidate: StructuralCandidate, filter_stage: SemanticFilterStage) -> tuple[DecisionStatus, list[str], dict[str, Any]]:
    if filter_stage.target != "self" and filter_stage.target in candidate.missing_captures:
        return (
            "unknown",
            ["capture-map-failure"],
            {"missing_target": filter_stage.target},
        )

    targets = _resolve_filter_targets(candidate=candidate, target=filter_stage.target)
    if filter_stage.predicate != "inherits_from":
        raise ValueError(f"Unsupported semantic predicate: {filter_stage.predicate}")

    qname_rule = (filter_stage.rule or {}).get("qname")
    if qname_rule is None:
        raise ValueError("'inherits_from' requires a qname rule")

    matched_qnames: list[str] = []
    unresolved_targets = 0

    for target in targets:
        qname, success = get_qualified_name(target)
        if success:
            if _qname_matches(qname, qname_rule):
                matched_qnames.append(qname)
        else:
            unresolved_targets += 1

    if matched_qnames:
        return (
            "confirmed",
            ["inherits-from-target"],
            {"matched_qnames": matched_qnames},
        )
    if unresolved_targets:
        return (
            "unknown",
            ["inheritance-qname-unresolved"],
            {"unresolved_targets": unresolved_targets},
        )

    return ("rejected", ["does-not-inherit-from-target"], {})


def _resolve_filter_targets(*, candidate: StructuralCandidate, target: str) -> list[Any]:
    if target == "self":
        self_node = candidate.captures.get("self")
        return [] if self_node is None else [self_node]

    if target not in candidate.captures:
        raise ValueError(f"Unknown semantic filter target: {target}")

    captured = candidate.captures[target]
    if captured is None:
        return []
    if isinstance(captured, list):
        return captured
    return [captured]


def _project_findings(
    *, spec: PipelineSpec, candidates: list[StructuralCandidate], decisions: list[SemanticDecision]
) -> list[Finding]:
    findings: list[Finding] = []

    for candidate, decision in zip(candidates, decisions, strict=True):
        if decision.status != "confirmed":
            continue

        evidence_chain = ["located-class", "mapped-classdef"]
        evidence_chain.append("confirmed-inheritance")

        findings.append(
            Finding(
                kind=spec.project.kind,
                primary_span=candidate.structural_span,
                evidence_chain=evidence_chain,
                fields={
                    "class_name": decision.facts.get("class_name"),
                    "decision_status": decision.status,
                },
            )
        )

    return findings


def _extract_single_capture_names(pattern: str) -> tuple[str, ...]:
    multi_names = set(_extract_multi_capture_names(pattern))
    return tuple(name for name in _SINGLE_CAPTURE_PATTERN.findall(pattern) if name not in multi_names)


def _extract_multi_capture_names(pattern: str) -> tuple[str, ...]:
    return tuple(_MULTI_CAPTURE_PATTERN.findall(pattern))


def _node_span(node: Any) -> dict[str, list[int]]:
    return {
        "start": [node.lineno, node.col_offset],
        "end": [node.end_lineno, node.end_col_offset],
    }


def _sg_node_span(sg_node: Any) -> dict[str, list[int]]:
    rng = sg_node.range()
    return {
        "start": [rng.start.line + 1, rng.start.column],
        "end": [rng.end.line + 1, rng.end.column],
    }


def _sg_node_text(sg_node: Any) -> str:
    text = sg_node.text()
    if isinstance(text, bytes):
        return text.decode("utf-8")
    return str(text)


def _qname_matches(qname: str, qname_rule: Any) -> bool:
    if isinstance(qname_rule, str):
        return qname == qname_rule
    if not isinstance(qname_rule, dict):
        return False

    exact = qname_rule.get("exact")
    prefix = qname_rule.get("prefix")
    suffix = qname_rule.get("suffix")

    if exact is not None and qname != exact:
        return False
    if prefix is not None and not qname.startswith(prefix):
        return False
    return suffix is None or qname.endswith(suffix)


__all__ = [
    "DecisionStatus",
    "Finding",
    "LocateStage",
    "MapStage",
    "PipelineRunResult",
    "PipelineSpec",
    "ProjectStage",
    "SemanticDecision",
    "SemanticFilterStage",
    "StructuralCandidate",
    "run_pipeline",
]
