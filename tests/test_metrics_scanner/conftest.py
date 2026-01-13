"""Pytest fixtures for metrics scanner tests."""

import pytest
from pathlib import Path

from upcast.scanners.metrics import MetricsScanner


@pytest.fixture
def scanner():
    """Create a MetricsScanner instance."""
    return MetricsScanner(verbose=False)


@pytest.fixture
def counter_metric():
    """Simple Counter metric definition."""
    return """
from prometheus_client import Counter

requests_total = Counter('http_requests_total', 'Total HTTP requests')
"""


@pytest.fixture
def gauge_metric():
    """Simple Gauge metric definition."""
    return """
from prometheus_client import Gauge

active_users = Gauge('active_users', 'Number of active users')
"""


@pytest.fixture
def histogram_metric():
    """Simple Histogram metric definition."""
    return """
from prometheus_client import Histogram

request_duration = Histogram('request_duration_seconds', 'Request duration in seconds')
"""


@pytest.fixture
def summary_metric():
    """Simple Summary metric definition."""
    return """
from prometheus_client import Summary

response_size = Summary('response_size_bytes', 'Response size in bytes')
"""


@pytest.fixture
def metric_with_labels():
    """Metric with labels."""
    return """
from prometheus_client import Counter

requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    labelnames=['method', 'endpoint', 'status']
)
"""


@pytest.fixture
def multiple_metrics():
    """Multiple metrics in one file."""
    return """
from prometheus_client import Counter, Gauge, Histogram

requests_total = Counter('http_requests_total', 'Total requests')
active_connections = Gauge('active_connections', 'Active connections')
request_duration = Histogram('request_duration_seconds', 'Request duration')
"""
