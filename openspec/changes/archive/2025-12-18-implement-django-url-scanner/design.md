# Design: Django URL Scanner Implementation

## Overview

This document describes the technical design for implementing a static analyzer that extracts Django URL routing configurations from Python source code.

## Architecture

### Module Structure

```
upcast/django_url_scanner/
├── __init__.py          # Public API exports
├── cli.py               # Main scanning orchestration
├── checker.py           # AST visitor for URL pattern detection
├── url_parser.py        # URL pattern parsing logic
├── view_resolver.py     # View reference resolution
└── export.py            # YAML output formatting
```

### Data Flow

```
Input Files
    ↓
File Discovery (common.file_utils)
    ↓
AST Parsing (astroid)
    ↓
URL Pattern Detection (checker.py)
    ↓
View Resolution (view_resolver.py)
    ↓
Result Aggregation
    ↓
YAML Export (export.py)
    ↓
Output
```

## Core Components

### 1. UrlPatternChecker (checker.py)

AST visitor that traverses Python modules to find `urlpatterns` assignments.

**Responsibilities:**

- Locate `urlpatterns = [...]` assignments
- Identify the module path of the file
- Extract route definitions from list/tuple
- Delegate parsing to specialized parsers

**Key Methods:**

```python
class UrlPatternChecker(nodes.NodeVisitor):
    def visit_assign(self, node):
        # Check if target is 'urlpatterns'
        # Extract routes from value

    def _parse_route_list(self, node):
        # Parse list/tuple of path() calls

    def _is_url_function(self, call_node):
        # Identify path(), re_path(), include()
```

### 2. ViewResolver (view_resolver.py)

Resolves view references to module paths and extracts metadata.

**Responsibilities:**

- Use astroid inference to resolve view references
- Handle function views, CBVs, ViewSets
- Extract docstrings
- Handle special cases (partial, conditional)

**Key Methods:**

```python
def resolve_view(view_node, context):
    """
    Returns: {
        'module': 'blog.views',
        'name': 'post_detail',
        'description': 'Display a blog post',
        'type': 'function' | 'class' | 'viewset',
        'resolved': True | False
    }
    """
```

### 3. UrlPatternParser (url_parser.py)

Parses individual URL pattern strings and extracts metadata.

**Responsibilities:**

- Parse converter syntax `<type:name>`
- Extract regex named groups
- Normalize path patterns

**Key Functions:**

```python
def parse_converters(pattern: str) -> dict[str, str]:
    """Extract converters from path pattern"""
    # "<int:id>/<slug:slug>/" → {"id": "int", "slug": "slug"}

def extract_regex_groups(pattern: str) -> list[str]:
    """Extract named groups from regex pattern"""
    # r"^tag/(?P<tag>[a-z]+)/$" → ["tag"]
```

### 4. Export (export.py)

Formats scan results into structured YAML.

**Output Structure:**

```yaml
# Module path as key
myapp.urls:
  module: "myapp.urls"
  urlpatterns:
    - pattern: "post/<int:id>/"
      view_module: "blog.views"
      view_name: "post_detail"
      view_type: "function"
      name: "post-detail"
      description: "Display a single blog post"
      converters:
        id: "int"

    - pattern: "api/"
      include_module: "myapp.api.urls"
      namespace: "api"
```

## Special Cases Handling

### 1. Include Detection

```python
path("api/", include("myapp.api.urls"))
path("api/", include(router.urls))
path("org/<int:id>/", include([...]))  # inline
```

**Strategy:**

- Detect `include()` calls by function name
- Extract first argument (module path or router.urls)
- For inline lists, mark as "inline" without module reference
- Do NOT recursively scan included modules

### 2. Class-Based Views

```python
path("edit/", EditView.as_view())
path("user/", UserViewSet.as_view({"get": "list"}))
```

**Strategy:**

- Detect `.as_view()` attribute access
- Resolve the class before `.as_view()`
- For ViewSets, extract action mapping dict if present
- Extract docstring from class, not as_view method

### 3. DRF Routers

```python
router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
urlpatterns = [path("api/", include(router.urls))]
```

**Strategy:**

- Track router variable assignments
- Track `register()` calls on router variables
- When `router.urls` appears in include, reference registrations
- Store registrations separately from regular patterns

