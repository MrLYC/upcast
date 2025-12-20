# env-var-scanner Specification

## MODIFIED Requirements

### Requirement: CLI Interface

The system SHALL provide a command-line interface for scanning projects and files.

#### Scenario: CLI respects include patterns

- **WHEN** user runs `upcast scan-env-vars <path> --include "*/settings.py"`
- **THEN** the system SHALL only scan files matching the include pattern
- **AND** pass the pattern to `scan_directory()` function
- **AND** use `collect_python_files()` with filtering enabled

**DIFF**: Fixed bug where --include option was accepted but ignored

#### Scenario: CLI respects exclude patterns

- **WHEN** user runs `upcast scan-env-vars <path> --exclude "*/tests/*.py"`
- **THEN** the system SHALL skip files matching the exclude pattern
- **AND** pass the pattern to `scan_directory()` function
- **AND** apply exclusions during file collection

**DIFF**: Fixed bug where --exclude option was accepted but ignored

#### Scenario: CLI respects no-default-excludes flag

- **WHEN** user runs `upcast scan-env-vars <path> --no-default-excludes`
- **THEN** the system SHALL not apply default exclude patterns (venv/, **pycache**/, etc.)
- **AND** pass `use_default_excludes=False` to file collection utilities
- **AND** scan all Python files including those normally excluded

**DIFF**: Fixed bug where --no-default-excludes flag was accepted but ignored

## ADDED Requirements

### Requirement: File Filtering Support

The system SHALL support file filtering in scanner functions to enable CLI filtering features.

#### Scenario: scan_directory accepts filtering parameters

- **WHEN** calling `scan_directory()` function
- **THEN** the function SHALL accept optional parameters:
  - `include_patterns: list[str] | None` - Glob patterns for files to include
  - `exclude_patterns: list[str] | None` - Glob patterns for files to exclude
  - `use_default_excludes: bool` - Whether to apply default exclusions (default: True)
- **AND** pass these parameters to `collect_python_files()` utility

**DIFF**: Added filtering parameters to scan_directory function signature

#### Scenario: Filtering is applied during file collection

- **WHEN** filtering parameters are provided to `scan_directory()`
- **THEN** the function SHALL use `collect_python_files()` with the filtering options
- **AND** only scan files that match the filtering criteria
- **AND** respect pattern precedence (exclude wins over include)

**DIFF**: Filtering is now applied before scanning, enabling CLI filtering features
