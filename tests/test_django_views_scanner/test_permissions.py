"""Tests for bounded DRF permission resolution."""

import astroid

from upcast.common.django.permission_resolver import (
    PermissionModule,
    apply_drf_defaults,
    extract_drf_defaults,
    resolve_permission_definitions,
)
from upcast.common.django.view_security import analyze_view_security
from upcast.models.django_views import ResolutionStatus


SETTINGS_SOURCE = '''
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.TokenAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
}
'''

PERMISSIONS_SOURCE = '''
from rest_framework.permissions import BasePermission


class OwnerPermission(BasePermission):
    """Require access to an object owned by the requester."""

    def has_permission(self, request, view):
        return access_service.allows(request)

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
'''

VIEWS_SOURCE = '''
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .permissions import OwnerPermission


class ReportsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated | OwnerPermission]


class DefaultedViewSet(ModelViewSet):
    pass


class RestrictedViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated & OwnerPermission]
'''


def test_permission_resolution_keeps_expression_shape_and_follows_custom_permission_once():
    """Local declarations override defaults while retaining one-hop permission facts."""
    settings_module = astroid.parse(SETTINGS_SOURCE, module_name="pkg.settings")
    permissions_module = astroid.parse(PERMISSIONS_SOURCE, module_name="pkg.permissions")
    views_module = astroid.parse(VIEWS_SOURCE, module_name="pkg.views")
    modules = [
        PermissionModule(settings_module, "pkg.settings", "pkg/settings.py"),
        PermissionModule(permissions_module, "pkg.permissions", "pkg/permissions.py"),
        PermissionModule(views_module, "pkg.views", "pkg/views.py"),
    ]
    defaults = extract_drf_defaults(modules)
    reports = views_module.locals["ReportsViewSet"][0]
    defaulted = views_module.locals["DefaultedViewSet"][0]
    restricted = views_module.locals["RestrictedViewSet"][0]

    reports_security, _ = analyze_view_security(
        reports,
        file="pkg/views.py",
        module_name="pkg.views",
        view_id="pkg.views.ReportsViewSet",
        kind="drf_viewset",
        recognition_status=ResolutionStatus.CONFIRMED,
    )
    defaulted_security, _ = analyze_view_security(
        defaulted,
        file="pkg/views.py",
        module_name="pkg.views",
        view_id="pkg.views.DefaultedViewSet",
        kind="drf_viewset",
        recognition_status=ResolutionStatus.CONFIRMED,
    )
    restricted_security, _ = analyze_view_security(
        restricted,
        file="pkg/views.py",
        module_name="pkg.views",
        view_id="pkg.views.RestrictedViewSet",
        kind="drf_viewset",
        recognition_status=ResolutionStatus.CONFIRMED,
    )

    resolved_reports = resolve_permission_definitions(apply_drf_defaults(reports_security, defaults), modules)
    resolved_defaulted = apply_drf_defaults(defaulted_security, defaults)
    resolved_restricted = resolve_permission_definitions(apply_drf_defaults(restricted_security, defaults), modules)

    authorization = resolved_reports.authorization
    expression = authorization.permission_expressions[0]
    definition = authorization.permission_definitions[0]

    assert authorization.effective_evidence[0].expression == "IsAuthenticated | OwnerPermission"
    assert expression.operator == "|"
    assert [child.qualified_name for child in expression.children] == [
        "rest_framework.permissions.IsAuthenticated",
        "pkg.permissions.OwnerPermission",
    ]
    assert definition.qualified_name == "pkg.permissions.OwnerPermission"
    assert definition.docstring == "Require access to an object owned by the requester."
    assert [method.expression for method in definition.check_methods] == [
        "def has_permission(self, request, view):\n    return access_service.allows(request)",
        "def has_object_permission(self, request, view, obj):\n    return obj.owner == request.user",
    ]
    assert resolved_defaulted.authorization.state == "default"
    assert resolved_defaulted.authorization.effective_evidence[0].qualified_name == "rest_framework.permissions.IsAuthenticated"
    assert resolved_defaulted.authentication.state == "default"
    assert resolved_defaulted.authentication.effective_evidence[0].qualified_name == "rest_framework.authentication.TokenAuthentication"
    assert resolved_restricted.authorization.permission_expressions[0].operator == "&"
