# Data Models Specification Delta

## ADDED Requirements

### Requirement: Optional Field None Pattern

The system SHALL use `| None` type annotations for optional fields instead of providing empty defaults.

#### Scenario: Optional fields use None not empty defaults

- **WHEN** a model field may be absent or not determinable
- **THEN** the field SHALL use `| None` type annotation
- **AND** SHALL use `Field(None, ...)` instead of empty string, dict, list, or zero defaults
- **EXAMPLE**: `code: str | None = Field(None, description="Code snippet")` not `code: str = Field("", description="Code snippet")`

**Rationale**: `| None` explicitly communicates optionality and allows distinguishing between "not provided" (None) and "provided but empty" (empty string/collection). This aligns with Python's "explicit is better than implicit" principle.

**Affected Fields** (changed from empty defaults to `| None`):

- String fields: code, message, description, signature, handler, pattern, sender, statement, function, class_name, namespace, subsystem, unit, base_module, value, overrides, view_module, view_name, include_module, namespace, name, viewset_module, viewset_name, basename, router_type, note, related_name, on_delete, status
- Collection fields: params, headers, json_body, data, context, meta, buckets
- Numeric fields: timeout, scan_duration_ms

#### Scenario: Legitimate defaults remain for semantic zeros

- **WHEN** a field value of zero/empty has semantic meaning (e.g., "no occurrences found")
- **OR** the field provides a safe mutable default container
- **THEN** the field MAY keep explicit defaults
- **EXAMPLE**: `pass_count: int = Field(default=0, ge=0, description="Number of pass statements")` - zero means no pass statements found

**Preserved Defaults**:

- `ExceptClause` log and control-flow counters: Zero means pattern not found (semantically meaningful)
- `base.metadata`: Mutable dict default for extensibility
- Collection fields that are never absent (always provided by scanner): Keep as required with no default

#### Scenario: Scanners pass None for absent values

- **WHEN** a scanner constructs a model with optional fields
- **AND** a field value is not determinable or not present
- **THEN** the scanner SHALL pass `None` explicitly (not empty string/dict/list/zero)
- **AND** SHALL NOT use fallback patterns like `or ""` / `or {}` / `or 0`
- **EXAMPLE**: `BlockingOperation(..., statement=safe_as_string(node) or None, ...)` not `statement=safe_as_string(node) or ""`

**Rationale**: Explicit None assignment makes intent clear and preserves semantic information about absence.

#### Scenario: JSON serialization excludes None fields

- **WHEN** serializing models to JSON
- **THEN** the system MAY use `exclude_none=True` option
- **AND** None fields will be omitted from output
- **EXAMPLE**: `model.model_dump_json(exclude_none=True)` omits fields with None values

**Rationale**: Cleaner JSON output and backwards compatibility with consumers expecting absent fields to be omitted.

## REMOVED Requirements

### Requirement: Field Default Discipline

The system SHALL only use Pydantic defaults when absence/zero/false is semantically meaningful; otherwise fields must be required.

**REMOVED**: The previous approach enforced using concrete empty defaults (empty strings, empty dicts, zeros) for optional fields. The new approach uses `| None` type annotations to explicitly express optionality, providing better semantic clarity and distinguishing "not provided" from "provided but empty".

## Implementation Notes

### Type Annotation Pattern

All optional fields follow this pattern:

```python
field_name: BaseType | None = Field(None, description="...")
```

Not:

```python
field_name: BaseType = Field("", description="...")  # Bad - hides None
field_name: BaseType = Field(default_factory=dict, description="...")  # Bad - treats absent as empty
```

### Scanner Update Pattern

**Before** (implicit empty defaults):

```python
BlockingOperation(
    statement=safe_as_string(node) or "",
    function=self._get_function_name(node) or "",
    context=context or {},
)
```

**After** (explicit None):

```python
BlockingOperation(
    statement=safe_as_string(node) or None,
    function=self._get_function_name(node),  # Returns None if not found
    context=context,  # Pass actual dict or None
)
```

### Test Update Pattern

**Before**:

```python
assert location.code == ""
assert info.default_value == ""
assert summary.scan_duration_ms == 0
```

**After**:

```python
assert location.code is None
assert info.default_value is None
assert summary.scan_duration_ms is None
```

### Serialization

Models can use `exclude_none=True` for cleaner JSON:

```python
output.model_dump_json(exclude_none=True)
```

This omits None fields from output, maintaining backwards compatibility.

## Cross-References

Affects all model files under `upcast/models/`:

- `http_requests.py`
- `env_vars.py`
- `base.py`
- `django_models.py`
- `blocking_operations.py`
- `exceptions.py`
- `django_settings.py`
- `signals.py`
- `metrics.py`
- `concurrency.py`
- `django_urls.py`
- `complexity.py`

And all corresponding scanners under `upcast/scanners/`.
