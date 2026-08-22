## ADDED Requirements

### Requirement: Queue Usage Command Registration

The CLI SHALL register `scan-queue-usage` as a standard `scan-*` command and expose the shared path, output, format, include, exclude, and verbose options.

#### Scenario: Show queue usage help

- **WHEN** the user runs `upcast scan-queue-usage --help`
- **THEN** the help SHALL describe static queue parameter analysis
- **AND** show at least two usage examples
