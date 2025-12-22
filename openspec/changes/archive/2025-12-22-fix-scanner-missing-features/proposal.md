# Proposal: Fix Scanner Missing Features

**Status**: PROPOSED

## What Changes

Restore missing fields and fix command naming for scanners that lost features during migration to the new architecture. Specifically:

1. **Complexity Scanner**: Add missing `description`, `signature`, `code`, `comment_lines`, and `code_lines` fields to `ComplexityResult` model
2. **Complexity Scanner**: Rename command from `scan-complexity` to `scan-complexity-patterns` to match specification
3. **Concurrency Scanner**: Rename command from `scan-concurrency` to `scan-concurrency-patterns` to match specification
4. **Django Model Scanner**: Add missing `description` field to `DjangoModel` model (extract from class docstring)
5. **Django Settings Scanner**: Change default `--mode` from `usage` to `both` to show both definitions and usages by default

**Affected Scanners**:

- `ComplexityScanner` (upcast/scanners/complexity.py)
- `ComplexityResult` model (upcast/models/complexity.py)
- `DjangoModelScanner` (upcast/scanners/django_models.py)
- `DjangoModel` model (upcast/models/django_models.py)
- `DjangoSettingsScanner` (upcast/scanners/django_settings.py)
- CLI command definitions (upcast/main.py)

## Why

**Problem**: During the migration to Pydantic models (change `2025-12-21-refactor-scanners-to-use-models`), several scanners lost important fields that were defined in their original specifications but never implemented:

1. **Complexity Scanner Missing Fields**:

   - Current output only shows: `name`, `line`, `end_line`, `complexity`, `severity`, `message`
   - Original spec (cyclomatic-complexity-scanner) required: `description`, `signature`, `code`, `comment_lines`, `code_lines`
   - These fields provide essential context for understanding and refactoring complex functions

2. **Django Model Scanner Missing Field**:

   - Current output lacks: `description` field
   - Original spec (django-model-scanner) requires: Extract docstring from model class as description
   - Users cannot see model purpose without opening files

3. **Django Settings Scanner Incomplete Default**:

   - Current default: `--mode usage` (only shows where settings are used)
   - Problem: Users don't see where settings are **defined** by default
   - Spec expects: Both definitions and usages for complete picture
   - Current workaround: Must explicitly use `--mode definitions` or run command twice

4. **Command Naming Inconsistency**:
   - Spec defines: `scan-complexity-patterns` (following the `-patterns` suffix convention)
   - Implementation uses: `scan-complexity` (missing the suffix)
   - Same issue for concurrency scanner

**Impact**:

- Users cannot see function signatures or docstrings without opening the file
- Missing source code in output requires manual lookup
- Cannot assess comment density (ratio of comments to code)
- Django models lack semantic context (what is this model for?)
- Settings scanner requires two runs or manual mode switching to get complete picture
- Command names don't match the published specifications
- Inconsistent naming convention across scanners

**Example of Missing Context**:

Current output:

```yaml
app/services/user.py:
  - name: process_user_registration
    line: 45
    end_line: 78
    complexity: 16
    severity: high_risk
    message: "Complexity 16 exceeds threshold 11"
```

Expected output (per spec):

```yaml
app/services/user.py:
  - name: process_user_registration
    line: 45
    end_line: 78
    complexity: 16
    severity: high_risk
    message: "Complexity 16 exceeds threshold 11"
    description: "Handle user registration with validation and email"
    signature: "def process_user_registration(user_data: dict, strict: bool = True) -> Result:"
    comment_lines: 8
    code_lines: 34
    code: |
      def process_user_registration(user_data: dict, strict: bool = True) -> Result:
          """Handle user registration with validation and email."""
          if not user_data:
              raise ValueError("User data required")
          # ... rest of implementation
```

## How

### Phase 1: Add Missing Fields to Complexity Scanner

**1.1 Update ComplexityResult Model**

Add missing fields to `upcast/models/complexity.py`:

```python
class ComplexityResult(BaseModel):
    """Complexity result for a single function."""

    name: str = Field(..., description="Function name")
    line: int = Field(..., ge=1, description="Start line number")
    end_line: int = Field(..., ge=1, description="End line number")
    complexity: int = Field(..., ge=0, description="Cyclomatic complexity score")
    severity: str = Field(..., description="Severity level")
    message: str | None = Field(None, description="Optional message")

    # NEW FIELDS (from original spec)
    description: str | None = Field(None, description="First line of docstring")
    signature: str | None = Field(None, description="Complete function signature")
    code: str | None = Field(None, description="Full function source code")
    comment_lines: int = Field(default=0, ge=0, description="Number of comment lines")
    code_lines: int = Field(default=0, ge=0, description="Total lines (code + comments + blank)")
```

**1.2 Enhance ComplexityScanner Implementation**

Update `upcast/scanners/complexity.py`:

- Extract function signature using astroid utilities
- Extract docstring first line as description
- Get full source code (already have `extract_function_code()` utility)
- Count comment lines using tokenize module
- Calculate total code lines from line range

**1.3 Leverage Existing Utilities**

Reuse code from `upcast/common/`:

