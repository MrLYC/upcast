# Proposal: Split Location Field into File and Line Number

## Status

- **State**: draft
- **Created**: 2025-12-23
- **Owner**: AI Agent

## Why

The current `location` field in `HttpRequestUsage` and `MetricUsage` models combines file path and line number into a single string (e.g., `"apiserver/paasng/file.py:101"`). This design has several issues:

1. **Parsing Complexity**: Consumers must parse the string to extract file and line number separately
2. **Type Safety**: No validation that the format is correct (file:line)
3. **Inconsistency**: `EnvVarLocation` already uses separate `file` and `line` fields, creating API inconsistency
4. **Querying Difficulty**: Cannot filter or sort by file or line number without string parsing
5. **Maintenance**: Format changes require updating all consumers

The `EnvVarLocation` model demonstrates the better pattern:

```python
class EnvVarLocation(BaseModel):
    file: str = Field(description="File path")
    line: int | None = Field(ge=1, description="Line number")
    column: int | None = Field(ge=0, description="Column number")
    pattern: str = Field(description="Access pattern")
    code: str | None = Field(None, description="Code snippet")
```

By adopting this pattern for HTTP requests and metrics, we gain:

- Type-safe line numbers (int vs string)
- Easy filtering and sorting
- Consistent API across all scanners
- Future extensibility (can add column, code snippet, etc.)

## What Changes

### 1. Update Data Models

**`HttpRequestUsage` (upcast/models/http_requests.py)**:

- Remove: `location: str`
- Add: `file: str` and `line: int | None`
- Optional: Add `column: int | None` for future use

**`MetricUsage` (upcast/models/metrics.py)**:

- Remove: `location: str`
- Add: `file: str` and `line: int | None`
- Optional: Add `column: int | None` for future use

### 2. Update Scanner Implementations

**HTTP Request Scanner** (upcast/scanners/http_requests.py):

- Parse location string into file and line components
- Pass separate `file=` and `line=` arguments to model

**Prometheus Metrics Scanner** (upcast/scanners/prometheus_metrics.py):

- Parse location string into file and line components
- Pass separate `file=` and `line=` arguments to model

### 3. Update Example Outputs

Regenerate:

- `example/scan-results/http-requests.yaml`
- `example/scan-results/metrics.yaml`

Expected output format change:

```yaml
# Before
usages:
  - location: apiserver/paasng/file.py:101
    statement: requests.get(url)

# After
usages:
  - file: apiserver/paasng/file.py
    line: 101
    statement: requests.get(url)
```

### 4. Update Tests

Update test assertions to check `file` and `line` separately instead of combined `location`.

## Success Criteria

- [ ] `HttpRequestUsage` model has `file` and `line` fields (no `location`)
- [ ] `MetricUsage` model has `file` and `line` fields (no `location`)
- [ ] HTTP request scanner outputs separate fields
- [ ] Metrics scanner outputs separate fields
- [ ] Example outputs updated and validated
- [ ] All tests pass
- [ ] Consistent with `EnvVarLocation` pattern

## Out of Scope

- Changes to other scanner models (they already use correct pattern or don't have location)
- Adding `column` or `code` fields (can be added later if needed)
- Migrating existing output files (breaking change, users update parsers)

## Breaking Change Notice

This is a **BREAKING CHANGE** for consumers parsing `http-requests.yaml` and `metrics.yaml`:

**Before**:

```python
location = usage["location"]
file, line = location.split(":")
```

**After**:

```python
file = usage["file"]
line = usage["line"]
```

Migration is straightforward as the information is still present, just structured differently.

## Dependencies

None - this change is self-contained within the scanner outputs.

## Related

- **Pattern**: Follows `EnvVarLocation` model design
- **Specs**: Updates data-models, http-request-scanner, prometheus-metrics-scanner
