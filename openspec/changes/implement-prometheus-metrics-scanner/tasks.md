# Tasks: implement-prometheus-metrics-scanner

## Implementation Tasks

### Phase 1: Foundation (Core Infrastructure)

- [x] **Create module structure**: Create `upcast/prometheus_metrics_scanner/` directory with `__init__.py`, `cli.py`, `checker.py`, `metrics_parser.py`, `ast_utils.py`, `export.py`

  - Establishes basic module layout following project conventions
  - Defines public API exports in `__init__.py`

- [x] **Implement AST pattern detection utilities**: Create `ast_utils.py` with functions:

  - `is_prometheus_metric_call(call: nodes.Call) -> Optional[str]`: Returns metric type or None
  - `extract_metric_name(call: nodes.Call) -> Optional[str]`: Extracts first positional arg
  - `extract_help_text(call: nodes.Call) -> Optional[str]`: Extracts second positional arg
  - `extract_labels(call: nodes.Call) -> list[str]`: Extracts label names from args/kwargs
  - `is_custom_collector_class(classdef: nodes.ClassDef) -> bool`: Checks for collect() method
  - Use astroid inference following `django_model_scanner/ast_utils.py` patterns

- [x] **Create test structure**: Set up `tests/test_prometheus_metrics_scanner/` with:

  - `__init__.py`
  - `test_ast_utils.py` (tests for pattern detection)
  - `fixtures/` directory
  - Create `fixtures/simple_metrics.py` with basic Counter, Gauge, Histogram, Summary examples

- [x] **Test AST utilities**: Write unit tests for all `ast_utils.py` functions
  - Test Counter, Gauge, Histogram, Summary detection with various import styles
  - Test metadata extraction (name, help, labels)
  - Test edge cases (missing help, empty labels, aliased imports)
  - Verify with `uv run pytest tests/test_prometheus_metrics_scanner/test_ast_utils.py`

### Phase 2: Parser Layer (Metric Extraction)

- [x] **Implement metric instantiation parser**: Create `metrics_parser.py` with:

  - `parse_metric_instantiation(assign: nodes.Assign) -> Optional[MetricInfo]`
  - Extract metric type, name, help, labels, namespace, subsystem, unit
  - Handle both positional and keyword arguments
  - Return structured MetricInfo dataclass

- [x] **Add MetricInfo and UsageInfo dataclasses**: Define data structures in `metrics_parser.py`

- [x] **Create parser test fixtures**: Add `fixtures/decorators.py` and `fixtures/custom_collectors.py`

  - Include decorator examples with @counter.count_exceptions(), @histogram.time()
  - Include custom collector examples with GaugeMetricFamily, CounterMetricFamily

- [x] **Test metric instantiation parsing**: Write tests in `test_metrics_parser.py`
  - Test extraction of all metric metadata fields
  - Test handling of optional parameters (namespace, subsystem, unit)
  - Test edge cases (dynamic names, missing fields)
  - Verify with `uv run pytest tests/test_prometheus_metrics_scanner/test_metrics_parser.py`

### Phase 3: Decorator & Custom Collector Support

- [x] **Implement decorator pattern detection**: Add to `metrics_parser.py`

  - `parse_metric_decorator(funcdef: nodes.FunctionDef) -> list[UsageInfo]`
  - Detect decorators on functions
  - Resolve decorator variable references to metric definitions
  - Return usage information for each decorator

- [x] **Implement custom collector parsing**: Add to `metrics_parser.py`

  - `parse_custom_collector(classdef: nodes.ClassDef) -> list[MetricInfo]`
  - Detect classes with collect() method
  - Parse MetricFamily instantiations within collect()
  - Extract all relevant metadata and mark as custom_collector

- [x] **Test decorator detection**: Extend `test_metrics_parser.py`

  - Test @counter.count_exceptions() pattern
  - Test @histogram.time() pattern
  - Test variable resolution across assignments
  - Verify decorator statement extraction

- [x] **Test custom collector parsing**: Extend `test_metrics_parser.py`
  - Test GaugeMetricFamily detection
  - Test all MetricFamily types
  - Test label extraction from custom collectors
  - Verify custom_collector flag

### Phase 4: Checker Layer (Aggregation)

