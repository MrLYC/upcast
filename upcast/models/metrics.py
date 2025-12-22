"""Data models for Prometheus metrics scanner."""

from pydantic import BaseModel, Field

from upcast.models.base import ScannerOutput, ScannerSummary


class MetricUsage(BaseModel):
    """A usage of a metric.

    Attributes:
        location: Location in 'file:line' format
        pattern: Usage pattern (e.g., counter.inc())
        statement: Code statement
    """

    location: str = Field(..., description="file:line format")
    pattern: str = Field(..., description="Usage pattern")
    statement: str = Field(..., description="Code statement")


class MetricInfo(BaseModel):
    """Information about a Prometheus metric.

    Attributes:
        name: Metric name
        type: Metric type (Counter, Gauge, Histogram, Summary)
        help: Metric help text
        labels: Label names
        namespace: Metric namespace
        subsystem: Metric subsystem
        unit: Metric unit
        custom_collector: Whether it's a custom collector
        buckets: Histogram buckets
        usages: List of metric usages
    """

    name: str = Field(..., description="Metric name")
    type: str = Field(..., description="Metric type (Counter, Gauge, Histogram, Summary)")
    help: str = Field(..., description="Metric help text")
    labels: list[str] = Field(default_factory=list, description="Label names")
    namespace: str | None = Field(None, description="Metric namespace")
    subsystem: str | None = Field(None, description="Metric subsystem")
    unit: str | None = Field(None, description="Metric unit")
    custom_collector: bool = Field(..., description="Custom collector")
    buckets: list[float] | None = Field(None, description="For Histogram")
    usages: list[MetricUsage] = Field(default_factory=list, description="Metric usages")


class PrometheusMetricSummary(ScannerSummary):
    """Summary statistics for Prometheus metrics.

    Attributes:
        total_metrics: Total number of metrics
        by_type: Count by metric type
    """

    total_metrics: int = Field(..., ge=0, description="Total metrics")
    by_type: dict[str, int] = Field(default_factory=dict, description="Count by type")


class PrometheusMetricOutput(ScannerOutput[dict[str, MetricInfo]]):
    """Complete output from Prometheus metrics scanner.

    Attributes:
        summary: Summary statistics
        results: Metrics keyed by metric name
    """

    summary: PrometheusMetricSummary
    results: dict[str, MetricInfo] = Field(..., description="Metrics")
