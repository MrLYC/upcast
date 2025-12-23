# Unit Test Scanner Specification Delta

## MODIFIED Requirements

### Requirement: Unit Test Detection

The system SHALL detect Python unit tests using pytest and unittest patterns through AST analysis.

#### Scenario: Detect pytest test functions with robust file discovery

- **WHEN** scanning a Python file
- **AND** file name matches `test*.py` or `*_test.py` pattern
- **AND** file is in tests directory or subdirectory
- **THEN** the system SHALL parse the file with AST
- **AND** SHALL identify functions starting with `test_`
- **AND** SHALL extract the function name, location (file:line), and body
- **AND** SHALL verify file patterns work across different directory structures

**Rationale**: Robust file discovery is critical for scanner functionality

**DIFF**: Added emphasis on file discovery and pattern matching verification

#### Scenario: Handle test discovery in nested directories

- **WHEN** test files are in nested directory structure
- **EXAMPLES**:
  - `tests/unit/test_models.py`
  - `apiserver/paasng/tests/paasng/platform/engine/test_managers.py`
- **THEN** the system SHALL discover these files correctly
- **AND** SHALL apply test detection to all matched files
- **AND** SHALL not be blocked by directory depth

**Rationale**: Real-world projects often have deeply nested test directories

**NEW**: Explicit nested directory support requirement

#### Scenario: Debug test file discovery failures

- **WHEN** no test files are found in a directory known to contain tests
- **THEN** the system SHALL log diagnostic information if verbose mode enabled:
  - Total files scanned
  - Files matched by pattern
  - Files excluded by ignore patterns
  - Files failing AST parsing
- **AND** SHALL help diagnose configuration or path issues

**Rationale**: Empty output should be debuggable; logging helps identify root cause

**NEW**: Debug logging requirement for discovery failures

### Requirement: Test Body Analysis

The system SHALL analyze test function bodies to extract assertions, calculate checksums, and identify dependencies.

#### Scenario: Handle parsing failures gracefully

- **WHEN** test file cannot be parsed due to syntax errors
- **THEN** the system SHALL log error with file path
- **AND** SHALL continue scanning other files
- **AND** SHALL include failed file in summary stats
- **AND** SHALL not crash or return empty output for all tests

**Rationale**: Partial results are better than total failure; graceful degradation is important

**NEW**: Error handling requirement for parse failures

## ADDED Requirements

### Requirement: File Discovery Validation

The system SHALL provide diagnostic information about test file discovery.

#### Scenario: Log discovery statistics

- **WHEN** scanning completes
- **THEN** summary SHALL include:
  - Total files scanned
  - Files matching test patterns
  - Test functions/methods detected
  - Files with parsing errors
- **AND** SHALL log file discovery stats if verbose mode enabled

**Rationale**: Statistics help verify scanner is working correctly and aid debugging

#### Scenario: Validate file pattern matching

- **WHEN** scanner initializes
- **THEN** the system SHALL verify file pattern regex is valid
- **AND** SHALL test pattern against sample paths
- **AND** SHALL log pattern configuration if verbose mode enabled
- **EXAMPLES**: Test patterns like `test*.py`, `*_test.py`, `test_*.py`

**Rationale**: Pattern configuration issues can silently break file discovery

### Requirement: Empty Output Prevention

The system SHALL produce meaningful output when tests exist but detection fails.

#### Scenario: Differentiate "no tests" from "detection failed"

- **WHEN** no tests are detected
- **THEN** summary SHALL indicate whether:
  - No test files matched patterns (legitimate empty)
  - Files matched but no test functions found (possible pattern issue)
  - Files matched but parsing failed (AST error)
- **AND** SHALL provide actionable guidance in verbose mode

**Rationale**: Users need to distinguish between "no tests in project" and "scanner malfunction"

#### Scenario: Warn on empty output for known test directories

- **WHEN** scanning a directory with path containing "test" or "tests"
- **AND** no tests are detected
- **THEN** the system SHOULD log warning
- **AND** SHOULD suggest checking file patterns and ignore rules

**Rationale**: Empty output from tests directory is usually unexpected and worth investigating

## REMOVED Requirements

None - all existing requirements remain with enhanced diagnostics and error handling.
