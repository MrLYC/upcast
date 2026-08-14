## Context

The existing Django URL scanner resolves direct view references and records DRF Router registrations, but it is intentionally URLconf-oriented. It cannot provide a durable audit record for view internals: inherited framework type, action-level overrides, model evidence, permission implementation references, or the distinction between explicit evidence and failed static inference.

The new capability must remain useful on projects with custom security layers without hard-coding project-specific decorator semantics. It must also avoid changing the existing URL scanner output merely to attach deeper details.

## Goals / Non-Goals

### Goals

- Provide a standalone `scan-django-views` command that scans all eligible Python files by default.
- Identify views from resolved Django/DRF framework semantics and confirmed route references, not filename conventions or short-name guesses.
- Provide exact, source-located evidence for routes, security controls, permission definitions, model use, and uncertainty.
- Support reverse linking to direct routes and mounted DRF Router registrations while retaining a separate URL command/output.
- Preserve raw expressions where custom behavior cannot be statically classified.

### Non-Goals

- Do not expand arbitrary call graphs, execute Django, import application modules, or claim runtime reachability.
- Do not synthesize complete Router URL strings or claim that unmounted registrations are endpoints.
- Do not add a project-specific decorator mapping file or encode project-specific security conventions.
- Do not modify the public `scan-django-urls` result schema.

## Decisions

### Decision: Keep views and URLs as separate scanner contracts

`scan-django-views` owns analysis of view internals. `scan-django-urls` remains the URLconf report. Both use a canonical resolved target made from module and symbol/qualified name; route references in the new report make the relationship inspectable without embedding view details into URL output.

### Decision: Use semantic detection with route-reference fallback

Classes are confirmed only when their resolved ancestor chain reaches a known Django/DRF view base. Functions are confirmed when they use a known DRF function-view decorator or are a confirmed direct URL target. Filename conventions can never be proof; they only influence user-supplied include/exclude filtering.

### Decision: Keep three-state evidence

Every resolution-sensitive finding carries `confirmed`, `partial`, or `unknown`. A failed inference retains the raw expression and source location. This prevents static-analysis gaps from becoming false security claims.

### Decision: Build a shared internal route-reference index

The index parses direct `path()`/`re_path()` targets, Router creation, `register()` calls, and `router.urls` mounts in both `include(router.urls)` and direct `urlpatterns = router.urls` forms. A registration becomes a confirmed route reference only after a mount is found; otherwise it remains an unmounted candidate. The index reuses existing URL/view/router parsing concepts but is not a new public command or a change to the URL scanner's serialized schema.

### Decision: Model ViewSets at action granularity

A ViewSet has a parent record plus nested action records. Explicit `@action` data captures HTTP methods, detail scope, optional route metadata, and action-level security/model overrides. Standard CRUD actions are inferred only for confirmed compatible DRF bases and are marked `framework_derived`.

### Decision: Separate authentication, authorization, and CSRF

The report does not equate `AllowAny` with a Django login exemption, and it does not equate `csrf_exempt` with either. Local declarations, inherited declarations, action overrides, and statically resolvable DRF defaults are preserved with precedence/evidence. Middleware and custom decorators that cannot be proven retain raw signals and an unknown/conditional status.

### Decision: Bound permission and model analysis

Permission expressions retain their boolean structure. Referenced permissions are followed one hop to their class/function definition and `has_permission`/`has_object_permission` methods, but their downstream calls are not recursively interpreted. Model evidence is limited to view declarations, direct ORM operations, and serializer `Meta.model`; custom managers, services, and dynamic model selection remain unknown evidence.

## Data Flow

1. Collect Python files through `BaseScanner` filters and parse modules once.
2. Build a module/symbol index and route-reference index.
3. Discover confirmed/partial/unknown view candidates and construct canonical IDs.
4. Enrich each candidate/action with security, permission, and model evidence.
5. Produce stable typed output ordered by canonical view ID and source location.

## Output Shape

Top-level results are keyed by canonical view ID. A view contains its recognition evidence, route references, security sections, model usages, and nested actions. Each evidence item includes a source location, raw expression, resolved qualified name when available, source kind, and status. This allows downstream tools to perform custom mappings without modifying scanner configuration.

## Risks / Trade-offs

- Astroid inference can be incomplete on framework-heavy projects. The three-state model and raw evidence mitigate loss of audit information.
- DRF Router behavior varies for custom routers. The implementation will report registration/mount evidence but will not fabricate concrete generated URLs.
- Permission semantics can be arbitrarily dynamic. One-hop references are informative without pretending to prove authorization behavior.
- Scanning all Python files costs more than convention-only scanning, but it avoids missing views located outside `views.py`; normal file filters remain available to narrow scope.

## Verification Strategy

- Use only synthetic, generic test fixtures in the repository.
- Cover direct and unresolved functions, CBVs, APIViews, ViewSets, custom actions, Router mount states, security precedence, raw unknown controls, permission references, serializer models, and direct ORM operation classifications.
- Verify CLI YAML/JSON output, filtering, help text, stable ordering, and no regression in existing Django URL tests.
- If out-of-repository manual validation is performed, do not commit its source, paths, output, counts, or project-specific mappings.
