# blocking-operation-scanner Specification

## Purpose

Detect blocking operations in Python code that may cause performance issues, particularly in async/concurrent contexts. The scanner identifies common anti-patterns such as synchronous sleep calls, database locks, subprocess operations, and synchronization primitives.

## Requirements

### Requirement: Time-Based Blocking Detection

The system SHALL detect time-based blocking operations that pause execution.

#### Scenario: Detect time.sleep() calls

- **WHEN** scanning a Python file containing `time.sleep()` calls
- **THEN** the system SHALL identify each sleep call
- **AND** extract the sleep duration when it's a literal value
- **AND** extract the file path, line number, and function context
- **AND** categorize it under `time_based.sleep`

**DIFF**: New requirement for detecting blocking sleep operations

#### Scenario: Handle sleep with variable duration

- **WHEN** scanning sleep calls with variable durations like `time.sleep(timeout)`
- **THEN** the system SHALL record the sleep call
- **AND** mark duration as unresolved/variable
- **AND** include the expression used for duration

**DIFF**: Handle dynamic duration values

#### Scenario: Detect imported sleep

- **WHEN** encountering `from time import sleep`
- **THEN** the system SHALL track the import
- **AND** detect `sleep()` calls
- **AND** categorize them same as `time.sleep()`

**DIFF**: Support import variants

### Requirement: Database Locking Detection

The system SHALL detect Django ORM operations that acquire database locks.

#### Scenario: Detect select_for_update() calls

- **WHEN** scanning Django code containing `.select_for_update()` calls
- **THEN** the system SHALL identify each call
- **AND** extract the QuerySet chain context
- **AND** extract any timeout or lock parameters
- **AND** categorize under `database.select_for_update`

**DIFF**: New requirement for database locking detection

#### Scenario: Detect chained select_for_update

- **WHEN** encountering method chains like `Model.objects.filter().select_for_update()`
- **THEN** the system SHALL correctly identify the select_for_update call
- **AND** preserve the full chain context
- **AND** extract the model being queried if possible

**DIFF**: Handle Django QuerySet method chaining

### Requirement: Synchronization Primitive Detection

The system SHALL detect synchronization primitives that may block execution.

#### Scenario: Detect threading.Lock().acquire()

- **WHEN** scanning code with `threading.Lock().acquire()` calls
- **THEN** the system SHALL identify the acquire operation
- **AND** extract timeout parameter if present
- **AND** extract blocking parameter if present
- **AND** categorize under `synchronization.lock_acquire`

**DIFF**: New requirement for lock detection

#### Scenario: Detect RLock and Semaphore acquire

- **WHEN** encountering `threading.RLock().acquire()` or `threading.Semaphore().acquire()`
- **THEN** the system SHALL detect these acquire calls
- **AND** categorize them under appropriate synchronization types
- **AND** extract timeout and blocking parameters

**DIFF**: Support multiple lock types

#### Scenario: Detect with statement lock usage

- **WHEN** encountering `with threading.Lock():`
- **THEN** the system SHALL detect the implicit acquire
- **AND** categorize under `synchronization.lock_context`
- **AND** note that it's a context manager pattern

**DIFF**: Detect implicit lock acquisition

### Requirement: Subprocess Operation Detection

The system SHALL detect subprocess operations that block waiting for completion.

#### Scenario: Detect subprocess.run() calls

- **WHEN** scanning code with `subprocess.run()` calls
- **THEN** the system SHALL identify each call
- **AND** extract the command being run if it's a literal
- **AND** extract timeout parameter if present
- **AND** categorize under `subprocess.run`

**DIFF**: New requirement for subprocess detection

#### Scenario: Detect Popen.wait() calls

- **WHEN** encountering `Popen.wait()` or `proc.wait()` calls
- **THEN** the system SHALL identify the wait operation
- **AND** extract timeout parameter if present
- **AND** track the Popen instance if possible
- **AND** categorize under `subprocess.wait`

**DIFF**: Detect explicit wait operations

#### Scenario: Detect Popen.communicate() calls

- **WHEN** encountering `Popen.communicate()` or `proc.communicate()` calls
- **THEN** the system SHALL identify the communicate operation
- **AND** extract timeout parameter if present
- **AND** note this operation reads stdout/stderr until completion
- **AND** categorize under `subprocess.communicate`

