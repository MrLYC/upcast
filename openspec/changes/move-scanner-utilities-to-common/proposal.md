# Proposal: Move Scanner Utilities to Common and Delete Old Modules

## Metadata

- **Change ID**: `move-scanner-utilities-to-common`
- **Status**: PROPOSED
- **Created**: 2025-12-22
- **Author**: Assistant
- **Related Changes**: `migrate-main-to-new-scanners` (prerequisite completed)

## Why

### Current State

After completing Phase 1-2 of `migrate-main-to-new-scanners`:

1. **CLI commands consolidated** ✅

   - All 12 commands now use new unified scanners
   - No duplicate `-new` suffixed commands
   - Clean import structure in main.py

2. **Partial module cleanup** ✅

   - Deleted: `exception_handler_scanner/`, `unit_test_scanner/` (no dependencies)
   - Remaining: 4 old modules still needed by new scanners

3. **Utility dependencies blocking deletion** ⚠️

   - **DjangoModelScanner** depends on:

     - `django_model_scanner.ast_utils.is_django_model`
     - `django_model_scanner.model_parser.merge_abstract_fields`
     - `django_model_scanner.model_parser.parse_model`

   - **DjangoUrlScanner** depends on:

     - `django_url_scanner.router_parser.parse_router_registrations`
     - `django_url_scanner.url_parser.parse_url_pattern`
     - `django_url_scanner.view_resolver.resolve_view`

   - **DjangoSettingsScanner** depends on:

     - `django_settings_scanner.ast_utils` (multiple functions)
     - `django_settings_scanner.definition_parser.is_settings_module`
     - `django_settings_scanner.definition_parser.parse_settings_module`

   - **SignalScanner** depends on:
     - `signal_scanner.checker.SignalChecker`

### Problems

1. **Code duplication**: ~25+ files across 4 old modules still exist
2. **Cannot complete cleanup**: Blocked by utility dependencies
3. **Maintenance burden**: Still need to maintain old module code
4. **Import complexity**: New scanners import from old module structure
5. **Technical debt**: Migration 80% complete but stalled

## What Changes

### 1. Extract and Move Utilities

Move utility functions from old modules to appropriate locations in `upcast/common/`:

#### Django Model Utilities

**From**: `upcast/django_model_scanner/`
**To**: `upcast/common/django/`

Files to migrate:

- `ast_utils.py` → `upcast/common/django/model_utils.py`
  - `is_django_model()` function
- `model_parser.py` → `upcast/common/django/model_parser.py`
  - `parse_model()` function
  - `merge_abstract_fields()` function

#### Django URL Utilities

**From**: `upcast/django_url_scanner/`
**To**: `upcast/common/django/`

Files to migrate:

- `router_parser.py` → `upcast/common/django/router_parser.py`
  - `parse_router_registrations()` function
- `url_parser.py` → `upcast/common/django/url_parser.py`
  - `parse_url_pattern()` function
- `view_resolver.py` → `upcast/common/django/view_resolver.py`
  - `resolve_view()` function

#### Django Settings Utilities

**From**: `upcast/django_settings_scanner/`
**To**: `upcast/common/django/`

Files to migrate:

- `ast_utils.py` → `upcast/common/django/settings_utils.py`
  - Extract only used functions
- `definition_parser.py` → `upcast/common/django/settings_parser.py`
  - `is_settings_module()` function
  - `parse_settings_module()` function

#### Signal Utilities

**From**: `upcast/signal_scanner/`
**To**: Inline into `upcast/scanners/signals.py`

**Decision**: Don't move to common, refactor SignalScanner instead

- SignalChecker is tightly coupled to SignalScanner
- Only used by one scanner
- Better to inline the logic directly

### 2. Update Scanner Imports

Update all new scanners to import from `upcast/common/`:

**upcast/scanners/django_models.py**:

```python
# OLD
from upcast.django_model_scanner.ast_utils import is_django_model
from upcast.django_model_scanner.model_parser import merge_abstract_fields, parse_model

# NEW
from upcast.common.django.model_utils import is_django_model
from upcast.common.django.model_parser import merge_abstract_fields, parse_model
```

**upcast/scanners/django_urls.py**:

```python
# OLD
from upcast.django_url_scanner.router_parser import parse_router_registrations
from upcast.django_url_scanner.url_parser import parse_url_pattern
from upcast.django_url_scanner.view_resolver import resolve_view

# NEW
from upcast.common.django.router_parser import parse_router_registrations
from upcast.common.django.url_parser import parse_url_pattern
from upcast.common.django.view_resolver import resolve_view
```

**upcast/scanners/django_settings.py**:

```python
# OLD
from upcast.django_settings_scanner.ast_utils import (...)
from upcast.django_settings_scanner.definition_parser import is_settings_module, parse_settings_module

# NEW
from upcast.common.django.settings_utils import (...)
from upcast.common.django.settings_parser import is_settings_module, parse_settings_module
```

**upcast/scanners/signals.py**:

```python
# OLD
from upcast.signal_scanner.checker import SignalChecker
# ... in scan() method:
checker = SignalChecker(root_path=str(path.resolve()), verbose=self.verbose)

# NEW
# Inline SignalChecker logic directly into SignalScanner.scan()
# Or extract to upcast/common/signals/ if reusable
```

### 3. Delete Old Module Directories

After utilities are moved and imports updated:

**Delete**:

- `upcast/django_model_scanner/` (7 files)
- `upcast/django_url_scanner/` (8 files)
- `upcast/django_settings_scanner/` (8 files)
- `upcast/signal_scanner/` (4 files)