- `extract_function_code(node)` - already extracts source
- `extract_function_signature(node)` - if exists, or create new utility
- `count_comment_lines(source)` - use tokenize module (as per original spec)

### Phase 2: Fix Command Naming

**2.1 Rename Commands in main.py**

Update `upcast/main.py`:

```python
# OLD: @main.command(name="scan-complexity")
# NEW: @main.command(name="scan-complexity-patterns")
def scan_complexity_patterns_cmd(...):
    """Scan Python files for high cyclomatic complexity patterns."""
    ...

# OLD: @main.command(name="scan-concurrency")
# NEW: @main.command(name="scan-concurrency-patterns")
def scan_concurrency_patterns_cmd(...):
    """Scan for concurrency patterns."""
    ...
```

**2.2 Update Documentation**

Update README.md:

- Change all `scan-complexity` examples to `scan-complexity-patterns`
- Change all `scan-concurrency` examples to `scan-concurrency-patterns`
- Update command reference table

### Phase 3: Testing and Validation

**3.1 Unit Tests**

Update `tests/test_scanners/test_complexity.py`:

- Add assertions for new fields (description, signature, code, comment_lines, code_lines)
- Test docstring extraction (with and without docstring)
- Test signature extraction (various parameter types)
- Test comment counting (tokenize-based)

**3.2 Integration Tests**

Create test fixtures with:

- Functions with docstrings
- Functions with type hints
- Functions with various complexity levels
- Functions with mixed comments and code

**3.3 Manual Validation**

Run on real projects to verify:

- All fields populate correctly
- Comment counting is accurate
- Signature extraction handles edge cases
- Output format matches specification

## Impact

### Users Affected

- All users of `scan-complexity` command (need to update to `scan-complexity-patterns`)
- All users of `scan-concurrency` command (need to update to `scan-concurrency-patterns`)
- Users will gain richer output with new fields

### Migration Required

**Breaking Change**: Command name changes

Users need to update scripts/CI pipelines:

```bash
# OLD
upcast scan-complexity /path/to/project
upcast scan-concurrency /path/to/project

# NEW
upcast scan-complexity-patterns /path/to/project
upcast scan-concurrency-patterns /path/to/project
```

**Migration Strategy**:

1. Keep old commands as aliases (deprecation warning)
2. Document name change in release notes
3. Remove aliases in next major version

### Performance Considerations

- Signature extraction: negligible overhead (AST already parsed)
- Docstring extraction: negligible (direct attribute access)
- Comment counting: ~10-20% overhead (requires tokenize pass)
- Source code extraction: already implemented, no change

Estimated total overhead: <15% for complexity scanner

## Alternatives Considered

### Alternative 1: Keep Current Implementation (Do Nothing)

**Pros**:

- No migration needed
- No performance overhead

**Cons**:

- Violates published specification
- Poor user experience (missing context)
- Inconsistent with other scanners
- Cannot accurately assess refactoring needs

**Decision**: Rejected - specification compliance is critical

### Alternative 2: Add Fields as Optional/Separate Mode

**Pros**:

- Backward compatible
- Users opt-in to overhead

**Cons**:

- Complicates CLI interface
- Default mode still violates spec
- Inconsistent with other scanners that always include metadata

**Decision**: Rejected - all metadata should always be available

### Alternative 3: Fix Fields but Keep Old Command Names

**Pros**:

- No migration needed
- Users get better output immediately

**Cons**:

- Still violates specification
- Naming inconsistency persists
- Technical debt continues

**Decision**: Rejected - both issues should be fixed together

### Alternative 4: Provide Backward Compatibility Aliases

**Pros**:

- Smooth migration path
- Users have time to update
- No immediate breaking change

**Cons**:

- Maintains technical debt temporarily
- Requires cleanup later
- Slightly more complex implementation

**Decision**: **ACCEPTED** - Best balance of spec compliance and user impact

## Open Questions

1. Should we add deprecation warnings to old command names immediately, or wait until next major version?

   - **Recommendation**: Add warnings immediately in CLI output, remove aliases in next major version

2. Should comment counting include docstrings or exclude them?

   - **Answer**: Exclude docstrings (as per original spec and tokenize behavior)

3. What should happen if source code cannot be extracted?

   - **Recommendation**: Set `code: null`, log warning if verbose mode enabled

4. Should we backfill fields for other scanners that might have similar issues?
   - **Recommendation**: No - this proposal focuses only on identified issues. Other scanners can be addressed in separate changes if needed.

## Success Criteria

1. **Functional Requirements**:

   - [x] `ComplexityResult` includes all 5 new fields
   - [x] Fields populate correctly for all function types
   - [x] Commands renamed to match specification
   - [x] Backward compatibility aliases work with deprecation warnings

2. **Quality Requirements**:

   - [x] All existing tests continue passing
   - [x] New tests cover all new fields
   - [x] Test coverage maintains ≥80%
   - [x] Ruff checks pass
   - [x] Documentation updated

3. **Validation**:

   - [x] Output matches original specification examples
   - [x] Comment counting is accurate (tokenize-based)
   - [x] Signature extraction handles type hints, defaults, etc.
   - [x] Real-world validation on wagtail or similar project

4. **Performance**:
   - [x] Overhead <20% for complexity scanner
   - [x] No regression in other scanners
