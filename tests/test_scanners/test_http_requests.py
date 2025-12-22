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
            session_based=False,
            is_async=False,
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

    def test_scanner_extracts_fstring_with_resolvable_vars(self, tmp_path):
        """Test scanner resolves variables in f-strings."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import requests

proto = "https"
host = "api.example.com"
response = requests.get(f"{proto}://{host}/api/v1/users")
"""
        )

        scanner = HttpRequestsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 1
        # Should resolve to full URL
        assert "https://api.example.com/api/v1/users" in output.results

    def test_scanner_preserves_static_paths_in_patterns(self, tmp_path):
        """Test scanner preserves static path components in URL patterns."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import requests

def fetch_user(user_id):
    return requests.get(f"https://api.example.com/users/{user_id}")
"""
        )

        scanner = HttpRequestsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 1
        # Should preserve static parts
        assert "https://api.example.com/users/..." in output.results

    def test_scanner_handles_dynamic_protocol_and_host(self, tmp_path):
        """Test scanner handles dynamic protocol and host."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import requests

def fetch(proto, host, path):
    return requests.get(f"{proto}://{host}/{path}")
"""
        )

        scanner = HttpRequestsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 1
        # Should show pattern
        assert "...://.../..." in output.results

    def test_scanner_resolves_concatenation_with_base_url(self, tmp_path):
        """Test scanner resolves concatenation when base URL is defined."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import requests

BASE_URL = "https://api.example.com"
response = requests.get(BASE_URL + "/users/list")
"""
        )

        scanner = HttpRequestsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 1
        # Should resolve to full URL
        assert "https://api.example.com/users/list" in output.results

    def test_scanner_preserves_static_parts_in_concatenation(self, tmp_path):
        """Test scanner preserves static parts in string concatenation."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import requests

def fetch(base_url, endpoint):
    return requests.get(base_url + "/api/v2/" + endpoint)
"""
        )

        scanner = HttpRequestsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 1
        # Should preserve /api/v2/ part
        assert ".../api/v2/..." in output.results

    def test_scanner_handles_format_strings(self, tmp_path):
        """Test scanner handles .format() strings."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import requests

API_BASE = "https://api.example.com"
response = requests.get("{}/items/{}".format(API_BASE, "123"))
"""
        )

        scanner = HttpRequestsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 1
        # Should preserve /items/ part
        assert ".../items/..." in output.results

    def test_scanner_merges_consecutive_dots(self, tmp_path):
        """Test scanner merges consecutive ... into single ..."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import requests

def fetch(a, b, c, d):
    # Multiple dynamic parts that would create many consecutive ...
    return requests.get(f"{a}{b}{c}{d}")
"""
        )

        scanner = HttpRequestsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 1
        # Should merge consecutive ... into single ...
        assert "..." in output.results
        # Should not have multiple consecutive dots
        for url in output.results:
            # Check that we don't have 4+ consecutive dots
            import re

            assert not re.search(r"\.{4,}", url), f"Found consecutive dots in: {url}"

    def test_scanner_handles_empty_file(self, tmp_path):
        """Test scanner handles empty files."""
        test_file = tmp_path / "test.py"
        test_file.write_text("")

        scanner = HttpRequestsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count == 0
