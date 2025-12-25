"""Tests for request_parser module."""

from astroid import parse
from upcast.http_request_scanner.request_parser import (
    detect_request_call,
    extract_headers,
    extract_json_body,
    extract_method,
    extract_params,
    extract_timeout,
    extract_url,
    is_async_call,
)


def test_detect_requests_get():
    """Test detection of requests.get() call."""
    code = """
import requests
requests.get('https://example.com')
"""
    tree = parse(code)
    # Get the Call node from tree.body[1] (the expression statement)
    call_node = tree.body[1].value
    library = detect_request_call(call_node)
    assert library == "requests"


def test_extract_url_simple():
    """Test URL extraction from simple string."""
    code = """
import requests
requests.get('https://api.example.com/users')
"""
    tree = parse(code)
    call_node = tree.body[1].value
    url = extract_url(call_node)
    assert url == "https://api.example.com/users"


def test_extract_method_get():
    """Test method extraction for GET."""
    code = """
import requests
requests.get('https://example.com')
"""
    tree = parse(code)
    call_node = tree.body[1].value
    method = extract_method(call_node)
    assert method == "GET"


def test_extract_method_post():
    """Test method extraction for POST."""
    code = """
import requests
requests.post('https://example.com')
"""
    tree = parse(code)
    call_node = tree.body[1].value
    method = extract_method(call_node)
    assert method == "POST"


def test_extract_params():
    """Test params extraction."""
    code = """
import requests
requests.get('https://example.com', params={'page': 1, 'limit': 10})
"""
    tree = parse(code)
    call_node = tree.body[1].value
    params = extract_params(call_node)
    assert params == {"page": 1, "limit": 10}


def test_extract_headers():
    """Test headers extraction."""
    code = """
import requests
requests.get('https://example.com', headers={'Authorization': 'Bearer token'})
"""
    tree = parse(code)
    call_node = tree.body[1].value
    headers = extract_headers(call_node)
    assert headers == {"Authorization": "Bearer token"}


def test_extract_json_body():
    """Test JSON body extraction."""
    code = """
import requests
requests.post('https://example.com', json={'username': 'admin', 'password': 'secret'})
"""
    tree = parse(code)
    call_node = tree.body[1].value
    json_body = extract_json_body(call_node)
    assert json_body == {"username": "admin", "password": "secret"}


def test_extract_timeout():
    """Test timeout extraction."""
    code = """
import requests
requests.get('https://example.com', timeout=5)
"""
    tree = parse(code)
    call_node = tree.body[1].value
    timeout = extract_timeout(call_node)
    assert timeout == 5


def test_is_async_call():
    """Test async call detection."""
    code = """
import httpx

async def fetch():
    await httpx.get('https://example.com')
"""
    tree = parse(code)
    func_def = tree.body[1]
    # Get the await node's value (the call)
    await_node = func_def.body[0].value
    call_node = await_node.value
    is_async = is_async_call(call_node)
    assert is_async is True


def test_is_not_async_call():
    """Test non-async call detection."""
    code = """
import requests

def fetch():
    requests.get('https://example.com')
"""
    tree = parse(code)
    func_def = tree.body[1]
    call_node = func_def.body[0].value
    is_async = is_async_call(call_node)
    assert is_async is False


def test_extract_json_body_returns_none_for_dynamic():
    """
    Regression test: extract_json_body should return None (not a placeholder)
    for bodies that cannot be statically inferred.

    Previously, the scanner would output {"<dynamic>": "..."} which was unhelpful.
    Now it should return None, and the Pydantic model will omit the field.
    """
    code = """
import requests

def api_call(data):
    # data is a variable - cannot be statically inferred
    requests.post('https://example.com', json=data)
"""
    tree = parse(code)
    func_def = tree.body[1]
    call_node = func_def.body[0].value
    json_body = extract_json_body(call_node)
    # Should return None for non-inferrable bodies
    assert json_body is None


def test_extract_params_returns_none_for_dynamic():
    """
    Regression test: extract_params should return None for params that
    cannot be statically inferred.
    """
    code = """
import requests

def api_call(query_params):
    # query_params is a variable - cannot be statically inferred
    requests.get('https://example.com', params=query_params)
"""
    tree = parse(code)
    func_def = tree.body[1]
    call_node = func_def.body[0].value
    params = extract_params(call_node)
    # Should return None for non-inferrable params
    assert params is None


def test_extract_headers_returns_none_for_dynamic():
    """
    Regression test: extract_headers should return None for headers that
    cannot be statically inferred.
    """
    code = """
import requests

def api_call(auth_headers):
    # auth_headers is a variable - cannot be statically inferred
    requests.get('https://example.com', headers=auth_headers)
"""
    tree = parse(code)
    func_def = tree.body[1]
    call_node = func_def.body[0].value
    headers = extract_headers(call_node)
    # Should return None for non-inferrable headers
    assert headers is None
