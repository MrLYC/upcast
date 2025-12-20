# Tasks: enhance-django-settings-scanner

## Implementation Tasks

### Phase 1: Data Structures and Module Detection

- [ ] **Define new data structures**: Add to `settings_parser.py`:

  - `SettingsDefinition`: Dataclass for a single settings variable definition (name, value, line, type, module_path, overrides)
  - `SettingsModule`: Dataclass for a settings module (module_path, definitions, star_imports, dynamic_imports)
  - `DynamicImport`: Dataclass for dynamic import patterns (pattern, base_module, file, line)
  - Include proper type hints for all fields

- [ ] **Add settings module detection**: Create `definition_parser.py` with:

  - `is_settings_module(file_path: str) -> bool`: Check if file path contains `settings/` or `config/`
  - `file_path_to_module_path(file_path: str, base_path: str) -> str`: Convert file path to Python module path
  - Handle both absolute and relative paths
  - Support nested structures (e.g., `myproject/settings/dev.py` → `myproject.settings.dev`)

- [ ] **Test module detection**: Write `tests/test_django_settings_scanner/test_definition_parser.py`:
  - Test `is_settings_module()` with various path patterns
  - Test `file_path_to_module_path()` conversion
  - Test edge cases (no base path, absolute paths, Windows paths)

### Phase 2: Uppercase Assignment Detection

- [ ] **Implement uppercase assignment detection**: Add to `definition_parser.py`:

  - `is_uppercase_assignment(node: nodes.Assign) -> bool`: Check if target is uppercase identifier
  - Validate: all uppercase, allows underscores, excludes dunder names (`__name__`, `__file__`)
  - Handle multiple targets (e.g., `A = B = value`)

- [ ] **Add AST utilities**: Extend `ast_utils.py`:

  - `is_uppercase_identifier(name: str) -> bool`: Validate uppercase naming convention
  - `extract_assignment_target(node: nodes.Assign) -> str | None`: Get variable name from assignment

- [ ] **Test uppercase detection**: Extend `test_definition_parser.py`:
  - Test valid uppercase names: `DEBUG`, `DATABASE_URL`, `CORS_ALLOWED_ORIGINS`
  - Test invalid names (reject): `debug`, `Debug`, `__name__`, `_internal`
  - Test multiple assignment targets
  - Test annotated assignments: `DEBUG: bool = True`

### Phase 3: Value Inference

- [ ] **Implement value inference**: Add to `definition_parser.py`:

  - `infer_setting_value(node: nodes.NodeNG) -> dict`: Infer value and type from AST node
  - Handle literals: `True`, `False`, `None`, integers, floats, strings
  - Handle containers: lists, tuples, dicts, sets
  - Handle expressions: mark as `<dynamic>` with expression text
  - Return dict with `value`, `type`, and optional `expression` fields

- [ ] **Handle literal types**: Add inference for:

  - **Booleans**: `DEBUG = True` → `{"value": true, "type": "literal"}`
  - **Integers**: `PORT = 8000` → `{"value": 8000, "type": "int"}`
  - **Floats**: `TIMEOUT = 30.5` → `{"value": 30.5, "type": "float"}`
  - **Strings**: `URL = "https://..."` → `{"value": "https://...", "type": "string"}`
  - **None**: `CACHE = None` → `{"value": null, "type": "none"}`

- [ ] **Handle container types**: Add inference for:

  - **Lists**: `APPS = ["app1", "app2"]` → `{"value": ["app1", "app2"], "type": "list"}`
  - **Tuples**: Same as lists but mark as tuple
  - **Dicts**: `DB = {"host": "localhost"}` → `{"value": {...}, "type": "dict"}`
  - **Sets**: `ALLOWED = {"a", "b"}` → `{"value": ["a", "b"], "type": "set"}`
  - Handle nested containers (e.g., list of dicts)

