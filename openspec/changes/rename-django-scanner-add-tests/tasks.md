# Implementation Tasks

## 1. Module Renaming

- [ ] 1.1 Rename directory `upcast/django_scanner/` to `upcast/django_model_scanner/`
- [ ] 1.2 Update imports in `upcast/django_model_scanner/__init__.py`
- [ ] 1.3 Update imports in `upcast/django_model_scanner/checker.py`
- [ ] 1.4 Update imports in `upcast/django_model_scanner/cli.py`
- [ ] 1.5 Update imports in `upcast/django_model_scanner/model_parser.py`
- [ ] 1.6 Update import in `upcast/main.py` from `upcast.django_scanner` to `upcast.django_model_scanner`
- [ ] 1.7 Update import in `tests/test_django_model.py` from `upcast.django_scanner` to `upcast.django_model_scanner`

## 2. Unit Test Suite

- [ ] 2.1 Create `tests/test_django_model_scanner/` directory
- [ ] 2.2 Add `tests/test_django_model_scanner/test_cli.py` with tests for:
  - [ ] `_find_project_root()` searching downward for `src/` directory
  - [ ] `_scan_file()` processing Python files correctly
  - [ ] `scan_django_models()` with directory path
  - [ ] `scan_django_models()` with file path
  - [ ] `scan_django_models()` with output file
  - [ ] Error handling for nonexistent paths
- [ ] 2.3 Add `tests/test_django_model_scanner/test_model_parser.py` with tests for:
  - [ ] `parse_model()` extracting basic model info
  - [ ] `_extract_field_type()` getting full module paths via inference + imports
  - [ ] `_extract_base_qname()` getting full module paths for base classes
  - [ ] `parse_meta_class()` parsing Meta options correctly
  - [ ] `merge_abstract_fields()` inheriting fields from abstract models
  - [ ] `_is_relationship_field()` detecting relationship fields
- [ ] 2.4 Add `tests/test_django_model_scanner/test_checker.py` with tests for:
  - [ ] `DjangoModelChecker` visiting model classes
  - [ ] Handling models in different file structures
  - [ ] Tracking module paths correctly
- [ ] 2.5 Add `tests/test_django_model_scanner/test_export.py` with tests for:
  - [ ] `format_model_output()` YAML formatting
  - [ ] `export_to_yaml()` writing to files
  - [ ] `export_to_yaml_string()` returning YAML strings
  - [ ] Output includes bases field
- [ ] 2.6 Add `tests/test_django_model_scanner/test_ast_utils.py` with tests for:
  - [ ] `is_django_model()` detecting Django models
  - [ ] `is_django_field()` detecting Django fields
  - [ ] `infer_literal_value()` extracting literal values
  - [ ] `safe_as_string()` handling different node types

## 3. Documentation Updates

- [ ] 3.1 Update README.md with corrected module name if mentioned
- [ ] 3.2 Verify CLI help text is clear and accurate

## 4. Validation

- [ ] 4.1 Run `pytest tests/test_django_model_scanner/` to verify all tests pass
- [ ] 4.2 Run `mypy upcast/django_model_scanner/` to verify type checking passes
- [ ] 4.3 Run `ruff check upcast/django_model_scanner/` to verify linting passes
- [ ] 4.4 Run existing integration test `pytest tests/test_django_model.py` to ensure compatibility
- [ ] 4.5 Test CLI command `upcast analyze-django-models` still works correctly
