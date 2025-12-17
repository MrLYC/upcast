# prometheus-metrics-scanner Specification

## Purpose

Automated detection and documentation of Prometheus metrics in Python codebases using prometheus_client library, providing centralized visibility into application observability instrumentation.

## ADDED Requirements

### Requirement: Prometheus Metric Detection

The system SHALL detect Prometheus metric instantiations using astroid-based semantic analysis of prometheus_client usage patterns.

#### Scenario: Counter detection

- **WHEN** code instantiates `Counter('metric_name', 'help text', ['label1', 'label2'])`
- **THEN** the system SHALL identify "metric_name" as a Counter metric
- **AND** extract metric type as "counter"
- **AND** extract help text as "help text"
- **AND** extract label names as ["label1", "label2"]
- **AND** record the file location and line number

#### Scenario: Gauge detection

- **WHEN** code instantiates `Gauge('memory_usage', 'Memory usage in bytes')`
- **THEN** the system SHALL identify "memory_usage" as a Gauge metric
- **AND** extract metric type as "gauge"
- **AND** extract help text
- **AND** handle metrics without labels (empty label list)

#### Scenario: Histogram detection

- **WHEN** code instantiates `Histogram('request_duration', 'Request duration', buckets=[0.1, 0.5, 1, 5])`
- **THEN** the system SHALL identify the metric as a Histogram
- **AND** extract metric type as "histogram"
- **AND** extract buckets configuration from keyword arguments

#### Scenario: Summary detection

- **WHEN** code instantiates `Summary('response_size', 'Response size in bytes')`
- **THEN** the system SHALL identify the metric as a Summary
- **AND** extract metric type as "summary"

#### Scenario: Import pattern resolution

- **WHEN** metrics are imported via `from prometheus_client import Counter` or `import prometheus_client`
- **THEN** the system SHALL resolve both patterns using astroid inference
- **AND** detect metrics regardless of import style

#### Scenario: Aliased import handling

- **WHEN** code uses `from prometheus_client import Counter as C`
- **THEN** the system SHALL resolve the alias through astroid
- **AND** correctly identify `C('name', 'help')` as a Counter metric

### Requirement: Metric Metadata Extraction

The system SHALL extract complete metric metadata including name, type, help text, labels, and optional parameters.

#### Scenario: Label extraction from list

- **WHEN** labels are provided as third positional argument `Counter('name', 'help', ['a', 'b'])`
- **THEN** the system SHALL extract labels as ["a", "b"]
- **AND** preserve label order

#### Scenario: Label extraction from labelnames keyword

- **WHEN** labels are provided via keyword `Counter('name', 'help', labelnames=['x', 'y'])`
- **THEN** the system SHALL extract labels from the keyword argument
- **AND** treat it equivalently to positional argument

#### Scenario: Namespace and subsystem extraction

- **WHEN** metric uses `Counter('requests', 'help', namespace='http', subsystem='api')`
- **THEN** the system SHALL extract namespace as "http"
- **AND** extract subsystem as "api"
- **AND** construct full metric name as "http_api_requests"

#### Scenario: Unit suffix extraction

- **WHEN** metric includes `unit` parameter like `Counter('size', 'help', unit='bytes')`
- **THEN** the system SHALL extract unit as "bytes"
- **AND** note that full metric name becomes "size_bytes"

#### Scenario: Registry tracking

- **WHEN** metric specifies custom registry via `Counter('name', 'help', registry=custom_registry)`
- **THEN** the system SHALL note the custom registry
- **AND** default to REGISTRY when not specified

#### Scenario: Missing help text

- **WHEN** metric is instantiated without help text `Counter('name')`
- **THEN** the system SHALL handle missing help gracefully
- **AND** set help to null in output

### Requirement: Decorator Pattern Detection

The system SHALL detect metrics used as function decorators for automatic instrumentation.

#### Scenario: count_exceptions decorator

- **WHEN** code uses `@CALLS.count_exceptions()` on a function
- **THEN** the system SHALL track this as a usage of the CALLS metric
- **AND** record pattern type as "decorator"
- **AND** extract the decorator statement

#### Scenario: time decorator for histograms

- **WHEN** code uses `@REQUEST_TIME.time()` on a function
- **THEN** the system SHALL detect the timing decorator
- **AND** associate it with the REQUEST_TIME histogram metric

#### Scenario: Decorator variable resolution

- **WHEN** decorator references a variable defined elsewhere
- **THEN** the system SHALL resolve the variable to its metric definition
- **AND** cross-reference the usage with the original metric

#### Scenario: Decorator with arguments

- **WHEN** decorator includes arguments like `@counter.count_exceptions(Exception)`
- **THEN** the system SHALL still detect the decorator pattern
- **AND** record the full decorator call

### Requirement: Custom Collector Detection

The system SHALL detect custom Prometheus collectors using MetricFamily classes for dynamic metrics.

#### Scenario: GaugeMetricFamily in collector

