# Django Model Scanner Specification

## ADDED Requirements

### Requirement: Django Model Detection

The system SHALL accurately detect Django model classes through semantic AST analysis using type inference.

#### Scenario: Direct Model inheritance

- **WHEN** a class directly inherits from `models.Model`
- **THEN** the system SHALL identify it as a Django model
- **AND** include it in the analysis output

#### Scenario: Indirect Model inheritance

- **WHEN** a class inherits from another class that inherits from `models.Model`
- **THEN** the system SHALL identify it as a Django model through ancestor analysis
- **AND** track the inheritance chain

#### Scenario: Aliased Model import

- **WHEN** a class inherits from an aliased import of Django Model
- **THEN** the system SHALL resolve the alias through type inference
- **AND** correctly identify it as a Django model

#### Scenario: Abstract model handling

- **WHEN** a model has `Meta.abstract = True`
- **THEN** the system SHALL mark it as abstract
- **AND** exclude it from table generation
- **AND** make its fields available for inheritance merging

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

### Requirement: Command Line Interface

The system SHALL provide a simple CLI command for scanning Django projects and generating model documentation.

#### Scenario: Scan Django project

- **WHEN** user runs `upcast analyze_django_models <project_path>`
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
