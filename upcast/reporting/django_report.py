"""Merge Django URL/view scan output and verify it against source code."""

from __future__ import annotations

import ast
import csv
import json
from pathlib import Path
from typing import Any

import yaml


def build_django_report(
    root: Path,
    urls_yaml: Path,
    views_yaml: Path,
    csv_path: Path,
    verification_path: Path,
) -> dict[str, int]:
    """Build a combined CSV and a source-verification YAML report.

    URL rows are retained even when a view cannot be statically linked.  View
    rows that have no linked URL are emitted separately, so neither scanner's
    inventory is silently discarded.  Linking uses exact module/name evidence
    or the exact source location recorded by the scanners; it never guesses
    from a view name alone.
    """
    root = root.resolve()
    urls = _load_yaml(urls_yaml)
    views = _load_yaml(views_yaml)
    view_records = [view for module_views in views.get("results", {}).values() for view in module_views or []]
    view_index = _build_view_index(view_records)
    route_index, module_line_index = _build_route_indexes(view_records)
    source_cache: dict[Path, tuple[ast.AST | None, str | None]] = {}

    rows: list[dict[str, str]] = []
    mismatches: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    referenced_views: set[tuple[str, str]] = set()

    for url_module, url_item in (urls.get("results", {}) or {}).items():
        for pattern in (url_item or {}).get("urlpatterns", []) or []:
            pattern = dict(pattern or {})
            matched_view, match_status = _match_view(
                pattern,
                url_module,
                view_index,
                route_index,
                module_line_index,
            )
            if matched_view is not None:
                referenced_views.add(_view_identity(matched_view))

            url_status, url_reason = _verify_url_pattern(root, pattern, source_cache)
            view_status, view_reason = ("", "")
            if matched_view is not None:
                view_status, view_reason = _verify_view(root, matched_view, source_cache)
            elif pattern.get("view_name"):
                view_status, view_reason = "unresolved", "No exact view module/name or source-location match"

            row = _url_row(url_module, pattern, matched_view, match_status, url_status, url_reason, view_status, view_reason)
            rows.append(row)
            _record_problem(
                mismatches,
                unresolved,
                row,
                source_status=url_status,
                source_reason=url_reason,
                source_kind="url",
            )
            if matched_view is not None:
                _record_problem(
                    mismatches,
                    unresolved,
                    row,
                    source_status=view_status,
                    source_reason=view_reason,
                    source_kind="view",
                )
            elif pattern.get("view_name"):
                unresolved.append(
                    {
                        "record_type": "url",
                        "file": pattern.get("file"),
                        "line": pattern.get("line"),
                        "reason": "No exact view module/name or source-location match",
                    }
                )

    for view in view_records:
        view_key = _view_identity(view)
        if view_key in referenced_views:
            continue
        view_status, view_reason = _verify_view(root, view, source_cache)
        row = _view_only_row(view, view_status, view_reason)
        rows.append(row)
        _record_problem(
            mismatches,
            unresolved,
            row,
            source_status=view_status,
            source_reason=view_reason,
            source_kind="view",
        )

    fieldnames = _fieldnames()
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "url_records": sum(1 for row in rows if row["record_type"] == "url"),
        "view_only_records": sum(1 for row in rows if row["record_type"] == "view"),
        "rows": len(rows),
        "mismatches": len(mismatches),
        "unresolved": len(unresolved),
    }
    verification_path.parent.mkdir(parents=True, exist_ok=True)
    verification_path.write_text(
        yaml.safe_dump(
            {"summary": summary, "mismatches": mismatches, "unresolved": unresolved},
            allow_unicode=True,
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return summary


def _load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(value, dict):
        raise TypeError(f"Expected mapping in YAML file: {path}")
    return value


def _build_view_index(views: list[dict[str, Any]]) -> dict[tuple[str, str], list[dict[str, Any]]]:
    index: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for view in views:
        module = view.get("module")
        name = view.get("name")
        if not module or not name:
            continue
        for alias in _module_aliases(module):
            index.setdefault((alias, name), []).append(view)
    return index


def _build_route_indexes(
    views: list[dict[str, Any]],
) -> tuple[dict[tuple[str | None, int | None], list[dict[str, Any]]], dict[tuple[str | None, int | None], list[dict[str, Any]]]]:
    by_location: dict[tuple[str | None, int | None], list[dict[str, Any]]] = {}
    by_module_line: dict[tuple[str | None, int | None], list[dict[str, Any]]] = {}
    for view in views:
        for link in view.get("route_linkage", []) or []:
            file_key = (link.get("file"), link.get("line"))
            by_location.setdefault(file_key, []).append(view)
            module_key = (link.get("url_module"), link.get("line"))
            by_module_line.setdefault(module_key, []).append(view)
    return by_location, by_module_line


def _match_view(
    pattern: dict[str, Any],
    url_module: str,
    view_index: dict[tuple[str, str], list[dict[str, Any]]],
    route_index: dict[tuple[str | None, int | None], list[dict[str, Any]]],
    module_line_index: dict[tuple[str | None, int | None], list[dict[str, Any]]],
) -> tuple[dict[str, Any] | None, str]:
    name = pattern.get("view_name")
    module = pattern.get("view_module")
    if name and module:
        exact: list[dict[str, Any]] = []
        for alias in _module_aliases(module):
            exact.extend(view_index.get((alias, name), []))
        exact = _unique_views(exact)
        if len(exact) == 1:
            return exact[0], "matched_exact"

    by_location = _unique_views(route_index.get((pattern.get("file"), pattern.get("line")), []))
    if len(by_location) == 1:
        return by_location[0], "matched_source_location"

    by_module_line = _unique_views(module_line_index.get((url_module, pattern.get("line")), []))
    if len(by_module_line) == 1:
        return by_module_line[0], "matched_url_module_location"

    return None, "unresolved" if name else "not_a_view_route"


def _url_row(
    url_module: str,
    pattern: dict[str, Any],
    view: dict[str, Any] | None,
    match_status: str,
    url_status: str,
    url_reason: str,
    view_status: str,
    view_reason: str,
) -> dict[str, str]:
    row = _empty_row()
    row.update(
        {
            "record_type": "url",
            "url_module": url_module,
            "url_type": _text(pattern.get("type")),
            "pattern": _text(pattern.get("pattern")),
            "full_path": _text(pattern.get("full_path")),
            "url_name": _text(pattern.get("name")),
            "include_module": _text(pattern.get("include_module")),
            "namespace": _text(pattern.get("namespace")),
            "router_type": _text(pattern.get("router_type")),
            "basename": _text(pattern.get("basename")),
            "url_view_module": _text(pattern.get("view_module")),
            "url_view_name": _text(pattern.get("view_name")),
            "source_file": _text(pattern.get("file")),
            "source_line": _text(pattern.get("line")),
            "view_match_status": match_status,
            "url_source_status": url_status,
            "url_source_reason": url_reason,
            "view_source_status": view_status,
            "view_source_reason": view_reason,
            "verification_status": _overall_status(url_status, view_status, bool(pattern.get("view_name"))),
        }
    )
    if view is not None:
        row.update(_view_fields(view))
    return row


def _view_only_row(view: dict[str, Any], status: str, reason: str) -> dict[str, str]:
    row = _empty_row()
    row.update(_view_fields(view))
    row.update(
        {
            "record_type": "view",
            "view_match_status": "unreferenced",
            "source_file": _text(view.get("file")),
            "source_line": _text(view.get("line")),
            "view_source_status": status,
            "view_source_reason": reason,
            "verification_status": status,
        }
    )
    return row


def _view_fields(view: dict[str, Any]) -> dict[str, str]:
    return {
        "view_module": _text(view.get("module")),
        "view_name": _text(view.get("name")),
        "view_qualname": _text(view.get("qualname")),
        "view_kind": _text(view.get("kind")),
        "view_status": _text(view.get("status")),
        "view_identified_by": _json_text(view.get("identified_by", [])),
        "view_bases": _json_text(view.get("bases", [])),
        "view_decorators": _json_text(view.get("decorators", [])),
        "http_methods": _json_text(view.get("http_methods", [])),
        "permission_classes": _json_text(view.get("permission_classes", [])),
        "authentication_classes": _json_text(view.get("authentication_classes", [])),
        "login_exempt": _text(view.get("login_exempt")),
        "csrf_exempt": _text(view.get("csrf_exempt")),
        "model_references": _json_text(view.get("model_references", [])),
        "serializer_class": _text(view.get("serializer_class")),
        "action_count": _text(len(view.get("actions", []) or [])),
    }


def _verify_url_pattern(  # noqa: C901
    root: Path,
    pattern: dict[str, Any],
    source_cache: dict[Path, tuple[ast.AST | None, str | None]],
) -> tuple[str, str]:
    source_path = _source_path(root, pattern.get("file"))
    if source_path is None or not source_path.exists():
        return "missing_source", "URL source file does not exist"
    tree, error = _get_tree(source_path, source_cache)
    if tree is None:
        return "parse_error", error or "Could not parse URL source"
    line = pattern.get("line")
    if pattern.get("type") == "dynamic":
        return "verified", "Dynamic urlpatterns assignment is present in parsed source"
    if not isinstance(line, int):
        return "unresolved", "URL record has no source line"

    call = _find_route_call(tree, line, pattern.get("type"), pattern.get("pattern"))
    if call is None:
        return "mismatch", f"No {pattern.get('type')} call found at source line {line}"
    reasons: list[str] = []
    if pattern.get("type") != "router_registration" and pattern.get("pattern") is not None:
        source_pattern = _literal_string(call.args[0]) if call.args else None
        if source_pattern != pattern.get("pattern"):
            return "mismatch", f"Reported pattern {pattern.get('pattern')!r} != source {source_pattern!r}"
        reasons.append("route literal matches")
    if pattern.get("type") == "include":
        include_call = next(
            (
                node
                for node in ast.walk(call)
                if isinstance(node, ast.Call) and _call_name(node.func) == "include"
            ),
            None,
        )
        if include_call is None:
            return "mismatch", "Reported include route has no include() call at source location"
        include_module = _include_module(include_call)
        if pattern.get("include_module") and include_module != pattern.get("include_module"):
            return "mismatch", f"Reported include {pattern.get('include_module')!r} != source {include_module!r}"
        reasons.append("include target matches")
    if pattern.get("type") == "router_registration":
        source_pattern = _literal_string(call.args[0]) if call.args else None
        reported_pattern = pattern.get("pattern")
        if reported_pattern not in {None, "", "<root>"}:
            normalized_reported = str(reported_pattern).strip("/")
            normalized_source = str(source_pattern or "").strip("/")
            if normalized_reported != normalized_source and not normalized_reported.endswith(
                f"/{normalized_source}"
            ):
                return "mismatch", f"Reported router pattern {reported_pattern!r} != source {source_pattern!r}"
        basename = _router_basename(call)
        if pattern.get("basename") and basename != pattern.get("basename"):
            return "mismatch", f"Reported basename {pattern.get('basename')!r} != source {basename!r}"
        router_name = call.func.value.id if isinstance(call.func, ast.Attribute) and isinstance(call.func.value, ast.Name) else None
        router_type = _router_type(tree, router_name) if router_name else None
        if pattern.get("router_type") and router_type != pattern.get("router_type"):
            return "mismatch", f"Reported router type {pattern.get('router_type')!r} != source {router_type!r}"
        reasons.append("router registration metadata matches")
    target = call.args[1] if len(call.args) > 1 else None
    if pattern.get("type") == "router_registration" and len(call.args) > 1:
        target = call.args[1]
    if pattern.get("view_name"):
        target_name = _target_name(target)
        if target_name != pattern.get("view_name"):
            return "mismatch", f"Reported view {pattern.get('view_name')!r} != source {target_name!r}"
        reasons.append("view reference matches")
    if pattern.get("type") == "router_registration":
        reasons.append("router.register call matches")
    return "verified", "; ".join(reasons) or "URL call matches source"


def _verify_view(  # noqa: C901
    root: Path,
    view: dict[str, Any],
    source_cache: dict[Path, tuple[ast.AST | None, str | None]],
) -> tuple[str, str]:
    source_path = _source_path(root, view.get("file"))
    if source_path is None or not source_path.exists():
        return "missing_source", "View source file does not exist"
    tree, error = _get_tree(source_path, source_cache)
    if tree is None:
        return "parse_error", error or "Could not parse view source"
    name = view.get("name")
    node, actual_kind = _find_view_node(tree, view)
    if node is None:
        return "mismatch", f"View {name!r} is not present in source"
    expected_kind = view.get("kind")
    if expected_kind and expected_kind != actual_kind:
        return "mismatch", f"Reported kind {expected_kind!r} != source {actual_kind!r}"
    reasons = ["view name, file, and kind match"]
    if isinstance(node, ast.ClassDef):
        actual_bases = {_ast_name(base) for base in node.bases}
        for base in view.get("bases", []) or []:
            if _last_name(base) not in {_last_name(value) for value in actual_bases}:
                return "mismatch", f"Reported base {base!r} is absent from source"
        try:
            _check_assignment(view, node, "permission_classes", reasons)
            _check_assignment(view, node, "authentication_classes", reasons)
            _check_assignment(view, node, "serializer_class", reasons)
        except _VerificationMismatch as exc:
            return "mismatch", str(exc)
        for action in view.get("actions", []) or []:
            method = next((child for child in node.body if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child.name == action.get("name")), None)
            if method is None:
                return "mismatch", f"Reported action {action.get('name')!r} is absent from source"
            if not any(_decorator_name(decorator) == "action" for decorator in method.decorator_list):
                return "mismatch", f"Reported action {action.get('name')!r} has no @action decorator in source"
    decorators = [_ast_expression(decorator) for decorator in getattr(node, "decorator_list", [])]
    decorator_names = {_decorator_name(decorator) for decorator in getattr(node, "decorator_list", [])}
    if view.get("login_exempt") is True and not any("login_exempt" in value.lower() for value in decorators):
        return "mismatch", "Reported login_exempt evidence is absent from source"
    if view.get("csrf_exempt") is True and not any("csrf_exempt" in value.lower() for value in decorators):
        return "mismatch", "Reported csrf_exempt evidence is absent from source"
    if view.get("decorators"):
        reported_names = {_last_name(value) for value in view["decorators"]}
        if not reported_names.intersection({_last_name(value) for value in decorators} | decorator_names):
            return "mismatch", "Reported decorators are absent from source"
    reasons.append("decorator and security evidence matches")
    return "verified", "; ".join(reasons)


def _find_view_node(tree: ast.AST, view: dict[str, Any]) -> tuple[ast.AST | None, str]:
    name = view.get("name")
    line = view.get("line")
    if view.get("kind") == "method":
        qualname = str(view.get("qualname") or "")
        parts = qualname.split(".")
        class_name = parts[-2] if len(parts) >= 2 else None
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef) and node.name == class_name]
        candidates = [
            child
            for class_node in classes
            for child in class_node.body
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child.name == name
        ]
        node = next((candidate for candidate in candidates if _node_locations(candidate) & {line}), None)
        if node is None and line is None and len(candidates) == 1:
            node = candidates[0]
        return node, "method"

    candidates = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == name
    ]
    node = next((candidate for candidate in candidates if _node_locations(candidate) & {line}), None)
    if node is None and line is None and len(candidates) == 1:
        node = candidates[0]
    actual_kind = "class" if isinstance(node, ast.ClassDef) else "function"
    return node, actual_kind


