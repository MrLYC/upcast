# data-models Spec Delta

## MODIFIED Requirements

### Requirement: Location Field Structure

The system SHALL use separate `file` and `line` fields instead of combined `location` strings for code location tracking.

#### Scenario: Separate file and line fields

- **WHEN** a model needs to record a code location
- **THEN** the model SHALL use `file: str` and `line: int | None` fields
- **AND** SHALL NOT use a combined `location: str = "file:line"` format
- **EXAMPLE**:
  ```python
  class Usage(BaseModel):
      file: str = Field(description="File path")
      line: int | None = Field(ge=1, description="Line number")
  ```
  not
  ```python
  class Usage(BaseModel):
      location: str = Field(description="file:line format")
  ```

**Rationale**:

- Type safety: Line numbers are validated as integers
- Easier querying: Can filter/sort by file or line without parsing
- Consistency: Matches `EnvVarLocation` pattern
- Extensibility: Easy to add `column` or `code` fields later

#### Scenario: Line number is optional

- **WHEN** line number may not be determinable
- **THEN** the `line` field SHALL be typed as `int | None`
- **AND** SHALL use constraint `ge=1` (line numbers start at 1)
- **EXAMPLE**: `line: int | None = Field(ge=1, description="Line number")`

**Rationale**: Some code locations may only have file path without specific line.

#### Scenario: Consistent across all usage models

- **WHEN** defining models like `HttpRequestUsage`, `MetricUsage`, etc.
- **THEN** all SHALL follow the `file` + `line` pattern
- **AND** SHALL maintain consistency with `EnvVarLocation`
- **AFFECTED MODELS**:
  - `HttpRequestUsage` - updated from `location: str`
  - `MetricUsage` - updated from `location: str`
  - `EnvVarLocation` - already follows pattern (reference)

## REMOVED Requirements

None - this adds constraints rather than removing them.

## ADDED Requirements

None - this modifies existing location field requirements.
