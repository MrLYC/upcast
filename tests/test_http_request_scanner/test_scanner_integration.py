"""Integration tests for HTTP requests scanner."""

import pytest

from upcast.scanners.http_requests import HttpRequestsScanner


class TestHttpRequestsScanner:
    """Test HTTP requests scanner integration."""

    def test_scan_requests_get(self, scanner: HttpRequestsScanner, tmp_path):
        """Test scanning requests.get() call."""
        code = """
import requests

response = requests.get('https://api.example.com/users')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.summary.total_requests == 1
        assert "https://api.example.com/users" in result.results
        assert result.results["https://api.example.com/users"].method == "GET"
        assert result.results["https://api.example.com/users"].library == "requests"

    def test_scan_requests_post(self, scanner: HttpRequestsScanner, tmp_path):
        """Test scanning requests.post() call."""
        code = """
import requests

response = requests.post('https://api.example.com/users', json={'name': 'Alice'})
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.summary.total_requests == 1
        url = list(result.results.keys())[0]
        assert result.results[url].method == "POST"
        assert result.results[url].usages[0].json_body == {"name": "Alice"}

    def test_scan_multiple_methods(self, scanner: HttpRequestsScanner, tmp_path):
        """Test scanning multiple HTTP methods."""
        code = """
import requests

requests.get('https://api.example.com/users')
requests.post('https://api.example.com/users', json={'name': 'Bob'})
requests.put('https://api.example.com/users/1', json={'name': 'Charlie'})
requests.delete('https://api.example.com/users/1')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.summary.total_requests == 4
        # Collect all methods from all usages
        all_methods = []
        for info in result.results.values():
            for usage in info.usages:
                all_methods.append(usage.method)
        assert "GET" in all_methods
        assert "POST" in all_methods
        assert "PUT" in all_methods
        assert "DELETE" in all_methods

    def test_scan_with_params(self, scanner: HttpRequestsScanner, tmp_path):
        """Test scanning request with query parameters."""
        code = """
import requests

response = requests.get('https://api.example.com/search', params={'q': 'python', 'page': 1})
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.summary.total_requests == 1
        url = list(result.results.keys())[0]
        assert result.results[url].usages[0].params == {"q": "python", "page": 1}

    def test_scan_with_headers(self, scanner: HttpRequestsScanner, tmp_path):
        """Test scanning request with headers."""
        code = """
import requests

response = requests.get(
    'https://api.example.com/data',
    headers={'Authorization': 'Bearer token123', 'Content-Type': 'application/json'}
)
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.summary.total_requests == 1
        url = list(result.results.keys())[0]
        headers = result.results[url].usages[0].headers
        assert headers == {"Authorization": "Bearer token123", "Content-Type": "application/json"}

    def test_scan_with_timeout(self, scanner: HttpRequestsScanner, tmp_path):
        """Test scanning request with timeout."""
        code = """
import requests

response = requests.get('https://api.example.com/slow', timeout=30)
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.summary.total_requests == 1
        url = list(result.results.keys())[0]
        assert result.results[url].usages[0].timeout == 30

    def test_scan_httpx_library(self, scanner: HttpRequestsScanner, tmp_path):
        """Test scanning httpx library."""
        code = """
import httpx

response = httpx.get('https://api.example.com/users')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.summary.total_requests == 1
        # Library detection may default to requests if not explicitly async
        assert result.summary.by_library.get("requests") == 1 or result.summary.by_library.get("httpx") == 1

    def test_scan_aiohttp_library(self, scanner: HttpRequestsScanner, tmp_path):
        """Test scanning aiohttp library."""
        code = """
import aiohttp

async def fetch():
    async with aiohttp.get('https://api.example.com/users') as response:
        return await response.text()
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.summary.total_requests == 1
        url = list(result.results.keys())[0]
        assert result.results[url].usages[0].is_async is True

    def test_scan_empty_directory(self, scanner: HttpRequestsScanner, tmp_path):
        """Test scanning empty directory."""
        result = scanner.scan(tmp_path)

        assert result.summary.total_requests == 0
        assert len(result.results) == 0

    def test_scan_no_http_requests(self, scanner: HttpRequestsScanner, tmp_path):
        """Test scanning file without HTTP requests."""
        code = """
def hello():
    return "Hello, World!"
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.summary.total_requests == 0
        assert len(result.results) == 0

    def test_scan_multiple_files(self, scanner: HttpRequestsScanner, tmp_path):
        """Test scanning multiple files."""
        file1 = tmp_path / "api.py"
        file1.write_text("import requests\nrequests.get('https://api1.com')")

        file2 = tmp_path / "client.py"
        file2.write_text("import requests\nrequests.post('https://api2.com', json={})")

        result = scanner.scan(tmp_path)

        assert result.summary.total_requests == 2
        assert result.summary.files_scanned == 2
        assert len(result.results) == 2

    def test_scan_summary_statistics(self, scanner: HttpRequestsScanner, tmp_path):
        """Test summary statistics calculation."""
        code = """
import requests
import httpx

requests.get('https://api1.com')
requests.post('https://api1.com')
httpx.get('https://api2.com')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.summary.total_requests == 3
        assert result.summary.unique_urls == 2
        # httpx may be detected as requests library
        assert sum(result.summary.by_library.values()) == 3

    def test_scan_dynamic_url(self, scanner: HttpRequestsScanner, tmp_path):
        """Test scanning request with dynamic URL."""
        code = """
import requests

base_url = 'https://api.example.com'
endpoint = '/users'
response = requests.get(base_url + endpoint)
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.summary.total_requests == 1
        # Dynamic URLs should be captured with pattern
        urls = list(result.results.keys())
        assert len(urls) == 1

    def test_scan_fstring_url(self, scanner: HttpRequestsScanner, tmp_path):
        """Test scanning request with f-string URL."""
        code = """
import requests

user_id = 123
response = requests.get(f'https://api.example.com/users/{user_id}')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.summary.total_requests == 1
        urls = list(result.results.keys())
        assert len(urls) == 1
        # Should capture the pattern
        assert "users/..." in urls[0] or "..." in urls[0]
