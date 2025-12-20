"""Custom collector examples for testing."""

from prometheus_client.core import (
    CounterMetricFamily,
    GaugeMetricFamily,
    HistogramMetricFamily,
)


class MyCollector:
    """Custom Prometheus collector."""

    def collect(self):
        """Collect metrics dynamically."""
        # GaugeMetricFamily
        g = GaugeMetricFamily("my_dynamic_metric", "动态计算的指标", labels=["type"])
        g.add_metric(["a"], 1)
        g.add_metric(["b"], 2)
        yield g

        # CounterMetricFamily
        c = CounterMetricFamily("my_counter", "A dynamic counter")
        c.add_metric([], 42)
        yield c


class AnotherCollector:
    """Another custom collector."""

    def collect(self):
        """Collect histogram metrics."""
        h = HistogramMetricFamily("my_histogram", "A dynamic histogram", labels=["endpoint"])
        h.add_metric(["api"], buckets=[(0.1, 5), (0.5, 10)], sum_value=15.5)
        yield h
