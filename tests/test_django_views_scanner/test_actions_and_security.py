"""Tests for bounded DRF action and local security analysis."""

import astroid

from upcast.common.django.view_security import analyze_function_security, analyze_view_security
from upcast.models.django_views import ResolutionStatus


SOURCE = """
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_not_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet


@csrf_exempt
@custom_guard
class OrdersViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(
        methods=["post"],
        detail=True,
        url_path="archive-item",
        url_name="archive-item",
        permission_classes=[AllowAny],
    )
    def archive(self, request):
        return None


@login_required
@custom_guard
def dashboard(request):
    return None


@login_not_required
def public_status(request):
    return None
"""


def test_viewset_actions_keep_overrides_and_unknown_decorators_as_evidence():
    """Explicit actions override class controls without hiding inherited evidence."""
    module = astroid.parse(SOURCE, module_name="pkg.views")
    class_node = module.locals["OrdersViewSet"][0]

    security, actions = analyze_view_security(
        class_node,
        file="pkg/views.py",
        module_name="pkg.views",
        view_id="pkg.views.OrdersViewSet",
        kind="drf_viewset",
        recognition_status=ResolutionStatus.CONFIRMED,
    )

    archive = next(action for action in actions if action.name == "archive")
    derived_names = {action.name for action in actions if action.origin == "framework_derived"}

    assert security.authentication.state == "configured"
    assert security.authorization.state == "configured"
    assert security.csrf.state == "exempt"
    assert {signal.expression for signal in security.raw_signals} == {"custom_guard"}
    assert archive.origin == "decorator"
    assert archive.methods == ["post"]
    assert archive.detail is True
    assert archive.url_path == "archive-item"
    assert archive.url_name == "archive-item"
    assert archive.security.authorization.effective_evidence[-1].expression == "AllowAny"
    assert [item.expression for item in archive.security.authorization.declarations] == [
        "IsAuthenticated",
        "AllowAny",
    ]
    assert {"list", "retrieve", "create", "update", "partial_update", "destroy"} <= derived_names


def test_function_security_does_not_turn_login_or_custom_decorators_into_login_exemption():
    """Authentication, CSRF, and unclassified decorators remain separate facts."""
    module = astroid.parse(SOURCE, module_name="pkg.views")
    function_node = module.locals["dashboard"][0]

    security = analyze_function_security(function_node, file="pkg/views.py", module_name="pkg.views")

    assert security.authentication.state == "login_required"
    assert security.authentication.state != "login_exempt"
    assert security.csrf.state == "unknown"
    assert [signal.expression for signal in security.raw_signals] == ["custom_guard"]


def test_function_security_reports_the_standard_explicit_login_exemption_only():
    """A framework login-not-required decorator is separate from DRF/CSRF signals."""
    module = astroid.parse(SOURCE, module_name="pkg.views")
    function_node = module.locals["public_status"][0]

    security = analyze_function_security(function_node, file="pkg/views.py", module_name="pkg.views")

    assert security.authentication.state == "login_exempt"
    assert security.authentication.declarations[0].qualified_name == "django.contrib.auth.decorators.login_not_required"
