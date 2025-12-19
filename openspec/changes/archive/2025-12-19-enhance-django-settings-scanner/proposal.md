# Proposal: enhance-django-settings-scanner

## What

Enhance the Django settings scanner to detect both settings **definitions** and **usages**, providing a comprehensive view of Django configuration across a project. Currently, the scanner only tracks where settings are used (`settings.DEBUG`, `getattr(settings, 'KEY')`). This change adds detection of where settings are defined (e.g., `DEBUG = True` in `settings/base.py`), with value inference and support for common Django settings patterns including inheritance and dynamic imports.

## Why

Understanding Django settings requires knowing both where they're defined and where they're used:

1. **Configuration Discovery**: Teams need to know which settings are defined in the project, not just where they're accessed
2. **Value Tracking**: Understanding default values and overrides helps with debugging and deployment
3. **Inheritance Patterns**: Django projects commonly use `settings/base.py` with environment-specific overrides in `settings/dev.py`, `settings/prod.py`
4. **Dynamic Import Support**: Many projects use `importlib` to dynamically load settings modules based on environment variables
5. **Migration Support**: When upgrading Django or restructuring settings, knowing both definitions and usages helps identify what's actually in use
6. **Documentation**: Auto-generate configuration documentation from settings definitions

Current output only shows usages:

```yaml
DEBUG:
  count: 5
  locations:
    - file: app/views.py
      line: 10
      pattern: attribute_access
```

Enhanced output will show both definitions and usages:

```yaml
definitions:
  settings.base:
    DEBUG:
      value: false
      line: 15
      type: literal
    INSTALLED_APPS:
      value: [...]
      line: 20
      type: list
  settings.dev:
    DEBUG:
      value: true
      line: 10
      type: literal
      overrides: settings.base

usages:
  DEBUG:
    count: 5
    locations: [...]
```

## How

### Core Approach

1. **Definition Detection**: Identify settings modules by file path patterns (`settings/`, `config/`) and scan for uppercase variable assignments
2. **Value Inference**: Use astroid to infer values for settings definitions (literals, lists, dicts, function calls)
3. **Inheritance Tracking**: Detect `from .base import *` patterns and track which settings override others
4. **Dynamic Import Support**: Recognize common dynamic import patterns (e.g., `importlib.import_module(f"settings.{env}")`)
5. **Module Path Keys**: Use Python module paths (e.g., `settings.base`, `myproject.config.dev`) as keys for definitions
6. **Unified Output**: Combine definitions and usages in a single YAML output with clear separation

### Settings Module Detection

Identify files that likely contain settings definitions:

1. **Path-based detection**: Files in directories named `settings/` or `config/`

   - Examples: `myproject/settings/base.py`, `config/settings.py`
   - Convert file path to module path: `myproject/settings/base.py` → `myproject.settings.base`

2. **Import-based detection** (enhanced accuracy):

   - Track modules imported by usage sites
   - If usage imports `from myproject.settings import DEBUG`, mark `myproject.settings` as a settings module
   - Handles non-standard locations (e.g., `myproject/core/configuration.py`)

3. **Dynamic import detection**:
   - Detect patterns like: `importlib.import_module(f"settings.{env}")`
   - Mark base module (`settings`) and common variants (`settings.dev`, `settings.prod`, `settings.test`)

### Variable Detection and Value Inference

For each identified settings module:

1. **Uppercase assignments**: Detect `NAME = value` where NAME is all uppercase

   - Include `_` in names: `DATABASE_URL`, `CORS_ALLOWED_ORIGINS`
   - Exclude Python constants: `__name__`, `__file__`, `__version__`

2. **Value inference** using astroid:

   - **Literals**: `DEBUG = True` → `{"value": true, "type": "literal"}`
   - **Strings**: `DATABASE_URL = "postgres://..."` → `{"value": "postgres://...", "type": "string"}`
   - **Lists/Tuples**: `INSTALLED_APPS = ["app1", "app2"]` → `{"value": ["app1", "app2"], "type": "list"}`
   - **Dicts**: `DATABASES = {"default": {...}}` → `{"value": {...}, "type": "dict"}`
   - **Function calls**: `BASE_DIR = Path(__file__).resolve().parent` → `{"value": "`Path(**file**).resolve().parent`", "type": "call"}`
   - **Unresolvable**: `SECRET_KEY = os.environ.get("SECRET")` → `{"value": "`os.environ.get('SECRET')`", "type": "dynamic"}`

3. **Type annotations**: Include type hints if present
   - `DEBUG: bool = True` → `{"type_hint": "bool", ...}`

### Inheritance Detection

Track which settings override others:

