# django-settings-scanner Specification

## Purpose

TBD - created by archiving change implement-django-settings-scanner. Update Purpose after archive.

## Requirements

### Requirement: Django Settings Import Detection

The system SHALL detect settings objects imported from `django.conf` using semantic type inference to distinguish Django's official settings from other similarly-named objects.

#### Scenario: Standard import pattern

- **WHEN** code uses `from django.conf import settings`
- **THEN** the system SHALL recognize `settings` as a Django settings object
- **AND** track all subsequent usages of this `settings` reference
- **AND** validate the import origin through astroid type inference

#### Scenario: Aliased import

- **WHEN** code uses `from django.conf import settings as config`
- **THEN** the system SHALL recognize `config` as a Django settings object
- **AND** track all usages of the aliased name
- **AND** resolve the alias to `django.conf.settings`

#### Scenario: Qualified import

- **WHEN** code uses `import django.conf` and references `django.conf.settings.KEY`
- **THEN** the system SHALL recognize the qualified access
- **AND** extract the settings variable name
- **AND** validate the module path is `django.conf`

#### Scenario: Exclude non-Django settings

- **WHEN** code defines a local `settings` variable or imports from non-django modules
- **EXAMPLES**: `settings = {}`, `from myapp.settings import KEY`
- **THEN** the system SHALL NOT detect these as Django settings
- **AND** produce zero false positives for non-Django code

### Requirement: Attribute Access Pattern Detection

The system SHALL detect direct attribute access to Django settings variables and extract the complete variable name.

#### Scenario: Simple attribute access

- **WHEN** code uses `settings.DATABASE_URL`
- **THEN** the system SHALL extract "DATABASE_URL" as the settings variable name
- **AND** record the file path, line number, and column number
- **AND** classify the pattern as "attribute_access"

#### Scenario: Chained attribute access

- **WHEN** code uses `settings.DATABASES['default']` or `settings.API.endpoint`
- **THEN** the system SHALL extract only the first-level attribute name
- **EXAMPLES**: Extract "DATABASES" from `settings.DATABASES['default']`
- **AND** ignore subsequent subscript or attribute operations

#### Scenario: Attribute access in expressions

- **WHEN** settings are used in conditional expressions or assignments
- **EXAMPLES**: `if settings.DEBUG:`, `db = settings.DATABASES`, `url = f"{settings.BASE_URL}/api"`
- **THEN** the system SHALL detect all attribute access regardless of context
- **AND** record each occurrence separately

### Requirement: getattr() Pattern Detection

The system SHALL detect dynamic settings access through `getattr()` calls and extract both the variable name and default value when present.

#### Scenario: getattr without default

- **WHEN** code uses `getattr(settings, "API_KEY")`
- **THEN** the system SHALL extract "API_KEY" as the settings variable name
- **AND** classify the pattern as "getattr"
- **AND** record default as None

#### Scenario: getattr with default value

- **WHEN** code uses `getattr(settings, "TIMEOUT", 30)` or `getattr(settings, "FEATURE_FLAG", False)`
- **THEN** the system SHALL extract the variable name from the second argument
- **AND** extract the default value from the third argument
- **AND** record both in the usage metadata

#### Scenario: getattr with variable name

- **WHEN** the second argument to getattr is a string literal
- **THEN** the system SHALL extract the variable name
- **AND** mark it as successfully extracted

#### Scenario: getattr with computed name

- **WHEN** the second argument to getattr is a variable or expression
- **EXAMPLES**: `getattr(settings, var_name)`, `getattr(settings, prefix + "_KEY")`
- **THEN** the system SHALL classify the usage as "getattr"
- **AND** record the variable name as "DYNAMIC"
- **AND** log a warning about unresolvable name

### Requirement: hasattr() Pattern Detection

The system SHALL detect settings existence checks through `hasattr()` calls, typically used for feature flags and optional configuration.

#### Scenario: hasattr for feature flags

- **WHEN** code uses `hasattr(settings, "FEATURE_ENABLED")`
- **THEN** the system SHALL extract "FEATURE_ENABLED" as the settings variable name
- **AND** classify the pattern as "hasattr"
- **AND** record the file location

#### Scenario: hasattr in conditionals

