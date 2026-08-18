"""Tests for merging Django URL and view scan output."""

import csv

import yaml

from upcast.reporting.django_report import build_django_report


def _write_scan_inputs(tmp_path, pattern="health/"):
    views_file = tmp_path / "app" / "views.py"
    urls_file = tmp_path / "app" / "urls.py"
    views_file.parent.mkdir()
    views_file.write_text(
        """
from rest_framework.decorators import api_view

@api_view(["GET"])
def health(request):
    return None
"""
    )
    urls_file.write_text(
        """
from django.urls import path
from .views import health

urlpatterns = [path("other/", health), path("health/", health, name="health")]
"""
    )
    urls_yaml = tmp_path / "urls.yaml"
    views_yaml = tmp_path / "views.yaml"
    urls_yaml.write_text(
        yaml.safe_dump(
            {
                "results": {
                    "app.urls": {
                        "urlpatterns": [
                            {
                                "type": "path",
                                "pattern": pattern,
                                "full_path": pattern,
                                "view_module": None,
                                "view_name": "health",
                                "name": "health",
                                "file": "app/urls.py",
                                "line": 5,
                            }
                        ]
                    }
                }
            }
        )
    )
    views_yaml.write_text(
        yaml.safe_dump(
            {
                "results": {
                    "app.views": [
                        {
                            "module": "app.views",
                            "name": "health",
                            "qualname": "app.views.health",
                            "kind": "function",
                            "status": "confirmed",
                            "identified_by": ["drf_api_view_decorator"],
                            "route_linkage": [
                                {
                                    "type": "path",
                                    "url_module": "app.urls",
                                    "pattern": pattern,
                                    "full_path": pattern,
                                    "name": "health",
                                    "file": "app/urls.py",
                                    "line": 5,
                                }
                            ],
                            "bases": [],
                            "decorators": ["api_view([\"GET\"])"],
                            "http_methods": ["GET"],
                            "actions": [],
                            "permission_classes": [],
                            "authentication_classes": [],
                            "login_exempt": None,
                            "csrf_exempt": None,
                            "model_references": [],
                            "serializer_class": None,
                            "file": "app/views.py",
                            "line": 5,
                        }
                    ]
                }
            }
        )
    )
    return urls_yaml, views_yaml


def test_build_django_report_merges_and_verifies_source(tmp_path):
    urls_yaml, views_yaml = _write_scan_inputs(tmp_path)
    csv_path = tmp_path / "report.csv"
    verification_path = tmp_path / "verification.yaml"

    summary = build_django_report(tmp_path, urls_yaml, views_yaml, csv_path, verification_path)

    assert summary["rows"] == 1
    assert summary["mismatches"] == 0
    with csv_path.open(newline="") as f:
        row = next(csv.DictReader(f))
    assert row["record_type"] == "url"
    assert row["view_match_status"] == "matched_source_location"
    assert row["url_source_status"] == "verified"
    assert row["view_source_status"] == "verified"
    verification = yaml.safe_load(verification_path.read_text())
    assert verification["summary"]["mismatches"] == 0


def test_build_django_report_marks_source_mismatch(tmp_path):
    urls_yaml, views_yaml = _write_scan_inputs(tmp_path, pattern="wrong/")
    csv_path = tmp_path / "report.csv"
    verification_path = tmp_path / "verification.yaml"

    summary = build_django_report(tmp_path, urls_yaml, views_yaml, csv_path, verification_path)

    assert summary["mismatches"] == 1
    with csv_path.open(newline="") as f:
        row = next(csv.DictReader(f))
    assert row["url_source_status"] == "mismatch"


