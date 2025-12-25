# env-var-scanner Specification

## Purpose

TBD - created by archiving change reimplement-env-var-scanner. Update Purpose after archive.

## Requirements

### Requirement: Environment Variable Detection

The system SHALL detect environment variable access patterns using semantic AST analysis with astroid.

#### Scenario: Context-validated os.getenv() detection

- **WHEN** code uses `os.getenv('VAR_NAME')`
- **THEN** the system SHALL verify the string 'VAR_NAME' is used as argument to getenv()
- **AND** SHALL verify parent node context is a Call to os.getenv or equivalent
- **AND** SHALL identify "VAR_NAME" as an environment variable only if validation passes
- **AND** mark it as not required (has implicit None default)
- **AND** record the file location and statement

**Rationale**: Context validation prevents false positives from strings in unrelated contexts

**DIFF**: Added explicit context validation requirement

#### Scenario: Reject strings from non-env contexts

- **WHEN** string literal appears in source code
- **AND** string is not an argument to env access function
- **EXAMPLES**:
  - API endpoint: `api.post('/api/config/', {'key': 'A1'})`
  - Dict key access: `data['environment']`
  - Logging: `logger.info('Checking variable: %s', name)`
  - Configuration: `config = {'id': 123}`
- **THEN** the system SHALL NOT report these strings as environment variables
- **AND** SHALL skip them during extraction
- **AND** SHALL log debug message about context mismatch if verbose mode enabled

**Rationale**: Many strings in code look like env var names but are used in different contexts

**NEW**: Explicit requirement to filter non-env contexts

### Requirement: Django-environ Pattern Detection

The system SHALL detect and parse django-environ library patterns with type extraction.

#### Scenario: Context-validated env() method detection

- **WHEN** code uses `env.str('VAR_NAME')` or similar
- **THEN** the system SHALL verify 'VAR_NAME' is argument to env.\* method call
- **AND** SHALL verify the method is called on an `Env` instance from django-environ
- **AND** extract the type from the method name
- **AND** record the type as 'str', 'int', 'bool', etc.
- **AND** mark as required if no default provided

**Rationale**: Same context validation principle applied to django-environ patterns

**DIFF**: Added context validation for django-environ calls

### Requirement: Type Inference

The system SHALL infer types from multiple sources with priority ordering.

#### Scenario: Type from explicit type conversion

- **WHEN** code uses `int(os.getenv('VAR_NAME', '10'))`
- **THEN** the system SHALL infer type as 'int' from the wrapper function
- **AND** record this as the highest priority type source

#### Scenario: Type fallback to str for standard getenv

- **WHEN** code uses `os.getenv('VAR_NAME')` without type conversion
- **THEN** the system SHALL default type to 'str'
- **AND** record this as the inferred type

#### Scenario: Type from 'or' expression with literal

- **WHEN** code uses `env('DEBUG') or False`
- **THEN** the system SHALL infer type as 'bool' from the right operand
- **AND** record 'False' as the default value

#### Scenario: Type from default value literal

- **WHEN** code uses `os.getenv('VAR_NAME', 123)`
- **THEN** the system SHALL infer type as 'int' from the integer literal default
- **AND** record this inferred type

#### Scenario: Type from django-environ method

- **WHEN** code uses `env.bool('VAR_NAME')` or `env.int('VAR_NAME')`
- **THEN** the system SHALL extract type as 'bool' or 'int' from the method name
- **AND** record this as the inferred type

#### Scenario: Type inference priority

- **WHEN** code uses `int(os.getenv('PORT', '8000'))`
- **THEN** the system SHALL prioritize the explicit `int()` cast
- **AND** record type as 'int' (not 'str' from the string literal default)

#### Scenario: Multiple type occurrences across codebase

- **WHEN** a variable is used with different types in different locations
  - **EXAMPLE**: `int(os.getenv('PORT', '8000'))` and `os.getenv('PORT', '8000')`
- **THEN** the system SHALL collect all unique types
- **AND** output as a list: `['int', 'str']`

#### Scenario: Type inference fallback

- **WHEN** no explicit cast, typed method, or default value is found
- **THEN** the system SHALL default to 'str' for getenv patterns
- **AND** record type as null for `os.environ['KEY']` patterns

### Requirement: Default Value Extraction

