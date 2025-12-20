# Design: implement-prometheus-metrics-scanner

## Architecture Overview

The Prometheus metrics scanner follows the established three-layer architecture pattern used by `django_model_scanner` and `env_var_scanner`:

```
┌─────────────────────────────────────────────────────────────┐
│ CLI Layer (cli.py)                                          │
│ - scan_prometheus_metrics(path, output, verbose)           │
│ - File discovery and orchestration                          │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ Checker Layer (checker.py)                                  │
│ - PrometheusMetricsChecker: AST visitor                    │
│ - Aggregates metrics across files                          │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│ Parser Layer (metrics_parser.py)                           │
│ - parse_metric_instantiation(): Extract metric definitions │
│ - parse_metric_decorator(): Detect @metric decorators      │
│ - parse_custom_collector(): Parse MetricFamily classes     │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
┌────────▼────────┐    ┌────────▼────────┐
│ AST Utils       │    │ Export          │
│ (ast_utils.py)  │    │ (export.py)     │
│ - Pattern       │    │ - YAML output   │
│   detection     │    │ - Formatting    │
└─────────────────┘    └─────────────────┘
```

## Core Detection Patterns

### 1. Metric Instantiation

**Pattern**: Direct metric object creation

```python
from prometheus_client import Counter, Gauge, Histogram, Summary

counter = Counter('metric_name', 'Help text', ['label1', 'label2'])
gauge = Gauge('metric_name', 'Help text')
histogram = Histogram('metric_name', 'Help text', buckets=[1, 2, 5, 10])
summary = Summary('metric_name', 'Help text')
```

**Detection Strategy**:

- Use `astroid.infer()` to resolve Call node function to prometheus_client classes
- Extract positional args: name (required), documentation (optional), labelnames (optional)
- Extract keyword args: labelnames, namespace, subsystem, unit, registry, buckets

**Implementation**:

```python
def _is_prometheus_metric_call(call: nodes.Call) -> Optional[str]:
    """Check if call instantiates a Prometheus metric.

    Returns:
        Metric type ('counter', 'gauge', 'histogram', 'summary') or None
    """
    # Use astroid inference to resolve the function
    for inferred in call.func.infer():
        if hasattr(inferred, 'qname'):
            qname = inferred.qname()
            if qname in PROMETHEUS_METRIC_CLASSES:
                return METRIC_TYPE_MAP[qname]
    return None
```

### 2. Decorator Pattern

**Pattern**: Metrics used as function decorators

```python
CALLS = Counter('function_calls_total', '函数调用次数')

@CALLS.count_exceptions()
def foo():
    ...

@REQUEST_TIME.time()
def process_request():
    ...
```

**Detection Strategy**:

- Identify FunctionDef nodes with decorators
- Resolve decorator Call nodes to metric instance attributes
- Track back to original metric definition using variable references

**Challenges**:

- Decorators may reference variables defined elsewhere
- Need to track variable assignments and cross-reference them
- May require second-pass aggregation like abstract field merging

### 3. Custom Collectors

**Pattern**: Custom metric families for dynamic metrics

```python
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily

class MyCollector:
    def collect(self):
        g = GaugeMetricFamily(
            'my_dynamic_metric',
            '动态计算的指标',
            labels=['type']
        )
        g.add_metric(['a'], 1)
        yield g
```

**Detection Strategy**:

- Detect classes with `collect()` method
- Parse MetricFamily instantiations within collect()
- Mark these metrics as `custom_collector: true`
- Track REGISTRY.register(collector) calls

### 4. Metric Operations (Usage Tracking)

**Pattern**: Increment, set, observe operations

```python
counter.inc()
counter.labels(method='GET').inc(2)
gauge.set(42)
histogram.observe(0.5)
```

**Detection Strategy** (Optional - for usage tracking):

- Detect attribute access on metric variables (`.inc()`, `.set()`, `.observe()`)
- Track `.labels()` calls to validate label names match definition
- Record usage locations separately from definitions

## Data Model

### MetricInfo Structure

```python
@dataclass
class MetricInfo:
    name: str                    # Metric name
    type: str                    # counter, gauge, histogram, summary
    help: Optional[str]          # Help/documentation text
    labels: list[str]            # Label names
    namespace: Optional[str]     # Namespace prefix
    subsystem: Optional[str]     # Subsystem prefix
    unit: Optional[str]          # Unit suffix (_bytes, _seconds, etc.)
    custom_collector: bool       # True if MetricFamily-based
    buckets: Optional[list]      # For histograms
    usages: list[UsageInfo]      # All usage locations

@dataclass
class UsageInfo:
    location: str                # file:line
    pattern: str                 # instantiation, decorator, custom_collector, increment
    statement: str               # Source code line
```

