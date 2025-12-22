# Proposal: Migrate main.py to New Scanner Architecture and Remove Old Implementations

## Metadata

- **Change ID**: `migrate-main-to-new-scanners`
- **Status**: PROPOSED
- **Created**: 2025-12-22
- **Author**: Assistant
- **Related Issues**: N/A

## Why

### Current State

After the successful migration of 11 scanners to unified architecture (completed in `refactor-scanners-to-use-models`), the codebase has:

1. **Two parallel architectures**:

   - **New**: `upcast/scanners/` with unified BaseScanner + Pydantic models
   - **Old**: Individual scanner packages (`django_model_scanner/`, `signal_scanner/`, etc.)

2. **Inconsistent CLI commands in main.py**:

   - Some commands use new architecture (complexity, env-vars, blocking-operations, etc.)
   - Some commands still use old implementations (django-models, django-urls, django-settings, unit-tests, signals)
   - Duplicate commands exist (e.g., `scan-django-models` vs `scan-django-models-new`)

3. **Old modules still referenced**:
   - `upcast/django_model_scanner/` (7 files)
   - `upcast/django_url_scanner/` (multiple files)
   - `upcast/django_settings_scanner/` (multiple files)
   - `upcast/unit_test_scanner/` (4 files)
   - `upcast/signal_scanner/` (4 files)
   - `upcast/exception_handler_scanner/` (3 files)

### Problems

1. **Code duplication**: Two implementations for same functionality
2. **Maintenance burden**: Bug fixes need to be applied in two places
3. **Inconsistent UX**: Different commands have different behaviors and options
4. **Confusing naming**: Commands like `-new` suffix are temporary workarounds
5. **Technical debt**: Old code prevents complete cleanup of migration
6. **Import complexity**: New scanners still import utilities from old modules

## What Changes

### 1. Update main.py CLI Commands

Replace all old scanner invocations with new unified scanners:

**Commands to migrate**:

- `scan-django-models` → Use `DjangoModelScanner` from `upcast.scanners`
- `scan-django-urls` → Use `DjangoUrlScanner` from `upcast.scanners`
- `scan-django-settings` → Use `DjangoSettingsScanner` from `upcast.scanners`
- `scan-unit-tests` → Already has new version, remove old duplicate
- `scan-signals` → Already uses new scanner, verified working

**Commands with duplicates to consolidate**:

- Remove `scan-django-models-new` → merge into `scan-django-models`
- Remove `scan-django-urls-new` → merge into `scan-django-urls`
- Remove `scan-django-settings-new` → merge into `scan-django-settings`
- Remove duplicate `scan-unit-tests` → keep only new implementation

### 2. Remove Old Scanner Module Imports

Clean up all imports from old modules in `main.py`:

**Remove**:

```python
from upcast.django_model_scanner import scan_django_models
from upcast.django_settings_scanner import scan_django_settings
from upcast.django_url_scanner import scan_django_urls
from upcast.unit_test_scanner.cli import scan_unit_tests
```

**Keep** (already using new architecture):

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
    SignalScanner,  # Added
    UnitTestScanner,
)
```

### 3. Delete Old Scanner Module Directories

After verifying all functionality is migrated:

**Directories to remove**:

- `upcast/django_model_scanner/` - 7 files
- `upcast/django_url_scanner/` - multiple files
- `upcast/django_settings_scanner/` - multiple files
- `upcast/unit_test_scanner/` - 4 files
- `upcast/signal_scanner/` - 4 files
- `upcast/exception_handler_scanner/` - 3 files

**Note**: Check if any utilities from these modules are still needed by new scanners. If so, move them to `upcast/common/` first.

### 4. Update CLI Command Names

Remove `-new` suffixes and consolidate duplicate commands:

**Before**:

- `scan-django-models` (old)
- `scan-django-models-new` (new)

**After**:

- `scan-django-models` (using new scanner)

### 5. Verify All Tests Pass

Ensure existing tests work with updated commands:

- Run full test suite
- Verify CLI commands work correctly
- Check backward compatibility for users

## Benefits

1. **Single source of truth**: One implementation per scanner
2. **Consistent UX**: All commands use same architecture and patterns
3. **Easier maintenance**: Bug fixes only need one location
4. **Cleaner codebase**: Remove ~30+ files of duplicate code
5. **Clear migration complete**: Remove all migration artifacts
6. **Better documentation**: Clear which commands to use

## Success Criteria

1. ✅ All CLI commands in main.py use new scanner architecture
2. ✅ No duplicate commands (remove all `-new` suffixed commands)
3. ✅ All old scanner module directories deleted
4. ✅ All tests pass with new implementation
5. ✅ No imports from old modules remain
6. ✅ CLI commands maintain backward compatibility
7. ✅ Documentation updated to reflect changes

## Out of Scope

- Adding new scanner features
- Changing scanner behavior or algorithms
- Modifying output formats
- Performance optimization
- Adding new CLI options

## Risks and Mitigations

### Risk 1: Breaking changes for users

**Mitigation**:

- Maintain same CLI command names (just change implementation)
- Keep same output formats (YAML/JSON)
- Run full test suite to catch regressions
- Test CLI commands manually before release

### Risk 2: Utilities still needed from old modules

**Mitigation**:

- Audit new scanners for imports from old modules
- Move any still-needed utilities to `upcast/common/`
- Update imports before deleting old modules
- Verify no import errors after deletion

### Risk 3: Hidden dependencies on old code

**Mitigation**:

- Search entire codebase for imports from old modules
- Run full test suite after changes
- Check for dynamic imports or string-based references
- Use grep to find all references before deletion

### Risk 4: Documentation becomes outdated

**Mitigation**:

- Update README.md with new command structure
- Remove references to old implementations
- Update any inline documentation in code
- Add migration notes for users of old commands

## Migration Notes

This change completes the scanner architecture migration started in previous changes. After this change:

- All scanners use unified `BaseScanner` architecture
- All scanners use Pydantic models for type safety
- All scanners use `run_scanner_cli` for consistent CLI behavior
- No duplicate implementations remain
- Codebase is significantly cleaner and more maintainable
