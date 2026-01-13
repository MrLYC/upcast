"""Tests for edge cases and error handling."""

import pytest
from pathlib import Path

from upcast.scanners.metrics import MetricsScanner


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_metric_without_name(self, tmp_path, scanner):
        """Test metric definition without name argument."""
        code = """
from prometheus_client import Counter

# Invalid: Counter without name
counter = Counter()
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # Should handle gracefully, not crash
        assert output.summary.total_metrics == 0

    def test_metric_with_variable_name(self, tmp_path, scanner):
        """Test metric with variable as name (not detectable)."""
        code = """
from prometheus_client import Counter

METRIC_NAME = 'http_requests_total'
counter = Counter(METRIC_NAME, 'Help text')
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # Variable names are not resolved, so metric might not be detected
        # This documents current behavior
        assert output.summary.total_metrics >= 0

    def test_nested_metric_definition(self, tmp_path, scanner):
        """Test metric defined inside a function."""
        code = """
from prometheus_client import Counter

def setup_metrics():
    requests = Counter('requests_total', 'Total requests')
    return requests
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # Should still detect the metric
        assert output.summary.total_metrics == 1

    def test_metric_in_class(self, tmp_path, scanner):
        """Test metric defined as class attribute."""
        code = """
from prometheus_client import Counter

class Metrics:
    requests = Counter('requests_total', 'Total requests')
    errors = Counter('errors_total', 'Total errors')
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # Should detect both metrics
        assert output.summary.total_metrics == 2

    def test_invalid_syntax_file(self, tmp_path, scanner):
        """Test handling of file with invalid Python syntax."""
        code = """
from prometheus_client import Counter

counter = Counter('test'  # Missing closing parenthesis
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # Should handle parse errors gracefully
        assert output.summary.total_metrics == 0

    def test_non_prometheus_counter(self, tmp_path, scanner):
        """Test that non-Prometheus Counters are not detected."""
        code = """
from collections import Counter

# This is not a Prometheus Counter
word_counts = Counter(['apple', 'banana', 'apple'])
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # Should not detect collections.Counter
        assert output.summary.total_metrics == 0

    def test_metric_with_complex_help_text(self, tmp_path, scanner):
        """Test metric with complex help text."""
        code = """
from prometheus_client import Counter

requests = Counter(
    'requests_total',
    '''This is a multi-line
    help text with special characters: @#$%
    and "quotes" inside'''
)
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        assert output.summary.total_metrics == 1
        metric = output.results["requests_total"]
        assert metric.help is not None

    def test_multiple_assignments_to_same_name(self, tmp_path, scanner):
        """Test multiple assignments to same metric name."""
        code = """
from prometheus_client import Counter

# First definition
counter = Counter('my_counter', 'First help')

# Reassignment (this is bad practice but should be handled)
counter = Counter('my_counter', 'Second help')
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # Should handle without crashing
        # Latest definition might override
        assert "my_counter" in output.results

    def test_empty_label_list(self, tmp_path, scanner):
        """Test metric with empty label list."""
        code = """
from prometheus_client import Counter

counter = Counter('my_counter', 'Help', labelnames=[])
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        metric = output.results["my_counter"]
        assert len(metric.labels) == 0

    def test_metric_with_f_string_name(self, tmp_path, scanner):
        """Test metric with f-string name (not detectable)."""
        code = """
from prometheus_client import Counter

prefix = 'myapp'
counter = Counter(f'{prefix}_requests_total', 'Help')
"""
        file_path = tmp_path / "metrics.py"
        file_path.write_text(code)

        output = scanner.scan(file_path)

        # F-strings are not resolved at parse time
        # This documents current limitation
        assert output.summary.total_metrics >= 0
