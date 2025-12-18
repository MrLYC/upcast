# Proposal: Implement Django URL Scanner

## Why

Django projects use URL routing configuration to map HTTP requests to view functions/classes. Understanding the URL structure is critical for:

1. **API Documentation**: Automatically generating API documentation from URL patterns
2. **Route Analysis**: Understanding application structure and endpoint organization
3. **Migration Planning**: Identifying endpoints when migrating to different frameworks or cloud services
4. **Security Audits**: Discovering all exposed endpoints for security review
5. **Dependency Analysis**: Understanding which views are used and how they're organized

Currently, there is no automated way to extract and document Django URL patterns from the codebase. Manual inspection is time-consuming and error-prone, especially for large projects with complex routing configurations.

## What Changes

### Add New Django URL Scanner

Implement `upcast.django_url_scanner` module with the following capabilities:

**Core Scanning Features:**

1. Detect `urlpatterns` variables in Python files
2. Parse `path()` and `re_path()` function calls
3. Extract URL patterns, view references, and route names
4. Handle various view types (functions, classes with `.as_view()`, ViewSets)
5. Track `include()` references without expanding (for recursive analysis)
6. Extract view docstrings as descriptions
7. Support DRF (Django REST Framework) router patterns

**URL Pattern Types:**

- Basic `path()` with function/class views
- Path converters: built-in (`<int:id>`, `<slug:slug>`) and custom (`<year:year>`)
- Regular expression patterns via `re_path()`
- Nested routing via `include()`
- DRF router-generated URLs
- Multiple routes to the same view
- Conditional routes (ternary expressions)

**View Types:**

- Function views
- Class-based views (CBV) with `.as_view()`
- DRF ViewSets with action mappings
- `functools.partial` wrapped views
- Conditional view references

### Output Format

YAML output structure with `type` field to categorize URL patterns:

```yaml
# Key: module path containing urlpatterns
myapp.urls:
  urlpatterns:
    - type: path
      pattern: <root>
      view_module: "blog.views"
      view_name: "index"
      name: "index"
      description: "Home page."

    - type: path
      pattern: "posts/"
      view_module: "blog.views"
      view_name: "post_list"
      name: "post-list"
      description: "List all posts."

    - type: path
      pattern: "posts/<int:id>/"
      view_module: "blog.views"
      view_name: "post_detail"
      name: "post-detail"
      description: "Display a single blog post"
      converters:
        id: "int"

    - type: re_path
      pattern: "^archive/(?P<year>\\d{4})/$"
      view_module: "blog.views"
      view_name: "archive"
      name: "archive"
      named_groups:
        - year

    - type: include
      pattern: "api/"
      include_module: "myapp.api.urls"

    - type: dynamic
      pattern: "<generated>"
      note: "URL patterns generated dynamically"
```

**Pattern Types:**

- `path` - Standard Django path() routes
- `re_path` - Regular expression routes
- `include` - Nested routing via include()
- `dynamic` - Dynamically generated patterns (list comprehension, += extension)

**Special Pattern Markers:**

- `<root>` - Empty string pattern representing root path ("/")
- `<not-detected>` - Pattern value could not be determined (None)
- `<generated>` - Pattern generated via list comprehension
- `<extended>` - Pattern added via dynamic += extension

### CLI Integration

Add `scan-django-urls` command to `upcast` CLI:

```bash
upcast scan-django-urls <path> [options]
  -o, --output FILE          Output file path
  -v, --verbose              Enable verbose output
  --include PATTERN          Include files matching pattern
  --exclude PATTERN          Exclude files matching pattern
  --no-default-excludes      Disable default exclusions
```

### Technical Approach

**Reuse Common Infrastructure:**

- Use `upcast.common.file_utils` for file discovery and filtering
- Use `upcast.common.ast_utils` for AST traversal and analysis
- Use `upcast.common.export` for YAML generation
- Follow established scanner patterns from Django models/settings scanners

**AST Analysis Strategy:**

1. Locate assignment nodes where target is `urlpatterns`
2. Parse list/tuple literals containing `path()` or `re_path()` calls
3. Extract positional and keyword arguments from route functions
4. Infer view module paths using astroid type inference
5. Extract docstrings from view functions/classes
6. Handle special cases (include, as_view, router, partial)

## Impact

### Benefits

- **Consistency**: Follows established scanner patterns in the project
- **Automation**: Eliminates manual URL documentation efforts
- **Accuracy**: Static analysis reduces human error
- **Integration**: Works with existing CLI and output formats
- **Extensibility**: Foundation for future route analysis features

### Risks

- **Complex Routing**: Some dynamic routing patterns may be difficult to analyze statically
- **DRF Complexity**: ViewSet action mappings and router internals may require special handling
- **Runtime Dependencies**: Custom converters and middleware might affect actual routing differently

### Breaking Changes

None - this is a new feature.

## Open Questions

### 1. ViewSet Action Mapping Detail Level

**Question**: For DRF ViewSets like `UserViewSet.as_view({"get": "list", "post": "create"})`, should we:

- A) Just record `UserViewSet` and the action mapping dict as-is
- B) Expand to individual methods (`UserViewSet.list`, `UserViewSet.create`)
- C) Both (nested structure)?

**Recommendation**: Option A (record as-is) for initial implementation, can enhance later.

### 2. URL Parameter Type Information

**Question**: For custom converters like `<year:year>`, should we:

- A) Just record the converter name ("year")
- B) Try to resolve the converter class definition
- C) Allow configuration for known converter mappings

**Recommendation**: Option A (converter name only), users can define converters separately.

### 3. Dynamic URL Construction

**Question**: How to handle URLs constructed at runtime?

```python
urlpatterns = []
if settings.DEBUG:
    urlpatterns += [path("debug/", debug_view)]
```

**Recommendation**: Detect pattern but mark as "conditional" without attempting to evaluate conditions.

### 4. Namespace Handling

**Question**: Django supports namespaces via `include("app.urls", namespace="api")`. Should we:

- A) Just record the namespace parameter
- B) Prefix all nested route names with namespace
- C) Create separate namespace section in output

**Recommendation**: Option A (record parameter), namespace resolution can be done in post-processing.

### 5. Regex Pattern Documentation

**Question**: For `re_path(r"^tag/(?P<tag>[a-z0-9\-]+)/$", ...)`, should we:

- A) Store raw regex string
- B) Parse and extract named groups
- C) Both

**Recommendation**: Option C - store raw pattern and extract named groups for clarity.

### 6. Error Handling for Unresolvable Views

**Question**: If view cannot be resolved (e.g., imported from unavailable module), should we:

- A) Skip the route entirely
- B) Record with placeholder/unknown marker
- C) Report as warning but continue

**Recommendation**: Option B (record with marker like `<unresolved>`) + Option C (warn in verbose mode).

### 7. Multiple URL Files

**Question**: Projects often have multiple `urls.py` files. Should the scanner:

- A) Only scan the file explicitly provided
- B) Auto-discover all files with `urlpatterns`
- C) Follow `include()` references to find related files

**Recommendation**: Option B (auto-discover in scan directory), user can filter with include/exclude patterns.

### 8. Router URL Generation

**Question**: For DRF routers, should we:

- A) Just record `router.urls` as an include
- B) Attempt to expand router patterns (e.g., `/users/`, `/users/{id}/`)
- C) Record ViewSet registrations separately

**Recommendation**: Option C - record router registrations with basename, don't expand (too complex and framework-specific).
