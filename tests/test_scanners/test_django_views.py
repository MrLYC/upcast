"""Tests for the Django view scanner."""

from upcast.scanners.django_views import DjangoViewScanner


def _views(output):
    return {view.name: view for views in output.results.values() for view in views}


def test_scans_drf_views_and_preserves_security_evidence(tmp_path):
    views_file = tmp_path / "demo" / "views.py"
    views_file.parent.mkdir()
    views_file.write_text(
        """
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from project.security.decorators import login_exempt


class UserViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    authentication_classes = []

    @action(
        methods=["post"],
        detail=False,
        url_path="sync",
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    @login_exempt
    def sync(self, request):
        return None


@csrf_exempt
@login_exempt
@api_view(["GET"])
def health(request):
    return None


@api_view(["POST"])
async def async_health(request):
    return None


class NotAView:
    pass
"""
    )

    output = DjangoViewScanner().scan(tmp_path)
    views = _views(output)

    assert set(views) == {"UserViewSet", "health", "async_health"}

    viewset = views["UserViewSet"]
    assert viewset.kind == "class"
    assert viewset.status == "confirmed"
    assert "drf_view_base" in viewset.identified_by
    assert viewset.permission_classes == ["AllowAny"]
    assert viewset.authentication_classes == []
    assert viewset.actions[0].name == "sync"
    assert viewset.actions[0].methods == ["POST"]
    assert viewset.actions[0].detail is False
    assert viewset.actions[0].permission_classes == ["AllowAny"]
    assert viewset.actions[0].authentication_classes == []
    assert viewset.actions[0].login_exempt is True

    health = views["health"]
    assert health.kind == "function"
    assert health.status == "confirmed"
    assert "drf_api_view_decorator" in health.identified_by
    assert health.http_methods == ["GET"]
    assert health.login_exempt is True
    assert health.csrf_exempt is True

    assert views["async_health"].http_methods == ["POST"]


def test_route_reference_identifies_plain_function_view(tmp_path):
    views_file = tmp_path / "demo" / "views.py"
    urls_file = tmp_path / "demo" / "urls.py"
    views_file.parent.mkdir()
    views_file.write_text(
        """
def health(request):
    return None
"""
    )
    urls_file.write_text(
        """
from django.urls import path
from .views import health

urlpatterns = [path("health/", health)]
"""
    )

    output = DjangoViewScanner().scan(tmp_path)
    views = _views(output)

    assert views["health"].status == "confirmed"
    assert "route_reference" in views["health"].identified_by
    assert views["health"].route_linkage[0].full_path == "health/"


def test_route_reference_identifies_instance_method_handler(tmp_path):
    views_file = tmp_path / "demo" / "handlers.py"
    urls_file = tmp_path / "demo" / "urls.py"
    views_file.parent.mkdir()
    views_file.write_text(
        """
class HealthHandler:
    def health(self, request):
        return None
"""
    )
    urls_file.write_text(
        """
from django.urls import path
from .handlers import HealthHandler

urlpatterns = [path("health/", HealthHandler().health)]
"""
    )

    output = DjangoViewScanner().scan(tmp_path)
    view = next(view for views in output.results.values() for view in views if view.qualname.endswith("HealthHandler.health"))

    assert view.kind == "method"
    assert view.status == "confirmed"
    assert view.name == "health"
    assert view.route_linkage[0].full_path == "health/"


def test_scans_unreferenced_views_in_arbitrarily_named_files(tmp_path):
    endpoint_file = tmp_path / "app" / "endpoints.py"
    endpoint_file.parent.mkdir()
    endpoint_file.write_text(
        """
from rest_framework.views import APIView


class HealthEndpoint(APIView):
    pass
"""
    )

    output = DjangoViewScanner().scan(tmp_path)
    view = next(view for views in output.results.values() for view in views if view.name == "HealthEndpoint")

    assert view.status == "confirmed"
    assert output.summary.files_scanned == 1


def test_resolves_view_inheritance_across_imported_modules(tmp_path):
    base_file = tmp_path / "app" / "base.py"
    views_file = tmp_path / "app" / "views.py"
    base_file.parent.mkdir()
    base_file.write_text(
        """
from rest_framework.views import APIView

class BaseApiView(APIView):
    pass
"""
    )
    views_file.write_text(
        """
from .base import BaseApiView

class ConcreteEndpoint(BaseApiView):
    pass
"""
    )

    output = DjangoViewScanner().scan(tmp_path)
    views = _views(output)

    assert views["ConcreteEndpoint"].status == "confirmed"
    assert "inherited_view_base" in views["ConcreteEndpoint"].identified_by


def test_resolves_module_imported_from_package_in_urlconf(tmp_path):
    views_file = tmp_path / "app" / "handlers.py"
    urls_file = tmp_path / "app" / "urls.py"
    views_file.parent.mkdir()
    views_file.write_text("def health(request):\n    return None\n")
    urls_file.write_text(
        """
from django.urls import path
from . import handlers

urlpatterns = [path("health/", handlers.health)]
"""
    )

    output = DjangoViewScanner().scan(tmp_path)
    views = _views(output)

    assert views["health"].status == "confirmed"
    assert views["health"].route_linkage[0].url_module == "app.urls"


def test_resolves_wildcard_view_import_in_urlconf(tmp_path):
    views_file = tmp_path / "app" / "views.py"
    urls_file = tmp_path / "app" / "urls.py"
    views_file.parent.mkdir()
    views_file.write_text("def health(request):\n    return None\n")
    urls_file.write_text(
        """
from django.urls import path
from .views import *

urlpatterns = [path("health/", health)]
"""
    )

    output = DjangoViewScanner().scan(tmp_path)
    views = _views(output)

    assert views["health"].status == "confirmed"
    assert views["health"].route_linkage[0].url_module == "app.urls"


