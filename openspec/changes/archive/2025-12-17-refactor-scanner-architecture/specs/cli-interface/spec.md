# cli-interface Specification

## ADDED Requirements

### Requirement: Consistent Command Naming

The system SHALL use a consistent naming pattern for all scanner commands following the `scan-*` convention.

#### Scenario: Standardize to scan prefix

- **WHEN** users run scanner commands
- **THEN** all commands SHALL use the `scan-*` pattern:
  - `scan-env-vars` (unchanged)
  - `scan-django-models` (renamed from `analyze-django-models`)
  - `scan-django-settings` (renamed from `scan-django-settings-cmd`)
  - `scan-prometheus-metrics` (renamed from `scan-prometheus-metrics-cmd`)

**DIFF**: Renamed commands for consistency

#### Scenario: Deprecated command aliases

- **WHEN** users run old command names
- **THEN** the system SHALL execute the command successfully
- **AND** print a deprecation warning to stderr
- **AND** show the new command name in the warning

**DIFF**: Added backward compatibility with deprecation

#### Scenario: Deprecation warning format

- **WHEN** showing deprecation warnings
- **THEN** the message SHALL follow format:
  ```
  Warning: 'analyze-django-models' is deprecated and will be removed in version X.Y. Use 'scan-django-models' instead.
  ```

**DIFF**: Specified deprecation message format

### Requirement: File Pattern Filtering

The system SHALL support flexible file filtering via include and exclude patterns for all scan commands.

#### Scenario: Include pattern option

- **WHEN** user specifies `--include` option
- **THEN** the system SHALL only scan files matching the pattern
- **AND** support glob patterns (e.g., `*.py`, `**/models/*.py`)
- **AND** allow multiple `--include` options
- **AND** default to `**/*.py` if not specified

**DIFF**: New requirement for file filtering

#### Scenario: Exclude pattern option

- **WHEN** user specifies `--exclude` option
- **THEN** the system SHALL skip files matching the pattern
- **AND** support glob patterns
- **AND** allow multiple `--exclude` options
- **AND** apply default excludes (venv/, **pycache**/, etc.)

**DIFF**: New requirement for exclusion patterns

#### Scenario: Disable default excludes

- **WHEN** user specifies `--no-default-excludes` flag
- **THEN** the system SHALL not apply default exclude patterns
- **AND** only apply user-specified `--exclude` patterns

**DIFF**: New flag for override behavior

#### Scenario: Pattern precedence

- **WHEN** both include and exclude patterns are specified
- **THEN** the system SHALL:
  1. Apply include patterns first
  2. Apply exclude patterns second (exclude wins)
  3. Log filtering decisions in verbose mode

**DIFF**: Specified pattern application order

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
