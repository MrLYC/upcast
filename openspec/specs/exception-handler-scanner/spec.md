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

### Requirement: Exception Handler Location Information

The system SHALL provide structured location information for exception handlers using separate fields instead of a combined string.

#### Scenario: Output structured location fields

- **WHEN** detecting an exception handler
- **THEN** the system SHALL output three separate fields:
  - `file`: The absolute or relative file path (string)
  - `lineno`: The starting line number (integer)
  - `end_lineno`: The ending line number (integer)
- **AND** NOT use a combined `location: "file:lineno-end_lineno"` format

#### Scenario: Programmatic parsing

- **GIVEN** structured location fields in the output
- **WHEN** a tool parses exception handler results
- **THEN** it SHALL access `file`, `lineno`, and `end_lineno` directly
- **AND** NOT need to parse a formatted string
- **AND** use standard data structure access patterns

**Output Format Example**:

```yaml
handlers:
  - file: api/views.py
    lineno: 45
    end_lineno: 67
    exception_types:
      - ValueError
      - KeyError
```

**Rationale**: Structured fields are easier to process programmatically than parsing formatted strings. This follows data modeling best practices.

**Breaking Change**: Tools expecting `location` field will need to be updated to use the new structured fields.
