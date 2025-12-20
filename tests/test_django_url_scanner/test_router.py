"""Tests for DRF router parsing."""

import yaml

from upcast.django_url_scanner.cli import scan_django_urls


class TestDrfRouterParsing:
    """Test DRF router URL parsing."""

    def test_parse_router_registrations(self, tmp_path):
        """Test parsing router.register() calls."""
        fixture_path = "tests/test_django_url_scanner/fixtures/drf_router_urls.py"

        yaml_output = scan_django_urls(fixture_path)
        result = yaml.safe_load(yaml_output)

        # Should have one module
        assert len(result) == 1
        module_name = next(iter(result.keys()))
        patterns = result[module_name]["urlpatterns"]

        # Find router registrations
        router_patterns = [p for p in patterns if p.get("type") == "router_registration"]

        # Should have expanded router registrations
        assert len(router_patterns) >= 2, f"Expected at least 2 router registrations, got {len(router_patterns)}"

        # Check user registration
        user_pattern = next((p for p in router_patterns if p.get("basename") == "user"), None)
        assert user_pattern is not None, "User registration not found"
        assert user_pattern["pattern"] == "api/users"
        assert user_pattern["viewset_name"] == "UserViewSet"
        assert user_pattern["basename"] == "user"
        assert user_pattern["router_type"] == "DefaultRouter"

        # Check post registration (no explicit basename)
        post_pattern = next((p for p in router_patterns if p.get("viewset_name") == "PostViewSet"), None)
        assert post_pattern is not None, "Post registration not found"
        assert post_pattern["pattern"] == "api/posts"
        assert post_pattern["viewset_name"] == "PostViewSet"
        assert post_pattern["router_type"] == "DefaultRouter"

        # Check simple router registration
        product_pattern = next(
            (p for p in router_patterns if p.get("viewset_name") == "UserViewSet" and "simple" in p.get("pattern", "")),
            None,
        )
        assert product_pattern is not None, "Product registration not found"
        assert product_pattern["pattern"] == "simple/products"
        assert product_pattern["router_type"] == "SimpleRouter"

    def test_router_without_registrations(self, tmp_path):
        """Test handling of router without any registrations."""
        # Create a test file with empty router
        test_file = tmp_path / "empty_router.py"
        test_file.write_text(
            """
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path("api/", include(router.urls)),
]
"""
        )

        yaml_output = scan_django_urls(str(test_file))
        result = yaml.safe_load(yaml_output)

        # Should still have the module
        assert len(result) == 1
        patterns = next(iter(result.values()))["urlpatterns"]

        # Should fall back to include since no registrations found
        include_pattern = next((p for p in patterns if p.get("type") == "include"), None)
        assert include_pattern is not None
        assert "<router:" in include_pattern.get("include_module", "")
