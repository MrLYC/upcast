"""Astroid-powered pattern matching utilities."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

import astroid
from astroid import nodes

from upcast.common.ast_utils import get_qualified_name
from upcast.common.inference import infer_type

_CAPTURE_PATTERN = re.compile(r"^\$([A-Z][A-Z0-9_]*)$")
_ALLOWED_RULE_KEYS = {"captures", "self", "has", "not"}
_ALLOWED_PREDICATE_KEYS = {"builtin_type", "inferable", "qname"}


@dataclass
class MatchResult:
    """Structured result for a successful astroid match."""

    node: nodes.NodeNG
    captures: dict[str, nodes.NodeNG] = field(default_factory=dict)

    @property
    def matched_node(self) -> nodes.NodeNG:
        return self.node


def match(node: nodes.NodeNG, pattern: str, rule: dict[str, Any] | None = None) -> MatchResult | None:
    """Match a single astroid node against a minimal ast-grep-like pattern."""
    capture_name = _parse_capture_pattern(pattern)

    captures = {capture_name: node}
    if not _matches_rule(node=node, captures=captures, rule=rule):
        return None

    return MatchResult(node=node, captures=captures)


def find_matches(root: nodes.NodeNG, pattern: str, rule: dict[str, Any] | None = None) -> list[MatchResult]:
    """Find all matches beneath ``root`` in stable traversal order."""
    results: list[MatchResult] = []
    seen: set[int] = set()

    for candidate in _walk_nodes(root):
        result = match(candidate, pattern, rule=rule)
        if result is None:
            continue

        node_id = id(result.node)
        if node_id in seen:
            continue

        seen.add(node_id)
        results.append(result)

    return results


def _parse_capture_pattern(pattern: str) -> str:
    stripped = pattern.strip()
    matched = _CAPTURE_PATTERN.fullmatch(stripped)
    if matched is None:
        msg = f"Unsupported pattern shape: {pattern!r}. v1 is capture-only and currently supports only '$NAME'."
        raise ValueError(msg)
    return matched.group(1)


def _walk_nodes(root: nodes.NodeNG):
    yield root
    for child in root.get_children():
        yield from _walk_nodes(child)


def _matches_rule(*, node: nodes.NodeNG, captures: dict[str, nodes.NodeNG], rule: dict[str, Any] | None) -> bool:
    if not rule:
        return True

    if not isinstance(rule, dict):
        return False

    unknown_rule_keys = set(rule) - _ALLOWED_RULE_KEYS
    if unknown_rule_keys:
        unknown_keys = ", ".join(sorted(unknown_rule_keys))
        raise ValueError(f"Unknown rule key(s): {unknown_keys}")

    capture_rules = rule.get("captures")
    if isinstance(capture_rules, dict):
        for capture_name, capture_rule in capture_rules.items():
            capture_node = captures.get(capture_name)
            if capture_node is None:
                return False
            if not _matches_predicates(capture_node, capture_rule):
                return False

    self_rule = rule.get("self")
    if self_rule is not None and not _matches_predicates(node, self_rule):
        return False

    has_rule = rule.get("has")
    if has_rule is not None and not _matches_has(node, has_rule):
        return False

    not_rule = rule.get("not")
    return not (not_rule is not None and _matches_rule(node=node, captures=captures, rule=not_rule))


def _matches_predicates(node: nodes.NodeNG, predicates: Any) -> bool:
    if not isinstance(predicates, dict):
        return False

    unknown_predicate_keys = set(predicates) - _ALLOWED_PREDICATE_KEYS
    if unknown_predicate_keys:
        unknown_keys = ", ".join(sorted(unknown_predicate_keys))
        raise ValueError(f"Unknown predicate key(s): {unknown_keys}")

    builtin_type = predicates.get("builtin_type")
    if builtin_type is not None:
        inferred_type, _ = infer_type(node)
        if inferred_type != builtin_type:
            return False

    inferable = predicates.get("inferable")
    if inferable is not None:
        if not isinstance(inferable, bool):
            raise ValueError("'inferable' predicate must be a boolean")
        if _is_inferable(node) is not inferable:
            return False

    qname = predicates.get("qname")
    return qname is None or _matches_qname(node, qname)


def _matches_has(node: nodes.NodeNG, has_rule: Any) -> bool:
    if not isinstance(has_rule, dict):
        return False

    pattern = has_rule.get("pattern")
    if not isinstance(pattern, str):
        return False

    nested_rule = has_rule.get("rule")
    for child in node.get_children():
        for descendant in _walk_nodes(child):
            if match(descendant, pattern, rule=nested_rule) is not None:
                return True

    return False


def _matches_qname(node: nodes.NodeNG, qname_rule: Any) -> bool:
    if isinstance(qname_rule, str):
        return any(_match_qname_value(qname, exact=qname_rule) for qname in _iter_qnames(node))

    if not isinstance(qname_rule, dict):
        return False

    exact = qname_rule.get("exact")
    prefix = qname_rule.get("prefix")
    suffix = qname_rule.get("suffix")

    if exact is None and prefix is None and suffix is None:
        return False

    return any(_match_qname_value(qname, exact=exact, prefix=prefix, suffix=suffix) for qname in _iter_qnames(node))


def _iter_qnames(node: nodes.NodeNG):
    seen: set[str] = set()

    direct_name, direct_success = get_qualified_name(node)
    if direct_success and direct_name not in seen:
        seen.add(direct_name)
        yield direct_name

    try:
        for inferred in node.infer():
            if inferred is astroid.Uninferable:
                continue
            if inferred.__class__.__name__ in {"Uninferable", "UninferableBase"}:
                continue

            inferred_name, inferred_success = get_qualified_name(inferred)
            if inferred_success and inferred_name not in seen:
                seen.add(inferred_name)
                yield inferred_name
    except (astroid.InferenceError, AttributeError, StopIteration):
        return


def _match_qname_value(
    qname: str,
    *,
    exact: str | None = None,
    prefix: str | None = None,
    suffix: str | None = None,
) -> bool:
    if exact is not None and qname != exact:
        return False
    if prefix is not None and not qname.startswith(prefix):
        return False
    return suffix is None or qname.endswith(suffix)


def _is_inferable(node: nodes.NodeNG) -> bool:
    try:
        for inferred in node.infer():
            if inferred is astroid.Uninferable:
                continue
            if inferred.__class__.__name__ in {"Uninferable", "UninferableBase"}:
                continue
            return True
    except (astroid.InferenceError, AttributeError, StopIteration):
        return False

    return False


__all__ = ["MatchResult", "find_matches", "match"]
