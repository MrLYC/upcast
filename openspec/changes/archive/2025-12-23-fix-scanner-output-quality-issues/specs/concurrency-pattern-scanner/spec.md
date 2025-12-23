# Concurrency Pattern Scanner Specification Delta

## MODIFIED Requirements

### Requirement: Multiprocessing Pattern Detection

The system SHALL detect multiprocessing-based concurrency patterns including Process creation and ProcessPoolExecutor usage.

#### Scenario: Detect multiprocessing.Process creation with qualified name verification

- **WHEN** scanning for process-based concurrency
- **THEN** the system SHALL identify `multiprocessing.Process()` instantiations
- **AND** SHALL verify the class is from `multiprocessing` module using import resolution
- **AND** SHALL reject custom classes named "Process" from other modules
- **AND** SHALL reject dataclasses or Pydantic models named "Process"
- **AND** extract the target function from `target=` keyword argument
- **AND** extract process name from `name=` keyword argument if specified
- **AND** store target and name in `details` field

**Rationale**: Prevents false positives from dataclasses, models, or domain objects that happen to be named "Process"

**DIFF**: Added strict module verification requirement to prevent false positives

#### Scenario: Skip non-multiprocessing Process classes

- **WHEN** code instantiates a class named "Process" from a non-multiprocessing module
- **EXAMPLES**: `PlainProcess(...)`, `RequestProcess(...)`, `@dataclass class Process`
- **THEN** the system SHALL NOT report this as a concurrency pattern
- **AND** SHALL NOT output a record for this instantiation
- **AND** SHALL log debug message about skipped Process class

**Rationale**: Dataclasses and domain models commonly use "Process" as a name; these are not concurrency patterns

**NEW**: Explicit requirement to skip false positive patterns

### Requirement: Threading Pattern Detection

The system SHALL detect threading-based concurrency patterns including Thread creation and ThreadPoolExecutor usage.

#### Scenario: Detect threading.Thread creation with qualified name verification

- **WHEN** scanning for thread-based concurrency
- **THEN** the system SHALL identify `threading.Thread()` instantiations
- **AND** SHALL verify the class is from `threading` module using import resolution
- **AND** SHALL reject custom Thread classes from other modules
- **AND** extract the target function or callable from `target=` keyword argument
- **AND** extract thread name from `name=` keyword argument if specified
- **AND** store target and name in `details` field
- **AND** categorize under `threading.thread_creation`

**Rationale**: Same false positive prevention logic as Process detection

**DIFF**: Added module verification requirement matching Process detection fix

## REMOVED Requirements

None - all requirements remain, with stricter validation added.
