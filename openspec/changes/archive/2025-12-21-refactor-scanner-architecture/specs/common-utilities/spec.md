# common-utilities Specification Delta

## ADDED Requirements

### Requirement: Pydantic Base Models for Scanner Outputs

The system SHALL provide base Pydantic models that all scanners extend to ensure type safety and consistent structure.

#### Scenario: Create scanner summary with base fields

- **GIVEN** a scanner has completed scanning
- **WHEN** creating a summary with `ScannerSummary`
- **THEN** the system SHALL validate required fields (total_count, files_scanned, scan_duration_ms)
- **AND** reject invalid values (negative counts)

#### Scenario: Extend base summary with scanner-specific fields

- **GIVEN** a scanner needs custom summary fields
- **WHEN** defining a summary class extending `ScannerSummary`
- **THEN** the system SHALL allow adding scanner-specific fields
- **AND** preserve base field validation

#### Scenario: Generic scanner output model

- **GIVEN** a scanner needs to return typed results
- **WHEN** using `ScannerOutput[T]` with type parameter
- **THEN** the system SHALL enforce the specified result type
- **AND** provide summary, results, and metadata fields

---

### Requirement: Abstract Base Scanner Class

The system SHALL provide an abstract base class for common scanner functionality including file discovery and filtering.

#### Scenario: File discovery with include patterns

- **GIVEN** a scanner with include patterns `["**/*.py"]`
- **WHEN** calling `get_files_to_scan()` on a directory
- **THEN** the system SHALL return only Python files
- **AND** use glob pattern matching

#### Scenario: File filtering with exclude patterns

- **GIVEN** a scanner with exclude patterns `["**/test_*.py"]`
- **WHEN** calling `should_scan_file()` on a test file
- **THEN** the system SHALL return False
- **AND** skip the file during scanning

#### Scenario: Combined include and exclude patterns

- **GIVEN** a scanner with include `["**/*.py"]` and exclude `["**/test_*.py"]`
- **WHEN** discovering files
- **THEN** the system SHALL include Python files
- **AND** exclude test files
- **AND** maintain correct priority (exclude overrides include)

---

### Requirement: Universal Export Function for Scanner Outputs

The system SHALL provide a unified export function that handles all Pydantic-based scanner outputs for YAML and JSON formats.

#### Scenario: Export to YAML format

- **GIVEN** a scanner output as Pydantic model
- **WHEN** calling `export_scanner_output(output, format="yaml")`
- **THEN** the system SHALL serialize to YAML string
- **AND** include summary, results, and metadata fields

#### Scenario: Export to JSON with file output

- **GIVEN** a scanner output and file path
- **WHEN** calling `export_scanner_output(output, format="json", file_path=Path("output.json"))`
- **THEN** the system SHALL write JSON to file
- **AND** return the JSON string

#### Scenario: Handle legacy dict outputs

- **GIVEN** a legacy scanner returning dict instead of Pydantic model
- **WHEN** calling `export_scanner_output()` with dict
- **THEN** the system SHALL still export correctly
- **AND** provide backward compatibility

---

### Requirement: Common CLI Argument Handling

The system SHALL provide reusable CLI utilities with standard arguments for all scanner commands.

#### Scenario: Standard argument parsing

- **GIVEN** a scanner CLI command
- **WHEN** parsing arguments with `create_scanner_parser()`
- **THEN** the system SHALL support path, -o/--output, --format, --include, --exclude, -v/--verbose, --legacy-format
- **AND** validate format choices (yaml, json)

#### Scenario: Multiple include patterns

- **GIVEN** CLI arguments `--include "**/*.py" --include "**/*.pyi"`
- **WHEN** parsing arguments
- **THEN** the system SHALL collect all include patterns in a list
- **AND** apply all patterns during file discovery

#### Scenario: Output to stdout when no file specified

- **GIVEN** no `-o/--output` argument provided
- **WHEN** running scanner CLI
- **THEN** the system SHALL output to stdout
- **AND** NOT create any files

---

## NEW Requirements

### Requirement: Export Functions Consolidated to Common Module

Scanner-specific `format_*_output()` functions SHALL be removed and replaced with unified `export_scanner_output()` from common module.

#### Scenario: Old export functions removed

- **GIVEN** a migrated scanner module
- **WHEN** inspecting the scanner's export.py
- **THEN** the system SHALL NOT have `format_*_output()` functions
- **AND** SHALL use `export_scanner_output()` from common module

#### Scenario: New export function handles all scanners

- **GIVEN** any scanner output (http-request, signal, django-model, etc.)
- **WHEN** calling `export_scanner_output()`
- **THEN** the system SHALL correctly export the output
- **AND** NOT require scanner-specific export code
