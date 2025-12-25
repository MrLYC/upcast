# Design: Move Scanner Utilities to Common and Delete Old Modules

## Problem

After completing CLI consolidation in `migrate-main-to-new-scanners`, 4 old scanner modules remain because new scanners still depend on their utility functions:

```
upcast/scanners/django_models.py
  ↓ imports from
upcast/django_model_scanner/ast_utils.py
upcast/django_model_scanner/model_parser.py

upcast/scanners/django_urls.py
  ↓ imports from
upcast/django_url_scanner/router_parser.py
upcast/django_url_scanner/url_parser.py
upcast/django_url_scanner/view_resolver.py

upcast/scanners/django_settings.py
  ↓ imports from
upcast/django_settings_scanner/ast_utils.py
upcast/django_settings_scanner/definition_parser.py

upcast/scanners/signals.py
  ↓ imports from
upcast/signal_scanner/checker.py
```

This prevents completing the migration cleanup and maintains technical debt.

## Solution Architecture

### High-Level Approach

1. **Extract utilities** from old modules to `upcast/common/django/`
2. **Update scanner imports** to use new utility locations
3. **Delete old modules** once no longer referenced
4. **Validate** all scanners work with new structure

### Component Relationships

```
Before:
┌─────────────────────────────────────┐
│     upcast/scanners/               │
│  ┌────────────────────────────┐   │
│  │ DjangoModelScanner         │   │
│  │ DjangoUrlScanner           │   │
│  │ DjangoSettingsScanner      │   │
│  │ SignalScanner              │   │
│  └──────────┬─────────────────┘   │
└─────────────┼───────────────────────┘
              │ imports from
              ↓
┌─────────────────────────────────────┐
│  Old Modules (to be deleted)       │
│  - django_model_scanner/           │
│  - django_url_scanner/             │
│  - django_settings_scanner/        │
│  - signal_scanner/                 │
└─────────────────────────────────────┘

After:
┌─────────────────────────────────────┐
│     upcast/scanners/               │
│  ┌────────────────────────────┐   │
│  │ DjangoModelScanner         │   │
│  │ DjangoUrlScanner           │   │
│  │ DjangoSettingsScanner      │   │
│  │ SignalScanner              │   │
│  └──────────┬─────────────────┘   │
└─────────────┼───────────────────────┘
              │ imports from
              ↓
┌─────────────────────────────────────┐
│  upcast/common/django/             │
│  ┌──────────────────────────────┐ │
│  │ model_utils.py               │ │
│  │ model_parser.py              │ │
│  │ router_parser.py             │ │
│  │ url_parser.py                │ │
│  │ view_resolver.py             │ │
│  │ settings_utils.py            │ │
│  │ settings_parser.py           │ │
│  └──────────────────────────────┘ │
└─────────────────────────────────────┘
```

### Key Design Decisions

#### 1. Create Django-Specific Common Directory

**Decision**: Create `upcast/common/django/` for Django-related utilities.

**Rationale**:

- Groups related Django utilities together
- Keeps `upcast/common/` organized by framework/domain
- Allows future addition of other framework utilities
- Clear namespace: `from upcast.common.django import ...`

**Structure**:

```
upcast/common/
├── __init__.py
├── scanner_base.py (existing)
├── django/
│   ├── __init__.py
│   ├── model_utils.py
│   ├── model_parser.py
│   ├── router_parser.py
│   ├── url_parser.py
│   ├── view_resolver.py
│   ├── settings_utils.py
│   └── settings_parser.py
```

#### 2. Copy Functions, Don't Refactor

**Decision**: Copy utility functions exactly as-is, preserve all logic.

**Rationale**:

- Minimizes risk of breaking changes
- Keeps function signatures compatible
- Avoids scope creep (refactoring is separate concern)
- Easier to verify correctness (no logic changes)

**Implementation**:

- Copy function implementations verbatim
- Keep original docstrings and type hints
- Preserve helper functions if used
- Maintain same import dependencies

#### 3. Handle SignalScanner Differently

**Decision**: Inline SignalChecker into SignalScanner instead of moving to common.

**Rationale**:

- SignalChecker is tightly coupled to SignalScanner
- Only used by one scanner (not shared utility)
- Inlining simplifies the code
- No other scanner needs signal checking logic

**Implementation Options**:

**Option A: Inline into scan() method** (Recommended)

```python
class SignalScanner(BaseScanner[SignalOutput]):
    def scan(self, path: Path) -> SignalOutput:
        # Inline SignalChecker logic here
        # No external dependency needed
```

**Option B: Extract to common if reusable**

