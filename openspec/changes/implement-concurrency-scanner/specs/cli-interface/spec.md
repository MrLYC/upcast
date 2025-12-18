# cli-interface Specification

## MODIFIED Requirements

### Requirement: CLI Command Structure

The system SHALL provide scanner commands for analyzing Python codebases.

#### Scenario: Add scan-concurrency command

- **WHEN** user needs to scan for Python concurrency patterns
- **THEN** the system SHALL provide `scan-concurrency` command
- **AND** accept path argument (file or directory) as first positional argument
- **AND** support standard options: `-o/--output`, `-v/--verbose`, `--include`, `--exclude`
- **AND** follow the same CLI patterns as other scanner commands

**DIFF**: New scan-concurrency command for detecting asyncio, threading, and multiprocessing patterns