- **WHEN** a class defines `collect()` method with `GaugeMetricFamily('name', 'help', labels=['type'])`
- **THEN** the system SHALL detect "name" as a gauge metric
- **AND** mark it with `custom_collector: true`
- **AND** extract labels from the MetricFamily constructor

#### Scenario: CounterMetricFamily detection

- **WHEN** collector uses `CounterMetricFamily('name', 'help')`
- **THEN** the system SHALL detect as counter type
- **AND** mark as custom collector

#### Scenario: HistogramMetricFamily and SummaryMetricFamily

- **WHEN** collector uses HistogramMetricFamily or SummaryMetricFamily
- **THEN** the system SHALL detect the appropriate metric type
- **AND** extract all relevant metadata

#### Scenario: REGISTRY.register() tracking

- **WHEN** code calls `REGISTRY.register(MyCollector())`
- **THEN** the system SHALL note that the collector is registered
- **AND** associate its metrics with the registry

#### Scenario: Collector class detection

- **WHEN** scanning for custom collectors
- **THEN** the system SHALL identify classes with `collect()` method
- **AND** scan the method body for MetricFamily instantiations
- **AND** treat each yield as a metric definition

### Requirement: Result Aggregation by Metric Name

The system SHALL aggregate all usages of each metric across the entire codebase under a single metric entry.

#### Scenario: Multiple instantiations of same metric

- **WHEN** the same metric name appears in multiple files
- **THEN** the system SHALL aggregate into a single metric entry
- **AND** collect all usage locations
- **AND** validate consistency (same type, help, labels)

#### Scenario: Conflict detection

- **WHEN** same metric name is defined with different types or labels
- **THEN** the system SHALL report a validation warning
- **AND** include all conflicting definitions in output

#### Scenario: Usage pattern tracking

- **WHEN** a metric is both instantiated and used as decorator
- **THEN** the system SHALL record both patterns in the usages list
- **AND** distinguish pattern types (instantiation, decorator, custom_collector)

#### Scenario: Location formatting

- **WHEN** recording usage locations
- **THEN** each location SHALL be formatted as "relative/path/to/file.py:line"
- **AND** use paths relative to scan root
- **AND** sort usages by file path then line number

### Requirement: YAML Output Format

The system SHALL export detected metrics in structured YAML format optimized for human readability and documentation generation.

#### Scenario: Basic metric output structure

- **WHEN** exporting metrics to YAML
- **THEN** each metric SHALL be a top-level key (metric name)
- **AND** include `type` field (counter, gauge, histogram, summary)
- **AND** include `help` field (documentation string or null)
- **AND** include `labels` field (list of label names, empty list if none)
- **AND** include `usages` list with location, pattern, and statement

#### Scenario: Optional fields in output

- **WHEN** metric has namespace, subsystem, unit, or buckets
- **THEN** these fields SHALL be included in the output
- **AND** omitted if not present in the definition

#### Scenario: Custom collector flag

- **WHEN** metric is defined in a custom collector
- **THEN** output SHALL include `custom_collector: true`
- **AND** distinguish these from standard metrics

#### Scenario: Usage details

- **WHEN** recording each usage
- **THEN** include `location` as "file:line"
- **AND** include `pattern` (instantiation, decorator, custom_collector, increment)
- **AND** include `statement` as the relevant source code line

#### Scenario: YAML formatting standards

- **WHEN** generating YAML output
- **THEN** use 2-space indentation
- **AND** use block style for lists and dicts
- **AND** preserve UTF-8 characters in help text and labels
- **AND** sort metrics alphabetically by name

#### Scenario: Example output structure