def _node_locations(node: ast.AST) -> set[int | None]:
    locations = {getattr(node, "lineno", None)}
    locations.update(getattr(decorator, "lineno", None) for decorator in getattr(node, "decorator_list", []))
    return locations


def _check_assignment(view: dict[str, Any], node: ast.ClassDef, field: str, reasons: list[str]) -> None:
    reported = view.get(field, [])
    if field == "serializer_class":
        if reported is None:
            return
        reported_text = _last_name(str(reported))
        source = _assignment_expression(node, field)
        if source is not None and _last_name(source) != reported_text:
            raise _VerificationMismatch(f"Reported {field} {reported!r} != source {source!r}")
        return
    if not reported:
        return
    source_values = _assignment_values(node, field)
    if source_values is None:
        raise _VerificationMismatch(f"Reported {field} is absent from source")
    if [_last_name(value) for value in source_values] != [_last_name(str(value)) for value in reported]:
        raise _VerificationMismatch(f"Reported {field} != source assignment")
    reasons.append(f"{field} matches")


class _VerificationMismatch(Exception):
    """Internal exception used to keep assignment checks concise."""


def _get_tree(path: Path, cache: dict[Path, tuple[ast.AST | None, str | None]]) -> tuple[ast.AST | None, str | None]:
    if path in cache:
        return cache[path]
    try:
        source = path.read_text(encoding="utf-8-sig")
        value: tuple[ast.AST | None, str | None] = (ast.parse(source, filename=str(path)), None)
    except (OSError, SyntaxError, UnicodeDecodeError) as exc:
        value = (None, str(exc))
    cache[path] = value
    return value


