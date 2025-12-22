# Module Cleanup Specification

## REMOVED Requirements

### Requirement: Old Scanner Module Directories

Old scanner module directories SHALL be removed after migration to new architecture.

#### Scenario: Remove django_model_scanner directory

**GIVEN** the directory `upcast/django_model_scanner/` exists
**WHEN** all functionality is migrated to `upcast/scanners/django_models.py`
**THEN** the directory `upcast/django_model_scanner/` SHALL be deleted
**AND** no code SHALL import from `upcast.django_model_scanner`

#### Scenario: Remove django_url_scanner directory

**GIVEN** the directory `upcast/django_url_scanner/` exists
**WHEN** all functionality is migrated to `upcast/scanners/django_urls.py`
**THEN** the directory `upcast/django_url_scanner/` SHALL be deleted
**AND** no code SHALL import from `upcast.django_url_scanner`

#### Scenario: Remove django_settings_scanner directory

**GIVEN** the directory `upcast/django_settings_scanner/` exists
**WHEN** all functionality is migrated to `upcast/scanners/django_settings.py`
**THEN** the directory `upcast/django_settings_scanner/` SHALL be deleted
**AND** no code SHALL import from `upcast.django_settings_scanner`

#### Scenario: Remove unit_test_scanner directory

**GIVEN** the directory `upcast/unit_test_scanner/` exists
**WHEN** all functionality is migrated to `upcast/scanners/unit_tests.py`
**THEN** the directory `upcast/unit_test_scanner/` SHALL be deleted
**AND** no code SHALL import from `upcast.unit_test_scanner`

#### Scenario: Remove signal_scanner directory

**GIVEN** the directory `upcast/signal_scanner/` exists
**WHEN** all functionality is migrated to `upcast/scanners/signals.py`
**THEN** the directory `upcast/signal_scanner/` SHALL be deleted
**AND** no code SHALL import from `upcast.signal_scanner`
**AND** the deprecation warning SHALL be removed from new scanner

#### Scenario: Remove exception_handler_scanner directory

**GIVEN** the directory `upcast/exception_handler_scanner/` exists
**WHEN** all functionality is migrated to `upcast/scanners/exceptions.py`
**THEN** the directory `upcast/exception_handler_scanner/` SHALL be deleted
**AND** no code SHALL import from `upcast.exception_handler_scanner`

## ADDED Requirements

### Requirement: No Orphaned Imports

After module deletion, no imports from deleted modules SHALL remain in codebase.

#### Scenario: Verify no imports from deleted modules

**GIVEN** old scanner modules have been deleted
**WHEN** the codebase is searched for imports
**THEN** no import statements from deleted modules SHALL be found
**AND** no dynamic imports using strings SHALL reference deleted modules
**AND** no **import** calls SHALL reference deleted modules

**Search command**:

```bash
rg "from upcast\.(django_model_scanner|django_url_scanner|django_settings_scanner|unit_test_scanner|signal_scanner|exception_handler_scanner)" --type py
```

#### Scenario: Tests pass after module deletion

**GIVEN** old scanner modules have been deleted
**WHEN** the complete test suite is executed
**THEN** all tests SHALL pass
**AND** no import errors SHALL occur
**AND** no missing module errors SHALL occur

### Requirement: Shared Utilities Preservation

Utilities needed by new scanners SHALL be moved to common before deletion.

#### Scenario: Move shared utilities to common

**GIVEN** a utility function used by both old and new implementations
**WHEN** the old module is being deleted
**THEN** the utility SHALL be moved to `upcast/common/` first
**AND** imports in new scanners SHALL be updated to use common location
**AND** the utility SHALL be tested to ensure it still works

**Example utilities that might need moving**:

- AST parsing helpers
- URL pattern parsers
- Router registration parsers
- View resolvers
- Test pattern detectors

#### Scenario: Update new scanner imports

**GIVEN** new scanners import utilities from old modules
**WHEN** utilities are moved to common
**THEN** new scanner imports SHALL be updated
**AND** no imports from old modules SHALL remain
**AND** new scanners SHALL still function correctly

**Example before**:

```python
from upcast.django_url_scanner.router_parser import parse_router_registrations
```

**Example after**:

```python
from upcast.common.django_utils import parse_router_registrations
```

## MODIFIED Requirements

None - this change removes old code, no existing specs modified.

## Validation Requirements

### Requirement: Pre-deletion Verification

Before deleting any module, verification steps SHALL be completed.

#### Scenario: Verify module can be deleted

**GIVEN** a module is ready to be deleted
**WHEN** pre-deletion checks are performed
**THEN** the following SHALL be verified:

- No imports from the module exist in production code
- No imports from the module exist in test code
- All tests pass without the module
- CLI commands work without the module
- No utilities from the module are needed by new implementation

#### Scenario: Incremental deletion

**GIVEN** multiple modules need to be deleted
**WHEN** deletion is performed
**THEN** modules SHALL be deleted one at a time
**AND** tests SHALL be run after each deletion
**AND** each deletion SHALL be committed separately
**AND** deletion SHALL stop if any test fails

**Deletion order** (safest first):

1. `exception_handler_scanner` (simple, few dependencies)
2. `unit_test_scanner` (moderate complexity)
3. `signal_scanner` (has deprecation warning)
4. `django_model_scanner` (complex, check dependencies)
5. `django_url_scanner` (complex, many utilities)
6. `django_settings_scanner` (complex, multiple modes)
