# Design: Migrate main.py to New Scanner Architecture

## Problem

The codebase has two parallel scanner architectures after migration:

- **New**: Unified architecture in `upcast/scanners/` using `BaseScanner` + Pydantic models
- **Old**: Individual packages (`django_model_scanner/`, `signal_scanner/`, etc.)

This creates:

- Code duplication (~30+ files)
- Inconsistent CLI behavior
- Maintenance overhead
- Confusing user experience (duplicate commands with `-new` suffix)

## Solution Architecture

### High-Level Approach

Complete the scanner migration by:

1. **Audit phase**: Identify and preserve any utilities still needed from old modules
2. **Consolidation phase**: Update all CLI commands to use new scanners
3. **Cleanup phase**: Delete old module directories
4. **Validation phase**: Ensure everything works correctly

### Component Relationships

```
Before:
┌─────────────────────────────────────────┐
│           upcast/main.py                │
│                                         │
│  ┌────────────────┐  ┌───────────────┐ │
│  │ Old Imports    │  │ New Imports   │ │
│  │ - django_model │  │ - scanners.   │ │
│  │   _scanner     │  │   Django      │ │
│  │ - signal_      │  │   ModelScanner│ │
│  │   scanner      │  │ - scanners.   │ │
│  │ - etc.         │  │   Complexity  │ │
│  └────────────────┘  └───────────────┘ │
└─────────────────────────────────────────┘
           │                    │
           ↓                    ↓
    ┌─────────────┐      ┌──────────────┐
    │ Old Modules │      │ New Scanners │
    │ - 6 dirs    │      │ - 1 unified  │
    │ - ~30 files │      │   package    │
    └─────────────┘      └──────────────┘

After:
┌─────────────────────────────────────────┐
│           upcast/main.py                │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │     Unified Scanner Imports      │  │
│  │  from upcast.scanners import (  │  │
│  │    DjangoModelScanner,          │  │
│  │    SignalScanner,               │  │
│  │    UnitTestScanner,             │  │
│  │    ... all 12 scanners          │  │
│  │  )                              │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
                    │
                    ↓
             ┌──────────────┐
             │ New Scanners │
             │ - 1 unified  │
             │   package    │
             │ - BaseScanner│
             │ - Pydantic   │
             └──────────────┘
```

### Key Design Decisions

#### 1. Incremental Deletion Strategy

**Decision**: Delete old modules one at a time with testing between each deletion.

**Rationale**:

- Minimizes risk of breaking changes
- Easier to identify which deletion caused issues
- Can be rolled back module-by-module if needed
- Each deletion is a separate commit for git history

**Order of deletion** (safest first):

1. `exception_handler_scanner` - Simple, few dependencies
2. `unit_test_scanner` - Moderate complexity
3. `signal_scanner` - Has deprecation warning to remove
4. `django_model_scanner` - Complex, check for shared utilities
5. `django_url_scanner` - Complex, many utility files
6. `django_settings_scanner` - Most complex, multiple modes

#### 2. Utility Preservation

**Decision**: Move shared utilities to `upcast/common/` before deletion.

**Rationale**:

- New scanners may still use utilities from old modules
- Prevents import errors after deletion
- Centralizes common code for future reuse
- Examples: AST parsing, URL pattern parsing, router parsing

**Process**:

1. Search for imports from old modules in new scanners
2. Identify utilities that are still needed
3. Move to appropriate location in `upcast/common/`
4. Update imports in new scanners
5. Test before deletion

#### 3. CLI Command Consolidation

**Decision**: Keep original command names, remove `-new` suffixes.

**Rationale**:

- Maintains backward compatibility for users
- Clearer user experience (no confusion about which to use)
- Follows principle of least surprise
- Users' existing scripts continue to work

**Implementation**:

```python
# Remove old command
@main.command(name="scan-django-models")  # OLD - DELETE
def scan_django_models_cmd(...):
    scan_django_models(...)  # Old implementation

@main.command(name="scan-django-models-new")  # NEW - RENAME
def scan_django_models_new_cmd(...):
    scanner = DjangoModelScanner(...)  # New implementation

# After consolidation:
@main.command(name="scan-django-models")  # FINAL
def scan_django_models_cmd(...):
    scanner = DjangoModelScanner(...)  # New implementation
```

#### 4. Testing Strategy

**Decision**: Run full test suite after each major change.

**Testing checkpoints**:

1. After moving each utility to common
2. After updating each CLI command
3. After deleting each old module
4. Final full test suite run
5. Manual CLI command testing

**Validation criteria**:

- All unit tests pass
- All CLI commands execute without errors
- Output format matches expected structure
- No import errors in any module

### Migration Safety Mechanisms

1. **Pre-deletion checklist**:

   - [ ] Search for imports from module
   - [ ] Verify no test imports remain
   - [ ] Check for utility dependencies
   - [ ] Run full test suite
   - [ ] Test CLI commands

2. **Rollback plan**:

   - Each deletion is separate commit
   - Can revert specific module deletion if needed
   - Git history preserves old code
   - Can cherry-pick fixes if needed

3. **User impact mitigation**:
   - Command names stay the same
   - Output format remains compatible
   - Options remain backward compatible
   - No breaking changes to CLI interface

## Alternative Approaches Considered

### Alternative 1: Big Bang Migration

**Approach**: Update all commands and delete all modules at once.

**Rejected because**:

- High risk of breaking multiple things
- Difficult to debug if something breaks
- No way to isolate which change caused issue
- All-or-nothing approach

### Alternative 2: Keep Both Implementations

**Approach**: Maintain both old and new scanners indefinitely.

**Rejected because**:

- Doubles maintenance burden
- Confusing for users
- Wastes disk space and mental overhead
- Defeats purpose of migration

### Alternative 3: Change Command Names

**Approach**: Keep old commands with old code, add new commands with new code.

**Rejected because**:

- Breaks user scripts
- Creates permanent confusion
- Doesn't clean up technical debt
- Not truly completing the migration

## Implementation Phases

### Phase 1: Audit (1-2 hours)

- Search codebase for old module imports
- Identify shared utilities
- Document dependencies
- Plan utility migration

### Phase 2: Consolidate CLI (2-3 hours)

- Update main.py imports
- Consolidate duplicate commands
- Remove `-new` suffixes
- Test each command

### Phase 3: Delete Modules (2-3 hours)

- Delete one module at a time
- Run tests after each deletion
- Commit each deletion separately
- Fix any issues immediately

### Phase 4: Validate (1 hour)

- Run full test suite
- Test all CLI commands manually
- Run quality checks (ruff, pre-commit)
- Update documentation

**Total estimated time**: 6-9 hours

## Success Metrics

1. ✅ Zero old module directories remain
2. ✅ Zero imports from old modules
3. ✅ All 12 CLI commands work correctly
4. ✅ No duplicate commands exist
5. ✅ All tests pass
6. ✅ Code quality checks pass
7. ✅ Documentation updated

## Risks and Mitigations

| Risk                         | Impact | Probability | Mitigation                          |
| ---------------------------- | ------ | ----------- | ----------------------------------- |
| Break existing CLI commands  | High   | Low         | Maintain same command names/options |
| Import errors after deletion | Medium | Medium      | Pre-deletion audit and testing      |
| Utilities still needed       | Medium | Low         | Move to common before deletion      |
| Test failures                | Medium | Low         | Run tests after each change         |
| User scripts break           | High   | Very Low    | Maintain backward compatibility     |

## Conclusion

This incremental, test-driven approach ensures safe migration completion while maintaining backward compatibility and minimizing risk. The consolidation improves codebase maintainability and provides clearer user experience.
