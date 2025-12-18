# cli-interface Specification

## MODIFIED Requirements

### Requirement: Consistent Command Naming

The system SHALL use a consistent naming pattern for all scanner commands following the `scan-*` convention.

#### Scenario: Add scan-signals command

- **WHEN** user needs to scan for Django and Celery signal patterns
- **THEN** the system SHALL provide `scan-signals` command
- **AND** accept path argument (file or directory) as first positional argument
- **AND** support standard options: `-o/--output`, `-v/--verbose`, `--include`, `--exclude`, `--no-default-excludes`
- **AND** follow the same CLI patterns as other scanner commands

**DIFF**: New scan-signals command for detecting Django and Celery signal handlers
