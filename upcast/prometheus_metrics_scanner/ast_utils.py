"""AST utilities for Prometheus metrics detection."""

from typing import Optional

from astroid import nodes

from upcast.common.ast_utils import infer_value_with_fallback

# Prometheus metric class qualified names
PROMETHEUS_METRIC_CLASSES = {
    "prometheus_client.Counter",
    "prometheus_client.Gauge",
    "prometheus_client.Histogram",
    "prometheus_client.Summary",
    "prometheus_client.metrics.Counter",
    "prometheus_client.metrics.Gauge",
    "prometheus_client.metrics.Histogram",
    "prometheus_client.metrics.Summary",
}

# Prometheus MetricFamily class qualified names
PROMETHEUS_METRIC_FAMILY_CLASSES = {
    "prometheus_client.core.CounterMetricFamily",
    "prometheus_client.core.GaugeMetricFamily",
    "prometheus_client.core.HistogramMetricFamily",
    "prometheus_client.core.SummaryMetricFamily",
}

# Map qualified names to metric types
METRIC_TYPE_MAP = {
    "prometheus_client.Counter": "counter",
    "prometheus_client.Gauge": "gauge",
    "prometheus_client.Histogram": "histogram",
    "prometheus_client.Summary": "summary",
    "prometheus_client.metrics.Counter": "counter",
    "prometheus_client.metrics.Gauge": "gauge",
    "prometheus_client.metrics.Histogram": "histogram",
    "prometheus_client.metrics.Summary": "summary",
    "prometheus_client.core.CounterMetricFamily": "counter",
    "prometheus_client.core.GaugeMetricFamily": "gauge",
    "prometheus_client.core.HistogramMetricFamily": "histogram",
    "prometheus_client.core.SummaryMetricFamily": "summary",
}


def is_prometheus_metric_call(call: nodes.Call) -> Optional[str]:
    """Check if call instantiates a Prometheus metric.

    Args:
        call: The Call node to check

    Returns:
        Metric type ('counter', 'gauge', 'histogram', 'summary') or None
    """
    try:
        # Try type inference first
        inferred_list = list(call.func.infer())
        for inferred in inferred_list:
            if hasattr(inferred, "qname"):
                qname = inferred.qname()
                if qname in METRIC_TYPE_MAP:
                    return METRIC_TYPE_MAP[qname]
    except Exception:  # noqa: S110
        pass

    # Fallback: pattern matching
    try:
        func_str = call.func.as_string()
        return _match_metric_pattern(func_str)
    except Exception:  # noqa: S110
        pass

    return None


def _match_metric_pattern(func_str: str) -> Optional[str]:
    """Match function string against known metric patterns.

    Args:
        func_str: Function string to match

    Returns:
        Metric type or None
    """
    # Only match prometheus_client module patterns
    metric_patterns = {
        "prometheus_client.Counter": "counter",
        "prometheus_client.Gauge": "gauge",
        "prometheus_client.Histogram": "histogram",
        "prometheus_client.Summary": "summary",
    }

    for pattern, metric_type in metric_patterns.items():
        if func_str == pattern or (func_str.endswith("." + pattern.split(".")[-1]) and "prometheus_client" in func_str):
            return metric_type

    return None


def extract_metric_name(call: nodes.Call) -> Optional[str]:
    """Extract metric name from a metric instantiation call.

    Args:
        call: The Call node

    Returns:
        Metric name or None
    """
    try:
        # First positional argument is the metric name
        if call.args and len(call.args) > 0:
            name_arg = call.args[0]
            if isinstance(name_arg, nodes.Const) and isinstance(name_arg.value, str):
                return name_arg.value

            # Use common inference with fallback
            inferred_value, success = infer_value_with_fallback(name_arg)
            return inferred_value
    except Exception:  # noqa: S110
        pass

    return None


