## ADDED Requirements

### Requirement: Offset Usage Scan Command

The CLI SHALL register `scan-offset-usage` as a standard scanner command and expose the shared path, output, format, include, exclude, and verbose options.

#### Scenario: Run offset scan

- **WHEN** the user runs `upcast scan-offset-usage <path>`
- **THEN** the command SHALL scan the supplied file or directory
- **AND** write the standard YAML report to stdout by default

#### Scenario: Request JSON output and filters

- **WHEN** the user supplies `--format json`, `--output`, `--include`, or `--exclude`
- **THEN** the command SHALL honor those options using the shared scanner CLI behavior

#### Scenario: Inspect command help

- **WHEN** the user runs `upcast scan-offset-usage --help`
- **THEN** help SHALL describe QuerySet slices, paginator/DRF patterns, raw SQL, and static-analysis limits
