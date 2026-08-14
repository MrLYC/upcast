"""Static DRF defaults and one-hop permission-definition resolution."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import astroid
from astroid import nodes

from upcast.models.django_views import (
    PermissionDefinition,
    PermissionExpression,
    ResolutionStatus,
    SecurityControl,
    SourceEvidence,
    ViewSecurity,
)


@dataclass(frozen=True)
class PermissionModule:
    """Parsed source context available for static permission resolution."""

    module: nodes.Module
    module_name: str
    file: str


def extract_drf_defaults(modules: Iterable[PermissionModule]) -> ViewSecurity:
    """Extract statically declared REST_FRAMEWORK authentication and permissions."""
    defaults = ViewSecurity()
    for context in modules:
        for assignment in _module_assignments(context.module):
            if _assignment_target_name(assignment) != "REST_FRAMEWORK":
                continue
            _add_rest_framework_defaults(defaults, assignment.value, context)
    return defaults


def apply_drf_defaults(security: ViewSecurity, defaults: ViewSecurity) -> ViewSecurity:
    """Apply DRF defaults only where a nearer source declaration is absent."""
    return ViewSecurity(
        authentication=_merge_default_control(security.authentication, defaults.authentication),
        authorization=_merge_default_control(security.authorization, defaults.authorization),
        csrf=security.csrf.model_copy(deep=True),
        raw_signals=list(security.raw_signals),
    )


def resolve_permission_definitions(
    security: ViewSecurity,
    modules: Iterable[PermissionModule],
) -> ViewSecurity:
    """Add expression trees and direct custom-permission definitions to security.

    This intentionally follows only the referenced permission definition.  It
    records check-method source without interpreting arbitrary calls in those
    methods.
    """
    contexts = list(modules)
    contexts_by_file = {context.file: context for context in contexts}
    definitions = _definition_index(contexts)
    resolved = security.model_copy(deep=True)
    authorization = resolved.authorization

    expressions: list[PermissionExpression] = []
    permission_definitions: list[PermissionDefinition] = []
    seen_definitions: set[str] = set()
    for declaration in authorization.effective_evidence:
        context = contexts_by_file.get(declaration.file)
        expression = _parse_permission_expression(declaration, context)
        expressions.append(expression)
        for qualified_name in _leaf_permission_names(expression):
            if qualified_name in seen_definitions:
                continue
            definition = definitions.get(qualified_name)
            if definition is None:
                continue
            permission_definitions.append(_permission_definition(qualified_name, definition))
            seen_definitions.add(qualified_name)

    authorization.permission_expressions = expressions
    authorization.permission_definitions = permission_definitions
    return resolved


def _add_rest_framework_defaults(
    defaults: ViewSecurity,
    value: nodes.NodeNG,
    context: PermissionModule,
) -> None:
    if not isinstance(value, nodes.Dict):
        return
    for key, item in value.items:
        if not (isinstance(key, nodes.Const) and isinstance(key.value, str)):
            continue
        if key.value == "DEFAULT_AUTHENTICATION_CLASSES":
            _add_default_values(defaults.authentication, item, context, "drf_default_authentication_classes")
        elif key.value == "DEFAULT_PERMISSION_CLASSES":
            _add_default_values(defaults.authorization, item, context, "drf_default_permission_classes")


def _add_default_values(
    control: SecurityControl,
    value: nodes.NodeNG,
    context: PermissionModule,
    kind: str,
) -> None:
    for item in _collection_items(value):
        qualified_name = item.value if isinstance(item, nodes.Const) and isinstance(item.value, str) else None
        evidence = _evidence(
            context.file,
            item,
            kind,
            ResolutionStatus.CONFIRMED if qualified_name else ResolutionStatus.UNKNOWN,
            qualified_name,
        )
        control.state = "default"
        control.declarations.append(evidence)
        control.effective_evidence.append(evidence)


def _merge_default_control(local: SecurityControl, default: SecurityControl) -> SecurityControl:
    has_local_declaration = bool(local.declarations)
    return SecurityControl(
        state=local.state if has_local_declaration else default.state,
        declarations=[*default.declarations, *local.declarations],
        effective_evidence=(local.effective_evidence if has_local_declaration else default.effective_evidence),
        permission_expressions=list(local.permission_expressions),
        permission_definitions=list(local.permission_definitions),
    )


def _parse_permission_expression(
    declaration: SourceEvidence,
    context: PermissionModule | None,
) -> PermissionExpression:
    try:
        parsed = astroid.parse(declaration.expression)
        statement = parsed.body[0]
        expression_node = statement.value if isinstance(statement, nodes.Expr) else None
    except (astroid.AstroidError, IndexError, SyntaxError):
        expression_node = None

    if expression_node is None:
        return PermissionExpression(
            expression=declaration.expression,
            status=ResolutionStatus.UNKNOWN,
            evidence=declaration,
        )
    return _permission_expression(expression_node, declaration, context)


def _permission_expression(
    node: nodes.NodeNG,
    source: SourceEvidence,
    context: PermissionModule | None,
) -> PermissionExpression:
    if isinstance(node, nodes.BinOp) and node.op in {"|", "&"}:
        children = [
            _permission_expression(node.left, source, context),
            _permission_expression(node.right, source, context),
        ]
        return PermissionExpression(
            expression=_expression(node),
            status=_combined_status(children),
            operator=node.op,
            children=children,
            evidence=_derived_evidence(source, node, "permission_expression", _combined_status(children)),
        )
    if isinstance(node, nodes.UnaryOp) and node.op == "~":
        child = _permission_expression(node.operand, source, context)
        return PermissionExpression(
            expression=_expression(node),
            status=child.status,
            operator=node.op,
            children=[child],
            evidence=_derived_evidence(source, node, "permission_expression", child.status),
        )

    qualified_name = _resolve_expression_name(node, context)
    status = ResolutionStatus.CONFIRMED if qualified_name else ResolutionStatus.UNKNOWN
    return PermissionExpression(
        expression=_expression(node),
        status=status,
        qualified_name=qualified_name,
        evidence=_derived_evidence(source, node, "permission_leaf", status, qualified_name),
    )


def _combined_status(expressions: list[PermissionExpression]) -> ResolutionStatus:
    statuses = {expression.status for expression in expressions}
    if statuses == {ResolutionStatus.CONFIRMED}:
        return ResolutionStatus.CONFIRMED
    if ResolutionStatus.CONFIRMED in statuses:
        return ResolutionStatus.PARTIAL
    return ResolutionStatus.UNKNOWN


def _leaf_permission_names(expression: PermissionExpression) -> list[str]:
    if expression.qualified_name:
        return [expression.qualified_name]
    return [name for child in expression.children for name in _leaf_permission_names(child)]


def _definition_index(modules: Iterable[PermissionModule]) -> dict[str, tuple[nodes.ClassDef, PermissionModule]]:
    definitions: dict[str, tuple[nodes.ClassDef, PermissionModule]] = {}
    for context in modules:
        for class_node in context.module.nodes_of_class(nodes.ClassDef):
            if class_node.parent is context.module:
                definitions[f"{context.module_name}.{class_node.name}"] = (class_node, context)
    return definitions


def _permission_definition(
    qualified_name: str,
    definition: tuple[nodes.ClassDef, PermissionModule],
) -> PermissionDefinition:
    class_node, context = definition
    bases = [
        _evidence(
            context.file,
            base,
            "permission_base",
            _status_for_name(_resolve_expression_name(base, context)),
            _resolve_expression_name(base, context),
        )
        for base in class_node.bases
    ]
    check_methods = [
        _evidence(context.file, method, "permission_check_method", ResolutionStatus.CONFIRMED, None)
        for method in _direct_methods(class_node)
        if method.name in {"has_permission", "has_object_permission"}
    ]
    return PermissionDefinition(
        qualified_name=qualified_name,
        status=ResolutionStatus.CONFIRMED,
        definition=_evidence(
            context.file, class_node, "permission_definition", ResolutionStatus.CONFIRMED, qualified_name
        ),
        bases=bases,
        check_methods=check_methods,
        docstring=_docstring(class_node),
    )


def _resolve_expression_name(node: nodes.NodeNG, context: PermissionModule | None) -> str | None:
    if context is None:
        return None
    bindings = _collect_import_bindings(context.module, context.module_name)
    if isinstance(node, nodes.Name):
        return bindings.get(node.name) or _local_symbol_name(node.name, context)
    if isinstance(node, nodes.Attribute):
        parent_name = _resolve_expression_name(node.expr, context)
        return f"{parent_name}.{node.attrname}" if parent_name else None
    if isinstance(node, nodes.Const) and isinstance(node.value, str):
        return node.value
    return None


def _local_symbol_name(name: str, context: PermissionModule) -> str | None:
    return f"{context.module_name}.{name}" if name in context.module.locals else None


def _collect_import_bindings(module: nodes.Module, module_name: str) -> dict[str, str]:
    bindings: dict[str, str] = {}
    for import_from in module.nodes_of_class(nodes.ImportFrom):
        base_module = _resolve_import_from_module(import_from, module_name)
        if base_module is None:
            continue
        for imported_name, alias in import_from.names:
            if imported_name != "*":
                bindings[alias or imported_name] = f"{base_module}.{imported_name}"
    for import_node in module.nodes_of_class(nodes.Import):
        for imported_name, alias in import_node.names:
            bindings[alias or imported_name.split(".")[0]] = imported_name
    return bindings


def _resolve_import_from_module(import_from: nodes.ImportFrom, module_name: str) -> str | None:
    level = getattr(import_from, "level", 0) or 0
    parts = module_name.split(".")[:-1]
    parts = parts[: max(0, len(parts) - (level - 1))] if level else []
    if import_from.modname:
        parts.extend(import_from.modname.split("."))
    return ".".join(parts) or None


def _module_assignments(module: nodes.Module) -> list[nodes.Assign]:
    return [node for node in module.body if isinstance(node, nodes.Assign)]


def _direct_methods(class_node: nodes.ClassDef) -> list[nodes.FunctionDef]:
    return [node for node in class_node.body if isinstance(node, nodes.FunctionDef)]


def _assignment_target_name(assignment: nodes.Assign) -> str | None:
    for target in assignment.targets:
        if isinstance(target, nodes.AssignName):
            return target.name
    return None


def _collection_items(node: nodes.NodeNG) -> list[nodes.NodeNG]:
    if isinstance(node, (nodes.List, nodes.Tuple, nodes.Set)):
        return list(node.elts)
    return [node]


def _docstring(class_node: nodes.ClassDef) -> str | None:
    doc_node = getattr(class_node, "doc_node", None)
    return doc_node.value if isinstance(doc_node, nodes.Const) and isinstance(doc_node.value, str) else None


def _status_for_name(qualified_name: str | None) -> ResolutionStatus:
    return ResolutionStatus.CONFIRMED if qualified_name else ResolutionStatus.UNKNOWN


def _derived_evidence(
    source: SourceEvidence,
    node: nodes.NodeNG,
    kind: str,
    status: ResolutionStatus,
    qualified_name: str | None = None,
) -> SourceEvidence:
    return SourceEvidence(
        file=source.file,
        line=source.line,
        column=source.column,
        expression=_expression(node),
        kind=kind,
        status=status,
        qualified_name=qualified_name,
    )


def _evidence(
    file: str,
    node: nodes.NodeNG,
    kind: str,
    status: ResolutionStatus,
    qualified_name: str | None,
) -> SourceEvidence:
    return SourceEvidence(
        file=file,
        line=getattr(node, "lineno", 1),
        column=getattr(node, "col_offset", None),
        expression=_expression(node),
        kind=kind,
        status=status,
        qualified_name=qualified_name,
    )


def _expression(node: nodes.NodeNG) -> str:
    return node.as_string().strip()
