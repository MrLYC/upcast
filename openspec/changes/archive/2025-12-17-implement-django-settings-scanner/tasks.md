# Tasks: Implement Django Settings Scanner

## Phase 1: Foundation Setup

- [x] Create module directory structure `upcast/django_settings_scanner/`
- [x] Create `__init__.py` with public API export
- [x] Create `ast_utils.py` with function stubs
- [x] Create `settings_parser.py` with dataclass definitions
- [x] Create empty `checker.py`, `export.py`, `cli.py`

## Phase 2: Pattern Detection (ast_utils.py)

- [x] Implement `is_django_settings(node)` - validate settings origin from django.conf
- [x] Implement `is_settings_attribute_access(node)` - detect `settings.KEY`
- [x] Implement `is_settings_getattr_call(node)` - detect `getattr(settings, "KEY")`
- [x] Implement `is_settings_hasattr_call(node)` - detect `hasattr(settings, "KEY")`
- [x] Implement `extract_setting_name(node)` - extract variable name from any pattern
- [x] Implement `extract_getattr_default(node)` - extract default value from getattr
- [x] Add docstrings and type hints to all functions

## Phase 3: Data Structures (settings_parser.py)

- [x] Define `SettingsUsage` dataclass with file, line, column, pattern, code fields
- [x] Define `SettingsVariable` dataclass with name, count, locations fields
- [x] Implement `parse_settings_attribute(node)` - parse attribute access
- [x] Implement `parse_settings_getattr(node)` - parse getattr call
- [x] Implement `parse_settings_hasattr(node)` - parse hasattr call
- [x] Implement `parse_settings_usage(node)` - unified parsing function
- [x] Add helper to extract source code snippet from AST node

## Phase 4: AST Visitor (checker.py)

- [x] Create `DjangoSettingsChecker` class extending astroid NodeVisitor
- [x] Implement `__init__(base_path)` - initialize settings dict
- [x] Implement `visit_Attribute(node)` - handle attribute access patterns
- [x] Implement `visit_Call(node)` - handle getattr/hasattr patterns
- [x] Implement `_register_usage(variable_name, usage)` - aggregate by variable
- [x] Implement `check_file(file_path)` - parse and visit file
- [x] Add error handling for parse failures

## Phase 5: YAML Export (export.py)

- [x] Implement `format_settings_output(settings_dict)` - convert to YAML structure
- [x] Sort variables alphabetically in output
- [x] Sort locations by (file, line) within each variable
- [x] Implement `export_to_yaml(settings_dict, output_path)` - write to file
- [x] Implement `export_to_yaml_string(settings_dict)` - return YAML string
- [x] Configure YAML writer: UTF-8, 2-space indent, block style
- [x] Add validation for output path creation

## Phase 6: CLI Interface (cli.py)

- [x] Implement `scan_django_settings(path, output, verbose)` - main entry point
- [x] Implement `_validate_path(path)` - check if path exists
- [x] Implement `_collect_python_files(path)` - recursive file discovery
- [x] Filter out venv/, build/, **pycache**/ directories
- [x] Implement progress reporting with click.echo
- [x] Implement `_process_files(checker, files, verbose)` - scan files with progress
- [x] Add error handling for file access failures
- [x] Add summary output (N settings found in M files)

## Phase 7: Main CLI Integration

- [x] Add import in `upcast/main.py`: `from upcast.django_settings_scanner import scan_django_settings`
- [x] Create `@main.command()` decorator for `scan_django_settings_cmd`
- [x] Add click arguments: `path` (required), `-o/--output` (optional), `-v/--verbose` (flag)
- [x] Wire up CLI command to call `scan_django_settings()`
- [x] Test CLI command: `uv run upcast scan-django-settings --help`

## Phase 8: Unit Tests - AST Utils

