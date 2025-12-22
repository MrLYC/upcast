# Tasks: Migrate main.py to New Scanner Architecture and Remove Old Implementations

## Phase 1: Audit and Preparation (Sequential)

### Task 1.1: Audit dependencies on old modules

- [ ] Search for all imports from old scanner modules across codebase
- [ ] Identify which utilities from old modules are used by new scanners
- [ ] Document dependencies that need to be preserved
- [ ] Create plan for moving shared utilities to `upcast/common/`

**Command to check**:

```bash
rg "from upcast\.(django_model_scanner|django_url_scanner|django_settings_scanner|unit_test_scanner|signal_scanner|exception_handler_scanner)" --type py
```

### Task 1.2: Move shared utilities to common

- [ ] Identify utilities used by new scanners from old modules
- [ ] Move shared utilities to `upcast/common/` if not already there
- [ ] Update imports in new scanners to use common utilities
- [ ] Verify new scanners still work after utility migration
- [ ] Run tests to confirm no breakage

**Examples of utilities that might need moving**:

- `django_model_scanner/ast_utils.py` functions
- `django_url_scanner/router_parser.py`, `url_parser.py`, `view_resolver.py`
- Any shared parsers or helpers

### Task 1.3: Verify new scanner feature parity

- [ ] Compare CLI options between old and new implementations
- [ ] Verify output format compatibility
- [ ] Test new scanners produce same results as old ones
- [ ] Document any intentional differences

## Phase 2: Update main.py Commands (Sequential)

### Task 2.1: Consolidate scan-django-models

- [ ] Remove `scan_django_models_cmd` (old implementation)
- [ ] Rename `scan_django_models_new_cmd` → `scan_django_models_cmd`
- [ ] Update command name from `scan-django-models-new` to `scan-django-models`
- [ ] Remove import: `from upcast.django_model_scanner import scan_django_models`
- [ ] Verify `DjangoModelScanner` import exists in scanners import block
- [ ] Test command works: `upcast scan-django-models --help`

### Task 2.2: Consolidate scan-django-urls

- [ ] Remove `scan_django_urls_cmd` (old implementation)
- [ ] Rename `scan_django_urls_new_cmd` → `scan_django_urls_cmd`
- [ ] Update command name from `scan-django-urls-new` to `scan-django-urls`
- [ ] Remove import: `from upcast.django_url_scanner import scan_django_urls`
- [ ] Verify `DjangoUrlScanner` import exists
- [ ] Test command works: `upcast scan-django-urls --help`

### Task 2.3: Consolidate scan-django-settings

- [ ] Remove `scan_django_settings_cmd` (old implementation)
- [ ] Rename `scan_django_settings_new_cmd` → `scan_django_settings_cmd`
- [ ] Update command name from `scan-django-settings-new` to `scan-django-settings`
- [ ] Remove import: `from upcast.django_settings_scanner import scan_django_settings`
- [ ] Verify `DjangoSettingsScanner` import exists
- [ ] Simplify options (remove old complex mode flags)
- [ ] Test command works: `upcast scan-django-settings --help`

### Task 2.4: Consolidate scan-unit-tests

- [ ] Remove duplicate `scan_unit_tests_cmd` (old implementation, line ~860)
- [ ] Keep `scan_unit_tests_new_cmd` and rename to `scan_unit_tests_cmd`
- [ ] Ensure command name is `scan-unit-tests` (no -new suffix)
- [ ] Remove import: `from upcast.unit_test_scanner.cli import scan_unit_tests`
- [ ] Verify `UnitTestScanner` import exists
- [ ] Test command works: `upcast scan-unit-tests --help`

### Task 2.5: Verify scan-signals

- [ ] Confirm `scan-signals` already uses new `SignalScanner`
- [ ] Remove any deprecated warning from scanner implementation
- [ ] Add `SignalScanner` to main imports if not present
- [ ] Test command works: `upcast scan-signals --help`

### Task 2.6: Clean up imports in main.py

- [ ] Remove all old scanner module imports
- [ ] Ensure all new scanners are in unified import block
- [ ] Remove unused imports
- [ ] Run ruff to check for import errors

**Expected final import block**:

```python
from upcast.scanners import (
    BlockingOperationsScanner,
    ComplexityScanner,
    ConcurrencyScanner,
    DjangoModelScanner,
    DjangoSettingsScanner,
    DjangoUrlScanner,
    EnvVarScanner,
    ExceptionHandlerScanner,
    HttpRequestsScanner,
    MetricsScanner,
    SignalScanner,
    UnitTestScanner,
)
```

## Phase 3: Delete Old Module Directories (Sequential)

