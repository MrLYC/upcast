# Proposal: implement-prometheus-metrics-scanner

## What

Implement a new scanner module `prometheus_metrics_scanner` to detect and analyze Prometheus metrics defined in Python codebases using `prometheus_client` library, outputting structured YAML documentation similar to existing scanners.

## Why

Observability is critical for production systems. Prometheus metrics provide runtime insights into application behavior, but these metrics are scattered across codebases and often poorly documented. Teams need:

1. **Centralized metrics inventory**: Know what metrics exist and where they're defined
2. **Label validation**: Ensure consistent label usage across metric instances
3. **Documentation generation**: Auto-generate metrics documentation for operations teams
4. **Migration assistance**: Track metrics when migrating between monitoring systems

Following the established pattern of `django_model_scanner` and `env_var_scanner`, this scanner provides automated discovery and documentation of Prometheus metrics using astroid-based AST analysis.

## How

### Core Approach

Use astroid to parse Python files and detect prometheus_client usage patterns:

1. **Metric instantiation detection**: Counter, Gauge, Histogram, Summary
2. **Decorator pattern detection**: @counter.count_exceptions(), @histogram.time()
3. **Custom collector detection**: GaugeMetricFamily, CounterMetricFamily
4. **REGISTRY registration tracking**: Explicit REGISTRY.register() calls

### Module Structure

```
upcast/prometheus_metrics_scanner/
├── __init__.py           # Public API exports
├── cli.py                # scan_prometheus_metrics() entry point
├── checker.py            # PrometheusMetricsChecker visitor
├── metrics_parser.py     # Metric extraction and parsing logic
├── ast_utils.py          # Pattern detection utilities
└── export.py             # YAML formatting and output
```

### Output Format

```yaml
http_requests_total:
  type: counter
  help: "HTTP 请求总数"
  labels: [method, path, status]
  usages:
    - location: "api/views.py:15"
      pattern: instantiation
      statement: "Counter('http_requests_total', 'HTTP 请求总数', ['method', 'path', 'status'])"
    - location: "api/middleware.py:42"
      pattern: increment
      statement: "http_requests_total.labels(method='GET', path='/api').inc()"

function_calls_total:
  type: counter
  help: "函数调用次数"
  labels: []
  usages:
    - location: "core/utils.py:8"
      pattern: decorator
      statement: "@CALLS.count_exceptions()"

my_dynamic_metric:
  type: gauge
  help: "动态计算的指标"
  labels: [type]
  custom_collector: true
  usages:
    - location: "metrics/collectors.py:23"
      pattern: custom_collector
      statement: "GaugeMetricFamily('my_dynamic_metric', '动态计算的指标', labels=['type'])"
```

## Impact

### New Files

- `upcast/prometheus_metrics_scanner/*.py` (6 files)
- `tests/test_prometheus_metrics_scanner/*.py` (5 test files)
- `openspec/specs/prometheus-metrics-scanner/spec.md`

### Modified Files

- `upcast/main.py`: Add CLI command registration (if centralized CLI exists)
- `pyproject.toml`: Add prometheus_client as test dependency (for fixtures)
- `README.md`: Document new scanner capability

### Dependencies

- Reuse existing `astroid` dependency (already in project)
- Add `prometheus_client` as dev/test dependency for creating test fixtures

### Backward Compatibility

No breaking changes. Pure addition of new functionality following established patterns.

## Alternatives Considered

1. **Static regex parsing**: Rejected because it cannot handle aliased imports or complex expressions
2. **Runtime instrumentation**: Rejected because it requires running the application and cannot detect unused metrics
3. **prometheus_client introspection**: Rejected because it only works at runtime and misses unregistered metrics

## Open Questions

1. **Registry tracking**: Should we track which REGISTRY each metric belongs to? (Default: REGISTRY)
2. **Metric renaming detection**: Should we detect when metrics are wrapped or renamed?
3. **Multi-process mode**: Should we detect prometheus_client.multiprocess patterns?
4. **Exemplar support**: Should we track OpenMetrics exemplar usage?

**Recommendation**: Start with basic patterns (instantiation, decorators, custom collectors) and extend based on user feedback.

## Success Criteria

- [ ] Detect all 4 core metric types (Counter, Gauge, Histogram, Summary)
- [ ] Extract metric names, help text, and label names
- [ ] Detect decorator patterns (@counter.count_exceptions, @histogram.time)
- [ ] Detect custom collectors (GaugeMetricFamily, etc.)
- [ ] Output structured YAML matching examples
- [ ] 90%+ test coverage following project patterns
- [ ] CLI integration: `python -m upcast.prometheus_metrics_scanner <path>`
- [ ] Documentation with usage examples
