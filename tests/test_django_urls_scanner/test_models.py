"""Test Pydantic models for Django URL scanner."""

import pytest
from pydantic import ValidationError

from upcast.models.django_urls import (
    UrlPattern,
    UrlModule,
    DjangoUrlSummary,
    DjangoUrlOutput,
)


class TestUrlPatternModel:
    """Test UrlPattern model validation."""

    def test_url_pattern_model_valid(self):
        """Test creating a valid UrlPattern instance."""
        pattern = UrlPattern(
            type="path",
            pattern="articles/",
            view_module="myapp.views",
            view_name="article_list",
            name="article-list",
            converters=[],
            named_groups=[],
            is_partial=False,
            is_conditional=False,
        )

        assert pattern.type == "path"
        assert pattern.pattern == "articles/"
        assert pattern.view_module == "myapp.views"
        assert pattern.view_name == "article_list"
        assert pattern.name == "article-list"
        assert pattern.converters == []
        assert pattern.named_groups == []
        assert pattern.is_partial is False
        assert pattern.is_conditional is False

    def test_url_pattern_with_converters(self):
        """Test UrlPattern with path converters."""
        pattern = UrlPattern(
            type="path",
            pattern="articles/<int:pk>/",
            view_module="myapp.views",
            view_name="article_detail",
            name="article-detail",
            converters=["int:pk"],
            named_groups=[],
            is_partial=False,
            is_conditional=False,
        )

        assert pattern.converters == ["int:pk"]
        assert pattern.pattern == "articles/<int:pk>/"

    def test_url_pattern_with_named_groups(self):
        """Test UrlPattern with named regex groups."""
        pattern = UrlPattern(
            type="re_path",
            pattern=r"^articles/(?P<year>[0-9]{4})/$",
            view_module="myapp.views",
            view_name="year_archive",
            name="year-archive",
            converters=[],
            named_groups=["year"],
            is_partial=False,
            is_conditional=False,
        )

        assert pattern.type == "re_path"
        assert pattern.named_groups == ["year"]

    def test_url_pattern_include(self):
        """Test UrlPattern for include()."""
        pattern = UrlPattern(
            type="include",
            pattern="api/",
            include_module="myapp.api.urls",
            namespace="api-v1",
            converters=[],
            named_groups=[],
            is_partial=False,
            is_conditional=False,
        )

        assert pattern.type == "include"
        assert pattern.include_module == "myapp.api.urls"
        assert pattern.namespace == "api-v1"

    def test_url_pattern_router_registration(self):
        """Test UrlPattern for DRF router registration."""
        pattern = UrlPattern(
            type="router_registration",
            pattern="articles",
            view_module="myapp.views",
            view_name="ArticleViewSet",
            basename="article",
            router_type="DefaultRouter",
            converters=[],
            named_groups=[],
            is_partial=False,
            is_conditional=False,
        )

        assert pattern.type == "router_registration"
        assert pattern.basename == "article"
        assert pattern.router_type == "DefaultRouter"

    def test_url_pattern_serialization(self):
        """Test that UrlPattern can be serialized to dict."""
        pattern = UrlPattern(
            type="path",
            pattern="posts/",
            view_name="post_list",
            converters=[],
            named_groups=[],
            is_partial=False,
            is_conditional=False,
        )

        data = pattern.model_dump()
        assert isinstance(data, dict)
        assert data["type"] == "path"
        assert data["pattern"] == "posts/"


class TestUrlModuleModel:
    """Test UrlModule model validation."""

    def test_url_module_valid(self):
        """Test creating a valid UrlModule instance."""
        pattern1 = UrlPattern(
            type="path",
            pattern="articles/",
            view_name="article_list",
            converters=[],
            named_groups=[],
            is_partial=False,
            is_conditional=False,
        )
        pattern2 = UrlPattern(
            type="path",
            pattern="posts/",
            view_name="post_list",
            converters=[],
            named_groups=[],
            is_partial=False,
            is_conditional=False,
        )

        module = UrlModule(urlpatterns=[pattern1, pattern2])

        assert len(module.urlpatterns) == 2
        assert module.urlpatterns[0].pattern == "articles/"
        assert module.urlpatterns[1].pattern == "posts/"

    def test_url_module_empty(self):
        """Test UrlModule with no patterns."""
        module = UrlModule(urlpatterns=[])
        assert len(module.urlpatterns) == 0


