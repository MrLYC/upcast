"""Tests for edge cases and error handling."""

import pytest
from pathlib import Path

from upcast.scanners.django_urls import DjangoUrlScanner


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_aliased_imports(self, tmp_path, scanner):
        """Test URLs with aliased imports."""
        code = """
from django.urls import path as url_path
from . import views

urlpatterns = [
    url_path('articles/', views.article_list, name='article-list'),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # The scanner currently does not support aliased imports
        # This is a known limitation - url_path is not recognized as path
        assert output.summary.total_patterns == 0

    def test_nested_includes(self, tmp_path, scanner):
        """Test nested include() calls."""
        code = """
from django.urls import path, include

urlpatterns = [
    path('api/', include([
        path('v1/', include('myapp.v1.urls')),
        path('v2/', include('myapp.v2.urls')),
    ])),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # Should detect the outer include
        assert output.summary.total_patterns >= 1

    def test_conditional_urlpatterns(self, tmp_path, scanner):
        """Test conditional URL patterns."""
        code = """
from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list),
]

if DEBUG:
    urlpatterns += [
        path('debug/', views.debug_view),
    ]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # Should detect the initial urlpatterns assignment
        # The conditional addition is not detected as it's not in the initial assignment
        assert output.summary.total_patterns >= 1

    def test_empty_urlpatterns(self, tmp_path, scanner):
        """Test empty urlpatterns list."""
        code = """
from django.urls import path

urlpatterns = []
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_patterns == 0

    def test_urlpatterns_with_comments(self, tmp_path, scanner):
        """Test urlpatterns with comments."""
        code = """
from django.urls import path
from . import views

urlpatterns = [
    # Main article URLs
    path('articles/', views.article_list, name='article-list'),
    # path('drafts/', views.draft_list),  # Commented out
    path('articles/<int:pk>/', views.article_detail, name='article-detail'),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # Should only detect the 2 uncommented patterns
        assert output.summary.total_patterns == 2

    def test_pattern_with_no_name(self, tmp_path, scanner):
        """Test URL pattern without name parameter."""
        code = """
from django.urls import path
from . import views

urlpatterns = [
    path('no-name/', views.some_view),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        module_name = list(output.results.keys())[0]
        pattern = output.results[module_name].urlpatterns[0]

        assert pattern.name is None
        assert pattern.pattern == "no-name/"

    def test_complex_view_resolution(self, tmp_path, scanner):
        """Test complex view references (Class-based views)."""
        code = """
from django.urls import path
from .views import ArticleListView

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article-list'),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_patterns == 1

        module_name = list(output.results.keys())[0]
        pattern = output.results[module_name].urlpatterns[0]

        # Should detect the pattern even with .as_view() call
        assert pattern.pattern == "articles/"

    def test_invalid_pattern_syntax(self, tmp_path, scanner):
        """Test handling of invalid Python syntax."""
        code = """
from django.urls import path
from . import views

urlpatterns = [
    path('valid/', views.valid_view),
"""  # Intentionally missing closing bracket
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        # Scanner should handle parse errors gracefully
        output = scanner.scan(file_path)

        # Should return empty results without crashing
        assert output.summary.total_patterns == 0
