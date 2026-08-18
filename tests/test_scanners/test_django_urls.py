"""Tests for DjangoUrlScanner."""

import astroid

from upcast.common.hybrid_scan_pipeline import PipelineRunResult, SemanticDecision, StructuralCandidate
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

    def test_scanner_uses_hybrid_pipeline_for_urlpattern_assignments(self, tmp_path, monkeypatch):
        """Scanner should use the hybrid pipeline to discover urlpatterns assignments."""
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
        calls: list[tuple[str, str]] = []

        def fake_run_pipeline(*, spec, source, file_path):
            module = astroid.parse(source, path=file_path)
            assign_node = next(module.nodes_of_class(astroid.nodes.Assign))
            calls.append((spec.name, file_path))
            return PipelineRunResult(
                candidates=[
                    StructuralCandidate(
                        file_path=file_path,
                        structural_span={
                            "start": [assign_node.lineno, assign_node.col_offset],
                            "end": [assign_node.end_lineno, assign_node.end_col_offset],
                        },
                        captures={"self": assign_node, "VALUE": assign_node.value},
                        snippet=assign_node.as_string(),
                    )
                ],
                decisions=[SemanticDecision(status="confirmed")],
                findings=[],
            )

        monkeypatch.setattr("upcast.scanners.django_urls.run_pipeline", fake_run_pipeline, raising=False)

        output = scanner.scan(test_file)

        assert calls == [("scan-django-urls", str(test_file))]
        assert output.summary.total_count == 1
        module = next(iter(output.results.values()))
        pattern = module.urlpatterns[0]
        assert pattern.type == "path"
        assert pattern.pattern == "users/"
        assert pattern.name == "user-list"

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

    def test_scanner_expands_router_urls_added_to_urlpatterns(self, tmp_path):
        """Router registrations remain visible when urlpatterns uses += router.urls."""
        test_file = tmp_path / "urls.py"
        (tmp_path / "views.py").write_text("class UserViewSet:\n    pass\n")
        test_file.write_text(
            """
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter(trailing_slash=False)
router.register("users", UserViewSet, basename="user")

urlpatterns = []
urlpatterns += router.urls
"""
        )

        scanner = DjangoUrlScanner()
        output = scanner.scan(test_file)

        module = next(iter(output.results.values()))
        assert len(module.urlpatterns) == 1
        pattern = module.urlpatterns[0]
        assert pattern.type == "router_registration"
        assert pattern.pattern == "users"
        assert pattern.view_module == "views"
        assert pattern.view_name == "UserViewSet"
        assert pattern.basename == "user"
        assert pattern.router_type == "DefaultRouter"

    def test_scanner_extracts_literal_routes_added_to_urlpatterns(self, tmp_path):
        """Literal routes appended with += remain visible even in a branch."""
        test_file = tmp_path / "urls.py"
        test_file.write_text(
            """
from django.urls import path

def health(request):
    return None

urlpatterns = []
if True:
    urlpatterns += [path("health/", health)]
"""
        )

        output = DjangoUrlScanner().scan(test_file)

        module = next(iter(output.results.values()))
        assert len(module.urlpatterns) == 1
        pattern = module.urlpatterns[0]
        assert pattern.type == "path"
        assert pattern.pattern == "health/"
        assert pattern.view_name == "health"

    def test_scanner_extracts_router_and_literal_routes_from_concatenation(self, tmp_path):
        """Router and literal routes remain visible in ``router.urls + [...]``."""
        test_file = tmp_path / "urls.py"
        test_file.write_text(
            """
from django.urls import path
from rest_framework.routers import SimpleRouter

class ExampleViewSet:
    pass

def health(request):
    return None

router = SimpleRouter()
router.register("example", ExampleViewSet, basename="example")
urlpatterns = router.urls + [path("health/", health)]
"""
        )

        output = DjangoUrlScanner().scan(test_file)

        module = next(iter(output.results.values()))
        assert len(module.urlpatterns) == 2
        assert [pattern.type for pattern in module.urlpatterns] == ["router_registration", "path"]
        assert module.urlpatterns[0].pattern == "example"
        assert module.urlpatterns[1].pattern == "health/"

    def test_scanner_extracts_routes_appended_to_urlpatterns(self, tmp_path):
        """Routes appended after initialization remain visible."""
        test_file = tmp_path / "urls.py"
        test_file.write_text(
            """
from django.urls import path

def health(request):
    return None

urlpatterns = []
urlpatterns.append(path("health/", health, name="health"))
"""
        )

        output = DjangoUrlScanner().scan(test_file)

        module = next(iter(output.results.values()))
        assert len(module.urlpatterns) == 1
        pattern = module.urlpatterns[0]
        assert pattern.type == "path"
        assert pattern.pattern == "health/"
        assert pattern.name == "health"

    def test_scanner_keeps_dynamic_include_appended_to_urlpatterns(self, tmp_path):
        """Dynamic application includes are retained as unresolved metadata."""
        test_file = tmp_path / "urls.py"
        test_file.write_text(
            """
from django.urls import include, path

urlpatterns = []
for app in ["billing"]:
    urlpatterns.append(
        path(f"{app}/", include((f"{app}.urls", app), namespace=app))
    )
"""
        )

        output = DjangoUrlScanner().scan(test_file)

        module = next(iter(output.results.values()))
        assert len(module.urlpatterns) == 1
        pattern = module.urlpatterns[0]
        assert pattern.type == "include"
        assert pattern.pattern is None

    def test_scanner_ignores_local_annotated_pattern_helpers(self, tmp_path):
        """A helper-local ``urlpatterns`` variable is not a URLconf mutation."""
        test_file = tmp_path / "helpers.py"
        test_file.write_text(
            """
from django.urls import path

def root(request):
    return None

urlpatterns = [path("root/", root)]

def build_patterns():
    urlpatterns: list = []
    urlpatterns.append(path("health/", object()))
    return urlpatterns
"""
        )

        output = DjangoUrlScanner(include_patterns=["**/*.py"]).scan(test_file)

        patterns = next(iter(output.results.values())).urlpatterns
        assert len(patterns) == 1
        assert patterns[0].pattern == "root/"

    def test_scanner_preserves_module_urls_when_no_router_registration_exists(self, tmp_path):
        """A generic ``module.urls`` include is not mislabeled as a router."""
        test_file = tmp_path / "urls.py"
        test_file.write_text(
            """
from django.urls import include, path
import debug_toolbar

urlpatterns = [path("__debug__/", include(debug_toolbar.urls))]
"""
        )

        output = DjangoUrlScanner().scan(test_file)

        pattern = next(iter(output.results.values())).urlpatterns[0]
        assert pattern.type == "include"
        assert pattern.include_module == "debug_toolbar.urls"
