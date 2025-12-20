# Design: Scanner Architecture Refactor

## Architecture Overview

```
upcast/
├── scanners/                    # New organized scanner package
│   ├── __init__.py             # Re-exports all scanners
│   ├── blocking_operation.py   # Scanner implementations
│   ├── concurrency_pattern.py
│   ├── ...
│   └── unit_test.py
├── common/                      # Shared utilities
│   ├── models.py               # Base Pydantic models (NEW)
│   ├── export.py               # Universal export functions (ENHANCED)
│   ├── cli.py                  # Shared CLI utilities (NEW)
│   └── scanner_base.py         # Abstract base classes (NEW)
└── [old modules]               # Deprecated wrappers (TEMPORARY)
    ├── blocking_operation_scanner/  # Import from new location + warning
    ├── ...
```

## Type System Design

### Base Models Hierarchy

```python
# upcast/common/models.py

from pydantic import BaseModel, Field, ConfigDict
from typing import TypeVar, Generic, Any
from datetime import datetime

class ScannerSummary(BaseModel):
    """Base summary model. All scanners extend this."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    total_count: int = Field(ge=0, description="Total items found")
    files_scanned: int = Field(ge=0, description="Number of files scanned")
    scan_duration_ms: int | None = Field(None, ge=0, description="Scan duration")

T = TypeVar('T')

class ScannerOutput(BaseModel, Generic[T]):
    """Base output model. All scanners use this."""
    model_config = ConfigDict(extra="allow")  # Allow scanner-specific metadata

    summary: ScannerSummary
    results: T
    metadata: dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for export."""
        return self.model_dump(mode="python", exclude_none=True)

    def to_json(self, **kwargs) -> str:
        """Export as JSON string."""
        return self.model_dump_json(**kwargs)
```

### Scanner-Specific Models

Each scanner defines its own summary and result types:

```python
# upcast/scanners/http_request.py

from upcast.common.models import ScannerSummary, ScannerOutput
from pydantic import BaseModel, Field, HttpUrl

class HttpRequestUsage(BaseModel):
    """Single usage of an HTTP request."""
    file: str
    line: int
    context_code: str

class HttpRequestInfo(BaseModel):
    """Information about a detected HTTP request."""
    url: str  # Normalized URL
    method: str
    library: str = Field(pattern="^(requests|urllib|httpx|aiohttp)$")
    has_timeout: bool
    timeout_value: int | None = None
    is_async: bool
    usages: list[HttpRequestUsage]

class HttpRequestSummary(ScannerSummary):
    """Summary specific to HTTP request scanner."""
    unique_urls: int = Field(ge=0)
    libraries_used: list[str]
    requests_without_timeout: int = Field(ge=0)
    async_requests: int = Field(ge=0)
    session_based_count: int = Field(ge=0)

class HttpRequestOutput(ScannerOutput[dict[str, HttpRequestInfo]]):
    """Output model for HTTP request scanner."""
    summary: HttpRequestSummary
    results: dict[str, HttpRequestInfo]  # URL -> info mapping
```

## Module Organization Design

### Old Structure → New Structure Mapping

| Old Module                    | New Module                       | Notes                        |
| ----------------------------- | -------------------------------- | ---------------------------- |
| `blocking_operation_scanner/` | `scanners/blocking_operation.py` | Single file, simpler         |
| `http_request_scanner/`       | `scanners/http_request.py`       | Single file if < 500 LOC     |
| `django_model_scanner/`       | `scanners/django_model/`         | Keep as package if > 500 LOC |

**Decision**: Most scanners → single `.py` file. Complex scanners (django_model, django_url) → packages.

### Import Design

**Public API (stable):**

```python
# Users import from top-level scanners module
from upcast.scanners import (
    scan_http_requests,
    scan_env_vars,
    scan_django_models,
)

# Or module-level
from upcast.scanners.http_request import scan, HttpRequestOutput
```

**Internal API (flexible):**

```python
# Internal use only, not guaranteed stable
from upcast.scanners.http_request import _normalize_url, _detect_library
```

**Deprecated Imports (temporary):**

```python
# Old import path - works with warning
from upcast.http_request_scanner import scan_http_requests
# Emits: DeprecationWarning: upcast.http_request_scanner is deprecated,
#        use upcast.scanners.http_request instead. Will be removed in v1.0.0
```

## Common Abstractions Design

### Abstract Scanner Base Class

```python
# upcast/common/scanner_base.py

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar
from upcast.common.models import ScannerOutput

T = TypeVar('T', bound=ScannerOutput)

class BaseScanner(ABC, Generic[T]):
    """Abstract base class for all scanners."""

    def __init__(
        self,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        verbose: bool = False,
    ):
        self.include_patterns = include_patterns or ["**/*.py"]
        self.exclude_patterns = exclude_patterns or []
        self.verbose = verbose

    @abstractmethod
    def scan(self, path: Path) -> T:
        """Scan the given path and return typed results."""
        pass

    @abstractmethod
    def scan_file(self, file_path: Path) -> Any:
        """Scan a single file. Returns scanner-specific intermediate results."""
        pass

    def get_files_to_scan(self, path: Path) -> list[Path]:
        """Get list of files to scan based on include/exclude patterns."""
        # Shared logic for file discovery
        ...

    def should_scan_file(self, file_path: Path) -> bool:
        """Check if file should be scanned."""
        # Shared logic for filtering
        ...
```

