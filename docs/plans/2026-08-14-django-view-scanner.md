# Django View Scanner Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add `scan-django-views`, a typed static-analysis command that reports Django/DRF views, actions, route evidence, security controls, permission references, and direct model use without changing `scan-django-urls` output.

**Architecture:** Add focused Pydantic output models and a `DjangoViewScanner` on the existing `BaseScanner` boundary. Build semantic view discovery and a reusable internal route-reference index from parsed astroid modules, then enrich confirmed/partial candidates with bounded security, permission, and model evidence. Preserve unresolved expressions as evidence instead of treating them as negative results.

**Tech Stack:** Python, astroid, Pydantic v2, Click, PyYAML, pytest, `click.testing.CliRunner`, Ruff, OpenSpec.

---

## Scope gate before coding

Do not start production code until `openspec validate add-django-view-scanner --strict` passes and the implementation is explicitly authorized. Review `openspec/changes/add-hybrid-scan-pipeline/` first: use its shared candidate pipeline only if its contract is accepted and available; the Django-view behavior must retain an AST fallback and must not block on that migration.

Repository tests must use only synthetic fixtures. Do not add any external-project source, absolute path, result snapshot, count, or project-specific security mapping to the repository.

### Task 1: Establish typed output contracts

**Files:**

- Create: `upcast/models/django_views.py`
- Modify: `upcast/models/__init__.py` only if imports are intentionally re-exported
- Create: `tests/test_django_views_scanner/test_models.py`

**Step 1: Write the failing model tests**

Create tests that construct and validate these minimum shapes:

```python
assert DjangoViewOutput(
    summary=DjangoViewSummary(total_count=1, files_scanned=1, scan_duration_ms=0, total_views=1),
    results={"pkg.views.HealthView": view},
    metadata={"scanner_name": "django-views"},
).results["pkg.views.HealthView"].recognition.status == "confirmed"
```

Cover `SourceEvidence`, route references, raw security signals, permission expression nodes, model usages, ViewSet actions, required/optional fields, and deterministic list defaults.

**Step 2: Run the test to verify it fails**

Run: `uv run pytest tests/test_django_views_scanner/test_models.py -q`

Expected: FAIL because `upcast.models.django_views` does not exist.

**Step 3: Implement the smallest models**

Define `ResolutionStatus` (`confirmed`, `partial`, `unknown`), source/evidence records, security sections, `DjangoViewAction`, `DjangoView`, `DjangoViewSummary`, and `DjangoViewOutput`. Make all absent scalar facts `T | None`; make collections required/default-factory only when a scanner always supplies them.

**Step 4: Run the focused tests**

Run: `uv run pytest tests/test_django_views_scanner/test_models.py -q`

Expected: PASS.

**Step 5: Commit**

```bash
git add upcast/models/django_views.py upcast/models/__init__.py tests/test_django_views_scanner/test_models.py
git commit -m "feat: add django view output models"
```

### Task 2: Implement semantic view discovery

**Files:**

- Create: `upcast/common/django/view_discovery.py`
- Create: `tests/test_django_views_scanner/test_view_discovery.py`
- Create: `tests/test_django_views_scanner/fixtures/views.py`

**Step 1: Write the failing discovery tests**

Use a synthetic module containing a direct Django CBV, DRF APIView, ModelViewSet, `@api_view` function, plain helper function, and unresolved custom base/decorator. Assert that only semantic framework candidates are confirmed before route fallback, and that uncertain expressions survive as raw evidence.

**Step 2: Run the test to verify it fails**

Run: `uv run pytest tests/test_django_views_scanner/test_view_discovery.py -q`

Expected: FAIL because the discovery helper does not exist.

**Step 3: Implement the minimal recognizer**

Implement helpers equivalent to:

```python
def discover_views(module: nodes.Module, context: DiscoveryContext) -> list[DiscoveredView]:
    # Resolve ancestor/decorator qnames first.
    # Return confirmed, partial, or unknown findings with SourceEvidence.
    # Never promote a candidate solely because of its filename or short name.
```

