# Proposal: Revert to Optional Fields with None Types

**Status**: PROPOSED

## What Changes

Reverse the recent field default removal by:

1. Removing all default values (empty strings, lists, dicts, zeros) from model fields
2. Adding `| None` type annotations to truly optional fields
3. Updating scanners to explicitly pass `None` for absent values
4. Updating tests to expect `None` for optional fields

This restores explicit optionality through type hints instead of implicit defaults.

**Affected Models** (all files under `upcast/models/`):

- `http_requests.py`: params, headers, json_body, data, timeout → `| None`
- `env_vars.py`: code, default_value → `| None`
- `base.py`: scan_duration_ms, metadata → keep metadata default_factory, scan_duration_ms → `| None`
- `django_models.py`: related_name, on_delete, meta, description → `| None` and remove defaults
- `blocking_operations.py`: statement, function, class_name → `| None`
- `exceptions.py`: else_clause, finally_clause → `| None` (remove placeholder defaults)
- `django_settings.py`: code, value, statement, overrides, base_module → `| None`
- `signals.py`: handler, pattern, code, sender, context, status → `| None`
- `metrics.py`: namespace, subsystem, unit, buckets → `| None`
- `concurrency.py`: statement, context → `| None`
- `django_urls.py`: pattern, view_module, view_name, include_module, namespace, name, viewset_module, viewset_name, basename, router_type, description, note → `| None`
- `complexity.py`: message, description, signature, code → keep as `| None` (already optional)

**Fields Keeping Legitimate Defaults**:

- `ExceptClause` log/control-flow counters: `default=0` (semantically meaningful zero)
- Base metadata: `default_factory=dict` (mutable default)

## Why

**Current Problem**: The recent change forced all fields to have concrete defaults (empty strings, empty dicts/lists, zeros), making it impossible to distinguish between "field not provided" and "field provided but empty/zero". This loses semantic information.

**Examples of Lost Information**:

```python
# Current (ambiguous):
EnvVarInfo(name="VAR", required=True, default_value="", locations=[...])
# Is default_value empty because it wasn't provided, or because it's actually ""?

HttpRequestUsage(..., timeout=0, ...)
# Is timeout 0 because no timeout specified, or because timeout=0 was explicitly set?

# After fix (clear):
EnvVarInfo(name="VAR", required=True, default_value=None, locations=[...])
# Clearly no default value provided

HttpRequestUsage(..., timeout=None, ...)
# Clearly no timeout specified
```

**Why Optional Types Are Better**:

1. **Explicit Optionality**: `| None` clearly communicates field may be absent
2. **Type Safety**: Type checkers can verify None handling
3. **Semantic Clarity**: `None` means "not provided", empty string means "provided but empty"
4. **JSON Serialization**: Pydantic's `exclude_none=True` removes None fields from output
5. **API Contracts**: Consumers know which fields may be missing

**Design Philosophy**: Python's "Explicit is better than implicit" (PEP 20) - use `| None` to express optionality, not default values.

## How

### Phase 1: Remove Empty String Defaults

Remove defaults from string fields that can be absent:

```python
# Before:
code: str = Field("", description="Code snippet")

# After:
code: str | None = Field(None, description="Code snippet")
```

**Affected fields**: code, message, description, signature, handler, pattern, sender, statement, function, class_name, namespace, subsystem, unit, base_module, value, overrides, view_module, view_name, etc.

### Phase 2: Remove Empty Collection Defaults

Remove `default_factory=dict/list` from truly optional collections:

```python
# Before:
context: dict[str, Any] = Field(default_factory=dict, description="Context")
buckets: list[float] = Field(default_factory=list, description="Buckets")

# After:
context: dict[str, Any] | None = Field(None, description="Context")
buckets: list[float] | None = Field(None, description="Buckets")
```

**Affected fields**: context (signals, concurrency), meta, buckets, params, headers, json_body, data

### Phase 3: Remove Numeric/Boolean Defaults

```python
# Before:
timeout: float | int = Field(0, description="Timeout")
scan_duration_ms: int = Field(0, ge=0, description="Duration")

# After:
timeout: float | int | None = Field(None, description="Timeout")
scan_duration_ms: int | None = Field(None, ge=0, description="Duration")
```

