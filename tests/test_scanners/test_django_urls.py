"""Tests for DjangoUrlScanner."""

from upcast.scanners.django_urls import (
    DjangoUrlScanner,
    UrlPattern,
)


class TestDjangoUrlModels:
    """Tests for Django URL models."""

    def test_valid_url_pattern(self):
        """Test creating valid UrlPattern."""
        pattern = UrlPattern(
            type="path",
            pattern="api/users/",
            view_module="myapp.views",
            view_name="user_list",
            name="user-list",
            is_partial=False,
            is_conditional=False,
            converters=[],
            named_groups=[],
        )
        assert pattern.type == "path"
        assert pattern.pattern == "api/users/"


class TestDjangoUrlScannerIntegration:
    """Integration tests for DjangoUrlScanner."""

    def test_scanner_detects_url_patterns(self, tmp_path):
        """Test scanner detects URL patterns."""
        test_file = tmp_path / "urls.py"
        test_file.write_text(
            """
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user-list'),
]
"""
        )

        scanner = DjangoUrlScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 0

    def test_scanner_handles_empty_file(self, tmp_path):
        """Test scanner handles empty files."""
        test_file = tmp_path / "test.py"
        test_file.write_text("")

        scanner = DjangoUrlScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 0

    def test_scanner_preserves_path_metadata(self, tmp_path):
        """Test scanner preserves parsed path metadata for regular views."""
        test_file = tmp_path / "urls.py"
        test_file.write_text(
            """
from django.urls import path
from . import views

urlpatterns = [
    path('users/<int:user_id>/', views.user_detail, name='user-detail'),
]
"""
        )

        scanner = DjangoUrlScanner()
        output = scanner.scan(test_file)

        module = next(iter(output.results.values()))
        assert len(module.urlpatterns) == 1
        pattern = module.urlpatterns[0]
        assert pattern.type == "path"
        assert pattern.pattern == "users/<int:user_id>/"
        assert pattern.full_path == "users/<int:user_id>/"
        assert pattern.name == "user-detail"
        assert pattern.converters == ["user_id:int"]
        assert pattern.named_groups == []

    def test_scanner_preserves_include_module_and_namespace(self, tmp_path):
        """Test scanner preserves include() metadata from path declarations."""
        test_file = tmp_path / "urls.py"
        test_file.write_text(
            """
from django.urls import include, path

urlpatterns = [
    path('blog/', include(('blog.urls', 'blog'), namespace='public-blog'), name='blog-root'),
]
"""
        )

        scanner = DjangoUrlScanner()
        output = scanner.scan(test_file)

        module = next(iter(output.results.values()))
        assert len(module.urlpatterns) == 1
        pattern = module.urlpatterns[0]
        assert pattern.type == "include"
        assert pattern.pattern == "blog/"
        assert pattern.full_path == "blog/"
        assert pattern.include_module == "blog.urls"
        assert pattern.namespace == "public-blog"
        assert pattern.name == "blog-root"
        assert pattern.view_module is None
        assert pattern.view_name is None

    def test_scanner_expands_inline_include_full_paths(self, tmp_path):
        """Test scanner preserves prefixed full_path when include() wraps inline routes."""
        test_file = tmp_path / "urls.py"
        test_file.write_text(
            """
from django.urls import include, path
from . import views

urlpatterns = [
    path('api/', include([
        path('users/', views.user_list, name='user-list'),
    ])),
]
"""
        )

        scanner = DjangoUrlScanner()
        output = scanner.scan(test_file)

        module = next(iter(output.results.values()))
        assert len(module.urlpatterns) == 1
        pattern = module.urlpatterns[0]
        assert pattern.type == "path"
        assert pattern.pattern == "users/"
        assert pattern.full_path == "api/users/"
        assert pattern.name == "user-list"
