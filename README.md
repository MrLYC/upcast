# upcast

[![Release](https://img.shields.io/github/v/release/mrlyc/upcast)](https://img.shields.io/github/v/release/mrlyc/upcast)
[![Build status](https://img.shields.io/github/actions/workflow/status/mrlyc/upcast/main.yml?branch=main)](https://github.com/mrlyc/upcast/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/mrlyc/upcast/branch/main/graph/badge.svg)](https://codecov.io/gh/mrlyc/upcast)
[![Commit activity](https://img.shields.io/github/commit-activity/m/mrlyc/upcast)](https://img.shields.io/github/commit-activity/m/mrlyc/upcast)
[![License](https://img.shields.io/github/license/mrlyc/upcast)](https://img.shields.io/github/license/mrlyc/upcast)

[English](https://github.com/MrLYC/upcast/blob/main/README.md) | [中文](https://www.zdoc.app/zh/MrLYC/upcast)

A comprehensive static analysis toolkit for Python projects. Upcast provides 12 specialized scanners to analyze code without execution, extracting insights about Django models, environment variables, HTTP requests, concurrency patterns, code complexity, and more.

- **Github repository**: <https://github.com/mrlyc/upcast/>
- **Documentation**: <https://mrlyc.github.io/upcast/>

## Quick Start

```bash
# Install
pip install upcast

# Scan environment variables
upcast scan-env-vars /path/to/project

# Analyze Django models
upcast scan-django-models /path/to/django/project

# Find blocking operations
upcast scan-blocking-operations /path/to/project -o blocking.yaml

# Check cyclomatic complexity
upcast scan-complexity-patterns /path/to/project --threshold 15
```

## Installation

```bash
pip install upcast
```

## Common Options

All scanner commands support powerful file filtering options:

```bash
# Include specific patterns
upcast scan-env-vars . --include "app/**" --include "core/**"

# Exclude patterns
upcast scan-env-vars . --exclude "tests/**" --exclude "migrations/**"

# Disable default excludes (venv/, build/, dist/, etc.)
upcast scan-env-vars . --no-default-excludes

# Combine options
upcast scan-env-vars . --include "src/**" --exclude "**/*_test.py"
```

**Other common options:**

- `-o, --output FILE`: Save results to file instead of stdout
- `--format FORMAT`: Choose output format (`yaml` or `json`)
- `-v, --verbose`: Enable detailed logging

## Django Scanners

### scan-django-models

Analyze Django model definitions, extracting fields, relationships, and metadata.

```bash
upcast scan-django-models /path/to/django/project
```

**Output example:**

```yaml
app.models.User:
  name: User
  module: app.models
  bases:
    - models.Model
  description: "User model for authentication and profile management."
  fields:
    username:
      type: models.CharField
      max_length: 150
      unique: true
    email:
      type: models.EmailField
    created_at:
      type: models.DateTimeField
      auto_now_add: true
  relationships:
    - type: ForeignKey
      to: Group
      field: group
```

**Key features:**

- Detects all Django model classes
- Extracts model descriptions from docstrings
- Extracts field types and parameters
- Identifies relationships (ForeignKey, ManyToMany, OneToOne)
- Captures model metadata and options

### scan-django-settings

Find all references to Django settings variables and extract settings definitions from your Django project.

**Basic usage (scan usages only):**

```bash
upcast scan-django-settings /path/to/django/project
```

**Scan definitions only:**

```bash
upcast scan-django-settings --definitions-only /path/to/django/project
```

**Scan both definitions and usages:**

```bash
upcast scan-django-settings --combined /path/to/django/project
```

**Output example (usages):**

```yaml
DEBUG:
  count: 5
  locations:
    - file: app/views.py
      line: 15
      column: 8
      code: settings.DEBUG
      pattern: attribute_access
    - file: middleware/security.py
      line: 23
      column: 12
      code: getattr(settings, 'DEBUG', False)
      pattern: getattr
```

**Output example (definitions):**

```yaml
definitions:
  settings.base:
    DEBUG:
      value: true
      line: 10
      type: bool
    SECRET_KEY:
      value: "base-secret-key"
      line: 11
      type: string
    INSTALLED_APPS:
      value: ["django.contrib.admin", "django.contrib.auth"]
      line: 15
      type: list
    __star_imports__:
      - settings.common

  settings.dev:
    DEBUG:
      value: false
      line: 5
      type: bool
      overrides: settings.base
    DEV_MODE:
      value: true
      line: 6
      type: bool
```

**Output example (combined):**

```yaml
definitions:
  settings.base:
    DEBUG:
      value: true
      line: 10
      type: bool

usages:
  DEBUG:
    count: 5
    locations:
      - file: app/views.py
        line: 15
```

**Key features:**

- **Usage scanning:**

  - Detects `settings.VARIABLE` access patterns
  - Finds `getattr(settings, ...)` calls
  - Tracks `from django.conf import settings` imports
  - Aggregates usage counts per setting

- **Definition scanning:**
  - Scans settings modules in `settings/` or `config/` directories
  - Extracts setting values with type inference
  - Detects inheritance via `from .base import *`
  - Tracks which settings override base settings
  - Supports dynamic imports (`importlib.import_module`)
  - Dynamic values wrapped in backticks (e.g., `` `os.environ.get('KEY')` ``)

**CLI options:**

- `--definitions-only`: Scan and output only settings definitions
- `--usages-only`: Scan and output only settings usages (default behavior)
- `--combined`: Scan and output both definitions and usages
- `--no-usages`: Skip usage scanning (faster when only definitions needed)
- `--no-definitions`: Skip definition scanning (default behavior)
- `-o, --output FILE`: Write results to YAML file
- `-v, --verbose`: Enable verbose output

### scan-django-urls

Scan Django URL configurations and extract route patterns.

```bash
upcast scan-django-urls /path/to/django/project
```

**Output example:**

```yaml
/api/users/:
  pattern: api/users/
  view: users.views.UserListView
  name: user-list
  methods:
    - GET
    - POST
  file: api/urls.py
  line: 15

/api/users/<int:pk>/:
  pattern: api/users/<int:pk>/
  view: users.views.UserDetailView
  name: user-detail
  methods:
    - GET
    - PUT
    - DELETE
  file: api/urls.py
  line: 16
```

**Key features:**

- Extracts URL patterns from `urlpatterns`
- Identifies view functions and classes
- Captures route names
- Detects path converters (`<int:id>`, `<slug:slug>`)

### scan-signals

Discover Django and Celery signal definitions and handlers.

```bash
# Basic usage
upcast scan-signals /path/to/project

# Save to file (supports JSON and YAML)
upcast scan-signals /path/to/project -o signals.yaml
upcast scan-signals /path/to/project -o signals.json --format json

# Filter signal files
upcast scan-signals /path/to/project --include "**/signals/**"
```

**Output format:**

```yaml
metadata:
  root_path: /path/to/project
  scanner_name: signal
summary:
  total_count: 5
  files_scanned: 3
  django_receivers: 4
  celery_receivers: 1
  custom_signals_defined: 2
  unused_custom_signals: 0
results:
  - signal: post_save
    type: django
    category: model_signals
    receivers:
      - handler: create_profile
        file: users/signals.py
        line: 25
        sender: User
        context:
          type: function
  - signal: user_logged_in
    type: django
    category: custom_signals
    receivers:
      - handler: log_login
        file: auth/handlers.py
        line: 42
    status: active
```

**Key features:**

- Detects Django signals (pre_save, post_save, m2m_changed, etc.)
- Finds Celery task signals (task_success, task_failure, etc.)
- Identifies custom signal definitions
- Tracks signal receivers and senders
- Supports decorator-based connections (`@receiver`)
- Detects unused custom signals
- Provides comprehensive statistics in summary

## Code Analysis Scanners

### scan-concurrency-patterns

Identify concurrency patterns including async/await, threading, and multiprocessing with detailed context and parameter extraction.

```bash
upcast scan-concurrency-patterns /path/to/project
```

**Output example:**

```yaml
summary:
  total_count: 15
  files_scanned: 8
  scan_duration_ms: 120
  by_category:
    threading: 6
    multiprocessing: 3
    asyncio: 6

results:
  threading:
    thread_creation:
      - file: workers/processor.py
        line: 78
        pattern: thread_creation
        function: start_worker
        class_name: WorkerManager
        details:
          target: process_batch
          name: worker-1
        statement: threading.Thread(target=process_batch, name="worker-1")

    thread_pool_executor:
      - file: tasks/parallel.py
        line: 45
        pattern: thread_pool_executor
        function: setup_executor
        details:
          max_workers: 4
        statement: ThreadPoolExecutor(max_workers=4)

    submit:
      - file: tasks/parallel.py
        line: 67
        pattern: executor_submit_thread
        function: process_items
        details:
          function: worker_function
        api_call: submit
        statement: executor.submit(worker_function, item)

  multiprocessing:
    process_creation:
      - file: compute/workers.py
        line: 123
        pattern: process_creation
        function: start_compute
        details:
          target: compute_intensive_task
        statement: multiprocessing.Process(target=compute_intensive_task)

    run_in_executor:
      - file: api/handlers.py
        line: 89
        pattern: run_in_executor_process
        function: async_handler
        details:
          executor_type: ProcessPoolExecutor
          function: cpu_intensive
        api_call: run_in_executor
        statement: await loop.run_in_executor(process_pool, cpu_intensive)

  asyncio:
    async_function:
      - file: api/client.py
        line: 45
        pattern: async_function
        function: fetch_data
        statement: async def fetch_data

    create_task:
      - file: api/client.py
        line: 78
        pattern: create_task
        function: fetch_all
        details:
          coroutine: fetch_data
        api_call: create_task
        statement: asyncio.create_task(fetch_data(url))

    run_in_executor:
      - file: api/handlers.py
        line: 56
        pattern: run_in_executor_thread
        function: async_handler
        details:
          executor_type: ThreadPoolExecutor
          function: io_operation
        api_call: run_in_executor
        statement: await loop.run_in_executor(thread_pool, io_operation)
```

**Key features:**

- **Pattern-Specific Detection**: Distinguishes Thread creation, ThreadPoolExecutor, submit() calls, etc.
- **Context Extraction**: Captures enclosing function and class names for each pattern
- **Parameter Extraction**: Extracts target functions, max_workers, coroutine names
- **Executor Resolution**: Two-pass scanning resolves executor variables in submit() and run_in_executor()
- **API Call Tracking**: Identifies specific API methods (create_task, submit, run_in_executor)
- **Smart Filtering**: Skips asyncio.create_task() with unresolvable coroutines to reduce noise

### scan-blocking-operations

Find blocking operations that may cause performance issues in async code.

```bash
upcast scan-blocking-operations /path/to/project
```

**Output example:**

```yaml
summary:
  total_operations: 8
  by_category:
    time_based: 3
    synchronization: 2
    subprocess: 3
  files_analyzed: 5

operations:
  time_based:
    - location: api/handlers.py:45:8
      type: time_based.sleep
      statement: time.sleep(5)
      duration: 5
      async_context: true
      function: async_handler

  synchronization:
    - location: cache/manager.py:67:12
      type: synchronization.lock_acquire
      statement: lock.acquire(timeout=10)
      timeout: 10
      async_context: true

  subprocess:
    - location: scripts/runner.py:23:15
      type: subprocess.run
      statement: subprocess.run(['ls', '-la'], timeout=30)
      timeout: 30
```

**Key features:**

- Detects `time.sleep()` in async functions
- Finds blocking lock operations
- Identifies subprocess calls without async wrappers
- Detects Django ORM `select_for_update()`
- Flags anti-patterns in async code

### scan-unit-tests

Analyze unit test files and extract test information.

```bash
upcast scan-unit-tests /path/to/tests
```

**Output example:**

```yaml
tests/test_users.py:
  framework: pytest
  test_count: 15
  tests:
    - name: test_create_user
      line: 45
      type: function
      async: false
      fixtures:
        - db
        - user_factory
    - name: test_update_user_email
      line: 67
      type: function
      async: false
      markers:
        - slow
        - integration

tests/test_api.py:
  framework: unittest
  test_count: 8
  classes:
    - name: UserAPITestCase
      line: 12
      tests:
        - test_get_user
        - test_create_user
        - test_delete_user
```

**Key features:**

- Detects pytest and unittest tests
- Extracts test function/method names
- Identifies async tests
- Captures fixtures and markers
- Counts tests per file

## Infrastructure Scanners

### scan-env-vars

Scan for environment variable usage with advanced type inference.

```bash
upcast scan-env-vars /path/to/project
```

**Output example:**

```yaml
DATABASE_URL:
  types:
    - str
  defaults:
    - postgresql://localhost/db
  usages:
    - location: config/settings.py:15
      statement: os.getenv('DATABASE_URL', 'postgresql://localhost/db')
      type: str
      default: postgresql://localhost/db
      required: false
    - location: config/database.py:8
      statement: env.str('DATABASE_URL')
      type: str
      required: true
  required: true

API_TIMEOUT:
  types:
    - int
  defaults:
    - 30
  usages:
    - location: api/client.py:23
      statement: int(os.getenv('API_TIMEOUT', '30'))
      type: int
      default: 30
      required: false
  required: false
```

**Key features:**

- Advanced type inference from default values and conversions
- Detects `os.getenv()`, `os.environ[]`, `os.environ.get()`
- Supports django-environ patterns (`env.int()`, `env.bool()`)
- Identifies required vs optional variables
- Aggregates all usages per variable

### scan-prometheus-metrics

Extract Prometheus metrics definitions with full metadata.

```bash
upcast scan-prometheus-metrics /path/to/project
```

**Output example:**

```yaml
http_requests_total:
  type: counter
  help: Total HTTP requests
  labels:
    - method
    - path
    - status
  namespace: myapp
  subsystem: api
  usages:
    - location: api/metrics.py:15
      pattern: instantiation
      statement: Counter('http_requests_total', 'Total HTTP requests', ['method', 'path', 'status'])

request_duration_seconds:
  type: histogram
  help: Request duration in seconds
  labels:
    - endpoint
  buckets:
    - 0.1
    - 0.5
    - 1.0
    - 5.0
  usages:
    - location: middleware/metrics.py:23
      pattern: instantiation
      statement: Histogram('request_duration_seconds', ...)
```

**Key features:**

- Detects Counter, Gauge, Histogram, Summary
- Extracts metric names, help text, and labels
- Captures namespace and subsystem
- Identifies histogram buckets
- Supports decorator patterns

## HTTP & Exception Scanners

### scan-http-requests

Find HTTP and API requests throughout your codebase with intelligent URL pattern detection.

```bash
upcast scan-http-requests /path/to/project
```

**Output example:**

```yaml
https://api.example.com/users/...:
  method: GET
  library: requests
  usages:
    - location: api/client.py:45
      method: GET
      statement: requests.get(f"https://api.example.com/users/{user_id}")
      session_based: false
      is_async: false

https://api.example.com/api/v2/data:
  method: GET
  library: requests
  usages:
    - location: services/http.py:67
      method: GET
      statement: requests.get(BASE_URL + "/api/v2/data")
      timeout: 30
      session_based: false
      is_async: false

...://.../console-acp/api/v1/token/login:
  method: POST
  library: requests
  usages:
    - location: auth/login.py:23
      method: POST
      statement: requests.post(f"{proto}://{host}/console-acp/api/v1/token/login")
      session_based: false
      is_async: false
```

**Key features:**

- **Smart URL Detection**: Detects `requests`, `httpx`, `urllib`, `aiohttp`
- **Context-Aware Resolution**: Infers variable values from assignments in the same scope
- **Pattern Preservation**: Preserves static URL parts while replacing dynamic segments with `...`
  - `f"https://api.example.com/users/{user_id}"` → `https://api.example.com/users/...`
  - `f"{proto}://{host}/api/v1/path"` → `...://.../api/v1/path`
  - `BASE_URL + "/api/data"` → resolves BASE_URL if defined
  - `f"{a}{b}{c}{d}"` → `...` (merges consecutive `...` into one)
- **Extracts HTTP methods** (GET, POST, PUT, DELETE)
- **Identifies URLs** when possible, with smart pattern normalization
- **Checks for timeout configuration**
- **Detects async requests** and session-based calls

### scan-exception-handlers

Analyze exception handling patterns in your code.

```bash
upcast scan-exception-handlers /path/to/project
```

**Output example:**

```yaml
handlers:
  - file: api/views.py
    lineno: 45
    end_lineno: 52
    type: try-except
    exceptions:
      - ValueError
      - KeyError
    has_bare_except: false
    reraises: false

  - file: services/processor.py
    lineno: 78
    end_lineno: 85
    type: try-except
    exceptions:
      - Exception
    has_bare_except: false
    reraises: true
    logs_error: true

  - file: legacy/old_code.py
    lineno: 123
    end_lineno: 127
    type: try-except
    has_bare_except: true
    warning: Bare except clause detected
```

**Key features:**

- Detects try-except blocks
- Identifies caught exception types
- Flags bare except clauses (anti-pattern)
- Checks for error logging
- Detects exception re-raising

## Code Quality Scanners

### scan-complexity-patterns

Analyze cyclomatic complexity to identify functions that may need refactoring.

```bash
upcast scan-complexity-patterns /path/to/project
```

**Output example:**

```yaml
summary:
  high_complexity_count: 12
  files_analyzed: 28
  by_severity:
    warning: 7 # 11-15
    high_risk: 4 # 16-20
    critical: 1 # >20

modules:
  app/services/user.py:
    - name: process_user_registration
      line: 45
      end_line: 98
      complexity: 14
      severity: warning
      message: "Complexity 14 exceeds threshold 11"
      description: "Validate user registration with multiple checks"
      signature: "def process_user_registration(data: dict, strict: bool = True) -> Result:"
      comment_lines: 8
      code_lines: 54
      code: |
        def process_user_registration(data: dict, strict: bool = True) -> Result:
            """Validate user registration with multiple checks."""
            # Check required fields
            if not data.get('email'):
                return Result.error('Email required')
            ...
```

**Usage options:**

```bash
# Scan with default threshold (11)
upcast scan-complexity-patterns /path/to/project

# Custom threshold
upcast scan-complexity-patterns . --threshold 15

# Include test files (excluded by default)
upcast scan-complexity-patterns . --include-tests

# Save to file
upcast scan-complexity-patterns . -o complexity-report.yaml

# JSON format
upcast scan-complexity-patterns . --format json
```

**Severity levels:**

- **healthy** (≤5): Very simple, minimal maintenance
- **acceptable** (6-10): Reasonable complexity
- **warning** (11-15): Refactoring recommended
- **high_risk** (16-20): Significant maintenance cost
- **critical** (>20): Design issues likely

**Key features:**

- **Accurate Calculation**: Counts decision points (if/elif, loops, except, boolean operators)
- **Code Extraction**: Full function source code included
- **Comment Statistics**: Uses Python tokenize for accurate comment counting
- **Test Exclusion**: Automatically excludes test files (configurable)
- **Detailed Metadata**: Function signature, docstring, line numbers
- **Actionable Output**: Sorted by severity with clear recommendations

## Architecture

### Data Models

Starting from version 0.3.0, Upcast provides standardized Pydantic models for all scanner outputs in the `upcast.models` package. This enables type-safe data handling for both scanners and future analyzers.

**Base Models:**

```python
from upcast.models import ScannerSummary, ScannerOutput

# All scanners extend these base classes
class MySummary(ScannerSummary):
    # Scanner-specific summary fields
    pass

class MyOutput(ScannerOutput[ResultType]):
    summary: MySummary
    results: ResultType
```

**Available Models:**

- **base**: `ScannerSummary`, `ScannerOutput` - Base classes for all scanners
- **blocking_operations**: `BlockingOperation`, `BlockingOperationsSummary`, `BlockingOperationsOutput`
- **concurrency**: `ConcurrencyUsage`, `ConcurrencyPatternSummary`, `ConcurrencyPatternOutput`
- **complexity**: `ComplexityResult`, `ComplexitySummary`, `ComplexityOutput`
- **django_models**: `DjangoField`, `DjangoModel`, `DjangoModelSummary`, `DjangoModelOutput`
- **django_settings**: `SettingsUsage`, `SettingDefinition`, `DjangoSettingsSummary`, `DjangoSettings*Output`
- **django_urls**: `UrlPattern`, `DjangoUrlSummary`, `DjangoUrlOutput`
- **env_vars**: `EnvVarInfo`, `EnvVarSummary`, `EnvVarOutput`
- **exceptions**: `ExceptionHandler`, `ExceptionHandlerSummary`, `ExceptionHandlerOutput`
- **http_requests**: `HttpRequestInfo`, `HttpRequestSummary`, `HttpRequestOutput`
- **metrics**: `MetricInfo`, `PrometheusMetricSummary`, `PrometheusMetricOutput`
- **signals**: `SignalInfo`, `SignalSummary`, `SignalOutput`
- **unit_tests**: `UnitTestInfo`, `UnitTestSummary`, `UnitTestOutput`

**Usage Example:**

```python
from upcast.models import EnvVarOutput, EnvVarInfo
from upcast.env_var_scanner import EnvironmentVariableScanner

# Type-safe scanner output
scanner = EnvironmentVariableScanner()
output: EnvVarOutput = scanner.scan(project_path)

# Access with full type hints
for var_name, var_info in output.results.items():
    var_info: EnvVarInfo
    print(f"{var_name}: required={var_info.required}")
    for location in var_info.locations:
        print(f"  {location.file}:{location.line}")
```

### Common Utilities

Upcast uses a shared utilities package (`upcast.common`) for consistency:

- **file_utils**: File discovery, path validation, package root detection
- **patterns**: Glob pattern matching with configurable excludes
- **ast_utils**: Unified AST analysis with astroid
- **export**: Consistent YAML/JSON output formatting

Benefits:

- 300+ fewer lines of duplicate code
- Consistent behavior across scanners
- Better error messages
- Unified file filtering

## Ke2 Features

- **Static Analysis**: No code execution - safe for any codebase
- **11 Specialized Scanners**: Comprehensive project analysis
- **Advanced Type Inference**: Smart detection of types and patterns
- **Powerful File Filtering**: Glob-based include/exclude patterns
- **Multiple Output Formats**: YAML (human-readable) and JSON (machine-readable)
- **Aggregated Results**: Group findings by variable/model/metric name
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Well-Tested**: Comprehensive test suite with high coverage

## Integration Testing

Upcast includes comprehensive integration tests that validate all scanners on a real-world Django project (blueking-paas).

### Running Integration Tests

```bash
# Run all scanners on example project
make test-integration
```

This command:

- Scans `example/blueking-paas` with all 12 scanners
- Outputs results to `example/scan-results/*.yaml`
- Takes approximately 1-2 minutes to complete

### CI Validation

The GitHub Actions workflow automatically:

- Runs integration tests on every PR
- Compares scan results against baseline
- Fails if scanner output changes unexpectedly
- Helps detect regressions in scanner behavior

### Updating Baseline

When scanner improvements intentionally change output:

```bash
# 1. Run integration tests
make test-integration

# 2. Copy new results to baseline
cp -r example/scan-results/* example/scan-results-baseline/

# 3. Commit baseline updates
git add example/scan-results-baseline/
git commit -m "Update scanner baseline: [describe changes]"
```

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
