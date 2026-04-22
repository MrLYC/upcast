# Scanner Follow-up Improvements Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Address the remaining high-value scanner improvements that were deferred from the latest narrow bugfix round, using TDD and atomic scanner-by-scanner changes.

**Architecture:** This plan keeps the next round split into scanner-local workstreams so each change starts with a failing regression test, lands with the smallest possible code change, and verifies against the scanner’s focused suite before moving on. Lower-risk precision fixes come first, schema-enrichment scanners come next, and legacy-backed or spec-heavy scanners stay isolated until the earlier waves are green.

**Tech Stack:** Python 3.13, pytest, astroid AST parsing, Pydantic models, upcast scanner architecture.

---

## Phase Order

1. Build the regression matrix and fixture inventory.
2. Ship high-ROI precision fixes: HTTP requests, concurrency, logging, Redis.
3. Ship schema-enrichment scanners: Django URLs, module symbols, unit tests.
4. Ship higher-risk bounded follow-ups: Django settings, signals.
5. Only if reproduced: complexity `comment_lines`.

## Ground Rules

- Every task starts with a failing test.
- Do not mix unrelated scanners in one commit.
- Prefer additive schema changes unless an existing model already requires restructuring.
- Keep fixtures close to the existing scanner test package unless a shared fixture is clearly better.
- Run only the targeted test module first; widen verification after green.

---

### Task 1: Build the regression matrix and fixture inventory

**Files:**
- Modify: `tests/TEST_PLAN.md`
- Review: `tests/test_http_request_scanner/`
- Review: `tests/test_concurrency_pattern_scanner/`
- Review: `tests/test_logging_scanner/`
- Review: `tests/test_redis_usage_scanner/`
- Review: `tests/test_django_urls_scanner/`
- Review: `tests/test_module_symbol_scanner/`
- Review: `tests/test_unit_test_scanner/`
- Review: `tests/test_django_settings_scanner/`
- Review: `tests/test_signals_scanner/`
- Review: `tests/test_cyclomatic_complexity_scanner/`
- Review: `tests/test_scanners/test_complexity.py`

**Step 1: Write the regression matrix**

Document each deferred improvement as one row in `tests/TEST_PLAN.md` with:
- scanner name
- bug / enhancement summary
- target test file
- target fixture file
- expected assertion
- whether schema changes are required

**Step 2: Review that each item has a target test entry point**

Run: no command required
Expected: every remaining improvement is mapped to one concrete test file and one fixture location.

**Step 3: Commit**

```bash
git add tests/TEST_PLAN.md
git commit -m "docs: map follow-up scanner regression work"
```

---

### Task 2: Exclude HTTP mocks and detect real httpx/aiohttp patterns

**Files:**
- Modify: `upcast/scanners/http_requests.py`
- Modify: `tests/test_http_request_scanner/test_edge_cases.py`
- Modify: `tests/test_http_request_scanner/test_scanner_integration.py`
- Modify: `tests/test_http_request_scanner/test_url_patterns.py`
- Create: `tests/test_http_request_scanner/fixtures/mock_vs_real_requests.py`

**Step 1: Write the failing tests**

Add focused failing tests for:
- `requests_mock` registration calls that must be ignored
- real `httpx.Client()` and `httpx.AsyncClient()` request calls that must be detected
- real `aiohttp.ClientSession()` request calls that must be detected when they are directly visible in AST patterns

**Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_http_request_scanner/test_edge_cases.py tests/test_http_request_scanner/test_scanner_integration.py -v`
Expected: FAIL on the newly added mock-exclusion and library-detection assertions.

**Step 3: Write minimal implementation**

Update `upcast/scanners/http_requests.py` to:
- reject known mock registration APIs before request classification
- recognize supported `httpx` call sites
- recognize supported `aiohttp` request call sites without broadening to speculative patterns

**Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_http_request_scanner -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add upcast/scanners/http_requests.py tests/test_http_request_scanner
git commit -m "fix: improve http request scanner precision"
```

---

### Task 3: Add Celery detection to concurrency patterns

**Files:**
- Modify: `upcast/scanners/concurrency.py`
- Modify: `tests/test_concurrency_pattern_scanner/test_edge_cases.py`
- Modify: `tests/test_concurrency_pattern_scanner/test_integration.py`
- Modify: `tests/test_concurrency_integration.py`
- Create: `tests/test_concurrency_pattern_scanner/fixtures/celery_patterns.py`

**Step 1: Write the failing tests**

