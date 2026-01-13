"""Pytest fixtures for HTTP request scanner tests."""

import pytest

from upcast.scanners.http_requests import HttpRequestsScanner


@pytest.fixture
def scanner():
    """Create HTTP requests scanner instance."""
    return HttpRequestsScanner(verbose=False)
