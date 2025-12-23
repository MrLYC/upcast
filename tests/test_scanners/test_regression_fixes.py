"""Regression tests for scanner quality fixes.

These tests verify that previously reported false positives and quality
issues have been fixed and do not reoccur.

Related OpenSpec change: fix-scanner-output-quality-issues
"""

import tempfile
from pathlib import Path

from upcast.scanners.concurrency import ConcurrencyScanner
from upcast.scanners.env_vars import EnvVarScanner
from upcast.scanners.http_requests import HttpRequestsScanner


class TestConcurrencyFalsePositives:
    """Regression tests for concurrency scanner false positives."""

    def test_no_false_positive_for_dataclass_process(self):
        """
        Verify that dataclasses named 'Process' are not detected as
        multiprocessing.Process creation.

        Previously reported false positive:
        PlainProcess(name="web", replicas=2) was detected as process creation.
        """
        code = """
from dataclasses import dataclass

@dataclass
class Process:
    name: str
    replicas: int

def create_plain_process():
    # This should NOT be detected as multiprocessing.Process
    return Process(name="web", replicas=2)
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            f.flush()

            scanner = ConcurrencyScanner()
            result = scanner.scan(Path(f.name))

            # Should not detect any process creation
            assert result.results["multiprocessing"].get("process_creation", []) == []

    def test_no_false_positive_for_custom_thread_class(self):
        """
        Verify that custom classes named 'Thread' are not detected as
        threading.Thread creation.
        """
        code = """
class Thread:
    def __init__(self, title: str):
        self.title = title

def create_thread():
    # This should NOT be detected as threading.Thread
    return Thread(title="Discussion")
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            f.flush()

            scanner = ConcurrencyScanner()
            result = scanner.scan(Path(f.name))

            # Should not detect any thread creation
            assert result.results["threading"].get("thread_creation", []) == []

    def test_detects_real_multiprocessing_process(self):
        """Verify that real multiprocessing.Process is still detected."""
        code = """
import multiprocessing

def worker():
    pass

def start_worker():
    p = multiprocessing.Process(target=worker)
    p.start()
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            f.flush()

            scanner = ConcurrencyScanner()
            result = scanner.scan(Path(f.name))

            # Should detect exactly one process creation
            assert len(result.results["multiprocessing"].get("process_creation", [])) == 1
            assert result.results["multiprocessing"]["process_creation"][0].pattern == "process_creation"

    def test_detects_real_threading_thread(self):
        """Verify that real threading.Thread is still detected."""
        code = """
import threading

def worker():
    pass

def start_worker():
    t = threading.Thread(target=worker)
    t.start()
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            f.flush()

            scanner = ConcurrencyScanner()
            result = scanner.scan(Path(f.name))

            # Should detect exactly one thread creation
            assert len(result.results["threading"].get("thread_creation", [])) == 1
            assert result.results["threading"]["thread_creation"][0].pattern == "thread_creation"


class TestEnvVarsFalsePositives:
    """Regression tests for env vars scanner false positives."""

    def test_no_false_positive_for_dict_subscript(self):
        """
        Verify that string literals in dict subscripts are not detected
        as environment variables.

        Previously reported false positive:
        response.data['id'] was reported as env var 'id'
        """
        code = """
def test():
    api_client.post(
        '/api/bkapps/applications/test/config_vars/',
        {'key': 'A1', 'value': 'foo'}
    ).data['id']
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            f.flush()

            scanner = EnvVarScanner()
            result = scanner.scan(Path(f.name))

            # Should not detect 'id' as an env var
            assert "id" not in result.results

    def test_no_false_positive_for_api_path_strings(self):
        """
        Verify that string literals in API paths are not detected
        as environment variables.
        """
        code = """
import requests

def test():
    requests.post(
        '/api/bkapps/applications/test/config_vars/',
        json={'key': 'A1', 'value': 'foo', 'environment_name': '_global_'}
    )
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            f.flush()

            scanner = EnvVarScanner()
            result = scanner.scan(Path(f.name))

            # Should not detect 'environment_name' as an env var from the dict
            # (Note: if there were os.getenv calls, those would be detected)
            # For this test, we expect no env vars detected at all
            assert len(result.results) == 0

    def test_detects_real_env_var_access(self):
        """Verify that real os.environ accesses are still detected."""
        code = """
import os

def get_config():
    db_url = os.environ['DATABASE_URL']
    api_key = os.getenv('API_KEY')
    return db_url, api_key
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            f.flush()

            scanner = EnvVarScanner()
            result = scanner.scan(Path(f.name))

            # Should detect both DATABASE_URL and API_KEY
            assert "DATABASE_URL" in result.results
            assert "API_KEY" in result.results


class TestHttpRequestsQuality:
    """Regression tests for HTTP requests scanner output quality."""

    def test_omits_json_body_when_not_inferrable(self):
        """
        Verify that json_body field is omitted (not set to <dynamic> placeholder)
        when the body cannot be statically inferred.

        Previously, the output contained: json_body: {"<dynamic>": "..."}
        Now it should omit the field entirely.
        """
        code = """
import requests

def api_call(data):
    # data is a variable - cannot be statically inferred
    requests.post('https://example.com/api', json=data)
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            f.flush()

            scanner = HttpRequestsScanner()
            result = scanner.scan(Path(f.name))

            # Should detect one HTTP request
            assert len(result.results) > 0

            # Find the POST request
            post_request = None
            for _url, request_info in result.results.items():
                if request_info.method == "POST":
                    post_request = request_info
                    break

            assert post_request is not None

            # json_body should be None (omitted from output)
            # Check that we have at least one usage
            assert len(post_request.usages) > 0
            usage = post_request.usages[0]
            # json_body should be None, not a dict with "<dynamic>"
            assert usage.json_body is None

    def test_includes_json_body_when_inferrable(self):
        """
        Verify that json_body is included when it can be statically inferred.
        """
        code = """
import requests

def api_call():
    # Literal dict - can be statically inferred
    requests.post('https://example.com/api', json={'username': 'admin', 'password': 'secret'})
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            f.flush()

            scanner = HttpRequestsScanner()
            result = scanner.scan(Path(f.name))

            # Should detect one HTTP request
            assert len(result.results) > 0

            # Find the POST request
            post_request = None
            for _url, request_info in result.results.items():
                if request_info.method == "POST":
                    post_request = request_info
                    break

            assert post_request is not None

            # json_body should contain the literal dict
            assert len(post_request.usages) > 0
            usage = post_request.usages[0]
            assert usage.json_body is not None
            assert usage.json_body.get("username") == "admin"
            assert usage.json_body.get("password") == "secret"
