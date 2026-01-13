"""Integration tests for Django URL scanner."""

import pytest
from pathlib import Path

from upcast.scanners.django_urls import DjangoUrlScanner
from upcast.models.django_urls import DjangoUrlOutput, UrlPattern


class TestScannerInstantiation:
    """Test scanner instantiation and basic functionality."""

    def test_scanner_instantiation(self, scanner):
        """Test that scanner can be instantiated."""
        assert scanner is not None
        assert isinstance(scanner, DjangoUrlScanner)

    def test_scanner_default_include_patterns(self):
        """Test that scanner has default include patterns for urls.py files."""
        scanner = DjangoUrlScanner()
        assert scanner.include_patterns == ["**/urls.py", "urls.py"]

    def test_scanner_custom_include_patterns(self):
        """Test that scanner accepts custom include patterns."""
        scanner = DjangoUrlScanner(include_patterns=["**/api_urls.py"])
        assert scanner.include_patterns == ["**/api_urls.py"]

    def test_scanner_verbose_mode(self):
        """Test that scanner can be instantiated with verbose mode."""
        scanner = DjangoUrlScanner(verbose=True)
        assert scanner.verbose is True


class TestBasicScanning:
    """Test basic scanning functionality."""

    def test_scan_empty_file(self, tmp_path, scanner):
        """Test scanning an empty file."""
        file_path = tmp_path / "urls.py"
        file_path.write_text("")

        output = scanner.scan(file_path)

        assert isinstance(output, DjangoUrlOutput)
        assert output.summary.total_patterns == 0
        assert output.summary.total_modules == 0
        assert len(output.results) == 0

    def test_scan_file_without_urlpatterns(self, tmp_path, scanner):
        """Test scanning a file without urlpatterns."""
        code = """
from django.urls import path

# No urlpatterns defined
def some_function():
    pass
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_patterns == 0
        assert len(output.results) == 0

    def test_scan_simple_path(self, tmp_path, scanner, path_fixtures):
        """Test scanning a file with a simple path()."""
        file_path = tmp_path / "urls.py"
        file_path.write_text(path_fixtures["SIMPLE_PATH"])

        output = scanner.scan(file_path)

        assert output.summary.total_patterns == 1
        assert output.summary.total_modules == 1
        assert len(output.results) == 1

        # Get the first module
        module_name = list(output.results.keys())[0]
        patterns = output.results[module_name].urlpatterns

        assert len(patterns) == 1
        pattern = patterns[0]
        assert pattern.type == "path"
        assert pattern.pattern == "articles/"
        assert pattern.name == "article-list"
        assert pattern.view_name == "article_list"

    def test_scan_path_with_converters(self, tmp_path, scanner, path_fixtures):
        """Test scanning a file with path converters."""
        file_path = tmp_path / "urls.py"
        file_path.write_text(path_fixtures["PATH_WITH_CONVERTERS"])

        output = scanner.scan(file_path)

        assert output.summary.total_patterns == 2

        module_name = list(output.results.keys())[0]
        patterns = output.results[module_name].urlpatterns

        # First pattern: articles/<int:pk>/
        pattern1 = patterns[0]
        assert pattern1.pattern == "articles/<int:pk>/"
        assert "pk:int" in pattern1.converters
        assert pattern1.name == "article-detail"

        # Second pattern: posts/<slug:slug>/
        pattern2 = patterns[1]
        assert pattern2.pattern == "posts/<slug:slug>/"
        assert "slug:slug" in pattern2.converters
        assert pattern2.name == "post-detail"

    def test_scan_re_path(self, tmp_path, scanner, re_path_fixtures):
        """Test scanning a file with re_path()."""
        file_path = tmp_path / "urls.py"
        file_path.write_text(re_path_fixtures["SIMPLE_RE_PATH"])

        output = scanner.scan(file_path)

        assert output.summary.total_patterns == 1

        module_name = list(output.results.keys())[0]
        patterns = output.results[module_name].urlpatterns

        pattern = patterns[0]
        assert pattern.type == "re_path"
        assert pattern.pattern == "^articles/$"
        assert pattern.name == "article-list"

    def test_scan_re_path_with_named_groups(self, tmp_path, scanner, re_path_fixtures):
        """Test scanning re_path with named groups."""
        file_path = tmp_path / "urls.py"
        file_path.write_text(re_path_fixtures["RE_PATH_WITH_GROUPS"])

        output = scanner.scan(file_path)

        assert output.summary.total_patterns == 1

        module_name = list(output.results.keys())[0]
        patterns = output.results[module_name].urlpatterns

        pattern = patterns[0]
        assert pattern.type == "re_path"
        assert "year" in pattern.named_groups
        assert pattern.name == "year-archive"

    def test_scan_include(self, tmp_path, scanner, include_fixtures):
        """Test scanning a file with include()."""
        file_path = tmp_path / "urls.py"
        file_path.write_text(include_fixtures["SIMPLE_INCLUDE"])

        output = scanner.scan(file_path)

        assert output.summary.total_patterns == 1

        module_name = list(output.results.keys())[0]
        patterns = output.results[module_name].urlpatterns

        pattern = patterns[0]
        assert pattern.type == "include"
        assert pattern.pattern == "api/"
        assert pattern.include_module == "myapp.api.urls"

    def test_scan_include_with_namespace(self, tmp_path, scanner, include_fixtures):
        """Test scanning include() with namespace."""
        file_path = tmp_path / "urls.py"
        file_path.write_text(include_fixtures["INCLUDE_WITH_NAMESPACE"])

        output = scanner.scan(file_path)

        assert output.summary.total_patterns == 1

        module_name = list(output.results.keys())[0]
        patterns = output.results[module_name].urlpatterns

        pattern = patterns[0]
        assert pattern.type == "include"
        assert pattern.include_module == "myapp.api.urls"
        assert pattern.namespace == "api-v1"

    def test_scan_directory(self, tmp_path):
        """Test scanning a directory with multiple urls.py files."""
        # Create scanner with custom pattern to match urls*.py
        scanner = DjangoUrlScanner(include_patterns=["**/urls*.py"])

        # Create multiple files
        file1 = tmp_path / "urls1.py"
        file1.write_text("""