- [ ] Create `tests/test_django_settings_scanner/test_ast_utils.py`
- [ ] Test `is_django_settings()` with django.conf.settings imports
- [ ] Test `is_django_settings()` with non-Django settings (negative case)
- [ ] Test `is_settings_attribute_access()` with `settings.KEY` patterns
- [ ] Test `is_settings_getattr_call()` with various getattr patterns
- [ ] Test `is_settings_hasattr_call()` with hasattr patterns
- [ ] Test `extract_setting_name()` for all pattern types
- [ ] Test import aliases: `from django.conf import settings as config`

## Phase 9: Unit Tests - Parser

- [ ] Create `tests/test_django_settings_scanner/test_settings_parser.py`
- [ ] Test `parse_settings_attribute()` extracts correct metadata
- [ ] Test `parse_settings_getattr()` extracts name and default
- [ ] Test `parse_settings_hasattr()` extracts name
- [ ] Test `parse_settings_usage()` handles all three patterns
- [ ] Test dataclass field types and validation
- [ ] Test source code snippet extraction

## Phase 10: Unit Tests - Checker

- [ ] Create `tests/test_django_settings_scanner/test_checker.py`
- [ ] Test `DjangoSettingsChecker` visits attribute access correctly
- [ ] Test checker visits getattr calls correctly
- [ ] Test checker visits hasattr calls correctly
- [ ] Test aggregation: same variable in multiple files
- [ ] Test aggregation: multiple usages in same file
- [ ] Test error handling for unparseable files

## Phase 11: Unit Tests - Export

- [ ] Create `tests/test_django_settings_scanner/test_export.py`
- [ ] Test `format_settings_output()` generates correct YAML structure
- [ ] Test variable name sorting (alphabetical)
- [ ] Test location sorting (file, line)
- [ ] Test `export_to_yaml()` writes valid YAML to file
- [ ] Test `export_to_yaml_string()` returns valid YAML string
- [ ] Test UTF-8 encoding and special characters
- [ ] Test empty results handling

## Phase 12: Unit Tests - CLI

- [ ] Create `tests/test_django_settings_scanner/test_cli.py`
- [ ] Test `scan_django_settings()` with directory path
- [ ] Test `scan_django_settings()` with single file path
- [ ] Test output file creation with `-o` option
- [ ] Test verbose mode output
- [ ] Test error handling for nonexistent paths
- [ ] Test file filtering (excludes **pycache**, venv/)

## Phase 13: Test Fixtures

- [x] Create `tests/test_django_settings_scanner/fixtures/simple_settings.py`
  - Basic `settings.KEY` patterns
  - Multiple variables
- [x] Create `fixtures/getattr_patterns.py`
  - `getattr(settings, "KEY")` with and without defaults
  - `hasattr(settings, "KEY")`
- [x] Create `fixtures/aliased_imports.py`
  - `from django.conf import settings as config`
  - `import django.conf as conf; conf.settings.KEY`
- [x] Create `fixtures/non_django_settings.py`
  - Local `settings = {}` object (should NOT be detected)
  - `from myapp.settings import KEY` (should NOT be detected)
- [x] Create `fixtures/mixed_settings.py`
  - Both Django and non-Django settings in same file
  - Verify only Django settings detected

## Phase 14: Integration Testing

- [ ] Run full test suite: `uv run pytest tests/test_django_settings_scanner/`
- [ ] Verify all tests pass (target: 45+ tests)
- [x] Run linting: `uv run ruff check upcast/django_settings_scanner/`
- [x] Fix any linting errors
- [x] Test CLI command manually on fixtures directory
- [x] Verify output YAML is valid and readable

## Phase 15: Documentation

- [ ] Add docstrings to all public functions
- [ ] Update main README with scan-django-settings command
- [ ] Add usage examples in README
- [ ] Document limitations (dynamic variable names)
- [ ] Add CLI help text with examples

## Phase 16: Validation

- [ ] Run `openspec validate implement-django-settings-scanner --strict`
- [ ] Resolve any validation errors
- [ ] Verify all tasks marked complete
- [ ] Test on a real Django project (if available)
- [ ] Confirm zero false positives on non-Django settings
