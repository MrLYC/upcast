# Design: Django Settings Scanner

## Overview

The Django Settings Scanner analyzes Python codebases to detect and aggregate usage of Django's `settings` object from `django.conf`. It uses astroid for semantic AST analysis to accurately distinguish Django settings from other similarly-named objects.

## Architecture Decisions

### 1. Semantic Analysis with Astroid

**Decision**: Use astroid for type inference instead of basic AST parsing

**Rationale**:

- **Accuracy**: Can resolve imports and distinguish `django.conf.settings` from `myapp.settings`
- **Alias Handling**: Supports `from django.conf import settings as config`
- **Consistency**: Matches existing scanner implementations (django_model_scanner, env_var_scanner, prometheus_metrics_scanner)
- **Robustness**: Handles complex import patterns including star imports

**Trade-offs**:

- ✅ Zero false positives from non-Django settings objects
- ✅ Handles refactored imports transparently
- ⚠️ Slower than regex (acceptable for development tools)
- ⚠️ Requires astroid dependency (already in project)

### 2. Three Access Pattern Detection

**Decision**: Support attribute access, getattr(), and hasattr()

**Rationale**:

- **Attribute Access** (`settings.KEY`): Most common pattern, 95%+ of usage
- **getattr()**: Used for dynamic configuration, optional features with defaults
- **hasattr()**: Used for feature flags and conditional behavior

**Pattern Recognition**:

```python
# Pattern 1: Attribute Access
node = ast.Attribute(value=<settings>, attr="KEY")
# Detection: Check if value resolves to django.conf.settings

# Pattern 2: getattr()
node = ast.Call(func=<getattr>, args=[<settings>, "KEY", default])
# Detection: Check first arg resolves to django.conf.settings

# Pattern 3: hasattr()
node = ast.Call(func=<hasattr>, args=[<settings>, "KEY"])
# Detection: Check first arg resolves to django.conf.settings
```

**Excluded Patterns**:

- ❌ `settings["KEY"]` - Not valid Django settings API
- ❌ `settings.__dict__` - Internal implementation detail
- ❌ `vars(settings)` - Rare, edge case

### 3. Aggregation by Variable Name

**Decision**: Group all usages by settings variable name as the primary key

**Rationale**:

- **User Goal**: "Where is DATABASE_URL used?" not "What settings are in file X?"
- **Usage Pattern**: Configuration reviews happen per-variable
- **Output Size**: 50-200 unique settings << 1000s of files in large projects
- **Deduplicated**: Count shows usage frequency immediately

**Data Structure**:

```python
@dataclass
class SettingsUsage:
    file: str           # Relative path from project root
    line: int           # Line number (1-based)
    column: int         # Column number (0-based)
    pattern: str        # "attribute_access" | "getattr" | "hasattr"
    code: str           # Source code snippet

@dataclass
class SettingsVariable:
    name: str                    # Variable name (e.g., "DATABASES")
    count: int                   # Total usage count
    locations: list[SettingsUsage]  # All usages sorted by file, line
```

### 4. Strict Module Validation

**Decision**: Only accept `settings` imported from `django.conf`

**Rationale**:

- **No False Positives**: Eliminates confusion with project-local settings modules
- **Semantic Clarity**: `django.conf.settings` is the official API
- **Explicit Scope**: Scanner purpose is "find Django configuration usage"

**Implementation**:

```python
def is_django_settings(node: nodes.Name) -> bool:
    """Check if a Name node refers to django.conf.settings."""
    try:
        for inferred in node.infer():
            # Check if it's the settings object from django.conf
            if (isinstance(inferred, nodes.Module) and
                inferred.qname() == "django.conf.settings"):
                return True
            # Handle LazySettings instance
            if (isinstance(inferred, astroid.Instance) and
                inferred.qname() == "django.conf.LazySettings"):
                return True
    except astroid.InferenceError:
        pass
    return False
```

### 5. Module Structure

**Decision**: Follow the established 5-file scanner pattern

**Files**:

1. **`ast_utils.py`**: Low-level AST pattern detection

   - `is_django_settings(node)` - Validate settings origin
   - `is_settings_attribute_access(node)` - Detect `settings.KEY`
   - `is_settings_getattr(node)` - Detect `getattr(settings, "KEY")`
   - `is_settings_hasattr(node)` - Detect `hasattr(settings, "KEY")`
   - `extract_setting_name(node)` - Extract variable name from any pattern

2. **`settings_parser.py`**: High-level parsing logic

   - `parse_settings_usage(node)` - Parse any pattern into SettingsUsage
   - `SettingsUsage` dataclass
   - `SettingsVariable` dataclass