- [ ] **Handle dynamic expressions**: Add inference for:

  - **Function calls**: `BASE_DIR = Path(__file__)` → `{"value": "<dynamic>", "type": "call", "expression": "Path(__file__)"}`
  - **Environment variables**: `KEY = os.environ.get("KEY")` → `{"value": "<dynamic>", "type": "dynamic", "expression": "os.environ.get('KEY')"}`
  - **Binary operations**: `TIMEOUT = 5 * 60` → Try to evaluate, fallback to dynamic
  - **Unresolvable**: Any complex expression → `{"value": "<dynamic>", "type": "dynamic", "expression": "..."}`

- [ ] **Test value inference**: Extend `test_definition_parser.py`:
  - Test literal inference for all types
  - Test container inference with nested structures
  - Test dynamic expression handling
  - Test error handling for unparseable values
  - Create fixture: `tests/test_django_settings_scanner/fixtures/settings_values.py` with various value types

### Phase 4: Inheritance Detection

- [ ] **Implement star import detection**: Add to `definition_parser.py`:

  - `detect_star_imports(module: nodes.Module) -> list[str]`: Find `from X import *` patterns
  - Resolve relative imports to module paths
  - Example: In `settings/dev.py`, `from .base import *` → resolve to `settings.base`
  - Handle absolute imports: `from myproject.settings.base import *`

- [ ] **Add import resolution utilities**: Extend `ast_utils.py`:

  - `resolve_relative_import(current_module: str, import_level: int, import_module: str) -> str`: Convert relative to absolute
  - Example: In `myproject.settings.dev`, `from ..config import *` → `myproject.config`
  - Handle different import levels (`.`, `..`, `...`)

- [ ] **Track override relationships**: Add to `definition_parser.py`:

  - `mark_overrides(modules: dict[str, SettingsModule]) -> None`: Identify which settings override others
  - If module has star import from base, mark subsequent uppercase assignments as overrides
  - Store override source in `SettingsDefinition.overrides` field

- [ ] **Test inheritance tracking**: Extend `test_definition_parser.py`:
  - Test star import detection
  - Test relative import resolution
  - Test override marking
  - Create fixtures:
    - `fixtures/settings_base.py`: Base settings with DEBUG, APPS
    - `fixtures/settings_dev.py`: Dev settings with `from .base import *` and override DEBUG

### Phase 5: Dynamic Import Detection

- [ ] **Implement dynamic import detection**: Add to `definition_parser.py`:

  - `detect_dynamic_imports(module: nodes.Module) -> list[DynamicImport]`: Find importlib patterns
  - Detect: `importlib.import_module(...)` calls
  - Extract f-string or concatenation patterns
  - Example: `importlib.import_module(f"settings.{env}")` → base_module="settings"

- [ ] **Parse dynamic import arguments**: Add helpers:

  - `extract_import_pattern(call_node: nodes.Call) -> str | None`: Get pattern string from argument
  - Handle f-strings: `f"settings.{env}"` → extract `settings.{env}`
  - Handle string concatenation: `"settings." + profile`
  - Handle format calls: `"settings.{}".format(env)`

- [ ] **Extract base module**: Add helper:

  - `extract_base_module(pattern: str) -> str`: Get module before dynamic part
  - Example: `settings.{env}` → `settings`
  - Example: `{project}.config` → cannot extract (too dynamic)

- [ ] **Test dynamic import detection**: Extend `test_definition_parser.py`:
  - Test importlib.import_module detection
  - Test pattern extraction from f-strings
  - Test base module extraction
  - Create fixture: `fixtures/settings_dynamic.py` with dynamic import patterns

### Phase 6: Settings Definition Parsing

- [ ] **Implement main parsing function**: Add to `definition_parser.py`:

  - `parse_settings_module(file_path: str, base_path: str) -> SettingsModule`: Parse entire settings file
  - Scan for uppercase assignments
  - Infer values for each assignment
  - Detect star imports
  - Detect dynamic imports
  - Build SettingsModule object

