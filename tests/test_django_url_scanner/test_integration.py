"""Tests for Django URL scanner checker."""

from pathlib import Path

import pytest

from upcast.django_url_scanner.cli import scan_django_urls


class TestUrlPatternChecker:
    """Integration tests for URL pattern detection."""

    @pytest.fixture
    def fixtures_dir(self):
        """Get the fixtures directory."""
        return Path(__file__).parent / "fixtures"

    def test_scan_simple_urls(self, fixtures_dir):
        """Test scanning simple URL patterns."""
        result = scan_django_urls(str(fixtures_dir / "simple_urls.py"), verbose=False)

        assert result
        assert "simple_urls" in result or "fixtures.simple_urls" in result

        # Parse YAML to verify structure
        import yaml

        data = yaml.safe_load(result)

        # Find the module (could be simple_urls or fixtures.simple_urls)
        module_data = None
        for key in data:
            if "simple_urls" in key:
                module_data = data[key]
                break

        assert module_data is not None
        assert "urlpatterns" in module_data
        patterns = module_data["urlpatterns"]

        assert len(patterns) >= 2

        # Check for index pattern
        index_pattern = next((p for p in patterns if p.get("name") == "index"), None)
        assert index_pattern is not None
        assert index_pattern["type"] == "path"
        assert index_pattern["pattern"] == "<root>"

        # Check for detail pattern
        detail_pattern = next((p for p in patterns if p.get("name") == "detail"), None)
        assert detail_pattern is not None
        assert detail_pattern["type"] == "path"
        assert detail_pattern["pattern"] == "detail/<int:id>/"
        assert detail_pattern.get("converters") == {"id": "int"}

    def test_scan_complex_urls(self, fixtures_dir):
        """Test scanning complex URL patterns."""
        result = scan_django_urls(str(fixtures_dir / "complex_urls.py"), verbose=False)

        assert result

        import yaml

        data = yaml.safe_load(result)

        # Find the module
        module_data = None
        for key in data:
            if "complex_urls" in key:
                module_data = data[key]
                break

        assert module_data is not None
        patterns = module_data["urlpatterns"]

        # Should have multiple patterns
        assert len(patterns) >= 5

        # Check for various pattern types
        pattern_names = [p.get("name") for p in patterns]
        assert "post-list" in pattern_names
        assert "post-detail" in pattern_names
        assert "archive" in pattern_names
        assert "edit" in pattern_names

        # Check converter parsing
        detail = next((p for p in patterns if p.get("name") == "post-detail"), None)
        assert detail is not None
        assert detail["type"] == "path"
        assert detail.get("converters") == {"id": "int"}

        # Check regex pattern
        archive = next((p for p in patterns if p.get("name") == "archive"), None)
        assert archive is not None
        assert archive["type"] == "re_path"
        assert "named_groups" in archive or "year" in str(archive)

        # Check include pattern
        include_pattern = next((p for p in patterns if p.get("include_module")), None)
        assert include_pattern is not None
        assert include_pattern["type"] == "include"
        assert include_pattern["pattern"] == "api/"
        assert include_pattern["include_module"] == "app.api.urls"

    def test_scan_dynamic_urls(self, fixtures_dir):
        """Test scanning dynamically generated URL patterns."""
        result = scan_django_urls(str(fixtures_dir / "dynamic_urls.py"), verbose=False)

        assert result

        import yaml

        data = yaml.safe_load(result)

        # Find the module
        module_data = None
        for key in data:
            if "dynamic_urls" in key:
                module_data = data[key]
                break

        assert module_data is not None
        patterns = module_data["urlpatterns"]

        # Should detect dynamic pattern
        assert len(patterns) >= 1

        # Check for dynamic type
        has_dynamic = any(p.get("type") == "dynamic" for p in patterns)
        assert has_dynamic

    def test_scan_directory(self, fixtures_dir):
        """Test scanning entire directory."""
        result = scan_django_urls(str(fixtures_dir), verbose=False)

        assert result

        import yaml

        data = yaml.safe_load(result)

        # Should find multiple modules
        assert len(data) >= 2

    def test_output_yaml_format(self, fixtures_dir, tmp_path):
        """Test YAML output format."""
        output_file = tmp_path / "urls.yaml"
        scan_django_urls(str(fixtures_dir / "simple_urls.py"), output=str(output_file), verbose=False)

        assert output_file.exists()

        import yaml

        with open(output_file) as f:
            data = yaml.safe_load(f)

        assert isinstance(data, dict)
        # Should have module path as key
        assert len(data) >= 1
