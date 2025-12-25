# logging-scanner Specification

## Purpose

TBD - created by archiving change add-logging-scanner. Update Purpose after archive.

## Requirements

### Requirement: Standard Library Logging Detection

The system SHALL detect logging calls using Python's standard `logging` module.

#### Scenario: Detect logger.info() with resolved module path

- **GIVEN** a Python file at `myapp/services/auth.py`
- **AND** the file contains `logger = logging.getLogger(__name__)`
- **AND** the file contains `logger.info("User logged in")`
- **WHEN** scanning the file
- **THEN** the system SHALL detect the log call
- **AND** resolve logger_name to `myapp.services.auth`
- **AND** record level as `info`
- **AND** record message as `"User logged in"`
- **AND** record lineno where the call occurs

**Rationale**: Standard logging with `__name__` is the most common pattern and requires module path resolution.

#### Scenario: Detect root logger calls

- **GIVEN** a Python file contains `logger = logging.getLogger()`
- **OR** contains `logging.info("message")`
- **WHEN** scanning the file
- **THEN** the system SHALL resolve logger_name to `root`
- **AND** detect the log call with correct level and message

**Rationale**: Root logger is used when no name is specified.

#### Scenario: Detect custom logger names

- **GIVEN** code contains `logger = logging.getLogger("myapp.custom")`
- **WHEN** scanning the file
- **THEN** the system SHALL use `"myapp.custom"` as logger_name
- **AND** preserve the exact string provided

**Rationale**: Custom logger names should be recorded as-is.

#### Scenario: Detect all logging levels

- **WHEN** code uses `logger.debug()`, `logger.info()`, `logger.warning()`, `logger.error()`, `logger.critical()`
- **THEN** the system SHALL detect each call
- **AND** record the correct level for each

**Rationale**: All log levels need to be tracked.

### Requirement: Multi-Library Support

The system SHALL detect logging calls from loguru, structlog, and Django logging utilities.

#### Scenario: Detect loguru logging

- **GIVEN** code contains `from loguru import logger`
- **AND** contains `logger.info("message")`
- **WHEN** scanning the file
- **THEN** the system SHALL categorize the call under the `loguru` library
- **AND** resolve logger_name from module path
- **AND** record the log call details

**Rationale**: Loguru is a popular alternative logging library.

#### Scenario: Detect structlog logging

- **GIVEN** code contains `import structlog`
- **AND** contains `logger = structlog.get_logger()`
- **AND** contains `logger.info("message")`
- **WHEN** scanning the file
- **THEN** the system SHALL categorize under `structlog` library
- **AND** detect the log call

**Rationale**: Structlog is commonly used for structured logging.

#### Scenario: Organize results by library

- **GIVEN** a file with logging calls from multiple libraries
- **WHEN** generating output
- **THEN** the system SHALL group results by library
- **AND** create separate lists for `logging`, `loguru`, `structlog`, `django`

**Rationale**: Users need to understand which libraries are in use.

### Requirement: Message and Argument Extraction

The system SHALL extract complete message strings and arguments from logging calls.

#### Scenario: Extract plain string message

- **GIVEN** code contains `logger.info("User logged in")`
- **WHEN** extracting the message
- **THEN** the system SHALL record message as `"User logged in"`
- **AND** record type as `string`
- **AND** record args as empty list

**Rationale**: Simple string messages are the baseline.

#### Scenario: Extract message with positional arguments

- **GIVEN** code contains `logger.info("User %s logged in", username)`
- **WHEN** extracting details
- **THEN** the system SHALL record message as `"User %s logged in"`
- **AND** record args as `["username"]`
- **AND** record type as `percent`

**Rationale**: Printf-style formatting is common in logging.

#### Scenario: Extract f-string message

- **GIVEN** code contains `logger.info(f"User {username} logged in")`
- **WHEN** extracting details
- **THEN** the system SHALL record the complete f-string
- **AND** record type as `fstring`
- **AND** extract variable names from f-string into args

**Rationale**: F-strings are increasingly common in Python 3.6+.

#### Scenario: Extract str.format() message

- **GIVEN** code contains `logger.info("User {} logged in".format(username))`
- **WHEN** extracting details
- **THEN** the system SHALL record the format string
- **AND** record type as `format`
- **AND** extract arguments from format() call

**Rationale**: str.format() is another common formatting style.

### Requirement: Sensitive Information Detection

The system SHALL detect potential sensitive information in log messages and arguments.

#### Scenario: Flag password keywords in message

- **GIVEN** code contains `logger.info("Password is %s", pwd)`
- **OR** contains `logger.debug(f"User password: {password}")`
- **WHEN** analyzing the log call
- **THEN** the system SHALL set has_sensitive to True
- **AND** record matched pattern in sensitive_patterns list
- **AND** include patterns like `password`, `pwd`, `passwd`

