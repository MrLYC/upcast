# django-model-scanner Spec Deltas

## MODIFIED Requirements

### Requirement: Field Parsing

The system SHALL extract complete information about Django model fields including type, options, and constraints.

#### Scenario: Field type with full module path

- **WHEN** a field is defined using qualified access like `models.CharField(max_length=100)`
- **THEN** the system SHALL extract the fully qualified field type
- **AND** return format like `"django.db.models.CharField"` (not just `"CharField"`)
- **AND** include the complete module path for unambiguous identification

#### Scenario: Field type inference from imports

- **WHEN** a field is defined using direct import like `CharField(max_length=100)`
- **THEN** the system SHALL attempt to infer the full module path through import resolution
- **AND** fall back to the short name if inference fails
- **AND** return the most complete type information available

#### Scenario: Custom field type preservation

- **WHEN** a field uses a custom field class
- **THEN** the system SHALL extract its fully qualified name
- **AND** distinguish it from Django's built-in fields
- **AND** preserve the complete module context

### Requirement: Meta Class Parsing

The system SHALL extract Django model Meta class options for database configuration and behavior.

#### Scenario: Abstract flag storage location

- **WHEN** a model's Meta class defines `abstract = True`
- **THEN** the system SHALL store it only in the `meta` dictionary
- **AND** NOT duplicate it as a top-level model field
- **AND** access it via `model["meta"].get("abstract", False)`

#### Scenario: Proxy model detection

- **WHEN** a model's Meta class defines `proxy = True`
- **THEN** the system SHALL extract the proxy flag
- **AND** store it in the `meta` dictionary
- **AND** preserve the model in output (even without fields)

## MODIFIED Requirements

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

## ADDED Requirements

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