def test_resolves_views_package_reexports(tmp_path):
    package = tmp_path / "app" / "views"
    urls_file = tmp_path / "app" / "urls.py"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("from .health import health\n")
    (package / "health.py").write_text("def health(request):\n    return None\n")
    urls_file.write_text(
        """
from django.urls import path
from . import views

urlpatterns = [path("health/", views.health)]
"""
    )

    output = DjangoViewScanner().scan(tmp_path)
    views = _views(output)

    assert views["health"].module == "app.views.health"
    assert views["health"].route_linkage[0].url_module == "app.urls"


def test_resolves_wildcard_views_package_reexports(tmp_path):
    package = tmp_path / "app" / "views"
    urls_file = tmp_path / "app" / "urls.py"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("from .health import *\n")
    (package / "health.py").write_text("def health(request):\n    return None\n")
    urls_file.write_text(
        """
from django.urls import path
from . import views

urlpatterns = [path("health/", views.health)]
"""
    )

    output = DjangoViewScanner().scan(tmp_path)
    views = _views(output)

    assert views["health"].module == "app.views.health"
    assert views["health"].route_linkage[0].url_module == "app.urls"


def test_resolves_imports_below_a_source_root_and_package_reexports(tmp_path):
    package = tmp_path / "workspace" / "app" / "views"
    urls_file = tmp_path / "workspace" / "app" / "urls.py"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("from .health import health\n")
    (package / "health.py").write_text("def health(request):\n    return None\n")
    urls_file.write_text(
        """
from django.urls import path
from app.views import health

urlpatterns = [path("health/", health)]
"""
    )

    output = DjangoViewScanner().scan(tmp_path)
    view = next(view for views in output.results.values() for view in views if view.name == "health")

    assert view.module == "workspace.app.views.health"
    assert view.route_linkage[0].url_module == "workspace.app.urls"


def test_resolves_nested_package_reexports_below_a_source_root(tmp_path):
    package = tmp_path / "workspace" / "app" / "views"
    viewsets = package / "viewsets"
    urls_file = tmp_path / "workspace" / "app" / "urls.py"
    viewsets.mkdir(parents=True)
    (package / "__init__.py").write_text("from .viewsets import *\n")
    (viewsets / "__init__.py").write_text("from .health import *\n")
    (viewsets / "health.py").write_text("def health(request):\n    return None\n")
    urls_file.write_text(
        """
from django.urls import path
from app.views import health

urlpatterns = [path("health/", health)]
"""
    )

    output = DjangoViewScanner().scan(tmp_path)
    view = next(view for views in output.results.values() for view in views if view.name == "health")

    assert view.module == "workspace.app.views.viewsets.health"
    assert view.route_linkage[0].url_module == "workspace.app.urls"


def test_resolves_imports_below_non_python_source_namespace(tmp_path):
    views_file = tmp_path / "vendor-tree" / "agent-package" / "apis" / "assistant.py"
    urls_file = tmp_path / "vendor-tree" / "agent-package" / "apis" / "urls.py"
    views_file.parent.mkdir(parents=True)
    views_file.write_text(
        """
from rest_framework.views import APIView

class AssistantView(APIView):
    pass
"""
    )
    urls_file.write_text(
        """
from django.urls import path
from apis.assistant import AssistantView

urlpatterns = [path("assistant/", AssistantView.as_view())]
"""
    )

    output = DjangoViewScanner().scan(tmp_path)
    views = _views(output)

    assert views["AssistantView"].module == "vendor-tree.agent-package.apis.assistant"
    assert views["AssistantView"].route_linkage[0].url_module == "vendor-tree.agent-package.apis.urls"


def test_does_not_link_unmounted_router_registration(tmp_path):
    views_file = tmp_path / "app" / "views.py"
    urls_file = tmp_path / "app" / "urls.py"
    views_file.parent.mkdir()
    views_file.write_text(
        """
from rest_framework.viewsets import ViewSet


class UserViewSet(ViewSet):
    pass
"""
    )
    urls_file.write_text(
        """
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
urlpatterns = []
"""
    )

    output = DjangoViewScanner().scan(tmp_path)
    view = next(view for views in output.results.values() for view in views if view.name == "UserViewSet")

    assert view.route_linkage == []


def test_links_router_registration_across_router_and_url_modules(tmp_path):
    views_file = tmp_path / "app" / "views.py"
    router_file = tmp_path / "app" / "router.py"
    urls_file = tmp_path / "app" / "urls.py"
    views_file.parent.mkdir()
    views_file.write_text(
        """
from rest_framework.viewsets import ViewSet


class UserViewSet(ViewSet):
    pass
"""
    )
    router_file.write_text(
        """
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
"""
    )
    urls_file.write_text(
        """
from django.urls import include, path
from .router import router

urlpatterns = [path("api/", include(router.urls))]
"""
    )

    output = DjangoViewScanner().scan(tmp_path)
    view = next(view for views in output.results.values() for view in views if view.name == "UserViewSet")

    assert len(view.route_linkage) == 1
    assert view.route_linkage[0].url_module == "app.urls"
    assert view.route_linkage[0].pattern == "users"


def test_does_not_treat_helper_routes_as_module_routes(tmp_path):
    views_file = tmp_path / "app" / "views.py"
    urls_file = tmp_path / "app" / "urls.py"
    views_file.parent.mkdir()
    views_file.write_text("def health(request):\n    return None\n")
    urls_file.write_text(
        """
from django.urls import path
from .views import health

urlpatterns = []

def build_patterns():
    return [path("health/", health)]
"""
    )

    output = DjangoViewScanner().scan(tmp_path)

    assert all(view.name != "health" for views in output.results.values() for view in views)
