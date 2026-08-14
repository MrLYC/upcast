"""Bounded extraction of Django and DRF security declarations."""

from __future__ import annotations

from astroid import nodes

from upcast.models.django_views import (
    DjangoViewAction,
    ResolutionStatus,
    SecurityControl,
    SourceEvidence,
    ViewSecurity,
)

_ACTION_DECORATOR = "rest_framework.decorators.action"
_API_VIEW_DECORATOR = "rest_framework.decorators.api_view"
_AUTHENTICATION_DECORATOR = "rest_framework.decorators.authentication_classes"
_PERMISSION_DECORATOR = "rest_framework.decorators.permission_classes"
_CSRF_EXEMPT_DECORATOR = "django.views.decorators.csrf.csrf_exempt"
_CSRF_PROTECT_DECORATOR = "django.views.decorators.csrf.csrf_protect"
_LOGIN_REQUIRED_DECORATOR = "django.contrib.auth.decorators.login_required"
_LOGIN_NOT_REQUIRED_DECORATOR = "django.contrib.auth.decorators.login_not_required"

_MODEL_VIEWSET_ACTIONS = [
    ("list", ["get"], False),
    ("retrieve", ["get"], True),
    ("create", ["post"], False),
    ("update", ["put"], True),
    ("partial_update", ["patch"], True),
    ("destroy", ["delete"], True),
]
_READ_ONLY_VIEWSET_ACTIONS = _MODEL_VIEWSET_ACTIONS[:2]


def analyze_view_security(
    class_node: nodes.ClassDef,
    *,
    file: str,
    module_name: str,
    view_id: str,
    kind: str,
    recognition_status: ResolutionStatus,
    inherited_security: ViewSecurity | None = None,
    inherited_actions: list[DjangoViewAction] | None = None,
) -> tuple[ViewSecurity, list[DjangoViewAction]]:
    """Return class-level security and bounded actions for a Django/DRF class.

    The helper only interprets a small set of framework declarations.  Every
    other decorator remains a raw signal rather than being treated as a login
    exemption, authentication bypass, or authorization rule.
    """
    bindings = _collect_import_bindings(class_node.root(), module_name)
    local_security = _local_security(class_node, file=file, bindings=bindings, scope="class")
    class_security = _merge_security(local_security, inherited_security) if inherited_security else local_security
    actions = _explicit_actions(
        class_node,
        file=file,
        bindings=bindings,
        view_id=view_id,
        inherited_security=class_security,
    )
    actions.extend(
        _framework_actions(
            class_node,
            file=file,
            bindings=bindings,
            view_id=view_id,
            kind=kind,
            recognition_status=recognition_status,
            security=class_security,
            inherited_actions=inherited_actions,
        )
    )
    return class_security, sorted(actions, key=lambda action: (action.line or 0, action.name, action.origin))


def analyze_function_security(
    function_node: nodes.FunctionDef,
    *,
    file: str,
    module_name: str,
) -> ViewSecurity:
    """Return local Django/DRF security declarations for one function view."""
    bindings = _collect_import_bindings(function_node.root(), module_name)
    return _local_security(function_node, file=file, bindings=bindings, scope="function")


def _explicit_actions(
    class_node: nodes.ClassDef,
    *,
    file: str,
    bindings: dict[str, str],
    view_id: str,
    inherited_security: ViewSecurity,
) -> list[DjangoViewAction]:
    actions: list[DjangoViewAction] = []
    for function_node in _direct_methods(class_node):
        decorator = _action_decorator(function_node, bindings)
        if decorator is None:
            continue
        action_status = _decorator_status(decorator, bindings, _ACTION_DECORATOR)
        local_security = _local_security(
            function_node,
            file=file,
            bindings=bindings,
            scope="action",
            ignored_decorators={id(decorator)},
        )
        _add_action_control_keywords(local_security, decorator, file=file, bindings=bindings)
        security = _merge_security(local_security, inherited_security)
        actions.append(
            DjangoViewAction(
                id=f"{view_id}#{function_node.name}",
                name=function_node.name,
                origin="decorator",
                methods=_action_methods(decorator),
                detail=_action_detail(decorator),
                url_path=_action_string_keyword(decorator, "url_path"),
                url_name=_action_string_keyword(decorator, "url_name"),
                line=function_node.lineno,
                security=security,
                evidence=[
                    _evidence(
                        file=file,
                        node=decorator,
                        kind="action_decorator",
                        status=action_status,
                        qualified_name=_resolve_decorator_name(decorator, bindings),
                    )
                ],
            )
        )
    return actions


