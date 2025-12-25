# Implementation Tasks

## Phase 1: Model Field Updates

### Task 1.1: Update string fields to Optional

- [ ] Update `env_vars.py`: code, default_value → `| None` with `Field(None, ...)`
- [ ] Update `blocking_operations.py`: statement, function, class_name → `| None`
- [ ] Update `django_settings.py`: code, value, statement, overrides, base_module → `| None`
- [ ] Update `signals.py`: handler, pattern, code, sender, status → `| None`
- [ ] Update `metrics.py`: namespace, subsystem, unit → `| None`
- [ ] Update `concurrency.py`: statement → `| None`
- [ ] Update `django_urls.py`: pattern, view_module, view_name, include_module, namespace, name, viewset_module, viewset_name, basename, router_type, description, note → `| None`
- [ ] Update `django_models.py`: related_name, on_delete, description → `| None`
- [ ] Verify `complexity.py` already has correct `| None` for message, description, signature, code

**Validation**: Run `ruff check upcast/models/` and verify type annotations

### Task 1.2: Update collection fields to Optional

- [ ] Update `http_requests.py`: params, headers, json_body, data → `| None` (remove `default_factory=dict`)
- [ ] Update `signals.py`: context → `| None` (remove `default_factory=dict`)
- [ ] Update `concurrency.py`: context → `| None` (remove `default_factory=dict`)
- [ ] Update `django_models.py`: meta → `| None` (remove `default_factory=dict`)
- [ ] Update `metrics.py`: buckets → `| None` (remove `default_factory=list`)
- [ ] Keep `base.py`: metadata with `default_factory=dict` (legitimate mutable default)

**Validation**: Verify no `default_factory` on truly optional collections

### Task 1.3: Update numeric fields to Optional

- [ ] Update `http_requests.py`: timeout → `| None` (remove `Field(0, ...)`)
- [ ] Update `base.py`: scan_duration_ms → `| None` (remove `Field(0, ...)`)
- [ ] Keep `ExceptClause` counters with `default=0` (semantically meaningful)

**Validation**: Verify legitimate defaults remain (log counters, etc.)

### Task 1.4: Fix exception clause placeholders

- [ ] Update `exceptions.py`: else_clause → `ElseClause | None = Field(None, ...)`
- [ ] Update `exceptions.py`: finally_clause → `FinallyClause | None = Field(None, ...)`
- [ ] Remove `default_factory=lambda: ElseClause(line=0, lines=0)` pattern
- [ ] Update ElseClause/FinallyClause line validation back to `ge=1`

**Validation**: Verify exception models accept None for optional clauses

## Phase 2: Scanner Updates

### Task 2.1: Update HTTP request scanner

- [ ] Change `timeout=self._extract_timeout(node) or 0` → `timeout=self._extract_timeout(node)`
- [ ] Verify `_extract_timeout` returns `None` when not found (not 0)
- [ ] Remove `or {}` fallbacks for params/headers/json_body/data

**Validation**: Run `pytest tests/test_scanners/test_http_requests.py -v`

### Task 2.2: Update environment variable scanner

- [ ] Change `default_value=default_value or ""` → `default_value=default_value`
- [ ] Change `code=safe_as_string(node)` → `code=safe_as_string(node) or None`
- [ ] Verify None passed when code extraction fails

**Validation**: Run `pytest tests/test_scanners/test_env_vars.py -v`

### Task 2.3: Update blocking operations scanner

- [ ] Change `statement=safe_as_string(node) or ""` → `statement=safe_as_string(node) or None`
- [ ] Change `function=self._get_function_name(node) or ""` → `function=self._get_function_name(node)`
- [ ] Change `class_name=self._get_class_name(node) or ""` → `class_name=self._get_class_name(node)`

**Validation**: Run `pytest tests/test_scanners/test_blocking_operations.py -v`

### Task 2.4: Update Django models scanner

- [ ] Change `related_name=rel_info.get("related_name") or ""` → `related_name=rel_info.get("related_name")`
- [ ] Change `on_delete=rel_info.get("on_delete") or ""` → `on_delete=rel_info.get("on_delete")`
- [ ] Change `meta=model_data.get("meta") or {}` → `meta=model_data.get("meta")`
- [ ] Change `description=model_data.get("description") or ""` → `description=model_data.get("description")`

**Validation**: Run `pytest tests/test_scanners/test_django_models.py -v`

### Task 2.5: Update exception scanner

- [ ] Change `else_clause = self._parse_else_clause(node) or ElseClause(line=0, lines=0)` → `else_clause = self._parse_else_clause(node)`
- [ ] Change `finally_clause = self._parse_finally_clause(node) or FinallyClause(line=0, lines=0)` → `finally_clause = self._parse_finally_clause(node)`
- [ ] Verify `_parse_else_clause` and `_parse_finally_clause` already return `None` when absent

**Validation**: Run `pytest tests/test_scanners/test_exceptions.py -v`

### Task 2.6: Update signals scanner

- [ ] Change `handler=usage_dict.get("handler") or ""` → `handler=usage_dict.get("handler")`
- [ ] Change `pattern=usage_dict.get("pattern") or ""` → `pattern=usage_dict.get("pattern")`
- [ ] Change `code=usage_dict.get("code") or ""` → `code=usage_dict.get("code")`
- [ ] Change `sender=usage_dict.get("sender") or ""` → `sender=usage_dict.get("sender")`
- [ ] Change `context=usage_dict.get("context") or {}` → `context=usage_dict.get("context")`
- [ ] Change `status=""` → `status=None` in SignalInfo creation

**Validation**: Run `pytest tests/test_scanners/test_signal.py -v`

### Task 2.7: Update metrics scanner

