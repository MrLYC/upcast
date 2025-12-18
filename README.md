# upcast

[![Release](https://img.shields.io/github/v/release/mrlyc/upcast)](https://img.shields.io/github/v/release/mrlyc/upcast)
[![Build status](https://img.shields.io/github/actions/workflow/status/mrlyc/upcast/main.yml?branch=main)](https://github.com/mrlyc/upcast/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/mrlyc/upcast/branch/main/graph/badge.svg)](https://codecov.io/gh/mrlyc/upcast)
[![Commit activity](https://img.shields.io/github/commit-activity/m/mrlyc/upcast)](https://img.shields.io/github/commit-activity/m/mrlyc/upcast)
[![License](https://img.shields.io/github/license/mrlyc/upcast)](https://img.shields.io/github/license/mrlyc/upcast)

A comprehensive static analysis toolkit for Python projects. Upcast provides 11 specialized scanners to analyze code without execution, extracting insights about Django models, environment variables, HTTP requests, concurrency patterns, and more.

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
  module: app.models
  bases:
    - models.Model
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
- Extracts field types and parameters
- Identifies relationships (ForeignKey, ManyToMany, OneToOne)
- Captures model metadata and options

### scan-django-settings

Find all references to Django settings variables throughout your codebase.

```bash
upcast scan-django-settings /path/to/django/project
```

**Output example:**

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

**Key features:**

- Detects `settings.VARIABLE` access patterns
- Finds `getattr(settings, ...)` calls
- Tracks `from django.conf import settings` imports
- Aggregates usage counts per setting

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
upcast scan-signals /path/to/project
```

**Output example:**

```yaml
post_save:
  type: django.signal
  receivers:
    - handler: users.signals.create_profile
      sender: User
      file: users/signals.py
      line: 25
    - handler: notifications.signals.send_welcome_email
      sender: User
      file: notifications/signals.py
      line: 42

task_success:
  type: celery.signal
  receivers:
    - handler: monitoring.handlers.log_task_success
      file: monitoring/handlers.py
      line: 15
```

**Key features:**

- Detects Django signals (pre_save, post_save, etc.)
- Finds Celery task signals
- Identifies signal receivers and senders
- Tracks decorator-based connections (`@receiver`)

## Code Analysis Scanners

### scan-concurrency-patterns

Identify concurrency patterns including async/await, threading, and multiprocessing.

```bash
upcast scan-concurrency-patterns /path/to/project
```

**Output example:**

```yaml
async_functions:
  - name: fetch_data
    file: api/client.py
    line: 45
    uses_await: true
    calls:
      - asyncio.gather
      - aiohttp.get

thread_usage:
  - pattern: threading.Thread
    file: workers/processor.py
    line: 78
    target: process_batch
    daemon: true

multiprocessing:
  - pattern: multiprocessing.Pool
    file: tasks/parallel.py
    line: 123
    workers: 4
```

**Key features:**

- Detects async/await patterns
- Identifies threading usage
- Finds multiprocessing constructs
- Tracks asyncio operations
- Flags potential concurrency issues

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

Find HTTP and API requests throughout your codebase.

```bash
upcast scan-http-requests /path/to/project
```

**Output example:**

```yaml
requests:
  - location: api/client.py:45
    method: GET
    library: requests
    statement: requests.get('https://api.example.com/users')
    url: https://api.example.com/users
    has_timeout: false

  - location: services/http.py:67
    method: POST
    library: httpx
    statement: httpx.post(url, json=data, timeout=30)
    has_timeout: true
    timeout: 30

  - location: tasks/fetch.py:23
    method: GET
    library: urllib
    statement: urllib.request.urlopen(url)
    has_timeout: false
```

**Key features:**

- Detects `requests`, `httpx`, `urllib`, `aiohttp`
- Extracts HTTP methods (GET, POST, PUT, DELETE)
- Identifies URLs when possible
- Checks for timeout configuration
- Flags missing timeout warnings

### scan-exception-handlers

Analyze exception handling patterns in your code.

```bash
upcast scan-exception-handlers /path/to/project
```

**Output example:**

```yaml
handlers:
  - location: api/views.py:45
    type: try-except
    exceptions:
      - ValueError
      - KeyError
    has_bare_except: false
    reraises: false

  - location: services/processor.py:78
    type: try-except
    exceptions:
      - Exception
    has_bare_except: false
    reraises: true
    logs_error: true

  - location: legacy/old_code.py:123
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

## Architecture

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

## Key Features

- **Static Analysis**: No code execution - safe for any codebase
- **11 Specialized Scanners**: Comprehensive project analysis
- **Advanced Type Inference**: Smart detection of types and patterns
- **Powerful File Filtering**: Glob-based include/exclude patterns
- **Multiple Output Formats**: YAML (human-readable) and JSON (machine-readable)
- **Aggregated Results**: Group findings by variable/model/metric name
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Well-Tested**: Comprehensive test suite with high coverage

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