```python
# If signal checking might be used elsewhere
from upcast.common.signals.signal_checker import SignalChecker
```

**Decision**: Start with Option A (inline), only move to Option B if needed.

#### 4. Delete Modules Incrementally

**Decision**: Delete one module at a time, test between each deletion.

**Rationale**:

- Easier to identify what broke if something fails
- Can rollback specific module if needed
- Validates each step independently
- Lower risk approach

**Order** (simple to complex):

1. `django_model_scanner` - Simple utilities, clear dependencies
2. `django_url_scanner` - Multiple files, well-defined utilities
3. `django_settings_scanner` - More complex, multiple modes
4. `signal_scanner` - Requires refactoring, handle last

#### 5. Preserve Import Compatibility at Package Level

**Decision**: Export utilities from `upcast/common/django/__init__.py`.

**Rationale**:

- Allows simpler imports: `from upcast.common.django import parse_model`
- Maintains flexibility to reorganize internal structure
- Standard Python package pattern
- Better developer experience

**Implementation**:

```python
# upcast/common/django/__init__.py
from upcast.common.django.model_utils import is_django_model
from upcast.common.django.model_parser import merge_abstract_fields, parse_model
# ... etc

__all__ = [
    "is_django_model",
    "merge_abstract_fields",
    "parse_model",
    # ... etc
]
```

### Migration Safety Mechanisms

1. **Pre-move validation**:

   - Search entire codebase for utility usage
   - Identify all functions that need moving
   - Document dependencies between utilities

2. **Copy-test-delete approach**:

   - Copy utility to new location
   - Update imports in scanners
   - Run tests to verify it works
   - Only then delete old module

3. **Incremental commits**:

   - One commit per module deletion
   - Clear commit messages
   - Easy to revert if needed

4. **Test coverage verification**:
   - Run tests after each move
   - Check coverage doesn't drop
   - Verify scanners still work

### Testing Strategy

**After each utility move**:

1. Run specific scanner tests
2. Run full test suite
3. Check for import errors
4. Verify output format unchanged

**Test checkpoints**:

- After creating common/django/ directory
- After moving each module's utilities
- After updating each scanner's imports
- After deleting each old module
- Final validation after all deletions

**Manual testing**:

- Test each scanner with real data
- Verify CLI commands still work
- Check output matches expected format

## Detailed Implementation Plan

### Phase 2: Django Model Scanner

**Files to move**:

1. **ast_utils.py → model_utils.py**

   - Function: `is_django_model(node: ast.ClassDef) -> bool`
   - Dependencies: Standard library only (ast, typing)
   - No circular dependencies

2. **model_parser.py → model_parser.py**
   - Function: `parse_model(node: ast.ClassDef, ...) -> ModelInfo`
   - Function: `merge_abstract_fields(...)-> dict`
   - Dependencies: May import from ast_utils
   - Helper functions needed

**Import update**:

```python
# upcast/scanners/django_models.py
# OLD:
from upcast.django_model_scanner.ast_utils import is_django_model
from upcast.django_model_scanner.model_parser import merge_abstract_fields, parse_model

# NEW:
from upcast.common.django.model_utils import is_django_model
from upcast.common.django.model_parser import merge_abstract_fields, parse_model
```

**Test validation**:

- Run `uv run pytest tests/test_scanners/test_django_models.py`
- Verify model detection still works
- Check field parsing accuracy

### Phase 3: Django URL Scanner

**Files to move**:

1. **router_parser.py → router_parser.py**

   - Function: `parse_router_registrations(...)`
   - Dependencies: ast, typing
   - Helper functions for DRF router detection

2. **url_parser.py → url_parser.py**

   - Function: `parse_url_pattern(...)`
   - Dependencies: ast, re
   - Pattern matching logic

3. **view_resolver.py → view_resolver.py**
   - Function: `resolve_view(...)`
   - Dependencies: ast, pathlib
   - Import path resolution

**Import update**:

```python
# upcast/scanners/django_urls.py
# OLD:
from upcast.django_url_scanner.router_parser import parse_router_registrations
from upcast.django_url_scanner.url_parser import parse_url_pattern
from upcast.django_url_scanner.view_resolver import resolve_view

# NEW:
from upcast.common.django.router_parser import parse_router_registrations
from upcast.common.django.url_parser import parse_url_pattern
from upcast.common.django.view_resolver import resolve_view
```

**Test validation**:

- Run `uv run pytest tests/test_scanners/test_django_urls.py`
- Verify URL pattern detection
- Check view resolution works

### Phase 4: Django Settings Scanner

**Files to move**:

