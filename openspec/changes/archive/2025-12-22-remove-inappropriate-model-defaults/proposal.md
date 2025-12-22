# Proposal: Remove Inappropriate Model Field Defaults

**Status**: PROPOSED

## What Changes

Remove inappropriate `default=` parameter from Pydantic model fields where the scanner always provides explicit values, preventing silent omissions of required data.

**Affected Models**:

- `SignalUsage` (`signals.py`): Remove `default=0` from `column` field
- `SignalSummary` (`signals.py`): Remove `default=0` from 6 count fields
- `ConcurrencyUsage` (`concurrency.py`): Remove `default=0` from `column` field
- `BlockingOperation` (`blocking_operations.py`): Remove `default=0` from `column` field
- `SettingsLocation` (`django_settings.py`): Remove `default=0` from `column` field
- `EnvVarLocation` (`env_vars.py`): Remove `default=0` from `column` field
- `HttpRequestUsage` (`http_requests.py`): Remove `default=False` from `session_based` and `is_async` fields
- `MetricInfo` (`metrics.py`): Remove `default=False` from `custom_collector` field
- `UrlPattern` (`django_urls.py`): Remove `default=False` from `is_partial` and `is_conditional` fields

**NOT Affected** (keeping defaults as they are appropriate):

- `ComplexityResult.comment_lines` and `code_lines`: May legitimately be 0 when extraction fails
- `ExceptClause` log/control flow counts: May legitimately be 0 when not present

## Why

**Problem**: Many model fields have `default=` values that mask missing assignments in scanner implementations. When a scanner forgets to assign a field, the default silently provides a value instead of raising a validation error.

**Impact of Current Defaults**:

1. **Column Numbers**: Fields like `column: int = Field(default=0, ...)` hide when scanners fail to extract actual column information from AST nodes. Zero is a valid column number, making bugs invisible.

2. **Boolean Flags**: Fields like `session_based: bool = Field(default=False, ...)` hide when scanners don't evaluate the condition. If logic is broken, False appears correct.

3. **Summary Counts**: Fields in `SignalSummary` with `default=0` hide when summary calculation is incomplete. Missing aggregation logic silently reports zero counts.

**Real-World Example**:

```python
# Current (buggy scanner doesn't fail):
SignalUsage(
    file="app/signals.py",
    line=42,
    # column forgotten - defaults to 0 silently
)

# After fix (buggy scanner raises ValidationError):
SignalUsage(
    file="app/signals.py",
    line=42,
    # column missing - ValidationError raised immediately
)
```

**Why These Defaults Are Wrong**:

1. **Column is always determinable**: Every AST node has `col_offset` attribute
2. **Boolean flags are always evaluated**: Scanners explicitly check conditions
3. **Summary counts are always calculated**: Aggregation logic always runs
4. **Not optional fields**: These fields are not marked `Optional[...]` in type hints

**Contrast with Appropriate Defaults**:

- `ComplexityResult.comment_lines = Field(default=0)`: **Correct** - tokenization may fail gracefully
- `ExceptClause.pass_count = Field(default=0)`: **Correct** - zero is semantically meaningful (no pass statements)

## How

### Phase 1: Remove Column Field Defaults

Remove `default=0` from `column` fields in:

- `SignalUsage` (signals.py)
- `ConcurrencyUsage` (concurrency.py)
- `BlockingOperation` (blocking_operations.py)
- `SettingsLocation` (django_settings.py)
- `EnvVarLocation` (env_vars.py)

Change from:

```python
column: int = Field(default=0, ge=0, description="Column number")
```

To:

```python
column: int = Field(..., ge=0, description="Column number")
```

**Scanner Updates**:

- Verify all scanners explicitly assign `column=node.col_offset`
- Remove any `or 0` fallbacks (e.g., `node.col_offset or 0`)
- Ensure all code paths provide column value

### Phase 2: Remove Boolean Flag Defaults

Remove `default=False` from boolean fields in:

- `HttpRequestUsage.session_based` and `is_async` (http_requests.py)
- `MetricInfo.custom_collector` (metrics.py)
- `UrlPattern.is_partial` and `is_conditional` (django_urls.py)

