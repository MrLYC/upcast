## 1. Specification and Scope Gate

- [ ] 1.1 Re-read this proposal/design and `openspec/specs/{cli-interface,common-utilities}/spec.md` before implementation.
- [ ] 1.2 Validate `add-django-view-scanner` with `openspec validate add-django-view-scanner --strict`.
- [ ] 1.3 Check active OpenSpec changes for shared hybrid-pipeline conflicts before adding production code.
- [ ] 1.4 Obtain explicit approval to start production implementation; this proposal approval alone does not authorize it.

## 2. Typed Output and Foundational Evidence

- [ ] 2.1 Add failing model tests for canonical IDs, source evidence, three-state status, security sections, route references, model usage, actions, and summary counts.
- [ ] 2.2 Implement the smallest Pydantic model set under `upcast/models/django_views.py` that makes those tests pass.
- [ ] 2.3 Export/register new models only where project conventions require it and run the focused model tests.

## 3. View and Route Discovery

- [ ] 3.1 Add failing synthetic tests for semantic function/CBV/APIView/ViewSet recognition and unknown fallback evidence.
- [ ] 3.2 Implement view discovery using resolved ancestor/decorator evidence and canonical symbol IDs.
- [ ] 3.3 Add failing route-index tests for direct routes, `router.register`, mounted `include(router.urls)`, direct `urlpatterns = router.urls`, and unmounted registrations.
- [ ] 3.4 Implement the shared internal route-reference index with stable ordering and no public URL-output change.
- [ ] 3.5 Run focused discovery/index tests and existing Django URL tests.

## 4. Action, Security, Permission, and Model Enrichment

- [ ] 4.1 Add failing tests for explicit `@action`, framework-derived CRUD actions, and action-level overrides.
- [ ] 4.2 Implement bounded ViewSet action extraction and precedence-aware inheritance.
- [ ] 4.3 Add failing tests for separate authentication/authorization/CSRF evidence, DRF defaults, and raw unresolved signals.
- [ ] 4.4 Implement security evidence extraction without project-specific semantic mappings.
- [ ] 4.5 Add failing tests for permission expression trees and one-hop permission definition/check-method references.
- [ ] 4.6 Implement bounded permission resolution with graceful unknown results.
- [ ] 4.7 Add failing tests for queryset/model declarations, direct ORM operations, serializer `Meta.model`, and unresolved expressions.
- [ ] 4.8 Implement model-use extraction and conservative operation classification.

## 5. Scanner and CLI Integration

- [ ] 5.1 Add a failing scanner integration test covering cross-file view/route linking and stable output.
- [ ] 5.2 Implement `DjangoViewScanner` on `BaseScanner`, scanning all Python files by default.
- [ ] 5.3 Add failing CLI tests for YAML, JSON file output, include/exclude behavior, empty projects, and help text.
- [ ] 5.4 Register `scan-django-views` in `upcast.main` and `upcast.scanners`, then make the CLI tests pass.

## 6. Documentation and Verification

- [ ] 6.1 Add `docs/scanners/django-views.md` and update README/documentation indexes using synthetic examples only.
- [ ] 6.2 Run focused scanner/model/CLI tests, existing Django URL tests, and lint/type checks for changed files.
- [ ] 6.3 Re-run `openspec validate add-django-view-scanner --strict` and update this checklist only after real verification.
- [ ] 6.4 Commit implementation in small, reviewable units: models, route/discovery, enrichment, CLI/docs, and final verification.