- [ ] Change `namespace=""` → `namespace=None` in MetricInfo creation
- [ ] Change `subsystem=""` → `subsystem=None`
- [ ] Change `unit=""` → `unit=None`
- [ ] Change `buckets=[]` → `buckets=None`

**Validation**: Run `pytest tests/test_scanners/test_metrics.py -v`

### Task 2.8: Update Django URLs scanner

- [ ] Change all `or ""` fallbacks to pass actual values or `None`
- [ ] Update UrlPattern instantiation to use `None` for absent fields
- [ ] Remove all empty string defaults in scanner logic

**Validation**: Run `pytest tests/test_scanners/test_django_urls.py -v`

### Task 2.9: Update Django settings scanner

- [ ] Change `value=defn.value if defn.type == "literal" else ""` → `value=defn.value if defn.type == "literal" else None`
- [ ] Change `statement=defn.value if defn.type != "literal" else ""` → `statement=defn.value if defn.type != "literal" else None`
- [ ] Change `overrides=defn.overrides or ""` → `overrides=defn.overrides`
- [ ] Change `base_module=di.base_module or ""` → `base_module=di.base_module`

**Validation**: Run `pytest tests/test_scanners/test_django_settings.py -v`

### Task 2.10: Update complexity scanner

- [ ] Change `code=code or ""` → `code=code` (keep as-is, already returns None on failure)
- [ ] Change `description=extract_description(node) or ""` → `description=extract_description(node)`
- [ ] Change `signature=extract_function_signature(node) or ""` → `signature=extract_function_signature(node)`

**Validation**: Run `pytest tests/test_scanners/test_complexity.py -v`

## Phase 3: Test Updates

### Task 3.1: Update base model tests

- [ ] Update `test_summary_without_duration`: Change `assert summary.scan_duration_ms == 0` → `assert summary.scan_duration_ms is None`

**Validation**: Run `pytest tests/test_common/test_models.py -v`

### Task 3.2: Update complexity tests

- [ ] Update `test_valid_output`: Change `message=""` → `message=None`

**Validation**: Run `pytest tests/test_scanners/test_complexity.py::TestComplexityOutputModel -v`

### Task 3.3: Update Django models tests

- [ ] Update `test_scanner_extracts_description`: Change `assert page_model.description == ""` → `assert page_model.description is None`

**Validation**: Run `pytest tests/test_scanners/test_django_models.py::TestDjangoModelScannerIntegration -v`

### Task 3.4: Update env vars tests

- [ ] Update `test_location_with_optional_fields`: Change `assert location.code == ""` → `assert location.code is None`
- [ ] Update `test_valid_env_var_info_required`: Change `default_value=""` → `default_value=None`, `assert info.default_value == ""` → `assert info.default_value is None`

**Validation**: Run `pytest tests/test_scanners/test_env_vars.py -v`

### Task 3.5: Update HTTP request tests

- [ ] Update `test_valid_usage`: Change all `params={}, headers={}, json_body={}, data={}, timeout=0` → `params=None, headers=None, json_body=None, data=None, timeout=None`

**Validation**: Run `pytest tests/test_scanners/test_http_requests.py::TestHttpRequestModels -v`

### Task 3.6: Update signal tests

- [ ] Update `test_signal_usage_minimal`: Change `assert usage.handler == ""` → `assert usage.handler is None`, `assert usage.pattern == ""` → `assert usage.pattern is None`

**Validation**: Run `pytest tests/test_scanners/test_signal.py::TestSignalUsageModel -v`

## Phase 4: Spec and Documentation Updates

### Task 4.1: Update data-models spec

- [ ] Modify `data-models/spec.md` to document optional field philosophy
- [ ] Add scenario: "Optional fields use None not defaults"
- [ ] Update examples to show `| None` pattern
- [ ] Document when defaults are appropriate (log counters, metadata)

**Validation**: Run `openspec validate revert-to-optional-fields --strict`

### Task 4.2: Update model docstrings

- [ ] Add comments explaining `| None` fields in each model
- [ ] Document when `None` is used vs when field is required
- [ ] Update module-level docstrings

**Validation**: Review docstrings for clarity

## Phase 5: Final Validation

### Task 5.1: Run full test suite

- [ ] Run `uv run pytest tests/ -v`
- [ ] Verify all 261 tests pass
- [ ] Check test coverage with `uv run pytest --cov=upcast --cov-report=term-missing`
- [ ] Ensure coverage ≥80%

**Validation**: All tests green, coverage acceptable

### Task 5.2: Run code quality checks

- [ ] Run `uv run ruff check .`
- [ ] Run `uv run mypy upcast/` (if type checking enabled)
- [ ] Verify no new warnings

**Validation**: Ruff and type checks pass

### Task 5.3: Manual validation

- [ ] Test scanners on real project (wagtail)
- [ ] Verify JSON output with `exclude_none=True`
- [ ] Check None handling in edge cases
- [ ] Verify backwards compatibility

**Validation**: Manual testing successful

### Task 5.4: Validate OpenSpec change

- [ ] Run `openspec validate revert-to-optional-fields --strict`
- [ ] Resolve any validation errors
- [ ] Verify all specs consistent

**Validation**: OpenSpec validation passes

## Dependencies

- Task 2.x depends on Task 1.x (scanners need updated models)
- Task 3.x depends on Task 1.x and 2.x (tests need updated models and scanners)
- Task 4.x can run in parallel with Task 1-3
- Task 5.x depends on all previous tasks

## Estimated Effort

- Phase 1 (Models): ~2 hours
- Phase 2 (Scanners): ~3 hours
- Phase 3 (Tests): ~2 hours
- Phase 4 (Docs): ~1 hour
- Phase 5 (Validation): ~1 hour

**Total**: ~9 hours of focused development time