The system SHALL extract and aggregate default values using astroid literal inference, preserve actual Python types, and exclude dynamic expressions from the aggregated defaults list.

#### Scenario: Boolean default preservation

- **WHEN** code uses `os.getenv('DEBUG', False)` with a boolean default
- **THEN** the system SHALL record the default as boolean `False` (not string `'False'`)
- **AND** include it in the `defaults` list as a boolean value
- **AND** the YAML output SHALL render it as `false` (not `'False'`)

#### Scenario: Integer default preservation

- **WHEN** code uses `os.getenv('PORT', 8000)` with an integer default
- **THEN** the system SHALL record the default as integer `8000` (not string `'8000'`)
- **AND** include it in the `defaults` list as an integer value
- **AND** the YAML output SHALL render it as `8000` (not `'8000'`)

#### Scenario: Float default preservation

- **WHEN** code uses `os.getenv('TIMEOUT', 3.14)` with a float default
- **THEN** the system SHALL record the default as float `3.14` (not string `'3.14'`)
- **AND** include it in the `defaults` list as a float value

#### Scenario: String default preservation

- **WHEN** code uses `os.getenv('API_URL', 'http://localhost')` with a string default
- **THEN** the system SHALL record the default as string (unchanged)
- **AND** include it in the `defaults` list as a string value

#### Scenario: None default preservation

- **WHEN** code uses `os.getenv('OPTIONAL_KEY', None)` with None default
- **THEN** the system SHALL record the default as `None` (not string `'None'`)
- **AND** include it in the `defaults` list as null/None
- **AND** the YAML output SHALL render it as `null` (not `'None'`)

#### Scenario: Exclude dynamic expression defaults

- **WHEN** code uses `os.getenv('VAR1', os.getenv('VAR2', ''))` where the default is another getenv call
- **THEN** the system SHALL wrap the default expression in backticks as `` `os.getenv('VAR2', '')` ``
- **AND** SHALL NOT include this backtick-wrapped value in the aggregated `defaults` list
- **AND** the full statement SHALL remain available in `usages[].statement`
- **REASON**: Dynamic expressions are not useful as "default values" and are redundant with usage statements

#### Scenario: Exclude uninferrable defaults

- **WHEN** code uses `os.getenv('VAR', some_function())` where the default cannot be inferred
- **THEN** the system SHALL wrap the default expression in backticks
- **AND** SHALL NOT include it in the aggregated `defaults` list
- **AND** the expression SHALL be available in the individual usage's `default` field for inspection

#### Scenario: Mixed defaults handling

- **WHEN** a variable has multiple usages with different defaults:
  - Usage 1: `os.getenv('VAR', 'static')`
  - Usage 2: `os.getenv('VAR', os.getenv('OTHER', ''))`
- **THEN** the `defaults` list SHALL include only `'static'` (the static value)
- **AND** SHALL NOT include the backtick-wrapped dynamic expression
- **AND** both statements SHALL be preserved in their respective usage entries

#### Scenario: Empty defaults list for all-dynamic

- **WHEN** all usages of a variable have dynamic/uninferrable defaults
- **THEN** the aggregated `defaults` list SHALL be empty `[]`
- **AND** the YAML output SHALL show `defaults: []`
- **AND** users can inspect individual `usages[].default` fields for the expressions

### Requirement: Variable Name Resolution

The system SHALL resolve environment variable names including concatenated strings and f-strings.

#### Scenario: Simple string literal

- **WHEN** code uses `os.getenv('VAR_NAME')`
- **THEN** the system SHALL extract "VAR_NAME" directly
- **AND** use it as the variable name

#### Scenario: String concatenation with constants

- **WHEN** code uses `os.getenv(PREFIX + 'NAME')` where `PREFIX = 'APP_'`
- **THEN** the system SHALL use astroid to resolve PREFIX value
- **AND** evaluate the concatenation to "APP_NAME"
- **AND** use the resolved name

#### Scenario: F-string variable names

- **WHEN** code uses `os.getenv(f'{PREFIX}NAME')` where `PREFIX = 'APP_'`
- **THEN** the system SHALL evaluate the f-string
- **AND** resolve to "APP_NAME"

#### Scenario: Format string variable names

