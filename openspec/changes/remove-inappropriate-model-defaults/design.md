# Design: Remove Inappropriate Model Field Defaults

## Overview

This change removes `default=` parameters from Pydantic model fields where scanners always provide explicit values, enforcing data completeness through validation rather than silent defaults.

## Problem Analysis

### Root Cause

Pydantic's `Field(default=value)` creates an **implicit contract** that the field is optional. However, many fields in our models are:

1. Always determinable from AST analysis
2. Required for semantic correctness
3. Not marked as `Optional[T]` in type hints

The mismatch between "required in type hint" and "has default in Field" creates a validation gap.

### Why This Matters

**Fail-Fast Principle**: Errors should be detected as early as possible. A ValidationError during model creation is better than incorrect data propagating through the system.

**Example Bug Scenario**:

```python
# Bad: Scanner has a bug but runs successfully
def analyze_signal(node):
    return SignalUsage(
        file="app/signals.py",
        line=node.lineno,
        # BUG: Forgot to add column - silently defaults to 0
    )

# Good: Scanner bug caught immediately
def analyze_signal(node):
    return SignalUsage(
        file="app/signals.py",
        line=node.lineno,
        # BUG: Forgot to add column - ValidationError raised
    )
    # ValidationError: Field required [type=missing, input_value=...]
```

## Architecture Decisions

### Decision 1: Remove Defaults vs. Make Fields Optional

**Options**:

1. Remove defaults (make fields required)
2. Change type hints to `Optional[T]` and keep defaults
3. Add runtime validation in scanners

**Choice**: Remove defaults (Option 1)

**Rationale**:

- Fields are semantically required (not optional)
- AST always provides the information (column, flags, counts)
- Pydantic validation is the correct layer for schema enforcement
- Type hints already declare fields as required (`int`, not `Optional[int]`)

### Decision 2: Scope of Changes

**Fields to Change**:

- `column: int` fields (5 models) - AST always has `col_offset`
- Boolean flags (5 fields) - Scanners always evaluate conditions
- Summary counts (6 fields in SignalSummary) - Aggregation always runs

**Fields to Keep Unchanged**:

- `ComplexityResult.comment_lines/code_lines` - Tokenization may fail gracefully
- `ExceptClause.*_count` fields - Zero is semantically meaningful (absence of pattern)

**Rationale**:

- Clear separation: "always available" vs. "may legitimately be zero/missing"
- Consistent pattern: If scanner can fail to compute, keep default; otherwise remove

### Decision 3: Scanner Update Strategy

**Pattern to Remove**:

```python
column=node.col_offset or 0  # BAD: Hides None
```

**Pattern to Use**:

```python
column=node.col_offset  # GOOD: None triggers ValidationError
```

**Rationale**:

- AST `col_offset` is never None in valid Python files
- If it somehow is None, we WANT the error (indicates parser issue)
- Explicit is better than implicit (PEP 20)

## Implementation Strategy

### Phase Order

1. **Column fields first**: Simple, high-impact, easy to verify
2. **Boolean flags second**: Slightly more complex logic to verify
3. **Summary counts third**: Requires verifying aggregation completeness
4. **Testing last**: Comprehensive validation after all changes

**Rationale**: Incremental changes allow easier debugging and rollback if issues arise.

### Testing Strategy

**Unit Tests**: Verify ValidationError on missing fields

```python
def test_signal_usage_requires_column():
    with pytest.raises(ValidationError) as exc_info:
        SignalUsage(file="test.py", line=42)  # Missing column
    assert "column" in str(exc_info.value)
```

**Integration Tests**: Verify scanners provide all required fields

```python
def test_signals_scanner_provides_column():
    scanner = SignalsScanner()
    results = scanner.scan(["tests/fixtures/signals.py"])
    for signal_info in results.results:
        for usage in signal_info.receivers:
            assert usage.column >= 0  # Validation would have failed if missing
```

**Manual Tests**: Run on real projects to catch edge cases

## Risk Assessment

### Low Risk Areas

- Model definitions: Simple Field() changes
- Test additions: Only additive, no existing tests affected
- Column fields: AST always provides col_offset

### Medium Risk Areas

- Boolean flags: Need to verify all scanner code paths assign values
- Summary counts: Need to verify aggregation completeness

### Mitigation Strategies

1. **Incremental rollout**: Phase-based implementation allows early detection
2. **Comprehensive testing**: Both unit and integration tests
3. **Manual validation**: Test on real projects before merge
4. **Easy rollback**: Changes are isolated, can revert single phase if needed

## Alternative Approaches Considered

### Approach 1: Add Validation Layer in Scanners

**Idea**: Keep defaults, add explicit validation in scanner code

```python
def validate_column(column: int) -> int:
    if column is None:
        raise ValueError("Column must be provided")
    return column
```

**Rejected Because**:

- Duplicates validation logic across many scanners
- Harder to maintain (validation scattered everywhere)
- Doesn't prevent future bugs (developers must remember to call validator)
- Pydantic already provides this capability

### Approach 2: Gradual Migration with Warnings

**Idea**: First add warnings when defaults are used, then remove defaults later

```python
def __init__(self, **kwargs):
    if "column" not in kwargs:
        warnings.warn("column should be provided explicitly")
    super().__init__(**kwargs)
```

**Rejected Because**:

- More complex implementation
- Delays benefits (validation errors)
- Warnings often ignored in CI/CD
- Not standard Pydantic pattern

### Approach 3: Make Defaults Explicit with Sentinel Values

**Idea**: Use sentinel like -1 to indicate "not set"

```python
column: int = Field(default=-1, ge=-1)
```

**Rejected Because**:

- Sentinel values are anti-pattern in type-safe code
- Requires runtime checks everywhere field is used
- Confusing for API consumers (is -1 valid?)
- Doesn't solve the root problem

## Dependencies

### Internal Dependencies

- None - changes are isolated to models and scanners

### External Dependencies

- Pydantic 2.x: Already using Pydantic validation
- Python 3.13: AST module guarantees col_offset exists

### Breaking Changes

- **None for users**: Output format unchanged
- **Internal**: Scanners must provide all fields (but they already do)

## Future Considerations

### Potential Follow-up Work

1. **Add mypy strict mode**: Further type safety improvements
2. **Create scanner test generator**: Automate validation test creation
3. **Add schema validation docs**: Document field requirements for contributors

### Extensibility

This pattern should be applied to future models:

- Default values only when field may legitimately be absent
- Required fields should never have defaults
- Use `Optional[T]` type hints when field is truly optional

## Success Metrics

### Immediate

- All tests pass after each phase
- No ValidationErrors in production scenarios
- Cleaner, more explicit model definitions

### Long-term

- Fewer bugs related to missing field assignments
- Easier debugging (validation errors point to exact issue)
- Better code maintainability (explicit requirements)