def _find_route_call(
    tree: ast.AST,
    line: int,
    pattern_type: str | None,
    reported_pattern: str | None = None,
) -> ast.Call | None:
    expected = {"path", "re_path", "url", "include"} if pattern_type == "include" else {pattern_type or ""}
    if pattern_type == "re_path":
        expected.add("url")
    if pattern_type == "router_registration":
        candidates = [node for node in ast.walk(tree) if isinstance(node, ast.Call) and _call_name(node.func) == "register"]
    else:
        candidates = [node for node in ast.walk(tree) if isinstance(node, ast.Call) and _call_name(node.func) in expected]
    candidates.sort(key=lambda node: (0 if node.lineno == line else 1, abs(node.lineno - line)))
    if reported_pattern is not None and pattern_type != "router_registration":
        matching = [
            node
            for node in candidates
            if node.args and _literal_string(node.args[0]) == reported_pattern
        ]
        if matching:
            candidates = matching
    return next((node for node in candidates if node.lineno <= line <= getattr(node, "end_lineno", node.lineno)), None)


def _include_module(call: ast.Call) -> str | None:
    if not call.args:
        return None
    value = call.args[0]
    if isinstance(value, ast.Constant) and isinstance(value.value, str):
        return value.value
    if isinstance(value, (ast.Tuple, ast.List)) and value.elts:
        return _literal_string(value.elts[0])
    if isinstance(value, ast.Attribute) and value.attr == "urls" and isinstance(value.value, ast.Name):
        return f"{value.value.id}.urls"
    return None


