"""Tests for HTTP request scanner models."""

import pytest

from upcast.models.http_requests import HttpRequestInfo, HttpRequestOutput, HttpRequestSummary, HttpRequestUsage


class TestHttpRequestUsage:
    """Test HttpRequestUsage model."""

    def test_basic_usage(self):
        """Test basic request usage creation."""
        usage = HttpRequestUsage(
            file="test.py",
            line=10,
            statement="requests.get('https://api.example.com')",
            method="GET",
            session_based=False,
            is_async=False,
        )

        assert usage.file == "test.py"
        assert usage.line == 10
        assert usage.method == "GET"
        assert usage.session_based is False
        assert usage.is_async is False

    def test_usage_with_params(self):
        """Test usage with query parameters."""
        usage = HttpRequestUsage(
            file="test.py",
            line=10,
            statement="requests.get(url, params={'key': 'value'})",
            method="GET",
            params={"key": "value"},
            session_based=False,
            is_async=False,
        )

        assert usage.params == {"key": "value"}

    def test_usage_with_headers(self):
        """Test usage with headers."""
        usage = HttpRequestUsage(
            file="test.py",
            line=10,
            statement="requests.get(url, headers={'Authorization': 'Bearer token'})",
            method="GET",
            headers={"Authorization": "Bearer token"},
            session_based=False,
            is_async=False,
        )

        assert usage.headers == {"Authorization": "Bearer token"}

    def test_usage_with_json_body(self):
        """Test usage with JSON body."""
        usage = HttpRequestUsage(
            file="test.py",
            line=10,
            statement="requests.post(url, json={'data': 'value'})",
            method="POST",
            json_body={"data": "value"},
            session_based=False,
            is_async=False,
        )

        assert usage.json_body == {"data": "value"}

    def test_usage_with_timeout(self):
        """Test usage with timeout."""
        usage = HttpRequestUsage(
            file="test.py",
            line=10,
            statement="requests.get(url, timeout=30)",
            method="GET",
            timeout=30,
            session_based=False,
            is_async=False,
        )

        assert usage.timeout == 30


class TestHttpRequestInfo:
    """Test HttpRequestInfo model."""

    def test_request_info(self):
        """Test request info creation."""
        usage = HttpRequestUsage(
            file="test.py",
            line=10,
            statement="requests.get(url)",
            method="GET",
            session_based=False,
            is_async=False,
        )

        info = HttpRequestInfo(
            method="GET",
            library="requests",
            usages=[usage],
        )

        assert info.method == "GET"
        assert info.library == "requests"
        assert len(info.usages) == 1


class TestHttpRequestSummary:
    """Test HttpRequestSummary model."""

    def test_summary(self):
        """Test summary creation."""
        summary = HttpRequestSummary(
            total_count=10,
            files_scanned=5,
            scan_duration_ms=100,
            total_requests=10,
            unique_urls=3,
            by_library={"requests": 7, "httpx": 3},
        )

        assert summary.total_requests == 10
        assert summary.unique_urls == 3
        assert summary.by_library == {"requests": 7, "httpx": 3}

    def test_summary_validation(self):
        """Test summary validation."""
        with pytest.raises(ValueError):
            HttpRequestSummary(
                total_count=-1,  # Invalid: negative count
                files_scanned=1,
                scan_duration_ms=100,
                total_requests=10,
                unique_urls=3,
                by_library={},
            )


class TestHttpRequestOutput:
    """Test HttpRequestOutput model."""

    def test_output_structure(self):
        """Test output structure."""
        usage = HttpRequestUsage(
            file="test.py",
            line=10,
            statement="requests.get('https://api.example.com')",
            method="GET",
            session_based=False,
            is_async=False,
        )

        info = HttpRequestInfo(
            method="GET",
            library="requests",
            usages=[usage],
        )

        summary = HttpRequestSummary(
            total_count=1,
            files_scanned=1,
            scan_duration_ms=50,
            total_requests=1,
            unique_urls=1,
            by_library={"requests": 1},
        )

        output = HttpRequestOutput(
            summary=summary,
            results={"https://api.example.com": info},
        )

        assert output.summary.total_requests == 1
        assert "https://api.example.com" in output.results
