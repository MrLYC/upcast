# Design: enhance-django-settings-scanner

## Architecture Overview

This enhancement extends the Django settings scanner from a **usage-only detector** to a **comprehensive settings analyzer** that tracks both definitions and usages. The design follows the established scanner pattern while adding a new definition parsing subsystem.

```
┌─────────────────────────────────────────────────────────────┐
│                    Django Settings Scanner                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────┐              ┌───────────────────┐       │
│  │  Usage Path   │              │  Definition Path  │       │
│  │  (Existing)   │              │     (New)         │       │
│  └───────┬───────┘              └─────────┬─────────┘       │
│          │                                │                  │
│          ▼                                ▼                  │
│  ┌───────────────┐              ┌───────────────────┐       │
│  │  ast_utils    │◄─────────────┤ definition_parser │       │
│  │               │  shared      │                   │       │
│  │ • is_django_  │  utilities   │ • is_settings_    │       │
│  │   settings()  │              │   module()        │       │
│  │ • is_settings_│              │ • parse_settings_ │       │
│  │   attribute() │              │   module()        │       │
│  │ • extract_    │              │ • infer_setting_  │       │
│  │   setting_    │              │   value()         │       │
│  │   name()      │              │ • detect_star_    │       │
│  └───────┬───────┘              │   imports()       │       │
│          │                      │ • detect_dynamic_ │       │
│          │                      │   imports()       │       │
│          │                      └─────────┬─────────┘       │
│          │                                │                  │
│          ▼                                ▼                  │
│  ┌──────────────────────────────────────────────┐           │
│  │            DjangoSettingsChecker             │           │
│  │                                              │           │
│  │  • usages: dict[str, SettingsVariable]      │           │
│  │  • definitions: dict[str, SettingsModule]   │           │
│  │                                              │           │
│  │  Methods:                                    │           │
│  │  • check_file() - scan for usages           │           │
│  │  • scan_definitions() - scan for defs       │           │
│  │  • get_usages_by_name()                     │           │
│  │  • get_definitions_by_module()              │           │
│  └──────────────────┬───────────────────────────┘           │
│                     │                                        │
│                     ▼                                        │
│  ┌──────────────────────────────────────────────┐           │
│  │                   export.py                  │           │
│  │                                              │           │
│  │  • format_definitions_output()              │           │
│  │  • format_usages_output() (existing)        │           │
│  │  • export_combined() / separate modes       │           │
│  └──────────────────┬───────────────────────────┘           │
│                     │                                        │
│                     ▼                                        │
│  ┌──────────────────────────────────────────────┐           │
│  │                    CLI                       │           │
│  │                                              │           │
│  │  scan-django-settings [path]                │           │
│  │    --definitions-only                       │           │
│  │    --usages-only                            │           │
│  │    --no-usages / --no-definitions           │           │
│  └──────────────────────────────────────────────┘           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Key Design Decisions

### 1. Settings Module Detection Strategy

**Decision**: Use **hybrid detection** combining path-based heuristics with import tracking.

**Rationale**:

- **Path-based** (`settings/`, `config/`) is fast and covers 90% of Django projects
- **Import tracking** catches non-standard locations (e.g., `myproject/core/configuration.py`)
- User feedback: "宁可多扫描也不要少扫描" - prefer over-detection over missing settings

**Implementation**:

```python
def is_settings_module(file_path: str) -> bool:
    """Detect if file is likely a settings module."""
    # Primary: path-based detection
    path_lower = file_path.lower()
    if '/settings/' in path_lower or '/config/' in path_lower:
        return True

    # Secondary: check if imported by usage sites
    # (implemented in checker phase - track imports)
    return False
```

**Trade-offs**:

- ✅ High recall (catches most settings files)
- ✅ Fast initial scan
- ⚠️ May include false positives (non-settings files in `config/`)
- ⚠️ May miss custom locations without import tracking

**Mitigations**:

- Add `--include-module <path>` CLI flag for custom paths
- Document detection logic clearly
- Provide `--verbose` output showing which files were detected

### 2. Value Inference Approach

**Decision**: Use **astroid literal inference** with fallback to `<dynamic>` marker.

**Rationale**:

- Astroid can safely infer literals without evaluation (no side effects)
- Complex expressions (function calls, env vars) cannot be resolved statically
- Marking as `<dynamic>` with expression text is honest and useful

**Implementation**:

```python
def infer_setting_value(node: nodes.NodeNG) -> dict:
    """Infer value and type from AST node."""
    # Try literal inference first
    try:
        inferred = node.inferred()
        if isinstance(inferred, nodes.Const):
            return {
                "value": inferred.value,
                "type": type(inferred.value).__name__
            }
        elif isinstance(inferred, (nodes.List, nodes.Tuple)):
            # Recursively infer elements
            ...
    except Exception:
        pass

    # Fallback to dynamic - wrap expression in backticks
    return {
        "value": f"`{node.as_string()}`",
        "type": "dynamic"
    }
