# Reimplement Django Model Scanner

## Why

The current `analyze_django_models` command uses ast-grep-py for Django model analysis, but it has several limitations:

- Limited accuracy in detecting Django model inheritance patterns
- Incomplete handling of abstract models and multi-table inheritance
- Missing support for relationship field analysis (ForeignKey, ManyToMany)
- No Meta class option extraction (db_table, abstract, etc.)
- JSON output format lacks structured relationship information

The `django-model-scanner` project (based on Pylint's astroid) provides a significantly better implementation with:

- Accurate Django model detection through type inference
- Complete abstract model inheritance merging
- Full relationship field parsing (ForeignKey, OneToOne, ManyToMany)
- Meta class option extraction
- YAML output format with structured, readable data
- Better handling of complex inheritance patterns

Reimplementing the scanner based on this proven approach will provide more accurate and complete Django model analysis.

## What Changes

- **BREAKING**: Remove existing `upcast/django_model/` module entirely
- **BREAKING**: Reimplement `analyze_django_models` command with new architecture
- Add astroid dependency for AST analysis
- Add PyYAML dependency for structured output
- Implement pylint-based model detection
- Add comprehensive model parsing (fields, relationships, Meta options)
- Support abstract model inheritance merging
- Change output format from JSON to YAML
- Update command interface and options

## Impact

- Affected specs: `django-model-scanner` (new capability)
- Affected code:
  - `upcast/main.py` - command implementation
  - `upcast/django_model/` - complete removal
  - `pyproject.toml` - add astroid and PyYAML dependencies
  - `tests/test_django_model.py` - rewrite tests
- Breaking changes:
  - **Output format**: Changed from JSON to YAML
  - **Output structure**: More detailed with relationships and Meta options
  - **Command options**: New option names and behavior
  - **API**: Complete rewrite, no backward compatibility
- Users will need to:
  - Update output parsing logic to handle YAML instead of JSON
  - Adapt to new output structure with additional fields
  - Update command invocation if using custom options
