# prometheus-metrics-scanner Spec Delta

## MODIFIED Requirements

### Requirement: Metric Location Recording

The system SHALL record metric locations using separate file and line number fields.

#### Scenario: Location fields in metric output (UPDATED)

- **WHEN** scanner detects a Prometheus metric
- **THEN** the output SHALL include `file: str` field with the file path
- **AND** SHALL include `line: int | None` field with the line number
- **AND** SHALL NOT include a combined `location: str` field
- **EXAMPLE**:
  ```yaml
  usages:
    - file: apiserver/paasng/metrics.py
      line: 25
      pattern: counter.inc()
      statement: request_counter.inc()
  ```

**DIFF**: Changed from `location: "file:line"` to separate `file` and `line` fields.

#### Scenario: File path extraction for metrics

- **WHEN** extracting metric location from AST node
- **THEN** scanner SHALL obtain file path relative to scan root
- **AND** SHALL store in `file` field
- **AND** file path SHALL use forward slashes regardless of platform

#### Scenario: Line number extraction for metrics

- **WHEN** extracting metric location from AST node
- **THEN** scanner SHALL obtain line number from node.lineno
- **AND** SHALL store as integer in `line` field
- **AND** line numbers SHALL be 1-based (matching editor conventions)

#### Scenario: Missing line number in metrics

- **WHEN** AST node does not provide line number
- **THEN** scanner SHALL set `line` to None
- **AND** SHALL still record `file` path

**Rationale**: Maintains consistency with other scanners and improves type safety for metric location tracking.

## ADDED Requirements

None - this modifies existing location recording requirements.

## REMOVED Requirements

None - enhanced specification, not removal.