class TestDjangoUrlSummaryModel:
    """Test DjangoUrlSummary model validation."""

    def test_summary_model_valid(self):
        """Test creating a valid DjangoUrlSummary instance."""
        summary = DjangoUrlSummary(
            total_count=10,
            files_scanned=3,
            total_modules=3,
            total_patterns=10,
            scan_duration_ms=150,
        )

        assert summary.total_count == 10
        assert summary.files_scanned == 3
        assert summary.total_modules == 3
        assert summary.total_patterns == 10
        assert summary.scan_duration_ms == 150

    def test_summary_model_zero_patterns(self):
        """Test summary with zero patterns."""
        summary = DjangoUrlSummary(
            total_count=0,
            files_scanned=5,
            total_modules=0,
            total_patterns=0,
            scan_duration_ms=50,
        )

        assert summary.total_patterns == 0
        assert summary.total_modules == 0

    def test_summary_model_validation(self):
        """Test that summary validates non-negative values."""
        with pytest.raises(ValidationError):
            DjangoUrlSummary(
                total_count=0,
                files_scanned=0,
                total_modules=-1,  # Invalid: must be >= 0
                total_patterns=0,
                scan_duration_ms=0,
            )


class TestDjangoUrlOutputModel:
    """Test DjangoUrlOutput model validation."""

    def test_output_model_valid(self):
        """Test creating a valid DjangoUrlOutput instance."""
        summary = DjangoUrlSummary(
            total_count=2,
            files_scanned=1,
            total_modules=1,
            total_patterns=2,
            scan_duration_ms=100,
        )

        pattern1 = UrlPattern(
            type="path",
            pattern="articles/",
            view_name="article_list",
            converters=[],
            named_groups=[],
            is_partial=False,
            is_conditional=False,
        )
        pattern2 = UrlPattern(
            type="path",
            pattern="posts/",
            view_name="post_list",
            converters=[],
            named_groups=[],
            is_partial=False,
            is_conditional=False,
        )

        module = UrlModule(urlpatterns=[pattern1, pattern2])
        output = DjangoUrlOutput(summary=summary, results={"myapp.urls": module})

        assert output.summary.total_patterns == 2
        assert len(output.results) == 1
        assert "myapp.urls" in output.results
        assert len(output.results["myapp.urls"].urlpatterns) == 2

    def test_output_model_empty_results(self):
        """Test output with no modules."""
        summary = DjangoUrlSummary(
            total_count=0,
            files_scanned=5,
            total_modules=0,
            total_patterns=0,
            scan_duration_ms=50,
        )

        output = DjangoUrlOutput(summary=summary, results={})

        assert output.summary.total_patterns == 0
        assert len(output.results) == 0

    def test_output_model_multiple_modules(self):
        """Test output with multiple URL modules."""
        summary = DjangoUrlSummary(
            total_count=4,
            files_scanned=2,
            total_modules=2,
            total_patterns=4,
            scan_duration_ms=200,
        )

        module1 = UrlModule(
            urlpatterns=[
                UrlPattern(
                    type="path",
                    pattern="articles/",
                    view_name="article_list",
                    converters=[],
                    named_groups=[],
                    is_partial=False,
                    is_conditional=False,
                )
            ]
        )
        module2 = UrlModule(
            urlpatterns=[
                UrlPattern(
                    type="path",
                    pattern="posts/",
                    view_name="post_list",
                    converters=[],
                    named_groups=[],
                    is_partial=False,
                    is_conditional=False,
                ),
                UrlPattern(
                    type="path",
                    pattern="comments/",
                    view_name="comment_list",
                    converters=[],
                    named_groups=[],
                    is_partial=False,
                    is_conditional=False,
                ),
            ]
        )

        output = DjangoUrlOutput(summary=summary, results={"myapp.urls": module1, "myapp.api.urls": module2})

        assert len(output.results) == 2
        assert len(output.results["myapp.urls"].urlpatterns) == 1
        assert len(output.results["myapp.api.urls"].urlpatterns) == 2

    def test_output_model_serialization(self):
        """Test that output can be serialized to dict."""
        summary = DjangoUrlSummary(
            total_count=1,
            files_scanned=1,
            total_modules=1,
            total_patterns=1,
            scan_duration_ms=100,
        )

        pattern = UrlPattern(
            type="path",
            pattern="home/",
            view_name="home_view",
            converters=[],
            named_groups=[],
            is_partial=False,
            is_conditional=False,
        )

        module = UrlModule(urlpatterns=[pattern])
        output = DjangoUrlOutput(summary=summary, results={"urls": module})

        data = output.model_dump()
        assert isinstance(data, dict)
        assert "summary" in data
        assert "results" in data
        assert "urls" in data["results"]
        assert len(data["results"]["urls"]["urlpatterns"]) == 1
