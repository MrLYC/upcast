"""Metric parsing and data structures."""

from dataclasses import dataclass, field
from typing import Any, Optional

from astroid import nodes

from upcast.prometheus_metrics_scanner.ast_utils import (
    extract_help_text,
    extract_labels,
    extract_metric_name,
    is_custom_collector_class,
    is_metric_family_call,
    is_prometheus_metric_call,
)


@dataclass
class UsageInfo:
    """Information about a single usage of a metric."""

    location: str  # file:line
    pattern: str  # instantiation, decorator, custom_collector, increment, etc.
    statement: str  # Source code line


@dataclass
class MetricInfo:
    """Complete information about a Prometheus metric."""

    name: str  # Original metric name from definition
    type: str  # counter, gauge, histogram, summary
    help: Optional[str]
    labels: list[str]
    namespace: Optional[str] = None
    subsystem: Optional[str] = None
    unit: Optional[str] = None
    custom_collector: bool = False
    buckets: Optional[list] = None
    usages: list[UsageInfo] = field(default_factory=list)

    def get_full_name(self) -> str:
        """Get the full metric name with namespace and subsystem.

        Returns:
            Full metric name (e.g., 'namespace_subsystem_name')
        """
        parts = []
        if self.namespace:
            parts.append(self.namespace)
        if self.subsystem:
            parts.append(self.subsystem)
        parts.append(self.name)
        return "_".join(parts)


def parse_metric_instantiation(
    assign: nodes.Assign,
    file_path: str,
    line_number: int,
) -> Optional[MetricInfo]:
    """Parse a metric instantiation from an assignment node.

    Args:
        assign: The Assign node
        file_path: Path to the file being parsed
        line_number: Line number of the assignment

    Returns:
        MetricInfo if this is a metric instantiation, None otherwise
    """
    try:
        # Check if this is a Call node
        if not isinstance(assign.value, nodes.Call):
            return None

        # Check if this is a Prometheus metric
        metric_type = is_prometheus_metric_call(assign.value)
        if not metric_type:
            return None

        # Extract metric name
        name = extract_metric_name(assign.value)
        if not name:
            return None

        # Extract help text
        help_text = extract_help_text(assign.value)

        # Extract labels
        labels = extract_labels(assign.value)

        # Extract optional parameters
        namespace = _extract_keyword_arg(assign.value, "namespace")
        subsystem = _extract_keyword_arg(assign.value, "subsystem")
        unit = _extract_keyword_arg(assign.value, "unit")
        buckets = _extract_buckets(assign.value)

        # Create usage info
        statement = assign.as_string()
        usage = UsageInfo(
            location=f"{file_path}:{line_number}",
            pattern="instantiation",
            statement=statement,
        )

        # Create MetricInfo
        metric_info = MetricInfo(
            name=name,
            type=metric_type,
            help=help_text,
            labels=labels,
            namespace=namespace,
            subsystem=subsystem,
            unit=unit,
            buckets=buckets,
            usages=[usage],
        )
    except Exception:
        return None
    else:
        return metric_info


def _extract_keyword_arg(call: nodes.Call, arg_name: str) -> Optional[str]:
    """Extract a string keyword argument from a call.

    Args:
        call: The Call node
        arg_name: Name of the keyword argument

    Returns:
        String value or None
    """
    try:
        for keyword in call.keywords:
            if keyword.arg == arg_name:
                if isinstance(keyword.value, nodes.Const) and isinstance(keyword.value.value, str):
                    return keyword.value.value

                # Try to infer
                try:
                    inferred_list = list(keyword.value.infer())
                    if len(inferred_list) == 1:
                        inferred = inferred_list[0]
                        if isinstance(inferred, nodes.Const) and isinstance(inferred.value, str):
                            return inferred.value
                except Exception:  # noqa: S110
                    pass
    except Exception:  # noqa: S110
        pass

    return None


def _extract_list_from_node(node: nodes.NodeNG) -> Optional[list[Any]]:
    """Extract list of constant values from a node.

    Args:
        node: The node to extract from

    Returns:
        List of values or None
    """
    if isinstance(node, nodes.List):
        buckets = []
        for elt in node.elts:
            if isinstance(elt, nodes.Const):
                buckets.append(elt.value)
        return buckets if buckets else None
    return None


def _extract_buckets(call: nodes.Call) -> Optional[list[Any]]:
    """Extract buckets parameter for Histogram metrics.

    Args:
        call: The Call node

    Returns:
        List of bucket values or None
    """
    try:
        for keyword in call.keywords:
            if keyword.arg == "buckets":
                # Try direct list extraction
                result = _extract_list_from_node(keyword.value)
                if result:
                    return result

                # Try inference
                try:
                    inferred_list = list(keyword.value.infer())
                    if len(inferred_list) == 1:
                        return _extract_list_from_node(inferred_list[0])
                except Exception:  # noqa: S110
                    pass
    except Exception:  # noqa: S110
        pass

    return None


def parse_metric_decorator(funcdef: nodes.FunctionDef, file_path: str) -> list[UsageInfo]:
    """Parse metric decorator usage from a function definition.

    Args:
        funcdef: The FunctionDef node
        file_path: Path to the file being parsed

    Returns:
        List of UsageInfo for decorator usages
    """
    usages = []

    try:
        for decorator in funcdef.decorator_list:
            # Check if decorator is a call (e.g., @counter.count_exceptions())
            if isinstance(decorator, nodes.Call):
                # Get the statement
                statement = decorator.as_string()
                usage = UsageInfo(
                    location=f"{file_path}:{decorator.lineno}",
                    pattern="decorator",
                    statement=statement,
                )
                usages.append(usage)
    except Exception:  # noqa: S110
        pass

    return usages


def parse_custom_collector(classdef: nodes.ClassDef, file_path: str) -> list[MetricInfo]:
    """Parse metrics from a custom collector class.

    Args:
        classdef: The ClassDef node
        file_path: Path to the file being parsed

    Returns:
        List of MetricInfo for metrics defined in the collector
    """
    metrics = []

    try:
        if not is_custom_collector_class(classdef):
            return metrics

        # Find the collect method
        for item in classdef.body:
            if isinstance(item, nodes.FunctionDef) and item.name == "collect":
                # Parse all assignments in collect()
                for assign in item.nodes_of_class(nodes.Assign):
                    if not isinstance(assign.value, nodes.Call):
                        continue

                    # Check if this is a MetricFamily call
                    metric_type = is_metric_family_call(assign.value)
                    if not metric_type:
                        continue

                    # Extract metric name
                    name = extract_metric_name(assign.value)
                    if not name:
                        continue

                    # Extract help text
                    help_text = extract_help_text(assign.value)

                    # Extract labels
                    labels = extract_labels(assign.value)

                    # Create usage info
                    statement = assign.as_string()
                    usage = UsageInfo(
                        location=f"{file_path}:{assign.lineno}",
                        pattern="custom_collector",
                        statement=statement,
                    )

                    # Create MetricInfo
                    metric_info = MetricInfo(
                        name=name,
                        type=metric_type,
                        help=help_text,
                        labels=labels,
                        custom_collector=True,
                        usages=[usage],
                    )

                    metrics.append(metric_info)
    except Exception:  # noqa: S110
        pass

    return metrics
