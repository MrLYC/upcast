# Design: fix-scanner-output-issues

## Architecture Overview

This change fixes two independent output bugs in scanner implementations:

1. **Django Models**: Missing module path resolution
2. **HTTP Requests**: Insufficient URL pattern normalization

Both fixes are localized to their respective scanner implementations with no cross-dependencies.

## Module Path Resolution Design (Django Models)

### Current Implementation

```python
# upcast/common/django/model_parser.py::parse_model()
qname = class_node.qname()  # Returns just "ClassName" when isolated
qname_parts = qname.split(".")
module_path = ".".join(qname_parts[:-1]) if len(qname_parts) > 1 else ""
# Result: module_path = "" (empty)
```

**Problem**: Astroid's `qname()` only returns the class name when parsing files in isolation without package context.

### Proposed Implementation

```python
def _calculate_module_path(file_path: Path, root_path: Path) -> str:
    """Calculate module path from file system structure.

    Examples:
        project/app/models.py → app.models
        project/app/models/base.py → app.models.base
        project/app/__init__.py → app
    """
    relative = file_path.relative_to(root_path)

    # Handle __init__.py
    if relative.name == "__init__.py":
        parts = relative.parent.parts
    else:
        parts = relative.with_suffix("").parts

    return ".".join(parts)

def parse_model(
    class_node: nodes.ClassDef,
    file_path: Path | None = None,
    root_path: Path | None = None,
) -> dict[str, Any] | None:
    """Parse Django model with optional file context."""

    # Calculate module path
    if file_path and root_path:
        module_path = _calculate_module_path(file_path, root_path)
    else:
        # Fallback to qname-based extraction (backward compat)
        qname = class_node.qname()
        module_path = ".".join(qname.split(".")[:-1])

    result = {
        "name": class_node.name,
        "module": module_path,  # Now populated!
        # ...
    }
```

**Benefits**:

- Reliable: Works regardless of astroid's inference
- Simple: Pure file system operation
- Backward Compatible: Fallback to old behavior if paths not provided

**Edge Cases**:

- Symlinks: Resolve before calculating relative path
- Namespace packages: Not supported, document limitation
- Non-Python files: Caller responsibility to pass valid paths

### Scanner Integration

```python
# upcast/scanners/django_models.py
class DjangoModelScanner(BaseScanner):
    def scan(self, path: Path) -> DjangoModelOutput:
        # Store root_path for module calculation
        self.root_path = path if path.is_dir() else path.parent
        # ...

    def _scan_file(self, file_path: Path) -> dict[str, dict]:
        module = self.parse_file(file_path)
        # ...
        for class_node in module.nodes_of_class(nodes.ClassDef):
            model_data = parse_model(
                class_node,
                file_path=file_path,        # NEW
                root_path=self.root_path,   # NEW
            )
```

## URL Pattern Normalization Design (HTTP Requests)

### Current Implementation

```python
# upcast/scanners/http_requests.py::_extract_url()
def _extract_url(self, node: nodes.Call) -> str | None:
    if node.args:
        url_value = safe_infer_value(node.args[0])
        if isinstance(url_value, str):
            return url_value  # Only handles literals
    return None  # Everything else becomes "unknown_url"
```

**Problem**: Only literal strings are extracted, all dynamic URLs collapse into `unknown_url`.

### Proposed Implementation

```python
def _normalize_url_pattern(self, node: nodes.NodeNG) -> str | None:
    """Normalize dynamic URL construction into pattern.

    Returns:
        Pattern string ("...", "...?...", etc.) or None if unrecognizable
    """
    # String concatenation: base + path
    if isinstance(node, nodes.BinOp) and node.op == '+':
        has_query = self._contains_query_indicator(node)
        return "...?..." if has_query else "..."

    # F-strings: f"{base}/api/{version}"
    if isinstance(node, nodes.JoinedStr):
        has_query = any('?' in safe_as_string(v) for v in node.values)
        has_path = any('/' in safe_as_string(v) for v in node.values)
        if has_query:
            return "...?..."
        elif has_path:
            return ".../..."
        return "..."

    # Format strings: "{}/api".format(base)
    if isinstance(node, nodes.Call) and isinstance(node.func, nodes.Attribute):
        if node.func.attrname == 'format':
            return "..."

    return None

def _contains_query_indicator(self, node: nodes.NodeNG) -> bool:
    """Check if node contains query param indicators."""
    as_str = safe_as_string(node)
    return '?' in as_str or 'urlencode' in as_str or 'params=' in as_str

def _extract_url(self, node: nodes.Call) -> str | None:
    """Extract URL with fallback to pattern normalization."""
    # Try literal inference first
    if node.args:
        url_value = safe_infer_value(node.args[0])
        if isinstance(url_value, str):
            return url_value  # Exact URL

    # Try pattern normalization
    if node.args:
        pattern = self._normalize_url_pattern(node.args[0])
        if pattern:
            return pattern  # Normalized pattern

    # Check keywords
    for kw in node.keywords or []:
        if kw.arg == 'url':
            url_value = safe_infer_value(kw.value)
            if isinstance(url_value, str):
                return url_value
            pattern = self._normalize_url_pattern(kw.value)
            if pattern:
                return pattern

    return None  # Truly unknown
```

