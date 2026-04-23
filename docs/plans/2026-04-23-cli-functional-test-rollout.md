# CLI Functional Tests Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task.

**Goal:** Lock down the public behavior of every CLI command exposed by `upcast.main:main` using functional tests only, so later refactors can preserve compatibility.

**Architecture:** Test the public Click group from `upcast.main` with `CliRunner.invoke(main, [...])`, because that is the smallest boundary that still exercises command registration in `upcast/main.py` and shared execution in `upcast/common/cli.py`. Keep tests under `tests/test_cli/`, use tiny synthetic projects via existing pytest fixtures, and avoid production-code changes unless a true testability blocker is proven.

**Tech Stack:** `pytest`, `click.testing.CliRunner`, `tmp_project`, `tmp_py_file`, `uv run pytest`, `make check`

---

## Public command inventory

Commands exposed by `upcast.main:main`:

- `scan-complexity-patterns`
- `scan-env-vars`
- `scan-blocking-operations`
- `scan-http-requests`
- `scan-metrics`
- `scan-logging`
- `scan-concurrency-patterns`
- `scan-exception-handlers`
- `scan-unit-tests`
- `scan-django-urls`
- `scan-django-models`
- `scan-signals`
- `scan-django-settings`
- `scan-redis-usage`
- `scan-module-symbols`

## Shared test rules

- Only test the public CLI group (`upcast.main:main`)
- Prefer real tiny input trees over mocking scanner internals
- Keep assertions user-facing: exit code, stdout/stderr, output file creation, parsed YAML/JSON structure, option effects
- One phase = one commit
- Each phase must pass its pytest slice and `make check` before moving on

## Minimum behavior matrix per command

| Command                     | Minimum behavior to lock                                                                                 |
| --------------------------- | -------------------------------------------------------------------------------------------------------- |
| `main` group                | `--help` succeeds and lists all public commands                                                          |
| `scan-env-vars`             | YAML stdout, JSON file output, include/exclude filtering, invalid path / empty project behavior          |
| `scan-blocking-operations`  | YAML stdout, JSON file output, include/exclude filtering                                                 |
| `scan-http-requests`        | YAML stdout, JSON file output, include/exclude filtering                                                 |
| `scan-metrics`              | YAML stdout, JSON file output, include/exclude filtering                                                 |
| `scan-exception-handlers`   | YAML stdout, JSON file output, include/exclude filtering                                                 |
| `scan-concurrency-patterns` | YAML stdout, JSON file output, include/exclude filtering                                                 |
| `scan-complexity-patterns`  | YAML stdout, JSON file output, `--threshold` changes result set                                          |
| `scan-logging`              | YAML stdout, JSON file output, `--sensitive-keywords` affects output                                     |
| `scan-module-symbols`       | YAML stdout, JSON file output, `--include-private` affects output                                        |
| `scan-django-settings`      | YAML stdout, JSON file output, verbose completion text                                                   |
| `scan-signals`              | YAML stdout, JSON file output, include/exclude filtering                                                 |
| `scan-redis-usage`          | YAML stdout, JSON file output, verbose start/completion text                                             |
| `scan-django-urls`          | YAML stdout, JSON file output, pin current include/exclude CLI behavior                                  |
| `scan-django-models`        | YAML stdout, JSON file output, pin current include/exclude CLI behavior                                  |
| `scan-unit-tests`           | YAML stdout, JSON file output, `--root-modules` affects output, pin current include/exclude CLI behavior |

## File rollout

Modify:

- `tests/test_cli/test_main.py`

Create:

- `tests/test_cli/test_scan_env_vars.py`
- `tests/test_cli/test_scan_blocking_operations.py`
- `tests/test_cli/test_scan_http_requests.py`
- `tests/test_cli/test_scan_metrics.py`
- `tests/test_cli/test_scan_exception_handlers.py`
- `tests/test_cli/test_scan_concurrency_patterns.py`
- `tests/test_cli/test_scan_complexity_patterns.py`
- `tests/test_cli/test_scan_logging.py`
- `tests/test_cli/test_scan_module_symbols.py`
- `tests/test_cli/test_scan_django_settings.py`
- `tests/test_cli/test_scan_signals.py`
- `tests/test_cli/test_scan_redis_usage.py`
- `tests/test_cli/test_scan_django_urls.py`
- `tests/test_cli/test_scan_django_models.py`
- `tests/test_cli/test_scan_unit_tests.py`