- **WHEN** hasattr is used in conditional expressions
- **EXAMPLES**: `if hasattr(settings, "CUSTOM_BACKEND"):`, `enabled = hasattr(settings, "NEW_FEATURE")`
- **THEN** the system SHALL detect the pattern
- **AND** extract the variable name from the second argument

#### Scenario: hasattr with computed name

- **WHEN** the second argument to hasattr is not a string literal
- **THEN** the system SHALL record the usage with name "DYNAMIC"
- **AND** log a warning about unresolvable name

### Requirement: Settings Usage Aggregation

The system SHALL aggregate all usages of each settings variable across the entire codebase, grouping by variable name with complete location tracking.

#### Scenario: Same variable, multiple files

- **WHEN** `settings.DATABASE_URL` is used in 3 different files
- **THEN** the system SHALL create one entry for "DATABASE_URL"
- **AND** include all 3 file locations in the locations list
- **AND** set count to 3

#### Scenario: Same variable, multiple patterns

- **WHEN** a variable is accessed via both `settings.KEY` and `getattr(settings, "KEY")`
- **THEN** the system SHALL group them under the same variable name
- **AND** record each usage with its specific pattern type
- **AND** increment count for each occurrence

#### Scenario: Multiple usages in same file

- **WHEN** `settings.DEBUG` is used 5 times in one file
- **THEN** the system SHALL record all 5 locations separately
- **AND** preserve line numbers for each usage
- **AND** set count to 5

#### Scenario: Location sorting

- **WHEN** formatting aggregated results
- **THEN** the system SHALL sort locations by file path first, then line number
- **AND** ensure deterministic output order
- **AND** make diffs git-friendly

### Requirement: YAML Output Format

The system SHALL export settings definitions and usage analysis in structured YAML format with alphabetically sorted variable names and module paths.

**Changes from previous version**:

- **ADDED**: definitions section grouped by module path
- **ADDED**: optional dynamic_imports section
- **MAINTAINED**: backward-compatible usages section
- **EXTENDED**: sorting to include module paths within definitions

#### Scenario: Enhanced YAML structure

- **WHEN** exporting results with both definitions and usages
- **THEN** the YAML SHALL include:
  - `definitions`: Grouped by module path with variable definitions
  - `dynamic_imports`: Optional section if detected
  - `usages`: Existing format unchanged
- **AND** all sections SHALL use alphabetical sorting

#### Scenario: Backward compatibility maintained

- **WHEN** existing tools parse the output
- **THEN** they SHALL continue to work by reading the usages section
- **AND** ignore the new definitions section
- **AND** maintain exact same usages format as before

### Requirement: File Discovery and Filtering

The system SHALL recursively discover Python files in the target directory while excluding common build artifacts and virtual environments.

#### Scenario: Recursive directory scanning

- **WHEN** scanning a directory path
- **THEN** the system SHALL find all `.py` files recursively
- **AND** include files in subdirectories at any depth
- **AND** follow the filesystem structure

#### Scenario: Exclude virtual environments

- **WHEN** discovering files
- **THEN** the system SHALL exclude directories named:
  - `venv/`, `env/`, `.venv/`
  - `virtualenv/`
  - `site-packages/`
- **AND** avoid scanning thousands of library files

#### Scenario: Exclude build artifacts

- **WHEN** discovering files
- **THEN** the system SHALL exclude:
  - `__pycache__/` directories
  - `build/`, `dist/` directories
  - `.egg-info/` directories
  - `.tox/`, `.pytest_cache/` directories
- **AND** improve scanning performance

#### Scenario: Single file input

- **WHEN** the input path is a single `.py` file
- **THEN** the system SHALL scan only that file
- **AND** skip directory traversal

#### Scenario: Nonexistent path handling

- **WHEN** the input path does not exist
- **THEN** the system SHALL raise a clear error message
- **AND** exit with non-zero status code

### Requirement: Django Settings Scanner CLI

The system SHALL provide a command-line interface for scanning Django projects and exporting settings usage to YAML files.

#### Scenario: Scan project directory

- **WHEN** user runs `upcast scan-django-settings /path/to/project`
- **THEN** the system SHALL scan all Python files in the project
- **AND** detect all Django settings usage
- **AND** output results to stdout in YAML format

#### Scenario: Custom output file

- **WHEN** user specifies `-o <output_path>` option
- **THEN** the system SHALL write YAML output to the specified file
- **AND** create parent directories if needed
- **AND** overwrite existing file

