## ADDED Requirements

### Requirement: Generate a Markdown project analysis report

The system SHALL provide a `generate-report` command that aggregates saved scanner YAML results into a deterministic Markdown report.

#### Scenario: Generate a report from available scanner results

- **WHEN** a user runs `upcast generate-report <scan-results-dir>`
- **THEN** the command SHALL load top-level YAML scanner results
- **AND** include an executive summary with scanner count, files scanned, and findings count when those fields exist
- **AND** include sections for each supported scanner family that is present

#### Scenario: Write the report to a file

- **WHEN** a user provides `-o/--output <path>`
- **THEN** the command SHALL write the Markdown report to that path
- **AND** report completion without dumping the full report to stdout

#### Scenario: Handle partial or newer input safely

- **WHEN** the input directory contains only a subset of scanner YAML files or fields unknown to the generator
- **THEN** the command SHALL still produce a report
- **AND** SHALL omit unavailable subsections or use zero/unknown summaries rather than crash

### Requirement: Preserve report determinism

The report generator SHALL produce stable section and key ordering for the same input files.

#### Scenario: Repeat the same generation

- **WHEN** the same YAML input is loaded twice
- **THEN** both generated Markdown strings SHALL be identical
