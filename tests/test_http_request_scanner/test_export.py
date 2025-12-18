"""Tests for export module."""

from upcast.http_request_scanner.export import format_request_output, format_single_usage
from upcast.http_request_scanner.request_parser import HttpRequest


def test_format_single_usage():
    """Test formatting a single HTTP request usage."""
    request = HttpRequest(
        location="api/client.py:15",
        statement="requests.get('https://api.example.com/users', params={'page': 1})",
        library="requests",
        url="https://api.example.com/users",
        method="GET",
        params={"page": 1},
        headers={"Authorization": "Bearer token"},
        json_body=None,
        data=None,
        timeout=5,
        session_based=False,
        is_async=False,
    )

    result = format_single_usage(request)

    assert result["location"] == "api/client.py:15"
    assert result["statement"] == "requests.get('https://api.example.com/users', params={'page': 1})"
    assert result["method"] == "GET"
    assert result["params"] == {"page": 1}
    assert result["headers"] == {"Authorization": "Bearer token"}
    assert result["json_body"] is None
    assert result["data"] is None
    assert result["timeout"] == 5
    assert result["session_based"] is False
    assert result["is_async"] is False


def test_format_request_output_single_url():
    """Test formatting output with a single URL."""
    requests = [
        HttpRequest(
            location="api/client.py:15",
            statement="requests.get('https://api.example.com/users')",
            library="requests",
            url="https://api.example.com/users",
            method="GET",
            params={},
            headers={},
            json_body=None,
            data=None,
            timeout=None,
            session_based=False,
            is_async=False,
        )
    ]
    requests_by_url = {"https://api.example.com/users": requests}
    summary = {
        "total_requests": 1,
        "unique_urls": 1,
        "libraries_used": ["requests"],
    }

    result = format_request_output(requests_by_url, summary)

    assert "summary" in result
    assert result["summary"] == summary
    assert "https://api.example.com/users" in result
    assert result["https://api.example.com/users"]["method"] == "GET"
    assert result["https://api.example.com/users"]["library"] == "requests"
    assert len(result["https://api.example.com/users"]["usages"]) == 1


def test_format_request_output_multiple_urls():
    """Test formatting output with multiple URLs."""
    requests_by_url = {
        "https://api.example.com/users": [
            HttpRequest(
                location="api/client.py:15",
                statement="requests.get('https://api.example.com/users')",
                library="requests",
                url="https://api.example.com/users",
                method="GET",
                params={},
                headers={},
                json_body=None,
                data=None,
                timeout=None,
                session_based=False,
                is_async=False,
            )
        ],
        "https://api.example.com/posts": [
            HttpRequest(
                location="api/client.py:20",
                statement="requests.get('https://api.example.com/posts')",
                library="requests",
                url="https://api.example.com/posts",
                method="GET",
                params={},
                headers={},
                json_body=None,
                data=None,
                timeout=None,
                session_based=False,
                is_async=False,
            )
        ],
    }
    summary = {
        "total_requests": 2,
        "unique_urls": 2,
        "libraries_used": ["requests"],
    }

    result = format_request_output(requests_by_url, summary)

    assert len(result) == 3  # 2 URLs + summary
    assert "https://api.example.com/users" in result
    assert "https://api.example.com/posts" in result


def test_format_request_output_same_url_multiple_usages():
    """Test formatting output where same URL is used multiple times."""
    requests_by_url = {
        "https://api.example.com/data": [
            HttpRequest(
                location="api/client.py:15",
                statement="requests.get('https://api.example.com/data')",
                library="requests",
                url="https://api.example.com/data",
                method="GET",
                params={},
                headers={},
                json_body=None,
                data=None,
                timeout=None,
                session_based=False,
                is_async=False,
            ),
            HttpRequest(
                location="api/client.py:20",
                statement="requests.post('https://api.example.com/data', json={'key': 'value'})",
                library="requests",
                url="https://api.example.com/data",
                method="POST",
                params={},
                headers={},
                json_body={"key": "value"},
                data=None,
                timeout=None,
                session_based=False,
                is_async=False,
            ),
        ]
    }
    summary = {
        "total_requests": 2,
        "unique_urls": 1,
        "libraries_used": ["requests"],
    }

    result = format_request_output(requests_by_url, summary)

    assert len(result["https://api.example.com/data"]["usages"]) == 2
    # Primary method should be GET (first in list, or most common)
    assert result["https://api.example.com/data"]["method"] in ["GET", "POST"]


def test_format_request_output_mixed_libraries():
    """Test formatting output with multiple libraries."""
    requests_by_url = {
        "https://example.com": [
            HttpRequest(
                location="api/client.py:15",
                statement="requests.get('https://example.com')",
                library="requests",
                url="https://example.com",
                method="GET",
                params={},
                headers={},
                json_body=None,
                data=None,
                timeout=None,
                session_based=False,
                is_async=False,
            ),
            HttpRequest(
                location="api/client.py:20",
                statement="httpx.get('https://example.com')",
                library="httpx",
                url="https://example.com",
                method="GET",
                params={},
                headers={},
                json_body=None,
                data=None,
                timeout=None,
                session_based=False,
                is_async=False,
            ),
        ]
    }
    summary = {
        "total_requests": 2,
        "unique_urls": 1,
        "libraries_used": ["requests", "httpx"],
    }

    result = format_request_output(requests_by_url, summary)

    # Should have both usages
    assert len(result["https://example.com"]["usages"]) == 2
    # Primary library should be one of them
    assert result["https://example.com"]["library"] in ["requests", "httpx"]


def test_format_request_output_sorted_urls():
    """Test that URLs are sorted alphabetically in output."""
    requests_by_url = {
        "https://z.com": [
            HttpRequest("z.py:1", "z", "requests", "https://z.com", "GET", {}, {}, None, None, None, False, False)
        ],
        "https://a.com": [
            HttpRequest("a.py:1", "a", "requests", "https://a.com", "GET", {}, {}, None, None, None, False, False)
        ],
        "https://m.com": [
            HttpRequest("m.py:1", "m", "requests", "https://m.com", "GET", {}, {}, None, None, None, False, False)
        ],
    }
    summary = {"total_requests": 3, "unique_urls": 3, "libraries_used": ["requests"]}

    result = format_request_output(requests_by_url, summary)

    # Extract keys (excluding 'summary')
    url_keys = [k for k in result if k != "summary"]
    # Check they are sorted
    assert url_keys == sorted(url_keys)
    requests_by_url = {
        "https://example.com": [
            HttpRequest(
                "z.py:30", "z", "requests", "https://example.com", "GET", {}, {}, None, None, None, False, False
            ),
            HttpRequest(
                "a.py:10", "a", "requests", "https://example.com", "GET", {}, {}, None, None, None, False, False
            ),
            HttpRequest(
                "m.py:20", "m", "requests", "https://example.com", "GET", {}, {}, None, None, None, False, False
            ),
        ]
    }
    summary = {"total_requests": 3, "unique_urls": 1, "libraries_used": ["requests"]}

    result = format_request_output(requests_by_url, summary)

    usages = result["https://example.com"]["usages"]
    locations = [u["location"] for u in usages]
    # Check they are sorted
    assert locations == sorted(locations)