### Unified Export Functions

```python
# upcast/common/export.py (enhanced)

from pathlib import Path
from typing import Literal
from pydantic import BaseModel

def export_scanner_output(
    output: BaseModel,
    format: Literal["yaml", "json"],
    file_path: Path | None = None,
) -> str:
    """
    Universal export function for all scanner outputs.

    Handles both Pydantic models and legacy dict outputs.
    Replaces 12 scattered format_*_output functions.
    """
    if isinstance(output, BaseModel):
        data = output.model_dump(mode="python", exclude_none=True)
    else:
        data = output  # Legacy dict support

    if format == "json":
        return export_to_json(data, file_path)
    else:
        return export_to_yaml(data, file_path)

def export_legacy_format(
    output: BaseModel,
    scanner_name: str,
    format: Literal["yaml", "json"],
    file_path: Path | None = None,
) -> str:
    """
    Export in legacy format for backward compatibility.
    Maps new unified structure back to old structure.
    """
    # Scanner-specific transformation logic
    ...
```

### Shared CLI Utilities

```python
# upcast/common/cli.py (new)

from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Callable

def create_scanner_parser(
    prog: str,
    description: str,
    version: str,
) -> ArgumentParser:
    """Create standard argument parser for scanners."""
    parser = ArgumentParser(prog=prog, description=description)
    parser.add_argument("--version", action="version", version=version)
    add_scanner_arguments(parser)
    return parser

def add_scanner_arguments(parser: ArgumentParser) -> None:
    """Add common scanner CLI arguments."""
    parser.add_argument("path", type=Path, help="Path to scan")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output file path (stdout if not specified)"
    )
    parser.add_argument(
        "--format",
        choices=["yaml", "json"],
        default="yaml",
        help="Output format"
    )
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="File patterns to include (can be specified multiple times)"
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="File patterns to exclude"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--legacy-format",
        action="store_true",
        help="Output in legacy format (deprecated)"
    )

def run_scanner_cli(
    scan_func: Callable[[Path], BaseModel],
    args: Namespace,
) -> None:
    """Common CLI execution logic for scanners."""
    from upcast.common.export import export_scanner_output, export_legacy_format

    # Run scan
    output = scan_func(args.path)

    # Export
    if args.legacy_format:
        result = export_legacy_format(output, scan_func.__name__, args.format, args.output)
    else:
        result = export_scanner_output(output, args.format, args.output)

    if not args.output:
        print(result)
```

## Output Format Standardization

### Unified Structure

**All scanners output:**

```yaml
summary:
  # Base fields (required)
  total_count: <int>
  files_scanned: <int>
  scan_duration_ms: <int|null>

  # Scanner-specific fields
  <scanner_field_1>: <value>
  <scanner_field_2>: <value>

results:
  # Scanner-specific structure
  # Can be: list, dict, nested objects

metadata:
  scanner_name: "http-request"
  scanner_version: "0.5.0"
  scan_timestamp: "2025-12-21T10:00:00Z"
  # Additional scanner-specific metadata
```

### Per-Scanner Result Structures

**HTTP Request Scanner:**

```yaml
results:
  "https://api.example.com/...":
    url: "https://api.example.com/..."
    method: "GET"
    library: "requests"
    has_timeout: true
    timeout_value: 30
    is_async: false
    usages:
      - file: "src/api.py"
        line: 42
        context_code: "response = requests.get(url, timeout=30)"
```

**Signal Scanner:**

```yaml
results:
  signals:
    - name: "user_logged_in"
      type: "built-in"
      sender: "User"
      file: "signals.py"
      line: 10
      receivers:
        - function: "send_welcome_email"
          file: "handlers.py"
          line: 25
```

**Environment Variable Scanner:**

```yaml
results:
  variables:
    DATABASE_URL:
      name: "DATABASE_URL"
      usages:
        - file: "settings.py"
          line: 15
          access_type: "os.environ"
          has_default: false
```

## Implementation Strategy

### Phase 1: Foundation (Week 1)

1. **Create base models** (`common/models.py`)
2. **Create base scanner class** (`common/scanner_base.py`)
3. **Create CLI utilities** (`common/cli.py`)
4. **Enhance export functions** (`common/export.py`)

**Testing**: Unit tests for base classes, no integration yet

### Phase 2: Pilot Scanner (Week 1-2)

