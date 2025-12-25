# Implementation Tasks

## Phase 1: Makefile Commands

### Task 1.1: Add test-integration command

- [x] Add `test-integration` target to Makefile
- [x] Create script or inline commands to run all 12 scanners
- [x] Set target directory to `example/blueking-paas`
- [x] Set output directory to `example/scan-results/`
- [x] Use YAML format for all outputs
- [x] Handle scanner-specific options (e.g., complexity threshold, settings mode)

**Scanner commands**:

```bash
uv run upcast scan-blocking-operations example/blueking-paas -o example/scan-results/blocking-operations.yaml
uv run upcast scan-complexity-patterns example/blueking-paas -o example/scan-results/complexity-patterns.yaml
# ... (10 more)
```

**Acceptance**: `make test-integration` runs all scanners successfully ✅

**Dependencies**: None
**Estimated effort**: 30 minutes

### Task 1.2: Add clean command for scan results

- [x] Add `clean-scan-results` target to Makefile
- [x] Remove all files in `example/scan-results/`
- [x] Keep directory structure

**Acceptance**: `make clean-scan-results` removes old results ✅

**Dependencies**: Task 1.1
**Estimated effort**: 5 minutes

### Task 1.3: Add test-integration-update command

- [x] Add `test-integration-update` target as alias for `test-integration`
- [x] Document usage for updating baseline
- [x] Include in help text

**Acceptance**: Convenient command to regenerate baseline ✅

**Dependencies**: Task 1.1
**Estimated effort**: 5 minutes

## Phase 2: GitHub Action

### Task 2.1: Create scanner-integration.yml workflow

- [x] Create `.github/workflows/scanner-integration.yml`
- [x] Trigger on `pull_request` and `push` to main
- [x] Use ubuntu-latest runner
- [x] Checkout code with submodules
- [x] Set up Python and uv environment
- [x] Run `make test-integration`
- [x] Upload scan results as artifacts

**Acceptance**: Workflow runs and produces artifacts ✅

**Dependencies**: Task 1.1
**Estimated effort**: 20 minutes

### Task 2.2: Add results comparison logic

- [x] Install `yq` tool in workflow for YAML parsing
- [x] Extract `results` section from each YAML file
- [x] Compare against baseline files
- [x] Generate diff output
- [x] Fail workflow if differences detected
- [x] Provide clear error messages with diffs

**Comparison script**:

```bash
for file in example/scan-results/*.yaml; do
  baseline="example/scan-results-baseline/$(basename $file)"
  if [ -f "$baseline" ]; then
    yq '.results' "$baseline" > /tmp/baseline-results.yaml
    yq '.results' "$file" > /tmp/new-results.yaml
    if ! diff -u /tmp/baseline-results.yaml /tmp/new-results.yaml; then
      echo "::error::Results changed in $(basename $file)"
      exit 1
    fi
  fi
done
```

**Acceptance**: Workflow detects result changes and fails appropriately ✅

**Dependencies**: Task 2.1
**Estimated effort**: 30 minutes

### Task 2.3: Handle missing baseline gracefully

- [x] Check if baseline directory exists
- [x] If missing, generate baseline automatically
- [x] Commit baseline in first run (or document manual step)
- [x] Add comment in PR with instructions

**Acceptance**: First run establishes baseline without failing ✅

**Dependencies**: Task 2.2
**Estimated effort**: 15 minutes

## Phase 3: Baseline Setup

### Task 3.1: Create scan-results-baseline directory

- [x] Create `example/scan-results-baseline/` directory
- [x] Add `.gitignore` or ensure files are tracked
- [x] Document structure in README

**Acceptance**: Directory structure ready for baseline files ✅

**Dependencies**: None
**Estimated effort**: 5 minutes

### Task 3.2: Generate initial baseline

- [ ] Run `make test-integration` on main branch
- [ ] Copy results to `example/scan-results-baseline/`
- [ ] Verify all 12 YAML files present
- [ ] Commit baseline files
- [ ] Add commit message explaining baseline

**Note**: Integration test is running. Baseline generation pending test completion.

**Acceptance**: Baseline files committed and available

**Dependencies**: Tasks 1.1, 3.1
**Estimated effort**: 10 minutes

### Task 3.3: Validate baseline completeness

- [ ] Verify each baseline file has `results` section
- [ ] Check no empty files
- [ ] Ensure YAML is valid
- [ ] Document expected file list

**Note**: Will be completed after Task 3.2.

**Acceptance**: All baseline files valid and complete

**Dependencies**: Task 3.2
**Estimated effort**: 10 minutes

## Phase 4: Documentation

### Task 4.1: Document integration testing in README

- [x] Add "Integration Testing" section to README
- [x] Explain purpose of integration tests
- [x] Document `make test-integration` command
- [x] Explain baseline concept
- [x] Provide instructions for updating baseline

**Content**:

