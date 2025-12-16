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