#### Scenario: Verbose mode

- **WHEN** user specifies `-v` or `--verbose` flag
- **THEN** the system SHALL print progress information during scanning
- **AND** show each file being processed
- **AND** display summary statistics at the end

#### Scenario: Summary output

- **WHEN** scanning completes
- **THEN** the system SHALL print a summary:
  - Number of unique settings variables found
  - Total usage count across all files
  - Number of files scanned
- **AND** display success or error status

#### Scenario: Error handling

- **WHEN** a file cannot be parsed due to syntax errors
- **THEN** the system SHALL log a warning with the file path
- **AND** continue scanning remaining files
- **AND** include successfully parsed results in output

### Requirement: Type Inference Accuracy

The system SHALL use astroid's semantic analysis to accurately resolve imports and distinguish Django settings from other objects with similar names.

#### Scenario: Resolve import aliases

- **WHEN** code uses aliased imports like `from django.conf import settings as config`
- **THEN** the system SHALL resolve `config` to `django.conf.settings`
- **AND** correctly identify all usages

#### Scenario: Handle star imports

- **WHEN** code uses `from django.conf import *`
- **THEN** the system SHALL resolve `settings` references through the star import
- **AND** detect them as Django settings

#### Scenario: Distinguish local variables

- **WHEN** code has both `from django.conf import settings` and local `settings = {}`
- **THEN** the system SHALL only track the Django settings object
- **AND** ignore the local variable

#### Scenario: Graceful inference failure

- **WHEN** type inference fails due to complex dynamic code
- **THEN** the system SHALL fall back to pattern matching (name == "settings")
- **AND** log a warning about potential false positives
- **AND** include the usage in results

### Requirement: Module Structure

The system SHALL follow the established scanner architecture pattern with clear separation of concerns across 5 core modules.

#### Scenario: Module organization

- **WHEN** the scanner is implemented
- **THEN** it SHALL have modules:
  - `ast_utils.py`: Low-level AST pattern detection
  - `settings_parser.py`: High-level parsing and data structures
  - `checker.py`: AST visitor and aggregation logic
  - `export.py`: YAML output formatting
  - `cli.py`: Command-line interface

#### Scenario: Public API

- **WHEN** importing the scanner programmatically
- **THEN** the main function SHALL be accessible via:
  - `from upcast.django_settings_scanner import scan_django_settings`
- **AND** follow the established naming convention

#### Scenario: Internal imports

- **WHEN** modules import from each other
- **THEN** they SHALL use absolute imports with `upcast.django_settings_scanner` prefix
- **AND** avoid circular dependencies

### Requirement: Unit Test Coverage

The system SHALL include comprehensive unit tests covering all pattern detection, parsing, aggregation, and export functionality.

#### Scenario: AST utilities testing

- **WHEN** testing AST utilities
- **THEN** tests SHALL verify:
  - `is_django_settings()` detects django.conf.settings imports
  - `is_django_settings()` rejects non-Django settings (negative case)
  - `is_settings_attribute_access()` detects `settings.KEY` patterns
  - `is_settings_getattr_call()` detects getattr patterns
  - `is_settings_hasattr_call()` detects hasattr patterns
  - `extract_setting_name()` works for all pattern types
  - Import alias resolution

#### Scenario: Parser testing

- **WHEN** testing settings parser
- **THEN** tests SHALL verify:
  - `parse_settings_attribute()` extracts correct metadata
  - `parse_settings_getattr()` extracts name and default
  - `parse_settings_hasattr()` extracts name
  - `parse_settings_usage()` handles all three patterns
  - Dataclass field types and validation
  - Source code snippet extraction

#### Scenario: Checker testing

- **WHEN** testing the AST checker
- **THEN** tests SHALL verify:
  - Visitor methods detect all pattern types
  - Aggregation groups by variable name correctly
  - Same variable in multiple files aggregates properly
  - Multiple usages in same file recorded separately
  - Error handling for unparseable files

#### Scenario: Export testing

- **WHEN** testing YAML export
- **THEN** tests SHALL verify:
  - `format_settings_output()` generates correct structure
  - Variable names sorted alphabetically
  - Locations sorted by file and line
  - `export_to_yaml()` writes valid YAML to file
  - `export_to_yaml_string()` returns valid YAML
  - UTF-8 encoding and special characters

#### Scenario: CLI testing

