# Tasks: Move Scanner Utilities to Common and Delete Old Modules

## Phase 1: Prepare Common Directory Structure

### Task 1.1: Create django common directory structure

- [ ] Create directory `upcast/common/django/`
- [ ] Create `upcast/common/django/__init__.py`
- [ ] Verify directory structure is correct
- [ ] Run import test to verify package is recognized

## Phase 2: Move Django Model Utilities

### Task 2.1: Extract model utilities

- [ ] Review `django_model_scanner/ast_utils.py`
- [ ] Identify `is_django_model()` function and dependencies
- [ ] Copy to `upcast/common/django/model_utils.py`
- [ ] Preserve all function signatures and logic exactly
- [ ] Add proper module docstring and imports

### Task 2.2: Extract model parser

- [ ] Review `django_model_scanner/model_parser.py`
- [ ] Identify `parse_model()` and `merge_abstract_fields()` functions
- [ ] Copy to `upcast/common/django/model_parser.py`
- [ ] Include all helper functions used by these functions
- [ ] Preserve docstrings and type hints

### Task 2.3: Update DjangoModelScanner imports

- [ ] Update imports in `upcast/scanners/django_models.py`:
  ```python
  from upcast.common.django.model_utils import is_django_model
  from upcast.common.django.model_parser import merge_abstract_fields, parse_model
  ```
- [ ] Remove old imports
- [ ] Verify no other files import from django_model_scanner

### Task 2.4: Test and delete django_model_scanner

- [ ] Run `uv run pytest tests/test_scanners/test_django_models.py -v`
- [ ] Verify DjangoModelScanner still works correctly
- [ ] Search for remaining imports: `rg "django_model_scanner" --type py`
- [ ] Delete `upcast/django_model_scanner/`
- [ ] Delete `tests/test_django_model_scanner/`
- [ ] Run full test suite to verify nothing broke
- [ ] Commit: "Move django model utilities to common and delete old module"

## Phase 3: Move Django URL Utilities

### Task 3.1: Extract router parser

- [ ] Review `django_url_scanner/router_parser.py`
- [ ] Copy `parse_router_registrations()` and dependencies
- [ ] Create `upcast/common/django/router_parser.py`
- [ ] Preserve all function logic exactly

### Task 3.2: Extract URL parser

- [ ] Review `django_url_scanner/url_parser.py`
- [ ] Copy `parse_url_pattern()` and dependencies
- [ ] Create `upcast/common/django/url_parser.py`
- [ ] Include helper functions if needed

### Task 3.3: Extract view resolver

- [ ] Review `django_url_scanner/view_resolver.py`
- [ ] Copy `resolve_view()` and dependencies
- [ ] Create `upcast/common/django/view_resolver.py`
- [ ] Preserve import resolution logic

### Task 3.4: Update DjangoUrlScanner imports

- [ ] Update imports in `upcast/scanners/django_urls.py`:
  ```python
  from upcast.common.django.router_parser import parse_router_registrations
  from upcast.common.django.url_parser import parse_url_pattern
  from upcast.common.django.view_resolver import resolve_view
  ```
- [ ] Remove old imports
- [ ] Verify no other files import from django_url_scanner

### Task 3.5: Test and delete django_url_scanner

- [ ] Run `uv run pytest tests/test_scanners/test_django_urls.py -v`
- [ ] Verify DjangoUrlScanner works correctly
- [ ] Search for remaining imports: `rg "django_url_scanner" --type py`
- [ ] Delete `upcast/django_url_scanner/`
- [ ] Delete `tests/test_django_url_scanner/`
- [ ] Run full test suite
- [ ] Commit: "Move django url utilities to common and delete old module"

## Phase 4: Move Django Settings Utilities

### Task 4.1: Extract settings utilities

- [ ] Review `django_settings_scanner/ast_utils.py`
- [ ] Identify which functions are actually used by new scanner
- [ ] Copy only used functions to `upcast/common/django/settings_utils.py`
- [ ] Exclude unused utility code

### Task 4.2: Extract settings parser

- [ ] Review `django_settings_scanner/definition_parser.py`
- [ ] Copy `is_settings_module()` and `parse_settings_module()`
- [ ] Create `upcast/common/django/settings_parser.py`
- [ ] Include all dependencies

### Task 4.3: Update DjangoSettingsScanner imports

- [ ] Update imports in `upcast/scanners/django_settings.py`:
  ```python
  from upcast.common.django.settings_utils import (...)
  from upcast.common.django.settings_parser import is_settings_module, parse_settings_module
  ```
- [ ] Remove old imports
- [ ] Verify no other files import from django_settings_scanner

### Task 4.4: Test and delete django_settings_scanner

- [ ] Run `uv run pytest tests/test_scanners/test_django_settings.py -v`
- [ ] Verify DjangoSettingsScanner works correctly
- [ ] Search for remaining imports: `rg "django_settings_scanner" --type py`
- [ ] Delete `upcast/django_settings_scanner/`
- [ ] Delete `tests/test_django_settings_scanner/`
- [ ] Run full test suite
- [ ] Commit: "Move django settings utilities to common and delete old module"