def _framework_actions(
    class_node: nodes.ClassDef,
    *,
    file: str,
    bindings: dict[str, str],
    view_id: str,
    kind: str,
    recognition_status: ResolutionStatus,
    security: ViewSecurity,
    inherited_actions: list[DjangoViewAction] | None,
) -> list[DjangoViewAction]:
    if kind != "drf_viewset" or recognition_status is not ResolutionStatus.CONFIRMED:
        return []

    action_contract = _viewset_action_contract(class_node, bindings) or _inherited_action_contract(inherited_actions)
    if action_contract is None:
        return []

    base_node = next(
        (base for base in class_node.bases if _resolve_expression_name(base, bindings) in _known_viewset_base_names()),
        None,
    )
    if base_node is None:
        base_node = class_node.bases[0] if class_node.bases else None
    if base_node is None:
        return []

    evidence = _evidence(
        file=file,
        node=base_node,
        kind="framework_action_contract" if _viewset_action_contract(class_node, bindings) else "inherited_action_contract",
        status=ResolutionStatus.CONFIRMED,
        qualified_name=_resolve_expression_name(base_node, bindings),
    )
    return [
        DjangoViewAction(
            id=f"{view_id}#{name}",
            name=name,
            origin="framework_derived",
            methods=methods,
            detail=detail,
            security=security.model_copy(deep=True),
            evidence=[evidence],
        )
        for name, methods, detail in action_contract
    ]


def _inherited_action_contract(
    inherited_actions: list[DjangoViewAction] | None,
) -> list[tuple[str, list[str], bool]] | None:
    if not inherited_actions:
        return None
    contract = [
        (action.name, list(action.methods), action.detail)
        for action in inherited_actions
        if action.origin == "framework_derived" and action.detail is not None
    ]
    return contract or None


def _viewset_action_contract(
    class_node: nodes.ClassDef,
    bindings: dict[str, str],
) -> list[tuple[str, list[str], bool]] | None:
    base_names = {
        _resolve_expression_name(base_node, bindings)
        for base_node in class_node.bases
    }
    if "rest_framework.viewsets.ModelViewSet" in base_names:
        return _MODEL_VIEWSET_ACTIONS
    if "rest_framework.viewsets.ReadOnlyModelViewSet" in base_names:
        return _READ_ONLY_VIEWSET_ACTIONS
    return None


def _known_viewset_base_names() -> set[str]:
    return {
        "rest_framework.viewsets.ModelViewSet",
        "rest_framework.viewsets.ReadOnlyModelViewSet",
    }


def _local_security(
    node: nodes.ClassDef | nodes.FunctionDef,
    *,
    file: str,
    bindings: dict[str, str],
    scope: str,
    ignored_decorators: set[int] | None = None,
) -> ViewSecurity:
    security = ViewSecurity()
    ignored_decorators = ignored_decorators or set()

    for decorator in _decorators(node):
        if id(decorator) in ignored_decorators:
            continue
        qualified_name = _resolve_decorator_name(decorator, bindings)
        if _apply_known_decorator(
            security,
            decorator,
            file=file,
            bindings=bindings,
            scope=scope,
            qualified_name=qualified_name,
        ):
            continue
        if qualified_name not in {_ACTION_DECORATOR, _API_VIEW_DECORATOR}:
            security.raw_signals.append(
                _evidence(
                    file,
                    decorator,
                    f"{scope}_decorator",
                    _status_for_resolved_name(qualified_name),
                    qualified_name,
                )
            )

    if isinstance(node, nodes.ClassDef):
        _apply_class_assignments(security, node, file=file, bindings=bindings)

    return security


