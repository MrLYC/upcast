"""Tests for HTTP request URL patterns and extraction."""

import pytest

from upcast.scanners.http_requests import HttpRequestsScanner


class TestUrlPatterns:
    """Test URL pattern detection and extraction."""

    def test_static_url(self, scanner: HttpRequestsScanner, tmp_path):
        """Test static URL extraction."""
        code = """
import requests
requests.get('https://api.example.com/users')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "https://api.example.com/users" in result.results

    def test_url_with_variable(self, scanner: HttpRequestsScanner, tmp_path):
        """Test URL with variable."""
        code = """
import requests
url = 'https://api.example.com/users'
requests.get(url)
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "https://api.example.com/users" in result.results

    def test_url_concatenation(self, scanner: HttpRequestsScanner, tmp_path):
        """Test URL built with concatenation."""
        code = """
import requests
base = 'https://api.example.com'
path = '/users'
requests.get(base + path)
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        urls = list(result.results.keys())
        assert len(urls) == 1
        # Should resolve the concatenation
        assert "https://api.example.com/users" in urls[0] or "..." in urls[0]

    def test_fstring_url_simple(self, scanner: HttpRequestsScanner, tmp_path):
        """Test f-string URL construction."""
        code = """
import requests
user_id = 123
requests.get(f'https://api.example.com/users/{user_id}')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        urls = list(result.results.keys())
        assert len(urls) == 1
        # Should have pattern with ...
        assert "..." in urls[0]

    def test_fstring_url_multiple_vars(self, scanner: HttpRequestsScanner, tmp_path):
        """Test f-string with multiple variables."""
        code = """
import requests
domain = 'api.example.com'
endpoint = 'users'
id = 123
requests.get(f'https://{domain}/{endpoint}/{id}')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        urls = list(result.results.keys())
        assert len(urls) == 1

    def test_format_string_url(self, scanner: HttpRequestsScanner, tmp_path):
        """Test .format() URL construction."""
        code = """
import requests
requests.get('https://api.example.com/users/{}'.format(123))
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        urls = list(result.results.keys())
        assert len(urls) == 1
        assert "..." in urls[0]

    def test_url_with_query_string(self, scanner: HttpRequestsScanner, tmp_path):
        """Test URL with query string."""
        code = """
import requests
requests.get('https://api.example.com/search?q=python&page=1')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        urls = list(result.results.keys())
        assert len(urls) == 1

    def test_url_from_keyword_arg(self, scanner: HttpRequestsScanner, tmp_path):
        """Test URL passed as keyword argument."""
        code = """
import requests
requests.get(url='https://api.example.com/users')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert "https://api.example.com/users" in result.results

    def test_url_percent_formatting(self, scanner: HttpRequestsScanner, tmp_path):
        """Test URL with % formatting."""
        code = """
import requests
requests.get('https://api.example.com/users/%s' % 123)
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        urls = list(result.results.keys())
        assert len(urls) == 1

    def test_same_url_multiple_times(self, scanner: HttpRequestsScanner, tmp_path):
        """Test same URL accessed multiple times."""
        code = """
import requests
requests.get('https://api.example.com/users')
requests.get('https://api.example.com/users')
requests.post('https://api.example.com/users', json={})
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.summary.total_requests == 3
        assert "https://api.example.com/users" in result.results
        assert len(result.results["https://api.example.com/users"].usages) == 3

    def test_different_urls_same_domain(self, scanner: HttpRequestsScanner, tmp_path):
        """Test different URLs on same domain."""
        code = """
import requests
requests.get('https://api.example.com/users')
requests.get('https://api.example.com/posts')
requests.get('https://api.example.com/comments')
"""
        file_path = tmp_path / "test.py"
        file_path.write_text(code)

        result = scanner.scan(tmp_path)

        assert result.summary.total_requests == 3
        assert result.summary.unique_urls == 3
        assert "https://api.example.com/users" in result.results
        assert "https://api.example.com/posts" in result.results
        assert "https://api.example.com/comments" in result.results
