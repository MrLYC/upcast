# Implementation Tasks

## Task List

- [x] **Update environment variable scanner**

  - Remove `root_path` from metadata in `upcast/scanners/env_vars.py`
  - Keep only `scanner_name` in metadata
  - Verify scanner still works correctly

- [x] **Update signal scanner**

  - Remove `root_path` from metadata in `upcast/scanners/signals.py`
  - Keep only `scanner_name` in metadata
  - Verify scanner still works correctly

- [x] **Update example outputs**

  - Regenerate `example/scan-results/env-vars.yaml`
  - Regenerate `example/scan-results/signals.yaml`
  - Verify metadata sections no longer contain `root_path`

- [x] **Update tests**

  - Update test fixtures that check metadata
  - Update test assertions that verify metadata contents
  - Ensure tests don't depend on `root_path` field

- [x] **Run integration tests**

  - Run full integration test suite
  - Verify all scanner outputs are clean
  - Confirm no `root_path` in any outputs

- [x] **Validate changes**
  - Run `make test` to verify all unit tests pass
  - Run `make test-integration` to verify integration tests pass
  - Run pre-commit checks