## Phase 5: Refactor SignalScanner

### Task 5.1: Analyze SignalChecker dependencies

- [ ] Review `signal_scanner/checker.py`
- [ ] Identify SignalChecker class and methods
- [ ] Understand how it's used by SignalScanner
- [ ] Decide: inline into scanner or extract to common

### Task 5.2: Refactor SignalScanner

**Option A: Inline SignalChecker logic**

- [ ] Copy SignalChecker logic into `SignalScanner.scan()` method
- [ ] Adapt to use SignalScanner's internal state
- [ ] Remove SignalChecker instantiation

**Option B: Extract to common**

- [ ] Create `upcast/common/signals/signal_checker.py`
- [ ] Move SignalChecker class to common
- [ ] Update SignalScanner import

### Task 5.3: Update SignalScanner implementation

- [ ] Implement chosen refactoring approach
- [ ] Update imports in `upcast/scanners/signals.py`
- [ ] Remove deprecation warnings from old implementation
- [ ] Verify logic equivalence

### Task 5.4: Test and delete signal_scanner

- [ ] Run `uv run pytest tests/test_scanners/test_signal.py -v`
- [ ] Verify SignalScanner works correctly
- [ ] Test with real signal detection scenarios
- [ ] Search for remaining imports: `rg "signal_scanner" --type py`
- [ ] Delete `upcast/signal_scanner/`
- [ ] Delete `tests/test_signal_scanner/` (update imports in tests first if needed)
- [ ] Run full test suite
- [ ] Commit: "Refactor SignalScanner and delete old signal_scanner module"

## Phase 6: Final Validation and Cleanup

### Task 6.1: Verify no old imports remain

- [ ] Search for old module imports:
  ```bash
  rg "from upcast\.(django_model_scanner|django_url_scanner|django_settings_scanner|signal_scanner)" --type py
  ```
- [ ] Verify only documentation references remain (if any)
- [ ] Check no dynamic imports or string references

### Task 6.2: Run complete test suite

- [ ] Run `uv run pytest tests/ -v`
- [ ] Verify all tests pass (expect 100% pass rate)
- [ ] Check test coverage: `uv run pytest --cov=upcast --cov-report=term-missing`
- [ ] Ensure coverage is ≥80%

### Task 6.3: Run quality checks

- [ ] Run `uv run ruff check .`
- [ ] Run `uv run ruff format --check .`
- [ ] Run `uv run pre-commit run --all-files`
- [ ] Fix any issues found

### Task 6.4: Test all CLI commands

- [ ] Test each scanner command with `--help`
- [ ] Test with sample data to verify output
- [ ] Verify all 12 scanners work correctly:
  - scan-django-models
  - scan-django-urls
  - scan-django-settings
  - scan-signals
  - scan-unit-tests
  - scan-exception-handlers
  - scan-complexity
  - scan-env-vars
  - scan-blocking-operations
  - scan-http-requests
  - scan-metrics
  - scan-concurrency

### Task 6.5: Verify directory cleanup

- [ ] List remaining directories: `ls upcast/`
- [ ] Confirm old modules are deleted:
  - No `django_model_scanner/`
  - No `django_url_scanner/`
  - No `django_settings_scanner/`
  - No `signal_scanner/`
  - No `exception_handler_scanner/`
  - No `unit_test_scanner/`
- [ ] Verify `upcast/common/django/` exists with new utilities

### Task 6.6: Update common package exports

- [ ] Update `upcast/common/django/__init__.py` to export utilities:

  ```python
  from upcast.common.django.model_utils import is_django_model
  from upcast.common.django.model_parser import merge_abstract_fields, parse_model
  from upcast.common.django.router_parser import parse_router_registrations
  from upcast.common.django.url_parser import parse_url_pattern
  from upcast.common.django.view_resolver import resolve_view
  from upcast.common.django.settings_utils import (...)
  from upcast.common.django.settings_parser import is_settings_module, parse_settings_module

  __all__ = [...]
  ```

- [ ] Verify imports work from package level

### Task 6.7: Final commit and documentation

- [ ] Final commit: "Complete scanner utility migration to common"
- [ ] Update OpenSpec status to COMPLETED
- [ ] Document any notable changes or gotchas
- [ ] Archive change proposal

## Dependencies

- **Prerequisite**: `migrate-main-to-new-scanners` Phase 1-2 completed ✅
- **Phase 1**: Can start immediately (directory setup)
- **Phase 2-5**: Sequential execution recommended (one module at a time)
- **Phase 6**: Runs after all phases complete

## Notes

- Work incrementally: complete one module at a time
- Commit after each module deletion
- Run tests frequently to catch issues early
- If SignalScanner refactor is too complex, can defer to separate change
- Keep exact function signatures to avoid breaking changes
- Use git to track what was moved from where
