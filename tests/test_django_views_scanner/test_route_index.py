"""Tests for reverse Django URL and DRF Router references."""

import astroid

from upcast.common.django.route_index import RouteModule, build_route_index
from upcast.models.django_views import ResolutionStatus


def test_route_index_links_direct_routes_and_mounted_router_registrations():
    """Route targets use canonical imported symbols and mounted routers are confirmed."""
    module = astroid.parse(
        """
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
        module_name="pkg.urls",
    )

    index = build_route_index([RouteModule(module=module, module_name="pkg.urls", file="pkg/urls.py")])

    direct_reference = index.references_for("pkg.views.health")[0]
    router_reference = index.references_for("pkg.views.OrderViewSet")[0]

    assert direct_reference.kind == "direct"
    assert direct_reference.pattern == "health/"
    assert direct_reference.status is ResolutionStatus.CONFIRMED
    assert router_reference.kind == "router"
    assert router_reference.status is ResolutionStatus.CONFIRMED
    assert router_reference.prefix == "orders"
    assert router_reference.basename == "order"
    assert router_reference.router_type == "DefaultRouter"
    assert len(router_reference.evidence) == 2


def test_route_index_links_re_path_targets():
    """Regular-expression URL routes use the same canonical target index."""
    module = astroid.parse(
        """
from django.urls import re_path
from .views import health

urlpatterns = [re_path(r"^health/$", health)]
""",
        module_name="pkg.urls",
    )

    index = build_route_index([RouteModule(module=module, module_name="pkg.urls", file="pkg/urls.py")])

    reference = index.references_for("pkg.views.health")[0]

    assert reference.kind == "direct"
    assert reference.pattern == "^health/$"


def test_route_index_keeps_unmounted_router_registration_as_partial_candidate():
    """A registration without a router.urls mount is not reported as a confirmed endpoint."""
    module = astroid.parse(
        """
from rest_framework.routers import SimpleRouter
from .views import AuditViewSet

router = SimpleRouter()
router.register("audits", AuditViewSet, basename="audit")
""",
        module_name="pkg.urls",
    )

    index = build_route_index([RouteModule(module=module, module_name="pkg.urls", file="pkg/urls.py")])

    reference = index.references_for("pkg.views.AuditViewSet")[0]

    assert reference.status is ResolutionStatus.PARTIAL
    assert reference.prefix == "audits"


def test_route_index_resolves_cbv_as_view_and_keeps_unresolved_route_target_evidence():
    """Direct routes distinguish a resolved CBV target from a dynamic callback."""
    module = astroid.parse(
        """
from django.urls import path
from .views import DetailView

urlpatterns = [
    path("detail/", DetailView.as_view()),
    path("dynamic/", build_callback()),
]
""",
        module_name="pkg.urls",
    )

    index = build_route_index([RouteModule(module=module, module_name="pkg.urls", file="pkg/urls.py")])

    reference = index.references_for("pkg.views.DetailView")[0]

    assert reference.kind == "direct"
    assert reference.pattern == "detail/"
    assert reference.status is ResolutionStatus.CONFIRMED
    assert len(index.unresolved) == 1
    assert index.unresolved[0].status is ResolutionStatus.UNKNOWN
    assert "build_callback()" in index.unresolved[0].evidence[0].expression


def test_route_index_confirms_router_assigned_directly_to_urlpatterns():
    """A router.urls assignment has the same mounted status as include(router.urls)."""
    module = astroid.parse(
        """
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register("orders", OrderViewSet)
urlpatterns = router.urls
""",
        module_name="pkg.urls",
    )

    index = build_route_index([RouteModule(module=module, module_name="pkg.urls", file="pkg/urls.py")])

    reference = index.references_for("pkg.views.OrderViewSet")[0]

    assert reference.status is ResolutionStatus.CONFIRMED
    assert reference.prefix == "orders"
    assert reference.evidence[-1].kind == "router_mount"


def test_route_index_recognizes_router_when_its_parent_package_is_imported():
    """`import rest_framework.routers` keeps the package-root binding intact."""
    module = astroid.parse(
        """
import rest_framework.routers
from .views import OrderViewSet

router = rest_framework.routers.DefaultRouter()
router.register("orders", OrderViewSet)
urlpatterns = router.urls
""",
        module_name="pkg.urls",
    )

    index = build_route_index([RouteModule(module=module, module_name="pkg.urls", file="pkg/urls.py")])

    assert index.references_for("pkg.views.OrderViewSet")[0].router_type == "DefaultRouter"


def test_route_index_matches_imported_router_mounts_across_modules():
    """Router registration and `.urls` mounting may live in separate URL modules."""
    router_module = astroid.parse(
        """
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register("orders", OrderViewSet)
""",
        module_name="pkg.router",
    )
    urls_module = astroid.parse(
        """
from .router import router

urlpatterns = router.urls
""",
        module_name="pkg.urls",
    )

    index = build_route_index([
        RouteModule(module=router_module, module_name="pkg.router", file="pkg/router.py"),
        RouteModule(module=urls_module, module_name="pkg.urls", file="pkg/urls.py"),
    ])

    reference = index.references_for("pkg.views.OrderViewSet")[0]

    assert reference.status is ResolutionStatus.CONFIRMED
    assert [evidence.file for evidence in reference.evidence] == ["pkg/router.py", "pkg/urls.py"]