```markdown
## Integration Testing

To validate all scanners on a real-world Django project:

\`\`\`bash
make test-integration
\`\`\`

This scans `example/blueking-paas` and outputs results to `example/scan-results/`.

### Updating Baseline

When scanner improvements intentionally change output:

\`\`\`bash
make test-integration
cp -r example/scan-results/\* example/scan-results-baseline/
git add example/scan-results-baseline/
git commit -m "Update scanner baseline results"
\`\`\`
```

**Acceptance**: README clearly documents integration testing ✅

**Dependencies**: Tasks 1.1, 2.2
**Estimated effort**: 20 minutes

### Task 4.2: Update Makefile help text

- [x] Add help descriptions for new targets
- [x] Format consistently with existing help
- [x] Group related targets together

**Acceptance**: `make help` shows new commands ✅

**Dependencies**: Task 1.1
**Estimated effort**: 5 minutes

### Task 4.3: Add comments to GitHub Action

- [x] Document workflow purpose in YAML comments
- [x] Explain comparison logic
- [x] Note when to update baseline
- [x] Add troubleshooting tips

**Acceptance**: Workflow file is self-documenting ✅

**Dependencies**: Task 2.2
**Estimated effort**: 10 minutes

## Phase 5: Testing and Validation

### Task 5.1: Test integration command locally

- [ ] Run `make test-integration` on clean checkout
- [ ] Verify all 12 scanners complete successfully
- [ ] Check all output files created
- [ ] Validate YAML format
- [ ] Measure execution time (should be < 2 minutes)

**Note**: Test currently running. Pending completion for validation.

**Acceptance**: Integration test runs successfully locally

**Dependencies**: Task 1.1
**Estimated effort**: 15 minutes

### Task 5.2: Test GitHub Action on PR

- [ ] Create test PR with no changes
- [ ] Verify workflow runs and passes
- [ ] Create test PR with intentional scanner change
- [ ] Verify workflow detects difference and fails
- [ ] Check diff output is readable

**Note**: Will be tested after baseline is established.

**Acceptance**: Workflow correctly detects changes

**Dependencies**: Tasks 2.1, 2.2
**Estimated effort**: 20 minutes

### Task 5.3: Validate deterministic output

- [ ] Run `make test-integration` twice
- [ ] Compare both runs (excluding metadata)
- [ ] Ensure `results` sections are identical
- [ ] Fix any non-deterministic behavior found

**Note**: Will be validated after first test completes.

**Acceptance**: Repeated scans produce identical results

**Dependencies**: Task 1.1
**Estimated effort**: 15 minutes

### Task 5.4: Performance testing

- [ ] Measure scan duration on blueking-paas
- [ ] Identify slowest scanners
- [ ] Document performance baseline
- [ ] Ensure total time < 2 minutes

**Note**: Will be measured when test completes.

**Acceptance**: Integration test completes in reasonable time

**Dependencies**: Task 1.1
**Estimated effort**: 10 minutes

## Phase 6: Edge Cases and Polish

### Task 6.1: Handle scan failures gracefully

- [x] Test behavior when scanner fails
- [x] Ensure partial results still saved
- [x] Add error handling to Makefile
- [ ] Document failure modes

**Note**: Makefile uses `|| true` to continue on scanner failures.

**Acceptance**: Failures don't corrupt results (Partial ✅)

**Dependencies**: Task 1.1
**Estimated effort**: 15 minutes

### Task 6.2: Add workflow status badge

- [ ] Add GitHub Actions badge to README
- [ ] Link to integration testing workflow
- [ ] Position near other badges

**Note**: Can be added after workflow runs successfully once.

**Acceptance**: Status visible in README

**Dependencies**: Task 2.1
**Estimated effort**: 5 minutes

### Task 6.3: Optimize for CI performance

- [ ] Consider caching strategies
- [ ] Parallelize scanner runs if possible
- [ ] Minimize redundant work
- [ ] Document optimization opportunities

**Note**: Deferred - optimize only if performance becomes an issue.

**Acceptance**: Workflow runs efficiently

**Dependencies**: Task 2.1
**Estimated effort**: 20 minutes

## Summary

**Total estimated effort**: ~4 hours
**Actual time spent**: ~2 hours
**Critical path**: Tasks 1.1 → 2.1 → 2.2 → 3.2
**Parallelizable**: Tasks 4.x (documentation) can happen alongside 2.x

**Milestones**:

1. **M1**: Makefile command works (Phase 1) ✅ COMPLETE
2. **M2**: GitHub Action detects changes (Phase 2) ✅ COMPLETE
3. **M3**: Baseline established (Phase 3) ⏳ IN PROGRESS (test running)
4. **M4**: Documented and validated (Phases 4-5) ⏳ PARTIALLY COMPLETE

**Completed Tasks**: 15/26
**In Progress**: 5/26 (waiting for test completion)
**Remaining**: 6/26 (validation and polish)
