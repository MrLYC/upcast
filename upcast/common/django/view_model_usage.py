"""Static extraction of direct Django model-use evidence."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from astroid import nodes

from upcast.models.django_views import ModelUsage, ResolutionStatus, SourceEvidence

_ORM_OPERATIONS = {
    "aggregate": "read",
    "all": "read",
    "count": "read",
    "create": "write",
    "delete": "delete",
    "exists": "read",
    "filter": "read",
    "first": "read",
    "get": "read",
    "get_or_create": "read_write",
    "in_bulk": "read",
    "last": "read",
    "latest": "read",
    "update": "write",
    "update_or_create": "read_write",
    "values": "read",
    "values_list": "read",
}


@dataclass(frozen=True)
class ModelModule:
    """Parsed source context used to resolve local model and serializer names."""

    module: nodes.Module
    module_name: str
    file: str


def extract_class_model_usages(
    class_node: nodes.ClassDef,
    *,
    file: str,
    module_name: str,
    modules: Iterable[ModelModule],
) -> list[ModelUsage]:
    """Extract direct class declarations and direct ORM calls in class methods."""
    contexts = list(modules)
    context = _context_for_module(contexts, module_name, file, class_node.root())
    usages = _class_declaration_usages(class_node, file=file, context=context, contexts=contexts)
    for method in _direct_methods(class_node):
        usages.extend(_function_orm_usages(method, file=file, context=context))
    return _sorted_unique(usages)


def extract_function_model_usages(
    function_node: nodes.FunctionDef,
    *,
    file: str,
    module_name: str,
    modules: Iterable[ModelModule],
) -> list[ModelUsage]:
    """Extract direct ORM calls from one function or explicit ViewSet action."""
    contexts = list(modules)
    context = _context_for_module(contexts, module_name, file, function_node.root())
    return _sorted_unique(_function_orm_usages(function_node, file=file, context=context))


def _class_declaration_usages(
    class_node: nodes.ClassDef,
    *,
    file: str,
    context: ModelModule,
    contexts: list[ModelModule],
) -> list[ModelUsage]:
    usages: list[ModelUsage] = []
    for assignment in _direct_assignments(class_node):
        target_name = _assignment_target_name(assignment)
        if target_name == "queryset":
            usages.append(_queryset_usage(assignment.value, file=file, context=context))
        elif target_name == "model":
            usages.append(_model_declaration_usage(assignment.value, file=file, context=context))
        elif target_name == "serializer_class":
            usages.append(_serializer_usage(assignment.value, file=file, context=context, contexts=contexts))
    return usages


def _queryset_usage(value: nodes.NodeNG, *, file: str, context: ModelModule) -> ModelUsage:
    model_name, operation = _recognized_orm_reference(value, context)
    if model_name is not None:
        return _usage(file, value, "queryset", model_name, operation, ResolutionStatus.CONFIRMED)
    return _usage(file, value, "queryset", None, "unknown", ResolutionStatus.UNKNOWN)


def _model_declaration_usage(value: nodes.NodeNG, *, file: str, context: ModelModule) -> ModelUsage:
    model_name = _resolve_expression_name(value, context)
    status = ResolutionStatus.CONFIRMED if model_name else ResolutionStatus.UNKNOWN
    return _usage(file, value, "model", model_name, "unknown", status)


def _serializer_usage(
    value: nodes.NodeNG,
    *,
    file: str,
    context: ModelModule,
    contexts: list[ModelModule],
) -> ModelUsage:
    serializer_name = _resolve_expression_name(value, context)
    serializer = _class_definition(serializer_name, contexts)
    if serializer is None:
        return _usage(file, value, "serializer", None, "unknown", ResolutionStatus.UNKNOWN)

    serializer_node, serializer_context = serializer
    model_assignment = _serializer_meta_model_assignment(serializer_node)
    if model_assignment is None:
        return _usage(file, value, "serializer", None, "unknown", ResolutionStatus.UNKNOWN)

    model_name = _resolve_expression_name(model_assignment.value, serializer_context)
    status = ResolutionStatus.CONFIRMED if model_name else ResolutionStatus.UNKNOWN
    return _usage(file, model_assignment.value, "serializer", model_name, "unknown", status)


def _function_orm_usages(
    function_node: nodes.FunctionDef,
    *,
    file: str,
    context: ModelModule,
) -> list[ModelUsage]:
    usages: list[ModelUsage] = []
    for call_node in function_node.nodes_of_class(nodes.Call):
        if not _belongs_to_scope(call_node, function_node) or _is_nested_call(call_node, function_node):
            continue
        usage = _orm_call_usage(call_node, file=file, context=context)
        if usage is not None:
            usages.append(usage)
    return usages


def _orm_call_usage(call_node: nodes.Call, *, file: str, context: ModelModule) -> ModelUsage | None:
    if not isinstance(call_node.func, nodes.Attribute):
        return None
    root, manager_kind = _manager_root(call_node.func.expr)
    if root is None or manager_kind is None:
        return None

    operation = _ORM_OPERATIONS.get(call_node.func.attrname)
    model_name = _resolve_expression_name(root, context)
    if manager_kind == "objects" and operation is not None and model_name is not None:
        return _usage(file, call_node, "orm_call", model_name, operation, ResolutionStatus.CONFIRMED)
    if manager_kind == "objects":
        return _usage(file, call_node, "orm_call", None, "unknown", ResolutionStatus.UNKNOWN)
    manager_name = _manager_attribute_name(call_node.func.expr)
    if manager_kind == "custom" and model_name is not None and _looks_like_manager_name(manager_name):
        return _usage(file, call_node, "orm_call", None, "unknown", ResolutionStatus.UNKNOWN)
    return None


def _recognized_orm_reference(value: nodes.NodeNG, context: ModelModule) -> tuple[str | None, str]:
    if not isinstance(value, nodes.Call) or not isinstance(value.func, nodes.Attribute):
        return None, "unknown"
    root, manager_kind = _manager_root(value.func.expr)
    operation = _ORM_OPERATIONS.get(value.func.attrname)
    if root is None or manager_kind != "objects" or operation is None:
        return None, "unknown"
    return _resolve_expression_name(root, context), operation


def _manager_root(node: nodes.NodeNG) -> tuple[nodes.NodeNG | None, str | None]:
    if isinstance(node, nodes.Attribute):
        if node.attrname == "objects":
            return node.expr, "objects"
        root, manager_kind = _manager_root(node.expr)
        if root is not None and manager_kind is None:
            return root, "custom"
        return root, manager_kind
    if isinstance(node, nodes.Call) and isinstance(node.func, nodes.Attribute):
        return _manager_root(node.func.expr)
    if isinstance(node, nodes.Name):
        return node, None
    return None, None


def _manager_attribute_name(node: nodes.NodeNG) -> str | None:
    if isinstance(node, nodes.Attribute):
        return node.attrname
    if isinstance(node, nodes.Call) and isinstance(node.func, nodes.Attribute):
        return _manager_attribute_name(node.func.expr)
    return None


def _looks_like_manager_name(name: str | None) -> bool:
    return bool(name and (name.endswith("manager") or name.endswith("objects")))


def _serializer_meta_model_assignment(serializer_node: nodes.ClassDef) -> nodes.Assign | None:
    for node in serializer_node.body:
        if not isinstance(node, nodes.ClassDef) or node.name != "Meta":
            continue
        for assignment in _direct_assignments(node):
            if _assignment_target_name(assignment) == "model":
                return assignment
    return None


def _class_definition(
    qualified_name: str | None,
    contexts: list[ModelModule],
) -> tuple[nodes.ClassDef, ModelModule] | None:
    if qualified_name is None:
        return None
    for context in contexts:
        prefix = f"{context.module_name}."
        if not qualified_name.startswith(prefix):
            continue
        class_name = qualified_name.removeprefix(prefix)
        definition = context.module.locals.get(class_name, [])
        if definition and isinstance(definition[0], nodes.ClassDef):
            return definition[0], context
    return None


def _context_for_module(
    contexts: list[ModelModule],
    module_name: str,
    file: str,
    module: nodes.Module,
) -> ModelModule:
    for context in contexts:
        if context.module_name == module_name:
            return context
    return ModelModule(module=module, module_name=module_name, file=file)


def _resolve_expression_name(node: nodes.NodeNG, context: ModelModule) -> str | None:
    bindings = _collect_import_bindings(context.module, context.module_name)
    if isinstance(node, nodes.Name):
        return bindings.get(node.name) or _local_symbol_name(node.name, context)
    if isinstance(node, nodes.Attribute):
        parent_name = _resolve_expression_name(node.expr, context)
        return f"{parent_name}.{node.attrname}" if parent_name else None
    return None


def _local_symbol_name(name: str, context: ModelModule) -> str | None:
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


def _direct_assignments(class_node: nodes.ClassDef) -> list[nodes.Assign]:
    return [node for node in class_node.body if isinstance(node, nodes.Assign)]


def _direct_methods(class_node: nodes.ClassDef) -> list[nodes.FunctionDef]:
    return [node for node in class_node.body if isinstance(node, nodes.FunctionDef)]


def _assignment_target_name(assignment: nodes.Assign) -> str | None:
    for target in assignment.targets:
        if isinstance(target, nodes.AssignName):
            return target.name
    return None


def _belongs_to_scope(node: nodes.NodeNG, scope: nodes.FunctionDef) -> bool:
    current = node.parent
    while current is not None:
        if isinstance(current, (nodes.FunctionDef, nodes.Lambda, nodes.ClassDef)):
            return current is scope
        current = current.parent
    return False


def _is_nested_call(call_node: nodes.Call, scope: nodes.FunctionDef) -> bool:
    current = call_node.parent
    while current is not None and current is not scope:
        if isinstance(current, nodes.Call):
            return True
        current = current.parent
    return False


def _usage(
    file: str,
    node: nodes.NodeNG,
    role: str,
    model: str | None,
    operation: str,
    status: ResolutionStatus,
) -> ModelUsage:
    return ModelUsage(
        model=model,
        role=role,
        operation=operation,
        evidence=SourceEvidence(
            file=file,
            line=getattr(node, "lineno", 1),
            column=getattr(node, "col_offset", None),
            expression=node.as_string(),
            kind=role,
            status=status,
            qualified_name=model,
        ),
    )


def _sorted_unique(usages: list[ModelUsage]) -> list[ModelUsage]:
    unique: dict[tuple[object, ...], ModelUsage] = {}
    for usage in usages:
        key = (
            usage.evidence.file,
            usage.evidence.line,
            usage.evidence.expression,
            usage.role,
            usage.model,
            usage.operation,
        )
        unique[key] = usage
    return sorted(
        unique.values(),
        key=lambda usage: (usage.evidence.file, usage.evidence.line, usage.role, usage.model or "", usage.operation),
    )
