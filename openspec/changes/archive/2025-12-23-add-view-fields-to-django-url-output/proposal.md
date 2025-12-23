# Proposal: Add View Fields to Django URL Scanner Output

## Problem Statement

The Django URL scanner's YAML output is missing critical `view_module` and `view_name` fields that are defined in the data model but never appear in the actual output. These fields are essential for:

1. **Understanding which views handle each URL pattern** - Without view information, users cannot determine which Python code handles a given URL
2. **Tracing request flows** - Migration analysis requires knowing the view function/class to understand application behavior
3. **Impact analysis** - When refactoring views, developers need to know which URLs are affected

### Current Behavior

Looking at `example/scan-results/django-urls.yaml`, every URL pattern entry lacks view information:

```yaml
- converters: []
  is_conditional: false
  is_partial: false
  name: wl_api.process_spec_plan
  named_groups: []
  pattern: wl_api/platform/process_spec_plan/
  type: path
```

The spec explicitly requires these fields:

> **Scenario: Format route entries**
>
> - `view_module`: Full module path of view (if resolved)
> - `view_name`: Function or class name

### Root Cause

The issue has two parts:

1. **View resolution may be failing** - The `resolve_view()` function returns `None` for `view_module` and `view_name` when inference fails
2. **Pydantic excludes None values** - Even when resolution succeeds, Pydantic's default serialization behavior excludes `None` values from YAML output

## Proposed Solution

### 1. Always Include View Fields in Output

Modify the `UrlPattern` model to always include `view_module` and `view_name` fields in output, even when `None`. This provides explicit indication of resolution status.

**Implementation**: Configure Pydantic model to exclude None fields optionally, not globally.

### 2. Improve View Resolution Success Rate

Enhance the `resolve_view()` function to handle more cases:

- Add fallback extraction from import statements when astroid inference fails
- Extract view names from Call nodes even when full module path cannot be resolved
- Handle Django's common view patterns (CBV mixins, decorators)

### 3. Add Resolution Status Field

Add an optional `view_resolved` boolean field to indicate whether view resolution succeeded, helping users distinguish between:

- Views that couldn't be resolved (technical limitation)
- Include/router patterns that legitimately have no view

## Success Criteria

1. **View fields always present**: Every path/re_path pattern in output includes `view_module` and `view_name` fields
2. **Resolution rate > 80%**: At least 80% of URL patterns should have non-null view information on real-world codebases like blueking-paas
3. **Clear status indication**: Users can easily distinguish between unresolved views and non-view patterns (includes, routers)
4. **Backward compatible**: Existing parsers continue to work with the enhanced output

## Impact Assessment

- **Breaking Changes**: None - this adds missing fields, doesn't remove or rename existing fields
- **Affected Components**:
  - `upcast/models/django_urls.py` - UrlPattern model
  - `upcast/common/django/view_resolver.py` - View resolution logic
  - `example/scan-results/django-urls.yaml` - Baseline will show new fields
- **Testing Requirements**:
  - Unit tests for view resolution edge cases
  - Integration test to verify field presence in output
  - Measure resolution success rate on blueking-paas

## Implementation Approach

1. **Phase 1**: Fix output serialization (ensure fields always appear)
2. **Phase 2**: Improve resolution logic (increase success rate)
3. **Phase 3**: Update integration test baseline and validate

## Alternatives Considered

1. **Leave as-is, document limitation**: Rejected - missing view info defeats the purpose of scanning URLs
2. **Add separate "unresolved views" report**: Rejected - should be in main output for completeness
3. **Use placeholder values like `<unknown>`**: Rejected - None is more explicit and allows filtering

## Open Questions

1. Should we add a `view_description` field for docstrings as the spec mentions?
2. Should we track resolution failures in summary statistics?
3. Should we support configuration to skip view resolution for performance?
