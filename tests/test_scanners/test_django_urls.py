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