- **WHEN** code uses `os.getenv('%sNAME' % PREFIX)` where `PREFIX = 'APP_'`
- **THEN** the system SHALL evaluate the format string
- **AND** resolve to "APP_NAME"

#### Scenario: Unresolvable variable names

- **WHEN** variable name depends on runtime values
- **THEN** the system SHALL fall back to string representation
- **AND** include a note in output about unresolved name

### Requirement: Result Aggregation by Variable Name

The system SHALL aggregate all usages of each environment variable across the entire codebase.

#### Scenario: Single variable, multiple locations

- **WHEN** `DATABASE_URL` is accessed in 3 different files
- **THEN** the system SHALL create one entry for "DATABASE_URL"
- **AND** list all 3 usages with complete context:
  - Each usage with its location, statement, type, default, and required flag
- **AND** aggregate unique types and defaults at the variable level

#### Scenario: Type aggregation

- **WHEN** a variable is used with types `['int', 'str', 'int']` across locations
- **THEN** the system SHALL deduplicate to `['int', 'str']`
- **AND** preserve the order of first occurrence

#### Scenario: Default value aggregation

- **WHEN** a variable has defaults `['value1', 'value2', 'value1']` across locations
- **THEN** the system SHALL deduplicate to `['value1', 'value2']`
- **AND** preserve the order of first occurrence

#### Scenario: Required flag determination

- **WHEN** a variable is accessed without a default value in any usage
- **THEN** the system SHALL mark that usage as `required: true`
- **AND** mark the variable-level `required: true` if ANY usage is required
- **AND** the determination follows these rules:
  - `os.environ['KEY']` → required (no default, raises KeyError)
  - `os.environ.get('KEY')` → not required (implicit None default)
  - `os.getenv('KEY')` → not required (implicit None default)
  - `os.getenv('KEY', default)` → not required (explicit default)
  - `env('KEY')` → required (django-environ without default)
  - `env('KEY', default=...)` → not required (explicit default)
  - `env.TYPE('KEY')` → required (no default)
  - `env.TYPE('KEY', default)` → not required (explicit default)

#### Scenario: Usage format and sorting

- **WHEN** recording usages
- **THEN** each usage SHALL include location in format: `"path/to/file.py:line"`
- **AND** use relative paths from project root
- **AND** sort usages by file path, then line number
- **AND** preserve all context (statement, type, default, required) for each usage

### Requirement: YAML Output Format

The system SHALL export aggregated results in structured YAML format optimized for human readability.

#### Scenario: Basic variable output structure

- **WHEN** exporting environment variables
- **THEN** each variable SHALL be a top-level key (variable name)
- **AND** include `types` list (aggregated unique types)
- **AND** include `defaults` list (aggregated unique defaults)
- **AND** include `usages` list with each usage containing:
  - `location`: file path and line number
  - `statement`: the actual code statement
  - `type`: inferred type for this specific usage (or null)
  - `default`: default value for this specific usage (or null)
  - `required`: boolean indicating if this specific usage requires the variable
- **AND** include `required` boolean (true if ANY usage is required)

#### Scenario: YAML formatting

- **WHEN** generating YAML output
- **THEN** the system SHALL use 2-space indentation
- **AND** use block style for lists and dicts
- **AND** preserve Unicode characters
- **AND** sort variables alphabetically by name

#### Scenario: Empty list handling

- **WHEN** a variable has no types or no defaults
- **THEN** the system SHALL output an empty list `[]`
- **AND** NOT omit the key

#### Scenario: Example output

```yaml
DATABASE_URL:
  types: [str]
  defaults: ["postgresql://localhost/db"]
  usages:
    - location: "config/settings.py:15"
      statement: "os.getenv('DATABASE_URL', 'postgresql://localhost/db')"
      type: str
      default: "postgresql://localhost/db"
      required: false
    - location: "config/database.py:8"
      statement: "env.str('DATABASE_URL')"
      type: str
      default: null
      required: true
  required: true

DEBUG:
  types: [bool]
  defaults: [false]
  usages:
    - location: "config/settings.py:10"
      statement: "env.bool('DEBUG', False)"
      type: bool
      default: false
      required: false
  required: false

API_KEY:
  types: []
  defaults: []
  usages:
    - location: "api/client.py:23"
      statement: "os.environ['API_KEY']"
      type: null
      default: null
      required: true
  required: true
```

