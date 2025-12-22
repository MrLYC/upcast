# fix-scanner-output-issues

**Status**: PROPOSED
**Created**: 2025-12-22
**Author**: AI Assistant

## Problem

Two critical scanners have output formatting bugs that make their results difficult to use:

### 1. Django Models Scanner - Missing Module Paths

The `scan-django-models` command produces model names with empty module prefixes, showing `.ModelName` instead of `module.path.ModelName`.

**Example from wagtail scan**:

```yaml
results:
  .AbstractCarouselItem: # ❌ Should be wagtail.contrib.typed_table_block.blocks.AbstractCarouselItem
    bases:
      - .AbstractLinkFields # ❌ Should include full module path
    module: "" # ❌ Empty module field
```

**Root Cause**: In `upcast/common/django/model_parser.py`, the `parse_model()` function extracts module path from `class_node.qname()`, but astroid's `qname()` only returns the class name when parsing files in isolation (not as part of a package).

**Impact**:

- Cannot determine which module/package a model belongs to
- Base class references are ambiguous
- Model qualified names lose context
- Results are not actionable for downstream tools

### 2. HTTP Requests Scanner - Poor URL Grouping

The `scan-http-requests` command groups all dynamic URLs into a single `unknown_url` category instead of attempting to normalize them.

**Example from wagtail scan**:

```yaml
results:
  unknown_url: # ❌ Should try to extract patterns
    usages:
      - statement: "Request(endpoint + '?' + urlencode(params))" # Should be "...?..."
      - statement: "requests.get(endpoint, params=params)" # Should be "..."
      - statement: "requests.delete(purge_url, json=data)" # Should be "..."
```

**Expected Behavior** (from product context):

- Dynamic URL construction with string concatenation → use `...` placeholder
- URL with query params → use `...?...` pattern
- Only truly unresolvable URLs → group as `unknown_url`

**Root Cause**: In `upcast/scanners/http_requests.py`, the `_extract_url()` method only handles simple string literals via `safe_infer_value()`. It doesn't:

- Detect BinOp nodes (string concatenation with `+`)
- Recognize common URL construction patterns
- Identify variable references that should become `...`
- Detect query parameter additions

**Impact**:

- All dynamic URLs collapse into single group
- Cannot identify URL patterns across codebase
- No visibility into endpoint diversity
- Results have minimal analytical value

## Solution

### Phase 1: Fix Django Models Module Path Resolution

**Goal**: Derive module paths from file system structure relative to scan root.

**Implementation**:

1. Pass `root_path` through scanner → parser
2. Calculate relative module path: `(file_path - root_path - '.py').replace('/', '.')`
3. Handle special cases: `__init__.py` → parent dir name
4. Update `parse_model()` signature to accept and use `file_path` and `root_path`
5. Set `module` field to calculated path instead of extracting from `qname()`

**Files Changed**:

- `upcast/scanners/django_models.py`: Pass paths to parser
- `upcast/common/django/model_parser.py`: Accept paths, calculate module
- Tests: Update assertions for correct module paths

### Phase 2: Enhance HTTP URL Pattern Extraction

**Goal**: Normalize dynamic URLs into actionable patterns.

**Implementation**:

1. Add `_normalize_url_pattern()` method that:

   - Detects string concatenation (BinOp with `+` operator)
   - Replaces variable/Name nodes with `...`
   - Identifies query param patterns (`?` or `urlencode`) → `...?...`
   - Detects path param patterns (`/` + variable) → `.../...`
   - Returns normalized pattern or `None` if truly unknown

2. Update `_extract_url()` to:

   - First try literal inference (current behavior)
   - If that fails, call `_normalize_url_pattern()`
   - Only return `"unknown_url"` as last resort

3. Pattern Recognition Rules:
   - `url + path` or `base + endpoint` → `...`
   - `url + '?' + params` → `...?...`
   - `f"{base}/api/{version}"` → `.../api/...`
   - Anything with `.format()`, `%` formatting → `...`

**Files Changed**:

- `upcast/scanners/http_requests.py`: Add pattern detection logic
- Tests: Add cases for concatenation, query params, f-strings

## Benefits

1. **Actionable Django Model Output**: Module paths enable proper model identification and cross-referencing
2. **Meaningful HTTP Pattern Analysis**: URL normalization reveals actual endpoint diversity
3. **Better Downstream Integration**: Both scanners produce structured data suitable for automated analysis
4. **User Trust**: Output matches documentation/examples, reducing confusion

## Risks & Mitigation

### Risk: Module path calculation breaks for edge cases

- **Examples**: Symlinks, namespace packages, src layouts
- **Mitigation**: Add fallback to qname-based extraction, document limitations
- **Test Coverage**: Add tests for common project structures

### Risk: URL pattern detection creates false patterns

- **Example**: Business logic string concatenation mis-identified as URL
- **Mitigation**: Only trigger on nodes that are args to known HTTP methods
- **Validation**: Manual review of wagtail results before/after

### Risk: Breaking changes to output format

- **Example**: Tools parsing old output format fail
- **Mitigation**:
  - Module path change is additive (was empty, now filled)
  - URL grouping change improves granularity (no keys removed)
  - Document changes in changelog
- **Assessment**: Low risk - output was already broken/unusable

## Alternatives Considered

### Alternative 1: Use astroid package inference

- **Approach**: Configure astroid to understand project structure
- **Rejected**: Too complex, requires dependency resolution, slow
- **Reason**: File-system based approach is simpler and sufficient

### Alternative 2: Keep unknown_url, add metadata

- **Approach**: Store pattern hints in usage metadata
- **Rejected**: Doesn't solve grouping problem, adds complexity
- **Reason**: Direct pattern normalization is clearer

## Dependencies

- None - pure refactoring of existing scanners
- No new external dependencies required
- Changes are backward compatible (improving empty/useless values)

## Validation Plan

1. **Unit Tests**:

   - Module path calculation for various file structures
   - URL pattern detection for common AST patterns
   - Edge cases: nested modules, special characters

2. **Integration Tests**:

   - Scan wagtail project (user's actual test case)
   - Verify module paths are populated
   - Verify URL patterns show diversity (not all `unknown_url`)

3. **Acceptance Criteria**:
   - No models with empty `module` field
   - No models with `.ClassName` format (must have at least one dot for module)
   - `unknown_url` usage drops significantly (<20% of total URLs)
   - Dynamic URL patterns show as `...`, `...?...`, `.../...`

## Timeline Estimate

- Phase 1 (Django Models): 2-4 hours
  - Implementation: 1-2 hours
  - Testing: 1-2 hours
- Phase 2 (HTTP Requests): 3-5 hours
  - Implementation: 2-3 hours
  - Testing: 1-2 hours
- **Total**: 5-9 hours

## Success Metrics

**Before**:

- Django models: 100% with empty module field
- HTTP requests: ~90% in `unknown_url` bucket

**After**:

- Django models: 0% with empty module field
- HTTP requests: <20% in `unknown_url` bucket
- URL patterns show meaningful groupings (`...`, `...?...`)

## Related Work

- This fixes regressions introduced during scanner architecture refactoring
- Addresses user-reported issues with scan output quality
- No spec changes required - fixing implementation bugs
