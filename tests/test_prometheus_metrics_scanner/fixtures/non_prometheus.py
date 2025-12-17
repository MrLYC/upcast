"""Test fixture with non-Prometheus Counter to verify strict matching."""

from collections import Counter

# This should NOT be detected as a Prometheus metric
word_counts = Counter(["apple", "banana", "apple"])

# This should NOT be detected as a Prometheus metric
letter_frequency = Counter("hello world")
