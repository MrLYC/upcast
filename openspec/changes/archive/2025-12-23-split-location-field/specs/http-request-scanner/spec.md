# http-request-scanner Spec Delta

## MODIFIED Requirements

### Requirement: Location Recording

The system SHALL record HTTP request locations using separate file and line number fields.

#### Scenario: Location fields in output (UPDATED)

- **WHEN** scanner detects an HTTP request
- **THEN** the output SHALL include `file: str` field with the file path
- **AND** SHALL include `line: int | None` field with the line number
- **AND** SHALL NOT include a combined `location: str` field
- **EXAMPLE**:
  ```yaml
  usages:
    - file: apiserver/paasng/client.py
      line: 101
      statement: requests.get(url)
      method: GET
  ```

**DIFF**: Changed from `location: "file:line"` to separate `file` and `line` fields.

#### Scenario: File path extraction

- **WHEN** extracting location from AST node
- **THEN** scanner SHALL obtain file path relative to scan root
- **AND** SHALL store in `file` field
- **AND** file path SHALL use forward slashes regardless of platform

#### Scenario: Line number extraction

- **WHEN** extracting location from AST node
- **THEN** scanner SHALL obtain line number from node.lineno
- **AND** SHALL store as integer in `line` field
- **AND** line numbers SHALL be 1-based (matching editor conventions)

#### Scenario: Missing line number handling

- **WHEN** AST node does not provide line number
- **THEN** scanner SHALL set `line` to None
- **AND** SHALL still record `file` path

**Rationale**: Maintains consistency with EnvVarLocation pattern and improves type safety.

## ADDED Requirements

None - this modifies existing location recording requirements.

## REMOVED Requirements

None - enhanced specification, not removal.
