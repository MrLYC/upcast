# Tasks: Improve Scanner Output Quality

## Phase 1: Parser Modifications

### Task 1: Skip unknown coroutines in concurrency scanner

**Goal**: Filter out asyncio.create_task() detections when coroutine cannot be determined
**Steps**:

1. Modify `parse_asyncio_create_task()` in `pattern_parser.py` to return `None` when coroutine is "unknown"
2. Update `PatternChecker.visit_call()` in `checker.py` to skip `None` results
3. Add test case for unknown coroutine (should not appear in output)

**Validation**:

- Run existing tests - should pass with fewer results
- Test with code that has `asyncio.create_task(some_func())` where `some_func` cannot be resolved
- Verify no "unknown" coroutines in output

**Dependencies**: None
**Parallelizable**: Yes
**Estimated Time**: 30 minutes

---

### Task 2: Extract full statement context for django-settings

**Goal**: Show complete statement instead of just `settings.XXX` fragment
**Steps**:

1. Create helper function `_get_containing_statement()` in `settings_parser.py`
2. Walk up AST from node to find parent Assign/Expr/Return/If statement
3. Update `_extract_source_code_snippet()` to use statement-level extraction
4. Handle edge cases (module-level, nested expressions)

**Validation**:

- Test with `if settings.DEBUG: ...` → should show full if statement
- Test with `x = settings.SECRET_KEY` → should show full assignment
- Compare old vs new output - verify improvement

**Dependencies**: None
**Parallelizable**: Yes
**Estimated Time**: 1 hour

---

### Task 3: Split location field in exception handler scanner

**Goal**: Provide structured location data for easier parsing
**Steps**:

1. Update `ExceptionHandler` dataclass in `handler_parser.py`:
   - Add `file`, `lineno`, `end_lineno` fields
   - Keep `location` but mark as deprecated in docstring
2. Update `parse_try_block()` to populate all fields
3. Modify `export.py` to include all location fields in output

**Validation**:

- Verify both old and new fields present in YAML output
- Test programmatic access: `handler.file`, `handler.lineno`, `handler.end_lineno`
- Ensure backward compatibility with tools using `location`

**Dependencies**: None
**Parallelizable**: Yes
**Estimated Time**: 45 minutes

---

### Task 4: Merge consecutive ellipsis in HTTP scanner

**Goal**: Simplify URL output by combining redundant placeholders
**Steps**:

1. Add `_normalize_url_placeholders()` helper function in `request_parser.py`
2. Use regex pattern `r'\.\.\.(\s*\+\s*\.\.\.)+` to find consecutive `...`
3. Replace matches with single `...`
4. Call from `_extract_url_from_node()` before returning result
5. Add unit tests for various URL concatenation patterns

**Validation**:

- Test: `"... + ..."` → `"..."`
- Test: `"base + ... + ... + end"` → `"base + ... + end"`
- Test: `"..."` (single) → `"..."` (unchanged)
- Run full test suite to ensure no regressions

**Dependencies**: None
**Parallelizable**: Yes
**Estimated Time**: 45 minutes

---

### Task 5: Standardize signal scanner output format

**Goal**: Make signal-scanner output consistent with other scanners
**Steps**:

1. Design new output schema (flat list of signals with handlers)
2. Refactor `format_signal_output()` in `export.py`
3. Update YAML structure to match other scanner patterns
4. Update JSON export as well for consistency

**Validation**:

- Compare old vs new YAML side-by-side
- Verify all information preserved (no data loss)
- Test with both Django and Celery signals
- Check output readability improvements

**Dependencies**: None
**Parallelizable**: Yes
**Estimated Time**: 1.5 hours

---

## Phase 2: Testing

### Task 6: Update existing tests

**Goal**: Ensure all tests pass with new output formats
**Steps**:

1. Update test fixtures for changed output structures
2. Modify assertions to check new fields (especially Task 3)
3. Remove tests checking for "unknown" coroutines (Task 1)
4. Update signal scanner test expectations (Task 5)

**Validation**:

- All unit tests pass: `pytest tests/`
- All integration tests pass
- No test skips or failures

**Dependencies**: Tasks 1-5
**Parallelizable**: No (requires completed implementations)
**Estimated Time**: 1 hour

