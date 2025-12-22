# Proposal: Improve Scanner Test Coverage and Remove Compatibility Aliases

## Metadata

- **Change ID**: `improve-scanner-test-coverage`
- **Status**: PROPOSED
- **Created**: 2025-12-22
- **Author**: Assistant
- **Related Issues**: N/A

## Why

### Current State

After the successful migration of 11 scanners to unified architecture (`refactor-scanners-to-use-models`), we have:

1. **Low test coverage**: Only 16% overall coverage for `upcast/scanners/`

   - Only `signals.py` has good coverage (62%)
   - All other 11 scanners have 10-16% coverage
   - Most scanner logic is untested

2. **Temporary compatibility code**: All Pydantic models have field aliases for backward compatibility

   - Example: `results: dict[str, DjangoModel] = Field(..., alias="models")`
   - 12 models have such aliases across the codebase
   - These aliases were added during migration but are no longer needed

3. **Quality risk**: Without adequate tests, future changes may break scanners

### Problems

1. **Insufficient test coverage** makes refactoring and maintenance risky
2. **Compatibility aliases** add unnecessary complexity:
   - Users must know to use `results` field even though alias exists
   - Code can use either `results` or the alias, causing confusion
   - Models are less clean and harder to understand
3. **No clear test patterns** for new scanner implementations
4. **Technical debt** from migration phase lingers

## What Changes

### 1. Add Comprehensive Tests for All Scanners

Create complete test suites for all 11 scanners in `tests/test_scanners/`:

**Test Structure** (following `test_signal.py` pattern):

```
tests/test_scanners/
├── test_blocking_operations.py  # NEW
├── test_complexity.py           # NEW
├── test_concurrency.py          # NEW
├── test_django_models.py        # NEW
├── test_django_settings.py      # NEW
├── test_django_urls.py          # NEW
├── test_env_vars.py             # NEW
├── test_exceptions.py           # NEW
├── test_http_requests.py        # NEW
├── test_metrics.py              # NEW
├── test_signal.py               # EXISTS (reference)
└── test_unit_tests.py           # NEW
```

**Each test file covers**:

1. **Model tests**: Pydantic model validation, field requirements, constraints
2. **Scanner integration tests**: End-to-end scanning functionality
3. **Edge cases**: Empty inputs, malformed code, error handling
4. **Output format**: Verify structure matches Pydantic models

### 2. Remove All Field Aliases

Clean up 12 Pydantic models by removing `alias` parameters:

**Models to update**:

- `upcast/models/blocking_operations.py` - Remove `alias="operations"`
- `upcast/models/complexity.py` - Remove `alias="modules"`
- `upcast/models/concurrency.py` - Remove `alias="concurrency_patterns"`
- `upcast/models/django_models.py` - Remove `alias="models"`
- `upcast/models/django_settings.py` - Remove `alias="settings"` and `alias="definitions"`
- `upcast/models/django_urls.py` - Remove `alias="url_modules"`
- `upcast/models/env_vars.py` - Remove `alias="env_vars"`
- `upcast/models/exceptions.py` - Remove `alias="exception_handlers"`
- `upcast/models/http_requests.py` - Remove `alias="requests"`
- `upcast/models/metrics.py` - Remove `alias="metrics"`
- `upcast/models/unit_tests.py` - Remove `alias="tests"`

**After cleanup**, all models use consistent field name: `results`

### 3. Update Scanner Code to Use `results`

Update scanners to use `results` field consistently:

- Remove any code using old alias names
- Use `results` everywhere in scanner implementations
- Update any internal references

### 4. Update Tests Using Old Aliases

Update existing tests that rely on aliases:

- `tests/test_file_filtering.py` already updated to use `results`
- Scan for any other references to old field names

## Benefits

1. **High confidence**: 80%+ test coverage ensures scanners work correctly
2. **Clean API**: Single, consistent field name (`results`) across all models
3. **Better maintainability**: Well-tested code is easier to refactor
4. **Documentation by example**: Tests serve as usage examples
5. **Prevent regressions**: Catch bugs before they reach users
6. **Cleaner models**: Remove temporary migration artifacts

## Success Criteria

1. ✅ Test coverage for `upcast/scanners/` reaches 80% or higher
2. ✅ All 11 scanners have comprehensive test suites
3. ✅ Zero field aliases remain in Pydantic models
4. ✅ All scanners use `results` field consistently
5. ✅ All tests pass (existing + new)
6. ✅ Ruff and pre-commit checks pass
7. ✅ Code quality improves (no new technical debt)

## Out of Scope

- Adding new scanner features
- Changing scanner behavior or algorithms
- Modifying CLI commands or output formats
- Performance optimization
- Documentation updates (beyond code comments)

## Risks and Mitigations

### Risk 1: Test writing takes significant time

**Mitigation**:

- Use `test_signal.py` as template for all tests
- Tests can be written in parallel for different scanners
- Focus on critical paths first, then edge cases

### Risk 2: Removing aliases may break something

**Mitigation**:

- Comprehensive grep search for all alias usage before removal
- Tests will catch any breakage immediately
- Scanners already use `results` internally (verified in migration)

### Risk 3: Test coverage target may be hard to reach

**Mitigation**:

- 80% is achievable - signal scanner reached 62% with basic tests
- Focus on main code paths, not edge cases initially
- Can adjust target if needed, but 80% is reasonable