Use resolved Django/DRF qualified base names, with a raw-expression fallback only for evidence. Generate canonical IDs from the resolved module and qualified symbol.

**Step 4: Run focused tests**

Run: `uv run pytest tests/test_django_views_scanner/test_view_discovery.py tests/test_django_views_scanner/test_models.py -q`

Expected: PASS.

**Step 5: Commit**

```bash
git add upcast/common/django/view_discovery.py tests/test_django_views_scanner
git commit -m "feat: discover django view candidates semantically"
```

### Task 3: Add the internal route-reference index

**Files:**

- Create: `upcast/common/django/route_index.py`
- Modify: `upcast/common/django/router_parser.py` only to extract reusable non-breaking helpers
- Modify: `upcast/common/django/view_resolver.py` only to expose reusable resolved/raw target evidence without changing URL output
- Create: `tests/test_django_views_scanner/test_route_index.py`
- Create: `tests/test_django_views_scanner/fixtures/urls.py`
- Test: `tests/test_django_urls_scanner/test_drf_routers.py`

**Step 1: Write failing route-index tests**

Cover:

- direct `path("x/", views.handler)` and `re_path()` resolution;
- `router.register("items", ItemViewSet, basename="item")` plus `include(router.urls)`;
- `urlpatterns = router.urls`;
- a registration with no mount, which must remain unmounted;
- unresolved view/router expressions, which must remain raw unknown evidence.

**Step 2: Run the test to verify it fails**

Run: `uv run pytest tests/test_django_views_scanner/test_route_index.py -q`

Expected: FAIL because the route index does not exist.

**Step 3: Implement the minimal index**

Create a typed internal index that associates a canonical target with records like:

```python
RouteReference(
    kind="router",
    status="confirmed",
    prefix="items",
    basename="item",
    target_id="pkg.views.ItemViewSet",
    evidence=[registration_evidence, mount_evidence],
)
```

Reuse URL/router resolution logic where possible. Treat a Router registration as confirmed only after a matching `.urls` mount is found. Do not generate concrete DRF URLs and do not alter `DjangoUrlOutput` serialization.

**Step 4: Run focused regression tests**

Run: `uv run pytest tests/test_django_views_scanner/test_route_index.py tests/test_django_urls_scanner/test_drf_routers.py tests/test_django_urls_scanner/test_integration.py -q`

Expected: PASS.

**Step 5: Commit**

```bash
git add upcast/common/django/route_index.py upcast/common/django/router_parser.py upcast/common/django/view_resolver.py tests/test_django_views_scanner
git commit -m "feat: index django view route references"
```

### Task 4: Extract ViewSet actions and local security evidence

**Files:**

- Create: `upcast/common/django/view_security.py`
- Modify: `upcast/common/django/view_discovery.py`
- Create: `tests/test_django_views_scanner/test_actions_and_security.py`
- Create: `tests/test_django_views_scanner/fixtures/security_views.py`

**Step 1: Write failing action/security tests**

Cover a confirmed ViewSet with class-level `authentication_classes` and `permission_classes`, an explicit `@action(methods=["post"], detail=True, permission_classes=[...])`, `AllowAny`, `csrf_exempt`, a standard Django `login_required`, and a custom undecidable decorator. Assert separate authentication/authorization/CSRF sections, override precedence, raw unknown signals, and no false login-exempt classification.

**Step 2: Run the test to verify it fails**

Run: `uv run pytest tests/test_django_views_scanner/test_actions_and_security.py -q`

Expected: FAIL because action/security extraction does not exist.

**Step 3: Implement bounded action/security extraction**

Implement explicit decorator parsing and a small standard-framework semantic table. Produce nested action records for explicit `@action`; add framework-derived CRUD actions only after a resolved compatible DRF base. Preserve all decorators/class attributes as raw `SourceEvidence` even when their semantic category is unknown.

**Step 4: Run focused tests**

Run: `uv run pytest tests/test_django_views_scanner/test_actions_and_security.py tests/test_django_views_scanner/test_view_discovery.py -q`

Expected: PASS.

