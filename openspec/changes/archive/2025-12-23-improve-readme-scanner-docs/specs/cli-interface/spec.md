# Specification Delta: CLI Interface Documentation

## MODIFIED Requirements

### Requirement: Scanner Documentation Structure

The README SHALL organize scanner documentation under a dedicated "Scanners" section with consistent subsections for each scanner.

**Rationale**: Users need a clear, navigable structure to find scanner information quickly.

#### Scenario: Scanners Section Navigation

- **GIVEN** a user reading the README
- **WHEN** they want to learn about available scanners
- **THEN** they SHALL find a clear "## Scanners" section
- **AND** scanners SHALL be grouped by category:
  - Django Scanners (4)
  - Code Analysis Scanners (3)
  - Infrastructure Scanners (2)
  - HTTP & Exception Scanners (2)
  - Code Quality Scanners (1)
- **AND** each scanner SHALL have a consistent subsection with:
  - Brief description
  - Command-line usage example
  - Representative output example
  - Key features list

#### Scenario: Example Output Integration

- **GIVEN** a user learning about a specific scanner
- **WHEN** they read the scanner documentation
- **THEN** the documentation SHALL reference the example output file in `example/scan-results/`
- **AND** SHALL include representative snippets from that file
- **AND** SHALL explain the output structure

#### Scenario: Complete Scanner Coverage

- **GIVEN** the README documentation
- **WHEN** reviewing scanner coverage
- **THEN** all 12 scanners SHALL be documented:
  - `scan-django-models`
  - `scan-django-settings`
  - `scan-django-urls`
  - `scan-signals`
  - `scan-concurrency-patterns`
  - `scan-blocking-operations`
  - `scan-unit-tests`
  - `scan-env-vars`
  - `scan-prometheus-metrics`
  - `scan-http-requests`
  - `scan-exception-handlers`
  - `scan-complexity-patterns`
- **AND** each SHALL follow the same documentation template

### Requirement: Documentation Consistency

Each scanner section SHALL follow a standardized format for predictability and ease of use.

**Rationale**: Consistent structure helps users quickly find the information they need across different scanners.

#### Scenario: Standardized Scanner Subsections

- **GIVEN** any scanner documentation section
- **WHEN** a user reads it
- **THEN** it SHALL include these elements in order:
  1. A heading with the command name (e.g., "### scan-django-models")
  2. A brief description (1-2 sentences)
  3. A usage example with the basic command
  4. An "**Output example:**" subsection with YAML snippet
  5. A "**Key features:**" list highlighting scanner capabilities
- **AND** the format SHALL be identical across all scanner sections

#### Scenario: Example Output Validation

- **GIVEN** output examples in scanner documentation
- **WHEN** users reference these examples
- **THEN** the examples SHALL be taken from actual files in `example/scan-results/`
- **AND** SHALL accurately represent current scanner output format
- **AND** SHALL be updated when scanner output format changes