```

**Examples**:

- `DEBUG = True` → `{"value": true, "type": "bool"}`
- `PORT = 8000` → `{"value": 8000, "type": "int"}`
- `SECRET = os.environ.get("KEY")` → `{"value": "`os.environ.get('KEY')`", "type": "dynamic"}`

**Trade-offs**:

- ✅ Safe (no code execution)
- ✅ Accurate for common cases (literals, containers)
- ✅ Honest about limitations (shows expression wrapped in backticks)
- ⚠️ Cannot resolve computed values (e.g., `BASE_DIR = Path(__file__).parent`)

### 3. Inheritance Tracking Design

**Decision**: Track **direct overrides only** (not full inheritance chain).

**Rationale**:

- Django settings commonly have 2-level hierarchy: base → environment
- Full chain (base → common → dev → local) is rare and complex
- Direct override information is most useful for understanding configuration

**Data Structure**:

```python
@dataclass
class SettingsDefinition:
    name: str
    value: Any
    line: int
    type: str
    module_path: str
    overrides: str | None = None  # Direct parent module path
```

**Example**:

```yaml
definitions:
  settings.base:
    DEBUG:
      value: false
      line: 10
  settings.dev:
    DEBUG:
      value: true
      line: 5
      overrides: settings.base # Direct override
```

**Trade-offs**:

- ✅ Simple and clear
- ✅ Covers 95% of Django patterns
- ✅ Easy to implement and test
- ⚠️ Doesn't show multi-level chains (rare)

**Future Enhancement**:
Could add `override_chain: [settings.base, settings.common]` if needed.

### 4. Dynamic Import Support

**Decision**: **Document patterns** rather than fully resolve them.

**Rationale**:

- Dynamic imports by definition cannot be fully resolved statically
- Common patterns (importlib + f-strings) are detectable
- Documenting presence helps with understanding, even if values unknown

**Detection Logic**:

```python
def detect_dynamic_imports(module: nodes.Module) -> list[DynamicImport]:
    """Find importlib.import_module patterns."""
    imports = []
    for node in module.nodes_of_type(nodes.Call):
        if is_importlib_call(node):
            pattern = extract_pattern_from_fstring(node.args[0])
            base = extract_base_module(pattern)
            imports.append(DynamicImport(
                pattern=pattern,
                base_module=base,
                file=module.file,
                line=node.lineno
            ))
    return imports
```

**Output Example**:

```yaml
dynamic_imports:
  - pattern: "importlib.import_module(f'settings.{profile}')"
    base_module: settings
    file: myproject/__init__.py
    line: 10
```

**Trade-offs**:

- ✅ Provides useful information about dynamic behavior
- ✅ Helps with understanding configuration loading
- ✅ Simple implementation (pattern matching)
- ⚠️ Cannot resolve actual module loaded at runtime
- ⚠️ Doesn't capture all possible dynamic patterns

### 5. Output Format Design

**Decision**: **Backward compatible** with optional sections.

**Rationale**:

- Existing users rely on `usages` format
- Adding `definitions` section at top doesn't break parsers that only read `usages`
- CLI flags allow filtering for specific needs

**Structure**:

```yaml
# New section (optional if no definitions found)
definitions:
  <module_path>:
    <VAR_NAME>:
      value: <inferred_value>
      line: <int>
      type: <type_string>
      overrides: <parent_module> # optional

# Optional section (only if dynamic imports detected)
dynamic_imports:
  - pattern: <string>
    base_module: <string>
    file: <path>
    line: <int>

# Existing section (unchanged structure)
usages:
  <VAR_NAME>:
    count: <int>
    locations:
      - file: <path>
        line: <int>
        column: <int>
        pattern: <pattern_type>
        code: <string>