**Rationale**: Logging passwords is a critical security issue.

#### Scenario: Flag token and API key patterns

- **GIVEN** message or args contain keywords: `token`, `api_key`, `secret`, `private_key`
- **WHEN** analyzing the log call
- **THEN** the system SHALL flag as sensitive
- **AND** record the matched keywords

**Rationale**: Tokens and keys should not be logged in plain text.

#### Scenario: Detect JWT tokens in message

- **GIVEN** message contains pattern matching JWT format (e.g., `eyJ...`)
- **WHEN** analyzing the log call
- **THEN** the system SHALL flag as sensitive
- **AND** record pattern as `jwt_token`

**Rationale**: JWT tokens in logs are a security risk.

#### Scenario: Flag sensitive variable names in arguments

- **GIVEN** code contains `logger.info("Key: %s", api_key)`
- **WHEN** analyzing arguments
- **THEN** the system SHALL detect `api_key` as sensitive variable name
- **AND** flag the call as sensitive

**Rationale**: Even if message is generic, sensitive variable names indicate risk.

#### Scenario: Exclude false positive keywords

- **GIVEN** message contains common terms like `user`, `name`, `id`, `value`
- **WHEN** analyzing for sensitive data
- **THEN** the system SHALL NOT flag these as sensitive
- **AND** only flag high-confidence patterns

**Rationale**: Too many false positives reduce usefulness.

### Requirement: Advanced Pattern Detection

The system SHALL detect logging calls through various access patterns beyond direct logger.method() calls.

#### Scenario: Detect instance attribute logger

- **GIVEN** code contains `self.logger.info("message")`
- **OR** contains `cls.logger.warning("message")`
- **WHEN** scanning the file
- **THEN** the system SHALL detect the log call
- **AND** resolve logger_name from module path

**Rationale**: Logger stored as instance/class attribute is common in OOP code.

#### Scenario: Detect conditional logging

- **GIVEN** code contains:
  ```python
  if logger.isEnabledFor(logging.DEBUG):
      logger.debug("Debug info")
  ```
- **WHEN** scanning the file
- **THEN** the system SHALL detect the debug() call
- **AND** mark it as conditional

**Rationale**: Performance-sensitive code uses conditional logging.

#### Scenario: Detect logger in exception handling

- **GIVEN** code contains logger calls within try/except blocks
- **WHEN** scanning the file
- **THEN** the system SHALL detect these calls
- **AND** note they occur in exception context

**Rationale**: Exception logging is common and important to track.

### Requirement: Module Path Resolution

The system SHALL resolve logger names using `__name__` to actual module paths based on file location.

#### Scenario: Resolve **name** to package module path

- **GIVEN** file at `myproject/services/auth/__init__.py`
- **AND** project root is `myproject/`
- **AND** code contains `logging.getLogger(__name__)`
- **WHEN** resolving logger name
- **THEN** the system SHALL resolve to `myproject.services.auth`

**Rationale**: Accurate module path helps understand logger hierarchy.

#### Scenario: Handle **main** in module files

- **GIVEN** a module file (not `__main__.py`)
- **AND** code contains `if __name__ == "__main__": logging.info("msg")`
- **WHEN** resolving logger name
- **THEN** the system SHALL use the module path, not `__main__`

**Rationale**: **main** should be replaced with actual module path.

### Requirement: Output Format and Organization

The system SHALL organize results by file and provide comprehensive statistics.

#### Scenario: Group results by file path

- **WHEN** generating output
- **THEN** the results dictionary SHALL be keyed by relative file path
- **AND** each file SHALL have a FileLoggingInfo object
- **AND** each FileLoggingInfo SHALL contain separate lists per library

**Rationale**: Consistent with other upcast scanners.

#### Scenario: Provide summary statistics

- **WHEN** generating output
- **THEN** the summary SHALL include total_log_calls count
- **AND** include files_scanned count
- **AND** include scan_duration_ms
- **AND** include by_library breakdown (counts per library)
- **AND** include by_level breakdown (counts per level)
- **AND** include sensitive_calls count

**Rationale**: Summary helps understand overall logging patterns.

### Requirement: Performance and Scalability

The system SHALL efficiently process large codebases with many logging calls.

#### Scenario: Process 1000 files in reasonable time

- **GIVEN** a codebase with 1000 Python files
- **WHEN** running the scanner
- **THEN** the scan SHALL complete in under 30 seconds
- **AND** memory usage SHALL remain under 500MB

**Rationale**: Scanner must be practical for large projects.

#### Scenario: Handle files with many log calls

- **GIVEN** a file with 100+ logging calls
- **WHEN** scanning the file
- **THEN** all calls SHALL be detected
- **AND** processing SHALL not degrade significantly

**Rationale**: Some files have extensive logging.
