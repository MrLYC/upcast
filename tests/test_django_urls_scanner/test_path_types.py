"""Tests for different URL path types (path, re_path, include)."""

import pytest
from pathlib import Path

from upcast.scanners.django_urls import DjangoUrlScanner


class TestPathTypes:
    """Test different URL path types."""

    def test_path_function_detection(self, tmp_path, scanner):
        """Test that path() function is correctly detected."""
        code = """
from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_view, name='test'),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        module_name = list(output.results.keys())[0]
        pattern = output.results[module_name].urlpatterns[0]

        assert pattern.type == "path"
        assert pattern.pattern == "test/"
        assert pattern.view_name == "test_view"
        assert pattern.name == "test"

    def test_re_path_function_detection(self, tmp_path, scanner):
        """Test that re_path() function is correctly detected."""
        code = """
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive, name='year-archive'),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        module_name = list(output.results.keys())[0]
        pattern = output.results[module_name].urlpatterns[0]

        assert pattern.type == "re_path"
        assert pattern.pattern == "^articles/(?P<year>[0-9]{4})/$"
        assert pattern.view_name == "year_archive"
        assert "year" in pattern.named_groups

    def test_url_function_detection(self, tmp_path, scanner):
        """Test that url() function (deprecated) is detected as re_path."""
        code = """
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^test/$', views.test_view, name='test'),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        module_name = list(output.results.keys())[0]
        pattern = output.results[module_name].urlpatterns[0]

        assert pattern.type == "re_path"  # url() is treated as re_path
        assert pattern.pattern == "^test/$"

    def test_include_function_detection(self, tmp_path, scanner):
        """Test that include() function is correctly detected."""
        code = """
from django.urls import path, include

urlpatterns = [
    path('api/', include('myapp.api.urls')),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        module_name = list(output.results.keys())[0]
        pattern = output.results[module_name].urlpatterns[0]

        assert pattern.type == "include"
        assert pattern.pattern == "api/"
        assert pattern.include_module == "myapp.api.urls"
        assert pattern.view_module is None
        assert pattern.view_name is None

    def test_include_with_tuple_format(self, tmp_path, scanner):
        """Test include() with tuple format (module, namespace)."""
        code = """
from django.urls import path, include

urlpatterns = [
    path('api/', include(('myapp.api.urls', 'api'))),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        module_name = list(output.results.keys())[0]
        pattern = output.results[module_name].urlpatterns[0]

        assert pattern.type == "include"
        assert pattern.include_module == "myapp.api.urls"
        assert pattern.namespace == "api"

    def test_mixed_path_types(self, tmp_path, scanner):
        """Test file with mixed path types."""
        code = """
from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('articles/', views.article_list, name='article-list'),
    re_path(r'^posts/(?P<year>[0-9]{4})/$', views.year_archive),
    path('api/', include('myapp.api.urls')),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        module_name = list(output.results.keys())[0]
        patterns = output.results[module_name].urlpatterns

        assert len(patterns) == 3
        assert patterns[0].type == "path"
        assert patterns[1].type == "re_path"
        assert patterns[2].type == "include"
