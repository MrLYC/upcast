# Django URL Scanner Specification Delta

## MODIFIED Requirements

### Requirement: View Resolution

The system SHALL resolve view references to their module paths and extract documentation.

#### Scenario: Always output view fields

- **WHEN** formatting any path/re_path pattern
- **THEN** the system SHALL always include `view_module` and `view_name` fields in output
- **AND** SHALL set fields to `null` when resolution fails
- **AND** SHALL NOT omit fields from output even when values are null
- **AND** allow users to distinguish between unresolved views and non-view patterns

**Rationale**: Explicit null values provide clearer indication of resolution status than missing fields

**DIFF**: Previously fields were omitted when null; now always included

#### Scenario: Extract view name even when module unknown

- **WHEN** view resolution partially succeeds
- **AND** view name can be extracted but module path cannot
- **THEN** the system SHALL record the view name
- **AND** SHALL set view_module to null
- **AND** SHALL mark view_resolved as false (if that field is present)

**Rationale**: Partial information is better than no information

**DIFF**: Added fallback extraction for view names

#### Scenario: Log resolution failures in verbose mode

- **WHEN** view resolution fails
- **AND** verbose mode is enabled
- **THEN** the system SHALL log:
  - The URL pattern that failed
  - The view node type that couldn't be resolved
  - Any inference errors encountered
- **AND** continue processing other patterns

**Rationale**: Debugging aid for understanding resolution failures

**DIFF**: Added structured logging for resolution failures

## ADDED Requirements

### Requirement: Resolution Status Tracking

The system SHALL provide explicit indication of view resolution success.

#### Scenario: Track resolution status

- **WHEN** resolving a view reference
- **THEN** the system SHALL determine if resolution was successful
- **AND** MAY include a `view_resolved` boolean field in output
- **AND** set to true only when both module and name are successfully resolved

**Rationale**: Allows users to filter and analyze resolution success rates

#### Scenario: Distinguish pattern types

- **WHEN** a pattern is not a view (include, router)
- **THEN** view_resolved SHALL be null or omitted
- **AND** view_module and view_name SHALL both be null
- **AND** other fields (include_module, router_type) SHALL indicate pattern type

**Rationale**: Clear distinction between unresolved views and non-view patterns

### Requirement: Output Field Guarantees

The system SHALL guarantee presence of critical fields in output.

#### Scenario: Required view fields

- **WHEN** exporting URL patterns to YAML or JSON
- **THEN** every path/re_path entry SHALL include:
  - `view_module` (string or null)
  - `view_name` (string or null)
- **AND** SHALL NOT omit these fields
- **AND** SHALL use explicit null values for unresolved views

**Rationale**: Consistent output structure simplifies parsing and analysis

#### Scenario: Optional description field

- **WHEN** a view's docstring can be extracted
- **THEN** the system SHALL include `description` field with docstring value
- **WHEN** docstring cannot be extracted
- **THEN** description MAY be null or omitted

**Rationale**: Description is supplementary information, not critical for routing analysis

## REMOVED Requirements

None - all existing requirements remain valid with enhancements noted above.
