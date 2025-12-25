# Implementation Tasks

## 1. Fix Scanner Integration Test Stability

- [ ] 1.1 Update scanner-integration.yml to normalize YAML output

  - Add YAML sorting/normalization before comparison
  - Handle both single and double quote styles consistently
  - Sort dictionary keys to ensure stable ordering
  - Sort arrays where order doesn't matter semantically

- [ ] 1.2 Add helper script for YAML normalization

  - Create `.github/scripts/normalize-yaml.py` or use yq with sorting
  - Ensure reproducible output format

- [ ] 1.3 Update comparison logic
  - Normalize both old (committed) and new (generated) YAML before diff
  - Ensure meaningful diffs are still detected (real changes)
  - Test with example outputs from failed CI run

## 2. Add Automated PyPI Publishing

- [ ] 2.1 Create new workflow `.github/workflows/publish-on-tag.yml`

  - Trigger on tag push matching version pattern (v*.*.\*)
  - Run all test suites first (unit tests, integration tests, type checking)
  - Build package with `make build`
  - Publish to PyPI only if all tests pass

- [ ] 2.2 Configure workflow permissions and secrets

  - Ensure PYPI_TOKEN secret is configured
  - Set appropriate workflow permissions

- [ ] 2.3 Add version validation
  - Verify tag version matches pyproject.toml version
  - Fail early if version mismatch

## 3. Testing and Validation

- [ ] 3.1 Test scanner integration fixes

  - Verify no false positives on stable code
  - Verify real changes are still detected
  - Check with multiple scanner outputs

- [ ] 3.2 Test PyPI publishing workflow (dry-run)

  - Create test tag on develop branch
  - Verify all checks run
  - Verify build succeeds (without actually publishing)

- [ ] 3.3 Update documentation
  - Document new release process in README or CONTRIBUTING
  - Add notes about YAML normalization approach