### Requirement: JSON Output Format Support

The system SHALL support JSON output format as an alternative to YAML.

#### Scenario: JSON format option

- **WHEN** user specifies `--format json`
- **THEN** the system SHALL output in JSON format
- **AND** use the same structure as YAML
- **AND** use 2-space indentation

#### Scenario: JSON vs YAML structure consistency

- **WHEN** outputting in either format
- **THEN** both formats SHALL have identical data structure
- **AND** be convertible between formats without data loss

### Requirement: CLI Interface

The system SHALL provide a command-line interface for scanning projects and files.

#### Scenario: CLI respects include patterns

- **WHEN** user runs `upcast scan-env-vars <path> --include "*/settings.py"`
- **THEN** the system SHALL only scan files matching the include pattern
- **AND** pass the pattern to `scan_directory()` function
- **AND** use `collect_python_files()` with filtering enabled

**DIFF**: Fixed bug where --include option was accepted but ignored

#### Scenario: CLI respects exclude patterns

- **WHEN** user runs `upcast scan-env-vars <path> --exclude "*/tests/*.py"`
- **THEN** the system SHALL skip files matching the exclude pattern
- **AND** pass the pattern to `scan_directory()` function
- **AND** apply exclusions during file collection

**DIFF**: Fixed bug where --exclude option was accepted but ignored

#### Scenario: CLI respects no-default-excludes flag

- **WHEN** user runs `upcast scan-env-vars <path> --no-default-excludes`
- **THEN** the system SHALL not apply default exclude patterns (venv/, **pycache**/, etc.)
- **AND** pass `use_default_excludes=False` to file collection utilities
- **AND** scan all Python files including those normally excluded

**DIFF**: Fixed bug where --no-default-excludes flag was accepted but ignored

### Requirement: AST Utilities

The system SHALL provide reusable AST utility functions following astroid best practices.

#### Scenario: is_env_var_call() detection

- **WHEN** given an astroid Call node
- **THEN** `is_env_var_call()` SHALL return True if it matches known patterns
- **AND** identify the pattern type (os.getenv, environ[], env(), etc.)

#### Scenario: infer_type_from_value()

- **WHEN** given an astroid node representing a default value
- **THEN** `infer_type_from_value()` SHALL infer Python type
- **AND** return type name as string ('str', 'int', 'bool', etc.)

#### Scenario: resolve_string_concat()

- **WHEN** given an astroid node with string concatenation
- **THEN** `resolve_string_concat()` SHALL evaluate constants
- **AND** return the resolved string value

#### Scenario: infer_literal_value()

- **WHEN** given an astroid node representing a literal
- **THEN** `infer_literal_value()` SHALL extract the Python value
- **AND** handle strings, numbers, booleans, None, lists, tuples, dicts

### Requirement: Pattern Extensibility

The system SHALL support custom environment variable patterns via configuration.

#### Scenario: Custom pattern via CLI

- **WHEN** user provides `--pattern "custom_getenv($NAME, $DEFAULT)"`
- **THEN** the system SHALL detect usages of this pattern
- **AND** extract variable name from $NAME
- **AND** extract default value from $DEFAULT

#### Scenario: Custom required pattern

- **WHEN** user provides `--required-pattern "custom_getenv_required($NAME)"`
- **THEN** the system SHALL detect this pattern
- **AND** mark matching variables as required

#### Scenario: Multiple custom patterns

- **WHEN** user provides multiple `--pattern` flags
- **THEN** the system SHALL detect all specified patterns
- **AND** aggregate results with built-in patterns

### Requirement: Import Context Tracking

The system SHALL track module imports to correctly resolve aliased and qualified names.

#### Scenario: Track direct imports

- **WHEN** code has `import os`
- **THEN** the system SHALL recognize `os.getenv()` calls
- **AND** track the import context

#### Scenario: Track from imports

- **WHEN** code has `from os import getenv`
- **THEN** the system SHALL recognize direct `getenv()` calls
- **AND** resolve them to `os.getenv`

#### Scenario: Track star imports

- **WHEN** code has `from os import *`
- **THEN** the system SHALL recognize all os module members
- **AND** handle them appropriately

#### Scenario: Track aliased imports

