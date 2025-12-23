# Specification Delta: Data Models - Scanner Metadata

## MODIFIED Requirements

### Requirement: Scanner Output Metadata Privacy

Scanner metadata SHALL NOT include absolute file system paths that could expose local directory structure or user information.

**Rationale**: Scanner outputs should be portable across environments and not expose sensitive local path information.

#### Scenario: Environment Variable Scanner Metadata

- **GIVEN** a user running `scan-env-vars` on a project
- **WHEN** the scanner produces output
- **THEN** the metadata section SHALL contain only `scanner_name`
- **AND** SHALL NOT contain `root_path` field
- **AND** file paths in results section SHALL remain relative

**DIFF**: Removed `root_path` from env-vars scanner metadata for privacy and portability

#### Scenario: Signal Scanner Metadata

- **GIVEN** a user running `scan-signals` on a project
- **WHEN** the scanner produces output
- **THEN** the metadata section SHALL contain only `scanner_name`
- **AND** SHALL NOT contain `root_path` field
- **AND** file paths in results section SHALL remain relative

**DIFF**: Removed `root_path` from signals scanner metadata for privacy and portability

#### Scenario: Portable Scanner Outputs

- **GIVEN** scanner output files from different machines
- **WHEN** comparing or sharing results
- **THEN** metadata SHALL NOT reveal machine-specific paths
- **AND** results SHALL be comparable across environments
- **AND** no user-specific information SHALL be exposed

**DIFF**: Scanner outputs are now portable and privacy-preserving

### Requirement: Metadata Consistency

Scanner metadata fields SHALL be consistent across all scanners where applicable.

**Rationale**: Consistent metadata structure makes scanner outputs predictable and easier to consume.

#### Scenario: Standard Metadata Fields

- **GIVEN** any scanner output
- **WHEN** examining the metadata section
- **THEN** it SHALL contain `scanner_name` field
- **AND** MAY contain scanner-specific fields as needed
- **BUT** SHALL NOT contain absolute file paths

**DIFF**: Standardized metadata to avoid exposing absolute paths
