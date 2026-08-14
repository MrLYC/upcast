"""Tests for semantic Django/DRF view discovery."""

import astroid

from upcast.common.django.view_discovery import discover_views
from upcast.models.django_views import ResolutionStatus


SOURCE = '''
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


class HomeView(View):
    pass


class OrdersViewSet(ModelViewSet):
    pass


class StatusAPIView(APIView):
    pass


@api_view(["GET"])
def health(request):
    return None


class MaybeViewSet(ViewSet):
    pass


def helper():
    return None
'''


def test_discover_views_uses_framework_imports_and_preserves_partial_candidates():
    """Known Django/DRF imports confirm views while unresolved known bases remain partial."""
    module = astroid.parse(SOURCE, module_name="pkg.views")
    views = discover_views(module, file="pkg/views.py", module_name="pkg.views")

    by_id = {view.id: view for view in views}

    assert by_id["pkg.views.HomeView"].kind == "django_cbv"
    assert by_id["pkg.views.HomeView"].recognition.status is ResolutionStatus.CONFIRMED
    assert by_id["pkg.views.OrdersViewSet"].kind == "drf_viewset"
    assert by_id["pkg.views.OrdersViewSet"].recognition.status is ResolutionStatus.CONFIRMED
    assert by_id["pkg.views.StatusAPIView"].kind == "drf_api_view"
    assert by_id["pkg.views.StatusAPIView"].recognition.status is ResolutionStatus.CONFIRMED
    assert by_id["pkg.views.health"].kind == "drf_function_view"
    assert by_id["pkg.views.health"].recognition.status is ResolutionStatus.CONFIRMED
    assert by_id["pkg.views.MaybeViewSet"].recognition.status is ResolutionStatus.PARTIAL
    assert "pkg.views.helper" not in by_id


def test_discover_views_follows_a_resolved_project_view_ancestor():
    """A project class inheriting a known framework view remains a confirmed view."""
    base_module = astroid.parse(
        '''
from django.views import View


class ProjectBaseView(View):
    pass
''',
        module_name="pkg.base_views",
    )
    child_module = astroid.parse(
        '''
from .base_views import ProjectBaseView


class ReportsView(ProjectBaseView):
    pass
''',
        module_name="pkg.views",
    )
    base_view = discover_views(base_module, file="pkg/base_views.py", module_name="pkg.base_views")[0]

    views = discover_views(
        child_module,
        file="pkg/views.py",
        module_name="pkg.views",
        known_view_bases={base_view.id: base_view},
    )

    assert views[0].id == "pkg.views.ReportsView"
    assert views[0].kind == "django_cbv"
    assert views[0].recognition.status is ResolutionStatus.CONFIRMED
    assert views[0].recognition.evidence[0].qualified_name == "pkg.base_views.ProjectBaseView"
