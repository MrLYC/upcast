# Scanner Architecture Spec

## Overview

This specification defines the unified architecture for all scanner modules in the Upcast static analysis toolkit. It establishes common patterns, base classes, type systems, and output formats that all scanners must follow.

## Requirements

### Module Organization

**Requirement**: Scanners Located in Unified Package

All scanner modules must be located in the `upcast.scanners` package:

**Scenario**: Scanner Module Structure

```python
# Simple scanners (< 500 LOC): Single module file
from upcast.scanners.signal import scan_signals
from upcast.scanners.http_request import scan_http_requests
from upcast.scanners.env_var import scan_env_vars

# Complex scanners (>= 500 LOC): Package with submodules
from upcast.scanners.django_model import scan_django_models
# django_model/ contains: __init__.py, models.py, parser.py, checker.py
```

**Module Naming Convention**:

- Package: `upcast.scanners`
- Module names: Snake case without `_scanner` suffix
- Examples: `signal`, `http_request`, `django_model`, `env_var`

---

### Base Classes

**Requirement**: All Scanners Extend Base Scanner Class

All scanner implementations must extend `BaseScanner` abstract class:

**Scenario**: Implementing a Scanner

```python
from upcast.common.scanner_base import BaseScanner
from upcast.common.models import ScannerOutput
from pathlib import Path

class HttpRequestScanner(BaseScanner[HttpRequestOutput]):
    def scan(self, path: Path) -> HttpRequestOutput:
        files = self.get_files_to_scan(path)
        results = {}

        for file_path in files:
            if self.should_scan_file(file_path):
                file_results = self.scan_file(file_path)
                results.update(file_results)

        return self._build_output(results)

    def scan_file(self, file_path: Path) -> dict:
        # File-specific scanning logic
        ...
```

---

### Type System

**Requirement**: Strongly Typed Output Models

All scanners must use Pydantic models for outputs with proper type validation:

**Scenario**: Scanner Output Model Definition

```python
from pydantic import BaseModel, Field
from upcast.common.models import ScannerSummary, ScannerOutput

class MyScanner SummaryFields(ScannerSummary):
    """Scanner-specific summary fields."""
    specific_count: int = Field(ge=0, description="Scanner-specific metric")
    categories: list[str] = Field(description="Categories found")

class MyItemInfo(BaseModel):
    """Individual item detected by scanner."""
    name: str
    file: str
    line: int = Field(gt=0)

class MyScannerOutput(ScannerOutput[dict[str, MyItemInfo]]):
    """Complete scanner output."""
    summary: MyScannerSummaryFields
    results: dict[str, MyItemInfo]
```

**Type Validation Rules**:

- All fields must have type annotations
- Use Pydantic `Field()` for validation constraints
- Summary models must extend `ScannerSummary`
- Output models must extend `ScannerOutput[T]`

---

### Unified Output Structure

**Requirement**: Consistent Output Format Across All Scanners

All scanners must return outputs following this structure:

```yaml
summary:
  # Base fields (required for all scanners)
  total_count: int # Total items found
  files_scanned: int # Number of files scanned
  scan_duration_ms: int # Scan duration in milliseconds

  # Scanner-specific fields (vary by scanner)
  <scanner_specific_field>: <value>

results:
  # Scanner-specific results structure
  # Can be: list, dict, nested objects
  # Must match the type parameter in ScannerOutput[T]

metadata:
  scanner_name: str # Scanner identifier
  scanner_version: str # Scanner version
  scan_timestamp: str # ISO 8601 timestamp
  # Optional scanner-specific metadata
```

**Scenario**: Output Structure Consistency

```python
def test_scanner_output_structure(scanner_func):
    output = scanner_func(Path("/project"))

    # All scanners have these top-level keys
    assert hasattr(output, "summary")
    assert hasattr(output, "results")
    assert hasattr(output, "metadata")

    # All summaries have base fields
    assert hasattr(output.summary, "total_count")
    assert hasattr(output.summary, "files_scanned")
    assert hasattr(output.summary, "scan_duration_ms")

    # All metadata has scanner info
    assert "scanner_name" in output.metadata
    assert "scanner_version" in output.metadata
```

---

### Export Functions

**Requirement**: Unified Export Interface

All scanners must use the common export function for serialization:

**Scenario**: Export Scanner Output

```python
from upcast.common.export import export_scanner_output
from pathlib import Path

output = scan_http_requests(Path("/project"))

# Export to YAML
yaml_output = export_scanner_output(output, format="yaml")

# Export to JSON with file
json_output = export_scanner_output(
    output,
    format="json",
    file_path=Path("output.json")
)
```

**Forbidden**: Scanner-specific `format_*_output()` functions are not allowed. Use unified export.

---

### CLI Interface

**Requirement**: Consistent CLI Commands and Arguments

All scanner CLI commands must follow standard patterns:

**Command Naming**: `upcast scan-<scanner-name> <path> [options]`

**Standard Arguments** (all scanners must support):

- `path`: Path to scan (positional, required)
- `-o/--output FILE`: Output file path
- `--format {yaml,json}`: Output format
- `--include PATTERN`: Include file patterns (multiple)
- `--exclude PATTERN`: Exclude file patterns (multiple)
- `-v/--verbose`: Verbose output
- `--legacy-format`: Legacy output format (deprecated)

**Scenario**: CLI Consistency Across Scanners

```bash
# All scanners follow same pattern
$ upcast scan-signals /project -o signals.yaml --format yaml
$ upcast scan-http-requests /project -o requests.json --format json
$ upcast scan-env-vars /project --include "**/*.py" --exclude "**/tests/**"
```

