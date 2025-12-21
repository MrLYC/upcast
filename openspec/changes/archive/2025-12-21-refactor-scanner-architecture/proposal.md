# Proposal: Refactor Scanner Architecture

## What Changes

Refactor the scanner module architecture to improve maintainability, type safety, and enable future analysis capabilities:

1. **Module Reorganization**: Rename scanner modules from `xxx_scanner` to `scanners.xxx` for better namespace organization
2. **Strongly Typed Models**: Introduce Pydantic models for all scanner outputs to ensure type safety and enable validation
3. **Unified Output Structure**: Standardize output format across all scanners with consistent `summary` and result fields
4. **Common I/O Abstractions**: Extract input/output logic into `common` module for reuse across scanners
5. **Comprehensive Documentation**: Create `docs/` directory with detailed documentation for each scanner's purpose, output fields, and value rules

## Why

**Current Problems:**

1. **Inconsistent Output Formats**: Each scanner has different output structures, making it difficult to build analysis tools that consume scanner results
2. **Lack of Type Safety**: Scanner outputs use plain dictionaries without type validation, leading to potential runtime errors
3. **Duplicated I/O Logic**: Each scanner implements its own export functions with repeated code for YAML/JSON formatting
4. **Poor Discoverability**: No centralized documentation explaining scanner capabilities, output schemas, or usage patterns
5. **Namespace Pollution**: Flat module structure (`xxx_scanner`) makes it harder to organize and discover scanners

**Benefits:**

- **Type Safety**: Pydantic models provide automatic validation, better IDE support, and clear contracts
- **Consistency**: Unified output format makes it easier to build downstream analysis and reporting tools
- **Maintainability**: Shared I/O abstractions reduce code duplication and simplify adding new scanners
- **Developer Experience**: Clear documentation and typed models improve onboarding and reduce errors
- **Future-Ready**: Standardized interfaces enable building analysis modules that work across multiple scanners

## How

### Phase 1: Module Reorganization

**Create new `scanners` package:**

```
upcast/
  scanners/
    __init__.py
    blocking_operation.py    # from blocking_operation_scanner
    concurrency_pattern.py   # from concurrency_pattern_scanner
    cyclomatic_complexity.py # from cyclomatic_complexity_scanner
    django_model.py          # from django_model_scanner
    django_settings.py       # from django_settings_scanner
    django_url.py            # from django_url_scanner
    env_var.py               # from env_var_scanner
    exception_handler.py     # from exception_handler_scanner
    http_request.py          # from http_request_scanner
    prometheus_metrics.py    # from prometheus_metrics_scanner
    signal.py                # from signal_scanner
    unit_test.py             # from unit_test_scanner
```

**Migration Strategy:**

- Keep old `xxx_scanner` modules as deprecated wrappers that import from new location
- Add deprecation warnings to old modules
- Update all internal imports to use new paths
- Update CLI commands to use new module paths while maintaining backward compatibility

### Phase 2: Strongly Typed Models

**Create Pydantic base models in `upcast/common/models.py`:**

```python
from pydantic import BaseModel, Field
from typing import Any, TypeVar, Generic

class ScannerSummary(BaseModel):
    """Base summary model for all scanners."""
    total_count: int = Field(description="Total items found")
    files_scanned: int = Field(description="Number of files scanned")
    scan_duration_ms: int | None = Field(None, description="Scan duration in milliseconds")

class ScannerOutput(BaseModel, Generic[T]):
    """Base output model for all scanners."""
    summary: ScannerSummary
    results: T
    metadata: dict[str, Any] = Field(default_factory=dict)
```

**Per-Scanner Models:**
Each scanner defines its own result models extending the base:

```python
# upcast/scanners/http_request.py
class HttpRequestSummary(ScannerSummary):
    unique_urls: int
    libraries_used: list[str]
    requests_without_timeout: int
    async_requests: int
    session_based_count: int

class HttpRequestResult(BaseModel):
    url: str
    method: str
    library: str
    usages: list[HttpRequestUsage]

class HttpRequestOutput(ScannerOutput[dict[str, HttpRequestResult]]):
    summary: HttpRequestSummary
    results: dict[str, HttpRequestResult]
```

### Phase 3: Common I/O Abstractions

**Extend `upcast/common/export.py`:**

```python
from typing import TypeVar, Protocol
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class Scanner(Protocol[T]):
    """Protocol for all scanners."""
    def scan(self, path: Path) -> T: ...

def export_scanner_output(
    output: BaseModel,
    format: Literal["yaml", "json"],
    file_path: Path | None = None
) -> str:
    """Universal export function for scanner outputs."""
    if format == "json":
        data = output.model_dump(mode="json")
        return export_to_json(data, file_path)
    else:
        data = output.model_dump(mode="python")
        return export_to_yaml(data, file_path)
```

**Shared CLI argument parsing:**

