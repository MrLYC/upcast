# Data Models Specification Delta

## MODIFIED Requirements

### Requirement: Field Default Values

The system SHALL use Pydantic field defaults only when fields may legitimately be absent or have zero/false as meaningful values.

#### Scenario: Required fields must not have defaults - ENFORCED

- **WHEN** a model field is always provided by the scanner
- **AND** the field represents determinable information from AST
- **THEN** the field SHALL NOT have a `default=` parameter
- **AND** the field SHALL use `Field(..., ...)` to mark it as required
- **EXAMPLE**: `column: int = Field(..., ge=0)` not `Field(default=0, ge=0)`

**Affected Fields**:

- `SignalUsage.column`
- `ConcurrencyUsage.column`
- `BlockingOperation.column`
- `SettingsLocation.column`
- `EnvVarLocation.column`
- `HttpRequestUsage.session_based`
- `HttpRequestUsage.is_async`
- `MetricInfo.custom_collector`
- `UrlPattern.is_partial`
- `UrlPattern.is_conditional`
- `SignalSummary.django_receivers`
- `SignalSummary.django_senders`
- `SignalSummary.celery_receivers`
- `SignalSummary.celery_senders`
- `SignalSummary.custom_signals_defined`
- `SignalSummary.unused_custom_signals`

**Rationale**: Defaults mask missing assignments, allowing bugs to propagate silently instead of failing fast with ValidationError.

#### Scenario: Appropriate defaults for legitimate zero values - PRESERVED

- **WHEN** a field may legitimately be zero or false
- **OR** extraction may fail gracefully
- **OR** zero/false has semantic meaning (absence of pattern)
- **THEN** the field SHALL have an appropriate `default=` parameter
- **EXAMPLE**: `comment_lines: int = Field(default=0, ge=0)`

**Preserved Defaults**:

- `ComplexityResult.comment_lines`: Tokenization may fail
- `ComplexityResult.code_lines`: Tokenization may fail
- `ExceptClause.log_*_count`: Zero means pattern not found (semantically meaningful)
- `ExceptClause.pass_count`: Zero means no pass statements
- Collection fields: `Field(default_factory=list/dict)` for mutable defaults

**Rationale**: These defaults represent legitimate absence or semantic zero, not missing data.

#### Scenario: Scanners must always provide required fields - ENFORCED

- **WHEN** a field has no `default=` parameter
- **THEN** all scanner code paths SHALL explicitly assign the field
- **AND** SHALL NOT use `or` fallback patterns (e.g., `node.col_offset or 0`)
- **EXAMPLE**: Use `column=node.col_offset` not `column=node.col_offset or 0`

**Changed Patterns**:

```python
# Before (BAD - hides None):
BlockingOperation(
    file=file,
    line=node.lineno,
    column=node.col_offset or 0,  # Masks potential None
    ...
)

# After (GOOD - explicit requirement):
BlockingOperation(
    file=file,
    line=node.lineno,
    column=node.col_offset,  # ValidationError if None
    ...
)
```

**Rationale**: Explicit is better than implicit. If AST data is missing, we want to know immediately.

#### Scenario: Validation errors guide debugging - IMPROVED

- **WHEN** a scanner forgets to assign a required field
- **THEN** Pydantic SHALL raise ValidationError with clear message
- **AND** error SHALL include field name and model type
- **AND** error SHALL occur at model instantiation time (not later)

**Example Error**:

```
ValidationError: 1 validation error for SignalUsage
column
  Field required [type=missing, input_value={'file': 'app/signals.py', 'line': 42, ...}]
```

**Rationale**: Immediate, clear errors are better than silent incorrect data.

## ADDED Requirements

### Requirement: Default Value Documentation

The system SHALL document the rationale for field defaults in model docstrings.

#### Scenario: Defaults must be justified - DOCUMENTED

- **WHEN** a field has a `default=` parameter
- **THEN** the model or field docstring SHALL explain why
- **AND** SHALL state when the default is used
- **EXAMPLE**: "Defaults to 0 when tokenization fails gracefully"

**Implementation**:

- Add comments near fields with defaults explaining usage
- Update model-level docstrings to note optional vs. required fields
- Include examples showing when defaults apply

**Rationale**: Future maintainers should understand why defaults exist.

## REMOVED Requirements

None - no requirements are being removed, only enforced more strictly.

## Implementation Notes

### Scanner Update Checklist

For each affected scanner:

1. ✅ Remove `or 0` and `or False` fallback patterns
2. ✅ Ensure all code paths assign required fields
3. ✅ Verify AST data is always available (never None)
4. ✅ Add test cases for edge cases (empty files, malformed AST)

### Testing Requirements

**Unit Tests**:

- Test ValidationError is raised when fields missing
- Test all scanner code paths provide required fields
- Test appropriate defaults still work correctly

**Integration Tests**:

- Run scanners on real projects
- Verify no ValidationErrors in production
- Check output completeness

**Regression Tests**:

- Test edge cases: empty files, incomplete AST, syntax errors
- Verify graceful degradation where appropriate

## Cross-References

This change affects all scanner implementations:

- Signal Scanner (`upcast/scanners/signals.py`)
- Concurrency Scanner (`upcast/scanners/concurrency.py`)
- Blocking Operations Scanner (`upcast/scanners/blocking_operations.py`)
- Django Settings Scanner (`upcast/scanners/django_settings.py`)
- Environment Variable Scanner (`upcast/scanners/env_vars.py`)
- HTTP Request Scanner (`upcast/scanners/http_requests.py`)
- Prometheus Metrics Scanner (`upcast/scanners/metrics.py`)
- Django URL Scanner (`upcast/scanners/django_urls.py`)

Related models:

- All models in `upcast/models/` directory
- Base models in `upcast/models/base.py`