Add failing tests for:
- `@shared_task`
- `@app.task`
- direct `.delay()` / `.apply_async()` patterns when they should count as Celery usage

**Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_concurrency_pattern_scanner/test_edge_cases.py tests/test_concurrency_pattern_scanner/test_integration.py tests/test_concurrency_integration.py -v`
Expected: FAIL because the `celery` result bucket stays empty.

**Step 3: Write minimal implementation**

Update `upcast/scanners/concurrency.py` so `scan()` fills the existing `celery` bucket from AST-detected Celery task and invocation patterns.

**Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_concurrency_pattern_scanner tests/test_concurrency_integration.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add upcast/scanners/concurrency.py tests/test_concurrency_pattern_scanner tests/test_concurrency_integration.py
git commit -m "fix: add celery coverage to concurrency scanner"
```

---

### Task 4: Tighten logging sensitivity and message extraction

**Files:**
- Modify: `upcast/scanners/logging_scanner.py`
- Modify: `tests/test_logging_scanner/test_edge_cases.py`
- Modify: `tests/test_logging_scanner/test_logger_names.py`
- Modify: `tests/test_logging_scanner/test_scanner.py`
- Create: `tests/test_logging_scanner/fixtures/sensitive_logging_patterns.py`

**Step 1: Write the failing tests**

Add failing tests for:
- `headers`, `token`, `password`, `cookie`, `auth`, `secret` sensitivity detection
- `logging.getLogger("name")` logger-name extraction
- `.format(...)` and `%` interpolation template cleanup so the message field stores the template rather than the full expression

**Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_logging_scanner/test_edge_cases.py tests/test_logging_scanner/test_logger_names.py tests/test_logging_scanner/test_scanner.py -v`
Expected: FAIL on new sensitivity and extraction assertions.

**Step 3: Write minimal implementation**

Update `upcast/scanners/logging_scanner.py` to:
- extend the sensitive-keyword set
- prefer logical logger names over file-path fallbacks where possible
- normalize `.format(...)` and `%`-style message extraction to the template string

**Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_logging_scanner -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add upcast/scanners/logging_scanner.py tests/test_logging_scanner
git commit -m "fix: improve logging scanner signal quality"
```

---

### Task 5: Expand Redis operation coverage and TTL accuracy

**Files:**
- Modify: `upcast/scanners/redis_usage.py`
- Modify: `tests/test_redis_usage_scanner/test_operations.py`
- Modify: `tests/test_redis_usage_scanner/test_edge_cases.py`
- Modify: `tests/test_redis_usage_scanner/test_config_detection.py`
- Create: `tests/test_redis_usage_scanner/fixtures/ttl_patterns.py`

**Step 1: Write the failing tests**

Add failing tests for:
- `cache.add`, `cache.delete_many`, `cache.clear`, `cache.touch`, `incr`, `decr`
- dynamic TTL parameters that must not be treated as missing TTL
- Redis URL configuration detection only if it fits the current model cleanly

**Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_redis_usage_scanner/test_operations.py tests/test_redis_usage_scanner/test_edge_cases.py tests/test_redis_usage_scanner/test_config_detection.py -v`
Expected: FAIL on the new operation and TTL assertions.

**Step 3: Write minimal implementation**

Update `upcast/scanners/redis_usage.py` to add the new operation families and distinguish `dynamic_ttl` from missing TTL.

**Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_redis_usage_scanner -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add upcast/scanners/redis_usage.py tests/test_redis_usage_scanner
git commit -m "fix: expand redis scanner coverage and ttl handling"
```

---

### Task 6: Enrich Django URL output with file, line, view, converter, and full path

**Files:**
- Modify: `upcast/models/django_urls.py`
- Modify: `upcast/scanners/django_urls.py`
- Modify: `upcast/common/django/view_resolver.py`
- Modify: `tests/test_django_urls_scanner/test_models.py`
- Modify: `tests/test_django_urls_scanner/test_edge_cases.py`
- Modify: `tests/test_django_urls_scanner/test_converters.py`
- Modify: `tests/test_django_urls_scanner/test_integration.py`
- Modify: `tests/test_django_urls_scanner/test_drf_routers.py`
- Create: `tests/test_django_urls_scanner/fixtures/nested_urls.py`

**Step 1: Write the failing tests**

Add failing tests for:
- `file` and `line`
- extracted view name / module where statically resolvable
- path converters like `<int:pk>`
- nested `include()` full-path reconstruction

**Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_django_urls_scanner/test_models.py tests/test_django_urls_scanner/test_edge_cases.py tests/test_django_urls_scanner/test_converters.py tests/test_django_urls_scanner/test_integration.py tests/test_django_urls_scanner/test_drf_routers.py -v`
Expected: FAIL on the new metadata and full-path assertions.

**Step 3: Write minimal implementation**

Update the URL models and scanner logic so the new fields are added without regressing current path extraction.

**Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_django_urls_scanner -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add upcast/models/django_urls.py upcast/scanners/django_urls.py upcast/common/django/view_resolver.py tests/test_django_urls_scanner
git commit -m "feat: enrich django url scanner metadata"
```

---

### Task 7: Enrich module symbol methods and function arguments

**Files:**
- Modify: `upcast/models/module_symbols.py`
- Modify: `upcast/scanners/module_symbols.py`
- Modify: `tests/test_module_symbol_scanner/test_classes.py`
- Modify: `tests/test_module_symbol_scanner/test_functions.py`
- Modify: `tests/test_module_symbol_scanner/test_models.py`
- Modify: `tests/test_module_symbol_scanner/test_integration.py`
- Create: `tests/test_module_symbol_scanner/fixtures/rich_symbols.py`

**Step 1: Write the failing tests**

Add failing tests for:
- per-method metadata with `line`, `args`, and decorators
- function argument extraction
- class-method details that are currently flattened to plain strings

**Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_module_symbol_scanner/test_classes.py tests/test_module_symbol_scanner/test_functions.py tests/test_module_symbol_scanner/test_models.py tests/test_module_symbol_scanner/test_integration.py -v`
Expected: FAIL because the current model/scanner do not carry the richer fields.

**Step 3: Write minimal implementation**

Update `upcast/models/module_symbols.py` and `upcast/scanners/module_symbols.py` so method metadata becomes structured and function args are extracted correctly.

**Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_module_symbol_scanner -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add upcast/models/module_symbols.py upcast/scanners/module_symbols.py tests/test_module_symbol_scanner
git commit -m "feat: enrich module symbol scanner details"
```

---

### Task 8: Enrich unit test scanner with class, fixture, mark, and parametrize structure

**Files:**
- Modify: `upcast/models/unit_tests.py`
- Modify: `upcast/scanners/unit_tests.py`
- Modify: `tests/test_unit_test_scanner/test_edge_cases.py`
- Modify: `tests/test_unit_test_scanner/test_targets.py`
- Modify: `tests/test_unit_test_scanner/test_assertions.py`
- Modify: `tests/test_unit_test_scanner/test_integration.py`
- Modify: `tests/test_unit_test_scanner/test_models.py`
- Create: `tests/test_unit_test_scanner/fixtures/test_structure_patterns.py`

**Step 1: Write the failing tests**

Add failing tests for:
- `class TestXxx` hierarchy
- `@pytest.fixture`
- `pytest.mark.*`
- `pytest.mark.parametrize`
- preserving current `assert_count` behavior

**Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_unit_test_scanner/test_edge_cases.py tests/test_unit_test_scanner/test_targets.py tests/test_unit_test_scanner/test_assertions.py tests/test_unit_test_scanner/test_integration.py tests/test_unit_test_scanner/test_models.py -v`
Expected: FAIL because the current scanner only emits flat test metadata.

**Step 3: Write minimal implementation**

Update `upcast/models/unit_tests.py` and `upcast/scanners/unit_tests.py` to add the richer structure while preserving existing flat fields where compatibility matters.

**Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_unit_test_scanner -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add upcast/models/unit_tests.py upcast/scanners/unit_tests.py tests/test_unit_test_scanner
git commit -m "feat: enrich unit test scanner structure"
```

---

### Task 9: Improve Django settings fidelity in a bounded way

**Files:**
- Modify: `upcast/scanners/django_settings.py`
- Modify: `upcast/models/django_settings.py`
- Modify: `tests/test_django_settings_scanner/test_edge_cases.py`
- Modify: `tests/test_django_settings_scanner/test_integration.py`
- Modify: `tests/test_django_settings_scanner/test_type_inference.py`
- Modify: `tests/test_django_settings_scanner/test_models.py`
- Create: `tests/test_django_settings_scanner/fixtures/standard_settings.py`

**Step 1: Write the failing tests**

Add failing tests for:
- standard settings such as `ROOT_URLCONF`, `TEMPLATES`, `WSGI_APPLICATION`, `ALLOWED_HOSTS`, `STATIC_URL`, `MEDIA_URL`
- tuple/list parsing that must ignore comments rather than inserting `null`

**Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_django_settings_scanner/test_edge_cases.py tests/test_django_settings_scanner/test_integration.py tests/test_django_settings_scanner/test_type_inference.py tests/test_django_settings_scanner/test_models.py -v`
Expected: FAIL on the new bounded settings assertions.

**Step 3: Write minimal implementation**

Update the Django settings scanner only enough to:
- recognize the targeted standard settings
- filter comment artifacts out of tuple/list parsing

**Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_django_settings_scanner -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add upcast/scanners/django_settings.py upcast/models/django_settings.py tests/test_django_settings_scanner
git commit -m "fix: improve django settings scanner fidelity"
```

---

### Task 10: Detect signal senders and custom signal definitions

**Files:**
- Modify: `upcast/scanners/signals.py`
- Modify: `upcast/common/signals/signal_checker.py`
- Modify: `upcast/common/signals/signal_parser.py`
- Modify: `tests/test_signals_scanner/test_integration.py`
- Modify: `tests/test_signals_scanner/test_models.py`
- Create: `tests/test_signals_scanner/fixtures/custom_signal_patterns.py`

**Step 1: Write the failing tests**

Add failing tests for:
- `.send()`
- `.send_robust()`
- `Signal()` definitions

**Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_signals_scanner/test_integration.py tests/test_signals_scanner/test_models.py -v`
Expected: FAIL because current output misses senders and custom signal definitions.

**Step 3: Write minimal implementation**

Update the wrapper and legacy signal helpers so sender calls and custom definitions are emitted without widening to arbitrary `.send()` methods.

**Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_signals_scanner -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add upcast/scanners/signals.py upcast/common/signals/signal_checker.py upcast/common/signals/signal_parser.py tests/test_signals_scanner
git commit -m "fix: improve signal scanner sender coverage"
```

---

### Task 11: Revisit complexity comment_lines only if reproduced

**Files:**
- Modify: `upcast/common/code_utils.py`
- Modify: `upcast/scanners/complexity.py`
- Modify: `tests/test_cyclomatic_complexity_scanner/test_code_utils.py`
- Modify: `tests/test_cyclomatic_complexity_scanner/test_scanner_integration.py`
- Modify: `tests/test_scanners/test_complexity.py`
- Create: `tests/test_cyclomatic_complexity_scanner/fixtures/comment_preservation.py`

**Step 1: Write the failing test**

Add one minimal failing test that proves `comment_lines` is lost for a concrete function fixture.

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_cyclomatic_complexity_scanner/test_code_utils.py tests/test_cyclomatic_complexity_scanner/test_scanner_integration.py tests/test_scanners/test_complexity.py -v`
Expected: FAIL on the new `comment_lines` assertion. If it does not fail, stop and drop this task.

**Step 3: Write minimal implementation**

Update source extraction / comment counting only enough to preserve real comment lines for the reproduced case.

**Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_cyclomatic_complexity_scanner tests/test_scanners/test_complexity.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add upcast/common/code_utils.py upcast/scanners/complexity.py tests/test_cyclomatic_complexity_scanner tests/test_scanners/test_complexity.py
git commit -m "fix: preserve complexity scanner comment lines"
```

---

## Final Verification Pass

After each task is green, run only that scanner’s focused suite first. After a whole phase finishes, run the phase-level verification:

- Phase 2: `uv run pytest tests/test_http_request_scanner tests/test_concurrency_pattern_scanner tests/test_concurrency_integration.py tests/test_logging_scanner tests/test_redis_usage_scanner -v`
- Phase 3: `uv run pytest tests/test_django_urls_scanner tests/test_module_symbol_scanner tests/test_unit_test_scanner -v`
- Phase 4: `uv run pytest tests/test_django_settings_scanner tests/test_signals_scanner -v`
- Phase 5: `uv run pytest tests/test_cyclomatic_complexity_scanner tests/test_scanners/test_complexity.py -v`

## Recommended Execution Order

1. Task 1
2. Tasks 2-5 in parallel by scanner
3. Tasks 6-8 in parallel by scanner
4. Task 9
5. Task 10
6. Task 11 only if its red test is real

## Notes

- The highest-confidence next wins are Tasks 2, 3, 4, and 5.
- The highest product value but larger schema churn sits in Tasks 6, 7, and 8.
- The highest regression-risk items are Tasks 9 and 10, so they should stay isolated.
