# Spec Delta: env-var-scanner

## MODIFIED Requirements

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

## MODIFIED Data Structures

### EnvVarUsage data class

**CHANGED**: `default` field type

- **Before**: `default: Optional[str] = None`
- **After**: `default: Optional[Any] = None`
- **Reason**: Preserve actual Python types instead of string representations

### EnvVarInfo data class

**CHANGED**: `defaults` field type

- **Before**: `defaults: list[str] = field(default_factory=list)`
- **After**: `defaults: list[Any] = field(default_factory=list)`
- **Reason**: Store actual typed values, support bool/int/float/None

**CHANGED**: `add_usage()` method behavior

- **Added logic**: Filter out backtick-wrapped defaults before adding to the list
- **Condition**: Skip if `isinstance(default, str) and default.startswith('`') and default.endswith('`')`

## MODIFIED Output Format

### YAML/JSON Export

**CHANGED**: `defaults` field value types

- **Before**: All values serialized as strings
  ```yaml
  defaults:
    - "False"
    - "0"
    - "None"
  ```
- **After**: Values serialized with their actual types
  ```yaml
  defaults:
    - false
    - 0
    - null
  ```

**CHANGED**: Dynamic defaults exclusion

- **Before**: Backtick-wrapped expressions appear in defaults
  ```yaml
  defaults:
    - "`os.getenv('OTHER', '')`"
  ```
- **After**: Backtick-wrapped expressions excluded
  ```yaml
  defaults: [] # Empty if all defaults are dynamic
  ```

## Implementation Notes

### Type Preservation

The change leverages existing `upcast.common.ast_utils.infer_value_with_fallback()` which already returns typed values. The fix is to stop converting these values to strings with `str()`.

### Backtick Detection

Dynamic expressions are wrapped in backticks by `infer_value_with_fallback()` when inference fails. The filter checks for this pattern to exclude them from the aggregated defaults list.

### Backward Compatibility

**Breaking change**: Tools consuming the scanner output must handle typed values instead of expecting all strings. This is intentional to improve data quality and semantic accuracy.
