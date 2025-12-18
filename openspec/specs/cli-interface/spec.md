# cli-interface Specification

## Purpose

TBD - created by archiving change refactor-scanner-architecture. Update Purpose after archive.

## Requirements

### Requirement: Consistent Command Naming

The system SHALL use a consistent naming pattern for all scanner commands following the `scan-*` convention.

#### Scenario: Add scan-concurrency-patterns command

- **WHEN** user needs to scan for Python concurrency patterns
- **THEN** the system SHALL provide `scan-concurrency-patterns` command
- **AND** accept path argument (file or directory) as first positional argument
- **AND** support standard options: `-o/--output`, `-v/--verbose`, `--include`, `--exclude`
- **AND** follow the same CLI patterns as other scanner commands

**DIFF**: New scan-concurrency-patterns command for detecting asyncio, threading, and multiprocessing patterns

### Requirement: File Pattern Filtering

The system SHALL support flexible file filtering via include and exclude patterns for all scan commands.

#### Scenario: env-var-scanner respects include patterns

- **WHEN** user specifies `--include` option for `scan-env-vars` command
- **THEN** the system SHALL only scan files matching the pattern
- **AND** pass the pattern to underlying scanner functions
- **AND** use `collect_python_files()` with filtering enabled

**DIFF**: Fixed bug where include patterns were ignored by scan-env-vars

#### Scenario: env-var-scanner respects exclude patterns

- **WHEN** user specifies `--exclude` option for `scan-env-vars` command
- **THEN** the system SHALL skip files matching the pattern
- **AND** pass the pattern to underlying scanner functions
- **AND** apply exclusions during file collection

**DIFF**: Fixed bug where exclude patterns were ignored by scan-env-vars

#### Scenario: env-var-scanner respects no-default-excludes flag

- **WHEN** user specifies `--no-default-excludes` flag for `scan-env-vars` command
- **THEN** the system SHALL not apply default exclude patterns
- **AND** pass this setting to `collect_python_files()`
- **AND** scan all Python files including those in venv/, **pycache**/, etc.

**DIFF**: Fixed bug where no-default-excludes flag was ignored by scan-env-vars

### Requirement: Consistent Option Naming

The system SHALL use consistent option names across all scan commands.

#### Scenario: Standard options for all commands

- **WHEN** invoking any scan command
- **THEN** the system SHALL support:
  - `-o, --output FILE` - Output file path
  - `-v, --verbose` - Enable verbose logging
  - `--include PATTERN` - Include files matching pattern (repeatable)
  - `--exclude PATTERN` - Exclude files matching pattern (repeatable)
  - `--no-default-excludes` - Disable default exclusions
  - `--format {yaml,json}` - Output format (where applicable)

**DIFF**: Standardized option names across commands

#### Scenario: Command-specific options

- **WHEN** a scanner has unique options
- **THEN** those options SHALL be documented separately
- **AND** follow the same naming conventions (kebab-case, clear intent)

**DIFF**: Allowed for scanner-specific extensions

### Requirement: Help Text Quality

The system SHALL provide clear, consistent help text for all commands and options.

#### Scenario: Command help includes examples

- **WHEN** user runs `upcast scan-<name> --help`
- **THEN** the help text SHALL include:
  - Brief description of what is scanned
  - Usage patterns with PATH argument
  - Option descriptions
  - At least 2 usage examples

**DIFF**: Required examples in help text

#### Scenario: Deprecation notice in help

- **WHEN** user runs help for a deprecated command
- **THEN** help text SHALL show deprecation notice at top
- **AND** link to the new command name

**DIFF**: Help text includes deprecation info
