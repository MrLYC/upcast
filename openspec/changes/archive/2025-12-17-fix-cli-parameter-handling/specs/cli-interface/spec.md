# cli-interface Specification

## MODIFIED Requirements

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
