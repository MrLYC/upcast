"""Integration tests for file filtering across all scanners."""

import tempfile
from pathlib import Path

import pytest

# Import new scanner implementations
from upcast.scanners import DjangoModelScanner, DjangoSettingsScanner, MetricsScanner


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
        scanner = DjangoModelScanner(verbose=False)
        result = scanner.scan(test_workspace)

        # Should find models in app/ but not venv/
        # Note: tests/ may or may not be included depending on file naming patterns
        model_names = [m.name for m in result.results.values()]
        assert "User" in model_names
        assert "VenvModel" not in model_names
        # TestModel might not be found if file is named test_*.py (test files are often excluded)

    def test_django_models_exclude_pattern(self, test_workspace):
        """Test exclude pattern in Django models scanner."""
        scanner = DjangoModelScanner(
            verbose=False,
            exclude_patterns=["tests/**"],
        )
        result = scanner.scan(test_workspace)

        # Should find only app/ models
        model_names = [m.name for m in result.results.values()]
        assert "User" in model_names
        assert "TestModel" not in model_names
        assert "VenvModel" not in model_names

    def test_django_models_include_pattern(self, test_workspace):
        """Test include pattern in Django models scanner."""
        scanner = DjangoModelScanner(
            verbose=False,
            include_patterns=["app/**"],
        )
        result = scanner.scan(test_workspace)

        # Should find only app/ models
        model_names = [m.name for m in result.results.values()]
        assert "User" in model_names
        assert "TestModel" not in model_names

    def test_prometheus_metrics_exclude_pattern(self, test_workspace):
        """Test exclude pattern in Prometheus metrics scanner."""
        scanner = MetricsScanner(
            verbose=False,
            exclude_patterns=["tests/**"],
        )
        result = scanner.scan(test_workspace)

        # Should find only app/ metrics
        metric_names = list(result.results.keys())
        assert "requests_total" in metric_names
        assert "test_counter" not in metric_names

    def test_prometheus_metrics_include_pattern(self, test_workspace):
        """Test include pattern in Prometheus metrics scanner."""
        scanner = MetricsScanner(
            verbose=False,
            include_patterns=["app/**"],
        )
        result = scanner.scan(test_workspace)

        # Should find only app/ metrics
        metric_names = list(result.results.keys())
        assert "requests_total" in metric_names
        assert "test_counter" not in metric_names

    def test_django_settings_exclude_pattern(self, test_workspace):
        """Test exclude pattern in Django settings scanner."""
        scanner = DjangoSettingsScanner(
            scan_mode="usage",
            verbose=False,
        )
        # Manually set exclude patterns
        scanner.exclude_patterns = ["tests/**"]
        result = scanner.scan(test_workspace)

        # Should find only app/ settings usage
        assert "DEBUG" in result.results
        # Check that the usage is only from app/views.py
        assert len(result.results["DEBUG"].locations) == 1
        assert "app/views.py" in result.results["DEBUG"].locations[0].file

    def test_django_settings_include_pattern(self, test_workspace):
        """Test include pattern in Django settings scanner."""
        scanner = DjangoSettingsScanner(
            scan_mode="usage",
            verbose=False,
        )
        # Manually set include patterns
        scanner.include_patterns = ["app/**"]
        result = scanner.scan(test_workspace)

        # Should find only app/ settings usage
        assert "DEBUG" in result.results
        assert len(result.results["DEBUG"].locations) == 1
        assert "app/views.py" in result.results["DEBUG"].locations[0].file

    def test_multiple_exclude_patterns(self, test_workspace):
        """Test multiple exclude patterns."""
        scanner = DjangoModelScanner(
            verbose=False,
            exclude_patterns=["tests/**", "venv/**"],
        )
        result = scanner.scan(test_workspace)

        # Should find only app/ models
        model_names = [m.name for m in result.results.values()]
        assert "User" in model_names
        assert "TestModel" not in model_names
        assert "VenvModel" not in model_names

    def test_include_and_exclude_patterns(self, test_workspace):
        """Test that exclude takes precedence over include."""
        scanner = DjangoModelScanner(
            verbose=False,
            include_patterns=["**/*.py"],  # Include all Python files
            exclude_patterns=["tests/**"],  # But exclude tests/
        )
        result = scanner.scan(test_workspace)

        # Should find only app/ models (exclude wins)
        model_names = [m.name for m in result.results.values()]
        assert "User" in model_names
        assert "TestModel" not in model_names