1. **Star imports**: Detect `from .base import *`

   - Resolve relative imports to module paths
   - Example: In `settings/dev.py`, `from .base import *` → imports from `settings.base`
   - Mark subsequent uppercase assignments as overrides

2. **Override tracking**:

   ```python
   # settings/base.py
   DEBUG = False

   # settings/dev.py
   from .base import *
   DEBUG = True  # Overrides settings.base.DEBUG
   ```

   Output:

   ```yaml
   definitions:
     settings.base:
       DEBUG:
         value: false
         line: 10
     settings.dev:
       DEBUG:
         value: true
         line: 15
         overrides: settings.base
   ```

3. **Multiple inheritance**: Track multiple base modules if present

### Dynamic Import Support

Recognize and document dynamic import patterns:

1. **importlib patterns**:

   ```python
   import importlib
   profile = os.environ.get("PROFILE", "dev")
   module = importlib.import_module(f"settings.{profile}")
   ```

   Detect:

   - `importlib.import_module()` calls with f-strings or string concatenation
   - Extract base module name (`settings`)
   - List possible values (`dev`, `prod`, `test`) if detectable

2. **Dynamic assignment patterns**:

   ```python
   for k in dir(module):
       if k.isupper():
           globals()[k] = getattr(module, k)
   ```

   Detect:

   - `globals()` dictionary updates
   - `setattr(sys.modules[__name__], k, v)` patterns
   - Mark module as having dynamic exports

3. **Output representation**:
   ```yaml
   dynamic_imports:
     - pattern: "importlib.import_module(f'settings.{profile}')"
       base_module: settings
       detected_variants: [dev, prod, test]
       file: myproject/__init__.py
       line: 10
   ```

### Output Structure

Restructure YAML output to include both definitions and usages:

```yaml
# Settings definitions grouped by module
definitions:
  settings.base:
    DEBUG:
      value: false
      line: 15
      type: literal
    INSTALLED_APPS:
      value:
        - django.contrib.admin
        - django.contrib.auth
        - myapp
      line: 20
      type: list
    SECRET_KEY:
      value: "`os.environ.get('SECRET_KEY')`"
      line: 30
      type: dynamic

  settings.dev:
    DEBUG:
      value: true
      line: 10
      type: literal
      overrides: settings.base
    ALLOWED_HOSTS:
      value: ["localhost", "127.0.0.1"]
      line: 15
      type: list

# Dynamic import patterns (if detected)
dynamic_imports:
  - pattern: "importlib.import_module(f'settings.{env}')"
    base_module: settings
    file: myproject/__init__.py
    line: 5

# Settings usages (existing functionality, unchanged)
usages:
  DEBUG:
    count: 5
    locations:
      - file: myapp/views.py
        line: 10
        column: 15
        pattern: attribute_access
        code: "settings.DEBUG"
```

### Module Structure Changes

Extend existing module structure:

```
upcast/django_settings_scanner/
├── __init__.py           # Add scan_settings_definitions
├── ast_utils.py          # Add is_uppercase_assignment, is_star_import
├── settings_parser.py    # Add SettingsDefinition, SettingsModule dataclasses
├── definition_parser.py  # NEW: Parse settings definitions and values
├── checker.py            # Extend to track both definitions and usages
├── export.py             # Update format to include definitions
└── cli.py                # Add --definitions-only, --usages-only flags
```

New module: `definition_parser.py`

- `detect_settings_module(file_path: str) -> bool`: Check if file is a settings module
- `parse_uppercase_assignment(node: nodes.Assign) -> SettingsDefinition | None`: Extract definition
- `infer_setting_value(node: nodes.NodeNG) -> dict`: Infer value and type
- `detect_star_imports(module: nodes.Module) -> list[str]`: Find `from X import *`
- `detect_dynamic_imports(module: nodes.Module) -> list[DynamicImport]`: Find importlib patterns

## Impact

### New Files

- `upcast/django_settings_scanner/definition_parser.py`: Settings definition detection and parsing
- `tests/test_django_settings_scanner/test_definition_parser.py`: Unit tests for definition parser
- `tests/test_django_settings_scanner/fixtures/settings_base.py`: Test fixture for base settings
- `tests/test_django_settings_scanner/fixtures/settings_dev.py`: Test fixture for dev settings override
- `tests/test_django_settings_scanner/fixtures/settings_dynamic.py`: Test fixture for dynamic imports

### Modified Files

- `upcast/django_settings_scanner/__init__.py`: Export new `scan_settings_definitions` function
- `upcast/django_settings_scanner/ast_utils.py`: Add helper functions for definition detection
- `upcast/django_settings_scanner/settings_parser.py`: Add `SettingsDefinition`, `SettingsModule` dataclasses
- `upcast/django_settings_scanner/checker.py`: Extend `DjangoSettingsChecker` to track definitions
- `upcast/django_settings_scanner/export.py`: Update output format to include definitions section
- `upcast/django_settings_scanner/cli.py`: Add CLI flags for filtering output
- `openspec/specs/django-settings-scanner/spec.md`: Add new requirements for definition detection

