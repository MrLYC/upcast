# upcast

[![Release](https://img.shields.io/github/v/release/mrlyc/upcast)](https://img.shields.io/github/v/release/mrlyc/upcast)
[![Build status](https://img.shields.io/github/actions/workflow/status/mrlyc/upcast/main.yml?branch=main)](https://github.com/mrlyc/upcast/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/mrlyc/upcast/branch/main/graph/badge.svg)](https://codecov.io/gh/mrlyc/upcast)
[![Commit activity](https://img.shields.io/github/commit-activity/m/mrlyc/upcast)](https://img.shields.io/github/commit-activity/m/mrlyc/upcast)
[![License](https://img.shields.io/github/license/mrlyc/upcast)](https://img.shields.io/github/license/mrlyc/upcast)

This project provides a series of tools to analyze Python projects. It does not actually execute code but only uses
static analysis methods. Therefore, it has a more universal application scenario.

- **Github repository**: <https://github.com/mrlyc/upcast/>
- **Documentation** <https://mrlyc.github.io/upcast/>

## Installation

```bash
pip install upcast
```

## Usage

All scanner commands support file filtering options for precise control over which files to analyze:

- `--include PATTERN`: Include files matching glob pattern (can be used multiple times)
- `--exclude PATTERN`: Exclude files matching glob pattern (can be used multiple times)
- `--no-default-excludes`: Disable default exclusion of common directories (venv/, build/, dist/, etc.)

### scan-env-vars

**New in this version!** Scan Python files for environment variable usage with advanced type inference and aggregation. This command uses astroid for semantic analysis and provides comprehensive information about environment variables used in your project.

```bash
upcast scan-env-vars /path/to/your/python/project/
```

Scan specific files:

```bash
upcast scan-env-vars file1.py file2.py
```

Output to a file:

```bash
upcast scan-env-vars /path/to/your/python/project/ -o env-vars.yaml
```

JSON output format:

```bash
upcast scan-env-vars /path/to/your/python/project/ --format json -o env-vars.json
```

Enable verbose output:

```bash
upcast scan-env-vars /path/to/your/python/project/ -v
```

Filter files to scan:

```bash
# Only scan files in app/ directory
upcast scan-env-vars /path/to/project/ --include "app/**"

# Exclude test files
upcast scan-env-vars /path/to/project/ --exclude "tests/**" --exclude "**/*_test.py"

# Scan everything including normally excluded directories
upcast scan-env-vars /path/to/project/ --no-default-excludes
```

**Output Format:**

The command generates YAML (or JSON) output with aggregated information by environment variable name:

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
      default: null
      required: true
  required: true

API_KEY:
  types: []
  defaults: []
  usages:
    - location: api/client.py:23
      statement: os.environ['API_KEY']
      type: null
      default: null
      required: true
  required: true
```

**Features:**

- **Advanced Type Inference**: Detects types from:
  - Explicit type conversions: `int(os.getenv('PORT'))`
  - Default value literals: `os.getenv('DEBUG', False)`
  - Django-environ typed methods: `env.int('WORKERS')`
  - `or` expressions: `env('DEBUG') or False`
- **Multiple Pattern Support**:
  - Standard library: `os.getenv()`, `os.environ[]`, `os.environ.get()`
  - Django-environ: `env()`, `env.str()`, `env.int()`, `env.bool()`, etc.
  - Aliased imports: `from os import getenv`
- **Aggregation by Variable**: Shows all usages of each variable across your codebase
- **Required Detection**: Identifies which variables are required vs optional
- **Multiple Output Formats**: YAML (human-readable) or JSON (machine-readable)

**Type Inference Rules:**

### scan-django-models

Scan Django models in Python files and extract comprehensive model information including fields, relationships, and metadata.

```bash
upcast scan-django-models /path/to/your/django/project/
```

Output to a file:

```bash
upcast scan-django-models /path/to/your/django/project/ -o models.yaml
```

Filter files:

```bash
# Only scan app models
upcast scan-django-models /path/to/project/ --include "apps/**/models.py"

# Exclude migrations
upcast scan-django-models /path/to/project/ --exclude "migrations/**"
```

**Output Format:**

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
```

### scan-django-settings

Scan Django project for settings variable usage and identify all configuration references.

```bash
upcast scan-django-settings /path/to/your/django/project/
```

Output to a file:

```bash
upcast scan-django-settings /path/to/your/django/project/ -o settings.yaml
```

Filter files:

```bash
# Only scan specific apps
upcast scan-django-settings /path/to/project/ --include "core/**" --include "api/**"
```

**Output Format:**

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

### scan-prometheus-metrics

**New in this version!** Scan Python files for Prometheus metrics usage with comprehensive metadata extraction. This command uses astroid for semantic analysis and provides detailed information about all Prometheus metrics defined in your project.

```bash
upcast scan-prometheus-metrics /path/to/your/python/project/
```

Scan specific files:

```bash
upcast scan-prometheus-metrics metrics.py
```

Output to a file:

```bash
upcast scan-prometheus-metrics /path/to/your/python/project/ -o metrics.yaml
```

Enable verbose output:

```bash
upcast scan-prometheus-metrics /path/to/your/python/project/ -v
```

Filter files:

```bash
# Only scan metrics files
upcast scan-prometheus-metrics /path/to/project/ --include "**/*metrics.py"

# Exclude test files
upcast scan-prometheus-metrics /path/to/project/ --exclude "tests/**"
```

**Output Format:**

The command generates YAML output with aggregated information by metric name:

```yaml
http_requests_total:
  type: counter
  help: HTTP 请求总数
  labels:
    - method
    - path
    - status
  namespace: myapp
  subsystem: api
  usages:
    - location: api/metrics.py:15
      pattern: instantiation
      statement: http_requests = Counter('http_requests_total', 'HTTP 请求总数', ['method', 'path', 'status'])

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
      statement: duration_hist = Histogram('request_duration_seconds', 'Request duration in seconds', ['endpoint'], buckets=[0.1, 0.5, 1.0, 5.0])
```

**Features:**

- **Multiple Metric Types**: Detects Counter, Gauge, Histogram, and Summary metrics
- **Complete Metadata Extraction**:
  - Metric name and help text
  - Label names
  - Namespace and subsystem (for metric name prefixing)
  - Unit suffix
  - Histogram buckets
  - Custom collector detection
- **Multiple Pattern Support**:
  - Direct instantiation: `Counter('name', 'help', ['labels'])`
  - Decorator patterns: `@counter.count_exceptions()`
  - Custom collectors: `GaugeMetricFamily` in `collect()` methods
- **Aggregation by Metric**: Shows all usages of each metric across your codebase
- **Import Style Support**: Works with both `from prometheus_client import Counter` and `import prometheus_client`
- **YAML Output**: Human-readable format with proper Unicode support

**Use Cases:**

- Document all Prometheus metrics in your application
- Identify duplicate or conflicting metric definitions
- Generate metrics documentation for monitoring teams
- Validate metric naming conventions and labeling patterns

## Architecture

### Common Utilities

The project uses a shared utilities package (`upcast.common`) to eliminate code duplication and ensure consistency across all scanners:

- **file_utils**: File discovery, path validation, and package root detection
- **patterns**: Glob pattern matching with configurable excludes (venv/, **pycache**, build/, etc.)
- **ast_utils**: Unified AST inference with explicit fallback markers for debugging
- **export**: Recursive sorting and consistent YAML/JSON export

This architecture provides:

- ~300+ fewer lines of duplicate code
- Consistent behavior across all scanners
- Better error messages with fallback markers (backticks for failed inference)
- Unified file filtering support

## Features

- **Static Analysis**: No code execution required - uses AST and semantic analysis
- **Multiple Scanners**: Environment variables, Django models/settings, Prometheus metrics
- **Advanced Type Inference**: Detects types from various patterns and conventions
- **File Filtering**: Powerful glob-based include/exclude patterns
- **Aggregated Output**: Results grouped by variable/model/metric name
- **Multiple Formats**: YAML (human-readable) and JSON (machine-readable)
- **Verbose Mode**: Detailed logging for debugging
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Migration Guide

If you're using older command names, they still work but are deprecated:

- `analyze-django-models` → Use `scan-django-models` instead
- `scan-prometheus-metrics-cmd` → Use `scan-prometheus-metrics` instead
- `scan-django-settings-cmd` → Use `scan-django-settings` instead

The old commands will show a deprecation warning.
