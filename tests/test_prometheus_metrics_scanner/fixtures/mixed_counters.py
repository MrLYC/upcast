"""Test fixture mixing Prometheus and non-Prometheus Counter usage."""

from collections import Counter

from prometheus_client import Counter as PrometheusCounter

# This should NOT be detected
word_counts = Counter(["hello", "world", "hello"])

# This SHOULD be detected as Prometheus metric
http_requests = PrometheusCounter(
    "http_requests_total",
    "Total HTTP requests",
    ["method"],
)

# This should NOT be detected
char_frequency = Counter("abcabc")