```

**Backward Compatibility**:

- Old parsers reading only `usages`: ✅ Work unchanged
- Old CLI calls: ✅ Same output + new `definitions` section
- Filtering flags allow exact old behavior if needed

**CLI Filtering**:

- Default: Output both definitions and usages (new format)
- `--usages-only`: Output only usages (exact old format)
- `--definitions-only`: Output only definitions (new section)
- `--no-usages`: Skip usage scanning (faster, definitions only)
- `--no-definitions`: Skip definition scanning (old behavior)

### 6. Module Path Convention

**Decision**: Use **Python module paths** (e.g., `myproject.settings.dev`), not file paths.

**Rationale**:

- User request: "用模块路径做 key"
- Consistent with Python import conventions
- Easier to map to `from X import Y` statements
- More portable (no OS-specific path separators)

**Conversion Logic**:

```python
def file_path_to_module_path(file_path: str, base_path: str) -> str:
    """Convert file path to Python module path.

    Examples:
        /project/myapp/settings/base.py -> myapp.settings.base
        /project/config/settings.py -> config.settings
    """
    # Get relative path from base
    rel_path = Path(file_path).relative_to(base_path)

    # Remove .py extension
    module_path = rel_path.with_suffix('')

    # Convert path separators to dots
    return str(module_path).replace(os.sep, '.')
```

**Trade-offs**:

- ✅ Pythonic and familiar
- ✅ Works cross-platform
- ✅ Matches user expectation
- ⚠️ Requires accurate base path detection

## Data Flow

### Definition Scanning Flow

```
┌─────────────────┐
│  scan_django_   │
│  settings()     │
└────────┬────────┘
         │
         ├─────────────────┐
         │                 │
         ▼                 ▼
┌────────────────┐  ┌──────────────────┐
│ Scan for       │  │ Scan for         │
│ Definitions    │  │ Usages           │
│                │  │ (existing)       │
└────────┬───────┘  └─────────┬────────┘
         │                    │
         ▼                    │
┌────────────────────┐        │
│ For each Python    │        │
│ file in project:   │        │
│                    │        │
│ 1. is_settings_    │        │
│    module()?       │        │
│    ├─ Yes ────────►│        │
│    └─ No (skip)    │        │
└────────┬───────────┘        │
         │                    │
         ▼                    │
┌────────────────────┐        │
│ parse_settings_    │        │
│ module():          │        │
│                    │        │
│ 1. Parse AST       │        │
│ 2. Find uppercase  │        │
│    assignments     │        │
│ 3. Infer values    │        │
│ 4. Detect star     │        │
│    imports         │        │
│ 5. Detect dynamic  │        │
│    imports         │        │
└────────┬───────────┘        │
         │                    │
         ▼                    │
┌────────────────────┐        │
│ Build              │        │
│ SettingsModule     │        │
└────────┬───────────┘        │
         │                    │
         ▼                    ▼
┌──────────────────────────────┐
│ mark_overrides():            │
│                              │
│ For each module with star   │
│ imports, mark subsequent     │
│ definitions as overrides     │
└────────────┬─────────────────┘
             │
             ▼
┌──────────────────────────────┐
│ Aggregate:                   │
│                              │
│ definitions: dict[str,       │
│   SettingsModule]            │
│                              │
│ usages: dict[str,            │
│   SettingsVariable]          │
└────────────┬─────────────────┘
             │
             ▼
┌──────────────────────────────┐
│ export_combined():           │
│                              │
│ Format and output YAML       │
└──────────────────────────────┘
```

### Override Resolution Example

```python
# Input files:
# settings/base.py
DEBUG = False
ALLOWED_HOSTS = []

# settings/dev.py
from .base import *
DEBUG = True
```

**Processing Steps**:

1. Parse `settings/base.py`:

   ```python
   SettingsModule(
       module_path="settings.base",
       definitions={
           "DEBUG": SettingsDefinition(
               name="DEBUG",
               value=False,
               line=1,
               type="bool",
               module_path="settings.base",
               overrides=None
           ),
           "ALLOWED_HOSTS": ...
       },
       star_imports=[],
       dynamic_imports=[]
   )
   ```

2. Parse `settings/dev.py`:

   ```python
   SettingsModule(
       module_path="settings.dev",
       definitions={
           "DEBUG": SettingsDefinition(
               name="DEBUG",
               value=True,
               line=2,
               type="bool",
               module_path="settings.dev",
               overrides=None  # Not yet marked
           )
       },
       star_imports=["settings.base"],
       dynamic_imports=[]
   )
   ```

3. `mark_overrides()` processing:

   - Iterate through `settings.dev.definitions`
   - For each definition, check if name exists in any star_import module
   - If found, set `overrides` field:

   ```python
   settings.dev.definitions["DEBUG"].overrides = "settings.base"
   ```

4. Final output:
   ```yaml
   definitions:
     settings.base:
       DEBUG:
         value: false
         line: 1
         type: bool
     settings.dev:
       DEBUG:
         value: true
         line: 2
         type: bool
         overrides: settings.base
   ```

## Error Handling

### Circular Import Detection

```python
def detect_circular_imports(modules: dict[str, SettingsModule]) -> list[str]:
    """Detect circular imports in star imports."""
    visited = set()
    path = []

    def dfs(module_path: str) -> bool:
        if module_path in path:
            # Circular reference found
            return True
        if module_path in visited:
            return False

        visited.add(module_path)
        path.append(module_path)

        module = modules.get(module_path)
        if module:
            for star_import in module.star_imports:
                if dfs(star_import):
                    return True

        path.pop()
        return False

    # Check each module
    for module_path in modules:
        if dfs(module_path):
            return path.copy()

    return []

