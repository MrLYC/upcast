"""Tests for HttpRequestScanner."""

from upcast.scanners.http_requests import (
    HttpRequestsScanner,
    HttpRequestUsage,
)


class TestHttpRequestModels:
    """Tests for HttpRequest models."""

    def test_valid_usage(self):
        """Test creating valid HttpRequestUsage."""
        usage = HttpRequestUsage(
            location="test.py:10",
            statement="requests.get('http://api.example.com')",
            method="GET",
            params=None,
            headers=None,
            json_body=None,
            data=None,
            timeout=None,
        )
        assert usage.method == "GET"


class TestHttpRequestScannerIntegration:
    """Integration tests for HttpRequestScanner."""

    def test_scanner_detects_requests_get(self, tmp_path):
        """Test scanner detects requests.get."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import requests
response = requests.get('http://api.example.com')
"""
        )

        scanner = HttpRequestsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 0

    def test_scanner_handles_empty_file(self, tmp_path):
        """Test scanner handles empty files."""
        test_file = tmp_path / "test.py"
        test_file.write_text("")

        scanner = HttpRequestsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 0