def extract_help_text(call: nodes.Call) -> Optional[str]:
    """Extract help text from a metric instantiation call.

    Args:
        call: The Call node

    Returns:
        Help text or None
    """
    try:
        # Second positional argument is the help text
        if call.args and len(call.args) > 1:
            help_arg = call.args[1]
            if isinstance(help_arg, nodes.Const) and isinstance(help_arg.value, str):
                return help_arg.value

            # Use common inference with fallback
            inferred_value, success = infer_value_with_fallback(help_arg)
            if success and isinstance(inferred_value, str):
                return inferred_value
    except Exception:  # noqa: S110
        pass

    return None


def extract_labels(call: nodes.Call) -> list[str]:
    """Extract label names from a metric instantiation call.

    Args:
        call: The Call node

    Returns:
        List of label names (empty if none)
    """
    labels = []

    try:
        # Check third positional argument (labelnames as list)
        if call.args and len(call.args) > 2:
            labels_arg = call.args[2]
            labels = _extract_labels_from_node(labels_arg)
            if labels:
                return labels

        # Check 'labelnames' keyword argument
        for keyword in call.keywords:
            if keyword.arg == "labelnames":
                labels = _extract_labels_from_node(keyword.value)
                if labels:
                    return labels

        # Check 'labels' keyword argument (for MetricFamily)
        for keyword in call.keywords:
            if keyword.arg == "labels":
                labels = _extract_labels_from_node(keyword.value)
                if labels:
                    return labels
    except Exception:  # noqa: S110
        pass

    return labels


def _extract_labels_from_node(node: nodes.NodeNG) -> list[str]:
    """Extract string list from a node.

    Args:
        node: Node to extract from

    Returns:
        List of strings
    """
    labels = []

    try:
        # Handle list literal
        if isinstance(node, nodes.List):
            for elt in node.elts:
                if isinstance(elt, nodes.Const) and isinstance(elt.value, str):
                    labels.append(elt.value)
            return labels

        # Try to infer the value
        inferred_list = list(node.infer())
        if len(inferred_list) == 1:
            inferred = inferred_list[0]
            if isinstance(inferred, nodes.List):
                for elt in inferred.elts:
                    if isinstance(elt, nodes.Const) and isinstance(elt.value, str):
                        labels.append(elt.value)
    except Exception:  # noqa: S110
        pass

    return labels


def is_custom_collector_class(classdef: nodes.ClassDef) -> bool:
    """Check if a class is a custom Prometheus collector.

    Args:
        classdef: The ClassDef node to check

    Returns:
        True if the class has a collect() method
    """
    try:
        for item in classdef.body:
            if isinstance(item, nodes.FunctionDef) and item.name == "collect":
                return True
    except Exception:  # noqa: S110
        pass

    return False


def is_metric_family_call(call: nodes.Call) -> Optional[str]:
    """Check if call instantiates a Prometheus MetricFamily.

    Args:
        call: The Call node to check

    Returns:
        Metric type ('counter', 'gauge', 'histogram', 'summary') or None
    """
    try:
        # Try type inference first
        inferred_list = list(call.func.infer())
        for inferred in inferred_list:
            if hasattr(inferred, "qname"):
                qname = inferred.qname()
                if qname in METRIC_TYPE_MAP:
                    return METRIC_TYPE_MAP[qname]
    except Exception:  # noqa: S110
        pass

    # Fallback: pattern matching
    try:
        func_str = call.func.as_string()
        return _match_metric_family_pattern(func_str)
    except Exception:  # noqa: S110
        pass

    return None


def _match_metric_family_pattern(func_str: str) -> Optional[str]:
    """Match function string against MetricFamily patterns.

    Args:
        func_str: Function string to match

    Returns:
        Metric type or None
    """
    metric_family_patterns = {
        "CounterMetricFamily": "counter",
        "GaugeMetricFamily": "gauge",
        "HistogramMetricFamily": "histogram",
        "SummaryMetricFamily": "summary",
    }

    for pattern, metric_type in metric_family_patterns.items():
        if pattern in func_str:
            return metric_type

    return None