- [ ] **Integrate with checker**: Extend `checker.py`:

  - Add `definitions: dict[str, SettingsModule]` field to store parsed modules
  - Add `scan_definitions(self, base_path: str) -> None`: Scan for settings modules in project
  - Call `parse_settings_module()` for each detected settings file
  - Integrate with existing `check_file()` workflow

- [ ] **Add definition tracking**: Extend `DjangoSettingsChecker`:

  - `get_definitions_by_module(self) -> dict[str, SettingsModule]`: Return all definitions
  - `get_all_defined_settings(self) -> set[str]`: Return unique setting names across all modules
  - Enable cross-referencing definitions with usages

- [ ] **Test integration**: Extend `tests/test_django_settings_scanner/test_checker.py`:
  - Test `scan_definitions()` finds settings modules
  - Test `parse_settings_module()` extracts definitions correctly
  - Test override tracking across multiple modules
  - Test integration with existing usage tracking

### Phase 7: Export Format Enhancement

- [ ] **Update export format**: Modify `export.py`:

  - Add `format_definitions_output(modules: dict[str, SettingsModule]) -> dict`: Format definitions section
  - Group definitions by module path
  - Include value, line, type, overrides for each definition
  - Add `dynamic_imports` section if any detected

- [ ] **Extend YAML structure**: Update `export_to_yaml()`:

  - Add `definitions` section at top level
  - Keep existing `usages` section (backward compatible)
  - Add optional `dynamic_imports` section
  - Maintain alphabetical sorting within each section

- [ ] **Add filtering options**: Add helper functions:

  - `export_definitions_only(modules: dict[str, SettingsModule], output_path: str) -> None`: Export only definitions
  - `export_usages_only(settings_dict: dict[str, SettingsVariable], output_path: str) -> None`: Export only usages (existing format)
  - `export_combined(modules: dict[str, SettingsModule], settings_dict: dict[str, SettingsVariable], output_path: str) -> None`: Export both

- [ ] **Test export format**: Extend `tests/test_django_settings_scanner/test_export.py`:
  - Test `format_definitions_output()` structure
  - Test combined output format
  - Test definitions-only format
  - Test usages-only format (backward compatibility)
  - Test dynamic_imports section
  - Verify YAML validity and sorting

### Phase 8: CLI Integration

- [ ] **Add CLI flags**: Extend `cli.py`:

  - Add `--definitions-only` flag: Output only definitions section
  - Add `--usages-only` flag: Output only usages section (existing behavior)
  - Add `--no-usages` flag: Skip usage scanning (definitions only, faster)
  - Add `--no-definitions` flag: Skip definition scanning (usages only, existing behavior)
  - Default: Scan and output both

- [ ] **Update scan function**: Modify `scan_django_settings()`:

  - Add parameters for definition scanning and filtering
  - Orchestrate both definition and usage scanning
  - Apply CLI flags to control output format
  - Maintain backward compatibility (default behavior unchanged)

- [ ] **Update CLI help text**: Extend command documentation:

  - Document new flags with examples
  - Show example output for each mode
  - Clarify backward compatibility

- [ ] **Test CLI integration**: Extend `tests/test_django_settings_scanner/test_cli.py`:
  - Test `--definitions-only` flag
  - Test `--usages-only` flag
  - Test combined output (default)
  - Test filtering flags with fixtures
  - Test backward compatibility (no flags = same as before + definitions)

### Phase 9: End-to-End Testing

- [ ] **Create comprehensive fixtures**: Add to `tests/test_django_settings_scanner/fixtures/`:

  - `project_settings/`: Directory structure simulating real Django project
    - `settings/__init__.py`: Empty or dynamic import logic
    - `settings/base.py`: Base settings with common variables
    - `settings/dev.py`: Dev overrides with `from .base import *`
    - `settings/prod.py`: Prod overrides
    - `settings/test.py`: Test overrides
  - `config_settings/`: Alternative structure with `config/` directory
  - `dynamic_settings/`: Project with dynamic import patterns

