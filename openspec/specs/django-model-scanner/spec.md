# django-model-scanner Specification

## Purpose

TBD - created by archiving change reimplement-django-scanner. Update Purpose after archive.

## Requirements

### Requirement: Django Model Detection

The system SHALL accurately detect Django model classes through semantic AST analysis using type inference.

#### Scenario: Empty model filtering

- **WHEN** a model has no fields and no relationships
- **AND** is not abstract (`meta.abstract != True`)
- **AND** is not a proxy model (`meta.proxy != True`)
- **THEN** the system SHALL return `None` for this model
- **AND** exclude it from the output
- **AND** treat it as a parsing artifact or incomplete definition

#### Scenario: Proxy model preservation

- **WHEN** a model has `Meta.proxy = True`
- **AND** has no fields or relationships
- **THEN** the system SHALL include it in the output
- **AND** preserve its metadata
- **AND** recognize it as a valid model type

#### Scenario: Abstract model without fields

- **WHEN** a model has `Meta.abstract = True`
- **AND** has no fields or relationships (yet)
- **THEN** the system SHALL include it in the output
- **AND** make it available for field inheritance
- **AND** mark it clearly as abstract in the `meta` dictionary

### Requirement: Field Parsing

The system SHALL extract complete information about Django model fields including type, options, and constraints.

#### Scenario: Basic field extraction

- **WHEN** a model defines a field like `name = models.CharField(max_length=100)`
- **THEN** the system SHALL extract field name as "name"
- **AND** extract field type as "CharField"
- **AND** extract field options including `max_length: 100`

#### Scenario: Field with multiple options

- **WHEN** a field has multiple keyword arguments
- **THEN** the system SHALL extract all keyword options
- **AND** preserve option types (bool, int, string, etc.)
- **AND** handle complex option values (choices, defaults)

#### Scenario: Field option type inference

- **WHEN** field options include literal values
- **THEN** the system SHALL infer Python types (True/False → bool, numbers → int/float)
- **AND** preserve quoted strings
- **AND** handle None values

### Requirement: Relationship Field Analysis

The system SHALL parse and structure relationship fields (ForeignKey, OneToOneField, ManyToManyField) with complete metadata.

#### Scenario: ForeignKey parsing

- **WHEN** a model defines a ForeignKey field
- **THEN** the system SHALL extract relationship type as "ForeignKey"
- **AND** extract target model from first positional argument
- **AND** extract relationship options (on_delete, related_name, etc.)

#### Scenario: ManyToMany parsing

- **WHEN** a model defines a ManyToManyField
- **THEN** the system SHALL extract relationship type as "ManyToManyField"
- **AND** extract target model
- **AND** extract through model if specified
- **AND** extract symmetrical option for self-references

#### Scenario: Relationship with related_name

- **WHEN** a relationship field has a related_name option
- **THEN** the system SHALL include it in relationship metadata
- **AND** document reverse relationship accessor

### Requirement: Meta Class Parsing

The system SHALL extract Django model Meta class options for database configuration and behavior.

#### Scenario: Extract db_table

- **WHEN** a model's Meta class defines `db_table`
- **THEN** the system SHALL extract the table name
- **AND** include it in model metadata

#### Scenario: Extract abstract flag

- **WHEN** a model's Meta class defines `abstract = True`
- **THEN** the system SHALL mark the model as abstract
- **AND** enable inheritance field merging

#### Scenario: Extract ordering

- **WHEN** a model's Meta class defines `ordering`
- **THEN** the system SHALL extract the ordering list
- **AND** preserve field names and direction indicators

#### Scenario: Extract verbose names

- **WHEN** a model's Meta class defines `verbose_name` or `verbose_name_plural`
- **THEN** the system SHALL extract the human-readable names
- **AND** include them in model metadata

### Requirement: Abstract Inheritance Merging

The system SHALL merge fields from abstract base models into concrete child models.

#### Scenario: Single abstract parent

- **WHEN** a concrete model inherits from one abstract model
- **THEN** the system SHALL copy all fields from the abstract parent
- **AND** include them in the concrete model's field list
- **AND** preserve field order

#### Scenario: Multiple abstract parents

- **WHEN** a concrete model inherits from multiple abstract models
- **THEN** the system SHALL merge fields from all abstract parents
- **AND** handle field name conflicts (last parent wins)
- **AND** maintain method resolution order

#### Scenario: Nested abstract inheritance

- **WHEN** an abstract model inherits from another abstract model
- **THEN** the system SHALL recursively merge fields from all ancestors
- **AND** propagate fields to concrete descendants

### Requirement: Multi-table Inheritance Detection

The system SHALL identify and document multi-table inheritance patterns where child models inherit from concrete parent models.

#### Scenario: Detect multi-table inheritance

- **WHEN** a model inherits from a concrete (non-abstract) Django model
- **THEN** the system SHALL mark inheritance_type as "multi-table"
- **AND** record the parent model reference
- **AND** document the implicit OneToOne link

#### Scenario: Multiple concrete parents

- **WHEN** a model inherits from multiple concrete models
- **THEN** the system SHALL list all concrete parent models
- **AND** document the complex inheritance structure

### Requirement: YAML Output Format

The system SHALL export model analysis results in structured YAML format for human readability and machine processing.

#### Scenario: Model export structure

- **WHEN** exporting a model to YAML
- **THEN** the output SHALL include module path as the key
- **AND** include model metadata (abstract, table name)
- **AND** include fields section with all field definitions
- **AND** include relationships section with all foreign keys

#### Scenario: Field formatting

- **WHEN** exporting field options to YAML
- **THEN** the system SHALL normalize option values to proper Python types
- **AND** use readable formatting (block style, proper indentation)
- **AND** preserve UTF-8 characters