- **WHEN** testing CLI functionality
- **THEN** tests SHALL verify:
  - `scan_django_settings()` works with directory paths
  - `scan_django_settings()` works with single file paths
  - Output file creation with `-o` option
  - Verbose mode output
  - Error handling for nonexistent paths
  - File filtering excludes venv, **pycache**, etc.

#### Scenario: Test fixtures

- **WHEN** creating test fixtures
- **THEN** the suite SHALL include:
  - `simple_settings.py`: Basic attribute access patterns
  - `getattr_patterns.py`: Dynamic access with getattr/hasattr
  - `aliased_imports.py`: Import aliases
  - `non_django_settings.py`: Non-Django settings (negative tests)
  - `mixed_settings.py`: Both Django and non-Django in same file

#### Scenario: Test coverage target

- **WHEN** running the test suite
- **THEN** the system SHALL have:
  - 45+ individual test cases
  - 100% test pass rate
  - Zero linting errors from ruff
  - Coverage of all three pattern types
  - Zero false positives validated

### Requirement: Settings Module Detection

The system SHALL identify Python modules that contain Django settings definitions using path-based heuristics and import tracking.

#### Scenario: Path-based detection - settings directory

- **WHEN** scanning a project with a `settings/` directory
- **EXAMPLES**: `myproject/settings/base.py`, `myproject/settings/dev.py`
- **THEN** the system SHALL mark all Python files in `settings/` as settings modules
- **AND** convert file paths to Python module paths (e.g., `myproject.settings.base`)

#### Scenario: Path-based detection - config directory

- **WHEN** scanning a project with a `config/` directory
- **EXAMPLES**: `myproject/config/settings.py`, `config/production.py`
- **THEN** the system SHALL mark all Python files in `config/` as settings modules
- **AND** use module path as the key in output

#### Scenario: File path to module path conversion

- **WHEN** converting file paths to module paths
- **EXAMPLES**:
  - `/project/myapp/settings/base.py` → `myapp.settings.base`
  - `/project/config/settings.py` → `config.settings`
- **THEN** the system SHALL remove the `.py` extension
- **AND** convert path separators to dots
- **AND** make path relative to project root

#### Scenario: Non-settings file exclusion

- **WHEN** scanning directories that don't match settings patterns
- **EXAMPLES**: `utils/helpers.py`, `models/user.py`
- **THEN** the system SHALL NOT mark them as settings modules
- **AND** skip definition scanning for those files

### Requirement: Uppercase Variable Detection

The system SHALL detect uppercase variable assignments in settings modules as settings definitions.

#### Scenario: Valid uppercase variable

- **WHEN** code contains `DEBUG = True` or `DATABASE_URL = "postgres://..."`
- **THEN** the system SHALL extract the variable name
- **AND** mark it as a settings definition
- **AND** record the line number

#### Scenario: Uppercase with underscores

- **WHEN** code contains `ALLOWED_HOSTS = []` or `CORS_ALLOWED_ORIGINS = []`
- **THEN** the system SHALL recognize it as uppercase (underscores allowed)
- **AND** extract as a valid setting

#### Scenario: Exclude dunder names

- **WHEN** code contains `__name__ = "..."` or `__version__ = "1.0"`
- **THEN** the system SHALL NOT treat them as settings
- **AND** exclude from definition list

#### Scenario: Exclude lowercase variables

- **WHEN** code contains `debug = True` or `config = {}`
- **THEN** the system SHALL NOT treat them as settings
- **AND** only detect all-uppercase names

#### Scenario: Type-annotated assignments

- **WHEN** code contains `DEBUG: bool = True`
- **THEN** the system SHALL extract the variable name "DEBUG"
- **AND** optionally record the type hint
- **AND** infer the value

### Requirement: Settings Value Inference

The system SHALL infer values for settings definitions using astroid analysis and mark unresolvable expressions as dynamic.

#### Scenario: Boolean literals

- **WHEN** a setting is defined as `DEBUG = True` or `ENABLED = False`
- **THEN** the system SHALL infer the value as boolean
- **AND** output `{"value": true, "type": "bool"}` or `{"value": false, "type": "bool"}`

#### Scenario: Integer and float literals

- **WHEN** a setting is defined as `PORT = 8000` or `TIMEOUT = 30.5`
- **THEN** the system SHALL infer the numeric value
- **AND** output `{"value": 8000, "type": "int"}` or `{"value": 30.5, "type": "float"}`