def _target_name(node: ast.AST | None) -> str | None:
    if isinstance(node, ast.Call):
        node = node.func.value if isinstance(node.func, ast.Attribute) and node.func.attr == "as_view" else node.func
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Name):
        return node.id
    return None


def _router_basename(call: ast.Call) -> str | None:
    if len(call.args) >= 3:
        value = _literal_string(call.args[2])
        if value is not None:
            return value
    for keyword in call.keywords:
        if keyword.arg == "basename":
            return _literal_string(keyword.value)
    return None


def _router_type(tree: ast.AST, router_name: str | None) -> str | None:
    if not router_name:
        return None
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Call):
            continue
        if not any(isinstance(target, ast.Name) and target.id == router_name for target in node.targets):
            continue
        name = _call_name(node.value.func)
        if name and "Router" in name:
            return name
    return None


def _assignment_expression(node: ast.ClassDef, name: str) -> str | None:
    for child in node.body:
        target, value = _assignment_parts(child)
        if target == name:
            return _ast_expression(value)
    return None


def _assignment_values(node: ast.ClassDef, name: str) -> list[str] | None:
    for child in node.body:
        target, value = _assignment_parts(child)
        if target != name or value is None:
            continue
        if isinstance(value, (ast.List, ast.Tuple, ast.Set)):
            return [_ast_expression(element) for element in value.elts]
        return [_ast_expression(value)]
    return None