#### Scenario: Readable output

- **WHEN** generating YAML output
- **THEN** the system SHALL use 2-space indentation
- **AND** use block style (not flow style)
- **AND** preserve insertion order of fields
- **AND** allow Unicode characters

### Requirement: Type Inference Accuracy

The system SHALL use astroid's type inference to accurately resolve imports and inheritance chains.

#### Scenario: Resolve import aliases

- **WHEN** code uses `from django.db import models as m`
- **THEN** the system SHALL resolve `m.Model` to `django.db.models.base.Model`
- **AND** correctly detect inheritance

#### Scenario: Resolve qualified imports

- **WHEN** code uses `import django.db.models`
- **THEN** the system SHALL resolve `django.db.models.Model`
- **AND** handle fully qualified names

#### Scenario: Handle inference failures gracefully

- **WHEN** type inference fails for complex dynamic code
- **THEN** the system SHALL fall back to pattern matching
- **AND** use heuristics (ends with "Model", "Field", etc.)
- **AND** log warnings for manual review

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

### Requirement: Field Type Resolution

The system SHALL resolve field types to fully qualified module paths for unambiguous identification.

#### Scenario: Qualified field access resolution

- **WHEN** a field is accessed through module attribute like `models.CharField`
- **THEN** the system SHALL infer the module's qualified name
- **AND** combine it with the attribute name
- **AND** return the full path (e.g., `django.db.models.CharField`)

#### Scenario: Type inference through astroid

- **WHEN** resolving field types
- **THEN** the system SHALL use astroid's type inference capabilities
- **AND** follow import chains to source modules
- **AND** handle aliased imports correctly

#### Scenario: Graceful degradation for unresolvable types

- **WHEN** type inference fails or returns ambiguous results
- **THEN** the system SHALL fall back to the short field name
- **AND** still include the field in output
- **AND** log a warning about incomplete type resolution

### Requirement: Model Metadata Extraction

The system SHALL extract comprehensive metadata from Django model classes including a description field from docstrings.

#### Scenario: Extract model description from docstring

- **WHEN** a Django model class has a docstring
- **THEN** the system SHALL extract the docstring text
- **AND** strip leading and trailing whitespace
- **AND** store it in a `description` field in the output

**DIFF**: Added description field extraction requirement

#### Scenario: Handle models without docstrings

- **WHEN** a Django model class has no docstring
- **THEN** the system SHALL omit the `description` field from output
- **OR** set it to empty string or null (implementation choice)

**DIFF**: New scenario for docstring absence handling

#### Scenario: Preserve multi-line docstrings

- **WHEN** a model has a multi-line docstring
- **THEN** the system SHALL preserve line breaks and formatting
- **AND** only strip leading/trailing whitespace from the entire docstring
- **EXAMPLE**:

  ```python
  class User(models.Model):
      """User account model.

      Stores user authentication and profile data.
      """
  ```

  → `description: "User account model.\n\nStores user authentication and profile data."`

**DIFF**: New scenario for multi-line docstring handling

### Requirement: Field Type Information

The system SHALL extract complete type information for Django model fields including full module paths.

#### Scenario: Extract fully qualified field type names

- **WHEN** extracting a field type
- **THEN** the system SHALL use astroid inference to get qualified name
- **AND** include the full module path
- **EXAMPLE**: `CharField` → `django.db.models.fields.CharField`

**DIFF**: Modified to require full module paths instead of simple type names

#### Scenario: Handle custom field types

- **WHEN** a model uses a custom field type
- **THEN** the system SHALL infer the full qualified name
- **EXAMPLE**: `myapp.fields.CustomField` not just `CustomField`

**DIFF**: New scenario for custom field types

#### Scenario: Fallback for unresolvable field types

- **WHEN** field type cannot be inferred
- **THEN** the system SHALL wrap type name in backticks `` `FieldType` ``
- **AND** set type to `"unknown"` if completely unresolvable

**DIFF**: Added fallback scenario using new common utilities

### Requirement: Consistent Output Formatting

The system SHALL export model data with consistently sorted fields and standardized formatting.

#### Scenario: Sort model dictionary keys

- **WHEN** exporting models to YAML
- **THEN** the system SHALL sort model names alphabetically
- **AND** sort field names alphabetically within each model
- **AND** sort relationship names alphabetically

**DIFF**: New requirement for sorted output

#### Scenario: Sort field metadata

- **WHEN** exporting field metadata
- **THEN** field properties SHALL be in consistent order:
  - name
  - type (with full module path)
  - required
  - default
  - max_length (if applicable)
  - choices (if applicable)
  - help_text (if applicable)

**DIFF**: Specified consistent field property ordering

### Requirement: Use Common Utilities

The system SHALL use shared common utilities for file discovery, AST inference, and export operations.

#### Scenario: Use common file discovery

- **WHEN** scanning for Django models
- **THEN** the system SHALL use `common.file_utils.collect_python_files()`
- **AND** support `--include` and `--exclude` pattern options
- **AND** respect default exclude patterns

**DIFF**: New requirement to use common utilities

#### Scenario: Use common inference with fallback

- **WHEN** inferring field default values or types
- **THEN** the system SHALL use `common.ast_utils.infer_value_with_fallback()`
- **AND** mark failed inferences with backticks
- **AND** use `unknown` type for unresolvable types

**DIFF**: New requirement for unified inference

#### Scenario: Use common export functions

- **WHEN** exporting to YAML
- **THEN** the system SHALL use `common.export.export_to_yaml()`
- **AND** benefit from consistent sorting and formatting

**DIFF**: New requirement for common export