#### Scenario: String literals

- **WHEN** a setting is defined as `DATABASE_URL = "postgres://localhost/db"`
- **THEN** the system SHALL infer the string value
- **AND** output `{"value": "postgres://localhost/db", "type": "string"}`

#### Scenario: List literals

- **WHEN** a setting is defined as `INSTALLED_APPS = ["app1", "app2", "app3"]`
- **THEN** the system SHALL infer the list value
- **AND** output `{"value": ["app1", "app2", "app3"], "type": "list"}`
- **AND** preserve element order

#### Scenario: Dictionary literals

- **WHEN** a setting is defined as `DATABASES = {"default": {"ENGINE": "...", "NAME": "..."}}`
- **THEN** the system SHALL infer the dictionary structure
- **AND** output `{"value": {...}, "type": "dict"}`
- **AND** preserve nested structure

#### Scenario: None value

- **WHEN** a setting is defined as `CACHE_BACKEND = None`
- **THEN** the system SHALL infer None
- **AND** output `{"value": null, "type": "none"}`

#### Scenario: Function calls - mark as dynamic

- **WHEN** a setting is defined as `BASE_DIR = Path(__file__).resolve().parent`
- **THEN** the system SHALL mark the value as dynamic
- **AND** output `{"value": "`Path(**file**).resolve().parent`", "type": "call"}`
- **AND** wrap the expression in backticks

#### Scenario: Environment variables - mark as dynamic

- **WHEN** a setting is defined as `SECRET_KEY = os.environ.get("SECRET_KEY")`
- **THEN** the system SHALL mark the value as dynamic
- **AND** output `{"value": "`os.environ.get('SECRET_KEY')`", "type": "dynamic"}`
- **AND** wrap the expression in backticks

#### Scenario: Complex expressions - mark as dynamic

- **WHEN** a setting uses complex logic that cannot be statically resolved
- **EXAMPLES**: `TIMEOUT = int(os.getenv("TIMEOUT", "30"))`, `DEBUG = not PRODUCTION`
- **THEN** the system SHALL mark as dynamic with the expression wrapped in backticks
- **AND** output like `{"value": "`int(os.getenv('TIMEOUT', '30'))`", "type": "dynamic"}`
- **AND** NOT attempt to evaluate (avoid side effects)

### Requirement: Settings Inheritance Detection

The system SHALL detect star import patterns (`from .base import *`) and track which settings override others.

#### Scenario: Detect star imports

- **WHEN** a settings module contains `from .base import *`
- **THEN** the system SHALL record "base" as a star import
- **AND** resolve relative import to absolute module path
- **AND** store in SettingsModule.star_imports list

#### Scenario: Resolve relative imports

- **WHEN** in module `settings.dev`, code has `from .base import *`
- **THEN** the system SHALL resolve to `settings.base`
- **AND** in module `settings.envs.prod`, `from ..base import *` → `settings.base`

#### Scenario: Detect absolute star imports

- **WHEN** code contains `from myproject.settings.base import *`
- **THEN** the system SHALL record `myproject.settings.base` as star import
- **AND** handle the same as relative imports

#### Scenario: Mark override relationships

- **WHEN** `settings.dev` imports `from .base import *` and defines `DEBUG = True`
- **AND** `settings.base` already defines `DEBUG = False`
- **THEN** the system SHALL mark `settings.dev.DEBUG.overrides = "settings.base"`
- **AND** preserve both definitions in output

#### Scenario: Multiple base imports

- **WHEN** a module has multiple star imports
- **EXAMPLES**: `from .base import *` then `from .common import *`
- **THEN** the system SHALL track all star imports
- **AND** mark overrides from any base module

#### Scenario: No override for new settings

- **WHEN** `settings.dev` defines `NEW_FEATURE = True` not in base
- **THEN** the system SHALL NOT set the overrides field
- **AND** treat as a new definition specific to dev

### Requirement: Dynamic Import Detection

The system SHALL detect and document dynamic import patterns using `importlib.import_module()`.

#### Scenario: Detect importlib import_module calls

- **WHEN** code contains `module = importlib.import_module(f"settings.{env}")`
- **THEN** the system SHALL detect the dynamic import pattern
- **AND** record the pattern string and location