def _assignment_parts(node: ast.AST) -> tuple[str | None, ast.AST | None]:
    if isinstance(node, ast.Assign) and node.targets and isinstance(node.targets[0], ast.Name):
        return node.targets[0].id, node.value
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        return node.target.id, node.value
    return None, None


def _source_path(root: Path, value: Any) -> Path | None:
    if not value:
        return None
    path = Path(str(value))
    return path if path.is_absolute() else root / path


def _module_aliases(module: str) -> set[str]:
    parts = module.split(".")
    aliases = {module}
    for index in range(1, len(parts)):
        suffix = parts[index:]
        if all(part.isidentifier() for part in suffix):
            aliases.add(".".join(suffix))
    return aliases


def _module_line_key(module: str | None, line: Any) -> tuple[str | None, int | None]:
    return module, line if isinstance(line, int) else None


def _unique_views(views: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unique: dict[tuple[str, str], dict[str, Any]] = {}
    for view in views:
        unique[_view_identity(view)] = view
    return list(unique.values())


def _view_identity(view: dict[str, Any]) -> tuple[str, str]:
    return view.get("module", ""), view.get("qualname") or view.get("name", "")


def _record_problem(
    mismatches: list[dict[str, Any]],
    unresolved: list[dict[str, Any]],
    row: dict[str, str],
    *,
    source_status: str,
    source_reason: str,
    source_kind: str,
) -> None:
    if source_status == "mismatch":
        mismatches.append(
            {
                "record_type": row["record_type"],
                "source_kind": source_kind,
                "file": row.get("source_file"),
                "line": row.get("source_line"),
                "reason": source_reason,
            }
        )
    elif source_status not in {"", "verified"}:
        unresolved.append(
            {
                "record_type": row["record_type"],
                "source_kind": source_kind,
                "file": row.get("source_file"),
                "line": row.get("source_line"),
                "reason": source_reason,
            }
        )


def _overall_status(url_status: str, view_status: str, has_view_name: bool) -> str:
    if "mismatch" in {url_status, view_status}:
        return "mismatch"
    if url_status not in {"verified", ""} or (has_view_name and view_status not in {"verified", ""}):
        return "unresolved"
    return "verified"


def _empty_row() -> dict[str, str]:
    return dict.fromkeys(_fieldnames(), "")


def _fieldnames() -> list[str]:
    return [
        "record_type",
        "url_module",
        "url_type",
        "pattern",
        "full_path",
        "url_name",
        "include_module",
        "namespace",
        "router_type",
        "basename",
        "url_view_module",
        "url_view_name",
        "view_match_status",
        "view_module",
        "view_name",
        "view_qualname",
        "view_kind",
        "view_status",
        "view_identified_by",
        "view_bases",
        "view_decorators",
        "http_methods",
        "permission_classes",
        "authentication_classes",
        "login_exempt",
        "csrf_exempt",
        "model_references",
        "serializer_class",
        "action_count",
        "source_file",
        "source_line",
        "url_source_status",
        "url_source_reason",
        "view_source_status",
        "view_source_reason",
        "verification_status",
    ]


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _json_text(value: Any) -> str:
    return json.dumps(value if value is not None else [], ensure_ascii=False, sort_keys=True)


def _ast_expression(node: ast.AST | None) -> str:
    if node is None:
        return ""
    try:
        return ast.unparse(node)
    except Exception:
        return ""


def _ast_name(node: ast.AST) -> str:
    return _ast_expression(node)


def _last_name(value: str) -> str:
    return value.replace(" ", "").split(".")[-1].split("(")[0]


def _decorator_name(node: ast.AST) -> str:
    target = node.func if isinstance(node, ast.Call) else node
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        return target.attr
    return _ast_expression(target)


def _call_name(node: ast.AST | None) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return ""


def _literal_string(node: ast.AST | None) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None
