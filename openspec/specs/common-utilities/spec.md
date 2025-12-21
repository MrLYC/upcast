# common-utilities Specification

## Purpose

TBD - created by archiving change refactor-scanner-architecture. Update Purpose after archive.

## Requirements

### Requirement: Unified File Discovery

The system SHALL provide a unified file discovery utility that all scanners can use to collect Python files with consistent filtering behavior.

#### Scenario: Collect Python files from directory

- **WHEN** given a directory path
- **THEN** the system SHALL recursively find all `*.py` files
- **AND** exclude default patterns (venv/, **pycache**/, build/, dist/, .tox/, node_modules/)
- **AND** return absolute paths sorted alphabetically

#### Scenario: Collect Python files from single file

- **WHEN** given a single `.py` file path
- **THEN** the system SHALL return that file in a list
- **AND** validate the file exists and is readable

#### Scenario: Apply include patterns

- **WHEN** user provides `--include` patterns
- **THEN** the system SHALL only include files matching at least one include pattern
- **AND** use glob pattern matching (not regex)
- **AND** match patterns relative to scan root

#### Scenario: Apply exclude patterns

- **WHEN** user provides `--exclude` patterns
- **THEN** the system SHALL exclude files matching any exclude pattern
- **AND** apply default excludes unless disabled with `--no-default-excludes`
- **AND** exclude patterns take precedence over include patterns

### Requirement: Python Package Root Detection

The system SHALL detect Python package root by locating `__init__.py` files to enable correct module path resolution.

#### Scenario: Find package root by walking up

- **WHEN** given a path inside a Python package
- **THEN** the system SHALL walk up parent directories
- **AND** stop at the first directory without `__init__.py`
- **AND** return the last directory that HAD `__init__.py` as package root

#### Scenario: Fallback when no package found

- **WHEN** no `__init__.py` files found in parent chain
- **THEN** the system SHALL return the original path as fallback
- **AND** log a warning in verbose mode

#### Scenario: Handle nested packages

- **WHEN** multiple nested packages exist
- **THEN** the system SHALL return the outermost package root
- **EXAMPLE**: `/project/src/myapp/__init__.py` → return `/project/src/myapp/`

### Requirement: Unified AST Inference with Fallback

The system SHALL provide unified astroid inference functions with explicit fallback markers for failed inferences.

#### Scenario: Successful value inference

- **WHEN** astroid successfully infers a literal value
- **THEN** the system SHALL return (value, True)
- **AND** value SHALL be the Python literal (str, int, bool, float, None, list, dict)

#### Scenario: Failed value inference with backtick marker

- **WHEN** astroid inference fails or returns Uninferable
- **THEN** the system SHALL return (`` `expression` ``, False)
- **AND** wrap the original AST expression in backticks
- **AND** preserve the expression string for debugging

#### Scenario: Successful type inference

- **WHEN** astroid successfully infers a type
- **THEN** the system SHALL return the fully qualified type name
- **EXAMPLE**: `django.db.models.CharField` not just `CharField`

#### Scenario: Failed type inference with unknown marker

- **WHEN** type inference fails
- **THEN** the system SHALL return `"unknown"` as type
- **AND** log failure in verbose mode

### Requirement: Unified Export with Sorted Output

The system SHALL provide unified YAML/JSON export functions with consistent field sorting.

#### Scenario: Export to YAML with sorted keys

- **WHEN** exporting data to YAML
- **THEN** the system SHALL sort top-level dictionary keys alphabetically
- **AND** sort nested dictionaries recursively
- **AND** sort list elements where applicable (e.g., usages by file/line)
- **AND** use UTF-8 encoding with 2-space indentation

#### Scenario: Export to JSON with sorted keys

- **WHEN** exporting data to JSON
- **THEN** the system SHALL sort keys alphabetically at all levels
- **AND** use 2-space indentation for readability
- **AND** ensure UTF-8 encoding

#### Scenario: Consistent collection sorting

- **WHEN** exporting collections like usages or locations
- **THEN** the system SHALL sort by primary key (file path)
- **AND** then by secondary key (line number)
- **AND** then by tertiary key (column number) if applicable

### Requirement: Qualified Name Resolution

The system SHALL resolve fully qualified names for types and classes using astroid's semantic analysis.

#### Scenario: Get qualified name from astroid node

- **WHEN** given an astroid ClassDef or FunctionDef node
- **THEN** the system SHALL return the fully qualified name
- **EXAMPLE**: Node for `CharField` → `"django.db.models.fields.CharField"`

#### Scenario: Handle inference failures for qualified names

- **WHEN** qualified name cannot be determined
- **THEN** the system SHALL return `` `node.as_string()` `` wrapped in backticks
- **AND** avoid raising exceptions

### Requirement: Path Validation

The system SHALL validate input paths before scanning and provide clear error messages.

#### Scenario: Validate existing path

- **WHEN** given a path that exists
- **THEN** the system SHALL return a Path object
- **AND** verify it's either a file or directory

#### Scenario: Reject nonexistent path

- **WHEN** given a path that doesn't exist
- **THEN** the system SHALL raise FileNotFoundError
- **AND** include the invalid path in error message

#### Scenario: Reject invalid path type

- **WHEN** given a path that is neither file nor directory (e.g., socket, device)
- **THEN** the system SHALL raise ValueError
- **AND** explain that only files and directories are supported

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