**DIFF**: Detect communicate operations

#### Scenario: Handle subprocess import variants

- **WHEN** encountering various import styles
  - `import subprocess`
  - `from subprocess import run, Popen`
  - `from subprocess import run as execute`
- **THEN** the system SHALL correctly track and detect operations
- **AND** normalize them to standard categories

**DIFF**: Support import variations

### Requirement: Context Extraction

The system SHALL extract comprehensive context for each blocking operation.

#### Scenario: Extract file location

- **WHEN** detecting any blocking operation
- **THEN** the system SHALL record the file path (relative to project root)
- **AND** record the line number
- **AND** record the column number if available

**DIFF**: Standard location tracking

#### Scenario: Extract function context

- **WHEN** a blocking operation occurs inside a function
- **THEN** the system SHALL extract the enclosing function name
- **AND** extract the function signature if it's async
- **AND** flag if blocking operation is in an async function

**DIFF**: Provide context for anti-pattern detection

#### Scenario: Extract class context

- **WHEN** a blocking operation occurs inside a method
- **THEN** the system SHALL extract the class name
- **AND** extract the method name
- **AND** preserve the full qualified path

**DIFF**: Method-level context

#### Scenario: Extract statement source code

- **WHEN** detecting any blocking operation
- **THEN** the system SHALL extract the full statement source code
- **AND** preserve formatting for human readability
- **AND** limit to single statement (not entire function)

**DIFF**: Include source for review

### Requirement: Output Formatting

The system SHALL format blocking operations into structured output.

#### Scenario: Group operations by category

- **WHEN** exporting results
- **THEN** the system SHALL group operations by category:
  - `time_based`
  - `database`
  - `synchronization`
  - `subprocess`
- **AND** sort operations within each category by file path and line number

**DIFF**: Organized output structure

#### Scenario: Support YAML output

- **WHEN** output format is YAML
- **THEN** the system SHALL generate valid YAML
- **AND** use human-readable formatting
- **AND** include all extracted metadata

**DIFF**: Standard YAML support

#### Scenario: Support JSON output

- **WHEN** output format is JSON
- **THEN** the system SHALL generate valid JSON
- **AND** include all extracted metadata
- **AND** use consistent field names

**DIFF**: Standard JSON support

#### Scenario: Include summary statistics

- **WHEN** generating output
- **THEN** the system SHALL include a summary section
- **AND** count operations by category
- **AND** count total operations
- **AND** list files analyzed

**DIFF**: Provide overview information

### Requirement: CLI Interface

The system SHALL provide a command-line interface following upcast conventions.

#### Scenario: Basic scanning command

- **WHEN** user runs `upcast scan-blocking-operations /path/to/project`
- **THEN** the system SHALL scan all Python files in the path
- **AND** apply default exclusions (venv/, **pycache**, etc.)
- **AND** output results to stdout in YAML format

**DIFF**: Standard CLI behavior

#### Scenario: File filtering options

- **WHEN** user provides `--include` and `--exclude` patterns
- **THEN** the system SHALL filter files accordingly
- **AND** support glob patterns
- **AND** allow multiple patterns

**DIFF**: Standard filtering support

#### Scenario: Output file option

- **WHEN** user provides `-o output.yaml`
- **THEN** the system SHALL write results to the specified file
- **AND** create parent directories if needed

**DIFF**: Standard output redirection

#### Scenario: Format selection

- **WHEN** user provides `--format json`
- **THEN** the system SHALL output in JSON format
- **AND** support both `yaml` and `json` values

**DIFF**: Format selection support

#### Scenario: Verbose logging

- **WHEN** user provides `-v` or `--verbose` flag
- **THEN** the system SHALL enable debug logging
- **AND** show files being scanned
- **AND** show pattern matching details

**DIFF**: Standard verbose mode

### Requirement: Performance

The system SHALL scan codebases efficiently.

#### Scenario: Large codebase scanning

- **WHEN** scanning a codebase with 1000+ Python files
- **THEN** the system SHALL complete within 10 seconds
- **AND** use reasonable memory (<500MB)

**DIFF**: Performance requirement

#### Scenario: Incremental scanning

- **WHEN** scanning specific files
- **THEN** the system SHALL only analyze those files
- **AND** skip unrelated files
- **AND** maintain same output format

**DIFF**: Efficient targeted scanning
