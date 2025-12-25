# Implementation Tasks

## Phase 1: Concurrency Scanner Fix

### Task 1.1: Strengthen Process creation detection

- [ ] Modify `_detect_process_creation()` to verify qualified name is `multiprocessing.Process`
- [ ] Add import resolution check using `get_import_info()`
- [ ] Skip class instantiations where class is not from multiprocessing module
- [ ] Add test case for `PlainProcess` dataclass (should not detect)
- [ ] Add test case for legitimate `multiprocessing.Process()` (should detect)

**Acceptance**: PlainProcess instantiation not reported; real Process creation still detected

**Dependencies**: None
**Estimated effort**: 1 hour

### Task 1.2: Apply same fix to Thread detection

- [ ] Update `_detect_thread_creation()` with same qualified name verification
- [ ] Verify thread name is from `threading` module
- [ ] Test with custom Thread classes to ensure no false positives

**Acceptance**: Only `threading.Thread` instances detected, not custom Thread classes

**Dependencies**: Task 1.1
**Estimated effort**: 30 minutes

## Phase 2: Django Settings Scanner - Restore Definitions Mode

### Task 2.1: Implement \_scan_definitions method

- [ ] Review existing `parse_settings_module()` in common utilities
- [ ] Implement `_scan_definitions()` to call parser for settings files
- [ ] Map parser output to `DjangoSettingsDefinitionOutput` model
- [ ] Handle multiple settings files (base, dev, prod, etc.)

**Acceptance**: Scanner with `--mode definitions` outputs setting definitions

**Dependencies**: None
**Estimated effort**: 2 hours

### Task 2.2: Test definitions mode

- [ ] Create test settings file with various setting types
- [ ] Verify all setting definitions are extracted
- [ ] Test with blueking-paas settings files
- [ ] Ensure values and types are captured correctly

**Acceptance**: Definitions mode works on real-world settings

**Dependencies**: Task 2.1
**Estimated effort**: 1 hour

### Task 2.3: Validate mode switching

- [ ] Test that `--mode usage` still works correctly
- [ ] Test that `--mode definitions` produces different output
- [ ] Verify CLI parameter handling
- [ ] Update CLI help text if needed

**Acceptance**: Both modes work independently without conflicts

**Dependencies**: Task 2.2
**Estimated effort**: 30 minutes

## Phase 3: Env Vars Scanner - Filter False Positives

### Task 3.1: Add context validation

- [ ] Modify string extraction to check parent node context
- [ ] Verify string is argument to env access function (getenv, environ[], etc.)
- [ ] Skip strings in unrelated Call nodes (API calls, logging, etc.)
- [ ] Add logging for skipped strings (debug level)

**Acceptance**: Only strings in env access contexts are reported

**Dependencies**: None
**Estimated effort**: 1.5 hours

### Task 3.2: Test with API call scenarios

- [ ] Create test file with API call containing env-like strings
- [ ] Verify these strings are not reported as env vars
- [ ] Test with blueking-paas API client files
- [ ] Ensure legitimate env vars still detected

**Acceptance**: No false positives from API calls

**Dependencies**: Task 3.1
**Estimated effort**: 1 hour

## Phase 4: HTTP Requests Scanner - Improve JSON Body Handling

### Task 4.1: Make json_body optional

- [ ] Update `HttpRequestUsage` model to make `json_body` optional
- [ ] Modify JSON extraction to return `None` for uninferrable content
- [ ] Remove `<dynamic>` placeholder logic
- [ ] Update tests to expect `json_body` absence

**Acceptance**: json_body field omitted when cannot be inferred

**Dependencies**: None
**Estimated effort**: 1 hour

### Task 4.2: Improve static JSON inference

- [ ] Enhance literal dict/list detection
- [ ] Handle simple variable references where value is inferrable
- [ ] Keep returning None for complex/computed bodies
- [ ] Test with various JSON body patterns

**Acceptance**: Static JSON bodies captured; dynamic ones omitted