### Pattern Recognition Rules

| AST Pattern            | Code Example            | Normalized Pattern       |
| ---------------------- | ----------------------- | ------------------------ |
| `BinOp +` without `?`  | `base + path`           | `...`                    |
| `BinOp +` with `?`     | `url + '?' + params`    | `...?...`                |
| `JoinedStr` (f-string) | `f"{base}/api"`         | `...` or `.../...`       |
| `Call.format()`        | `"{}/api".format(base)` | `...`                    |
| Literal `Const`        | `"http://example.com"`  | Exact string             |
| Unknown                | `get_url()`             | `None` → `"unknown_url"` |

**Benefits**:

- Preserves exact URLs (no change for literals)
- Reveals URL pattern diversity
- Actionable groupings for analysis
- Clear conventions (`...` = placeholder)

**Limitations**:

- May normalize some non-URL string operations
  - Mitigation: Only applies to nodes passed as URL arguments to HTTP methods
- Cannot resolve complex runtime URLs
  - Expected: Those remain `unknown_url`
- Pattern may be too generic for some use cases
  - Future: Add option for more specific patterns

## Testing Strategy

### Unit Tests

**Django Models - Module Path Calculation**:

```python
def test_calculate_module_path_models_py():
    root = Path("/project")
    file = Path("/project/app/models.py")
    assert _calculate_module_path(file, root) == "app.models"

def test_calculate_module_path_init_py():
    root = Path("/project")
    file = Path("/project/app/__init__.py")
    assert _calculate_module_path(file, root) == "app"

def test_calculate_module_path_nested():
    root = Path("/project")
    file = Path("/project/a/b/c/models.py")
    assert _calculate_module_path(file, root) == "a.b.c.models"
```

**HTTP Requests - Pattern Normalization**:

```python
def test_normalize_simple_concat():
    # base + "/api"
    node = parse("base + '/api'").body[0].value
    assert scanner._normalize_url_pattern(node) == "..."

def test_normalize_query_params():
    # url + '?' + urlencode(params)
    node = parse("url + '?' + urlencode(params)").body[0].value
    assert scanner._normalize_url_pattern(node) == "...?..."

def test_normalize_fstring():
    # f"{base}/api/{version}"
    node = parse('f"{base}/api/{version}"').body[0].value
    assert scanner._normalize_url_pattern(node) == ".../..."
```

### Integration Tests

Create fixtures with realistic code patterns:

**Fixture: django_project/myapp/models.py**:

```python
class User(models.Model):
    name = models.CharField(max_length=100)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
```

**Test**:

```python
def test_django_models_integration():
    scanner = DjangoModelScanner()
    result = scanner.scan(Path("fixtures/django_project"))

    assert "myapp.models.User" in result.results
    assert result.results["myapp.models.User"].module == "myapp.models"
```

**Fixture: http_requests/api.py**:

```python
import requests

base_url = "https://api.example.com"
requests.get(f"{base_url}/users")
requests.post(base_url + "/users", json={})
requests.get("https://exact.com/path")
```

**Test**:

```python
def test_http_requests_patterns():
    scanner = HttpRequestsScanner()
    result = scanner.scan(Path("fixtures/http_requests"))

    assert "..." in result.results  # f-string and concat
    assert "https://exact.com/path" in result.results  # literal
    assert len(result.results) >= 2  # Not all unknown_url
```

## Validation Plan

### Pre-Deployment Validation

1. **Unit Tests**: All new helper functions
2. **Integration Tests**: Real fixtures mimicking project structures
3. **Regression Tests**: Existing tests still pass
4. **Coverage Check**: Maintain ≥80% coverage

### Post-Deployment Validation

1. **Real Project Scan**: Run on wagtail (user's test case)

   ```bash
   upcast scan-django-models ~/github/wagtail --format yaml > after_models.yaml
   upcast scan-http-requests ~/github/wagtail/wagtail/embeds --format yaml > after_http.yaml
   ```

2. **Quality Checks**:

   - Django models: No empty `module` fields
   - HTTP requests: `unknown_url` < 20% of total
   - Compare before/after: Verify improvements

3. **User Acceptance**:
   - User confirms module paths are correct
   - User confirms URL patterns are meaningful

## Risk Mitigation

### Risk: Module path wrong for non-standard layouts

**Mitigation**:

- Document assumption: Root path is project root
- Add tests for common layouts (src/, flat, nested)
- Provide fallback to qname-based extraction

### Risk: URL patterns too generic

**Mitigation**:

- Keep literal URLs unchanged (exact strings)
- Only normalize when clearly dynamic
- Document pattern conventions in output

### Risk: Performance degradation

**Assessment**: Low risk

- Module path: Single Path operation per model
- URL pattern: Only on inference failure (rare path)
- No new file I/O or network calls

**Validation**: Time scans before/after on large codebase

## Future Enhancements

**Not in scope for this change**:

1. Configurable pattern templates (e.g., `<dynamic>` instead of `...`)
2. Smarter URL inference (resolve variables from context)
3. Support for namespace packages in module paths
4. Extract query param names from `params={}` dicts

**Rationale**: Keep fix focused on immediate bugs, defer enhancements to future changes.
