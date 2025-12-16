# django-model-scanner Specification Delta

## RENAMED Requirements

- FROM: `### Requirement: Command Line Interface`
- TO: `### Requirement: Django Model Scanner CLI`

**Reason**: More descriptive and aligns with module rename to `django_model_scanner`

## MODIFIED Requirements

### Requirement: Django Model Scanner CLI

The system SHALL provide a simple CLI command for scanning Django projects and generating model documentation, accessible through the `upcast.django_model_scanner` module.

#### Scenario: Scan Django project

- **WHEN** user runs `upcast analyze-django-models <project_path>`
- **THEN** the system SHALL scan all Python files in the project
- **AND** detect all Django models
- **AND** output results to default location

#### Scenario: Custom output path

- **WHEN** user specifies `-o <output_path>` option
- **THEN** the system SHALL write YAML output to the specified path
- **AND** create parent directories if needed
- **AND** report success or errors

#### Scenario: Error handling

- **WHEN** scanning encounters parsing errors
- **THEN** the system SHALL continue scanning other files
- **AND** report errors to stderr
- **AND** complete successfully for parseable models

#### Scenario: Module import path

- **WHEN** user imports the scanner programmatically
- **THEN** the system SHALL be accessible via `from upcast.django_model_scanner import scan_django_models`
- **AND** maintain consistent naming across CLI and API

## ADDED Requirements

### Requirement: Unit Test Coverage

The system SHALL include comprehensive unit tests covering all core functionality to ensure reliability and maintainability.

#### Scenario: CLI function testing

- **WHEN** running unit tests for CLI functions
- **THEN** the tests SHALL verify `_find_project_root()` searches downward for `src/` directory
- **AND** verify `_scan_file()` processes Python files correctly
- **AND** verify `scan_django_models()` works with directory paths, file paths, and output files
- **AND** verify error handling for nonexistent paths

#### Scenario: Model parser testing

- **WHEN** running unit tests for model parsing
- **THEN** the tests SHALL verify `parse_model()` extracts basic model information
- **AND** verify `_extract_field_type()` gets full module paths via inference and import tracking
- **AND** verify `_extract_base_qname()` gets full module paths for base classes
- **AND** verify `parse_meta_class()` parses Meta options correctly
- **AND** verify `merge_abstract_fields()` inherits fields from abstract models
- **AND** verify `_is_relationship_field()` detects relationship fields

#### Scenario: Checker testing

- **WHEN** running unit tests for AST checker
- **THEN** the tests SHALL verify `DjangoModelChecker` visits model classes correctly
- **AND** verify handling of models in different file structures
- **AND** verify module path tracking

#### Scenario: Export testing

- **WHEN** running unit tests for YAML export
- **THEN** the tests SHALL verify `format_model_output()` YAML formatting
- **AND** verify `export_to_yaml()` writes to files correctly
- **AND** verify `export_to_yaml_string()` returns valid YAML strings
- **AND** verify output includes bases field

#### Scenario: AST utilities testing

- **WHEN** running unit tests for AST utilities
- **THEN** the tests SHALL verify `is_django_model()` detects Django models
- **AND** verify `is_django_field()` detects Django fields
- **AND** verify `infer_literal_value()` extracts literal values
- **AND** verify `safe_as_string()` handles different node types

#### Scenario: Test suite organization

- **WHEN** organizing the test suite
- **THEN** tests SHALL be grouped into separate modules:
  - `tests/test_django_model_scanner/test_cli.py`
  - `tests/test_django_model_scanner/test_model_parser.py`
  - `tests/test_django_model_scanner/test_checker.py`
  - `tests/test_django_model_scanner/test_export.py`
  - `tests/test_django_model_scanner/test_ast_utils.py`
- **AND** follow pytest conventions and project testing patterns

### Requirement: Module Naming Consistency

The system SHALL use `django_model_scanner` as the module name to accurately reflect its specific focus on Django model analysis.

#### Scenario: Module directory structure

- **WHEN** accessing the scanner implementation
- **THEN** the module SHALL be located at `upcast/django_model_scanner/`
- **AND** contain submodules: `cli.py`, `checker.py`, `model_parser.py`, `export.py`, `ast_utils.py`

#### Scenario: Import path consistency

- **WHEN** importing the scanner in user code
- **THEN** the import SHALL be `from upcast.django_model_scanner import scan_django_models`
- **AND** all internal imports SHALL use `upcast.django_model_scanner` prefix

#### Scenario: Backward compatibility consideration

- **WHEN** users upgrade from previous versions using `django_scanner`
- **THEN** they SHALL update imports from `upcast.django_scanner` to `upcast.django_model_scanner`
- **AND** the change SHALL be documented as a breaking change

**Reason**: The previous name `django_scanner` was misleading as it suggests scanning all Django components, when the module specifically focuses on Django models. The new name `django_model_scanner` clearly indicates the module's scope and purpose.
