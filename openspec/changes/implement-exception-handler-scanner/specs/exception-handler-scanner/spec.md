# exception-handler-scanner Specification

## Purpose

Detect and analyze exception handling patterns in Python codebases to identify anti-patterns, validate logging practices, and provide structured documentation of try/except/else/finally blocks.

## Requirements

### Requirement: Try Block Detection

The system SHALL detect all try/except/else/finally blocks and extract their structural information.

#### Scenario: Detect basic try/except block

- **WHEN** scanning a Python file containing `try/except` blocks
- **THEN** the system SHALL identify each try block
- **AND** extract the file path and line range
- **AND** calculate the number of lines in the try body
- **AND** categorize under `exception_handlers`

**DIFF**: New requirement for detecting exception handling structures

#### Scenario: Detect try/except/else structure

- **WHEN** scanning try blocks with else clauses
- **THEN** the system SHALL detect the else clause
- **AND** extract the else block's line number
- **AND** calculate the number of lines in the else body
- **AND** include in handler structure as `else_clause`

**DIFF**: Support for else clause detection

#### Scenario: Detect try/except/finally structure

- **WHEN** scanning try blocks with finally clauses
- **THEN** the system SHALL detect the finally clause
- **AND** extract the finally block's line number
- **AND** calculate the number of lines in the finally body
- **AND** include in handler structure as `finally_clause`

**DIFF**: Support for finally clause detection

#### Scenario: Calculate block line counts

- **WHEN** processing each try block section
- **THEN** the system SHALL count the number of lines in try body
- **AND** count lines in each except clause body
- **AND** count lines in else clause if present
- **AND** count lines in finally clause if present
- **AND** report all line counts in output

**DIFF**: Line count metrics for each block section

### Requirement: Exception Type Extraction

The system SHALL extract and classify exception types from except clauses.

#### Scenario: Extract single exception type

- **WHEN** scanning except clause with single exception type
- **THEN** the system SHALL extract the exception class name
- **AND** resolve qualified name (e.g., `ValueError`, `requests.HTTPError`)
- **AND** store in `exception_types` list

**DIFF**: Single exception type extraction

#### Scenario: Extract multiple exception types

- **WHEN** scanning except clause with tuple of exceptions
- **THEN** the system SHALL extract all exception class names
- **AND** resolve each to qualified name
- **AND** store all types in `exception_types` list
- **AND** preserve order from source code

**DIFF**: Multiple exception types from tuple

#### Scenario: Detect bare except clause

- **WHEN** scanning except clause without exception type
- **THEN** the system SHALL identify it as bare except
- **AND** store empty list in `exception_types`
- **AND** flag as potential anti-pattern

**DIFF**: Bare except detection for anti-pattern analysis

### Requirement: Logging Detection

The system SHALL count logging calls within except blocks by severity level.

#### Scenario: Count logger.error() calls

- **WHEN** scanning except block containing `logger.error()` calls
- **THEN** the system SHALL increment `log_error_count`
- **AND** count each distinct error() call

**DIFF**: Error level logging counting

#### Scenario: Count logger.exception() calls

- **WHEN** scanning except block containing `logger.exception()` calls
- **THEN** the system SHALL increment `log_exception_count`
- **AND** count each distinct exception() call

**DIFF**: Exception level logging counting

#### Scenario: Count all logging levels

- **WHEN** scanning except blocks with logging calls
- **THEN** the system SHALL count each logging level separately
- **AND** support levels: debug, info, warning, error, exception, critical
- **AND** store counts as: `log_debug_count`, `log_info_count`, `log_warning_count`, `log_error_count`, `log_exception_count`, `log_critical_count`

**DIFF**: Separate counters for each logging level

#### Scenario: Support different logger naming conventions

- **WHEN** scanning for logging calls
- **THEN** the system SHALL recognize various logger variable names
- **AND** support `logger`, `log`, `LOG`, `LOGGER`, `_logger`
- **AND** support instance loggers: `self.logger`, `cls.logger`
- **AND** support module-level loggers

**DIFF**: Flexible logger name detection

#### Scenario: Initialize all counters to zero

