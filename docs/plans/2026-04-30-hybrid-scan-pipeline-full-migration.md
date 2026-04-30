# Hybrid Scan Pipeline Full Migration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task.

**Goal:** Close the remaining hybrid pipeline risk and migrate every scanner command to the new core incrementally while preserving public CLI behavior through explicit old-vs-new comparisons.

**Architecture:** Keep `upcast.main:main` and `upcast/common/cli.py::run_scanner_cli(...)` as the public boundary. Adopt `upcast/common/hybrid_scan_pipeline.py` behind existing scanners in waves, using shared adapters and projection helpers so each migrated scanner can preserve its current `ScannerOutput` contract.

**Tech Stack:** `pytest`, `click.testing.CliRunner`, `uv run pytest`, `openspec validate --strict`, `ruff`, `astroid`, `ast-grep-py`, existing scanner/output models under `upcast/scanners/` and `upcast/models/`.

---

## Scope gate before coding

This plan assumes `add-hybrid-scan-pipeline` has been expanded to cover:

- all scanner command migration under `upcast.main:main`
- explicit `map-failure -> unknown` risk closure
- old-vs-new parity checks per command
- incremental adoption without replacing CLI wiring

Do not start migration code until that OpenSpec delta validates and is accepted.

## Scanner inventory and wave order

### Wave 0: risk closure + harness

- Shared core: `upcast/common/hybrid_scan_pipeline.py`
- Shared exports: `upcast/common/__init__.py`
- Shared CLI boundary: `upcast/common/cli.py`
- Shared scanner seam: `upcast/common/scanner_base.py`
- CLI parity tests: `tests/test_cli/`
- Hybrid core tests: `tests/test_common/test_hybrid_scan_pipeline.py`

### Wave 1: low-risk / structurally aligned scanners

- `upcast/scanners/complexity.py`
- `upcast/scanners/module_symbols.py`
- `upcast/scanners/exceptions.py`
- `upcast/scanners/blocking_operations.py`

### Wave 2: medium-risk scanners

- `upcast/scanners/logging_scanner.py`
- `upcast/scanners/metrics.py`
- `upcast/scanners/unit_tests.py`
- `upcast/scanners/concurrency.py`
- `upcast/scanners/redis_usage.py`
- `upcast/scanners/django_urls.py`

### Wave 3: high-risk scanners

- `upcast/scanners/http_requests.py`
- `upcast/scanners/django_models.py`
- `upcast/scanners/django_settings.py`
- `upcast/scanners/env_vars.py`
- `upcast/scanners/signals.py`

## Shared rules for every task

1. Write the failing test first.
2. Verify RED with the smallest relevant pytest slice.
3. Implement the minimum code to pass.
4. Re-run the focused test slice.
5. Run the old-vs-new CLI comparison for the migrated command.
6. Only then move to the next task.

## Task 1: Close `map-failure -> unknown` semantics

**Files:**

- Modify: `tests/test_common/test_hybrid_scan_pipeline.py`
- Modify: `upcast/common/hybrid_scan_pipeline.py`

**Step 1: Write the failing test**

Add tests that prove:

- a primary CST-to-astroid map failure becomes internal `unknown` evidence rather than disappearing
- a capture-specific map failure preserves enough reason context for debugging/parity review

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_common/test_hybrid_scan_pipeline.py -q`

Expected: FAIL because the current implementation silently drops unmapped candidates.

**Step 3: Write minimal implementation**

Update `upcast/common/hybrid_scan_pipeline.py` so the pipeline retains mapping ambiguity as internal `unknown` semantics without breaking the current public finding projection.

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_common/test_hybrid_scan_pipeline.py tests/test_common/test_cst_ast_mapper.py tests/test_common/test_astroid_matcher.py -q`

Expected: PASS.

## Task 2: Add shared migration/parity helpers

**Files:**

- Modify: `upcast/common/scanner_base.py`
- Create or modify: `upcast/common/adapter.py`
- Create or modify: `tests/test_cli/` helper modules as needed

**Step 1: Write the failing test**

Add failing tests for a minimal adapter that lets a scanner reuse the hybrid pipeline without changing `run_scanner_cli(...)` semantics.

**Step 2: Run test to verify it fails**

Run the smallest new pytest slice under `tests/test_common/` and/or `tests/test_cli/`.

**Step 3: Write minimal implementation**

Implement only the adapter/projection plumbing needed for the first migrated scanner and CLI parity comparison.

**Step 4: Run test to verify it passes**

Run focused common/CLI tests and `uv run --extra dev ruff check` on changed files.

## Task 3: Build old-vs-new CLI comparison harness

**Files:**

- Modify: `tests/test_cli/` helper modules
- Modify: `docs/plans/2026-04-23-cli-functional-test-rollout.md` only if a cross-reference is useful

**Step 1: Write the failing test**

Add a parity helper test that compares:

- exit code
- default YAML stdout
- JSON output file content
- normalized `results`

for one proving command through `CliRunner.invoke(upcast.main:main, ...)`.

**Step 2: Run test to verify it fails**

Run the relevant CLI pytest slice.

**Step 3: Write minimal implementation**

Implement the comparison helper with normalization rules that ignore non-deterministic metadata.

