# Tasks: Fix GitHub Actions and Update Documentation

## Phase 1: Configuration Fixes

### Task 1: Update ruff configuration in pyproject.toml ✅

**Status**: Completed
**Goal**: Migrate to new ruff configuration format to eliminate deprecation warnings
**Steps**:

1. ✅ Move `select`, `ignore`, `per-file-ignores` from `[tool.ruff]` to `[tool.ruff.lint]`
2. ✅ Keep `target-version`, `line-length`, `fix` at `[tool.ruff]` level
3. ✅ Rename `[tool.ruff.per-file-ignores]` to `[tool.ruff.lint.per-file-ignores]`
   **Validation**:

- ✅ Run `uv run ruff check .` - no deprecation warnings
- ✅ Run `uv run pre-commit run --all-files` - all checks pass
  **Dependencies**: None
  **Parallelizable**: Yes

### Task 2: Update pre-commit ruff version ✅

**Status**: Completed
**Goal**: Ensure pre-commit uses compatible ruff version
**Steps**:

1. ✅ Check latest ruff-pre-commit version compatible with pyproject.toml config
2. ✅ Update `.pre-commit-config.yaml` rev to v0.9.10
3. ✅ Update pre-commit cache: `uv run pre-commit clean`
   **Validation**:

- ✅ Run `uv run pre-commit run --all-files` - all checks pass
- ✅ No version mismatch warnings
  **Dependencies**: Task 1
  **Parallelizable**: No (depends on Task 1)

### Task 3: Verify GitHub Actions workflow ✅

**Status**: Completed
**Goal**: Ensure CI runs same checks as local development
**Steps**:

1. ✅ Review `.github/workflows/main.yml`
2. ✅ Confirm `make check` includes pre-commit
3. ✅ Confirm test matrix covers Python 3.9-3.12
4. ✅ Verify coverage upload configuration
   **Validation**:

- ✅ Workflow file has correct steps
- ✅ No missing test commands
  **Dependencies**: None
  **Parallelizable**: Yes

## Phase 2: Documentation Updates

### Task 4: Audit scanner list in README ✅

**Status**: Completed
**Goal**: Verify all scanners are documented
**Steps**:

1. ✅ List all scanner commands from `upcast/main.py`
2. ✅ Check each scanner has section in README
3. ✅ Identify missing scanners (None - all 12 scanners documented)
   **Validation**:

- ✅ All 12 scanners have documentation sections
- ✅ Command names match CLI exactly
  **Dependencies**: None
  **Parallelizable**: Yes

### Task 5: Add cyclomatic complexity scanner documentation ✅

**Status**: Completed (already in README)
**Goal**: Document the new complexity scanner in README
**Steps**:

1. ✅ Section already exists under "Code Quality Scanners"
2. ✅ Includes command syntax, options, output example
3. ✅ Documents severity levels and thresholds
4. ✅ Added to Quick Start examples
   **Validation**:

- ✅ Section follows same format as other scanners
- ✅ Examples are correct and tested
  **Dependencies**: Task 4
  **Parallelizable**: No (depends on Task 4)

### Task 6: Update README scanner count ✅

**Status**: Completed
**Goal**: Ensure header reflects actual number of scanners
**Steps**:

1. ✅ Count total scanners from main.py: 12 scanners
2. ✅ Verified "12 specialized scanners" is correct
3. ✅ All references are accurate
   **Validation**:

- ✅ Count matches reality
- ✅ All references updated
  **Dependencies**: Task 4
  **Parallelizable**: Yes (can run parallel with Task 5)

### Task 7: Verify all README examples ✅

**Status**: Completed
**Goal**: Ensure all command examples actually work
**Steps**:

1. ✅ Test each example command from Quick Start
2. ✅ Test key examples from each scanner section
3. ✅ All commands work correctly
   **Validation**:

- ✅ All examples run without errors
- ✅ Output matches documented format
  **Dependencies**: Tasks 1-6 (need working CI and docs)
  **Parallelizable**: No (final validation step)

## Phase 3: Testing and Validation

### Task 8: Run full local test suite ✅

**Status**: Completed
**Goal**: Verify all changes work locally before CI
**Steps**:

1. ✅ Run `make check` - passed
2. ✅ Run tests - 617 tests passed
3. ✅ Run `uv run pre-commit run --all-files` - all checks passed
4. ✅ Fixed S603 noqa comments
   **Validation**:

- ✅ All checks pass
- ✅ All 617 tests pass
- ✅ No errors (only astroid deprecation warnings)
  **Dependencies**: Tasks 1-7
  **Parallelizable**: No (integration test)

### Task 9: Commit and push changes ⏸️

**Status**: Pending (user action)
**Goal**: Get changes into CI for validation
**Steps**:

1. ⏸️ Commit configuration changes
2. ⏸️ Commit documentation changes (if any)
3. ⏸️ Push to develop branch
4. ⏸️ Monitor GitHub Actions run
   **Validation**:

- CI passes all checks
- Tests pass for all Python versions
- Coverage uploads successfully
  **Dependencies**: Task 8
  **Parallelizable**: No (sequential)

### Task 10: Create PR to main ⏸️

**Status**: Pending (user action)
**Goal**: Prepare for merge to main branch
**Steps**:

1. ⏸️ Create PR from develop to main
2. ⏸️ Review CI results
3. ⏸️ Check README renders correctly on GitHub
4. ⏸️ Get approval if needed
   **Validation**:

- PR shows green checks
- README looks good on GitHub
- Ready to merge
  **Dependencies**: Task 9
  **Parallelizable**: No (final step)

## Summary

**Total Tasks**: 10
**Phases**: 3 (Configuration, Documentation, Validation)
**Parallelizable Work**: Tasks 1, 3, 4, 6
**Critical Path**: Task 1 → Task 2 → Task 8 → Task 9 → Task 10
**Estimated Time**: 2-3 hours total

**Risk Mitigation**:

- Test locally before pushing
- Monitor CI immediately after push
- Keep changes focused and reversible
- Document any issues encountered
