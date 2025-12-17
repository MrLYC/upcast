# django-model-scanner Specification

## ADDED Requirements

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