def test_build_django_report_verifies_instance_method_view(tmp_path):
    handlers_file = tmp_path / "app" / "handlers.py"
    urls_file = tmp_path / "app" / "urls.py"
    handlers_file.parent.mkdir()
    handlers_file.write_text(
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
    urls_yaml = tmp_path / "urls.yaml"
    views_yaml = tmp_path / "views.yaml"
    urls_yaml.write_text(
        yaml.safe_dump(
            {
                "results": {
                    "app.urls": {
                        "urlpatterns": [
                            {
                                "type": "path",
                                "pattern": "health/",
                                "full_path": "health/",
                                "view_module": None,
                                "view_name": "health",
                                "file": "app/urls.py",
                                "line": 5,
                            }
                        ]
                    }
                }
            }
        )
    )
    views_yaml.write_text(
        yaml.safe_dump(
            {
                "results": {
                    "app.handlers": [
                        {
                            "module": "app.handlers",
                            "name": "health",
                            "qualname": "app.handlers.HealthHandler.health",
                            "kind": "method",
                            "status": "confirmed",
                            "identified_by": ["route_reference"],
                            "route_linkage": [
                                {
                                    "type": "path",
                                    "url_module": "app.urls",
                                    "pattern": "health/",
                                    "full_path": "health/",
                                    "file": "app/urls.py",
                                    "line": 5,
                                }
                            ],
                            "decorators": [],
                            "http_methods": [],
                            "actions": [],
                            "permission_classes": [],
                            "authentication_classes": [],
                            "login_exempt": None,
                            "csrf_exempt": None,
                            "model_references": [],
                            "serializer_class": None,
                            "file": "app/handlers.py",
                            "line": 3,
                        }
                    ]
                }
            }
        )
    )

    summary = build_django_report(
        tmp_path,
        urls_yaml,
        views_yaml,
        tmp_path / "report.csv",
        tmp_path / "verification.yaml",
    )

    assert summary["mismatches"] == 0
    with (tmp_path / "report.csv").open(newline="") as report_file:
        row = next(csv.DictReader(report_file))
    assert row["view_qualname"] == "app.handlers.HealthHandler.health"


def test_build_django_report_detects_router_metadata_mismatch(tmp_path):
    urls_file = tmp_path / "app" / "urls.py"
    urls_file.parent.mkdir()
    urls_file.write_text(
        """
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter(trailing_slash=False)
router.register("users", UserViewSet, basename="user")
urlpatterns = []
urlpatterns += router.urls
"""
    )
    urls_yaml = tmp_path / "urls.yaml"
    urls_yaml.write_text(
        yaml.safe_dump(
            {
                "results": {
                    "app.urls": {
                        "urlpatterns": [
                            {
                                "type": "router_registration",
                                "pattern": "wrong",
                                "full_path": "wrong",
                                "view_module": "app.views",
                                "view_name": "UserViewSet",
                                "basename": "wrong",
                                "router_type": "SimpleRouter",
                                "file": "app/urls.py",
                                "line": 6,
                            }
                        ]
                    }
                }
            }
        )
    )
    views_yaml = tmp_path / "views.yaml"
    views_yaml.write_text(yaml.safe_dump({"results": {}}))

    summary = build_django_report(
        tmp_path,
        urls_yaml,
        views_yaml,
        tmp_path / "report.csv",
        tmp_path / "verification.yaml",
    )

    assert summary["mismatches"] == 1


def test_build_django_report_verifies_callable_factory_routes(tmp_path):
    urls_file = tmp_path / "urls.py"
    urls_file.write_text(
        """
from django.urls import path

def schema_view(**kwargs):
    return None

urlpatterns = [
    path("doc/", schema_view(cache_timeout=0)),
    path("ui/", schema_view.with_ui("swagger", cache_timeout=0)),
]
"""
    )
    urls_yaml = tmp_path / "urls.yaml"
    urls_yaml.write_text(
        yaml.safe_dump(
            {
                "results": {
                    "urls": {
                        "urlpatterns": [
                            {
                                "type": "path",
                                "pattern": "doc/",
                                "view_name": "schema_view",
                                "file": "urls.py",
                                "line": 8,
                            },
                            {
                                "type": "path",
                                "pattern": "ui/",
                                "view_name": "with_ui",
                                "file": "urls.py",
                                "line": 9,
                            },
                        ]
                    }
                }
            }
        )
    )
    views_yaml = tmp_path / "views.yaml"
    views_yaml.write_text(yaml.safe_dump({"results": {}}))

    summary = build_django_report(
        tmp_path,
        urls_yaml,
        views_yaml,
        tmp_path / "report.csv",
        tmp_path / "verification.yaml",
    )

    assert summary["mismatches"] == 0


def test_build_django_report_matches_modules_with_source_root_prefix(tmp_path):
    urls_file = tmp_path / "workspace" / "sample_app" / "core" / "api" / "v2.py"
    views_file = tmp_path / "workspace" / "sample_app" / "core" / "views.py"
    urls_file.parent.mkdir(parents=True)
    views_file.parent.mkdir(parents=True, exist_ok=True)
    urls_file.write_text(
        """
from rest_framework.routers import DefaultRouter
from sample_app.core.views import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
urlpatterns = router.urls
"""
    )
    views_file.write_text(
        """
from rest_framework.viewsets import ModelViewSet


class UserViewSet(ModelViewSet):
    pass
"""
    )
    urls_yaml = tmp_path / "urls.yaml"
    urls_yaml.write_text(
        yaml.safe_dump(
            {
                "results": {
                    "workspace.sample_app.core.api.v2": {
                        "urlpatterns": [
                            {
                                "type": "router_registration",
                                "pattern": "users",
                                "view_module": "sample_app.core.views",
                                "view_name": "UserViewSet",
                                "basename": "user",
                                "router_type": "DefaultRouter",
                                "file": "workspace/sample_app/core/api/v2.py",
                                "line": 6,
                            }
                        ]
                    }
                }
            }
        )
    )
    views_yaml = tmp_path / "views.yaml"
    views_yaml.write_text(
        yaml.safe_dump(
            {
                "results": {
                    "workspace.sample_app.core.views": [
                        {
                            "module": "workspace.sample_app.core.views",
                            "name": "UserViewSet",
                            "qualname": "workspace.sample_app.core.views.UserViewSet",
                            "kind": "class",
                            "status": "confirmed",
                            "identified_by": ["drf_view_base"],
                            "route_linkage": [],
                            "bases": ["ModelViewSet"],
                            "decorators": [],
                            "http_methods": [],
                            "actions": [],
                            "permission_classes": [],
                            "authentication_classes": [],
                            "login_exempt": None,
                            "csrf_exempt": None,
                            "model_references": [],
                            "serializer_class": None,
                            "file": "workspace/sample_app/core/views.py",
                            "line": 5,
                        }
                    ]
                }
            }
        )
    )

    summary = build_django_report(
        tmp_path,
        urls_yaml,
        views_yaml,
        tmp_path / "report.csv",
        tmp_path / "verification.yaml",
    )

    assert summary["mismatches"] == 0
    assert summary["unresolved"] == 0
    with (tmp_path / "report.csv").open(newline="") as report_file:
        row = next(csv.DictReader(report_file))
    assert row["view_match_status"] == "matched_exact"
    assert row["view_qualname"] == "workspace.sample_app.core.views.UserViewSet"


def test_build_django_report_verifies_generic_module_urls_include(tmp_path):
    urls_file = tmp_path / "urls.py"
    urls_file.write_text(
        """
from django.urls import include, path
import debug_toolbar

urlpatterns = [path("__debug__/", include(debug_toolbar.urls))]
"""
    )
    urls_yaml = tmp_path / "urls.yaml"
    urls_yaml.write_text(
        yaml.safe_dump(
            {
                "results": {
                    "urls": {
                        "urlpatterns": [
                            {
                                "type": "include",
                                "pattern": "__debug__/",
                                "full_path": "__debug__/",
                                "include_module": "debug_toolbar.urls",
                                "file": "urls.py",
                                "line": 5,
                            }
                        ]
                    }
                }
            }
        )
    )
    views_yaml = tmp_path / "views.yaml"
    views_yaml.write_text(yaml.safe_dump({"results": {}}))

    summary = build_django_report(
        tmp_path,
        urls_yaml,
        views_yaml,
        tmp_path / "report.csv",
        tmp_path / "verification.yaml",
    )

    assert summary["mismatches"] == 0
    assert summary["unresolved"] == 0
