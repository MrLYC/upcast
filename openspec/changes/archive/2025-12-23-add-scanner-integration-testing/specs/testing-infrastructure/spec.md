# Testing Infrastructure Specification Delta

## ADDED Requirements

### Requirement: Integration Test Command

The system SHALL provide a Makefile command to run all scanners on a real-world project.

#### Scenario: Run all scanners on example project

- **WHEN** developer runs `make test-integration`
- **THEN** the system SHALL execute all 12 scanners sequentially
- **AND** SHALL scan the `example/blueking-paas` directory
- **AND** SHALL output results to `example/scan-results/*.yaml`
- **AND** SHALL use YAML format for human readability
- **AND** SHALL complete within 2 minutes

**Rationale**: Provides automated validation that all scanners work on a large, realistic codebase.

#### Scenario: Scanner-specific configuration

- **WHEN** running integration tests
- **THEN** each scanner SHALL use appropriate options
- **AND** complexity scanner SHALL use threshold=10
- **AND** django-settings scanner SHALL use mode=usage
- **AND** all scanners SHALL use default exclude patterns

**Rationale**: Ensures realistic scanner configurations are tested.

#### Scenario: Handle scanner failures gracefully

- **WHEN** a scanner fails during integration test
- **THEN** the system SHALL continue running remaining scanners
- **AND** SHALL save partial results
- **AND** SHALL report which scanner failed
- **AND** SHALL exit with non-zero code

**Rationale**: One failing scanner shouldn't block testing others.

### Requirement: Result Baseline Management

The system SHALL maintain baseline scan results for regression detection.

#### Scenario: Store baseline results

- **WHEN** integration tests complete
- **THEN** the system SHALL store results in `example/scan-results-baseline/`
- **AND** SHALL version control baseline files
- **AND** SHALL maintain one YAML file per scanner (12 total)

**Rationale**: Baseline enables automatic detection of output regressions.

#### Scenario: Update baseline

- **WHEN** scanner behavior intentionally changes
- **THEN** developer SHALL run `make test-integration`
- **AND** SHALL copy new results to baseline directory
- **AND** SHALL commit updated baseline files
- **AND** SHALL document changes in commit message

**Rationale**: Explicit baseline updates prevent accidental regressions.

#### Scenario: Validate baseline completeness

- **WHEN** baseline is established
- **THEN** all 12 scanner outputs SHALL be present
- **AND** each file SHALL contain valid YAML
- **AND** each file SHALL have a `results` section
- **AND** no file SHALL be empty

**Rationale**: Incomplete baseline would cause false negatives.

### Requirement: CI Integration Test Workflow

The system SHALL provide a GitHub Action to validate scan result consistency.

#### Scenario: Run integration tests in CI

- **WHEN** PR is opened or updated
- **THEN** the workflow SHALL checkout code with submodules
- **AND** SHALL set up Python and uv environment
- **AND** SHALL run `make test-integration`
- **AND** SHALL upload scan results as artifacts

**Rationale**: Automated validation on every change.

#### Scenario: Compare results against baseline

- **WHEN** integration tests complete in CI
- **THEN** the workflow SHALL extract `results` section from each YAML
- **AND** SHALL compare against baseline using deterministic diff
- **AND** SHALL ignore metadata fields (scan_duration_ms, timestamps)
- **AND** SHALL fail if results differ
- **AND** SHALL display unified diff output

**Rationale**: Only semantic changes should be detected, not timing variations.

#### Scenario: Handle missing baseline

- **WHEN** baseline file doesn't exist for a scanner
- **THEN** the workflow SHALL skip comparison for that scanner
- **AND** SHALL print warning message
- **AND** SHALL NOT fail the workflow

**Rationale**: New scanners can be added without immediate baseline.

#### Scenario: Provide actionable failure output

- **WHEN** results comparison fails
- **THEN** the workflow SHALL show which scanner outputs changed
- **AND** SHALL display unified diff for each change
- **AND** SHALL provide instructions for updating baseline
- **AND** SHALL include link to scan result artifacts

**Rationale**: Developers need clear information to resolve failures.

### Requirement: Deterministic Scanner Output

The system SHALL ensure scanners produce identical results on repeated runs.

#### Scenario: Stable output ordering

- **WHEN** scanner runs multiple times on same code
- **THEN** output SHALL maintain consistent ordering
- **AND** SHALL sort results by file path and line number
- **AND** SHALL use deterministic dictionary key ordering

**Rationale**: Non-deterministic output causes false positives in comparisons.

#### Scenario: Exclude non-deterministic metadata

- **WHEN** comparing scan results
- **THEN** the comparison SHALL exclude `scan_duration_ms`
- **AND** SHALL exclude any timestamp fields
- **AND** SHALL only compare `results` section content

**Rationale**: Timing varies between runs, not a regression indicator.

#### Scenario: Validate determinism

- **WHEN** integration tests run
- **THEN** developer SHOULD be able to run twice locally
- **AND** both runs SHOULD produce identical `results` sections
- **AND** any non-determinism SHALL be considered a bug

**Rationale**: Ensures comparison logic is reliable.

### Requirement: Performance Monitoring

The system SHALL track integration test performance.

#### Scenario: Measure scan duration

- **WHEN** integration tests run
- **THEN** the system SHALL measure total execution time
- **AND** SHALL report time in workflow output
- **AND** SHALL warn if exceeds 2 minutes

**Rationale**: Performance regressions should be visible.

#### Scenario: Identify slow scanners

- **WHEN** analyzing performance
- **THEN** the system SHOULD track per-scanner duration
- **AND** SHOULD identify scanners taking > 15 seconds
- **AND** SHOULD report slowest scanners in summary

**Rationale**: Helps prioritize performance optimizations.

### Requirement: Documentation

The system SHALL document integration testing for developers.

#### Scenario: Document testing workflow

- **WHEN** developer needs to run integration tests
- **THEN** README SHALL explain `make test-integration` command
- **AND** SHALL describe purpose of integration testing
- **AND** SHALL provide examples of typical output

**Rationale**: Developers need to understand the testing system.

#### Scenario: Document baseline updates

- **WHEN** scanner behavior changes intentionally
- **THEN** documentation SHALL explain how to update baseline
- **AND** SHALL provide step-by-step instructions
- **AND** SHALL explain when updates are necessary

**Rationale**: Clear process prevents confusion and mistakes.

#### Scenario: Document CI behavior

- **WHEN** CI checks fail
- **THEN** documentation SHALL explain what CI validates
- **AND** SHALL provide troubleshooting steps
- **AND** SHALL link to baseline update instructions

**Rationale**: Reduces support burden and developer friction.

## MODIFIED Requirements

None - this is a new capability.

## REMOVED Requirements

None - this is a new capability.
