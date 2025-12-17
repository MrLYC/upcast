# django-settings-scanner Specification

## ADDED Requirements

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

The system SHALL export settings usage analysis in structured YAML format with alphabetically sorted variable names and detailed location metadata.

#### Scenario: Variable entry structure

- **WHEN** exporting a settings variable
- **THEN** the output SHALL include:
  - Variable name as the top-level key
  - `count` field with total usage count
  - `locations` list with all usage details
- **AND** use human-readable formatting

#### Scenario: Location metadata

- **WHEN** exporting each usage location
- **THEN** the output SHALL include:
  - `file`: Relative path from project root
  - `line`: Line number (1-based)
  - `column`: Column number (0-based)
  - `pattern`: One of "attribute_access", "getattr", "hasattr"
  - `code`: Source code snippet showing the usage
- **AND** preserve UTF-8 characters in code snippets

#### Scenario: Alphabetical sorting

- **WHEN** formatting the output
- **THEN** the system SHALL sort variable names alphabetically
- **AND** produce deterministic output for version control
- **AND** make manual review easier

#### Scenario: YAML formatting options

- **WHEN** writing YAML output
- **THEN** the system SHALL use:
  - 2-space indentation
  - Block style (not flow style)
  - UTF-8 encoding
  - Explicit start marker (---)
- **AND** ensure valid YAML syntax

#### Scenario: Empty results

- **WHEN** no settings usage is found in the scanned files
- **THEN** the system SHALL output an empty YAML document
- **AND** include a comment explaining no usage was detected

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