**Also delete test directories**:

- `tests/test_django_model_scanner/`
- `tests/test_django_url_scanner/`
- `tests/test_django_settings_scanner/`
- `tests/test_signal_scanner/`

### 4. Create Common Directory Structure

Establish organized common utility structure:

```
upcast/common/
├── __init__.py
├── scanner_base.py (existing)
├── django/
│   ├── __init__.py
│   ├── model_utils.py (NEW)
│   ├── model_parser.py (NEW)
│   ├── router_parser.py (NEW)
│   ├── url_parser.py (NEW)
│   ├── view_resolver.py (NEW)
│   ├── settings_utils.py (NEW)
│   └── settings_parser.py (NEW)
└── (other common utilities)
```

## Benefits

1. **Complete migration cleanup**: Remove all old module code (~25 files)
2. **Centralized utilities**: Django-related utilities in one place
3. **Easier maintenance**: One location for shared code
4. **Better organization**: Clear separation of concerns
5. **Reduced duplication**: Utilities can be reused by future scanners
6. **Clean architecture**: No dependencies on deprecated modules

## Success Criteria

1. ✅ All utility functions moved to `upcast/common/django/`
2. ✅ All scanner imports updated to use new locations
3. ✅ All tests pass with new import structure
4. ✅ All 4 old module directories deleted
5. ✅ No imports from old modules remain in codebase
6. ✅ Pre-commit checks pass (ruff, ruff-format)
7. ✅ Code coverage maintained at ≥80%

## Out of Scope

- Refactoring utility function logic (just move them)
- Changing scanner behavior or output
- Adding new features to scanners
- Performance optimization
- Documentation updates (will be separate task)

## Risks and Mitigations

### Risk 1: Breaking changes in utility functions

**Mitigation**:

- Copy functions exactly, don't modify logic
- Keep original function signatures
- Run full test suite after each move
- Test scanners individually after import updates

### Risk 2: Hidden dependencies on old modules

**Mitigation**:

- Search entire codebase for imports before deletion
- Use grep to find all references
- Check test files for imports
- Run tests after each deletion

### Risk 3: Test failures after deletion

**Mitigation**:

- Update test imports alongside scanner imports
- Run pytest after each module deletion
- Keep git history for easy rollback
- Delete one module at a time

### Risk 4: SignalScanner refactoring complexity

**Mitigation**:

- Start with simpler modules (django_model, django_url, django_settings)
- Handle signal_scanner last
- Consider keeping SignalChecker temporarily if refactor is too complex
- Can defer signal_scanner deletion if needed

## Migration Strategy

### Phase 1: Prepare Common Directory Structure

1. Create `upcast/common/django/` directory
2. Create `__init__.py` files
3. Set up proper package structure

### Phase 2: Move Django Model Utilities

1. Copy `ast_utils.py` functions to `model_utils.py`
2. Copy `model_parser.py` functions to `model_parser.py`
3. Update DjangoModelScanner imports
4. Run tests for django_model_scanner
5. Delete `upcast/django_model_scanner/` and tests

### Phase 3: Move Django URL Utilities

1. Copy router_parser.py to common
2. Copy url_parser.py to common
3. Copy view_resolver.py to common
4. Update DjangoUrlScanner imports
5. Run tests
6. Delete `upcast/django_url_scanner/` and tests

### Phase 4: Move Django Settings Utilities

1. Extract used functions from ast_utils.py
2. Copy definition_parser.py functions
3. Update DjangoSettingsScanner imports
4. Run tests
5. Delete `upcast/django_settings_scanner/` and tests

### Phase 5: Refactor SignalScanner

1. Inline SignalChecker logic into SignalScanner
2. Or extract to common if reusable
3. Update imports
4. Run tests
5. Delete `upcast/signal_scanner/` and tests

### Phase 6: Final Validation

1. Run complete test suite
2. Verify no old module imports remain
3. Run pre-commit checks
4. Manual testing of all scanners

## Timeline Estimate

- **Phase 1**: 1 hour (setup structure)
- **Phase 2**: 2-3 hours (django_model utilities + tests)
- **Phase 3**: 2-3 hours (django_url utilities + tests)
- **Phase 4**: 2-3 hours (django_settings utilities + tests)
- **Phase 5**: 3-4 hours (signal_scanner refactor)
- **Phase 6**: 1 hour (validation)

**Total**: 11-15 hours of focused work

## Alternative Approaches Considered

### Alternative 1: Leave utilities in old modules temporarily

**Approach**: Keep old modules as utility libraries, just for imports.

**Rejected because**:

- Maintains technical debt indefinitely
- Confusing for developers (why do these modules exist?)
- Still have maintenance burden
- Doesn't complete the migration

### Alternative 2: Inline all utilities into each scanner

**Approach**: Copy utility code directly into scanner files.

**Rejected because**:

- Creates code duplication
- Harder to maintain (same fix in multiple places)
- Violates DRY principle
- Makes scanner files too large

### Alternative 3: Move utilities to separate packages

**Approach**: Create dedicated packages for each utility type.

**Rejected because**:

- Over-engineering for current needs
- Adds complexity without benefit
- Common directory is sufficient
- Can always refactor later if needed

## Dependencies

- **Prerequisite**: `migrate-main-to-new-scanners` Phase 1-2 completed ✅
- **Follows**: CLI consolidation must be done first
- **Blocks**: Final cleanup and documentation updates

## Related Changes

- **Completed**: `migrate-main-to-new-scanners` (Phase 1-2)
- **Next**: Documentation updates after this change completes
