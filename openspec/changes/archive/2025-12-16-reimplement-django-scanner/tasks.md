# Implementation Tasks

## 1. Setup and Dependencies

- [ ] 1.1 Add astroid dependency to pyproject.toml
- [ ] 1.2 Add PyYAML dependency to pyproject.toml
- [ ] 1.3 Update uv.lock with new dependencies
- [ ] 1.4 Create upcast/django_scanner/ module directory
- [ ] 1.5 Create **init**.py with package exports

## 2. Implement Core Detection (ast_utils.py)

- [ ] 2.1 Implement `is_django_model()` function with type inference
- [ ] 2.2 Implement `_check_base_is_django_model()` for recursive checking
- [ ] 2.3 Implement `_check_direct_bases_for_django()` for fallback detection
- [ ] 2.4 Implement `_is_django_import()` for import resolution
- [ ] 2.5 Implement `is_abstract_model()` to check Meta.abstract
- [ ] 2.6 Implement `is_concrete_model()` helper
- [ ] 2.7 Implement `is_django_field()` for field detection
- [ ] 2.8 Add unit tests for model detection with various inheritance patterns

## 3. Implement Field Parsing (model_parser.py)

- [ ] 3.1 Implement `parse_field()` to extract field name, type, and options
- [ ] 3.2 Implement `infer_literal_value()` for option type inference
- [ ] 3.3 Implement `normalize_relation()` for relationship fields
- [ ] 3.4 Implement `parse_meta_class()` to extract Meta options
- [ ] 3.5 Implement `get_meta_option()` for specific Meta attribute extraction
- [ ] 3.6 Implement `parse_model()` main function to orchestrate parsing
- [ ] 3.7 Implement `merge_abstract_fields()` for inheritance merging
- [ ] 3.8 Add unit tests for field parsing with various field types

## 4. Implement Pylint Checker (checker.py)

- [ ] 4.1 Create `DjangoModelChecker` class inheriting from `BaseChecker`
- [ ] 4.2 Implement `__init__()` to initialize model storage
- [ ] 4.3 Implement `visit_classdef()` to visit class definitions
- [ ] 4.4 Add model detection and parsing in visitor
- [ ] 4.5 Implement `close()` for second-pass inheritance merging
- [ ] 4.6 Implement `register()` function for Pylint integration
- [ ] 4.7 Add checker options (output path, verbose mode)
- [ ] 4.8 Add integration tests with sample Django models

## 5. Implement YAML Export (export.py)

- [ ] 5.1 Implement `normalize_value()` to convert AST strings to Python types
- [ ] 5.2 Implement `format_field_options()` to structure field data
- [ ] 5.3 Implement `format_model_output()` to structure model data
- [ ] 5.4 Implement `export_to_yaml()` to write YAML file
- [ ] 5.5 Implement `export_to_yaml_string()` for testing
- [ ] 5.6 Add unit tests for YAML formatting and output

## 6. Implement CLI Wrapper (cli.py)

- [ ] 6.1 Create CLI module with command function
- [ ] 6.2 Implement path validation helpers
- [ ] 6.3 Implement `run_scanner()` to execute Pylint with checker
- [ ] 6.4 Add error handling and user-friendly messages
- [ ] 6.5 Add verbose mode support
- [ ] 6.6 Add unit tests for CLI functions

## 7. Integrate with upcast Command

- [ ] 7.1 Update `upcast/main.py` to import new scanner
- [ ] 7.2 Replace `analyze_django_models` command implementation
- [ ] 7.3 Update command arguments (-o for output, new defaults)
- [ ] 7.4 Remove old `from upcast.django_model` imports
- [ ] 7.5 Add deprecation notice if desired (optional)

## 8. Remove Old Implementation

- [ ] 8.1 Delete `upcast/django_model/__init__.py`
- [ ] 8.2 Delete `upcast/django_model/core.py`
- [ ] 8.3 Delete `upcast/django_model/models.py`
- [ ] 8.4 Remove `upcast/django_model/` directory
- [ ] 8.5 Update any imports that referenced old module

## 9. Update Tests

- [ ] 9.1 Rewrite `tests/test_django_model.py` for new implementation
- [ ] 9.2 Create test fixtures with sample Django models
- [ ] 9.3 Add tests for basic model detection
- [ ] 9.4 Add tests for abstract inheritance
- [ ] 9.5 Add tests for multi-table inheritance
- [ ] 9.6 Add tests for relationship fields
- [ ] 9.7 Add tests for Meta class options
- [ ] 9.8 Add tests for YAML output format
- [ ] 9.9 Add tests for error handling
- [ ] 9.10 Ensure all tests pass with `uv run pytest`

## 10. Documentation

- [ ] 10.1 Update README.md with new command examples
- [ ] 10.2 Document breaking changes in CHANGELOG or migration guide
- [ ] 10.3 Add example YAML output to documentation
- [ ] 10.4 Document new command options
- [ ] 10.5 Add docstrings to all public functions
- [ ] 10.6 Update CONTRIBUTING.md if development workflow changed

## 11. Validation

- [ ] 11.1 Test with example Django project (simple models)
- [ ] 11.2 Test with complex Django project (inheritance, relationships)
- [ ] 11.3 Compare output quality with old implementation
- [ ] 11.4 Verify YAML output is valid and readable
- [ ] 11.5 Run type checking: `uv run mypy`
- [ ] 11.6 Run linting: `uv run pre-commit run -a`
- [ ] 11.7 Ensure CI passes on all Python versions (3.9-3.12)

## 12. Performance Testing (Optional)

- [ ] 12.1 Benchmark scanning time on medium project (~100 models)
- [ ] 12.2 Compare performance with old implementation
- [ ] 12.3 Profile if performance issues found
- [ ] 12.4 Document performance characteristics
