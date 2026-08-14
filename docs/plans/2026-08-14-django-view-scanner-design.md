# Django View Scanner Design

## Purpose

Add a focused `scan-django-views` command that complements `scan-django-urls`. It must show view internals needed for static security and impact analysis: view/action identity, route linkage, model use, authentication, authorization, CSRF, and evidence quality.

## Confirmed Product Decisions

- The first version is a standalone command. It does not add view internals to the public `scan-django-urls` output.
- Views are recognized by framework semantics and confirmed route references, not by a `views.py` filename convention.
- The scanner examines all Python files by default; existing include/exclude filtering remains the way to narrow scope.
- ViewSet output is action-aware. Explicit `@action` declarations and safely derived standard actions are distinct.
- A shared internal route index links direct routes and mounted Router registrations back to views. It does not synthesize complete Router URLs.
- Authentication, authorization, and CSRF are separate output concepts. `AllowAny` and `csrf_exempt` are never silently treated as login exemptions.
- Nonstandard decorators, authentication classes, and permission expressions are retained verbatim with source evidence. No custom semantic mapping file is part of v1.
- Referenced permission implementations are followed exactly one hop. Arbitrary service/IAM/call-graph traversal is out of scope.
- Model evidence covers view declarations, direct ORM calls, and resolvable serializer `Meta.model`; it includes conservative read/write/delete labels.
- Failed resolution is data, not omission: all uncertain findings carry `confirmed`, `partial`, or `unknown` plus raw expression/location evidence.

## Architecture

```text
eligible Python files
        |
        +--> parsed module/symbol index
        |          |
        |          +--> semantic view discovery
        |
        +--> internal URL/Router reference index
                       |
                       v
              canonical view/action records
                       |
                       +--> security and permission enrichment
                       +--> model-use enrichment
                       v
              DjangoViewOutput (YAML / JSON / Markdown)
```

The scanner builds the route index and symbol index before it finalizes candidate status. This lets a plain function become a confirmed view when a direct route resolves to it, while preventing a bare function in a convention-named file from becoming a false positive.

## Canonical Identity and Output

View results are keyed by fully qualified identity. Class actions append `#action`. Route references carry the corresponding resolved target identity, not a short-name heuristic.

```yaml
results:
  package.api.OrderViewSet:
    kind: drf_viewset
    recognition:
      status: confirmed
      evidence: []
    route_refs: []
    security:
      authentication: {}
      authorization: {}
      csrf: {}
      raw_signals: []
    model_usages: []
    actions: []
```

Every evidence record carries enough source information for another tool or reviewer to interpret custom project semantics later. The scanner reports facts and bounded inferences; it does not claim runtime access control behavior.

## DRF Router Rules

1. Discover supported Router variables and their creation evidence.
2. Record `register(prefix, ViewSet, basename)` calls with the resolved ViewSet target when possible.
3. Find Router `.urls` mounts through `include(router.urls)` or direct `urlpatterns = router.urls`.
4. Mark a registration as a confirmed route reference only when it has a mount. Otherwise retain it as an unmounted candidate.
5. Do not generate concrete URL templates for custom/default routers.

## Security and Model Rules

Security declarations retain scope and precedence: action/method overrides class declarations, which override statically resolvable DRF defaults. The scanner separately records authentication, authorization permission expressions, and CSRF. A custom decorator remains raw evidence unless it is a standard supported semantic marker.

Model use distinguishes queryset/model declarations, direct ORM calls, and serializer-derived models. Direct recognized operations receive a conservative category; dynamic expressions, custom managers, and service calls remain unknown rather than becoming guessed model access.

## Validation Boundaries

Repository tests use only small synthetic fixtures. They cover successful resolution, uncertainty preservation, Router mount states, action overrides, permission references, and ORM/model cases. Any optional manual validation outside this repository remains non-persistent: its source, paths, output, counts, and custom conventions are not copied into source, tests, documentation, or baselines.

## OpenSpec Relationship

The design is captured by OpenSpec change `add-django-view-scanner`. It is additive and preserves the current URL scanner's public contract. Before production work begins, implementation must review active changes, particularly shared scanner-pipeline work, and avoid coupling to an unapproved shared contract.
