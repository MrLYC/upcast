# Django URL Prefix Propagation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reconstruct complete Django URL paths across named `include()` boundaries so report `full_path` values represent mounted routes rather than only local URL fragments.

**Architecture:** Keep each URLconf's locally parsed `pattern` unchanged, then build a module graph from parsed `include_module` references after all files are scanned. Propagate every reachable parent prefix through that graph, clone patterns for distinct mount contexts, and retain local paths for unmounted or unresolved modules. Resolve exact module names plus explicitly configured source-root aliases, preserve unresolved Router sentinels, and avoid guessing ambiguous or external module references.

**Tech Stack:** Python, astroid, Pydantic models, pytest, Click CLI, YAML/CSV report generation.

---

### Task 1: Add a failing cross-module prefix regression test (completed)

**Files:**

- Modify: `tests/test_scanners/test_django_urls.py`

**Step 1: Write the failing test**

Create a temporary project with a parent `urls.py` that mounts a child `child/urls.py` at `^api/`, and assert the child route keeps `pattern == "^users/$"` while its `full_path == "^api/users/$"`.

Also cover two parent mounts of the same child and a regex-only parent prefix `^`, so the expected behavior includes multiple complete paths and does not produce `^/^users/$`.

**Step 2: Run the focused test**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -p no:cacheprovider -q tests/test_scanners/test_django_urls.py -k cross_module_prefix
```

Expected: FAIL because the current scanner returns the child-local path.

### Task 2: Implement generic URLconf graph propagation (completed)

**Files:**

- Modify: `upcast/scanners/django_urls.py`
- Possibly modify: `upcast/models/django_urls.py` only if metadata needs to document mount-context duplication

**Step 1: Build local URL modules first**

Preserve the current per-file extraction and local `pattern` values. After scanning, collect include edges from `UrlPattern(type="include")` records.

**Step 2: Resolve include targets safely**

Build exact module aliases and configurable source-root aliases (default `src`) for scanned module paths. Resolve an include only when one scanned module matches; leave external, dynamic, relative-unresolved, and ambiguous includes as local records. Keep unresolved DRF Router includes distinct from ordinary `module.urls` includes.

**Step 3: Propagate mount contexts**

Traverse from modules without incoming edges and from otherwise unvisited modules. For each `(module, prefix)` context, clone local patterns with a joined `full_path`; enqueue child modules with the include record's complete prefix. Preserve multiple distinct prefixes for modules mounted more than once and guard cycles.

Apply a configurable per-module mount-context limit and fail explicitly before producing partial output if the limit is exceeded.

**Step 4: Join regex and path fragments correctly**

Keep the regex anchor `^` once, remove a child-leading anchor when a parent prefix already supplies the route start, preserve trailing slashes, and never remove meaningful regex content.

### Task 3: Verify scanner compatibility (completed)

**Files:**

- Modify: `tests/test_scanners/test_django_urls.py` as needed for existing inline/router behavior
- Modify: `tests/test_cli/test_scan_django_urls.py` only if CLI counts intentionally change

**Step 1: Run focused scanner tests**

Run the new regression tests plus existing Django URL tests.

**Step 2: Run the full test suite and lint**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -p no:cacheprovider -q
RUFF_CACHE_DIR=/tmp/upcast-ruff-cache-url-prefix .venv/bin/ruff check upcast/scanners/django_urls.py tests/test_scanners/test_django_urls.py
git diff --check
```

### Task 4: Regenerate and independently validate Kingeye outputs (completed)

**Files:**

- Generate: `/home/liuyicong/udisk/tmp/kingeye/urls.yaml`
- Reuse unchanged: `/home/liuyicong/udisk/tmp/kingeye/views.yaml`
- Generate: `/home/liuyicong/udisk/tmp/kingeye/django-report.csv`
- Generate: `/home/liuyicong/udisk/tmp/django-login-exempt-summary.csv`

**Step 1: Rescan URL and view data**

Run the URL scanner and `merge-django-report` against the Kingeye repository. The view scanner is unchanged; reuse its existing `views.yaml` because a fresh full view scan is substantially slower than the URL-only change being verified.

**Step 2: Rebuild the three-column summary**

Aggregate all source reports by immediate directory name, retain non-empty `full_path` rows, and normalize only `True/TRUE` to `TRUE` in `login_exempt`.

**Step 3: Independently verify route composition**

Check known source chains such as `klc/urls.py` → `log_search/urls.py`, assert complete paths like `^api/v1/log/search/operators/$`, ensure no child route remains only `^search/operators/$`, and report unresolved/external includes separately.

### Task 5: Review the final diff and hand off (completed)

**Step 1: Inspect changed files and generated counts**

Confirm no unrelated repository-specific logic was added, the source report verification has no new mismatches, and the generated summary has no blank `full_path` values.

**Step 2: Report results**

Provide the fix summary, test evidence, regenerated file links, and any remaining ambiguity caused by multiple Kingeye `ROOT_URLCONF` entry points.