**Step 5: Commit**

```bash
git add upcast/common/django/view_security.py upcast/common/django/view_discovery.py tests/test_django_views_scanner
git commit -m "feat: analyze django view actions and security evidence"
```

### Task 5: Resolve DRF defaults and permission definitions one hop

**Files:**

- Create: `upcast/common/django/permission_resolver.py`
- Modify: `upcast/common/django/view_security.py`
- Create: `tests/test_django_views_scanner/test_permissions.py`
- Create: `tests/test_django_views_scanner/fixtures/permissions.py`
- Create: `tests/test_django_views_scanner/fixtures/settings.py`

**Step 1: Write failing permission tests**

Assert that:

- a statically defined `REST_FRAMEWORK` default participates only when no nearer declaration exists;
- `A | B` and `A & B` retain their expression structure;
- resolved permission classes report definition and `has_permission`/`has_object_permission` evidence;
- a superclass/service call stays unknown rather than recursively expanded.

**Step 2: Run the test to verify it fails**

Run: `uv run pytest tests/test_django_views_scanner/test_permissions.py -q`

Expected: FAIL because default/permission resolution is unavailable.

**Step 3: Implement one-hop resolution**

Represent permission expressions as a raw string plus a typed expression tree only when operators/names can be resolved safely. Resolve referenced definitions once; collect base qnames, source locations, docstrings, and directly declared check methods. Do not infer business authorization from arbitrary calls.

**Step 4: Run focused tests**

Run: `uv run pytest tests/test_django_views_scanner/test_permissions.py tests/test_django_views_scanner/test_actions_and_security.py -q`

Expected: PASS.

**Step 5: Commit**

```bash
git add upcast/common/django/permission_resolver.py upcast/common/django/view_security.py tests/test_django_views_scanner
git commit -m "feat: resolve django view permission evidence"
```

### Task 6: Extract model usage and operation categories

**Files:**

- Create: `upcast/common/django/view_model_usage.py`
- Create: `tests/test_django_views_scanner/test_model_usage.py`
- Create: `tests/test_django_views_scanner/fixtures/model_views.py`

**Step 1: Write failing model-use tests**

Cover `queryset = Order.objects.all()`, `model = Order`, `serializer_class = OrderSerializer` with `Meta.model`, direct `Order.objects.filter()`, `Order.objects.create()`, `Order.objects.filter().delete()`, and dynamic/custom-manager expressions. Assert source roles and `read`, `write`, `delete`, `read_write`, or `unknown` classifications.

**Step 2: Run the test to verify it fails**

Run: `uv run pytest tests/test_django_views_scanner/test_model_usage.py -q`

Expected: FAIL because model-use extraction is unavailable.

**Step 3: Implement conservative extraction**

Recognize only direct ORM/model/serializer forms. Keep a small explicit operation table; classify `get_or_create` and `update_or_create` as `read_write`; never inspect custom manager/service method bodies to fabricate a model relationship.

**Step 4: Run focused tests**

Run: `uv run pytest tests/test_django_views_scanner/test_model_usage.py tests/test_django_views_scanner/test_models.py -q`

Expected: PASS.

**Step 5: Commit**

```bash
git add upcast/common/django/view_model_usage.py tests/test_django_views_scanner
git commit -m "feat: report django view model usage"
```

### Task 7: Assemble the scanner and test cross-file behavior

**Files:**

- Create: `upcast/scanners/django_views.py`
- Modify: `upcast/scanners/__init__.py`
- Create: `tests/test_django_views_scanner/conftest.py`
- Create: `tests/test_django_views_scanner/test_integration.py`

**Step 1: Write the failing integration test**

Create a temporary synthetic package with separate URL, view, serializer, permission, model, and settings modules. Assert a direct function route and a mounted ViewSet route link to the expected canonical records; assert action-level evidence survives and results are source-sorted.

**Step 2: Run the test to verify it fails**

Run: `uv run pytest tests/test_django_views_scanner/test_integration.py -q`

Expected: FAIL because `DjangoViewScanner` is not importable.

