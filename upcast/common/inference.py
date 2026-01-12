"""Structured inference utilities for type and value inference."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Literal

import astroid
from astroid import nodes

Confidence = Literal["exact", "partial", "unknown"]


@dataclass
class InferenceResult:
    """Structured result for value inference.

    Attributes:
        value: The inferred value (None if unknown)
        confidence: "exact" (static), "partial" (has dynamic parts), or "unknown"
        is_static: Whether the value is completely static
        node: Original AST node for reference
    """

    value: Any
    confidence: Confidence
    is_static: bool
    node: nodes.NodeNG

    @property
    def is_dynamic(self) -> bool:
        return not self.is_static

    @property
    def is_exact(self) -> bool:
        return self.confidence == "exact"

    def get_exact(self, default: Any = None) -> Any:
        return self.value if self.confidence == "exact" else default

    def get_if_type(self, expected_type: type | tuple[type, ...], default: Any = None) -> Any:
        if self.confidence == "exact" and isinstance(self.value, expected_type):
            return self.value
        return default

    def __repr__(self) -> str:
        if self.confidence == "exact":
            return f"InferenceResult({self.value!r}, exact)"
        elif self.confidence == "partial":
            return f"InferenceResult({self.value!r}, partial)"
        else:
            return f"InferenceResult(<unknown>, node={_safe_as_string(self.node)!r})"


DYNAMIC = ...


@dataclass
class StringPattern:
    """Structured result for string pattern inference.

    Attributes:
        parts: List of static strings and Ellipsis markers for dynamic parts
        node: Original AST node for reference
    """

    parts: list[Any]
    node: nodes.NodeNG = field(repr=False)

    @property
    def is_static(self) -> bool:
        return ... not in self.parts

    @property
    def is_dynamic(self) -> bool:
        return not self.is_static

    def to_pattern(self) -> str:
        return "".join("..." if part is ... else str(part) for part in self.parts)

    def static_prefix(self) -> str:
        prefix_parts = []
        for part in self.parts:
            if part is ...:
                break
            prefix_parts.append(str(part))
        return "".join(prefix_parts)

    def static_suffix(self) -> str:
        suffix_parts = []
        for part in reversed(self.parts):
            if part is ...:
                break
            suffix_parts.insert(0, str(part))
        return "".join(suffix_parts)

    def static_parts(self) -> list[str]:
        return [str(p) for p in self.parts if p is not ...]

    def dynamic_count(self) -> int:
        return sum(1 for p in self.parts if p is ...)

    def to_inference_result(self) -> InferenceResult:
        if self.is_static:
            return InferenceResult(self.to_pattern(), "exact", True, self.node)
        return InferenceResult(self.to_pattern(), "partial", False, self.node)

    def __repr__(self) -> str:
        parts_repr = ["..." if p is ... else repr(p) for p in self.parts]
        return f"StringPattern([{', '.join(parts_repr)}])"


def _safe_as_string(node: Any) -> str:
    if isinstance(node, nodes.NodeNG):
        try:
            return node.as_string()
        except Exception:
            return ""
    return str(node)


def infer_value(node: nodes.NodeNG) -> InferenceResult:
    try:
        inferred_list = list(node.infer())

        if not inferred_list or len(inferred_list) != 1:
            return InferenceResult(None, "unknown", False, node)

        inferred = inferred_list[0]

        if inferred is astroid.Uninferable or inferred.__class__.__name__ in (
            "Uninferable",
            "UninferableBase",
        ):
            return InferenceResult(None, "unknown", False, node)

        if isinstance(inferred, nodes.Const):
            return InferenceResult(inferred.value, "exact", True, node)

        if isinstance(inferred, nodes.List):
            return _infer_list(inferred, node)

        if isinstance(inferred, nodes.Tuple):
            return _infer_tuple(inferred, node)

        if isinstance(inferred, nodes.Dict):
            return _infer_dict(inferred, node)

        return InferenceResult(None, "unknown", False, node)

    except (astroid.InferenceError, StopIteration, AttributeError):
        return InferenceResult(None, "unknown", False, node)


def _infer_list(list_node: nodes.List, original_node: nodes.NodeNG) -> InferenceResult:
    result = []
    all_static = True

    for elem in list_node.elts:
        if isinstance(elem, nodes.NodeNG):
            elem_result = infer_value(elem)
            result.append(elem_result.value)
            if not elem_result.is_static:
                all_static = False
        else:
            result.append(None)
            all_static = False

    confidence: Confidence = "exact" if all_static else "partial"
    return InferenceResult(result, confidence, all_static, original_node)


def _infer_tuple(tuple_node: nodes.Tuple, original_node: nodes.NodeNG) -> InferenceResult:
    result = []
    all_static = True

    for elem in tuple_node.elts:
        if isinstance(elem, nodes.NodeNG):
            elem_result = infer_value(elem)
            result.append(elem_result.value)
            if not elem_result.is_static:
                all_static = False
        else:
            result.append(None)
            all_static = False

    confidence: Confidence = "exact" if all_static else "partial"
    return InferenceResult(tuple(result), confidence, all_static, original_node)


def _infer_dict(dict_node: nodes.Dict, original_node: nodes.NodeNG) -> InferenceResult:
    result = {}
    all_static = True

    for key_node, value_node in dict_node.items:
        if isinstance(key_node, nodes.NodeNG) and isinstance(value_node, nodes.NodeNG):
            key_result = infer_value(key_node)
            val_result = infer_value(value_node)

            if isinstance(key_result.value, (str, int, float, bool, type(None))):
                result[key_result.value] = val_result.value
                if not key_result.is_static or not val_result.is_static:
                    all_static = False
            else:
                all_static = False
        else:
            all_static = False

    confidence: Confidence = "exact" if all_static else "partial"
    return InferenceResult(result, confidence, all_static, original_node)


def infer_string_pattern(node: nodes.NodeNG) -> StringPattern:
    parts = _extract_string_parts(node)
    return StringPattern(parts=parts, node=node)


def _extract_string_parts(node: nodes.NodeNG) -> list[Any]:
    if isinstance(node, nodes.JoinedStr):
        return _extract_fstring_parts(node)

    if isinstance(node, nodes.BinOp) and node.op == "+":
        return _extract_binop_parts(node)

    if isinstance(node, nodes.BinOp) and node.op == "%":
        return _extract_percent_format_parts(node)

    if _is_format_call(node):
        return _extract_format_call_parts(node)  # type: ignore[arg-type]

    result = infer_value(node)
    if result.confidence == "exact" and isinstance(result.value, str):
        return [result.value]

    if isinstance(node, nodes.Const) and isinstance(node.value, str):
        return [node.value]

    return [...]


def _extract_fstring_parts(node: nodes.JoinedStr) -> list[Any]:
    parts: list[Any] = []

    for value in node.values:
        if isinstance(value, nodes.Const):
            parts.append(str(value.value))
        elif isinstance(value, nodes.FormattedValue):
            inner_result = infer_value(value.value)
            if inner_result.confidence == "exact" and isinstance(inner_result.value, str):
                parts.append(inner_result.value)
            else:
                parts.append(...)
        else:
            parts.append(...)

    return _normalize_parts(parts)


def _extract_binop_parts(node: nodes.BinOp) -> list[Any]:
    parts: list[Any] = []
    _collect_binop_parts_recursive(node, parts)
    return _normalize_parts(parts)


def _collect_binop_parts_recursive(node: nodes.NodeNG, parts: list[Any]) -> None:
    if isinstance(node, nodes.BinOp) and node.op == "+":
        _collect_binop_parts_recursive(node.left, parts)
        _collect_binop_parts_recursive(node.right, parts)
    elif isinstance(node, nodes.Const) and isinstance(node.value, str):
        parts.append(node.value)
    elif isinstance(node, nodes.JoinedStr):
        parts.extend(_extract_fstring_parts(node))
    else:
        result = infer_value(node)
        if result.confidence == "exact" and isinstance(result.value, str):
            parts.append(result.value)
        else:
            parts.append(...)


def _extract_percent_format_parts(node: nodes.BinOp) -> list[Any]:
    if not isinstance(node.left, nodes.Const) or not isinstance(node.left.value, str):
        return [...]

    template = node.left.value
    # Regex: %s, %d, %r, %f, %(name)s, etc.
    pattern = re.compile(r"%(?:\([^)]+\))?[-+0 #]*\d*(?:\.\d+)?[sdrifoxXeEgGcba%]")

    parts: list[Any] = []
    last_end = 0

    for match in pattern.finditer(template):
        if match.start() > last_end:
            parts.append(template[last_end : match.start()])
        if match.group() != "%%":
            parts.append(...)
        else:
            parts.append("%")
        last_end = match.end()

    if last_end < len(template):
        parts.append(template[last_end:])

    return _normalize_parts(parts)


def _is_format_call(node: nodes.NodeNG) -> bool:
    return (
        isinstance(node, nodes.Call)
        and isinstance(node.func, nodes.Attribute)
        and node.func.attrname == "format"
        and isinstance(node.func.expr, nodes.Const)
        and isinstance(node.func.expr.value, str)
    )


def _extract_format_call_parts(node: nodes.Call) -> list[Any]:
    template = node.func.expr.value  # type: ignore[union-attr]
    # Regex: {}, {0}, {name}, {name:format}
    pattern = re.compile(r"\{[^}]*\}")

    parts: list[Any] = []
    last_end = 0

    for match in pattern.finditer(template):
        if match.start() > last_end:
            parts.append(template[last_end : match.start()])
        parts.append(...)
        last_end = match.end()

    if last_end < len(template):
        parts.append(template[last_end:])

    return _normalize_parts(parts)


def _normalize_parts(parts: list[Any]) -> list[Any]:
    if not parts:
        return []

    result: list[Any] = []
    current_str = ""

    for part in parts:
        if part is ...:
            if current_str:
                result.append(current_str)
                current_str = ""
            if not result or result[-1] is not ...:
                result.append(...)
        else:
            current_str += str(part)

    if current_str:
        result.append(current_str)

    return result


def infer_type(node: nodes.NodeNG) -> tuple[str, Confidence]:
    try:
        if isinstance(node, nodes.Const):
            return _get_const_type(node.value), "exact"

        inferred_list = list(node.infer())

        if inferred_list and len(inferred_list) == 1:
            inferred = inferred_list[0]

            if isinstance(inferred, nodes.Const):
                return _get_const_type(inferred.value), "exact"

            if isinstance(inferred, nodes.List):
                return "list", "exact"

            if isinstance(inferred, nodes.Dict):
                return "dict", "exact"

            if isinstance(inferred, nodes.Tuple):
                return "tuple", "exact"

        return "unknown", "unknown"

    except (astroid.InferenceError, StopIteration, AttributeError):
        return "unknown", "unknown"


def _get_const_type(value: Any) -> str:
    if isinstance(value, bool):
        return "bool"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, str):
        return "str"
    elif value is None:
        return "None"
    return "unknown"


__all__ = [
    "Confidence",
    "InferenceResult",
    "StringPattern",
    "DYNAMIC",
    "infer_value",
    "infer_string_pattern",
    "infer_type",
]