- [ ] **Write integration tests**: Create `tests/test_django_settings_scanner/test_integration_definitions.py`:

  - Test full scan of project_settings directory
  - Test definition extraction from all modules
  - Test override chain tracking (base → dev → prod)
  - Test dynamic import detection
  - Test combined definitions + usages output
  - Test filtering modes (definitions-only, usages-only)

- [ ] **Verify output correctness**: Add assertions for:

  - All settings from base.py detected
  - Overrides correctly marked in dev.py and prod.py
  - Values inferred correctly (literals vs dynamic)
  - Dynamic imports listed in output
  - Usages cross-referenced with definitions
  - YAML structure matches specification

- [ ] **Test edge cases**: Add tests for:
  - Settings modules with circular imports (warning + skip)
  - Settings files outside typical paths (manual include)
  - Dynamic imports that cannot be resolved
  - Mixed usage of aliased and direct settings imports
  - Large settings files (performance)

### Phase 10: Documentation and Validation

- [ ] **Update module docstrings**: Add comprehensive docstrings to:

  - `definition_parser.py`: Explain definition detection and value inference
  - Updated functions in `checker.py`, `export.py`, `cli.py`
  - Data structures in `settings_parser.py`

- [ ] **Create usage examples**: Add examples in docstrings and tests:

  - Example 1: Basic settings module with definitions
  - Example 2: Settings with inheritance (base → dev)
  - Example 3: Dynamic import pattern
  - Example 4: Combined definitions + usages output

- [ ] **Update CLI help**: Enhance command documentation:

  - Add examples showing new output format
  - Document each CLI flag with use cases
  - Show migration path from old to new usage

- [ ] **Run full test suite**: Execute comprehensive validation:

  - `uv run pytest tests/test_django_settings_scanner/ -v`
  - `uv run pytest` (ensure no regressions in other scanners)
  - Verify 85%+ test coverage for new code
  - Run `uv run ruff check upcast/django_settings_scanner/`
  - Fix any linting issues

- [ ] **Update README.md**: Document new capability:

  - Add section on settings definition detection
  - Show example output with definitions and usages
  - Explain common use cases (inheritance, dynamic imports)
  - Document CLI flags and filtering options

- [ ] **Create spec delta**: Add `openspec/changes/enhance-django-settings-scanner/specs/django-settings-scanner/spec.md`:

  - ADDED requirements for definition detection
  - ADDED requirements for value inference
  - ADDED requirements for inheritance tracking
  - ADDED requirements for dynamic import detection
  - MODIFIED requirement for output format (add definitions section)
  - Include scenarios for each new requirement

- [ ] **Validate with OpenSpec**: Run validation:
  - `openspec validate enhance-django-settings-scanner --strict`
  - Fix any validation errors
  - Ensure all requirements have scenarios
  - Verify spec deltas are correctly formatted

## Validation Checkpoints

After each phase:

1. Run relevant tests: `uv run pytest tests/test_django_settings_scanner/test_definition_parser.py -v`
2. Check code style: `uv run ruff check upcast/django_settings_scanner/`
3. Verify no regressions: `uv run pytest tests/test_django_settings_scanner/`

Final validation:

1. Full test suite: `uv run pytest tests/test_django_settings_scanner/ -v` (all tests passing)
2. Coverage check: `uv run pytest tests/test_django_settings_scanner/ --cov=upcast.django_settings_scanner --cov-report=term-missing` (85%+)
3. Integration test with real Django project settings
4. Verify YAML output matches specification examples
5. Test backward compatibility: existing usage-only tests still pass
6. Run OpenSpec validation: `openspec validate enhance-django-settings-scanner --strict`
7. Manual review of output format with team
