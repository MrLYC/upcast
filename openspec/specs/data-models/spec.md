# data-models Specification

## Purpose

TBD - created by archiving change remove-inappropriate-model-defaults. Update Purpose after archive.

## Requirements

### Requirement: Default Value Documentation

The system SHALL document why a field has a default.

#### Scenario: Defaults must be justified

- **WHEN** a field defines a default
- **THEN** its docstring/comment SHALL explain the rationale and when it applies (e.g., "Defaults to 0 when tokenization fails gracefully").

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
