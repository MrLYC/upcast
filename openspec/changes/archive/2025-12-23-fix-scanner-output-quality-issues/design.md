# Design: Scanner Output Quality Improvements

## Context

Integration testing revealed systematic false positives and missing functionality across 5 scanners. This design addresses root causes and establishes patterns for quality assurance.

## Root Cause Analysis

### 1. Concurrency Scanner: Overly Broad Pattern Matching

**Issue**: Matches class names like "Process" without verifying module origin

**Root Cause**: Pattern detection uses simple name matching instead of qualified name resolution

**Example False Positive**:

```python
# This is detected as process creation:
PlainProcess(name="web", replicas=2)  # attrs/Pydantic dataclass

# This is what we actually want:
multiprocessing.Process(target=worker_fn)  # Real process creation
```

**Technical Debt**: Similar issue exists for Thread detection and potentially other patterns

### 2. Django Settings Scanner: Incomplete Implementation

**Issue**: Only `usage` mode works; `definitions` mode stub exists but not implemented

**Root Cause**: Original implementation focused on usage tracking; definition extraction was deferred

**Missing Functionality**:

```python
# settings.py
DEBUG = True
DATABASE_URL = os.getenv("DATABASE_URL")

# Should output:
# {
#   "DEBUG": {"value": True, "type": "bool", "location": "settings.py:10"},
#   "DATABASE_URL": {"value": "<from_env>", "type": "str", "location": "settings.py:11"}
# }
```

**Impact**: Cannot generate complete settings inventory for migration planning

### 3. Env Vars Scanner: Context-Free String Extraction

**Issue**: Extracts variable names from any string literal in source code

**Root Cause**: String extraction logic doesn't validate parent node context

**Example False Positive**:

```python
# This string is extracted as env var "id":
api_client.post(
    f'/api/bkapps/applications/{code}/config_vars/',
    {'key': 'A1', 'value': 'foo', 'environment_name': '_global_', 'description': 'foo'}
).data['id']
```

**Why It Happens**: Scanner sees string `'id'` and reports it without checking it's a dict key access, not `os.getenv('id')`

### 4. HTTP Requests Scanner: Uninformative Placeholder Values

**Issue**: Outputs `{"<dynamic>": "..."}` for JSON bodies that can't be statically inferred

**Root Cause**: Placeholder was added to preserve field in output schema, but provides no value

**Better Approach**:

```yaml
# Current (unhelpful):
json_body:
  <dynamic>: "..."
# Proposed (omit field):
# (no json_body field)
```

**Rationale**: Optional field absence conveys "not statically determinable" more clearly than placeholder

### 5. Unit Tests Scanner: File Discovery Failure

**Issue**: Returns empty results despite test files existing

**Root Cause**: Unknown - needs debugging. Potential causes:

- File pattern matching excludes test directories
- Path normalization issues
- AST parsing failures on test files
- Silent errors in detection logic

**Investigation Needed**: Add comprehensive logging to diagnose

## Design Decisions

### Decision 1: Strict Module Path Verification

**Choice**: Require qualified name resolution for concurrency patterns

**Alternatives**:

1. Keep simple name matching, filter false positives post-processing
2. Use heuristics (e.g., "if name is Process and in threading module, likely real")
3. Require explicit module path verification

**Selected**: Option 3 (explicit verification)

**Rationale**:

- Prevents entire class of false positives (dataclasses, models, custom wrappers)
- Astroid provides robust module resolution
- Slightly slower but accuracy > speed for code analysis
- Sets precedent for other scanners

**Implementation**: Use `get_import_info()` to resolve qualified names, reject unresolved

### Decision 2: Restore Definitions Mode vs. Deprecate

**Choice**: Fully implement definitions mode rather than remove it

**Alternatives**:

1. Remove definitions mode, document as usage-only scanner
2. Implement definitions mode as separate scanner tool
3. Complete original spec by implementing definitions mode

**Selected**: Option 3 (complete implementation)

**Rationale**:

- Original spec defined this capability
- Definition scanning complements usage scanning for migration analysis
- Existing `parse_settings_module()` utility already does heavy lifting
- Small effort (2-3 hours) for significant value

**Implementation**: Call existing parser, map to output model, handle multiple settings files

