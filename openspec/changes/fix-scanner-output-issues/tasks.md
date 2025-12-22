# Tasks: fix-scanner-output-issues

## Phase 1: Fix Django Models Module Path Resolution

### 1.1 Update Model Parser to Accept File Context

- [ ] Update `parse_model()` signature in `upcast/common/django/model_parser.py`
  - Add `file_path: Path` parameter
  - Add `root_path: Path` parameter
  - Keep both optional for backward compatibility

### 1.2 Implement Module Path Calculation

- [ ] Add `_calculate_module_path(file_path: Path, root_path: Path) -> str` helper function
  - Get relative path from root to file
  - Handle `__init__.py` → use parent directory name
  - Handle `models.py` → use parent directory as module
  - Handle `models/xxx.py` → use `parent.models.xxx` format
  - Replace path separators with dots
  - Strip `.py` extension

### 1.3 Update parse_model Implementation

- [ ] Replace qname-based module extraction with file-based calculation
  - When `file_path` and `root_path` provided, call `_calculate_module_path()`
  - Fallback to qname extraction if paths not provided (backward compat)
  - Update `module` field in result dictionary

### 1.4 Update Django Model Scanner

- [ ] Pass file context to parser in `_scan_file()`
  - Calculate `root_path` from scanner initialization (scan target)
  - Pass `file_path` and `root_path` to `parse_model()`
  - Store root_path in scanner instance

### 1.5 Add Unit Tests for Module Path Calculation

- [ ] Test `_calculate_module_path()` function
  - Simple case: `project/app/models.py` → `app.models`
  - Init file: `project/app/__init__.py` → `app`
  - Nested models: `project/app/models/base.py` → `app.models.base`
  - Deep nesting: `project/a/b/c/models.py` → `a.b.c.models`
  - Root level: `project/models.py` → `models`

### 1.6 Update Integration Tests

- [ ] Update existing Django model scanner tests
  - Fix assertions expecting empty module field
  - Add assertions verifying module paths are populated
  - Test with real project structure (create fixtures)

### 1.7 Validation Against Real Projects

- [ ] Test scan-django-models on wagtail
  - Run: `upcast scan-django-models ~/github/wagtail --format yaml`
  - Verify: No models with empty `module` field
  - Verify: No models starting with just `.ClassName`
  - Verify: Base classes show proper module paths

## Phase 2: Enhance HTTP URL Pattern Extraction

### 2.1 Add URL Pattern Analysis Module

- [ ] Create helper methods in `HttpRequestsScanner`:
  - `_is_string_concat(node: nodes.NodeNG) -> bool` - detect BinOp with `+`
  - `_has_query_params(node: nodes.NodeNG) -> bool` - detect `?` or `urlencode`
  - `_normalize_binop_url(node: nodes.BinOp) -> str | None` - handle concatenation

### 2.2 Implement URL Pattern Normalization

- [ ] Add `_normalize_url_pattern(node: nodes.NodeNG) -> str | None` method
  - Handle `nodes.BinOp` (string concatenation): return `...`
  - Handle `nodes.JoinedStr` (f-strings): return `...`
  - Handle `nodes.Call` with `.format()`: return `...`
  - Detect query param indicators: return `...?...`
  - Detect path segment patterns: return `.../...`
  - Return `None` if no pattern recognized

### 2.3 Update URL Extraction Logic

- [ ] Modify `_extract_url()` method
  - Keep current literal inference as first attempt
  - If literal inference fails, try `_normalize_url_pattern()`
  - Only return `"unknown_url"` if both fail
  - Document decision flow in docstring

### 2.4 Add Pattern Detection Rules

- [ ] Implement pattern recognition:
  - String `+` operator → `...`
  - F-string with variables → `...`
  - `.format()` method → `...`
  - Pattern with `?` character → `...?...`
  - `urlencode()` in expression → `...?...`
  - `/` with variables → `.../...`

### 2.5 Add Unit Tests for Pattern Detection

- [ ] Test `_normalize_url_pattern()`:
  - Simple concatenation: `base + path` → `...`
  - Query params: `url + '?' + params` → `...?...`
  - F-string: `f"{base}/api"` → `...`
  - Format: `"{}/api".format(base)` → `...`
  - Mixed: `f"{base}/api?id={id}"` → `...?...`
  - Literal: `"http://example.com"` → `None` (handled by inference)
  - Unknown: `complex_function()` → `None`

### 2.6 Add Unit Tests for URL Extraction

- [ ] Test updated `_extract_url()` flow:
  - Literal string → exact URL
  - Variable + literal → `...`
  - Query construction → `...?...`
  - Complex unknown → `"unknown_url"`

### 2.7 Update Integration Tests

- [ ] Test scanner with realistic HTTP code:
  - Create fixtures with various URL patterns
  - Verify concatenation becomes `...`
  - Verify query params become `...?...`
  - Verify `unknown_url` is rare (<20%)

### 2.8 Validation Against Real Projects

- [ ] Test scan-http-requests on wagtail/embeds
  - Run: `upcast scan-http-requests ~/github/wagtail/wagtail/embeds --format yaml`
  - Verify: Multiple distinct URL patterns (not all `unknown_url`)
  - Verify: Patterns use `...`, `...?...` placeholders
  - Verify: Expected patterns from code review appear in results

## Phase 3: Documentation and Validation

### 3.1 Update Documentation

- [ ] Update README.md scanner examples
  - Show corrected django-models output with module paths
  - Show corrected http-requests output with patterns
  - Document URL pattern conventions (`...`, `...?...`)

### 3.2 Add CHANGELOG Entry

- [ ] Document breaking changes (improvements):
  - Django models now include proper module paths
  - HTTP requests now group by normalized URL patterns
  - Migration notes for tools parsing old output

### 3.3 End-to-End Validation

- [ ] Run both scanners on user's test case (wagtail):
  - Django models: All models have module paths
  - HTTP requests: URL diversity visible
  - Compare before/after outputs
  - Confirm acceptance criteria met

### 3.4 Pre-commit and Quality Checks

- [ ] Verify all tests pass: `uv run pytest`
- [ ] Verify ruff compliance: `uv run ruff check`
- [ ] Verify coverage maintained: `uv run pytest --cov`
- [ ] Run pre-commit hooks

## Acceptance Criteria

### Django Models Scanner

- ✓ No models with `module: ''` (empty field)
- ✓ No model keys starting with just `.ClassName`
- ✓ Base class references include module paths
- ✓ Module paths match file system structure

### HTTP Requests Scanner

- ✓ Less than 20% of URLs in `unknown_url` group
- ✓ Dynamic URL patterns show as `...`
- ✓ Query param patterns show as `...?...`
- ✓ Literal URLs remain unchanged
- ✓ Multiple distinct URL pattern groups visible

### Quality Standards

- ✓ All unit tests pass
- ✓ Integration tests pass with real fixtures
- ✓ Ruff checks pass (PEP8 compliance)
- ✓ Test coverage ≥ 80%
- ✓ Pre-commit hooks pass

### User Validation

- ✓ Wagtail scan produces expected django-models output
- ✓ Wagtail scan produces expected http-requests output
- ✓ User confirms issues resolved
