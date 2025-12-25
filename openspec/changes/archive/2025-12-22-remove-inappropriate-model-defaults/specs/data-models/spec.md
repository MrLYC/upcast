# Data Models Specification

## ADDED Requirements

### Requirement: Field Default Discipline

The system SHALL only use Pydantic defaults when absence/zero/false is semantically meaningful; otherwise fields must be required.

#### Scenario: Required fields must not have defaults

- **WHEN** a model field is always provided by the scanner
- **AND** the field represents determinable AST information or aggregation counts
- **THEN** the field SHALL use `Field(..., ...)` (no `default=`)
- **Examples (required)**: `SignalUsage.column`, `ConcurrencyUsage.column`, `BlockingOperation.column`, `SettingsLocation.column`, `EnvVarLocation.column`, `HttpRequestUsage.session_based`, `HttpRequestUsage.is_async`, `MetricInfo.custom_collector`, `UrlPattern.is_partial`, `UrlPattern.is_conditional`, `SignalSummary.*` count fields.

#### Scenario: Appropriate defaults are allowed when meaningful

- **WHEN** a field may legitimately be zero/empty/false or extraction may fail gracefully
- **THEN** the field MAY specify an explicit default (e.g., `comment_lines: int = Field(default=0, ge=0)`; `Field(default_factory=list/dict)` for collections)
- **Examples (allowed defaults)**: `ComplexityResult.comment_lines`, `ComplexityResult.code_lines`, `ExceptClause` log/control-flow counters.

#### Scenario: Scanners must supply required fields

- **WHEN** a field is required (no default)
- **THEN** all scanner code paths SHALL assign it explicitly
- **AND** SHALL NOT use fallback patterns like `or 0` / `or False`.

#### Scenario: Validation errors surface missing data

- **WHEN** a required field is omitted
- **THEN** Pydantic SHALL raise ValidationError at model instantiation with the field name and model type.

### Requirement: Default Value Documentation

The system SHALL document why a field has a default.

#### Scenario: Defaults must be justified

- **WHEN** a field defines a default
- **THEN** its docstring/comment SHALL explain the rationale and when it applies (e.g., "Defaults to 0 when tokenization fails gracefully").

## Implementation Notes

- Remove `or 0` / `or False` fallbacks in scanners; assign required fields directly.
- Maintain tests that ensure ValidationError on missing required fields and coverage ≥80%.
- Preserve legitimate defaults where absence/zero is meaningful.

## Cross-References

- Applies to models under `upcast/models/` and corresponding scanners (`signals`, `concurrency`, `blocking_operations`, `django_settings`, `env_vars`, `http_requests`, `metrics`, `django_urls`, etc.).