def _apply_known_decorator(
    security: ViewSecurity,
    decorator: nodes.NodeNG,
    *,
    file: str,
    bindings: dict[str, str],
    scope: str,
    qualified_name: str | None,
) -> bool:
    if qualified_name == _CSRF_EXEMPT_DECORATOR:
        _add_control_declaration(
            security.csrf,
            _evidence(file, decorator, f"{scope}_csrf_exempt", ResolutionStatus.CONFIRMED, qualified_name),
            state="exempt",
        )
        return True
    if qualified_name == _CSRF_PROTECT_DECORATOR:
        _add_control_declaration(
            security.csrf,
            _evidence(file, decorator, f"{scope}_csrf_protect", ResolutionStatus.CONFIRMED, qualified_name),
            state="configured",
        )
        return True
    if qualified_name == _LOGIN_REQUIRED_DECORATOR:
        _add_control_declaration(
            security.authentication,
            _evidence(file, decorator, f"{scope}_login_required", ResolutionStatus.CONFIRMED, qualified_name),
            state="login_required",
        )
        return True
    if qualified_name == _LOGIN_NOT_REQUIRED_DECORATOR:
        _add_control_declaration(
            security.authentication,
            _evidence(file, decorator, f"{scope}_login_not_required", ResolutionStatus.CONFIRMED, qualified_name),
            state="login_exempt",
        )
        return True
    if qualified_name == _AUTHENTICATION_DECORATOR and isinstance(decorator, nodes.Call):
        _add_value_declarations(
            security.authentication,
            decorator.args[0] if decorator.args else None,
            file=file,
            bindings=bindings,
            kind=f"{scope}_authentication_classes",
            state="configured",
        )
        return True
    if qualified_name == _PERMISSION_DECORATOR and isinstance(decorator, nodes.Call):
        _add_value_declarations(
            security.authorization,
            decorator.args[0] if decorator.args else None,
            file=file,
            bindings=bindings,
            kind=f"{scope}_permission_classes",
            state="configured",
        )
        return True
    return False


def _apply_class_assignments(
    security: ViewSecurity,
    class_node: nodes.ClassDef,
    *,
    file: str,
    bindings: dict[str, str],
) -> None:
    controls = {
        "authentication_classes": (security.authentication, "class_authentication_classes"),
        "permission_classes": (security.authorization, "class_permission_classes"),
    }
    for assignment in _direct_assignments(class_node):
        control_data = controls.get(_assignment_target_name(assignment))
        if control_data is None:
            continue
        control, kind = control_data
        _add_value_declarations(
            control,
            assignment.value,
            file=file,
            bindings=bindings,
            kind=kind,
            state="configured",
        )


def _add_action_control_keywords(
    security: ViewSecurity,
    decorator: nodes.Call,
    *,
    file: str,
    bindings: dict[str, str],
) -> None:
    for keyword in decorator.keywords:
        if keyword.arg == "authentication_classes":
            _add_value_declarations(
                security.authentication,
                keyword.value,
                file=file,
                bindings=bindings,
                kind="action_authentication_classes",
                state="configured",
            )
        elif keyword.arg == "permission_classes":
            _add_value_declarations(
                security.authorization,
                keyword.value,
                file=file,
                bindings=bindings,
                kind="action_permission_classes",
                state="configured",
            )


def _merge_security(local: ViewSecurity, inherited: ViewSecurity) -> ViewSecurity:
    return ViewSecurity(
        authentication=_merge_control(local.authentication, inherited.authentication),
        authorization=_merge_control(local.authorization, inherited.authorization),
        csrf=_merge_control(local.csrf, inherited.csrf),
        raw_signals=[*inherited.raw_signals, *local.raw_signals],
    )


def _merge_control(local: SecurityControl, inherited: SecurityControl) -> SecurityControl:
    local_has_declaration = bool(local.declarations)
    return SecurityControl(
        state=local.state if local_has_declaration else inherited.state,
        declarations=[*inherited.declarations, *local.declarations],
        effective_evidence=(local.effective_evidence if local_has_declaration else inherited.effective_evidence),
    )


def _add_control_declaration(control: SecurityControl, evidence: SourceEvidence, *, state: str) -> None:
    control.state = state
    control.declarations.append(evidence)
    control.effective_evidence.append(evidence)