```python
# upcast/common/cli.py
def add_scanner_arguments(parser: ArgumentParser) -> None:
    """Add common scanner CLI arguments."""
    parser.add_argument("path", help="Path to scan")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("--format", choices=["yaml", "json"], default="yaml")
    parser.add_argument("-v", "--verbose", action="store_true")
    # ... include/exclude patterns, etc.
```

### Phase 4: Unified Output Structure

**Before (inconsistent):**

```yaml
# http-request-scanner
summary: { ... }
https://api.example.com: { ... }

# signal-scanner
signals: [...]

# env-var-scanner
DATABASE_URL: { ... }
```

**After (consistent):**

```yaml
summary:
  total_count: 10
  files_scanned: 5
  scan_duration_ms: 250
  # scanner-specific summary fields

results:
  # scanner-specific results structure

metadata:
  scanner_version: "0.5.0"
  scan_timestamp: "2025-12-21T10:00:00Z"
```

### Phase 5: Documentation

**Create `docs/scanners/` directory:**

```
docs/
  scanners/
    README.md                    # Overview of all scanners
    blocking-operation.md        # Detailed doc for each scanner
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
```

**Documentation Template:**

````markdown
# Scanner Name

## Purpose

Brief description of what this scanner detects and why it's useful.

## Usage

```bash
upcast scan-xxx /path/to/project -o output.yaml
```
````

## Output Schema

### Summary Fields

- `field_name` (type): Description and rules

### Result Fields

- `field_name` (type): Description and rules

## Examples

### Input Code

```python
# example code
```

### Output

```yaml
# example output
```

## Implementation Notes

Technical details about how detection works.

```

## Impact

### Users Affected
- All users of the scanner modules
- Developers building analysis tools on top of upcast
- Contributors adding new scanners

### Migration Path

**Breaking Changes (Major Version Bump Required):**
- Module import paths change from `upcast.xxx_scanner` to `upcast.scanners.xxx`
- Output format changes to unified structure with `summary`/`results`/`metadata`

**Backward Compatibility:**
- Old import paths remain available with deprecation warnings for 1 minor version
- CLI commands remain unchanged (use new paths internally)
- New `--legacy-format` flag to output old format for migration period

**Migration Steps:**
1. Update imports: `from upcast.http_request_scanner import X` → `from upcast.scanners.http_request import X`
2. Update result parsing to expect `output.results` instead of direct fields
3. Update summary parsing to expect `output.summary` instead of mixed format
4. Remove `--legacy-format` flag usage after migration

### Performance Considerations
- Pydantic model validation adds ~5-10% overhead (negligible for I/O-bound operations)
- Unified export functions may be slightly slower due to generic handling
- Documentation has zero runtime impact

## Alternatives Considered

### Alternative 1: Keep Current Structure, Only Add Types

**Pros**: Minimal disruption, gradual adoption
**Cons**: Doesn't address inconsistency or duplication issues
**Decision**: Rejected - half measures don't solve the core problems

### Alternative 2: Use TypedDict Instead of Pydantic

**Pros**: Standard library, no dependencies, lighter weight
**Cons**: No runtime validation, less feature-rich, harder to serialize
**Decision**: Rejected - Pydantic's benefits (validation, serialization, docs) outweigh the cost

### Alternative 3: Create Separate Analysis Package

**Pros**: Keeps scanner code unchanged
**Cons**: Doesn't improve scanner maintainability, adds complexity
**Decision**: Rejected - better to fix the foundation first

## Open Questions

1. **Pydantic Version**: Use Pydantic v1 (current standard) or v2 (better performance)?
   - Recommendation: v2 for better performance and future-proofing

2. **Deprecation Timeline**: How long to maintain old module paths?
   - Recommendation: 1 minor version with warnings, remove in next major

3. **Versioning**: Should scanner outputs include schema version?
   - Recommendation: Yes, add to metadata for forward compatibility

4. **Configuration**: Should scanners support configuration files?
   - Recommendation: Out of scope for this refactor, consider in future change

5. **Async Support**: Should scanner APIs support async operations?
   - Recommendation: Out of scope, file I/O is the bottleneck

## Success Criteria

1. **Code Quality**:
   - ✅ All scanners use Pydantic models for outputs
   - ✅ All scanners use common I/O abstractions
   - ✅ Zero code duplication in export logic
   - ✅ All scanners follow unified output structure

2. **Documentation**:
   - ✅ Complete documentation for all 12 scanners
   - ✅ Schema documentation generated from Pydantic models
   - ✅ Migration guide published

3. **Testing**:
   - ✅ All existing tests pass with new structure
   - ✅ Type validation tests for all scanner outputs
   - ✅ Round-trip tests (serialize → deserialize) for all outputs

4. **Backward Compatibility**:
   - ✅ Old import paths work with deprecation warnings
   - ✅ `--legacy-format` flag produces old output format
   - ✅ CLI commands unchanged

5. **Performance**:
   - ✅ No more than 10% regression in scan time
   - ✅ Memory usage remains acceptable
```