- **WHEN** processing except clause without logging calls
- **THEN** the system SHALL set all log level counters to 0

**DIFF**: Explicit zero initialization

### Requirement: Control Flow Analysis

The system SHALL count control flow statements within except blocks.

#### Scenario: Count pass statements

- **WHEN** scanning except block containing `pass` statements
- **THEN** the system SHALL increment `pass_count` for each pass

**DIFF**: Pass statement counting

#### Scenario: Count return statements

- **WHEN** scanning except block containing `return` statements
- **THEN** the system SHALL increment `return_count` for each return

**DIFF**: Return statement counting

#### Scenario: Count raise statements

- **WHEN** scanning except block containing `raise` statements
- **THEN** the system SHALL increment `raise_count` for each raise
- **AND** count both bare raise and raise with exception

**DIFF**: Raise statement counting

#### Scenario: Count break and continue statements

- **WHEN** scanning except block in loop context
- **THEN** the system SHALL increment `break_count` for each break
- **AND** increment `continue_count` for each continue

**DIFF**: Loop control flow counting

#### Scenario: Initialize all counters to zero

- **WHEN** processing except clause
- **THEN** the system SHALL initialize all control flow counters to 0
- **AND** provide counts as: `pass_count`, `return_count`, `break_count`, `continue_count`, `raise_count`

**DIFF**: Explicit counter initialization

### Requirement: Summary Statistics

The system SHALL calculate and report summary statistics about exception handling patterns.

#### Scenario: Calculate exception handler counts

- **WHEN** aggregating scan results
- **THEN** the system SHALL count total try blocks
- **AND** count total except clauses across all try blocks
- **AND** report in summary section

**DIFF**: Basic counting statistics

#### Scenario: Calculate bare except statistics

- **WHEN** aggregating scan results
- **THEN** the system SHALL count except clauses with empty exception_types
- **AND** report as `bare_excepts` in summary

**DIFF**: Bare except counting

#### Scenario: Calculate control flow statistics

- **WHEN** aggregating scan results
- **THEN** the system SHALL count except clauses with pass statements
- **AND** count except clauses with return statements
- **AND** count except clauses with raise statements
- **AND** report as `except_with_pass`, `except_with_return`, `except_with_raise` in summary

**DIFF**: Control flow usage statistics

#### Scenario: Calculate logging statistics

- **WHEN** aggregating scan results
- **THEN** the system SHALL count total logging calls across all levels
- **AND** count except clauses without any logging
- **AND** report as `total_log_calls` and `except_without_logging` in summary

**DIFF**: Logging usage statistics

### Requirement: YAML Output Format

The system SHALL export exception handler information in structured YAML format.

#### Scenario: Format exception handler output

- **WHEN** exporting scan results
- **THEN** the system SHALL output YAML with `exception_handlers` list
- **AND** include summary section with statistics
- **AND** format each handler with all detected information
- **AND** use null for absent optional fields (else_clause, finally_clause)

**DIFF**: Structured YAML output format

#### Scenario: Sort handlers by location

- **WHEN** formatting output
- **THEN** the system SHALL sort handlers by file path
- **AND** sort by line number within same file
- **AND** produce consistent output order

**DIFF**: Deterministic output ordering

## ADDED Requirements

### Requirement: CLI Integration

The system SHALL provide a command-line interface following project conventions.

#### Scenario: Add scan-exception-handlers command

- **WHEN** user needs to scan for exception handling patterns
- **THEN** the system SHALL provide `scan-exception-handlers` command
- **AND** accept path argument (file or directory) as first positional argument
- **AND** support standard options: `-o/--output`, `-v/--verbose`, `--include`, `--exclude`
- **AND** follow the same CLI patterns as other scanner commands

**DIFF**: New scan-exception-handlers command

#### Scenario: Support file filtering

- **WHEN** running scan-exception-handlers
- **THEN** the system SHALL support `--include` patterns for file matching
- **AND** support `--exclude` patterns for file exclusion
- **AND** use common pattern matching utilities
- **AND** respect default exclusions (venv, migrations, etc.)

**DIFF**: File filtering support
