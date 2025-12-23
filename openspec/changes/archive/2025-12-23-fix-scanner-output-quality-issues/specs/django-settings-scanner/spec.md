# Django Settings Scanner Specification Delta

## MODIFIED Requirements

### Requirement: Scanner Modes

The system SHALL support two scanning modes: usage tracking and definition extraction.

#### Scenario: Usage mode (existing behavior)

- **WHEN** scanner runs with `mode=usage` (default)
- **THEN** the system SHALL detect settings access patterns across codebase
- **AND** output `DjangoSettingsUsageOutput` with usage locations
- **AND** group results by setting name
- **THIS BEHAVIOR IS UNCHANGED**

#### Scenario: Definitions mode (restored functionality)

- **WHEN** scanner runs with `mode=definitions`
- **THEN** the system SHALL scan Django settings files
- **AND** SHALL extract all setting definitions with their values
- **AND** SHALL output `DjangoSettingsDefinitionOutput` with definitions grouped by module
- **AND** SHALL include setting name, value, type, and source location
- **AND** SHALL handle multiple settings modules (base, dev, prod, local)

**Rationale**: Definition mode complements usage mode for complete settings inventory during migration analysis

**DIFF**: Definitions mode was specified but not implemented; now fully functional

#### Scenario: Settings file identification

- **WHEN** scanning in definitions mode
- **THEN** the system SHALL identify settings files by:
  - File name matches `settings.py` or `settings/*.py` pattern
  - File location is in project root or `<appname>/settings/` directory
  - File contains Django settings module marker (imports from `django.conf` or has settings metadata)
- **AND** SHALL scan all identified settings files
- **AND** SHALL use `parse_settings_module()` from common utilities

**Rationale**: Robust detection of settings files in various Django project structures

**NEW**: Explicit settings file identification logic

#### Scenario: Setting value extraction

- **WHEN** parsing settings definitions
- **THEN** the system SHALL extract:
  - Setting name (variable name at module level)
  - Value (as string representation)
  - Type (inferred from value: str, int, bool, list, dict, etc.)
  - Source location (file path and line number)
- **AND** SHALL handle environment variable references specially
  - Mark value as "<from_env: VAR_NAME>" when using `os.getenv()` or `env()`
  - Extract default value if provided
- **AND** SHALL handle complex expressions
  - Simplify to type description if value cannot be safely evaluated
  - Example: `[func() for x in range(10)]` → `<computed: list>`

**Rationale**: Provides actionable information for settings migration and validation

**NEW**: Detailed value extraction requirements

## ADDED Requirements

### Requirement: Settings Module Output Format

The system SHALL output settings definitions grouped by module with consistent structure.

#### Scenario: Output structure for definitions mode

- **WHEN** outputting settings definitions
- **THEN** the structure SHALL be:
  ```yaml
  results:
    settings.base:
      DEBUG:
        value: "False"
        type: "bool"
        location: "myapp/settings/base.py:10"
      DATABASE_URL:
        value: "<from_env: DATABASE_URL>"
        type: "str"
        location: "myapp/settings/base.py:15"
        default: "sqlite:///db.sqlite3"
  ```
- **AND** SHALL use module path as top-level key
- **AND** SHALL use setting name as second-level key
- **AND** SHALL include value, type, location, and optional default fields

**Rationale**: Consistent structure enables automated processing and comparison

#### Scenario: Handle settings inheritance

- **WHEN** settings files import from each other (e.g., `from .base import *`)
- **THEN** the system SHALL track which file defines each setting
- **AND** SHALL record the actual definition location, not the import
- **AND** MAY note if setting is overridden in multiple files
- **AND** SHALL preserve the inheritance chain if tracked

**Rationale**: Django projects often split settings across multiple files; tracking origin is important

## REMOVED Requirements

None - existing requirements remain intact with enhanced implementation.