```yaml
http_requests_total:
  type: counter
  help: "HTTP 请求总数"
  labels: [method, path, status]
  usages:
    - location: "api/views.py:15"
      pattern: instantiation
      statement: "Counter('http_requests_total', 'HTTP 请求总数', ['method', 'path', 'status'])"

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

### Requirement: CLI Interface

The system SHALL provide a command-line interface for scanning Python projects and generating metrics documentation.

#### Scenario: Scan directory

- **WHEN** user runs `python -m upcast.prometheus_metrics_scanner /path/to/project`
- **THEN** the system SHALL recursively scan all Python files
- **AND** detect all Prometheus metrics
- **AND** output YAML to stdout

#### Scenario: Scan specific file

- **WHEN** user runs scanner with a single file path
- **THEN** the system SHALL scan only that file
- **AND** output results

#### Scenario: Output to file

- **WHEN** user specifies `-o output.yaml` option
- **THEN** the system SHALL write YAML to the specified file
- **AND** create parent directories if needed
- **AND** report success or errors to stderr

#### Scenario: Verbose mode

- **WHEN** user specifies `-v` or `--verbose` flag
- **THEN** the system SHALL output detailed logging to stderr
- **AND** include file scanning progress
- **AND** report parsing warnings

#### Scenario: Error handling

- **WHEN** scanning encounters a syntax error in a file
- **THEN** the system SHALL log error to stderr
- **AND** continue scanning other files
- **AND** include partial results for successfully parsed files

### Requirement: AST Utilities

The system SHALL provide reusable AST utility functions following astroid best practices.

#### Scenario: is_prometheus_metric_call() detection

- **WHEN** given an astroid Call node
- **THEN** `is_prometheus_metric_call()` SHALL return metric type if it matches Counter, Gauge, Histogram, or Summary
- **AND** return None for non-metric calls

#### Scenario: extract_metric_name() function

- **WHEN** given a metric instantiation Call node
- **THEN** `extract_metric_name()` SHALL extract the first positional argument as metric name
- **AND** handle string literals and resolvable constants
- **AND** return None for dynamic names

#### Scenario: extract_help_text() function

- **WHEN** given a metric Call node
- **THEN** `extract_help_text()` SHALL extract the second positional argument
- **AND** return None if not provided

#### Scenario: extract_labels() function

- **WHEN** given a metric Call node
- **THEN** `extract_labels()` SHALL extract label names from third positional arg or labelnames keyword
- **AND** return empty list if no labels specified
- **AND** handle both list literals and resolvable constants

#### Scenario: is_custom_collector_class() detection

- **WHEN** given an astroid ClassDef node
- **THEN** `is_custom_collector_class()` SHALL return True if class has a `collect()` method
- **AND** return False otherwise

### Requirement: Type Inference Accuracy

The system SHALL use astroid's type inference to accurately resolve imports and qualified names.

#### Scenario: Resolve qualified imports

- **WHEN** code uses `import prometheus_client` and `prometheus_client.Counter(...)`
- **THEN** the system SHALL resolve to Counter class
- **AND** detect the metric correctly

#### Scenario: Resolve from imports

- **WHEN** code uses `from prometheus_client import Counter`
- **THEN** the system SHALL track the import
- **AND** recognize direct `Counter()` calls

#### Scenario: Handle inference failures gracefully

- **WHEN** type inference fails for complex dynamic code
- **THEN** the system SHALL fall back to pattern matching
- **AND** use heuristics (function names ending in 'Counter', 'Gauge', etc.)
- **AND** log warnings for manual review

### Requirement: Unit Test Coverage

The system SHALL include comprehensive unit tests covering all core functionality to ensure reliability.

#### Scenario: Pattern detection tests

- **WHEN** running unit tests for metric detection
- **THEN** tests SHALL verify Counter, Gauge, Histogram, Summary detection
- **AND** verify import pattern resolution
- **AND** cover aliased imports and module imports

#### Scenario: Metadata extraction tests

- **WHEN** running tests for metadata parsing
- **THEN** tests SHALL verify name, help, labels extraction
- **AND** verify namespace, subsystem, unit handling
- **AND** cover edge cases (missing help, empty labels)

#### Scenario: Decorator detection tests

- **WHEN** running tests for decorator patterns
- **THEN** tests SHALL verify count_exceptions, time decorators
- **AND** verify variable resolution for decorator references
- **AND** cover nested decorators

#### Scenario: Custom collector tests

- **WHEN** running tests for custom collectors
- **THEN** tests SHALL verify MetricFamily detection
- **AND** verify collect() method parsing
- **AND** cover all MetricFamily types

#### Scenario: Aggregation tests

- **WHEN** running tests for result aggregation
- **THEN** tests SHALL verify multi-file aggregation
- **AND** verify conflict detection
- **AND** verify usage pattern tracking

#### Scenario: Export tests

- **WHEN** running tests for YAML export
- **THEN** tests SHALL verify output structure
- **AND** verify formatting (indentation, UTF-8, sorting)
- **AND** verify all required and optional fields

#### Scenario: Test organization

- **WHEN** organizing the test suite
- **THEN** tests SHALL be in `tests/test_prometheus_metrics_scanner/`
- **AND** separated into modules:
  - `test_ast_utils.py` (pattern detection)
  - `test_metrics_parser.py` (metadata extraction)
  - `test_checker.py` (aggregation)
  - `test_cli.py` (CLI integration)
  - `test_export.py` (YAML output)
- **AND** use pytest fixtures for common test data
- **AND** include `fixtures/` directory with sample Python files

### Requirement: Module Structure Consistency

The system SHALL follow the established module structure pattern used by django_model_scanner and env_var_scanner.

#### Scenario: Module directory structure

- **WHEN** accessing the scanner implementation
- **THEN** the module SHALL be located at `upcast/prometheus_metrics_scanner/`
- **AND** contain submodules: `cli.py`, `checker.py`, `metrics_parser.py`, `export.py`, `ast_utils.py`
- **AND** follow the same organization as sibling scanners

#### Scenario: Import path consistency

- **WHEN** importing the scanner in user code
- **THEN** the import SHALL be `from upcast.prometheus_metrics_scanner import scan_prometheus_metrics`
- **AND** all internal imports SHALL use `upcast.prometheus_metrics_scanner` prefix

#### Scenario: Public API consistency

- **WHEN** users access the scanner
- **THEN** the main entry point SHALL be `scan_prometheus_metrics(path, output, verbose)`
- **AND** match the signature pattern of sibling scanners
- **AND** return YAML string when output is None
- **AND** write to file when output path is provided