### Task 3.1: Remove django_model_scanner

- [ ] Verify no remaining imports from `upcast.django_model_scanner`
- [ ] Check new scanner doesn't depend on this module
- [ ] Delete directory: `rm -rf upcast/django_model_scanner/`
- [ ] Run tests to verify nothing broke
- [ ] Commit: "Remove old django_model_scanner module"

### Task 3.2: Remove django_url_scanner

- [ ] Verify no remaining imports from `upcast.django_url_scanner`
- [ ] Confirm utilities moved to common or new scanner
- [ ] Delete directory: `rm -rf upcast/django_url_scanner/`
- [ ] Run tests to verify nothing broke
- [ ] Commit: "Remove old django_url_scanner module"

### Task 3.3: Remove django_settings_scanner

- [ ] Verify no remaining imports from `upcast.django_settings_scanner`
- [ ] Check new scanner doesn't depend on this module
- [ ] Delete directory: `rm -rf upcast/django_settings_scanner/`
- [ ] Run tests to verify nothing broke
- [ ] Commit: "Remove old django_settings_scanner module"

### Task 3.4: Remove unit_test_scanner

- [ ] Verify no remaining imports from `upcast.unit_test_scanner`
- [ ] Check new scanner doesn't depend on this module
- [ ] Delete directory: `rm -rf upcast/unit_test_scanner/`
- [ ] Run tests to verify nothing broke
- [ ] Commit: "Remove old unit_test_scanner module"

### Task 3.5: Remove signal_scanner

- [ ] Verify no remaining imports from `upcast.signal_scanner`
- [ ] Remove deprecation warning from new SignalScanner
- [ ] Delete directory: `rm -rf upcast/signal_scanner/`
- [ ] Run tests to verify nothing broke
- [ ] Commit: "Remove old signal_scanner module"

### Task 3.6: Remove exception_handler_scanner

- [ ] Verify no remaining imports from `upcast.exception_handler_scanner`
- [ ] Check new scanner doesn't depend on this module
- [ ] Delete directory: `rm -rf upcast/exception_handler_scanner/`
- [ ] Run tests to verify nothing broke
- [ ] Commit: "Remove old exception_handler_scanner module"

## Phase 4: Validation and Cleanup (Sequential)

### Task 4.1: Run complete test suite

- [ ] Run `uv run pytest tests/ -v`
- [ ] Verify all tests pass
- [ ] Fix any test failures
- [ ] Check for import errors

### Task 4.2: Test all CLI commands

- [ ] Test `upcast scan-complexity --help`
- [ ] Test `upcast scan-env-vars --help`
- [ ] Test `upcast scan-blocking-operations --help`
- [ ] Test `upcast scan-http-requests --help`
- [ ] Test `upcast scan-metrics --help`
- [ ] Test `upcast scan-concurrency --help`
- [ ] Test `upcast scan-exception-handlers --help`
- [ ] Test `upcast scan-unit-tests --help`
- [ ] Test `upcast scan-django-urls --help`
- [ ] Test `upcast scan-django-models --help`
- [ ] Test `upcast scan-django-settings --help`
- [ ] Test `upcast scan-signals --help`

### Task 4.3: Test CLI commands with real data

- [ ] Run each scanner on actual test files
- [ ] Verify output format is correct (YAML/JSON)
- [ ] Check summary information is accurate
- [ ] Test with --verbose flag
- [ ] Test with --output flag

### Task 4.4: Run quality checks

- [ ] Run `uv run ruff check`
- [ ] Run `uv run ruff format --check`
- [ ] Fix any linting issues
- [ ] Run `uv run pre-commit run --all-files`

### Task 4.5: Update documentation

- [ ] Update README.md with correct command list
- [ ] Remove references to `-new` commands
- [ ] Update usage examples
- [ ] Add migration notes if needed
- [ ] Document any breaking changes

### Task 4.6: Final verification

- [ ] Verify no old module directories remain
- [ ] Check no imports from old modules
- [ ] Confirm all CLI commands work
- [ ] Run full test suite one final time
- [ ] Review git diff for unintended changes

## Dependencies

- **Phase 1 must complete first**: Need to identify and preserve dependencies
- **Phase 2 depends on Phase 1**: Can't update main.py until utilities are moved
- **Phase 3 depends on Phase 2**: Can't delete modules until main.py updated
- **Phase 4 is final validation**: Runs after all changes complete

## Notes

- Take incremental approach: update one command at a time
- Commit after each module deletion
- Run tests frequently to catch issues early
- Keep old code until absolutely sure new code works
- Document any differences between old and new implementations
