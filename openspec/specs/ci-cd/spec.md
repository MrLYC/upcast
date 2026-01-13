# ci-cd Specification

## Purpose

TBD - created by archiving change improve-github-actions. Update Purpose after archive.

## Requirements

### Requirement: Stable Scanner Integration Tests

The scanner integration test workflow SHALL compare scanner outputs reliably regardless of non-semantic differences in YAML formatting.

#### Scenario: YAML key ordering differences

- **WHEN** scanner output has different key ordering but identical semantic content
- **THEN** the comparison does not report a false positive difference

#### Scenario: Quote style variations

- **WHEN** scanner output uses single quotes in one run and double quotes in another
- **THEN** the comparison treats them as semantically equivalent

#### Scenario: Array ordering in metadata

- **WHEN** arrays contain the same elements but in different order (for metadata fields)
- **THEN** the comparison normalizes order before comparison

#### Scenario: Real changes detected

- **WHEN** scanner behavior genuinely changes (e.g., new findings, different analysis)
- **THEN** the comparison correctly identifies and reports the change

### Requirement: Automated PyPI Publishing

The CI/CD system SHALL automatically publish releases to PyPI when version tags are pushed, but only after all quality checks pass.

#### Scenario: Tag triggers publishing workflow

- **WHEN** a version tag matching pattern `v*.*.*` is pushed
- **THEN** the publishing workflow is triggered

#### Scenario: Tests run before publishing

- **WHEN** publishing workflow is triggered
- **THEN** all test suites (unit, integration, type checking) execute first
- **AND** publishing only proceeds if all tests pass

#### Scenario: Version mismatch detection

- **WHEN** tag version does not match pyproject.toml version
- **THEN** the workflow fails with a clear error message
- **AND** no package is published

#### Scenario: Publishing on test failure

- **WHEN** any test suite fails during the publishing workflow
- **THEN** the workflow stops before publishing
- **AND** no package is published to PyPI

#### Scenario: Successful automated release

- **WHEN** tag is pushed with matching version and all tests pass
- **THEN** package is built with `make build`
- **AND** package is published to PyPI using `uv publish`
- **AND** workflow reports success with published version

### Requirement: Develop Branch CI Stability

The develop branch CI workflows SHALL run reliably without false positive failures from scanner integration tests.

#### Scenario: Develop branch push

- **WHEN** code is pushed to develop branch
- **THEN** scanner integration tests run with normalized comparison
- **AND** tests pass when scanner behavior is unchanged

#### Scenario: Scanner improvements

- **WHEN** scanner improvements change output format or findings
- **THEN** integration tests clearly indicate what changed
- **AND** developers can review and commit updated baselines