**Dependencies**: Task 4.1
**Estimated effort**: 1.5 hours

## Phase 5: Unit Tests Scanner - Fix Empty Output

### Task 5.1: Debug test file discovery

- [ ] Add debug logging to file discovery logic
- [ ] Verify `test*.py` and `*_test.py` pattern matching
- [ ] Test with blueking-paas test directory structure
- [ ] Check if path filters are excluding test directories

**Acceptance**: Test files are discovered and scanned

**Dependencies**: None
**Estimated effort**: 1 hour

### Task 5.2: Verify test function detection

- [ ] Ensure AST parsing works on test files
- [ ] Verify `test_` prefix detection for functions
- [ ] Verify unittest.TestCase subclass detection
- [ ] Add logging for detected tests

**Acceptance**: Test functions/methods are detected

**Dependencies**: Task 5.1
**Estimated effort**: 1 hour

### Task 5.3: Fix output generation

- [ ] Debug why summary shows 0 tests despite detection
- [ ] Verify test data flows to output model correctly
- [ ] Check for filtering logic that might drop tests
- [ ] Test with simple test file first, then blueking-paas

**Acceptance**: Detected tests appear in output

**Dependencies**: Task 5.2
**Estimated effort**: 1.5 hours

## Phase 6: Integration Testing & Validation

### Task 6.1: Run integration tests

- [ ] Run `make test-integration` with fixes
- [ ] Review all 12 scanner outputs for quality
- [ ] Verify fixes resolved identified issues
- [ ] Check for any new issues introduced

**Acceptance**: Integration tests pass with improved output

**Dependencies**: Tasks 1.1-5.3
**Estimated effort**: 1 hour

### Task 6.2: Update baselines

- [ ] Compare new outputs with previous baseline
- [ ] Document changes in each scanner output
- [ ] Update baseline files in `example/scan-results-baseline/`
- [ ] Commit baseline updates with detailed message

**Acceptance**: Baselines updated and documented

**Dependencies**: Task 6.1
**Estimated effort**: 30 minutes

### Task 6.3: Update documentation

- [ ] Document fixed issues in CHANGELOG or release notes
- [ ] Update scanner README sections if needed
- [ ] Note any behavior changes in scanner specs
- [ ] Add examples of corrected output

**Acceptance**: Changes documented for users

**Dependencies**: Task 6.2
**Estimated effort**: 30 minutes

## Phase 7: Add Regression Prevention

### Task 7.1: Add unit tests for fixes

- [ ] Test concurrency: PlainProcess not detected
- [ ] Test env-vars: API call strings not detected
- [ ] Test http-requests: dynamic json_body omitted
- [ ] Test unit-tests: real test files detected

**Acceptance**: All fixes have explicit test coverage

**Dependencies**: Tasks 1.1-5.3
**Estimated effort**: 2 hours

### Task 7.2: Consider validation framework

- [ ] Evaluate need for output validation rules
- [ ] Could add schema validation for common mistakes
- [ ] Could add confidence scoring system
- [ ] Document approach in design doc if implemented

**Acceptance**: Approach documented or implemented

**Dependencies**: Task 7.1
**Estimated effort**: 1 hour (evaluation only)

## Summary

**Total estimated effort**: ~16 hours
**Critical path**:

- Task 5.1 → 5.2 → 5.3 (unit tests fix - likely most complex)
- Task 2.1 → 2.2 → 2.3 (definitions mode restoration)

**Parallelizable work**:

- Phases 1, 3, 4 can be worked simultaneously (different scanners)
- Phase 7 can be worked in parallel with Phase 6

**Milestones**:

1. **M1**: All 5 scanner fixes implemented (Tasks 1.1-5.3) - ~10 hours
2. **M2**: Integration tests passing with improved quality (Task 6.1) - +1 hour
3. **M3**: Baselines updated and changes documented (Tasks 6.2-6.3) - +1 hour
4. **M4**: Regression tests added (Task 7.1) - +2 hours