**Step 3: Implement scanner orchestration**

Implement `DjangoViewScanner(BaseScanner[DjangoViewOutput])`. Use `BaseScanner` default `**/*.py` behavior, parse all eligible files once, build indexes, enrich records, calculate summary fields, and return metadata `{"scanner_name": "django-views"}`. Preserve parse errors/unknown evidence through verbose logging rather than aborting the scan.

**Step 4: Run scanner tests**

Run: `uv run pytest tests/test_django_views_scanner -q`

Expected: PASS.

**Step 5: Commit**

```bash
git add upcast/scanners/django_views.py upcast/scanners/__init__.py tests/test_django_views_scanner
git commit -m "feat: add django view scanner"
```

### Task 8: Expose and verify the CLI

**Files:**

- Modify: `upcast/main.py`
- Modify: `tests/test_cli/test_main.py`
- Create: `tests/test_cli/test_scan_django_views.py`

**Step 1: Write failing CLI tests**

Use `CliRunner` with a synthetic project. Cover default YAML, JSON output file, include/exclude filtering, empty-project handling, and `--help` examples:

```python
result = runner.invoke(main, ["scan-django-views", str(project_dir)])
assert result.exit_code == 0
assert yaml.safe_load(result.output)["metadata"]["scanner_name"] == "django-views"
```

**Step 2: Run the test to verify it fails**

Run: `uv run pytest tests/test_cli/test_scan_django_views.py tests/test_cli/test_main.py -q`

Expected: FAIL because the Click command is not registered.

**Step 3: Implement command wiring**

Follow the `scan-django-urls` Click option pattern, constructing `DjangoViewScanner` and calling `run_scanner_cli`. Add concise help text stating semantic discovery and include/exclude narrowing; do not add custom semantic-mapping options.

**Step 4: Run CLI tests**

Run: `uv run pytest tests/test_cli/test_scan_django_views.py tests/test_cli/test_main.py -q`

Expected: PASS.

**Step 5: Commit**

```bash
git add upcast/main.py tests/test_cli/test_main.py tests/test_cli/test_scan_django_views.py
git commit -m "feat: expose django view scan command"
```

### Task 9: Document and perform final verification

**Files:**

- Create: `docs/scanners/django-views.md`
- Modify: `docs/README.md`
- Modify: `README.md`
- Modify: `openspec/changes/add-django-view-scanner/tasks.md`

**Step 1: Write documentation using only synthetic examples**

Document command usage, output fields, evidence statuses, route-reference limits, security separation, model operation labels, and the fact that custom controls remain raw signals.

**Step 2: Run targeted verification**

Run:

```bash
uv run pytest tests/test_django_views_scanner tests/test_cli/test_scan_django_views.py tests/test_cli/test_main.py tests/test_django_urls_scanner -q
uv run --extra dev ruff check upcast/models/django_views.py upcast/scanners/django_views.py upcast/common/django tests/test_django_views_scanner tests/test_cli/test_scan_django_views.py
openspec validate add-django-view-scanner --strict
```

Expected: all commands PASS. If any existing URL test fails, stop and restore URL behavior before marking work complete.

**Step 3: Perform optional non-persistent manual validation**

If a larger local codebase is used, inspect results interactively only. Do not add its path, source, output, counts, expected results, or project-specific rule to the repository.

**Step 4: Update the task checklist**

Mark only verified tasks complete; leave anything not actually executed unchecked.

**Step 5: Commit**

```bash
git add docs/scanners/django-views.md docs/README.md README.md openspec/changes/add-django-view-scanner/tasks.md
git commit -m "docs: document django view scanner"
```

## Completion Criteria

- `scan-django-views` emits typed, stable records for confirmed/partial/unknown view evidence.
- Direct routes and mounted Router registrations are linked without changing `scan-django-urls` output.
- ViewSet actions, security evidence, one-hop permission references, and direct model usage follow the confirmed design boundaries.
- Tests are synthetic and contain no external-project artifacts.
- CLI, focused scanner tests, existing Django URL tests, lint, and strict OpenSpec validation pass.
