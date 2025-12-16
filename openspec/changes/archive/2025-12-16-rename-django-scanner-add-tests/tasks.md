# Implementation Tasks

## 1. Module Renaming

- [x] 1.1 Rename directory `upcast/django_scanner/` to `upcast/django_model_scanner/`
- [x] 1.2 Update imports in `upcast/django_model_scanner/__init__.py`
- [x] 1.3 Update imports in `upcast/django_model_scanner/checker.py`
- [x] 1.4 Update imports in `upcast/django_model_scanner/cli.py`
- [x] 1.5 Update imports in `upcast/django_model_scanner/model_parser.py`
- [x] 1.6 Update import in `upcast/main.py` from `upcast.django_scanner` to `upcast.django_model_scanner`
- [x] 1.7 Update import in `tests/test_django_model.py` from `upcast.django_scanner` to `upcast.django_model_scanner`

## 2. Unit Test Suite

- [x] 2.1 Create `tests/test_django_model_scanner/` directory
- [x] 2.2 Add `tests/test_django_model_scanner/test_cli.py` with tests for:
  - [x] `_find_project_root()` searching downward for `src/` directory
  - [x] `_scan_file()` processing Python files correctly
  - [x] `scan_django_models()` with directory path
  - [x] `scan_django_models()` with file path
  - [x] `scan_django_models()` with output file
  - [x] Error handling for nonexistent paths
- [x] 2.3 Add `tests/test_django_model_scanner/test_model_parser.py` with tests for:
  - [x] `parse_model()` extracting basic model info
  - [x] `_extract_field_type()` getting full module paths via inference + imports
  - [x] `_extract_base_qname()` getting full module paths for base classes
  - [x] `parse_meta_class()` parsing Meta options correctly
  - [x] `merge_abstract_fields()` inheriting fields from abstract models
  - [x] `_is_relationship_field()` detecting relationship fields
- [x] 2.4 Add `tests/test_django_model_scanner/test_checker.py` with tests for:
  - [x] `DjangoModelChecker` visiting model classes
  - [x] Handling models in different file structures
  - [x] Tracking module paths correctly
- [x] 2.5 Add `tests/test_django_model_scanner/test_export.py` with tests for:
  - [x] `format_model_output()` YAML formatting
  - [x] `export_to_yaml()` writing to files
  - [x] `export_to_yaml_string()` returning YAML strings
  - [x] Output includes bases field
- [x] 2.6 Add `tests/test_django_model_scanner/test_ast_utils.py` with tests for:
  - [x] `is_django_model()` detecting Django models
  - [x] `is_django_field()` detecting Django fields
  - [x] `infer_literal_value()` extracting literal values
  - [x] `safe_as_string()` handling different node types

## 3. Documentation Updates

- [x] 3.1 Update README.md with corrected module name if mentioned
- [x] 3.2 Verify CLI help text is clear and accurate

## 4. Validation

- [x] 4.1 Run `pytest tests/test_django_model_scanner/` to verify all tests pass
- [x] 4.2 Run `mypy upcast/django_model_scanner/` to verify type checking passes
- [x] 4.3 Run `ruff check upcast/django_model_scanner/` to verify linting passes
- [x] 4.4 Run existing integration test `pytest tests/test_django_model.py` to ensure compatibility
- [x] 4.5 Test CLI command `upcast analyze-django-models` still works correctly