1. **Choose simple scanner**: `signal_scanner` (smallest, no existing dataclass)
2. **Create `scanners/signal.py`** with new structure
3. **Define `SignalOutput` model** with Pydantic
4. **Update CLI** to use new common utilities
5. **Create deprecation wrapper** in old `signal_scanner/`

**Testing**: Ensure all signal_scanner tests pass with new implementation

### Phase 3: Migrate Remaining Scanners (Week 2-4)

**Batch 1 (Simple - no existing dataclass):**

- cyclomatic_complexity
- django_url
- unit_test

**Batch 2 (Medium - partial dataclass):**

- blocking_operation
- concurrency_pattern
- django_settings
- env_var
- prometheus_metrics

**Batch 3 (Complex - full dataclass):**

- exception_handler
- http_request
- django_model (largest, keep as package)

**Testing**: Each scanner's tests updated and passing before next batch

### Phase 4: Documentation (Week 4-5)

1. **Create `docs/scanners/` directory**
2. **Write per-scanner documentation** (template-driven)
3. **Generate schema documentation** from Pydantic models
4. **Update main README** with new import examples
5. **Write migration guide**

### Phase 5: Cleanup (Week 5)

1. **Remove deprecated modules** (if timeline allows, otherwise defer to v1.0.0)
2. **Update all internal imports**
3. **Remove legacy export functions**
4. **Final test sweep**: all 617 tests + new validation tests

## Testing Strategy

### Model Validation Tests

```python
# tests/test_models/test_scanner_output.py

def test_scanner_output_requires_summary():
    """All scanner outputs must have summary."""
    with pytest.raises(ValidationError):
        HttpRequestOutput(results={})  # Missing summary

def test_scanner_output_freezes_summary():
    """Summaries are immutable."""
    output = HttpRequestOutput(summary=..., results={})
    with pytest.raises(ValidationError):
        output.summary.total_count = 999

def test_scanner_output_round_trip():
    """Output can be serialized and deserialized."""
    original = create_http_request_output()
    json_str = original.to_json()
    restored = HttpRequestOutput.model_validate_json(json_str)
    assert restored == original
```

### Integration Tests

```python
# tests/integration/test_scanner_consistency.py

@pytest.mark.parametrize("scanner_name", ALL_SCANNERS)
def test_scanner_has_unified_output(scanner_name):
    """All scanners return ScannerOutput."""
    scanner = get_scanner(scanner_name)
    output = scanner.scan(TEST_PROJECT_PATH)

    assert isinstance(output, ScannerOutput)
    assert hasattr(output, "summary")
    assert hasattr(output, "results")
    assert hasattr(output, "metadata")

@pytest.mark.parametrize("scanner_name", ALL_SCANNERS)
def test_scanner_summary_has_base_fields(scanner_name):
    """All scanner summaries have required base fields."""
    scanner = get_scanner(scanner_name)
    output = scanner.scan(TEST_PROJECT_PATH)

    assert output.summary.total_count >= 0
    assert output.summary.files_scanned >= 0
```

### Backward Compatibility Tests

```python
# tests/test_backward_compatibility.py

def test_legacy_import_works_with_warning():
    """Old import paths work but emit warnings."""
    with pytest.warns(DeprecationWarning, match="use upcast.scanners.http_request"):
        from upcast.http_request_scanner import scan_http_requests

def test_legacy_format_flag():
    """--legacy-format produces old output structure."""
    result = run_cli(["scan-http-requests", ".", "--legacy-format", "--format", "json"])
    output = json.loads(result)

    # Old format: no summary/results/metadata wrapper
    assert "summary" in output  # But at top level
    assert "https://..." in output  # URLs as keys
    assert "results" not in output  # No wrapper
```

## Risk Mitigation

### Risk 1: Breaking Changes for Users

**Mitigation:**

- Maintain old import paths with deprecation warnings
- Provide `--legacy-format` CLI flag for 1 minor version
- Clear migration guide with examples
- Gradual deprecation timeline (v0.5.0 → v0.6.0 → v1.0.0)

### Risk 2: Performance Regression

**Mitigation:**

- Benchmark before/after for each scanner
- Use Pydantic v2 for better performance
- Lazy validation where possible
- Profile and optimize hot paths

### Risk 3: Complex Migration

**Mitigation:**

- Pilot with simplest scanner first
- Batch migration by complexity
- Comprehensive test coverage
- Rollback plan (keep old code until validation complete)

### Risk 4: Documentation Overhead

**Mitigation:**

- Template-driven documentation generation
- Auto-generate schema docs from Pydantic models
- Dedicate Week 4-5 exclusively to documentation
- Make documentation part of definition of done

## Success Metrics

1. **Code Quality**: All scanners use unified base classes ✅
2. **Type Safety**: 100% of scanner outputs are Pydantic models ✅
3. **Test Coverage**: All 617 existing tests pass + 50+ new validation tests ✅
4. **Performance**: < 10% regression in scan time ✅
5. **Documentation**: Complete docs for all 12 scanners ✅
6. **Backward Compatibility**: Old imports work with warnings ✅
