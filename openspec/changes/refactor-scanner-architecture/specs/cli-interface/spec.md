# cli-interface Specification Delta

## MODIFIED Requirements

### Requirement: Scanner Module Import Paths Updated

CLI commands SHALL import scanners from `upcast.scanners.*` instead of `upcast.*_scanner`.

#### Scenario: Import from new location

- **GIVEN** a scanner command in the CLI
- **WHEN** importing scanner functions
- **THEN** the system SHALL use `from upcast.scanners.signal import scan_signals`
- **AND** NOT use `from upcast.signal_scanner import scan_signals`

#### Scenario: Old imports emit deprecation warnings

- **GIVEN** code using old import path `from upcast.signal_scanner import ...`
- **WHEN** the import is executed
- **THEN** the system SHALL emit a DeprecationWarning
- **AND** the warning SHALL mention new import path
- **AND** the warning SHALL mention removal version (v2.0.0)

---

### Requirement: Unified Output Structure Across All Scanners

All scanner outputs SHALL follow unified structure with `summary`, `results`, and `metadata` fields instead of scanner-specific structures.

#### Scenario: All scanners return structured output

- **GIVEN** any scanner command (scan-signals, scan-http-requests, etc.)
- **WHEN** running the command with `--format yaml`
- **THEN** the output SHALL have top-level keys: summary, results, metadata
- **AND** NOT mix results directly at top level

#### Scenario: Summary field present in all outputs

- **GIVEN** any scanner output
- **WHEN** inspecting the output structure
- **THEN** the summary field SHALL contain total_count, files_scanned, scan_duration_ms
- **AND** MAY contain scanner-specific fields

#### Scenario: Metadata includes scanner information

- **GIVEN** any scanner output
- **WHEN** inspecting metadata field
- **THEN** the metadata SHALL contain scanner_name, scanner_version
- **AND** MAY contain scan_timestamp and other metadata

---

## ADDED Requirements

### Requirement: Legacy Format Support Flag

The system SHALL provide `--legacy-format` flag to output results in old format for backward compatibility during migration period.

#### Scenario: Legacy format flag produces old structure

- **GIVEN** a scanner command with `--legacy-format` flag
- **WHEN** running the command
- **THEN** the system SHALL output in old format without summary/results/metadata wrapper
- **AND** match the pre-v1.0 output structure

#### Scenario: Legacy format works with all scanners

- **GIVEN** any scanner (signal, http-request, env-var, etc.)
- **WHEN** running with `--legacy-format`
- **THEN** the system SHALL produce scanner-specific old format
- **AND** allow gradual migration for users

#### Scenario: Legacy format is deprecated

- **GIVEN** documentation and help text
- **WHEN** describing `--legacy-format` flag
- **THEN** the system SHALL mark it as deprecated
- **AND** indicate removal in v2.0.0

---

### Requirement: Standard CLI Arguments Across All Scanners

The system SHALL support consistent set of arguments for all scanner commands.

#### Scenario: All scanners accept path argument

- **GIVEN** any scanner command
- **WHEN** invoking the command
- **THEN** the system SHALL require a path argument (positional)
- **AND** the path SHALL be the directory or file to scan

#### Scenario: All scanners support output file argument

- **GIVEN** any scanner command
- **WHEN** providing `-o output.yaml` or `--output output.json`
- **THEN** the system SHALL write results to specified file
- **AND** NOT output to stdout

#### Scenario: All scanners support format selection

- **GIVEN** any scanner command
- **WHEN** providing `--format json` or `--format yaml`
- **THEN** the system SHALL output in the specified format
- **AND** default to yaml if not specified

#### Scenario: All scanners support include patterns

- **GIVEN** a scanner command with `--include "**/*.py" --include "**/*.pyi"`
- **WHEN** scanning
- **THEN** the system SHALL only scan files matching the patterns
- **AND** allow multiple include patterns

#### Scenario: All scanners support exclude patterns

- **GIVEN** a scanner command with `--exclude "**/test_*.py" --exclude "**/migrations/**"`
- **WHEN** scanning
- **THEN** the system SHALL skip files matching the patterns
- **AND** allow multiple exclude patterns

#### Scenario: All scanners support verbose mode

- **GIVEN** a scanner command with `-v` or `--verbose`
- **WHEN** scanning
- **THEN** the system SHALL output detailed progress information
- **AND** show files being scanned
