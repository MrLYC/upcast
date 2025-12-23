# Implementation Tasks

## Phase 1: Fix Output Serialization

### Task 1.1: Configure Pydantic to include None fields

- [ ] Modify `UrlPattern` model class config to set `exclude_none=False` for model_dump
- [ ] OR add Field configuration with `exclude=False` for view_module and view_name
- [ ] Ensure common export utilities respect this configuration
- [ ] Test that None values appear in YAML output

**Acceptance**: Running scanner on any project shows `view_module: null` and `view_name: null` for unresolved views

**Dependencies**: None
**Estimated effort**: 30 minutes

### Task 1.2: Update export utility if needed

- [ ] Check if `common.export` module needs updates to respect model configuration
- [ ] Ensure YAML serialization preserves None values
- [ ] Verify JSON export also includes None fields

**Acceptance**: Both YAML and JSON output include view fields

**Dependencies**: Task 1.1
**Estimated effort**: 15 minutes

## Phase 2: Improve View Resolution

### Task 2.1: Add fallback name extraction

- [ ] Modify `resolve_view()` to always extract view_name even when full path fails
- [ ] For attribute access (`views.index`), extract "index" even if module unknown
- [ ] For Call nodes, extract function name from node structure
- [ ] Add unit tests for fallback extraction

**Acceptance**: View names extracted in >90% of cases, even when module path unknown

**Dependencies**: Task 1.1
**Estimated effort**: 1 hour

### Task 2.2: Improve module path resolution

- [ ] Enhance `_resolve_import_name()` to handle more import patterns
- [ ] Add support for resolving relative imports
- [ ] Try multiple inference strategies before giving up
- [ ] Add logging for resolution failures in verbose mode

**Acceptance**: View module resolution rate increases by 20-30%

**Dependencies**: Task 2.1
**Estimated effort**: 1.5 hours

### Task 2.3: Handle Django-specific patterns

- [ ] Add special handling for common Django CBV patterns
- [ ] Recognize decorator patterns (@login_required, etc.)
- [ ] Handle DRF view classes and viewsets
- [ ] Test with blueking-paas codebase

**Acceptance**: Django-specific view patterns resolve correctly

**Dependencies**: Task 2.2
**Estimated effort**: 1 hour

## Phase 3: Add Resolution Status

### Task 3.1: Add view_resolved field (optional)

- [ ] Add `view_resolved: bool | None` field to UrlPattern model
- [ ] Set to True when resolution succeeds, False when fails, None for non-view patterns
- [ ] Update view_resolver to return resolution status
- [ ] Document field meaning in model docstring

**Acceptance**: Users can filter by resolution status

**Dependencies**: Task 2.3
**Estimated effort**: 30 minutes

## Phase 4: Testing and Validation

### Task 4.1: Add unit tests

- [ ] Test UrlPattern serialization includes None fields
- [ ] Test view resolution fallback mechanisms
- [ ] Test edge cases: lambdas, complex imports, missing modules
- [ ] Ensure all new code paths have test coverage

**Acceptance**: Test coverage > 80% for modified code

**Dependencies**: Tasks 1.1-3.1
**Estimated effort**: 1 hour

### Task 4.2: Run integration test

- [ ] Scan blueking-paas project
- [ ] Verify view_module and view_name fields present in output
- [ ] Measure resolution success rate
- [ ] Update baseline if output format changed

**Acceptance**: Integration test passes with new baseline

**Dependencies**: Task 4.1
**Estimated effort**: 30 minutes

### Task 4.3: Validate on real codebase

- [ ] Manual review of django-urls.yaml output quality
- [ ] Check that resolved views are correct
- [ ] Verify unresolved views are legitimate edge cases
- [ ] Document any remaining limitations

**Acceptance**: Output quality meets expectations

**Dependencies**: Task 4.2
**Estimated effort**: 30 minutes

## Phase 5: Documentation

### Task 5.1: Update README

- [ ] Document view_module and view_name fields
- [ ] Explain what null values mean
- [ ] Add example of resolved vs unresolved views
- [ ] Note any known limitations

**Acceptance**: README clearly explains view resolution

**Dependencies**: Task 4.3
**Estimated effort**: 20 minutes

### Task 5.2: Update spec if needed

- [ ] Verify spec matches implementation
- [ ] Add any missing scenarios
- [ ] Document resolution behavior

**Acceptance**: Spec is accurate and complete

**Dependencies**: Task 5.1
**Estimated effort**: 15 minutes

## Summary

**Total estimated effort**: ~7.5 hours

**Critical path**:

- Task 1.1 → 2.1 → 2.2 → 2.3 → 4.1 → 4.2 → 4.3

**Parallelizable work**:

- Task 3.1 can be done in parallel with Phase 2
- Phase 5 can start once Phase 4 is done

**Milestones**:

1. **M1**: View fields appear in output (Task 1.2) - +45 min
2. **M2**: Resolution improvements complete (Task 2.3) - +3.5 hours
3. **M3**: Testing complete (Task 4.3) - +2 hours
4. **M4**: Documentation updated (Task 5.2) - +35 min
