# Tasks: Use Git Diff for CI Baseline Comparison

## Phase 1: Update CI Workflow

### Task 1.1: Modify scanner-integration.yml workflow

- [ ] Remove BASELINE_DIR variable
- [ ] Remove baseline directory checks
- [ ] Replace file-based comparison with git diff comparison
- [ ] Update "Compare results against baseline" step to:
  - Extract results section from committed and current files
  - Use `git show HEAD:<file>` to get committed version
  - Compare using diff
  - Handle new files (not in git history)
- [ ] Update error messages and instructions
- [ ] Remove references to copying/committing baseline directory
- [ ] Test locally with act or manual workflow run

**Success Criteria**:

- Workflow detects changes in scan results correctly
- Clear diff output when results change
- Handles new scanner files gracefully
- Instructions are accurate and actionable

### Task 1.2: Test CI workflow changes

- [ ] Create test branch
- [ ] Modify a scan result file intentionally
- [ ] Push and verify CI detects the change
- [ ] Verify diff output is clear
- [ ] Add a new scanner result file
- [ ] Verify CI handles new file correctly
- [ ] Merge when tests pass

**Success Criteria**:

- CI correctly identifies changed results
- CI correctly handles new results
- Diff output is helpful for debugging

## Phase 2: Clean Up Repository

### Task 2.1: Remove baseline directory (if exists)

- [ ] Check if `example/scan-results-baseline/` exists
- [ ] If exists, remove directory: `rm -rf example/scan-results-baseline/`
- [ ] Remove from `.gitignore` if present
- [ ] Commit removal with message: "Remove scan-results-baseline directory"

**Success Criteria**:

- No baseline directory in repository
- Git history preserved (can restore if needed)

### Task 2.2: Verify scan-results directory

- [ ] Ensure `example/scan-results/` exists and is committed
- [ ] Verify all scanner outputs are present
- [ ] Run `make test-integration` to ensure files are up-to-date
- [ ] Commit any updates

**Success Criteria**:

- All scanner results committed and current
- Directory structure clean

## Phase 3: Update Documentation

### Task 3.1: Update README.md

- [ ] Find all mentions of `scan-results-baseline`
- [ ] Update integration test section to remove baseline instructions
- [ ] Add new section explaining CI behavior:
  - CI compares against committed results
  - How to accept changes (just commit)
  - What to do if unexpected changes appear
- [ ] Update troubleshooting section
- [ ] Add examples of expected CI output

**Success Criteria**:

- No mentions of baseline directory
- Clear instructions for updating results
- Examples show actual CI output

### Task 3.2: Update testing-infrastructure spec

- [ ] Remove "Result Baseline Management" requirement
- [ ] Update "CI Integration Test Workflow" requirement
- [ ] Add "Git-Based Comparison" requirement
- [ ] Update scenarios to reflect git diff approach
- [ ] Remove references to baseline directory

**Success Criteria**:

- Spec accurately reflects new implementation
- No contradictions with actual behavior

### Task 3.3: Update archived change documentation

- [ ] Find archived changes mentioning baseline
- [ ] Add notes that design changed
- [ ] Reference this change ID
- [ ] Keep original docs for historical context

**Success Criteria**:

- Historical context preserved
- Clear evolution of design

## Phase 4: Validation

### Task 4.1: Run full integration test suite

- [ ] Run `make test-integration` locally
- [ ] Verify all scanners complete successfully
- [ ] Check all output files are valid YAML
- [ ] Commit any updated results

**Success Criteria**:

- All tests pass
- Results committed and up-to-date

### Task 4.2: Validate OpenSpec change

- [ ] Run `openspec validate use-git-diff-for-ci-baseline --strict`
- [ ] Fix any validation errors
- [ ] Ensure all scenarios have proper format
- [ ] Check cross-references are valid

**Success Criteria**:

- No validation errors
- All requirements have scenarios
- Deltas properly formatted

### Task 4.3: Test CI end-to-end

- [ ] Create PR with this change
- [ ] Verify CI runs successfully
- [ ] Check CI output is clear and helpful
- [ ] Make a trivial change to a scan result
- [ ] Verify CI detects and reports it correctly
- [ ] Accept the change and verify CI passes

**Success Criteria**:

- CI works correctly in real PR
- Changes are detected accurately
- Instructions work as documented

## Dependencies

- No external dependencies
- Requires `yq` to be installed in CI (already present)
- Requires git (already present)

## Rollback Plan

If issues are found:

1. Revert `.github/workflows/scanner-integration.yml`
2. Restore baseline directory from git history:
   ```bash
   git checkout HEAD~1 -- example/scan-results-baseline/
   git add example/scan-results-baseline/
   git commit -m 'Revert: restore baseline directory'
   ```
3. Update documentation to match reverted state

## Estimated Effort

- Task 1: Update CI Workflow - 2 hours
- Task 2: Clean Up Repository - 30 minutes
- Task 3: Update Documentation - 1 hour
- Task 4: Validation - 1 hour

**Total**: ~4.5 hours
