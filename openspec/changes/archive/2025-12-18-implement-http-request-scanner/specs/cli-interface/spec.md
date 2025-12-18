# cli-interface Specification Delta

## ADDED Requirements

### Requirement: scan-http-requests Command

The system SHALL provide a `scan-http-requests` command to detect and analyze HTTP/API requests in Python code.

#### Scenario: Basic usage

- **WHEN** user runs `upcast scan-http-requests <path>`
- **THEN** the system SHALL scan the specified path for HTTP requests
- **AND** output results in YAML format to stdout

#### Scenario: Output to file

- **WHEN** user runs `upcast scan-http-requests <path> -o output.yaml`
- **THEN** the system SHALL write results to the specified file
- **AND** create parent directories if needed

#### Scenario: JSON format output

- **WHEN** user runs `upcast scan-http-requests <path> --format json`
- **THEN** the system SHALL output results in JSON format instead of YAML

#### Scenario: Include patterns

- **WHEN** user runs `upcast scan-http-requests <path> --include "*/api/*.py"`
- **THEN** the system SHALL only scan files matching the glob pattern

#### Scenario: Exclude patterns

- **WHEN** user runs `upcast scan-http-requests <path> --exclude "*/tests/*.py"`
- **THEN** the system SHALL skip files matching the glob pattern

#### Scenario: Verbose mode

- **WHEN** user runs `upcast scan-http-requests <path> -v`
- **THEN** the system SHALL enable debug logging
- **AND** show detailed processing information

#### Scenario: Command help

- **WHEN** user runs `upcast scan-http-requests --help`
- **THEN** the system SHALL display usage information
- **AND** document all available options
- **AND** provide examples
