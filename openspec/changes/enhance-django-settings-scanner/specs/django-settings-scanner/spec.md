# Spec Delta: django-settings-scanner

## ADDED Requirements

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

## MODIFIED Requirements

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

## REMOVED Requirements

None - this is a purely additive enhancement with backward compatibility maintained.