### Phase 4: Fix Exception Clause Placeholders

Remove the placeholder pattern for else/finally clauses:

```python
# Before:
else_clause: ElseClause = Field(default_factory=lambda: ElseClause(line=0, lines=0), ...)
finally_clause: FinallyClause = Field(default_factory=lambda: FinallyClause(line=0, lines=0), ...)

# After:
else_clause: ElseClause | None = Field(None, description="Else clause")
finally_clause: FinallyClause | None = Field(None, description="Finally clause")
```

### Phase 5: Update Scanners

Update all scanners to:

1. Remove `or ""` / `or {}` / `or []` / `or 0` fallback patterns
2. Explicitly pass `None` for absent values
3. Use Pydantic's `exclude_none=True` when serializing

```python
# Before:
BlockingOperation(..., statement=safe_as_string(node) or "", ...)

# After:
BlockingOperation(..., statement=safe_as_string(node) or None, ...)
```

### Phase 6: Update Tests

Update all tests expecting empty defaults to expect None:

```python
# Before:
assert location.code == ""
assert usage.handler == ""
assert summary.scan_duration_ms == 0

# After:
assert location.code is None
assert usage.handler is None
assert summary.scan_duration_ms is None
```

### Phase 7: Update Spec

Modify data-models spec to reflect optional field philosophy:

```markdown
#### Scenario: Optional fields use None not defaults

- **WHEN** a field may be absent or not determinable
- **THEN** the field SHALL use `| None` type annotation
- **AND** SHALL use `Field(None, ...)` not empty defaults
- **EXAMPLE**: `code: str | None = Field(None, ...)` not `code: str = Field("", ...)`
```

## Impact

### Users Affected

None - internal model change, API output unchanged when using `exclude_none=True`

### Migration Required

None - JSON output can remain compatible with `exclude_none=True` serialization

### Performance Considerations

- Negligible: None vs empty value has no performance impact
- Slightly smaller JSON when using `exclude_none=True`

## Alternatives Considered

### Alternative 1: Keep Current Defaults (Do Nothing)

**Pros**: No changes needed

**Cons**:

- Loses semantic information (can't distinguish absent vs empty)
- Violates Python's explicit optionality principle
- Type checkers can't help verify None handling
- Harder to understand API contracts

**Decision**: Rejected - explicit optionality is worth the refactor

### Alternative 2: Use Sentinel Values

**Pros**: Can distinguish None (explicitly set) from MISSING (not set)

**Cons**:

- More complex
- Non-standard pattern
- Harder to serialize
- Overkill for current needs

**Decision**: Rejected - `| None` is sufficient and idiomatic

### Alternative 3: Split Models (Required vs Optional)

**Pros**: Type system enforces required fields

**Cons**:

- Model proliferation
- Code duplication
- Harder to maintain

**Decision**: Rejected - single model with `| None` is simpler

## Open Questions

None - path forward is clear

## Success Criteria

1. **Functional Requirements**:

   - [ ] All empty string defaults removed from optional fields
   - [ ] All empty collection defaults removed from optional fields
   - [ ] All zero defaults removed from optional numeric fields
   - [ ] Exception clause placeholders replaced with `| None`
   - [ ] All optional fields have `| None` type annotation

2. **Scanner Updates**:

   - [ ] All scanners pass `None` for absent values
   - [ ] No `or ""` / `or {}` / `or 0` fallback patterns remain
   - [ ] Scanners use actual values or explicit `None`

3. **Testing**:

   - [ ] All tests updated to expect `None` for optional fields
   - [ ] All 261 tests passing
   - [ ] Test coverage maintains ≥80%
   - [ ] Ruff checks pass

4. **Validation**:

   - [ ] Type checkers accept `| None` annotations
   - [ ] Pydantic validation works correctly
   - [ ] JSON serialization with `exclude_none=True` works
   - [ ] Manual validation on real projects (wagtail)

5. **Documentation**:
   - [ ] Data models spec updated
   - [ ] Model docstrings clarify optional fields
   - [ ] No breaking changes in public API