#### Scenario: Extract base module from f-strings

- **WHEN** pattern is `f"settings.{env}"` or `f"settings.{profile}"`
- **THEN** the system SHALL extract "settings" as the base module
- **AND** recognize it as a dynamic selector pattern

#### Scenario: Extract pattern from string concatenation

- **WHEN** pattern is `"settings." + env` or `"config." + environment`
- **THEN** the system SHALL extract the base module
- **AND** document the concatenation pattern

#### Scenario: Detect format method patterns

- **WHEN** pattern is `"settings.{}".format(env)`
- **THEN** the system SHALL extract "settings" as base
- **AND** recognize the dynamic placeholder

#### Scenario: Document in output

- **WHEN** dynamic imports are detected
- **THEN** the output SHALL include a `dynamic_imports` section
- **AND** list each pattern with location, base_module, and detected pattern

#### Scenario: Cannot extract base module

- **WHEN** pattern is too dynamic (e.g., `importlib.import_module(get_module_name())`)
- **THEN** the system SHALL document the pattern as-is
- **AND** mark base_module as null or "<unknown>"

### Requirement: Enhanced Output Format

The system SHALL output both settings definitions and usages in a unified YAML structure with definitions grouped by module path.

#### Scenario: Definitions section structure

- **WHEN** outputting definitions
- **THEN** the YAML SHALL have a top-level `definitions` key
- **AND** group by module path (e.g., `settings.base`, `settings.dev`)
- **AND** each variable SHALL include: value, line, type, and optional overrides

#### Scenario: Definition entry format

- **WHEN** outputting a single definition
- **THEN** the entry SHALL include:
  - Variable name as key
  - `value`: Inferred value or `<dynamic>`
  - `line`: Line number where defined
  - `type`: Value type (literal, int, float, string, list, dict, dynamic, call)
  - `overrides`: Parent module path (optional, only if overriding)

#### Scenario: Dynamic imports section

- **WHEN** dynamic imports are detected
- **THEN** the output SHALL include a `dynamic_imports` section
- **AND** list each import with: pattern, base_module, file, line
- **AND** place it after definitions, before usages

#### Scenario: Usages section unchanged

- **WHEN** outputting the complete result
- **THEN** the `usages` section SHALL maintain the existing format
- **AND** ensure backward compatibility with existing parsers

#### Scenario: Combined output example

- **WHEN** both definitions and usages exist
- **THEN** the output structure SHALL be:
  ```yaml
  definitions:
    <module_path>:
      <VAR_NAME>:
        value: <value>
        line: <int>
        type: <type>
        overrides: <parent_module> # optional
  dynamic_imports: # optional section
    - pattern: <string>
      base_module: <string>
      file: <path>
      line: <int>
  usages:
    <VAR_NAME>:
      count: <int>
      locations: [...]
  ```

#### Scenario: Alphabetical sorting within sections

- **WHEN** formatting output
- **THEN** module paths SHALL be sorted alphabetically
- **AND** variable names within each module SHALL be sorted alphabetically
- **AND** maintain consistent ordering for version control

### Requirement: CLI Filtering Flags

The system SHALL provide CLI flags to filter output to definitions-only, usages-only, or combined modes.

#### Scenario: Default behavior - combined output

- **WHEN** user runs `upcast scan-django-settings <path>` with no flags
- **THEN** the system SHALL output both definitions and usages
- **AND** maintain backward compatibility (existing behavior + definitions)

#### Scenario: Definitions-only mode

- **WHEN** user specifies `--definitions-only` flag
- **THEN** the output SHALL include only the `definitions` section
- **AND** optionally include `dynamic_imports`
- **AND** exclude the `usages` section

#### Scenario: Usages-only mode

- **WHEN** user specifies `--usages-only` flag
- **THEN** the output SHALL include only the `usages` section
- **AND** match the exact pre-enhancement format
- **AND** skip definition scanning (faster execution)

#### Scenario: No-usages flag

- **WHEN** user specifies `--no-usages` flag
- **THEN** the system SHALL scan for definitions only
- **AND** skip usage detection entirely
- **AND** output definitions and dynamic_imports sections only

#### Scenario: No-definitions flag

- **WHEN** user specifies `--no-definitions` flag
- **THEN** the system SHALL scan for usages only
- **AND** output only the usages section
- **AND** behave identically to pre-enhancement version