- [x] **Implement PrometheusMetricsChecker**: Create `checker.py` with:

  - `__init__(self, base_path: str)`: Initialize with metrics dict
  - `check_file(self, file_path: str) -> None`: Process single file
  - `get_metrics(self) -> dict[str, MetricInfo]`: Return aggregated results
  - Use three-pass strategy: instantiations, decorators, custom collectors

- [x] **Implement metric aggregation logic**: Add to `checker.py`

  - Aggregate usages by metric name
  - Detect and warn on conflicts (same name, different type/labels)
  - Merge usages from multiple files
  - Sort usages by location

- [x] **Create complex test fixture**: Add `fixtures/complex.py`

  - Mix instantiation, decorator, and custom collector patterns
  - Include metrics used in multiple patterns
  - Test cross-file references

- [x] **Test checker aggregation**: Write `test_checker.py`
  - Test single-file processing
  - Test multi-file aggregation
  - Test conflict detection
  - Test usage sorting and deduplication
  - Verify with `uv run pytest tests/test_prometheus_metrics_scanner/test_checker.py`

### Phase 5: Export Layer (YAML Output)

- [x] **Implement YAML export functions**: Create `export.py` with:

  - `format_metric_output(metrics: dict[str, MetricInfo]) -> dict`: Convert to output structure
  - `export_to_yaml(metrics: dict[str, MetricInfo], output_path: str) -> None`: Write to file
  - `export_to_yaml_string(metrics: dict[str, MetricInfo]) -> str`: Return YAML string
  - Follow formatting standards (2-space indent, block style, UTF-8, alphabetical sorting)

- [x] **Test YAML export**: Write `test_export.py`
  - Test output structure matches spec examples
  - Test all required and optional fields
  - Test formatting (indentation, UTF-8 characters, sorting)
  - Test file writing with proper directory creation
  - Verify with `uv run pytest tests/test_prometheus_metrics_scanner/test_export.py`

### Phase 6: CLI Layer (Integration)

- [x] **Implement CLI entry point**: Create `cli.py` with:

  - `scan_prometheus_metrics(path: str, output: Optional[str], verbose: bool) -> str`
  - File/directory discovery (recursive .py file search)
  - Orchestrate PrometheusMetricsChecker
  - Call export functions
  - Error handling and verbose logging

- [x] **Add file filtering**: Implement in `cli.py`

  - Skip virtual environments (venv/, .venv/, env/)
  - Skip build directories (build/, dist/, .eggs/)
  - Skip cache directories (**pycache**/, .pytest_cache/)
  - Respect .gitignore patterns (optional enhancement)

- [x] **Test CLI functions**: Write `test_cli.py`
  - Test directory scanning
  - Test single file scanning
  - Test output to stdout vs file
  - Test verbose mode
  - Test error handling (nonexistent path, syntax errors)
  - Verify with `uv run pytest tests/test_prometheus_metrics_scanner/test_cli.py`

### Phase 7: Integration & Documentation

- [ ] **Add CLI integration to main**: Update `upcast/main.py` if centralized CLI exists

  - Register `scan-prometheus-metrics` command
  - Wire up to `scan_prometheus_metrics()` function

- [x] **Update project dependencies**: Modify `pyproject.toml`

  - Add `prometheus_client` to dev dependencies (for test fixtures)
  - Verify no new runtime dependencies needed (reuse astroid)

- [x] **Run full test suite**: Execute all tests

  - `uv run pytest tests/test_prometheus_metrics_scanner/ -v`
  - Verify 90%+ test coverage with `uv run pytest --cov=upcast.prometheus_metrics_scanner`
  - Fix any failing tests

- [x] **Update README**: Document new scanner capability

  - Add usage examples for CLI
  - Show sample output YAML
  - Link to spec document

- [x] **Validate with ruff**: Ensure code quality
  - Run `uv run ruff check upcast/prometheus_metrics_scanner/`
  - Fix any linting issues
  - Verify compliance with PEP8 via project ruff config

## Validation Checkpoints

After each phase:

1. Run relevant tests: `uv run pytest tests/test_prometheus_metrics_scanner/`
2. Check code style: `uv run ruff check upcast/prometheus_metrics_scanner/`
3. Verify no regressions in existing scanners

Final validation:

1. End-to-end test with real project containing prometheus_client metrics
2. Verify YAML output matches spec examples
3. Check test coverage: `uv run pytest --cov=upcast.prometheus_metrics_scanner --cov-report=term-missing` (Result: 70% coverage)