from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list),
]
""")

        file2 = tmp_path / "urls2.py"
        file2.write_text("""
from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.post_list),
    path('posts/<int:pk>/', views.post_detail),
]
""")

        output = scanner.scan(tmp_path)

        assert output.summary.total_patterns == 3
        assert output.summary.total_modules == 2

    def test_scan_summary_statistics(self, tmp_path, scanner):
        """Test that summary statistics are calculated correctly."""
        file_path = tmp_path / "urls.py"
        file_path.write_text("""
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('articles/', views.article_list),
    path('articles/<int:pk>/', views.article_detail),
    re_path(r'^posts/$', views.post_list),
]
""")

        output = scanner.scan(file_path)

        assert output.summary.total_patterns == 3
        assert output.summary.total_modules == 1
        assert output.summary.files_scanned == 1
        assert output.summary.scan_duration_ms >= 0

    def test_scan_dynamic_urlpatterns(self, tmp_path, scanner):
        """Test scanning file with dynamically generated urlpatterns."""
        code = """
from django.urls import path
from . import views

urlpatterns = [
    path(f'{prefix}/', views.handler) for prefix in ['a', 'b', 'c']
]
"""
        file_path = tmp_path / "urls.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # Should detect as dynamic
        assert output.summary.total_patterns == 1

        module_name = list(output.results.keys())[0]
        patterns = output.results[module_name].urlpatterns

        pattern = patterns[0]
        assert pattern.type == "dynamic"
        assert pattern.pattern == "<generated>"
        assert pattern.note == "URL patterns generated dynamically"

    def test_scan_module_path_calculation(self, tmp_path, scanner):
        """Test that module paths are calculated correctly."""
        # Create nested directory structure
        app_dir = tmp_path / "myapp"
        app_dir.mkdir()

        file_path = app_dir / "urls.py"
        file_path.write_text("""
from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_view),
]
""")

        output = scanner.scan(tmp_path)

        assert output.summary.total_modules == 1
        module_names = list(output.results.keys())
        assert len(module_names) == 1
        assert "myapp.urls" in module_names[0] or "myapp/urls" in module_names[0]

    def test_scan_duration_measurement(self, tmp_path, scanner):
        """Test that scan duration is measured."""
        file_path = tmp_path / "urls.py"
        file_path.write_text("""
from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_view),
]
""")

        output = scanner.scan(file_path)

        assert output.summary.scan_duration_ms >= 0
        assert isinstance(output.summary.scan_duration_ms, int)