**Step 4: Run test to verify it passes**

Run the proving CLI slice and then `make test-integration` if the helper touches snapshot/baseline logic.

## Task 4: Migrate Wave 1 scanners one by one

### 4.1 `scan-complexity-patterns`

**Files:**

- Modify: `upcast/scanners/complexity.py`
- Modify: `upcast/models/complexity.py` only if projection needs a non-breaking helper
- Modify/Test: `tests/test_cli/test_scan_complexity_patterns.py`
- Modify/Test: scanner-specific tests already covering complexity behavior

**Per-scanner steps:**

1. Write a failing scanner-local or CLI parity test.
2. Run it to confirm RED.
3. Migrate only the candidate-selection/semantic portion that fits the single-round pipeline.
4. Re-run focused tests.
5. Run old-vs-new comparison for `scan-complexity-patterns` including `--threshold`.

### 4.2 `scan-module-symbols`

**Files:**

- Modify: `upcast/scanners/module_symbols.py`
- Modify/Test: `tests/test_cli/test_scan_module_symbols.py`

Repeat the same RED → GREEN → parity sequence, including `--include-private` behavior.

### 4.3 `scan-exception-handlers`

**Files:**

- Modify: `upcast/scanners/exceptions.py`
- Modify/Test: `tests/test_cli/test_scan_exception_handlers.py`

### 4.4 `scan-blocking-operations`

**Files:**

- Modify: `upcast/scanners/blocking_operations.py`
- Modify/Test: `tests/test_cli/test_scan_blocking_operations.py`

**Wave 1 verification:**

Run:

- `uv run pytest tests/test_cli/test_scan_complexity_patterns.py tests/test_cli/test_scan_module_symbols.py tests/test_cli/test_scan_exception_handlers.py tests/test_cli/test_scan_blocking_operations.py -q`
- `uv run --extra dev ruff check <changed files>`

Commit each scanner separately after parity passes.

## Task 5: Migrate Wave 2 scanners one by one

**Files (scanner side):**

- `upcast/scanners/logging_scanner.py`
- `upcast/scanners/metrics.py`
- `upcast/scanners/unit_tests.py`
- `upcast/scanners/concurrency.py`
- `upcast/scanners/redis_usage.py`
- `upcast/scanners/django_urls.py`

**Files (CLI tests):**

- `tests/test_cli/test_scan_logging.py`
- `tests/test_cli/test_scan_metrics.py`
- `tests/test_cli/test_scan_unit_tests.py`
- `tests/test_cli/test_scan_concurrency_patterns.py`
- `tests/test_cli/test_scan_redis_usage.py`
- `tests/test_cli/test_scan_django_urls.py`

For each scanner:

1. Add a failing parity test for default YAML/JSON behavior.
2. Add one command-specific failing check (`--sensitive-keywords`, `--root-modules`, verbose text, etc.).
3. Implement the minimum pipeline adoption.
4. Re-run focused tests.
5. Run old-vs-new comparison before committing.

## Task 6: Migrate Wave 3 scanners one by one

**Files (scanner side):**

- `upcast/scanners/http_requests.py`
- `upcast/scanners/django_models.py`
- `upcast/scanners/django_settings.py`
- `upcast/scanners/env_vars.py`
- `upcast/scanners/signals.py`

**Files (CLI tests):**

- `tests/test_cli/test_scan_http_requests.py`
- `tests/test_cli/test_scan_django_models.py`
- `tests/test_cli/test_scan_django_settings.py`
- `tests/test_cli/test_scan_env_vars.py`
- `tests/test_cli/test_scan_signals.py`

For each scanner:

1. Start with a failing parity test.
2. Keep scanner-specific aggregation/projection if full pipeline replacement would break parity.
3. Re-run focused tests and old-vs-new comparisons.
4. Stop the wave immediately if an unexpected CLI/output regression appears.

## Task 7: Final sweep and submission readiness

**Files:**

- Any touched scanner/common/test/doc files
- OpenSpec tasks/checklists for this change

**Step 1: Run full validation**

Run at minimum:

- `uv run pytest tests/test_common/test_hybrid_scan_pipeline.py tests/test_cli -q`
- `make test-integration`
- `uv run --extra dev ruff check <all changed files>`
- `openspec validate add-hybrid-scan-pipeline --strict`

**Step 2: Verify parity evidence**

For all 15 commands in `upcast/main.py`, ensure there is recorded evidence of old-vs-new comparison, including command-specific option coverage.

**Step 3: Update tasks**

Mark the corresponding OpenSpec checklist items complete only after verification is real.

**Step 4: Commit**

Keep history atomic:

- one commit for scope/doc expansion
- one commit for risk closure
- one commit for shared harness/adapters
- one commit per migrated scanner
- one final validation/doc cleanup commit only if needed

## Success criteria

- `add-hybrid-scan-pipeline` scope explicitly covers all scanner migrations and parity checks
- mapping ambiguity is preserved as internal `unknown` evidence
- all 15 scanner commands remain available through `upcast.main:main`
- every migrated command has old-vs-new parity evidence
- scanner output contracts remain compatible unless intentionally documented otherwise
- full common/CLI/integration validation passes before final submission