1. **ast_utils.py → settings_utils.py** (subset)

   - Only copy functions actually used by new scanner
   - May need: type inference, value extraction
   - Skip unused utility code

2. **definition_parser.py → settings_parser.py**
   - Function: `is_settings_module(...)`
   - Function: `parse_settings_module(...)`
   - Settings file detection logic

**Import update**:

```python
# upcast/scanners/django_settings.py
# OLD:
from upcast.django_settings_scanner.ast_utils import (
    get_setting_value,
    infer_setting_type,
    # ... other functions
)
from upcast.django_settings_scanner.definition_parser import (
    is_settings_module,
    parse_settings_module
)

# NEW:
from upcast.common.django.settings_utils import (
    get_setting_value,
    infer_setting_type,
    # ... other functions
)
from upcast.common.django.settings_parser import (
    is_settings_module,
    parse_settings_module
)
```

**Test validation**:

- Run `uv run pytest tests/test_scanners/test_django_settings.py`
- Verify settings detection
- Check value parsing accuracy

### Phase 5: Signal Scanner

**Refactoring approach**:

**Analyze SignalChecker**:

```python
# signal_scanner/checker.py
class SignalChecker:
    def __init__(self, root_path: str, verbose: bool = False):
        self.root_path = root_path
        self.verbose = verbose
        self.signals: list = []

    def check_file(self, file_path: str) -> None:
        # Parse file and detect signals
        # Append to self.signals
```

**Inline into SignalScanner**:

```python
# upcast/scanners/signals.py
class SignalScanner(BaseScanner[SignalOutput]):
    def scan(self, path: Path) -> SignalOutput:
        signals = []
        files = self.get_files_to_scan(path)

        for file_path in files:
            # Inline signal detection logic here
            file_signals = self._check_file_for_signals(file_path)
            signals.extend(file_signals)

        # Build output...

    def _check_file_for_signals(self, file_path: Path) -> list[SignalInfo]:
        # Logic from SignalChecker.check_file()
```

**Alternative if too complex**:
Move SignalChecker to `upcast/common/signals/` and import from there.

**Test validation**:

- Run `uv run pytest tests/test_scanners/test_signal.py`
- Verify signal detection works
- Test Django and Celery signals

## Alternative Approaches Considered

### Alternative 1: Keep Old Modules as Library

**Approach**: Rename old modules to `*_utils`, keep as utility libraries.

**Rejected because**:

- Still maintains duplicate code structure
- Confusing naming convention
- Doesn't complete migration
- Adds to maintenance burden

### Alternative 2: Inline All Utilities into Scanners

**Approach**: Copy utility code directly into each scanner file.

**Rejected because**:

- Violates DRY principle
- Makes scanner files too large
- Harder to test utilities independently
- Future reuse becomes impossible

### Alternative 3: Create Separate Utility Packages

**Approach**: Create `upcast-django-utils` as separate package.

**Rejected because**:

- Over-engineering for current needs
- Adds dependency management complexity
- Not needed unless utilities are reused externally
- Can always extract later if needed

### Alternative 4: Leave utilities in old location

**Approach**: Don't move utilities, just import from old modules.

**Rejected because**:

- Maintains technical debt
- Confusing for developers
- Old module structure remains
- Doesn't achieve cleanup goal

## Risk Assessment

### Low Risk Items

- Moving model utilities (simple, well-tested)
- Moving URL parser utilities (clear dependencies)
- Creating common directory structure

### Medium Risk Items

- Moving settings utilities (complex type inference)
- Updating all scanner imports simultaneously
- Ensuring no missed imports

### High Risk Items

- Refactoring SignalScanner (logic changes required)
- Verifying no hidden dependencies exist
- Maintaining test coverage during transition

### Mitigation Strategies

**For high-risk items**:

- Handle SignalScanner last (most time to test)
- Extensive grep searches for imports before deletion
- Run coverage report to verify tests still cover code

**For medium-risk items**:

- Update imports immediately after moving utilities
- Test scanner individually before moving to next
- Keep git history clean for easy rollback

**For low-risk items**:

- Proceed with confidence
- Standard copy-test-delete approach
- Quick validation sufficient

## Success Metrics

1. **Code reduction**: Remove ~25 files from old modules
2. **Import cleanliness**: Zero imports from old modules
3. **Test success**: 100% test pass rate maintained
4. **Coverage maintenance**: Keep ≥80% code coverage
5. **No functionality loss**: All scanners work identically
6. **Clean structure**: Well-organized common utilities

## Dependencies

- **Requires**: `migrate-main-to-new-scanners` Phase 1-2 complete ✅
- **Blocks**: Documentation updates
- **Enables**: Complete migration cleanup
