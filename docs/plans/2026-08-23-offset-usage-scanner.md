# Offset Usage Scanner Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a static `scan-offset-usage` command that finds common Django ORM/DRF and raw-SQL patterns capable of producing costly SQL `OFFSET` pagination.

**Architecture:** Add Pydantic models for parameter evidence and offset findings, then implement an import-aware Astroid scanner that recognizes QuerySet slices, Django/DRF paginator declarations and page calls, and SQL text containing offset clauses. Register the scanner through the existing `run_scanner_cli` path and document that results are source evidence rather than runtime query-plan measurements.

**Tech Stack:** Python, Astroid, Pydantic, Click, pytest, Ruff, mypy, OpenSpec.

---

### Task 1: Approve and validate the OpenSpec change

**Files:**

- Create: `openspec/changes/add-offset-usage-scanner/proposal.md`
- Create: `openspec/changes/add-offset-usage-scanner/design.md`
- Create: `openspec/changes/add-offset-usage-scanner/tasks.md`
- Create: `openspec/changes/add-offset-usage-scanner/specs/offset-usage-scanner/spec.md`
- Create: `openspec/changes/add-offset-usage-scanner/specs/cli-interface/spec.md`
- Create: `openspec/changes/add-offset-usage-scanner/specs/data-models/spec.md`
- Create: `openspec/changes/add-offset-usage-scanner/specs/scanner-architecture/spec.md`

**Step 1: Validate the proposal**

Run: `openspec validate add-offset-usage-scanner --strict`

Expected: the change is valid.

**Step 2: Obtain approval before implementation**

Confirm the supported pattern scope and command name with the user before writing production code.

### Task 2: Write failing model tests

**Files:**

- Create: `tests/test_offset_usage_scanner/test_models.py`

**Step 1: Write tests**

Cover parameter hardcoded states, finding pattern/framework fields, nullable evidence, summary counts, and the shared output shape.

**Step 2: Run the focused tests**

Run: `uv run pytest -q tests/test_offset_usage_scanner/test_models.py`

Expected: FAIL because the new models do not exist.

### Task 3: Implement the typed models

**Files:**

- Create: `upcast/models/offset_usage.py`
- Modify: `upcast/models/__init__.py`

**Step 1: Implement the smallest model surface required by the failing tests**

Define parameter evidence, offset usage, summary, and output models using the shared scanner base models.

**Step 2: Re-run model tests**

Run: `uv run pytest -q tests/test_offset_usage_scanner/test_models.py`

Expected: PASS.

### Task 4: Write failing scanner tests

**Files:**

- Create: `tests/test_offset_usage_scanner/test_integration.py`
- Create: `tests/test_offset_usage_scanner/fixtures/offset_patterns.py`

**Step 1: Add source fixtures**

Cover QuerySet slices, computed page offsets, Django Paginator, DRF page/limit-offset declarations, raw SQL/RawSQL/cursor calls, aliases, dynamic values, zero offsets, ordinary list slices, and CursorPagination.

**Step 2: Run the focused tests**

Run: `uv run pytest -q tests/test_offset_usage_scanner/test_integration.py`

Expected: FAIL because the scanner does not exist.

### Task 5: Implement the static scanner

**Files:**

- Create: `upcast/scanners/offset_usage.py`
- Modify: `upcast/scanners/__init__.py`

**Step 1: Implement import-aware detection**

Use Astroid nodes and existing inference helpers to identify supported patterns, retain source expressions, classify hardcoded/dynamic values, and keep ordinary collection slices out.

**Step 2: Run scanner tests**

Run: `uv run pytest -q tests/test_offset_usage_scanner/test_integration.py`

Expected: PASS.

### Task 6: Integrate the CLI

**Files:**

- Create: `tests/test_cli/test_scan_offset_usage.py`
- Modify: `upcast/main.py`

**Step 1: Write failing CLI tests**

Cover help text, YAML stdout, JSON output, and include/exclude forwarding.

**Step 2: Register the command with the shared CLI helper**

Expose the standard scanner options and pass the scanner instance to `run_scanner_cli`.

**Step 3: Run CLI tests**

Run: `uv run pytest -q tests/test_cli/test_scan_offset_usage.py`

Expected: PASS.

### Task 7: Document and verify

**Files:**

- Create: `docs/scanners/offset-usage.md`
- Modify: `README.md`
- Modify: `docs/README.md`

**Step 1: Document supported patterns and limits**

Include command examples, output schema, examples of findings, exclusions, and the distinction between static evidence and runtime query plans.

**Step 2: Run validation**

Run: `uv run pytest -q`, targeted Ruff/format/type checks, `git diff --check`, and `openspec validate add-offset-usage-scanner --strict`.

Expected: all tests and checks pass.