3. **`checker.py`**: AST visitor and aggregation

   - `DjangoSettingsChecker` - NodeVisitor that collects all usages
   - `visit_Attribute()` - Handle attribute access
   - `visit_Call()` - Handle getattr/hasattr
   - `_register_usage()` - Aggregate by variable name

4. **`export.py`**: YAML formatting

   - `format_settings_output()` - Convert dict to YAML structure
   - `export_to_yaml()` - Write to file
   - `export_to_yaml_string()` - Return YAML string

5. **`cli.py`**: Command-line interface
   - `scan_django_settings()` - Main entry point
   - File discovery and filtering
   - Progress reporting

**Rationale**: Proven pattern from 3 existing scanners, clear separation of concerns

### 6. YAML Output Format

**Decision**: Use human-readable YAML with sorted keys

**Format**:

```yaml
variable_name:
  count: N
  locations:
    - file: path/to/file.py
      line: 10
      column: 5
      pattern: attribute_access
      code: "settings.VARIABLE_NAME"
```

**Sorting**:

1. Variables sorted alphabetically (predictable, git-friendly)
2. Locations sorted by (file, line) for logical grouping

**Rationale**:

- **Consistency**: Matches other scanners' YAML output
- **Readability**: Easy to review in PRs and diffs
- **Tooling**: Standard YAML parsers for automation
- **Git-Friendly**: Sorted keys reduce merge conflicts

### 7. CLI Integration

**Decision**: Add `scan-django-settings` command to main CLI

**Implementation**:

```python
# upcast/main.py
@main.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("-o", "--output", help="Output YAML file path")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def scan_django_settings_cmd(path: str, output: str | None, verbose: bool) -> None:
    """Scan Django project for settings usage."""
    from upcast.django_settings_scanner import scan_django_settings
    scan_django_settings(path, output, verbose)
```

**Rationale**: Consistent with `scan-prometheus-metrics`, `analyze-django-models` commands

## Testing Strategy

### Test Coverage

1. **Unit Tests** (tests/test_django_settings_scanner/)

   - `test_ast_utils.py` - Pattern detection functions
   - `test_settings_parser.py` - Parsing logic and dataclasses
   - `test_checker.py` - AST visitor and aggregation
   - `test_export.py` - YAML formatting
   - `test_cli.py` - CLI functionality

2. **Test Fixtures** (tests/test_django_settings_scanner/fixtures/)
   - `simple_settings.py` - Basic attribute access patterns
   - `getattr_patterns.py` - Dynamic access with getattr/hasattr
   - `aliased_imports.py` - Import aliases
   - `non_django_settings.py` - Should NOT be detected (false positive checks)
   - `mixed_settings.py` - Django + non-Django settings objects

### Validation

- ✅ 100% test pass rate
- ✅ ruff linting clean
- ✅ No false positives in non_django_settings.py
- ✅ Correct aggregation (same variable, multiple files)
- ✅ All three patterns detected

## Implementation Order

1. **Foundation** (ast_utils.py, settings_parser.py)

   - Pattern detection functions
   - Data structures

2. **Core Logic** (checker.py)

   - AST visitor
   - Aggregation logic

3. **I/O** (export.py, cli.py)

   - YAML formatting
   - File discovery
   - CLI command

4. **Integration** (main.py, **init**.py)

   - Add CLI command
   - Public API

5. **Testing** (tests/)
   - Unit tests for each module
   - Fixtures for all patterns

## Risk Mitigation

### Risk: Performance on Large Codebases

**Mitigation**:

- File filtering (exclude venv/, node_modules/, **pycache**/)
- Incremental scanning (scan changed files only)
- Early exit on parse errors

### Risk: False Positives from Non-Django Settings

**Mitigation**:

- Strict type inference with astroid
- Test fixtures with negative cases
- Require explicit django.conf origin

### Risk: Dynamic Variable Names

**Limitation**: Cannot resolve runtime-computed names:

```python
key = get_key_from_database()
value = getattr(settings, key)  # ❌ Cannot extract "key"
```

**Mitigation**:

- Document limitation in README
- Log warning for unresolvable patterns
- Still record the usage with placeholder name "DYNAMIC"

## Success Metrics

- ✅ Zero false positives on non-Django settings objects
- ✅ Detects all three access patterns (attribute, getattr, hasattr)
- ✅ Handles 1000+ file Django projects in <30 seconds
- ✅ 45+ unit tests passing
- ✅ CLI integration complete