- **WHEN** code has `import os as operating_system`
- **THEN** the system SHALL resolve `operating_system.getenv()`
- **AND** recognize it as `os.getenv()`

### Requirement: Unit Test Coverage

The system SHALL include comprehensive unit tests covering all core functionality.

#### Scenario: Pattern detection tests

- **WHEN** running unit tests for pattern detection
- **THEN** tests SHALL verify all os module patterns
- **AND** verify django-environ patterns
- **AND** verify custom pattern support
- **AND** cover edge cases (missing imports, syntax variations)

#### Scenario: Type inference tests

- **WHEN** running tests for type inference
- **THEN** tests SHALL verify inference from casts
- **AND** verify inference from defaults
- **AND** verify inference from django-environ methods
- **AND** verify handling of multiple types

#### Scenario: Aggregation tests

- **WHEN** running tests for result aggregation
- **THEN** tests SHALL verify aggregation by variable name
- **AND** verify type deduplication
- **AND** verify default deduplication
- **AND** verify location sorting
- **AND** verify required flag logic

#### Scenario: Export format tests

- **WHEN** running tests for output formatting
- **THEN** tests SHALL verify YAML structure
- **AND** verify JSON structure
- **AND** verify format consistency
- **AND** verify handling of edge cases (empty lists, special characters)

#### Scenario: CLI tests

- **WHEN** running tests for CLI
- **THEN** tests SHALL verify directory scanning
- **AND** verify file scanning
- **AND** verify output to file
- **AND** verify format selection
- **AND** verify error handling

#### Scenario: Test organization

- **WHEN** organizing the test suite
- **THEN** tests SHALL be in `tests/test_env_var_scanner/`
- **AND** separated into modules:
  - `test_ast_utils.py`
  - `test_env_var_parser.py`
  - `test_checker.py`
  - `test_cli.py`
  - `test_export.py`
- **AND** use pytest fixtures for common test setup

### Requirement: File Filtering Support

The system SHALL support file filtering in scanner functions to enable CLI filtering features.

#### Scenario: scan_directory accepts filtering parameters

- **WHEN** calling `scan_directory()` function
- **THEN** the function SHALL accept optional parameters:
  - `include_patterns: list[str] | None` - Glob patterns for files to include
  - `exclude_patterns: list[str] | None` - Glob patterns for files to exclude
  - `use_default_excludes: bool` - Whether to apply default exclusions (default: True)
- **AND** pass these parameters to `collect_python_files()` utility

**DIFF**: Added filtering parameters to scan_directory function signature

#### Scenario: Filtering is applied during file collection

- **WHEN** filtering parameters are provided to `scan_directory()`
- **THEN** the function SHALL use `collect_python_files()` with the filtering options
- **AND** only scan files that match the filtering criteria
- **AND** respect pattern precedence (exclude wins over include)

**DIFF**: Filtering is now applied before scanning, enabling CLI filtering features

### Requirement: Parent Node Context Validation

The system SHALL validate parent node context before reporting environment variables.

#### Scenario: Verify Call node ancestry

- **WHEN** extracting variable name from string literal
- **THEN** the system SHALL traverse AST upward to find parent Call node
- **AND** SHALL verify Call node is one of:
  - `os.getenv(string_arg)`
  - `os.environ.get(string_arg)`
  - `env(string_arg)` or `env.TYPE(string_arg)`
  - Other registered env access patterns
- **AND** SHALL verify string literal is the variable name argument (typically first arg)
- **AND** SHALL reject string if no matching Call pattern found

**Rationale**: AST structure provides reliable context information to filter false positives

#### Scenario: Handle subscript access context

- **WHEN** string appears in subscript: `os.environ['VAR_NAME']`
- **THEN** the system SHALL verify parent is Subscript node
- **AND** SHALL verify Subscript.value resolves to `os.environ`
- **AND** SHALL accept this as valid env var context
- **DIFF**: Dict subscript is valid env access pattern; other subscripts are not

#### Scenario: Log rejected strings in verbose mode

- **WHEN** string literal looks like env var name but fails context validation
- **AND** verbose mode is enabled
- **THEN** the system SHALL log debug message with:
  - String value
  - File and line location
  - Parent node type
  - Reason for rejection
- **AND** SHALL NOT output this string in results

**Rationale**: Debugging support helps understand and refine filter logic