## Phase plan

### Phase 1: public surface + env vars

**Files:**

- Modify: `tests/test_cli/test_main.py`
- Create: `tests/test_cli/test_scan_env_vars.py`

**Behavior to lock:**

- `main --help` lists all 15 public commands
- `scan-env-vars` YAML stdout
- `scan-env-vars --format json --output ...`
- `scan-env-vars` include/exclude filtering
- parser-level invalid path failure
- runtime empty-project failure

**Verification:**

- `uv run pytest tests/test_cli/test_main.py tests/test_cli/test_scan_env_vars.py -q`
- `make check`

**Commit:**

- `test(cli): lock main command surface and env var command`

### Phase 2: shared-flow core commands

**Files:**

- `tests/test_cli/test_scan_blocking_operations.py`
- `tests/test_cli/test_scan_http_requests.py`
- `tests/test_cli/test_scan_metrics.py`
- `tests/test_cli/test_scan_exception_handlers.py`
- `tests/test_cli/test_scan_concurrency_patterns.py`

**Behavior to lock:**

- default YAML stdout
- JSON file output
- include/exclude filtering
- one minimal semantic assertion per command

**Verification:**

- `uv run pytest tests/test_cli/test_scan_blocking_operations.py tests/test_cli/test_scan_http_requests.py tests/test_cli/test_scan_metrics.py tests/test_cli/test_scan_exception_handlers.py tests/test_cli/test_scan_concurrency_patterns.py -q`
- `make check`

**Commit:**

- `test(cli): lock shared-flow core scanner commands`

### Phase 3: unique-option commands

**Files:**

- `tests/test_cli/test_scan_complexity_patterns.py`
- `tests/test_cli/test_scan_logging.py`
- `tests/test_cli/test_scan_module_symbols.py`

**Behavior to lock:**

- `scan-complexity-patterns`: `--threshold`
- `scan-logging`: `--sensitive-keywords`
- `scan-module-symbols`: `--include-private`
- default YAML and JSON output in each file

**Verification:**

- `uv run pytest tests/test_cli/test_scan_complexity_patterns.py tests/test_cli/test_scan_logging.py tests/test_cli/test_scan_module_symbols.py -q`
- `make check`

**Commit:**

- `test(cli): lock unique option scanner commands`

### Phase 4: custom-behavior infra / Django commands

**Files:**

- `tests/test_cli/test_scan_django_settings.py`
- `tests/test_cli/test_scan_signals.py`
- `tests/test_cli/test_scan_redis_usage.py`

**Behavior to lock:**

- YAML stdout
- JSON file output
- current verbose side effects for each command

**Verification:**

- `uv run pytest tests/test_cli/test_scan_django_settings.py tests/test_cli/test_scan_signals.py tests/test_cli/test_scan_redis_usage.py -q`
- `make check`

**Commit:**

- `test(cli): lock settings, signals, and redis commands`

### Phase 5: filter-quirk commands

**Files:**

- `tests/test_cli/test_scan_django_urls.py`
- `tests/test_cli/test_scan_django_models.py`
- `tests/test_cli/test_scan_unit_tests.py`

**Behavior to lock:**

- YAML stdout
- JSON file output
- current include/exclude CLI behavior as exposed today
- `scan-unit-tests --root-modules` behavior

**Verification:**

- `uv run pytest tests/test_cli/test_scan_django_urls.py tests/test_cli/test_scan_django_models.py tests/test_cli/test_scan_unit_tests.py -q`
- `make check`

**Commit:**

- `test(cli): lock django urls, django models, and unit test commands`

### Phase 6: full sweep

**Verification:**

- `uv run pytest tests/test_cli -q`
- `make check`

**Commit:**

- only if a final test-only fix is needed

## Execution rules

For every phase:

1. Add/expand tests first
2. Run the phase pytest slice
3. Fix only test issues or proven testability blockers
4. Run `make check`
5. Commit only that phase’s files

## Success criteria

- Every public command in `upcast/main.py` has direct functional coverage under `tests/test_cli/`
- Tests invoke `upcast.main:main`, not private scanner CLIs
- Every phase passes its pytest slice and `make check`
- History stays phase-based and atomic
- `uv run pytest tests/test_cli -q` passes at the end
