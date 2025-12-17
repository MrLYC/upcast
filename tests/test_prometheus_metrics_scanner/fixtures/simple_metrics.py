"""Simple Prometheus metrics examples for testing."""

import prometheus_client
from prometheus_client import Counter, Gauge, Histogram, Summary

# Basic Counter
http_requests_total = Counter("http_requests_total", "HTTP 请求总数", ["method", "path", "status"])

# Gauge without labels
memory_usage_bytes = Gauge("memory_usage_bytes", "Memory usage in bytes")

# Histogram with buckets
request_duration_seconds = Histogram(
    "request_duration_seconds", "Request duration in seconds", buckets=[0.1, 0.5, 1.0, 2.5, 5.0]
)

# Summary
response_size_bytes = Summary("response_size_bytes", "Response size in bytes")

# Counter with namespace and subsystem
api_errors = Counter("errors", "API errors", ["error_type"], namespace="api", subsystem="http")

# Metric without help text (edge case)
simple_counter = Counter("simple_counter")

# Module import style
module_style_counter = prometheus_client.Counter("module_style_counter", "Counter using module import")
