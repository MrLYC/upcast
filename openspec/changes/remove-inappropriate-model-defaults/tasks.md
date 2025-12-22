# Tasks: Remove Inappropriate Model Field Defaults

**Status**: Not Started

## Task Breakdown

### Phase 1: Remove Column Field Defaults ⏳ Not Started

**Objective**: Remove `default=0` from `column` fields and ensure scanners always provide explicit values.

- [ ] 1.1: Remove `default=0` from `SignalUsage.column` in `upcast/models/signals.py`
- [ ] 1.2: Remove `default=0` from `ConcurrencyUsage.column` in `upcast/models/concurrency.py`
- [ ] 1.3: Remove `default=0` from `BlockingOperation.column` in `upcast/models/blocking_operations.py`
- [ ] 1.4: Remove `default=0` from `SettingsLocation.column` in `upcast/models/django_settings.py`
- [ ] 1.5: Remove `default=0` from `EnvVarLocation.column` in `upcast/models/env_vars.py`
- [ ] 1.6: Update `SignalsScanner` to always assign `column=node.col_offset`
- [ ] 1.7: Update `ConcurrencyScanner` to always assign `column=node.col_offset`
- [ ] 1.8: Update `BlockingOperationsScanner` to remove `or 0` fallbacks
- [ ] 1.9: Update `DjangoSettingsScanner` to remove `or 0` fallbacks
- [ ] 1.10: Update `EnvVarScanner` to always assign `column=node.col_offset`
- [ ] 1.11: Run tests to verify all column values are provided

**Acceptance Criteria**:

- All 5 `column` fields have `Field(..., ge=0, ...)` instead of `Field(default=0, ge=0, ...)`
- No scanner code uses `node.col_offset or 0` pattern
- All scanners explicitly assign `column=node.col_offset`
- Tests pass without ValidationErrors

**Dependencies**: None

---

### Phase 2: Remove Boolean Flag Defaults ⏳ Not Started

**Objective**: Remove `default=False` from boolean fields and ensure scanners always evaluate conditions.

- [ ] 2.1: Remove `default=False` from `HttpRequestUsage.session_based` in `upcast/models/http_requests.py`
- [ ] 2.2: Remove `default=False` from `HttpRequestUsage.is_async` in `upcast/models/http_requests.py`
- [ ] 2.3: Remove `default=False` from `MetricInfo.custom_collector` in `upcast/models/metrics.py`
- [ ] 2.4: Remove `default=False` from `UrlPattern.is_partial` in `upcast/models/django_urls.py`
- [ ] 2.5: Remove `default=False` from `UrlPattern.is_conditional` in `upcast/models/django_urls.py`
- [ ] 2.6: Verify `HttpRequestsScanner` always assigns `session_based` and `is_async`
- [ ] 2.7: Verify `PrometheusMetricsScanner` always assigns `custom_collector`
- [ ] 2.8: Verify `DjangoUrlScanner` always assigns `is_partial` and `is_conditional`
- [ ] 2.9: Run tests to verify all boolean flags are provided

**Acceptance Criteria**:

- All 5 boolean fields have `Field(..., ...)` instead of `Field(default=False, ...)`
- All scanners explicitly assign boolean values in all code paths
- Tests pass without ValidationErrors

**Dependencies**: Phase 1 (recommended to complete first for easier debugging)

---

### Phase 3: Remove Summary Field Defaults ⏳ Not Started

**Objective**: Remove `default=0` from `SignalSummary` count fields and ensure complete summary calculation.

- [ ] 3.1: Remove `default=0` from `SignalSummary.django_receivers` in `upcast/models/signals.py`
- [ ] 3.2: Remove `default=0` from `SignalSummary.django_senders` in `upcast/models/signals.py`
- [ ] 3.3: Remove `default=0` from `SignalSummary.celery_receivers` in `upcast/models/signals.py`
- [ ] 3.4: Remove `default=0` from `SignalSummary.celery_senders` in `upcast/models/signals.py`
- [ ] 3.5: Remove `default=0` from `SignalSummary.custom_signals_defined` in `upcast/models/signals.py`
- [ ] 3.6: Remove `default=0` from `SignalSummary.unused_custom_signals` in `upcast/models/signals.py`
- [ ] 3.7: Verify `SignalsScanner._create_summary()` always provides all 6 counts
- [ ] 3.8: Run tests to verify summary completeness

**Acceptance Criteria**:

- All 6 count fields have `Field(..., ge=0, ...)` instead of `Field(default=0, ge=0, ...)`
- Summary calculation provides all counts in all scenarios
- Tests pass without ValidationErrors

**Dependencies**: Phases 1 and 2 (for cleaner diff and easier debugging)

---

### Phase 4: Testing and Validation ⏳ Not Started

**Objective**: Add comprehensive tests and validate changes across the codebase.

- [ ] 4.1: Add unit test: `test_signal_usage_requires_column`
- [ ] 4.2: Add unit test: `test_concurrency_usage_requires_column`
- [ ] 4.3: Add unit test: `test_blocking_operation_requires_column`
- [ ] 4.4: Add unit test: `test_settings_location_requires_column`
- [ ] 4.5: Add unit test: `test_env_var_location_requires_column`
- [ ] 4.6: Add unit test: `test_http_request_requires_boolean_flags`
- [ ] 4.7: Add unit test: `test_metric_info_requires_custom_collector`
- [ ] 4.8: Add unit test: `test_url_pattern_requires_boolean_flags`
- [ ] 4.9: Add unit test: `test_signal_summary_requires_all_counts`
- [ ] 4.10: Run full test suite to verify no regressions
- [ ] 4.11: Check test coverage (should maintain ≥80%)
- [ ] 4.12: Run ruff to verify code quality
- [ ] 4.13: Manual test: Run signal scanner on real project
- [ ] 4.14: Manual test: Run concurrency scanner on real project
- [ ] 4.15: Manual test: Run all scanners on test fixtures

**Acceptance Criteria**:

- 9 new unit tests verify ValidationError on missing fields
- All existing tests pass
- Test coverage ≥80%
- Ruff checks pass
- Manual validation on real projects succeeds
- No ValidationErrors in production scenarios

**Dependencies**: Phases 1, 2, and 3 (must complete implementation first)

---

## Summary

**Total Tasks**: 42

- Phase 1: 11 tasks
- Phase 2: 9 tasks
- Phase 3: 8 tasks
- Phase 4: 15 tasks

**Estimated Time**:

- Phase 1: 1-2 hours
- Phase 2: 1 hour
- Phase 3: 30 minutes
- Phase 4: 2-3 hours
- **Total**: 5-7 hours

**Risk Level**: Low

- Changes are isolated to model definitions
- Immediate validation feedback prevents bugs
- No external API changes
- Easy to rollback if needed

**Parallelization Opportunities**:

- Phases 1, 2, 3 can be done in parallel by different developers
- Phase 4 must wait for all implementations to complete
