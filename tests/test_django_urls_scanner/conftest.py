"""Pytest fixtures for Django URL scanner tests."""

import pytest
from pathlib import Path

from upcast.scanners.django_urls import DjangoUrlScanner


@pytest.fixture
def scanner():
    """Create a DjangoUrlScanner instance."""
    return DjangoUrlScanner(verbose=False)


@pytest.fixture
def fixtures_dir():
    """Get the fixtures directory path."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def path_fixtures():
    """Path pattern fixtures as dict."""
    return {
        "SIMPLE_PATH": """
from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list, name='article-list'),
]
""",
        "PATH_WITH_CONVERTERS": """
from django.urls import path
from . import views

urlpatterns = [
    path('articles/<int:pk>/', views.article_detail, name='article-detail'),
    path('posts/<slug:slug>/', views.post_detail, name='post-detail'),
]
""",
    }


@pytest.fixture
def re_path_fixtures():
    """re_path pattern fixtures as dict."""
    return {
        "SIMPLE_RE_PATH": """
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^articles/$', views.article_list, name='article-list'),
]
""",
        "RE_PATH_WITH_GROUPS": """
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive, name='year-archive'),
]
""",
    }


@pytest.fixture
def include_fixtures():
    """Include pattern fixtures as dict."""
    return {
        "SIMPLE_INCLUDE": """
from django.urls import path, include

urlpatterns = [
    path('api/', include('myapp.api.urls')),
]
""",
        "INCLUDE_WITH_NAMESPACE": """
from django.urls import path, include

urlpatterns = [
    path('api/', include(('myapp.api.urls', 'api'), namespace='api-v1')),
]
""",
    }


@pytest.fixture
def router_fixtures():
    """DRF router fixtures as dict."""
    return {
        "DEFAULT_ROUTER": """
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')

urlpatterns = router.urls
""",
        "SIMPLE_ROUTER": """
from rest_framework.routers import SimpleRouter
from .views import PostViewSet

router = SimpleRouter()
router.register(r'posts', PostViewSet)

urlpatterns = router.urls
""",
    }