Change from:

```python
session_based: bool = Field(default=False, description="Using session")
```

To:

```python
session_based: bool = Field(..., description="Using session")
```

**Scanner Updates**:

- Verify all creation sites explicitly assign boolean values
- Ensure no code paths omit these fields

### Phase 3: Remove Summary Field Defaults

Remove `default=0` from `SignalSummary` fields:

- `django_receivers`
- `django_senders`
- `celery_receivers`
- `celery_senders`
- `custom_signals_defined`
- `unused_custom_signals`

Change from:

```python
django_receivers: int = Field(default=0, ge=0, description="Django signal receivers")
```

To:

```python
django_receivers: int = Field(..., ge=0, description="Django signal receivers")
```

**Scanner Updates**:

- Verify summary calculation always provides all 6 counts
- Ensure no code paths omit count fields

### Phase 4: Testing and Validation

**Unit Tests**:

- Add tests that verify ValidationError is raised when fields are missing
- Test all scanner code paths to ensure fields are always assigned
- Add regression tests for edge cases (empty files, malformed AST, etc.)

**Integration Tests**:

- Run all scanners on test fixtures
- Verify output validation succeeds
- Confirm no silent defaults hiding bugs

**Manual Validation**:

- Run scanners on real projects (wagtail, django)
- Verify no ValidationErrors in production
- Check output completeness

## Impact

### Users Affected

None - this is an internal model improvement with no API changes.

### Migration Required

None - output format unchanged, only validation strictness improved.

### Performance Considerations

- Negligible: Validation happens once per object creation
- No runtime performance impact
- Slightly faster failures (immediate ValidationError vs. silent wrong data)

## Alternatives Considered

### Alternative 1: Keep All Defaults (Do Nothing)

**Pros**:

- No changes needed
- Backwards compatible

**Cons**:

- Bugs remain hidden
- Data quality issues persist
- Future maintainers inherit technical debt

**Decision**: Rejected - silent failures are worse than validation errors

### Alternative 2: Add Defaults Only Where Truly Optional

**Pros**:

- More nuanced approach
- Preserves some flexibility

**Cons**:

- Hard to determine "truly optional" without deep scanner knowledge
- Inconsistent - some fields have defaults, others don't
- Doesn't solve the root problem

**Decision**: Rejected - binary choice (required or optional) is clearer

### Alternative 3: Make Fields Optional[T] Instead

**Pros**:

- Explicitly marks optionality in type system
- Allows None as valid value

**Cons**:

- Changes output format (None vs. 0/False)
- Breaks existing parsers
- Not semantically correct (fields aren't actually optional)

**Decision**: Rejected - these fields are always required, not optional

### Alternative 4: Add Validation in Scanners Instead

**Pros**:

- Centralizes validation logic
- Can provide better error messages

**Cons**:

- Duplicates validation across many scanners
- Doesn't prevent future bugs
- Harder to maintain

**Decision**: Rejected - Pydantic validation is the right layer for this

## Open Questions

None - all affected fields and scanners have been identified and verified.

## Success Criteria

1. **Functional Requirements**:

   - [ ] All `column` fields have `default=` removed
   - [ ] All boolean flag fields have `default=` removed
   - [ ] All SignalSummary count fields have `default=` removed
   - [ ] Appropriate defaults (ComplexityResult, ExceptClause) remain unchanged

2. **Quality Requirements**:

   - [ ] All existing tests continue passing
   - [ ] New tests verify ValidationError on missing fields
   - [ ] Test coverage maintains ≥80%
   - [ ] Ruff checks pass

3. **Validation**:

   - [ ] All scanners explicitly assign removed-default fields
   - [ ] No `or 0` or `or False` fallbacks remain
   - [ ] Integration tests confirm output completeness
   - [ ] Manual validation on real projects (wagtail)

4. **Documentation**:
   - [ ] Model docstrings accurate
   - [ ] No breaking changes in public API
   - [ ] Scanner implementation notes updated if needed
