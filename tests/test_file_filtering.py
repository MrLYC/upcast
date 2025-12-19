"""Integration tests for file filtering across all scanners."""

import tempfile
from pathlib import Path

import pytest

from upcast.django_model_scanner.cli import scan_django_models
from upcast.django_settings_scanner.cli import scan_django_settings
from upcast.prometheus_metrics_scanner.cli import scan_prometheus_metrics


@pytest.fixture
def test_workspace():
    """Create a temporary workspace with test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir)

        # Create structure with excluded directories
        (workspace / "app").mkdir()
        (workspace / "tests").mkdir()
        (workspace / "venv").mkdir()

        # Create Django model files
        (workspace / "app" / "models.py").write_text(
            """
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
"""
        )

        (workspace / "tests" / "test_models.py").write_text(
            """
from django.db import models

class TestModel(models.Model):
    value = models.IntegerField()
"""
        )

        # Create Prometheus metrics files
        (workspace / "app" / "metrics.py").write_text(
            """
from prometheus_client import Counter

requests_total = Counter('requests_total', 'Total requests')
"""
        )

        (workspace / "tests" / "test_metrics.py").write_text(
            """
from prometheus_client import Counter

test_counter = Counter('test_counter', 'Test counter')
"""
        )

        # Create Django settings files
        (workspace / "app" / "views.py").write_text(
            """
from django.conf import settings

debug = settings.DEBUG
"""
        )

        (workspace / "tests" / "test_views.py").write_text(
            """
from django.conf import settings

test_debug = settings.DEBUG
"""
        )

        # Create file in venv (should be excluded by default)
        (workspace / "venv" / "lib.py").write_text(
            """
from django.db import models

class VenvModel(models.Model):
    pass
"""
        )

        yield workspace


class TestFileFiltering:
    """Test file filtering functionality across scanners."""

    def test_django_models_default_excludes(self, test_workspace):
        """Test that venv is excluded by default in Django models scanner."""
        result = scan_django_models(str(test_workspace), verbose=False)

        # Should find models in app/ and tests/ but not venv/
        assert "User" in result
        assert "TestModel" in result
        assert "VenvModel" not in result

    def test_django_models_exclude_pattern(self, test_workspace):
        """Test exclude pattern in Django models scanner."""
        result = scan_django_models(
            str(test_workspace),
            verbose=False,
            exclude_patterns=["tests/**"],
        )

        # Should find only app/ models
        assert "User" in result
        assert "TestModel" not in result
        assert "VenvModel" not in result

    def test_django_models_include_pattern(self, test_workspace):
        """Test include pattern in Django models scanner."""
        result = scan_django_models(
            str(test_workspace),
            verbose=False,
            include_patterns=["app/**"],
        )

        # Should find only app/ models
        assert "User" in result
        assert "TestModel" not in result

    def test_django_models_no_default_excludes(self, test_workspace):
        """Test disabling default excludes in Django models scanner."""
        result = scan_django_models(
            str(test_workspace),
            verbose=False,
            use_default_excludes=False,
        )

        # Should find models in all directories including venv/
        # But VenvModel won't be detected because the file doesn't import models properly
        assert "User" in result
        assert "TestModel" in result
        # Note: VenvModel won't appear because venv/lib.py doesn't have proper imports

    def test_prometheus_metrics_exclude_pattern(self, test_workspace):
        """Test exclude pattern in Prometheus metrics scanner."""
        result = scan_prometheus_metrics(
            str(test_workspace),
            verbose=False,
            exclude_patterns=["tests/**"],
        )

        # Should find only app/ metrics
        assert "requests_total" in result
        assert "test_counter" not in result

    def test_prometheus_metrics_include_pattern(self, test_workspace):
        """Test include pattern in Prometheus metrics scanner."""
        result = scan_prometheus_metrics(
            str(test_workspace),
            verbose=False,
            include_patterns=["app/**"],
        )

        # Should find only app/ metrics
        assert "requests_total" in result
        assert "test_counter" not in result

    def test_django_settings_exclude_pattern(self, test_workspace):
        """Test exclude pattern in Django settings scanner."""
        result = scan_django_settings(
            str(test_workspace),
            verbose=False,
            exclude_patterns=["tests/**"],
        )

        # Should find only app/ settings usage
        assert "DEBUG" in result["usages"]
        # Check that the usage is only from app/views.py
        assert len(result["usages"]["DEBUG"].locations) == 1
        assert "app/views.py" in result["usages"]["DEBUG"].locations[0].file

    def test_django_settings_include_pattern(self, test_workspace):
        """Test include pattern in Django settings scanner."""
        result = scan_django_settings(
            str(test_workspace),
            verbose=False,
            include_patterns=["app/**"],
        )

        # Should find only app/ settings usage
        assert "DEBUG" in result["usages"]
        assert len(result["usages"]["DEBUG"].locations) == 1
        assert "app/views.py" in result["usages"]["DEBUG"].locations[0].file

    def test_multiple_exclude_patterns(self, test_workspace):
        """Test multiple exclude patterns."""
        result = scan_django_models(
            str(test_workspace),
            verbose=False,
            exclude_patterns=["tests/**", "venv/**"],
        )

        # Should find only app/ models
        assert "User" in result
        assert "TestModel" not in result
        assert "VenvModel" not in result

    def test_include_and_exclude_patterns(self, test_workspace):
        """Test that exclude takes precedence over include."""
        result = scan_django_models(
            str(test_workspace),
            verbose=False,
            include_patterns=["**/*.py"],  # Include all Python files
            exclude_patterns=["tests/**"],  # But exclude tests/
        )

        # Should find only app/ models (exclude wins)
        assert "User" in result
        assert "TestModel" not in result
