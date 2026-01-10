"""Tests for Django REST Framework router detection."""

import pytest
from pathlib import Path

from upcast.scanners.django_urls import DjangoUrlScanner


class TestDRFRouters:
    """Test DRF router detection and expansion."""

    def test_default_router_detection(self, tmp_path, scanner):
        """Test detection of DefaultRouter usage."""
        code = """
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')

urlpatterns = [
    path('api/', include(router.urls)),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # Should detect router include and expand it
        assert output.summary.total_patterns >= 1

        module_name = list(output.results.keys())[0]
        patterns = output.results[module_name].urlpatterns

        # Check that at least one pattern is a router registration
        router_patterns = [p for p in patterns if p.type == "router_registration"]
        assert len(router_patterns) >= 1

        # Check the first router pattern
        router_pattern = router_patterns[0]
        assert router_pattern.basename == "article"
        assert router_pattern.router_type == "DefaultRouter"

    def test_simple_router_detection(self, tmp_path, scanner):
        """Test detection of SimpleRouter usage."""
        code = """
from rest_framework.routers import SimpleRouter
from .views import PostViewSet

router = SimpleRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('api/', include(router.urls)),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_patterns >= 1

        module_name = list(output.results.keys())[0]
        patterns = output.results[module_name].urlpatterns

        router_patterns = [p for p in patterns if p.type == "router_registration"]
        assert len(router_patterns) >= 1

        router_pattern = router_patterns[0]
        assert router_pattern.basename == "post"
        assert router_pattern.router_type == "SimpleRouter"

    def test_router_without_basename(self, tmp_path, scanner):
        """Test router registration without explicit basename."""
        code = """
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_patterns >= 1

        module_name = list(output.results.keys())[0]
        patterns = output.results[module_name].urlpatterns

        router_patterns = [p for p in patterns if p.type == "router_registration"]
        assert len(router_patterns) >= 1

    def test_multiple_router_registrations(self, tmp_path, scanner):
        """Test multiple ViewSets registered to same router."""
        code = """
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('api/', include(router.urls)),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        module_name = list(output.results.keys())[0]
        patterns = output.results[module_name].urlpatterns

        router_patterns = [p for p in patterns if p.type == "router_registration"]

        # Should have 3 router registrations
        assert len(router_patterns) == 3

        basenames = {p.basename for p in router_patterns}
        assert basenames == {"article", "post", "comment"}

    def test_router_urls_assigned_directly(self, tmp_path, scanner):
        """Test urlpatterns = router.urls pattern."""
        code = """
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')

urlpatterns = router.urls
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # When urlpatterns = router.urls, it's an attribute access
        # The scanner doesn't detect this as it's not a list/tuple
        # This is expected behavior - patterns are not statically defined
        assert output.summary.total_patterns == 0

    def test_router_with_prefix(self, tmp_path, scanner):
        """Test router include with URL prefix."""
        code = """
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_patterns >= 1

        module_name = list(output.results.keys())[0]
        patterns = output.results[module_name].urlpatterns

        router_patterns = [p for p in patterns if p.type == "router_registration"]
        assert len(router_patterns) >= 1

        # Check that the pattern includes the prefix
        router_pattern = router_patterns[0]
        assert router_pattern.pattern.startswith("api/v1/")
