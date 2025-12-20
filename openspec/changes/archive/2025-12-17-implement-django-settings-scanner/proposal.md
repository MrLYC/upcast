# Proposal: Implement Django Settings Scanner

## Why

Django projects rely heavily on configuration through the `django.conf.settings` object. Understanding which settings variables are actually used in the codebase is critical for:

1. **Configuration Migration**: When moving between environments or refactoring settings, knowing which variables are actively used prevents breaking changes
2. **Dead Configuration Cleanup**: Identifying unused settings variables to remove technical debt
3. **Security Audits**: Tracking where sensitive settings (API keys, database credentials) are accessed
4. **Documentation**: Auto-generating configuration documentation based on actual usage
5. **Dependency Analysis**: Understanding configuration dependencies between modules

Currently, developers must manually search for settings usage with text-based grep, which:

- Misses dynamic access patterns (`getattr(settings, var_name)`)
- Cannot distinguish Django's `settings` from other similarly-named objects
- Produces false positives from comments, strings, or non-Django code
- Doesn't aggregate usage by variable name across the codebase

## What Changes

Add a new `django_settings_scanner` module to the `upcast` package that:

1. **Scans Python files** for Django settings usage through semantic AST analysis
2. **Detects three access patterns**:
   - Direct attribute access: `settings.DATABASE_URL`
   - Dynamic access with getattr: `getattr(settings, "API_KEY", default)`
   - Existence checks with hasattr: `hasattr(settings, "FEATURE_FLAG")`
3. **Validates settings origin** by ensuring the `settings` object is imported from `django.conf`
4. **Aggregates results by variable name** with all usage locations
5. **Outputs structured YAML** with file paths, line numbers, and access patterns

### Scope Constraints

- ✅ Only scan `from django.conf import settings` (official Django way)
- ✅ Support aliased imports: `from django.conf import settings as config`
- ❌ Exclude project-local settings modules (e.g., `from myproject.settings import X`)
- ❌ Exclude `LazySettings` direct usage (rarely used by developers)

### Example Output

```yaml
DATABASES:
  count: 3
  locations:
    - file: myapp/models.py
      line: 10
      column: 5
      pattern: attribute_access
      code: settings.DATABASES
    - file: myapp/utils.py
      line: 25
      column: 12
      pattern: getattr
      code: getattr(settings, 'DATABASES')
    - file: myapp/checks.py
      line: 40
      column: 8
      pattern: hasattr
      code: hasattr(settings, 'DATABASES')

DEBUG:
  count: 2
  locations:
    - file: myapp/middleware.py
      line: 15
      column: 8
      pattern: attribute_access
      code: settings.DEBUG
    - file: myapp/views.py
      line: 50
      column: 20
      pattern: attribute_access
      code: settings.DEBUG
```

### Architecture

Follow the established scanner architecture pattern:

```
upcast/django_settings_scanner/
├── __init__.py           # Public API
├── cli.py                # Command-line interface
├── checker.py            # AST visitor and aggregation
├── ast_utils.py          # Pattern detection helpers
├── settings_parser.py    # Settings usage extraction
└── export.py             # YAML output formatting
```

### CLI Integration

```bash
# Scan project directory
uv run upcast scan-django-settings /path/to/django/project

# Specify output file
uv run upcast scan-django-settings /path/to/project -o settings_usage.yaml

# Verbose mode
uv run upcast scan-django-settings /path/to/project -v
```

### Delta Summary

This change introduces a **new capability**: `django-settings-scanner`

See `specs/django-settings-scanner/spec.md` for complete requirements.