### 4. Functools.partial

```python
path("ping/", partial(health_check, timeout=10))
```

**Strategy:**

- Detect `partial()` calls
- Extract first argument as the actual view function
- Mark as "partial" in metadata
- Resolve underlying function for module/docstring

### 5. Conditional Views

```python
path("debug/", debug_view if settings.DEBUG else stub_view)
```

**Strategy:**

- Detect ternary expression (`IfExp` node)
- Resolve both branches
- Mark route as "conditional"
- Store both possible views

### 6. Multiple Routes to Same View

```python
path("latest/", blog_views.latest),
path("recent/", blog_views.latest),
```

**Strategy:**

- Each route is independent entry in output
- View resolution is idempotent (same result for both)
- No special handling needed

## AST Analysis Strategy

### Node Types to Handle

1. **Assign**: `urlpatterns = [...]`
2. **Call**: `path()`, `re_path()`, `include()`
3. **Attribute**: `router.urls`, `View.as_view()`
4. **Name**: View function references
5. **IfExp**: Conditional view selection
6. **List/Tuple**: Route collections

### Inference Strategy

Use astroid's inference engine to resolve:

- Import statements (aliased imports)
- Function and class definitions
- Attribute access chains
- Variable assignments

**Fallback**: If inference fails, use string-based pattern matching as last resort.

## Error Handling Philosophy

**Principle**: Fail gracefully, continue scanning, report issues.

1. **Parse Errors**: Log warning, skip problematic route, continue
2. **Unresolvable Views**: Mark as `<unresolved>`, continue
3. **Import Errors**: Mark view as unresolved, log in verbose mode
4. **Invalid Syntax**: Skip file, log error, continue with other files

## Performance Considerations

1. **Lazy Loading**: Only parse files that match include/exclude patterns
2. **Caching**: Cache inference results for imported modules
3. **Parallel Processing**: Not needed for initial implementation (sequential is sufficient)
4. **Memory**: Process files one at a time, don't load all in memory

## Testing Strategy

### Unit Tests

- URL pattern parser functions
- Converter extraction
- Regex group extraction
- View type detection

### Integration Tests

- Full scanning with test fixtures
- Various Django URL patterns
- DRF router configurations
- Edge cases (partial, conditional, etc.)

### Test Fixtures

Create `tests/test_django_url_scanner/fixtures/` with:

- `basic_urls.py` - Simple path() patterns
- `regex_urls.py` - re_path() patterns
- `cbv_urls.py` - Class-based views
- `drf_urls.py` - DRF routers and ViewSets
- `complex_urls.py` - All edge cases combined

## Implementation Phases

### Phase 1: Core Detection (MVP)

- Basic path() detection
- Function view resolution
- Simple YAML output
- CLI integration

### Phase 2: Advanced Patterns

- re_path() support
- Class-based views
- Include detection
- Converter parsing

### Phase 3: DRF Support

- Router detection
- ViewSet registrations
- Action mappings

### Phase 4: Edge Cases

- Partial views
- Conditional routing
- Inline includes
- Error handling polish

## Open Design Questions

### Q1: Module Path Resolution

**Issue**: How to determine the "module path" for a file?

**Options:**
A. Use file path relative to scan root
B. Try to infer from package structure (**init**.py)
C. Allow user to specify project root

**Recommendation**: Option B (infer from **init**.py), fallback to Option A.

### Q2: Router URL Expansion

**Issue**: Should we expand router-generated URLs?

**Considerations:**

- Routers generate multiple URLs per registration
- Logic is framework-specific and version-dependent
- Would make output verbose

**Recommendation**: Don't expand. Record registrations, let users process separately.

### Q3: Docstring Format

**Issue**: How to handle multi-line docstrings?

**Options:**
A. First line only
B. Full docstring with newlines preserved
C. Smart extraction (summary + first paragraph)

**Recommendation**: Option B (full docstring), use YAML literal block style.

### Q4: Unresolved View Representation

**Issue**: How to represent views that couldn't be resolved?

**Options:**
A. Omit from output
B. Use `null` for module/name
C. Use special marker string like `<unresolved>`
D. Include raw AST representation

**Recommendation**: Option C + include raw text representation in verbose mode.
