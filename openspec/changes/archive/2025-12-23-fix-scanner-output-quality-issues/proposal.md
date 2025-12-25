# Proposal: Fix Scanner Output Quality Issues

## Problem Statement

Integration testing on the `blueking-paas` project revealed several scanner output quality issues that produce false positives, missing data, or meaningless values:

1. **concurrency-patterns**: Line 35 reports `PlainProcess(...)` as `process_creation` pattern, but `PlainProcess` is a dataclass instantiation, not actual multiprocessing.Process creation
2. **django-settings**: Only outputs settings usage locations, missing settings definitions mode that was specified in the original spec
3. **env-vars**: Line 124 reports API endpoint string `'/api/bkapps/applications/{bk_app.code}/modules/{bk_module.name}/config_vars/'` as environment variable `id`, which is clearly a false positive from API call context
4. **http-requests**: Line 9 outputs `json_body: {"<dynamic>": "..."}` which provides no useful information when body content cannot be inferred
5. **unit-tests**: Outputs empty results despite `apiserver/paasng/tests/paasng/platform/engine/test_managers.py` and other test files existing in the project

These issues reduce trust in scanner output and require manual filtering to identify legitimate findings.

## Proposed Solution

### 1. Concurrency Scanner: Stricter Process Creation Detection

**Current behavior**: Detects any call to a class named "Process" as process creation
**Target behavior**: Only detect `multiprocessing.Process()` instantiations by verifying the qualified module path

**Changes**:

- In `_detect_process_creation()`, verify the call resolves to `multiprocessing.Process` via import resolution
- Skip dataclass/Pydantic model instantiations that happen to be named "Process"
- Apply same strictness to `threading.Thread` detection

### 2. Django Settings Scanner: Restore Definitions Mode

**Current behavior**: Scanner only supports `usage` mode despite spec defining `definitions` mode
**Target behavior**: When `mode=definitions`, scan settings modules and extract setting definitions with their values

**Changes**:

- Implement `_scan_definitions()` method to parse settings files
- Use existing `parse_settings_module()` from common utilities
- Output settings definitions with values, types, and source locations
- Ensure both modes work as specified in original design

### 3. Env Vars Scanner: Filter API Call False Positives

**Current behavior**: Extracts variable names from any string literal in the file, including API endpoints
**Target behavior**: Only report strings that are actually used as environment variable lookups

**Changes**:

- In extraction logic, verify the string appears in actual env access patterns (`os.getenv()`, `os.environ[]`, `env()`)
- Skip string literals from unrelated contexts (API calls, logging, etc.)
- Use AST parent node analysis to validate context before reporting

### 4. HTTP Requests Scanner: Omit Uninferrable JSON Bodies

**Current behavior**: Outputs `{"<dynamic>": "..."}` when json body cannot be inferred
**Target behavior**: Omit `json_body` field entirely when content cannot be meaningfully inferred

**Changes**:

- In JSON body extraction, return `None` instead of placeholder dict when inference fails
- Update output model to make `json_body` optional
- Only include `json_body` in output when actual static content is detected

### 5. Unit Tests Scanner: Fix Empty Output

**Current behavior**: Returns empty results despite test files existing
**Target behavior**: Detect and report pytest and unittest style tests as specified

**Changes**:

- Debug why test files are not being scanned (file pattern matching issue?)
- Ensure `test*.py` and `*_test.py` patterns work correctly
- Verify AST analysis correctly identifies test functions/methods
- Add logging to diagnose scanning process

## Success Criteria

1. Concurrency scanner: `PlainProcess` and similar dataclass instantiations are not reported as concurrency patterns
2. Django settings scanner: Running with `--mode definitions` successfully outputs setting definitions from settings files
3. Env vars scanner: API endpoint strings and other non-env-var strings are not reported
4. HTTP requests scanner: `json_body` field is omitted when content is dynamic/unknown (no more `<dynamic>` placeholders)
5. Unit tests scanner: Detects and reports tests from `test_managers.py` and other test files in blueking-paas

## Impact Assessment

- **Breaking Changes**: None - these are bug fixes that improve output quality
- **Affected Components**: 5 scanners (concurrency, django-settings, env-vars, http-requests, unit-tests)
- **Testing Requirements**: Re-run integration tests on blueking-paas and verify fixed output quality

## Implementation Approach

1. Fix issues in order of severity (most false positives first)
2. Add targeted unit tests for each fix to prevent regression
3. Update integration test baseline after fixes are validated
4. Consider adding validation rules to detect similar issues in future

## Alternatives Considered

- **Post-processing filter**: Could filter output after scanning, but this doesn't address root cause and adds complexity
- **Ignore problematic patterns**: Could document limitations, but this reduces scanner utility
- **Relaxed validation**: Could allow current behavior, but this defeats purpose of quality tooling

## Open Questions

1. Should we add telemetry to track false positive rates in scanner outputs?
2. Should we implement confidence scores for detections to flag uncertain findings?
3. Should we add a `--strict` mode that errors on ambiguous detections?
