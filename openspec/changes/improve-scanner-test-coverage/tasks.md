# Tasks: Improve Scanner Test Coverage and Remove Compatibility Aliases

## Phase 1: Add Tests for Simple Scanners (Parallel)

### Task 1.1: Add tests for EnvVarScanner

- [ ] Create `tests/test_scanners/test_env_vars.py`
- [ ] Add model validation tests (EnvVarInfo, EnvVarOutput)
- [ ] Add scanner integration tests with fixtures
- [ ] Test edge cases (no env vars, malformed code)
- [ ] Verify coverage reaches 80%+

### Task 1.2: Add tests for ComplexityScanner

- [ ] Create `tests/test_scanners/test_complexity.py`
- [ ] Add model validation tests (ComplexityResult, ComplexityOutput)
- [ ] Add scanner integration tests
- [ ] Test threshold filtering
- [ ] Verify coverage reaches 80%+

### Task 1.3: Add tests for BlockingOperationsScanner

- [ ] Create `tests/test_scanners/test_blocking_operations.py`
- [ ] Add model validation tests
- [ ] Add scanner integration tests
- [ ] Test different blocking operation types
- [ ] Verify coverage reaches 80%+

### Task 1.4: Add tests for HttpRequestsScanner

- [ ] Create `tests/test_scanners/test_http_requests.py`
- [ ] Add model validation tests
- [ ] Add scanner integration tests
- [ ] Test various HTTP libraries (requests, httpx, aiohttp)
- [ ] Verify coverage reaches 80%+

### Task 1.5: Add tests for MetricsScanner

- [ ] Create `tests/test_scanners/test_metrics.py`
- [ ] Add model validation tests
- [ ] Add scanner integration tests
- [ ] Test different metric types (Counter, Gauge, Histogram, Summary)
- [ ] Verify coverage reaches 80%+

### Task 1.6: Add tests for ConcurrencyScanner

- [ ] Create `tests/test_scanners/test_concurrency.py`
- [ ] Add model validation tests
- [ ] Add scanner integration tests
- [ ] Test different concurrency patterns
- [ ] Verify coverage reaches 80%+

## Phase 2: Add Tests for Complex Scanners (Parallel)

### Task 2.1: Add tests for ExceptionHandlerScanner

- [ ] Create `tests/test_scanners/test_exceptions.py`
- [ ] Add model validation tests
- [ ] Add scanner integration tests
- [ ] Test try/except/else/finally patterns
- [ ] Verify coverage reaches 80%+

### Task 2.2: Add tests for UnitTestScanner

- [ ] Create `tests/test_scanners/test_unit_tests.py`
- [ ] Add model validation tests
- [ ] Add scanner integration tests
- [ ] Test pytest and unittest patterns
- [ ] Test target resolution with root_modules
- [ ] Verify coverage reaches 80%+

### Task 2.3: Add tests for DjangoUrlScanner

- [ ] Create `tests/test_scanners/test_django_urls.py`
- [ ] Add model validation tests
- [ ] Add scanner integration tests
- [ ] Test path(), re_path(), include() patterns
- [ ] Test router expansion
- [ ] Verify coverage reaches 80%+

### Task 2.4: Add tests for DjangoModelScanner

- [ ] Create `tests/test_scanners/test_django_models.py`
- [ ] Add model validation tests
- [ ] Add scanner integration tests
- [ ] Test abstract model inheritance
- [ ] Test field and relationship detection
- [ ] Verify coverage reaches 80%+

### Task 2.5: Add tests for DjangoSettingsScanner

- [ ] Create `tests/test_scanners/test_django_settings.py`
- [ ] Add model validation tests
- [ ] Add scanner integration tests for both modes (usage + definitions)
- [ ] Test settings pattern detection
- [ ] Verify coverage reaches 80%+

## Phase 3: Remove Field Aliases (Sequential)

### Task 3.1: Verify no external usage of aliases

- [ ] Grep search for all alias field names in tests
- [ ] Grep search for all alias field names in documentation
- [ ] Document any found usages

### Task 3.2: Remove aliases from models

- [ ] Remove `alias="operations"` from `blocking_operations.py`
- [ ] Remove `alias="modules"` from `complexity.py`
- [ ] Remove `alias="concurrency_patterns"` from `concurrency.py`
- [ ] Remove `alias="models"` from `django_models.py`
- [ ] Remove `alias="settings"` from `django_settings.py`
- [ ] Remove `alias="definitions"` from `django_settings.py`
- [ ] Remove `alias="url_modules"` from `django_urls.py`
- [ ] Remove `alias="env_vars"` from `env_vars.py`
- [ ] Remove `alias="exception_handlers"` from `exceptions.py`
- [ ] Remove `alias="requests"` from `http_requests.py`
- [ ] Remove `alias="metrics"` from `metrics.py`
- [ ] Remove `alias="tests"` from `unit_tests.py`

### Task 3.3: Update scanner implementations

- [ ] Verify all scanners use `results` field (should already be correct)
- [ ] Check for any lingering references to old names
- [ ] Run ruff to catch any issues

### Task 3.4: Update tests to use `results`

- [ ] Verify `test_file_filtering.py` uses `results` (already done)
- [ ] Check any other tests for alias usage
- [ ] Update if needed

## Phase 4: Validation (Sequential)

### Task 4.1: Run complete test suite

- [ ] Run `uv run pytest tests/ -v`
- [ ] Verify all tests pass
- [ ] Fix any failures

### Task 4.2: Verify coverage target

- [ ] Run coverage report: `uv run pytest tests/test_scanners/ --cov=upcast/scanners --cov-report=term`
- [ ] Verify overall coverage >= 80%
- [ ] Document final coverage numbers

### Task 4.3: Run quality checks

- [ ] Run `uv run ruff check`
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
