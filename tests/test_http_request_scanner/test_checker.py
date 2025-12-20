"""Tests for checker module."""

import tempfile
from pathlib import Path

from upcast.http_request_scanner.checker import HttpRequestChecker


def test_check_simple_requests():
    """Test checking a simple file with requests."""
    code = """
import requests

def fetch_data():
    response = requests.get('https://api.example.com/data')
    return response.json()
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text(code)

        checker = HttpRequestChecker(Path(tmpdir))
        checker.check_file(test_file)

        assert len(checker.requests) == 1
        assert "https://api.example.com/data" in checker.requests
        usages = checker.requests["https://api.example.com/data"]
        assert len(usages) == 1
        assert usages[0].library == "requests"
        assert usages[0].method == "GET"


def test_check_multiple_urls():
    """Test checking a file with multiple different URLs."""
    code = """
import requests

def fetch_users():
    requests.get('https://api.example.com/users')

def fetch_posts():
    requests.get('https://api.example.com/posts')
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text(code)

        checker = HttpRequestChecker(Path(tmpdir))
        checker.check_file(test_file)

        assert len(checker.requests) == 2
        assert "https://api.example.com/users" in checker.requests
        assert "https://api.example.com/posts" in checker.requests


def test_check_same_url_multiple_times():
    """Test checking a file where same URL is used multiple times."""
    code = """
import requests

def fetch_data():
    requests.get('https://api.example.com/data')
    requests.post('https://api.example.com/data', json={'key': 'value'})
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text(code)

        checker = HttpRequestChecker(Path(tmpdir))
        checker.check_file(test_file)

        assert len(checker.requests) == 1
        usages = checker.requests["https://api.example.com/data"]
        assert len(usages) == 2
        # Check both methods are captured
        methods = {usage.method for usage in usages}
        assert methods == {"GET", "POST"}


def test_get_summary():
    """Test summary statistics."""
    code = """
import requests

requests.get('https://api.example.com/users')
requests.get('https://api.example.com/posts')
requests.post('https://api.example.com/users', json={})
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text(code)

        checker = HttpRequestChecker(Path(tmpdir))
        checker.check_file(test_file)

        summary = checker.get_summary()
        assert summary["total_requests"] == 3
        assert summary["unique_urls"] == 2
        assert summary["libraries_used"] == ["requests"]
