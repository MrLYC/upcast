"""Tests for URL pattern parsing utilities."""

from upcast.django_url_scanner.url_parser import (
    extract_path_converters,
    extract_regex_named_groups,
    parse_url_pattern,
)


class TestExtractPathConverters:
    """Tests for extract_path_converters function."""

    def test_no_converters(self):
        """Test pattern with no converters."""
        result = extract_path_converters("posts/")
        assert result == {}

    def test_single_converter(self):
        """Test pattern with single converter."""
        result = extract_path_converters("posts/<int:id>/")
        assert result == {"id": "int"}

    def test_multiple_converters(self):
        """Test pattern with multiple converters."""
        result = extract_path_converters("archive/<int:year>/<int:month>/")
        assert result == {"year": "int", "month": "int"}

    def test_default_str_converter(self):
        """Test pattern with implicit str converter."""
        result = extract_path_converters("category/<slug>/")
        assert result == {"slug": "str"}

    def test_custom_converter(self):
        """Test pattern with custom converter type."""
        result = extract_path_converters("year/<year:year>/")
        assert result == {"year": "year"}

    def test_mixed_converters(self):
        """Test pattern with mixed converter types."""
        result = extract_path_converters("post/<int:id>/<slug>/edit/")
        assert result == {"id": "int", "slug": "str"}


class TestExtractRegexNamedGroups:
    """Tests for extract_regex_named_groups function."""

    def test_no_named_groups(self):
        """Test regex pattern with no named groups."""
        result = extract_regex_named_groups(r"^posts/$")
        assert result == []

    def test_single_named_group(self):
        """Test regex pattern with single named group."""
        result = extract_regex_named_groups(r"^post/(?P<id>\d+)/$")
        assert result == ["id"]

    def test_multiple_named_groups(self):
        """Test regex pattern with multiple named groups."""
        result = extract_regex_named_groups(r"^archive/(?P<year>\d{4})/(?P<month>\d{2})/$")
        assert result == ["year", "month"]

    def test_complex_regex(self):
        """Test complex regex pattern."""
        result = extract_regex_named_groups(r"^(?P<category>[a-z]+)/(?P<slug>[\w-]+)/$")
        assert result == ["category", "slug"]


class TestParseUrlPattern:
    """Tests for parse_url_pattern function."""

    def test_path_pattern(self):
        """Test parsing Django path() pattern."""
        result = parse_url_pattern("posts/<int:id>/")
        assert result["is_regex"] is False
        assert result["converters"] == {"id": "int"}
        assert result["named_groups"] == []

    def test_regex_pattern(self):
        """Test parsing regex pattern."""
        result = parse_url_pattern(r"^post/(?P<id>\d+)/$")
        assert result["is_regex"] is True
        assert result["converters"] == {}
        assert result["named_groups"] == ["id"]

    def test_simple_pattern(self):
        """Test parsing simple pattern without parameters."""
        result = parse_url_pattern("about/")
        assert result["is_regex"] is False
        assert result["converters"] == {}
        assert result["named_groups"] == []

    def test_complex_path_pattern(self):
        """Test parsing complex path pattern."""
        result = parse_url_pattern("archive/<int:year>/<int:month>/<slug>/")
        assert result["is_regex"] is False
        assert result["converters"] == {"year": "int", "month": "int", "slug": "str"}
        assert result["named_groups"] == []
