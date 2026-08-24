## ADDED Requirements

### Requirement: Offset Scanner Uses Shared Architecture

The offset scanner SHALL extend `BaseScanner`, use the shared file collection and export pipeline, and avoid scanner-specific serialization or runtime framework imports.

#### Scenario: Scan filtered source files

- **WHEN** the scanner receives include/exclude patterns
- **THEN** it SHALL pass them through the standard file collection path
- **AND** it SHALL return a typed output even when no findings are present

#### Scenario: Stable static result

- **WHEN** the same source tree is scanned repeatedly
- **THEN** findings and summary category ordering SHALL be deterministic apart from scan timing metadata
