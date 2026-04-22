# Scan-Upcast Repair Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Review the generated `/tmp/scan-upcast` suggestions objectively, accept only the ones that are currently valuable and correct for `upcast`, and fix them step-by-step with TDD and per-step verification.

**Architecture:** Treat `/tmp/scan-upcast/specs/improvement-spec.md` as an input, not as authoritative truth. Split work into scanner-local bugfixes first, keep each change atomic, and defer cross-scanner output-contract or performance work into a separate proposal track.

**Tech Stack:** Python, pytest, astroid, Pydantic, pre-commit, ruff, OpenSpec.

---

## Objective Review Summary

### Accept now as current bugfixes

1. `scan-http-requests`: invalid dict keys in `params` / `headers` / `json_body` can break `HttpRequestUsage` model construction.
2. `scan-concurrency-patterns`: substring-based `create_task` detection causes false positives.
3. `scan-django-models`: `files_scanned` is explicitly wrong because it uses model count.
4. `scan-unit-tests`: default include patterns miss `**/tests.py`.

### Accept only with narrower framing later

1. `scan-metrics`: `Gauge` / `Summary` unsupported is stale, but coverage and `usages` gaps still need targeted follow-up.
2. `scan-logging`: `logging.log()` support is likely a valid gap, but should stay scanner-local.
3. Several scanner-specific `files_scanned` issues are real, but should be fixed one scanner at a time rather than as a shared contract change.

### Defer / requires proposal

1. `files_with_issues` / `parse_failures` summary fields.
2. Parallel scanning, AST caching, skip-large-file heuristics, compact output flags.
3. Richer Semgrep/CodeQL-style report metadata.

### Reject as stale for current branch

1. `scan-env-vars` “all types unknown” is no longer current on this branch.

---

## Execution Order

1. Fix `scan-http-requests` invalid dict-key crash risk.
2. Fix `scan-concurrency-patterns` `create_task` false positives.
3. Fix `scan-django-models` `files_scanned`.
4. Fix `scan-unit-tests` default include patterns.
5. Reassess the remaining suggestions with fresh evidence after those four land.

---

### Task 1: Harden HTTP request usage extraction against invalid dict keys

**Files:**

- Modify: `tests/test_http_request_scanner/test_edge_cases.py`
- Modify: `upcast/scanners/http_requests.py`

**Step 1: Write the failing tests**

Add focused failing tests for three keyword fields:

- `headers={None: 'token'}` should not crash the scan; `usage.headers` should be omitted.
- `params={None: 'x'}` should not crash the scan; `usage.params` should be omitted.
- `json={None: 'x'}` should not crash the scan; `usage.json_body` should be omitted.

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_http_request_scanner/test_edge_cases.py -k "invalid_header_keys_are_omitted or invalid_param_keys_are_omitted or invalid_json_body_keys_are_omitted" -q`

Expected: FAIL because the scanner currently forwards raw dicts into `HttpRequestUsage`, whose fields require `dict[str, Any]`.

**Step 3: Write minimal implementation**

Keep the fix local to `upcast/scanners/http_requests.py`:

- do not change Pydantic models
- do not change shared inference helpers
- add a small helper that returns `None` unless the inferred value is a dict with all-string keys
- reuse that helper for `params`, `headers`, and `json_body`

**Step 4: Run tests to verify it passes**

Run: `uv run pytest tests/test_http_request_scanner -q`

Expected: PASS.

**Step 5: Run formatter and pre-commit checks**

Run:

- `uv run ruff check upcast/scanners/http_requests.py tests/test_http_request_scanner/test_edge_cases.py`
- `uv run ruff format --check upcast/scanners/http_requests.py tests/test_http_request_scanner/test_edge_cases.py`
- `uv run pre-commit run --files upcast/scanners/http_requests.py tests/test_http_request_scanner/test_edge_cases.py`

Expected: PASS.

**Step 6: Commit**

```bash
GIT_MASTER=1 git add upcast/scanners/http_requests.py tests/test_http_request_scanner/test_edge_cases.py
GIT_MASTER=1 git commit -m ":bug: fix: omit invalid http request metadata dicts"
```

---

### Task 2: Make `create_task` detection precise

**Files:**

- Modify: `tests/test_concurrency_pattern_scanner/...`
- Modify: `upcast/scanners/concurrency.py`

**Step 1: Write the failing test**

Add a regression test proving that a function whose name merely contains `create_task` is not treated as asyncio task creation.

**Step 2: Run test to verify it fails**

Run the smallest targeted pytest slice for the new regression.

**Step 3: Write minimal implementation**

Change detection from substring matching to exact supported call-shape matching.

**Step 4: Run tests to verify it passes**

Run the focused concurrency suite.

**Step 5: Run formatter and pre-commit checks**

Run targeted `ruff`, `ruff format --check`, and `pre-commit run --files`.

**Step 6: Commit**

Create one atomic commit for scanner + test.

---

### Task 3: Correct `scan-django-models` `files_scanned`

**Files:**

- Modify: `tests/test_django_models_scanner/...`
- Modify: `upcast/scanners/django_models.py`

Write one failing test, change only summary calculation, verify, run pre-commit, commit.

---

### Task 4: Include `tests.py` in unit-test scanner defaults

**Files:**

- Modify: `tests/test_unit_test_scanner/...`
- Modify: `upcast/scanners/unit_tests.py`

Write one failing test, update include patterns minimally, verify, run pre-commit, commit.

---

## Rules for every step

1. Start with RED and confirm the new test fails for the expected reason.
2. Make the smallest local change only.
3. Run the relevant scanner test slice before broadening.
4. Run `ruff`, `ruff format --check`, and `pre-commit run --files` before commit.
5. Commit only the implementation file and its direct tests.
6. Do not mix proposal-level work into these bugfix commits.