### Modified Specs

- `openspec/changes/enhance-django-settings-scanner/specs/django-settings-scanner/spec.md`:
  - ADDED: Requirements for settings definition detection
  - ADDED: Requirements for value inference
  - ADDED: Requirements for inheritance tracking
  - ADDED: Requirements for dynamic import detection
  - MODIFIED: Output format requirement to include definitions section

### Dependencies

- No new external dependencies (reuse existing astroid)
- Leverage existing `upcast.common` utilities

### Backward Compatibility

**Compatible**: The enhanced output includes usages in the same format as before, just with an additional `definitions` section at the top. Existing tools that only parse the `usages` section will continue to work.

Optional CLI flags allow filtering:

- `--definitions-only`: Output only definitions (new format)
- `--usages-only`: Output only usages (existing format, maintains full backward compatibility)
- Default: Output both (enhanced format)

## Alternatives Considered

1. **Separate scanner tool** (`scan-django-settings-definitions`):

   - **Rejected**: Better to have unified understanding of settings in one tool
   - Users want to see definitions and usages together, not in separate commands

2. **Parse settings.py only** (no path-based detection):

   - **Rejected**: Django projects commonly split settings into multiple modules
   - Path-based detection with import tracking provides better coverage

3. **Runtime inspection** (import settings module and inspect):

   - **Rejected**: Requires Django environment setup, can trigger side effects
   - Static analysis is safer and works without environment configuration

4. **Regex-based parsing** instead of AST:

   - **Rejected**: Cannot handle complex expressions, inheritance, or dynamic patterns
   - AST analysis provides accurate parsing and value inference

5. **Store values as strings** (no type information):
   - **Rejected**: Loses important type information (bool vs string "False")
   - Type inference helps with validation and migration

## Open Questions

1. **Settings module detection accuracy**:

   - Path-based (`settings/`, `config/`) may catch non-settings files or miss custom locations
   - **Recommendation**: Start with path-based + import tracking, add `--include-module` flag for custom paths
   - **Trade-off**: Better to over-detect (宁可多扫描也不要少扫描) and let users filter, than miss actual settings

2. **Dynamic import support depth**:

   - Should we support all importlib patterns or just common ones?
   - **Recommendation**: Support common patterns first (f-strings with env vars), document limitations
   - Users can extend with custom patterns if needed

3. **Value inference limits**:

   - Complex expressions (e.g., `BASE_DIR = Path(__file__).resolve().parent.parent`) may not resolve
   - **Recommendation**: Mark as `<dynamic>` with expression text, don't attempt full evaluation
   - Attempting to evaluate could trigger side effects or errors

4. **Override chain representation**:

   - If `prod.py` imports from `dev.py` which imports from `base.py`, show full chain?
   - **Recommendation**: Show direct override only (`overrides: settings.dev`), not full chain
   - Users can trace chain manually if needed, keeps output simple

5. **Circular imports**:

   - What if settings modules have circular imports?
   - **Recommendation**: Detect and warn, skip circular references in output
   - Circular imports in settings are rare and indicate configuration smell

6. **Module path format**:

   - Use Python module path (`settings.base`) or file path (`settings/base.py`)?
   - **Recommendation**: Python module path (requested: "用模块路径做 key")
   - More consistent with Python conventions, easier to map to imports

7. **Performance with large projects**:
   - Scanning all Python files for settings modules could be slow
   - **Recommendation**: Add caching for settings module detection, parallel file processing
   - Optimize in follow-up if needed based on real-world performance data

## Success Criteria

- [ ] Detect settings definitions in files matching `settings/` or `config/` path patterns
- [ ] Convert file paths to Python module paths (e.g., `myproject/settings/base.py` → `myproject.settings.base`)
- [ ] Extract uppercase variable assignments with values
- [ ] Infer literal values (bool, int, float, string, list, dict)
- [ ] Mark dynamic values as `<dynamic>` with expression text
- [ ] Detect `from .base import *` inheritance patterns
- [ ] Track which settings override others (show `overrides` field)
- [ ] Detect `importlib.import_module()` dynamic import patterns
- [ ] Output definitions grouped by module path
- [ ] Output usages in existing format (backward compatible)
- [ ] Support `--definitions-only` and `--usages-only` CLI flags
- [ ] 85%+ test coverage for new definition parsing functionality
- [ ] All existing tests continue to pass (no regressions)
- [ ] Documentation updated with examples of new output format