---

### Task 7: Add new test cases

**Goal**: Cover new edge cases and validation scenarios
**Steps**:

1. Add test for unknown coroutine filtering (Task 1)
2. Add tests for statement extraction edge cases (Task 2)
3. Add tests for location field backward compatibility (Task 3)
4. Add tests for various URL placeholder patterns (Task 4)
5. Add tests for new signal output structure (Task 5)

**Validation**:

- New tests pass
- Code coverage maintained or improved
- Edge cases properly handled

**Dependencies**: Task 6
**Parallelizable**: No
**Estimated Time**: 1 hour

---

## Phase 3: Documentation

### Task 8: Update README examples

**Goal**: Show users the improved output formats
**Steps**:

1. Update concurrency scanner example (no unknown coroutines)
2. Update django-settings example (show full statement context)
3. Update exception-handler example (show new location fields)
4. Update http-request example (show cleaner URLs)
5. Update signal scanner example (show new structure)

**Validation**:

- Examples match actual output from scanners
- Clear improvement visible in before/after
- Migration notes for breaking changes

**Dependencies**: Tasks 1-5
**Parallelizable**: Yes (can do alongside testing)
**Estimated Time**: 45 minutes

---

### Task 9: Document breaking changes

**Goal**: Help users understand and adapt to changes
**Steps**:

1. Add CHANGELOG entry describing all changes
2. Create migration guide for signal-scanner users
3. Document deprecation of `location` field (exception-handler)
4. Update API documentation if exists

**Validation**:

- CHANGELOG follows semantic versioning guidelines
- Migration guide includes code examples
- Deprecation timeline clearly stated

**Dependencies**: Task 8
**Parallelizable**: No
**Estimated Time**: 30 minutes

---

### Task 10: Update spec files

**Goal**: Sync OpenSpec requirements with implementation
**Steps**:

1. Update concurrency-pattern-scanner spec
2. Update django-settings-scanner spec
3. Update exception-handler-scanner spec
4. Update http-request-scanner spec
5. Update signal-scanner spec (if exists)

**Validation**:

- Run `openspec validate improve-scanner-output-quality --strict`
- All specs have proper scenario blocks
- Requirements match implementation

**Dependencies**: Tasks 1-9
**Parallelizable**: No
**Estimated Time**: 1 hour

---

## Phase 4: Quality Assurance

### Task 11: Manual verification

**Goal**: Verify improvements with real-world code
**Steps**:

1. Run all modified scanners on sample projects
2. Compare old vs new output quality
3. Verify readability improvements
4. Check for any unexpected behavior

**Validation**:

- Output quality visibly improved
- No false positives introduced
- No information lost in transformations

**Dependencies**: Tasks 1-10
**Parallelizable**: No
**Estimated Time**: 1 hour

---

### Task 12: Final validation

**Goal**: Ensure everything works end-to-end
**Steps**:

1. Run full test suite: `make test`
2. Run code quality checks: `make check`
3. Run mypy: `uv run mypy`
4. Test all scanner commands manually
5. Verify OpenSpec validation: `openspec validate --strict`

**Validation**:

- All tests pass (617+ tests)
- All quality checks pass
- No type errors
- OpenSpec validation clean

**Dependencies**: Task 11
**Parallelizable**: No
**Estimated Time**: 30 minutes

---

## Summary

**Total Tasks**: 12
**Phases**: 4 (Parser Modifications, Testing, Documentation, QA)
**Parallelizable Tasks**: Tasks 1-5, 8
**Critical Path**: Tasks 1-5 → 6 → 7 → 9 → 10 → 11 → 12
**Estimated Total Time**: 10-12 hours

**Key Milestones**:

1. All parsers modified (End of Phase 1) - ~4.5 hours
2. All tests passing (End of Phase 2) - ~6.5 hours
3. Documentation complete (End of Phase 3) - ~8.5 hours
4. Ready for merge (End of Phase 4) - ~10.5 hours

**Risk Mitigation**:

- Test incrementally after each parser change
- Keep backward compatibility where possible (Task 3)
- Document breaking changes clearly (Task 9)
- Manual verification catches issues automated tests miss (Task 11)
