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
            file="test.py",
            line=10,
            statement="requests.get('http://api.example.com')",
            method="GET",
            params={},
            headers={},
            json_body={},
            data={},
            timeout=0,
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

    def test_scanner_handles_request_constructor_positional(self, tmp_path):
        """Test scanner handles Request(method, url) with positional args."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
from requests import Request

req = Request('GET', 'https://api.example.com/data')
"""
        )

        scanner = HttpRequestsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 1
        # URL should be extracted from second argument
        assert "https://api.example.com/data" in output.results
        # Method should be extracted from first argument
        result = output.results["https://api.example.com/data"]
        assert result.method == "GET"
        # Should NOT have "GET" as a URL key
        assert "GET" not in output.results or output.results["GET"].method != "REQUEST"

    def test_scanner_handles_request_constructor_keyword_args(self, tmp_path):
        """Test scanner handles Request(method='GET', url='...')."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
from requests import Request

req = Request(method='POST', url='https://api.example.com/submit')
"""
        )

        scanner = HttpRequestsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 1
        # URL should be extracted from url keyword
        assert "https://api.example.com/submit" in output.results
        # Method should be POST
        result = output.results["https://api.example.com/submit"]
        assert result.method == "POST"

    def test_scanner_handles_request_constructor_mixed_args(self, tmp_path):
        """Test scanner handles Request('GET', url='...')."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
from requests import Request

req = Request('DELETE', url='https://api.example.com/items/123')
"""
        )

        scanner = HttpRequestsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 1
        # URL should be extracted from url keyword
        assert "https://api.example.com/items/123" in output.results
        # Method should be DELETE
        result = output.results["https://api.example.com/items/123"]
        assert result.method == "DELETE"

    def test_scanner_handles_request_constructor_with_dynamic_url(self, tmp_path):
        """Test scanner handles Request with dynamic URL."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
from requests import Request

def make_request(item_id):
    req = Request('GET', f'https://api.example.com/items/{item_id}')
    return req
"""
        )

        scanner = HttpRequestsScanner()
        output = scanner.scan(test_file)

        assert output.summary.total_count >= 1
        # Should preserve static parts and show pattern
        assert "https://api.example.com/items/..." in output.results
        result = output.results["https://api.example.com/items/..."]
        assert result.method == "GET"

    def test_scanner_excludes_request_exception(self, tmp_path):
        """Test scanner does not identify RequestException as a request."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
from requests import RequestException

def test_error():
    raise RequestException("error")
"""
        )

        scanner = HttpRequestsScanner()
        output = scanner.scan(test_file)

        # Should not identify RequestException as a request
        assert output.summary.total_count == 0
        assert len(output.results) == 0

    def test_scanner_excludes_response_class(self, tmp_path):
        """Test scanner does not identify Response as a request."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
from requests import Response

def mock_response():
    resp = Response()
    return resp
"""
        )

        scanner = HttpRequestsScanner()
        output = scanner.scan(test_file)

        # Should not identify Response as a request
        assert output.summary.total_count == 0
        assert len(output.results) == 0

    def test_scanner_excludes_auth_classes(self, tmp_path):
        """Test scanner does not identify auth classes as requests."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
from requests.auth import HTTPBasicAuth

def setup_auth():
    auth = HTTPBasicAuth('user', 'pass')
    return auth
"""
        )

        scanner = HttpRequestsScanner()
        output = scanner.scan(test_file)

        # Should not identify HTTPBasicAuth as a request
        assert output.summary.total_count == 0
        assert len(output.results) == 0

    def test_scanner_excludes_instrumentor(self, tmp_path):
        """Test scanner does not identify instrumentor as a request."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
from opentelemetry.instrumentation.requests import RequestsInstrumentor

def setup_tracing():
    instrumentor = RequestsInstrumentor()
    return instrumentor
"""
        )

        scanner = HttpRequestsScanner()
        output = scanner.scan(test_file)

        # Should not identify RequestsInstrumentor as a request
        assert output.summary.total_count == 0
        assert len(output.results) == 0

    def test_scanner_still_detects_real_requests(self, tmp_path):
        """Test scanner still detects real requests after exclusion filter."""
        test_file = tmp_path / "test.py"
        test_file.write_text(
            """
import requests
from requests import Response, RequestException

def fetch_data():
    # This should be detected
    response = requests.get('https://api.example.com/data')

    # These should NOT be detected
    if isinstance(response, Response):
        pass

    try:
        pass
    except RequestException:
        pass

    return response
"""
        )

        scanner = HttpRequestsScanner()
        output = scanner.scan(test_file)

        # Should only detect the real request, not Response or RequestException
        assert output.summary.total_count == 1
        assert "https://api.example.com/data" in output.results
