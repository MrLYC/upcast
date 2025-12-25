# Improve GitHub Actions CI/CD

## Why

The current GitHub Actions workflows on the develop branch have two critical issues:

1. Scanner integration tests fail due to unstable output ordering in YAML results, causing false positives when comparing against baseline
2. There's no automated PyPI publishing workflow for tagged releases

These issues prevent reliable CI/CD and require manual intervention for releases.

## What Changes

- Normalize YAML output ordering in scanner results before comparison to ensure stable diffs
- Handle quote style inconsistencies (single vs double quotes) in YAML comparisons
- Add automated PyPI publishing workflow triggered by version tags
- Ensure PyPI publishing only occurs after all tests pass successfully

## Impact

- Affected specs: `ci-cd` (new capability)
- Affected files:
  - `.github/workflows/scanner-integration.yml` - Enhanced comparison logic
  - `.github/workflows/publish-on-tag.yml` - New workflow for automated releases
  - Integration test workflow becomes more reliable
  - Release process becomes fully automated