### Decision 3: Context-Aware String Extraction

**Choice**: Validate parent node context before reporting strings

**Alternatives**:

1. Keep current extraction, document limitations
2. Post-process to filter known false positive patterns
3. Only extract strings from validated env access contexts

**Selected**: Option 3 (context validation)

**Rationale**:

- Addresses root cause rather than symptoms
- AST provides parent node access for context checking
- More robust than keyword filtering
- Generalizable pattern for other scanners

**Implementation**: Before reporting, verify parent is `Call` node with env access function

### Decision 4: Optional JSON Body Field

**Choice**: Make `json_body` optional; omit when uninferrable

**Alternatives**:

1. Keep placeholder, document meaning
2. Add `inferrable: bool` field alongside body
3. Omit field entirely when not determinable

**Selected**: Option 3 (omit field)

**Rationale**:

- Optional fields in Pydantic naturally express "not present"
- Reduces output clutter
- Users can check field presence to determine if static analysis succeeded
- Aligns with Python idiom of "explicit is better than implicit"

**Implementation**: Return `None` from extraction function; Pydantic excludes None optionals

### Decision 5: Debug-First Approach for Unit Tests

**Choice**: Thoroughly diagnose before implementing fix

**Alternatives**:

1. Rewrite scanner from scratch
2. Add logging and debug systematically
3. Compare with similar working scanners

**Selected**: Option 2 (debug systematically)

**Rationale**:

- Scanner architecture is sound (works for other types)
- Likely a subtle bug or configuration issue
- Logging will reveal exact failure point
- May uncover issues in other scanners

**Implementation**: Add debug logs at each stage: file discovery → parsing → detection → output

## Cross-Cutting Concerns

### Quality Assurance Pattern

**Observation**: All issues stem from lack of validation

**Proposed Pattern**: Scanner output validation

```python
def validate_output(output: ScannerOutput) -> List[ValidationIssue]:
    """Validate scanner output for common quality issues."""
    issues = []

    # Check for placeholder values
    if "<dynamic>" in str(output):
        issues.append("Contains placeholder values")

    # Check for suspiciously high count
    if output.summary.total_count > 1000:
        issues.append("Unusually high detection count - possible false positives")

    # Scanner-specific rules
    ...

    return issues
```

**Benefits**: Catch quality issues before they reach users

**Cost**: Additional development and maintenance

**Decision**: Defer to separate quality framework proposal

### Testing Strategy

**Unit Tests**: Each fix gets targeted test

- Concurrency: Test dataclass named "Process"
- Env vars: Test API call with env-like strings
- HTTP: Test uninferrable JSON body
- Unit tests: Test simple pytest file

**Integration Tests**: Verify on blueking-paas

- Current: 6/12 scanners generated output
- After fixes: All 12 should generate quality output
- Baseline updates document improvements

**Regression Prevention**: Tests remain in suite permanently

### Performance Implications

**Qualified Name Resolution**: ~10-20% slower than name matching

- Acceptable tradeoff for accuracy
- Still completes in <1s for typical files

**Context Validation**: Minimal overhead (single parent node check)

**Overall**: No user-visible performance impact expected

## Migration Path

1. **Phase 1**: Fix all 5 scanner issues
2. **Phase 2**: Run integration tests, update baselines
3. **Phase 3**: Add regression tests
4. **Phase 4**: Document changes

**Backwards Compatibility**: All changes are bug fixes

- Output may have fewer entries (removed false positives)
- Output may have new fields (restored definitions mode)
- No breaking changes to output schema

**User Communication**:

- Release notes highlight quality improvements
- Document specific false positive categories fixed
- Recommend re-running scans to get corrected output

## Open Questions

1. **Confidence Scores**: Should we add confidence level to detections?

   - Pro: Users can filter uncertain findings
   - Con: Adds complexity; binary detection is clearer
   - Decision: Defer - focus on improving detection accuracy first

2. **Telemetry**: Should we track false positive rates?

   - Pro: Quantify improvements, identify future issues
   - Con: Privacy concerns, implementation overhead
   - Decision: Consider for future quality initiative

3. **Validation Framework**: Separate proposal needed?
   - Pro: Systematic approach to output quality
   - Con: Scope creep for this fix
   - Decision: Note as future work in task 7.2
