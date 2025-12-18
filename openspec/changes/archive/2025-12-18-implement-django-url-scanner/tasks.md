# Tasks

## 1. Create Django URL Scanner Module Structure

- [x] Create `upcast/django_url_scanner/` directory
- [x] Create `__init__.py` with public API
- [x] Create `cli.py` for main scanning function
- [x] Create `checker.py` for AST visitor implementation
- [x] Create `url_parser.py` for URL pattern parsing logic
- [x] Create `export.py` for YAML output formatting

## 2. Implement URL Pattern Detection

- [x] Implement AST visitor to find `urlpatterns` assignments
- [x] Extract module path from file being scanned
- [x] Parse list/tuple literals containing route definitions
- [x] Handle both `path()` and `re_path()` function calls
- [x] Extract URL pattern string (first positional argument)
- [x] Extract view reference (second positional argument)
- [x] Extract `name` keyword argument if present

## 3. Implement View Resolution

- [x] Resolve view function references using astroid inference
- [x] Handle direct function references (`blog_views.index`)
- [x] Handle class-based views with `.as_view()` calls
- [x] Handle `functools.partial` wrapped views
- [x] Handle conditional view expressions (ternary operators)
- [x] Extract view module path and function/class name
- [x] Extract docstring from view function/class as description

## 4. Implement Include Detection

- [x] Detect `include()` calls in URL patterns
- [x] Extract included module path
- [x] Extract namespace if provided
- [x] Mark as include without expanding nested patterns

## 5. Implement Converter Parsing

- [x] Parse path converter syntax `<type:name>`
- [x] Extract converter type and parameter name
- [x] Store converter information in output
- [x] Handle both built-in and custom converters

## 6. Implement Regex Pattern Parsing

- [x] Store raw regex pattern from `re_path()`
- [x] Extract named groups from regex patterns
- [x] Document captured parameter names

## 7. Implement DRF Router Support

- [x] Detect router instance creation (`DefaultRouter()`, etc.)
- [x] Track `router.register()` calls
- [x] Extract ViewSet class and basename
- [x] Record as special route type (don't expand)

## 8. Implement ViewSet Action Mapping

- [x] Parse `.as_view()` with action mapping dict
- [x] Store HTTP method to action mappings
- [x] Associate with ViewSet class

## 9. Implement Output Formatting

- [x] Design YAML output structure
- [x] Group routes by module path (urlpatterns location)
- [x] Format each route with pattern, view, name, description
- [x] Handle include routes specially
- [x] Add converter information to routes
- [x] Use common export utilities for consistent formatting

## 10. Add CLI Command

- [x] Add `scan-django-urls` command to `upcast/main.py`
- [x] Support standard options: `-o`, `-v`, `--include`, `--exclude`
- [x] Implement `--no-default-excludes` flag
- [x] Add command help text with examples
- [x] Wire up to scanner implementation

## 11. Implement Error Handling

- [x] Handle unresolvable view references gracefully
- [x] Mark unresolved views with placeholder
- [x] Log warnings in verbose mode
- [x] Continue scanning on errors (don't fail entire scan)
- [x] Report parsing errors clearly

## 12. Add Integration Tests

- [x] Create test fixtures with various URL patterns
- [x] Test basic path() detection
- [x] Test re_path() with regex
- [x] Test include() detection
- [x] Test class-based views
- [x] Test ViewSet action mappings
- [x] Test DRF router registration
- [x] Test converter parsing
- [x] Test conditional routes
- [x] Test functools.partial views
- [x] Test multiple routes to same view
- [x] Test unresolvable view handling
- [x] Test YAML output format

## 13. Add Unit Tests

- [x] Test URL pattern parser functions
- [x] Test AST visitor logic
- [x] Test view resolution functions
- [x] Test converter extraction
- [x] Test regex named group extraction
- [x] Test export formatting

## 14. Add Documentation

- [x] Add docstrings to all public functions
- [x] Document output YAML format
- [x] Add CLI command examples
- [x] Document limitations and edge cases

## 15. Validate and Polish

- [x] Run all tests (ensure 100% pass rate)
- [x] Check code style with ruff
- [x] Verify CLI integration works
- [x] Test on real Django project samples
- [x] Update main README if needed
