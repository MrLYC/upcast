"""Tests for URL pattern converters."""

import pytest
from pathlib import Path

from upcast.scanners.django_urls import DjangoUrlScanner


class TestConverters:
    """Test URL pattern converter detection."""

    def test_int_converter(self, tmp_path, scanner):
        """Test detection of <int:name> converter."""
        code = """
from django.urls import path
from . import views

urlpatterns = [
    path('articles/<int:pk>/', views.article_detail, name='article-detail'),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        module_name = list(output.results.keys())[0]
        pattern = output.results[module_name].urlpatterns[0]

        assert pattern.pattern == "articles/<int:pk>/"
        assert "pk:int" in pattern.converters
        assert len(pattern.converters) == 1

    def test_slug_converter(self, tmp_path, scanner):
        """Test detection of <slug:name> converter."""
        code = """
from django.urls import path
from . import views

urlpatterns = [
    path('posts/<slug:slug>/', views.post_detail, name='post-detail'),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        module_name = list(output.results.keys())[0]
        pattern = output.results[module_name].urlpatterns[0]

        assert pattern.pattern == "posts/<slug:slug>/"
        assert "slug:slug" in pattern.converters
        assert len(pattern.converters) == 1

    def test_str_converter(self, tmp_path, scanner):
        """Test detection of <str:name> converter."""
        code = """
from django.urls import path
from . import views

urlpatterns = [
    path('users/<str:username>/', views.user_profile, name='user-profile'),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        module_name = list(output.results.keys())[0]
        pattern = output.results[module_name].urlpatterns[0]

        assert pattern.pattern == "users/<str:username>/"
        assert "username:str" in pattern.converters

    def test_uuid_converter(self, tmp_path, scanner):
        """Test detection of <uuid:name> converter."""
        code = """
from django.urls import path
from . import views

urlpatterns = [
    path('objects/<uuid:id>/', views.object_detail, name='object-detail'),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        module_name = list(output.results.keys())[0]
        pattern = output.results[module_name].urlpatterns[0]

        assert pattern.pattern == "objects/<uuid:id>/"
        assert "id:uuid" in pattern.converters

    def test_multiple_converters_in_pattern(self, tmp_path, scanner):
        """Test detection of multiple converters in a single pattern."""
        code = """
from django.urls import path
from . import views

urlpatterns = [
    path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail, name='article-detail'),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        module_name = list(output.results.keys())[0]
        pattern = output.results[module_name].urlpatterns[0]

        assert pattern.pattern == "articles/<int:year>/<int:month>/<slug:slug>/"
        assert len(pattern.converters) == 3
        assert "year:int" in pattern.converters
        assert "month:int" in pattern.converters
        assert "slug:slug" in pattern.converters

    def test_re_path_named_groups(self, tmp_path, scanner):
        """Test detection of named groups in re_path patterns."""
        code = """
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive, name='month-archive'),
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        module_name = list(output.results.keys())[0]
        pattern = output.results[module_name].urlpatterns[0]

        assert pattern.type == "re_path"
        assert len(pattern.named_groups) == 2
        assert "year" in pattern.named_groups
        assert "month" in pattern.named_groups
        # re_path patterns don't use converters
        assert len(pattern.converters) == 0
