# Tasks: Refactor Scanner Architecture

## Phase 1: Common Utilities Foundation (10 tasks)

- [ ] 1.1 Create `upcast/common/` package structure with `__init__.py`
- [ ] 1.2 Implement `upcast/common/file_utils.py` with `collect_python_files()`, `validate_path()`, `find_package_root()`
- [ ] 1.3 Add tests for `file_utils.py` (path validation, file collection, package root detection)
- [ ] 1.4 Implement `upcast/common/patterns.py` with glob pattern matching for include/exclude
- [ ] 1.5 Add tests for `patterns.py` (pattern matching, default excludes)
- [ ] 1.6 Implement `upcast/common/ast_utils.py` with `infer_value_with_fallback()`, `infer_type_with_fallback()`, `get_qualified_name()`, `safe_as_string()`
- [ ] 1.7 Add tests for `ast_utils.py` (inference success/failure, backtick wrapping, unknown types)
- [ ] 1.8 Implement `upcast/common/export.py` with `export_to_yaml()`, `export_to_json()`, `sort_dict_recursive()`
- [ ] 1.9 Add tests for `export.py` (YAML/JSON output, field sorting)
- [ ] 1.10 Run linting and type checking on common module

**Validation**: All tests pass, ruff check clean, mypy validates types

## Phase 2: Migrate Environment Variable Scanner (8 tasks)

- [ ] 2.1 Update `env_var_scanner` to use `common.file_utils` for file collection
- [ ] 2.2 Replace local inference functions with `common.ast_utils.infer_value_with_fallback()`
- [ ] 2.3 Update type inference to use `common.ast_utils.infer_type_with_fallback()`
- [ ] 2.4 Add backtick wrapping for failed value inferences
- [ ] 2.5 Set type to `unknown` for failed type inferences
- [ ] 2.6 Update export to use `common.export` with sorted YAML output
- [ ] 2.7 Remove duplicated utility functions from `env_var_scanner`
- [ ] 2.8 Update tests to verify new inference fallback behavior

**Validation**: All env-var scanner tests pass, output sorting verified

## Phase 3: Migrate Django Models Scanner (10 tasks)

- [ ] 3.1 Update `django_model_scanner` to use `common.file_utils`
- [ ] 3.2 Replace local `infer_literal_value()` with `common.ast_utils` version
- [ ] 3.3 Add `description` field extraction from model class docstrings
- [ ] 3.4 Strip leading/trailing whitespace from docstrings
- [ ] 3.5 Update field type extraction to include full module paths (e.g., `django.db.models.CharField`)
- [ ] 3.6 Use `common.ast_utils.get_qualified_name()` for type names
- [ ] 3.7 Update export to use `common.export` with sorted fields
- [ ] 3.8 Remove duplicated functions (`safe_as_string`, `infer_literal_value`)
- [ ] 3.9 Update tests to verify `description` field and sorted output
- [ ] 3.10 Add test cases for docstring extraction (with/without docstrings)

**Validation**: Models include description, types have module paths, YAML sorted

## Phase 4: Migrate Django Settings Scanner (7 tasks)

- [ ] 4.1 Update `django_settings_scanner` to use `common.file_utils`
- [ ] 4.2 Replace `_collect_python_files()` with `common.file_utils.collect_python_files()`
- [ ] 4.3 Replace `_validate_path()` with `common.file_utils.validate_path()`
- [ ] 4.4 Update export to use `common.export` with sorted output
- [ ] 4.5 Ensure location sorting uses (file, line, column) order
- [ ] 4.6 Remove duplicated utility functions
- [ ] 4.7 Update tests to verify sorted output

**Validation**: Settings scanner uses common utilities, output sorted

## Phase 5: Migrate Prometheus Metrics Scanner (7 tasks)

- [ ] 5.1 Update `prometheus_metrics_scanner` to use `common.file_utils`
- [ ] 5.2 Replace `_validate_path()` and `_collect_python_files()` with common versions
- [ ] 5.3 Update inference functions to use `common.ast_utils` with fallbacks
- [ ] 5.4 Add backtick wrapping for dynamic metric names
- [ ] 5.5 Update export to use `common.export` with sorted output
- [ ] 5.6 Remove duplicated functions
- [ ] 5.7 Update tests for inference fallback behavior

**Validation**: Metrics scanner migrated, dynamic values marked with backticks

## Phase 6: Add File Pattern Filtering (8 tasks)

- [ ] 6.1 Add `--include` option to all scan commands (accepts multiple values)
- [ ] 6.2 Add `--exclude` option to all scan commands (accepts multiple values)
- [ ] 6.3 Add `--no-default-excludes` flag to disable default exclude patterns
- [ ] 6.4 Update `scan-env-vars` to support file patterns
- [ ] 6.5 Update `scan-django-models` to support file patterns (see Phase 7 for rename)
- [ ] 6.6 Update `scan-django-settings` to support file patterns
- [ ] 6.7 Update `scan-prometheus-metrics` to support file patterns (see Phase 7 for rename)
- [ ] 6.8 Add integration tests for include/exclude patterns

**Validation**: All scanners support file filtering, tests verify pattern matching

## Phase 7: Standardize Command Names (8 tasks)

- [ ] 7.1 Rename `analyze-django-models` to `scan-django-models` in implementation
- [ ] 7.2 Add deprecated alias `analyze-django-models` with warning message
- [ ] 7.3 Remove `-cmd` suffix from `scan-prometheus-metrics-cmd` → `scan-prometheus-metrics`
- [ ] 7.4 Add deprecated alias `scan-prometheus-metrics-cmd` with warning
- [ ] 7.5 Remove `-cmd` suffix from `scan-django-settings-cmd` → `scan-django-settings`
- [ ] 7.6 Add deprecated alias `scan-django-settings-cmd` with warning
- [ ] 7.7 Update CLI help text to show deprecation notices
- [ ] 7.8 Update README with command name changes and migration guide

**Validation**: New commands work, old commands show deprecation warnings

## Phase 8: Documentation & Examples (7 tasks)

- [ ] 8.1 Update README with new command names
- [ ] 8.2 Add examples for `--include`/`--exclude` usage
- [ ] 8.3 Document inference fallback behavior (backticks, unknown type)
- [ ] 8.4 Add migration guide for users (old → new commands)
- [ ] 8.5 Document common utilities for future scanner development
- [ ] 8.6 Add API documentation for `upcast.common` package
- [ ] 8.7 Update CONTRIBUTING.md with refactoring guidelines

**Validation**: Documentation complete, examples tested

## Phase 9: Testing & Validation (8 tasks)

- [ ] 9.1 Run full test suite: `uv run pytest tests/`
- [ ] 9.2 Verify all scanners pass tests (env-var, django-models, django-settings, prometheus)
- [ ] 9.3 Run linting: `uv run ruff check upcast/ tests/`
- [ ] 9.4 Fix any linting errors
- [ ] 9.5 Test deprecated commands show warnings
- [ ] 9.6 Test file filtering with real projects
- [ ] 9.7 Verify YAML output sorting is consistent
- [ ] 9.8 Performance test: compare before/after execution time

**Validation**: All tests pass, linting clean, no performance regression

## Phase 10: OpenSpec Validation (3 tasks)

- [ ] 10.1 Run `openspec validate refactor-scanner-architecture --strict`
- [ ] 10.2 Resolve any validation errors
- [ ] 10.3 Mark all tasks complete in this checklist

**Validation**: OpenSpec validation passes

## Total: 76 tasks across 10 phases