def _add_value_declarations(
    control: SecurityControl,
    value: nodes.NodeNG | None,
    *,
    file: str,
    bindings: dict[str, str],
    kind: str,
    state: str,
) -> None:
    if value is None:
        return
    for item in _collection_items(value):
        qualified_name = _resolve_expression_name(item, bindings)
        if isinstance(item, nodes.Const) and isinstance(item.value, str):
            qualified_name = item.value
        _add_control_declaration(
            control,
            _evidence(file, item, kind, _status_for_resolved_name(qualified_name), qualified_name),
            state=state,
        )


def _action_decorator(function_node: nodes.FunctionDef, bindings: dict[str, str]) -> nodes.Call | None:
    for decorator in _decorators(function_node):
        if not isinstance(decorator, nodes.Call):
            continue
        qualified_name = _resolve_decorator_name(decorator, bindings)
        if qualified_name == _ACTION_DECORATOR or (qualified_name is None and _simple_name(decorator.func) == "action"):
            return decorator
    return None


def _action_methods(decorator: nodes.Call) -> list[str]:
    value = _keyword_value(decorator, "methods")
    if value is None and decorator.args:
        value = decorator.args[0]
    return [
        item.value.lower()
        for item in _collection_items(value)
        if isinstance(item, nodes.Const) and isinstance(item.value, str)
    ]


def _action_detail(decorator: nodes.Call) -> bool | None:
    value = _keyword_value(decorator, "detail")
    return value.value if isinstance(value, nodes.Const) and isinstance(value.value, bool) else None


def _action_string_keyword(decorator: nodes.Call, name: str) -> str | None:
    value = _keyword_value(decorator, name)
    return value.value if isinstance(value, nodes.Const) and isinstance(value.value, str) else None


def _keyword_value(call_node: nodes.Call, name: str) -> nodes.NodeNG | None:
    for keyword in call_node.keywords:
        if keyword.arg == name:
            return keyword.value
    return None


def _direct_methods(class_node: nodes.ClassDef) -> list[nodes.FunctionDef]:
    return [node for node in class_node.body if isinstance(node, nodes.FunctionDef)]


def _direct_assignments(class_node: nodes.ClassDef) -> list[nodes.Assign]:
    return [node for node in class_node.body if isinstance(node, nodes.Assign)]


def _assignment_target_name(assignment: nodes.Assign) -> str | None:
    for target in assignment.targets:
        if isinstance(target, nodes.AssignName):
            return target.name
    return None


def _decorators(node: nodes.ClassDef | nodes.FunctionDef) -> list[nodes.NodeNG]:
    return list(node.decorators.nodes) if node.decorators else []


def _resolve_decorator_name(node: nodes.NodeNG, bindings: dict[str, str]) -> str | None:
    target = node.func if isinstance(node, nodes.Call) else node
    return _resolve_expression_name(target, bindings)


def _decorator_status(node: nodes.Call, bindings: dict[str, str], expected_name: str) -> ResolutionStatus:
    return ResolutionStatus.CONFIRMED if _resolve_decorator_name(node, bindings) == expected_name else ResolutionStatus.PARTIAL


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


def _resolve_expression_name(node: nodes.NodeNG, bindings: dict[str, str]) -> str | None:
    if isinstance(node, nodes.Name):
        return bindings.get(node.name)
    if isinstance(node, nodes.Attribute):
        parent_name = _resolve_expression_name(node.expr, bindings)
        return f"{parent_name}.{node.attrname}" if parent_name else None
    return None


def _simple_name(node: nodes.NodeNG) -> str | None:
    if isinstance(node, nodes.Name):
        return node.name
    if isinstance(node, nodes.Attribute):
        return node.attrname
    return None


def _collection_items(node: nodes.NodeNG | None) -> list[nodes.NodeNG]:
    if isinstance(node, (nodes.List, nodes.Tuple, nodes.Set)):
        return list(node.elts)
    return [node] if node is not None else []


def _status_for_resolved_name(qualified_name: str | None) -> ResolutionStatus:
    return ResolutionStatus.CONFIRMED if qualified_name else ResolutionStatus.UNKNOWN


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
        expression=node.as_string(),
        kind=kind,
        status=status,
        qualified_name=qualified_name,
    )
