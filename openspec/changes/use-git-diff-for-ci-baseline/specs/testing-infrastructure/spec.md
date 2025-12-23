# testing-infrastructure Specification Changes

## REMOVED Requirements

### Requirement: Result Baseline Management

~~The system SHALL maintain baseline scan results for regression detection.~~

**Rationale**: Replaced with Git-based comparison. Baseline directory is no longer needed.

#### Scenario: Store baseline results

~~- **WHEN** integration tests complete~~
~~- **THEN** the system SHALL store results in `example/scan-results-baseline/`~~
~~- **AND** SHALL version control baseline files~~
~~- **AND** SHALL maintain one YAML file per scanner (12 total)~~

**Rationale**: Results are now compared against Git-committed versions.

#### Scenario: Update baseline

~~- **WHEN** scanner behavior intentionally changes~~
~~- **THEN** developer SHALL run `make test-integration`~~
~~- **AND** SHALL copy new results to baseline directory~~
~~- **AND** SHALL commit updated baseline files~~
~~- **AND** SHALL document changes in commit message~~

**Rationale**: Updating baseline now means simply committing the new results.

#### Scenario: Validate baseline completeness

~~- **WHEN** baseline is established~~
~~- **THEN** all 12 scanner outputs SHALL be present~~
~~- **AND** each file SHALL contain valid YAML~~
~~- **AND** each file SHALL have a `results` section~~
~~- **AND** no file SHALL be empty~~

**Rationale**: Git history ensures completeness; no separate validation needed.

---

## MODIFIED Requirements

### Requirement: CI Integration Test Workflow

The system SHALL provide a GitHub Action to validate scan result consistency **using Git-based comparison**.

#### Scenario: Compare results against baseline

- **WHEN** integration tests complete in CI
- **THEN** the workflow SHALL use `git show HEAD:<file>` to retrieve committed results
- **AND** SHALL extract `results` section from both committed and current files
- **AND** SHALL compare using diff
- **AND** SHALL ignore metadata fields (scan_duration_ms, timestamps)
- **AND** SHALL fail if results differ
- **AND** SHALL display unified diff output

**Rationale**: Git provides built-in version tracking, eliminating need for separate baseline directory.

#### Scenario: Handle new scanner files

- **WHEN** a scanner result file is not in Git history
- **THEN** the workflow SHALL detect this using `git ls-files --error-unmatch`
- **AND** SHALL print informative message about new file
- **AND** SHALL NOT fail the workflow
- **AND** SHALL suggest committing the file to establish baseline

**Rationale**: New scanners should not break CI.

#### Scenario: Provide actionable failure output

- **WHEN** results comparison fails
- **THEN** the workflow SHALL show which scanner outputs changed
- **AND** SHALL display unified diff for each change
- **AND** SHALL provide instructions: "run make test-integration and commit results"
- **AND** SHALL include link to scan result artifacts

**Rationale**: Simplified workflow - no baseline directory to manage.

---

## ADDED Requirements

### Requirement: Git-Based Result Comparison

The system SHALL use Git history as the source of truth for scan result baselines.

#### Scenario: Compare against committed results

- **WHEN** CI validates scan results
- **THEN** the system SHALL retrieve committed version using `git show HEAD:<file>`
- **AND** SHALL extract `results` section from committed YAML
- **AND** SHALL compare against current results
- **AND** SHALL detect any differences in scanner output

**Rationale**: Git provides built-in versioning without additional infrastructure.

#### Scenario: Accept result changes

- **WHEN** scan results change intentionally (scanner improvements)
- **THEN** developer SHALL run `make test-integration`
- **AND** SHALL review the changes
- **AND** SHALL commit updated results: `git add example/scan-results/ && git commit -m 'Update scan results'`
- **AND** SHALL NOT need to copy files to separate directory

**Rationale**: Simplified workflow aligns with standard Git practices.

#### Scenario: Investigate unexpected changes

- **WHEN** scan results change unexpectedly (possible bugs)
- **THEN** developer SHALL review the diff in CI output
- **AND** SHALL use `git diff example/scan-results/` locally to see changes
- **AND** SHALL identify which code change caused the difference
- **AND** SHALL either fix the bug or accept the change

**Rationale**: Standard Git tooling for change tracking.

#### Scenario: Extract results for comparison

- **WHEN** comparing scan results
- **THEN** the system SHALL use `yq '.results'` to extract results section
- **AND** SHALL compare only the extracted results
- **AND** SHALL exclude summary metadata
- **AND** SHALL ensure deterministic comparison

**Rationale**: Metadata varies between runs, only results matter for regression detection.

---

## MODIFIED Requirements

### Requirement: Documentation

The system SHALL document integration testing **with Git-based comparison**.

#### Scenario: Document testing workflow

- **WHEN** developer needs to run integration tests
- **THEN** README SHALL explain `make test-integration` command
- **AND** SHALL describe Git-based comparison approach
- **AND** SHALL provide examples of typical output

**Rationale**: Documentation must reflect current implementation.

#### Scenario: Document result updates

- **WHEN** scanner behavior changes intentionally
- **THEN** documentation SHALL explain to simply commit new results
- **AND** SHALL provide step-by-step instructions
- **AND** SHALL explain when updates are necessary

**Rationale**: Simplified process, clearer instructions.

#### Scenario: Document CI behavior

- **WHEN** CI checks fail
- **THEN** documentation SHALL explain Git-based comparison
- **AND** SHALL provide troubleshooting steps
- **AND** SHALL link to result update instructions

**Rationale**: Developers need to understand the new approach.
