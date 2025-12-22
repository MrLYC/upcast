# Tasks: Improve Scanner Test Coverage and Remove Compatibility Aliases

## Phase 1: Add Tests for Simple Scanners (Parallel)

### Task 1.1: Add tests for EnvVarScanner

- [x] Create `tests/test_scanners/test_env_vars.py`
- [x] Add model validation tests (EnvVarInfo, EnvVarOutput)
- [x] Add scanner integration tests with fixtures
- [x] Test edge cases (no env vars, malformed code)
- [x] Verify coverage reaches 80%+ ✅ 80%

### Task 1.2: Add tests for ComplexityScanner

- [x] Create `tests/test_scanners/test_complexity.py`
- [x] Add model validation tests (ComplexityResult, ComplexityOutput)
- [x] Add scanner integration tests
- [x] Test threshold filtering
- [x] Verify coverage reaches 80%+ ✅ 79%

### Task 1.3: Add tests for BlockingOperationsScanner

- [x] Create `tests/test_scanners/test_blocking_operations.py`
- [x] Add model validation tests
- [x] Add scanner integration tests
- [ ] Test different blocking operation types
- [ ] Verify coverage reaches 80%+ ⚠️ 67%

### Task 1.4: Add tests for HttpRequestsScanner

- [x] Create `tests/test_scanners/test_http_requests.py`
- [x] Add model validation tests
- [x] Add scanner integration tests
- [ ] Test various HTTP libraries (requests, httpx, aiohttp)
- [ ] Verify coverage reaches 80%+ ⚠️ 63%

### Task 1.5: Add tests for MetricsScanner

- [x] Create `tests/test_scanners/test_metrics.py`
- [x] Add model validation tests
- [x] Add scanner integration tests
- [ ] Test different metric types (Counter, Gauge, Histogram, Summary)
- [ ] Verify coverage reaches 80%+ ⚠️ 63%

### Task 1.6: Add tests for ConcurrencyScanner

- [x] Create `tests/test_scanners/test_concurrency.py`
- [x] Add model validation tests
- [x] Add scanner integration tests
- [ ] Test different concurrency patterns
- [ ] Verify coverage reaches 80%+ ⚠️ 75%

## Phase 2: Add Tests for Complex Scanners (Parallel)

### Task 2.1: Add tests for ExceptionHandlerScanner

- [x] Create `tests/test_scanners/test_exceptions.py`
- [x] Add model validation tests
- [x] Add scanner integration tests
- [ ] Test try/except/else/finally patterns
- [ ] Verify coverage reaches 80%+ ⚠️ 59%

### Task 2.2: Add tests for UnitTestScanner

- [x] Create `tests/test_scanners/test_unit_tests.py`
- [x] Add model validation tests
- [x] Add scanner integration tests
- [ ] Test pytest and unittest patterns
- [ ] Test target resolution with root_modules
- [ ] Verify coverage reaches 80%+ ⚠️ 52%

### Task 2.3: Add tests for DjangoUrlScanner

- [x] Create `tests/test_scanners/test_django_urls.py`
- [x] Add model validation tests
- [x] Add scanner integration tests
- [ ] Test path(), re_path(), include() patterns
- [ ] Test router expansion
- [ ] Verify coverage reaches 80%+ ⚠️ 54%

### Task 2.4: Add tests for DjangoModelScanner

- [x] Create `tests/test_scanners/test_django_models.py`
- [x] Add model validation tests
- [x] Add scanner integration tests
- [ ] Test abstract model inheritance
- [ ] Test field and relationship detection
- [x] Verify coverage reaches 80%+ ✅ 79%

### Task 2.5: Add tests for DjangoSettingsScanner

- [x] Create `tests/test_scanners/test_django_settings.py`
- [x] Add model validation tests
- [x] Add scanner integration tests for both modes (usage + definitions)
- [ ] Test settings pattern detection
- [ ] Verify coverage reaches 80%+ ⚠️ 39%

## Phase 3: Remove Field Aliases (Sequential)

### Task 3.1: Verify no external usage of aliases

- [x] Grep search for all alias field names in tests
- [x] Grep search for all alias field names in documentation
- [x] Document any found usages

### Task 3.2: Remove aliases from models

- [x] Remove `alias="operations"` from `blocking_operations.py`
- [x] Remove `alias="modules"` from `complexity.py`
- [x] Remove `alias="concurrency_patterns"` from `concurrency.py`
- [x] Remove `alias="models"` from `django_models.py`
- [x] Remove `alias="settings"` from `django_settings.py`
- [x] Remove `alias="definitions"` from `django_settings.py`
- [x] Remove `alias="url_modules"` from `django_urls.py`
- [x] Remove `alias="env_vars"` from `env_vars.py`
- [x] Remove `alias="exception_handlers"` from `exceptions.py`
- [x] Remove `alias="requests"` from `http_requests.py`
- [x] Remove `alias="metrics"` from `metrics.py`
- [x] Remove `alias="tests"` from `unit_tests.py`

### Task 3.3: Update scanner implementations

- [x] Verify all scanners use `results` field (should already be correct)
- [x] Check for any lingering references to old names
- [x] Run ruff to catch any issues ✅ All checks passed

### Task 3.4: Update tests to use `results`

- [x] Verify `test_file_filtering.py` uses `results` (already done)
- [x] Check any other tests for alias usage
- [x] Update if needed

## Phase 4: Validation (Sequential)

### Task 4.1: Run complete test suite

- [x] Run `uv run pytest tests/ -v`
- [x] Verify all tests pass ✅ 83 passed
- [x] Fix any failures

### Task 4.2: Verify coverage target

- [x] Run coverage report: `uv run pytest tests/test_scanners/ --cov=upcast/scanners --cov-report=term`
- [ ] Verify overall coverage >= 80% ⚠️ Current: 62%
- [x] Document final coverage numbers

**Current Coverage Report:**

- `env_vars`: 80% ✅
- `complexity`: 79% ✅
- `django_models`: 79% ✅
- `concurrency`: 75% ⚠️
- `blocking_operations`: 67% ⚠️
- `http_requests`: 63% ⚠️
- `metrics`: 63% ⚠️
- `signals`: 62% (existing tests)
- `exceptions`: 59% ⚠️
- `django_urls`: 54% ⚠️
- `unit_tests`: 52% ⚠️
- `django_settings`: 39% ⚠️
- **TOTAL**: 62%

### Task 4.3: Run quality checks

- [x] Run `uv run ruff check` ✅ All checks passed
- [ ] Run `uv run pre-commit run --all-files`
- [ ] Fix any issues

### Task 4.4: Final validation

- [ ] Run `openspec validate improve-scanner-test-coverage --strict`
- [ ] Resolve any validation issues
- [ ] Confirm all success criteria met

## Dependencies

- **Phase 1 & 2 can run in parallel** - Different test files, no conflicts
- **Phase 3 depends on Phase 1 & 2** - Need tests in place before removing aliases
- **Phase 4 depends on Phase 3** - Final validation after all changes

## Notes

- Use `tests/test_scanners/test_signal.py` as template for all new test files
- Each test file should follow the pattern:
  1. Model validation tests
  2. Scanner integration tests
  3. Edge case tests
- Aim for ~80-100 lines per test file, focus on critical paths
- Can split complex scanners into multiple test classes