# Usage:
circular = detect_circular_imports(modules)
if circular:
    logger.warning(f"Circular import detected: {' -> '.join(circular)}")
    # Skip circular references in override marking
```

### Value Inference Fallback

```python
def infer_setting_value(node: nodes.NodeNG) -> dict:
    """Infer value with safe fallback."""
    try:
        # Attempt literal inference
        inferred = list(node.infer())

        if not inferred or all(i is astroid.Uninferable for i in inferred):
            raise InferenceException("Cannot infer")

        # Process inferred value
        ...

    except Exception as e:
        # Safe fallback: mark as dynamic
        logger.debug(f"Cannot infer value for {node.as_string()}: {e}")
        return {
            "value": "<dynamic>",
            "type": "dynamic",
            "expression": node.as_string()
        }
```

### Parsing Error Handling

```python
def parse_settings_module(file_path: str, base_path: str) -> SettingsModule | None:
    """Parse settings module with error handling."""
    try:
        # Parse file
        with open(file_path, 'r') as f:
            code = f.read()

        module = astroid.parse(code, path=file_path)

        # Extract definitions
        ...

    except SyntaxError as e:
        logger.warning(f"Syntax error in {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to parse {file_path}: {e}")
        return None
```

## Performance Considerations

### Scan Optimization

1. **Parallel file processing**: Process multiple settings files concurrently
2. **Early filtering**: Skip non-Python files before parsing
3. **Caching**: Cache module path resolution for repeated scans
4. **Lazy loading**: Only parse files when needed

### Memory Management

1. **Streaming**: Don't load all files into memory at once
2. **AST cleanup**: Release AST nodes after processing
3. **Result batching**: Process definitions in chunks for large projects

### Expected Performance

- Small project (< 10 files): < 1 second
- Medium project (< 100 files): < 5 seconds
- Large project (< 1000 files): < 30 seconds

Settings files are typically small and few in number, so performance should not be a significant concern.

## Testing Strategy

### Unit Tests

1. **Module detection**: Test path patterns, edge cases
2. **Value inference**: Test all type conversions, fallbacks
3. **Star import resolution**: Test relative/absolute imports
4. **Override marking**: Test single and multi-level
5. **Dynamic import detection**: Test common patterns

### Integration Tests

1. **Full project scan**: Simulate real Django project structure
2. **Output format**: Validate YAML structure and content
3. **CLI flags**: Test all filtering modes
4. **Backward compatibility**: Ensure old tests pass

### Fixtures

```
tests/test_django_settings_scanner/fixtures/
├── settings_base.py           # Base settings
├── settings_dev.py            # Dev overrides
├── settings_prod.py           # Prod overrides
├── settings_dynamic.py        # Dynamic imports
├── settings_complex_values.py # Various value types
└── project_structure/         # Full project simulation
    ├── myproject/
    │   └── settings/
    │       ├── __init__.py
    │       ├── base.py
    │       ├── dev.py
    │       └── prod.py
    └── config/
        └── settings.py
```

## Future Enhancements

1. **Type validation**: Check if usage types match definition types
2. **Unused settings**: Report settings defined but never used
3. **Environment-specific analysis**: Track which settings differ across environments
4. **Migration support**: Generate migration scripts when settings structure changes
5. **IDE integration**: Provide jump-to-definition for settings in code
6. **Documentation generation**: Auto-generate settings documentation from definitions
7. **Full chain tracking**: Support multi-level inheritance chains if needed
8. **Custom detection patterns**: Allow users to define custom settings module patterns
