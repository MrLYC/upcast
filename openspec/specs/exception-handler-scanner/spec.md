# exception-handler-scanner Specification

## Purpose

TBD - created by archiving change implement-exception-handler-scanner. Update Purpose after archive.

## Requirements

### Requirement: CLI Integration

The system SHALL provide a command-line interface following project conventions.

#### Scenario: Add scan-exception-handlers command

- **WHEN** user needs to scan for exception handling patterns
- **THEN** the system SHALL provide `scan-exception-handlers` command
- **AND** accept path argument (file or directory) as first positional argument
- **AND** support standard options: `-o/--output`, `-v/--verbose`, `--include`, `--exclude`
- **AND** follow the same CLI patterns as other scanner commands

**DIFF**: New scan-exception-handlers command

#### Scenario: Support file filtering

- **WHEN** running scan-exception-handlers
- **THEN** the system SHALL support `--include` patterns for file matching
- **AND** support `--exclude` patterns for file exclusion
- **AND** use common pattern matching utilities
- **AND** respect default exclusions (venv, migrations, etc.)

**DIFF**: File filtering support