### Aggregation Strategy

Similar to `env_var_scanner`, aggregate by metric name:

1. **First pass**: Collect all metric definitions and usages
2. **Aggregation**: Group by metric name (handle namespace/subsystem prefixes)
3. **Validation**: Check for conflicts (same name, different type/labels)
4. **Output**: Generate YAML with aggregated information

## AST Traversal Strategy

### PrometheusMetricsChecker

```python
class PrometheusMetricsChecker:
    def __init__(self, base_path: str):
        self.metrics: dict[str, MetricInfo] = {}
        self.metric_variables: dict[str, str] = {}  # var_name -> metric_name
        self.base_path = base_path

    def check_file(self, file_path: str) -> None:
        """Process a single file."""
        module = MANAGER.ast_from_file(file_path)

        # First pass: Find metric instantiations
        for assign in module.nodes_of_class(nodes.Assign):
            metric_info = parse_metric_assignment(assign)
            if metric_info:
                self._register_metric(metric_info, file_path, assign)

        # Second pass: Find decorators
        for funcdef in module.nodes_of_class(nodes.FunctionDef):
            decorator_usages = parse_metric_decorators(funcdef)
            for usage in decorator_usages:
                self._add_usage(usage)

        # Third pass: Find custom collectors
        for classdef in module.nodes_of_class(nodes.ClassDef):
            collector_metrics = parse_custom_collector(classdef)
            for metric_info in collector_metrics:
                self._register_metric(metric_info, file_path, classdef)
```

## Import Resolution

Handle various import patterns:

```python
# Direct import
from prometheus_client import Counter
counter = Counter('name', 'help')

# Module import
import prometheus_client
counter = prometheus_client.Counter('name', 'help')

# Aliased import
from prometheus_client import Counter as C
counter = C('name', 'help')

# Import from core
from prometheus_client.core import GaugeMetricFamily
```

**Strategy**: Use astroid's inference engine to resolve qualified names, similar to `_extract_field_type()` in django_model_scanner.

## Edge Cases & Error Handling

### Name Resolution Failures

```python
# Dynamic metric name - cannot resolve
metric_name = get_config('metric_name')
counter = Counter(metric_name, 'help')
```

**Handling**: Fall back to `.as_string()` representation, mark as `unresolved_name: true`

### Label Mismatch Detection

```python
counter = Counter('requests', 'help', ['method', 'path'])
counter.labels(method='GET', status=200).inc()  # 'status' not in labels!
```

**Handling**: Optionally validate labels in usage against definition (can be validation warning)

### Multiprocess Mode

```python
from prometheus_client import multiprocess
# Special handling required
```

**Handling**: Initial version skips, add in future iteration

## Testing Strategy

### Test Structure

```
tests/test_prometheus_metrics_scanner/
├── __init__.py
├── test_ast_utils.py          # Pattern detection tests
├── test_metrics_parser.py     # Metric parsing tests
├── test_checker.py            # Checker aggregation tests
├── test_cli.py                # CLI integration tests
├── test_export.py             # YAML output tests
└── fixtures/                  # Sample Python files
    ├── simple_metrics.py      # Basic counter/gauge/histogram
    ├── decorators.py          # Decorator patterns
    ├── custom_collectors.py   # MetricFamily patterns
    └── complex.py             # Mixed patterns
```

### Test Coverage Requirements

- **Pattern detection**: Test all metric types and import variants
- **Parser**: Test extraction of name, help, labels, special args
- **Aggregation**: Test multi-file metric aggregation
- **Edge cases**: Dynamic names, missing help, zero labels
- **Export**: Test YAML structure and formatting

## Performance Considerations

### File Filtering

Only scan Python files, skip:

- Virtual environments (`venv/`, `.venv/`, `env/`)
- Build directories (`build/`, `dist/`, `.eggs/`)
- Cache directories (`__pycache__/`, `.pytest_cache/`)

### Lazy Parsing

Parse files only when needed, use astroid's caching when available.

### Memory Management

For large codebases (1000+ files), process files in batches to avoid memory issues.

## Future Enhancements

1. **Label validation**: Warn when labels used don't match definition
2. **Metric naming conventions**: Validate against Prometheus best practices
3. **Duplicate detection**: Warn when same metric defined multiple times
4. **Registry tracking**: Track which REGISTRY metrics belong to
5. **OpenMetrics support**: Detect exemplar usage
6. **Grafana integration**: Generate Grafana dashboard JSON from metrics
