"""Integration tests for the standalone Django view scanner."""

from upcast.models.django_views import ResolutionStatus
from upcast.scanners.django_views import DjangoViewScanner


def test_scanner_links_cross_file_routes_and_enriches_view_records(tmp_project):
    """A synthetic project keeps direct/function and Router/ViewSet evidence mergeable."""
    project_dir = tmp_project({
        "pkg/__init__.py": "",
        "pkg/settings.py": """
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
}
""",
        "pkg/models.py": """
class Order:
    pass
""",
        "pkg/permissions.py": """
from rest_framework.permissions import BasePermission


class OwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
""",
        "pkg/serializers.py": """
from .models import Order


class OrderSerializer:
    class Meta:
        model = Order
""",
        "pkg/views.py": """
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import Order
from .permissions import OwnerPermission
from .serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [OwnerPermission]

    @action(methods=["post"], detail=True, permission_classes=[AllowAny])
    def archive(self, request):
        return Order.objects.create()


@custom_audit
def health(request):
    return None
""",
        "pkg/urls.py": """
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet, health

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="order")

urlpatterns = [
    path("health/", health),
    path("api/", include(router.urls)),
]
""",
    })

    output = DjangoViewScanner().scan(project_dir)

    order_view = output.results["pkg.views.OrderViewSet"]
    health_view = output.results["pkg.views.health"]
    archive = next(action for action in order_view.actions if action.name == "archive")

    assert list(output.results) == sorted(output.results)
    assert output.summary.total_views == 2
    assert output.summary.total_actions >= 7
    assert order_view.route_refs[0].kind == "router"
    assert order_view.route_refs[0].status is ResolutionStatus.CONFIRMED
    assert health_view.recognition.status is ResolutionStatus.CONFIRMED
    assert health_view.route_refs[0].pattern == "health/"
    assert [signal.expression for signal in health_view.security.raw_signals] == ["custom_audit"]
    assert (
        order_view.security.authorization.permission_definitions[0].qualified_name == "pkg.permissions.OwnerPermission"
    )
    assert any(usage.model == "pkg.models.Order" for usage in order_view.model_usages)
    assert archive.security.authorization.effective_evidence[-1].qualified_name == "rest_framework.permissions.AllowAny"
    assert archive.model_usages[0].operation == "write"


def test_scanner_keeps_route_referenced_unconfirmed_class_controls_for_follow_up(tmp_project):
    """A route does not turn an unknown class into confirmed, but its evidence survives."""
    project_dir = tmp_project({
        "pkg/__init__.py": "",
        "pkg/views.py": """
@custom_guard
class AuditEndpoint(CustomEndpoint):
    authentication_classes = [ExternalAuthentication]
""",
        "pkg/urls.py": """
from django.urls import path
from .views import AuditEndpoint

urlpatterns = [path("audit/", AuditEndpoint.as_view())]
""",
    })

    output = DjangoViewScanner().scan(project_dir)
    audit_view = output.results["pkg.views.AuditEndpoint"]

    assert audit_view.recognition.status is ResolutionStatus.PARTIAL
    assert audit_view.route_refs[0].status is ResolutionStatus.CONFIRMED
    assert [signal.expression for signal in audit_view.security.raw_signals] == ["custom_guard"]
    assert audit_view.security.authentication.declarations[0].expression == "ExternalAuthentication"
    assert audit_view.security.authentication.declarations[0].status is ResolutionStatus.UNKNOWN


def test_scanner_inherits_project_viewset_security_and_standard_action_contract(tmp_project):
    """A confirmed project ViewSet ancestor contributes bounded inherited evidence."""
    project_dir = tmp_project({
        "pkg/__init__.py": "",
        "pkg/base_views.py": """
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class ProjectViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
""",
        "pkg/views.py": """
from .base_views import ProjectViewSet


class ReportsViewSet(ProjectViewSet):
    pass
""",
    })

    output = DjangoViewScanner().scan(project_dir)
    reports = output.results["pkg.views.ReportsViewSet"]

    assert reports.recognition.status is ResolutionStatus.CONFIRMED
    assert (
        reports.security.authorization.effective_evidence[0].qualified_name
        == "rest_framework.permissions.IsAuthenticated"
    )
    assert {action.name for action in reports.actions if action.origin == "framework_derived"} == {
        "list",
        "retrieve",
        "create",
        "update",
        "partial_update",
        "destroy",
    }


def test_scanner_exposes_unresolved_route_targets_without_creating_a_fake_view(tmp_project):
    """Dynamic callback expressions remain inspectable outside the internal route index."""
    project_dir = tmp_project({
        "pkg/urls.py": """
from django.urls import path

urlpatterns = [path("dynamic/", build_callback())]
""",
    })

    output = DjangoViewScanner().scan(project_dir)

    assert output.results == {}
    assert len(output.unresolved_route_references) == 1
    assert output.unresolved_route_references[0].status is ResolutionStatus.UNKNOWN
    assert "build_callback()" in output.unresolved_route_references[0].evidence[0].expression


def test_scanner_links_router_registration_and_mount_across_modules(tmp_project):
    """A Router module can be mounted from a separate URLconf module."""
    project_dir = tmp_project({
        "pkg/__init__.py": "",
        "pkg/views.py": """
from rest_framework.viewsets import ModelViewSet


class OrderViewSet(ModelViewSet):
    pass
""",
        "pkg/router.py": """
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register("orders", OrderViewSet)
""",
        "pkg/urls.py": """
from .router import router

urlpatterns = router.urls
""",
    })

    output = DjangoViewScanner().scan(project_dir)
    reference = output.results["pkg.views.OrderViewSet"].route_refs[0]

    assert reference.status is ResolutionStatus.CONFIRMED
    assert [evidence.file for evidence in reference.evidence] == ["pkg/router.py", "pkg/urls.py"]
