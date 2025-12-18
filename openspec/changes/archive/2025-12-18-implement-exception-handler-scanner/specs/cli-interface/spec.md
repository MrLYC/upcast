# cli-interface Specification Delta

## MODIFIED Requirements

### Requirement: Consistent Command Naming

The system SHALL use a consistent naming pattern for all scanner commands following the `scan-*` convention.

#### Scenario: Add scan-exception-handlers command

- **WHEN** user needs to scan for Python exception handling patterns
- **THEN** the system SHALL provide `scan-exception-handlers` command
- **AND** accept path argument (file or directory) as first positional argument
- **AND** support standard options: `-o/--output`, `-v/--verbose`, `--include`, `--exclude`
- **AND** follow the same CLI patterns as other scanner commands

**DIFF**: New scan-exception-handlers command for detecting try/except patterns and anti-patterns