---

### Documentation

**Requirement**: Comprehensive Scanner Documentation

Each scanner must have complete documentation in `docs/scanners/<scanner-name>.md`:

**Required Sections**:

1. **Purpose**: What the scanner detects and why it's useful
2. **Usage**: CLI command examples
3. **Output Schema**: Field descriptions (auto-generated from Pydantic)
4. **Examples**: Input code → output examples
5. **Implementation Notes**: Technical details

**Scenario**: Documentation Completeness

```bash
$ ls docs/scanners/
blocking-operation.md
concurrency-pattern.md
cyclomatic-complexity.md
django-model.md
django-settings.md
django-url.md
env-var.md
exception-handler.md
http-request.md
prometheus-metrics.md
signal.md
unit-test.md
README.md
```

---

### Backward Compatibility

**Requirement**: Deprecated Import Paths with Warnings

Old import paths must remain functional with deprecation warnings:

**Scenario**: Deprecated Import Path

```python
import warnings

# Old import emits warning
with warnings.catch_warnings(record=True) as w:
    from upcast.http_request_scanner import scan_http_requests

    assert len(w) == 1
    assert issubclass(w[0].category, DeprecationWarning)
    assert "upcast.scanners.http_request" in str(w[0].message)
    assert "will be removed in v2.0.0" in str(w[0].message)
```

**Deprecation Timeline**:

- v1.0.0: Old paths work with warnings
- v1.x: Warnings continue
- v2.0.0: Old paths removed

---

### Performance

**Requirement**: Scanner Performance Standards

Scanner refactoring must not significantly degrade performance:

**Scenario**: Performance Regression Limits

```python
import time

def benchmark_scanner(scanner_func, path):
    start = time.time()
    output = scanner_func(path)
    duration = time.time() - start
    return duration

old_duration = benchmark_scanner(old_scan_http_requests, test_path)
new_duration = benchmark_scanner(new_scan_http_requests, test_path)

# Less than 10% regression allowed
regression = (new_duration - old_duration) / old_duration
assert regression < 0.10, f"Performance regression: {regression:.1%}"
```

---

### Testing

**Requirement**: Comprehensive Scanner Testing

All scanners must have test coverage for:

1. Model validation (Pydantic models)
2. Scanner functionality (detection logic)
3. Output structure (summary, results, metadata)
4. Serialization (JSON, YAML round-trips)
5. CLI interface (argument parsing, output formats)
6. Backward compatibility (old imports, legacy format)

**Scenario**: Scanner Test Suite Structure

```python
# tests/test_scanners/test_signal.py

class TestSignalModels:
    """Test Pydantic model validation."""
    def test_signal_info_validation(self): ...
    def test_signal_summary_validation(self): ...

class TestSignalScanner:
    """Test scanner functionality."""
    def test_detects_built_in_signals(self): ...
    def test_detects_custom_signals(self): ...

class TestSignalOutput:
    """Test output structure."""
    def test_output_has_required_fields(self): ...
    def test_summary_calculation(self): ...

class TestSignalSerialization:
    """Test serialization."""
    def test_json_round_trip(self): ...
    def test_yaml_export(self): ...

class TestSignalCLI:
    """Test CLI interface."""
    def test_cli_arguments(self): ...
    def test_output_formats(self): ...
```

---

## Non-Requirements

**Out of Scope**:

1. **Async Scanner APIs**: Scanners remain synchronous (file I/O is bottleneck)
2. **Scanner Configuration Files**: No config file support (use CLI flags)
3. **Scanner Plugins**: No dynamic scanner loading (import explicitly)
4. **Real-time Scanning**: Batch scanning only, no file watchers
5. **Distributed Scanning**: Single-machine execution only

---

## Migration Guide

### For Users

**Import Path Changes**:

```python
# Old
from upcast.http_request_scanner import scan_http_requests

# New
from upcast.scanners.http_request import scan_http_requests
```

**Output Format Changes**:

```python
# Old: Direct access to results
output = scan_signals(path)
signals = output["signals"]

# New: Access through results field
output = scan_signals(path)
signals = output.results["signals"]
summary = output.summary.total_count
```

**CLI Usage** (unchanged):

```bash
# Commands remain the same
$ upcast scan-signals /project -o output.yaml
```

### For Developers

**Adding New Scanners**:

1. Create module in `upcast/scanners/`
2. Define Pydantic models (Summary, Info, Output)
3. Extend `BaseScanner` class
4. Use common CLI utilities
5. Use common export functions
6. Add documentation in `docs/scanners/`
7. Write comprehensive tests

**Scanner Template**:

```python
# upcast/scanners/my_scanner.py

from pathlib import Path
from pydantic import BaseModel, Field
from upcast.common.scanner_base import BaseScanner
from upcast.common.models import ScannerSummary, ScannerOutput

class MyItemInfo(BaseModel):
    name: str
    file: str
    line: int

class MySummary(ScannerSummary):
    custom_field: int

class MyOutput(ScannerOutput[list[MyItemInfo]]):
    summary: MySummary
    results: list[MyItemInfo]

class MyScanner(BaseScanner[MyOutput]):
    def scan(self, path: Path) -> MyOutput:
        # Implementation
        ...

    def scan_file(self, file_path: Path) -> list[MyItemInfo]:
        # File scanning
        ...

def scan_my_items(path: Path) -> MyOutput:
    scanner = MyScanner()
    return scanner.scan(path)
```
