# Design: Improve Scanner Output Quality

## Overview

This change improves output quality across five scanners by addressing specific usability issues. The modifications are focused on output formatting and filtering rather than detection logic, making them low-risk improvements.

## Architecture

### Component Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                    Scanner Commands (CLI)                    │
│  scan-concurrency  scan-django-settings  scan-exception-     │
│  scan-http-requests  scan-signals                            │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    Parser Layer (Modified)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ pattern_     │  │ settings_    │  │ handler_     │      │
│  │ parser.py    │  │ parser.py    │  │ parser.py    │      │
│  │              │  │              │  │              │      │
│  │ • Skip       │  │ • Extract    │  │ • Split      │      │
│  │   unknown    │  │   full       │  │   location   │      │
│  │   coroutine  │  │   statement  │  │   field      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │ request_     │  │ export.py    │                         │
│  │ parser.py    │  │ (signals)    │                         │
│  │              │  │              │                         │
│  │ • Merge      │  │ • Flatten    │                         │
│  │   ellipsis   │  │   structure  │                         │
│  └──────────────┘  └──────────────┘                         │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                   Export Layer (export.py)                   │
│  • YAML formatting                                           │
│  • JSON formatting                                           │
│  • Field serialization                                       │
└─────────────────────────────────────────────────────────────┘
```

## Design Decisions

### 1. Skip vs Flag Unknown Coroutines

**Decision**: Return `None` to skip entries instead of flagging with "unknown"

**Rationale**:

- Output should only include actionable detections
- "unknown" provides no value to users
- Simpler than adding filter flags/config options
- Consistent with how other scanners handle unresolvable cases

**Trade-offs**:

- **Pro**: Cleaner output, less noise
- **Pro**: No breaking changes (just fewer results)
- **Con**: Users won't know detection was attempted but failed
- **Con**: Cannot distinguish "not present" from "present but unknown"

**Alternatives Considered**:

- Add `--include-unknown` flag: Rejected - adds complexity
- Add separate "unresolved" section: Rejected - still noise
- Keep current behavior: Rejected - degrades output quality

### 2. Statement vs Expression Context

**Decision**: Extract full containing statement for django-settings code field

**Rationale**:

- Statement provides usage context (if condition, assignment, etc.)
- Expression alone (`settings.DEBUG`) lacks actionable information
- Better for understanding how setting affects behavior
- Aligns with how developers think about code

**Implementation Approach**:

```python
def _get_containing_statement(node: nodes.NodeNG) -> nodes.NodeNG:
    """Walk up AST to find containing statement."""
    current = node
    while current.parent:
        # Statement types: Assign, AugAssign, Expr, Return, If, etc.
        if isinstance(current.parent, (nodes.Assign, nodes.Expr,
                                        nodes.Return, nodes.If)):
            return current.parent
        current = current.parent
    return node  # Fallback to original node
```

**Trade-offs**:

- **Pro**: Much more useful output
- **Pro**: No breaking changes (just better data)
- **Con**: Longer output strings
- **Con**: May include unrelated code in multi-line statements

### 3. Location Field Structure

**Decision**: Replace combined string with structured fields

**Rationale**:

- Structured data (`file`, `lineno`, `end_lineno`) is easier to parse
- Simpler implementation without maintaining dual formats
- Cleaner data model

**Data Structure**:

```python
@dataclass
class ExceptionHandler:
    file: str
    lineno: int
    end_lineno: int
```

**Trade-offs**:

- **Pro**: Clean, simple data model
- **Pro**: No maintenance burden for dual formats
- **Con**: Breaking change for existing tools

### 4. Ellipsis Normalization

**Decision**: Post-process URLs to merge consecutive `...` placeholders

**Rationale**:

- Multiple `...` convey same meaning as single `...`
- Cleaner output without losing information
- Simple regex-based solution
- Low risk of false positives

**Implementation**:

```python
def _normalize_url_placeholders(url: str) -> str:
    """Merge consecutive ... placeholders."""
    # Pattern matches: ... + ... or ... + ... + ...
    # Handles optional whitespace around +
    return re.sub(r'\.\.\.(\s*\+\s*\.\.\.)+', '...', url)
```

**Edge Cases**:

- Literal `...` in URL path: Won't match (no `+` operator)
- Three dots as domain: Won't match (no repetition)
- `... + text + ...`: Correctly preserves intermediate parts

**Trade-offs**:

- **Pro**: No information loss
- **Pro**: Much cleaner output
- **Pro**: Simple implementation
- **Con**: May need adjustment if URL format changes

### 5. Signal Output Structure

**Decision**: Flatten nested structure to match other scanner patterns

**Current Structure** (Complex):

```yaml
django:
  model_signals:
    post_save:
      receivers:
        - handler: ...
  custom_signals:
    my_signal:
      receivers:
        - handler: ...
```

**New Structure** (Flat):

```yaml
signals:
  - signal: django.db.models.signals.post_save
    category: model_signals
    type: django
    receivers:
      - handler: ...

  - signal: myapp.signals.my_signal
    category: custom_signals
    type: django
    receivers:
      - handler: ...
```

**Rationale**:

- Consistent with http-request-scanner, exception-handler-scanner patterns
- Easier to iterate over in tools/scripts
- Better for grep/search operations
- More flexible for future extensions

**Trade-offs**:

- **Pro**: Consistency across scanners
- **Pro**: Easier to process programmatically
- **Pro**: Better extensibility
- **Con**: Breaking change for existing tools
- **Con**: Slightly more verbose (signal name repeated)

**Migration Support**:

- Document structure change in CHANGELOG
- Provide example migration script
- Consider adding `--legacy-format` flag for transition period

## Risk Assessment

### Low Risk Changes

1. **Concurrency scanner filtering**: Only removes noise, no logic change
2. **Settings statement context**: Additive improvement, no breaking changes

### Medium Risk Changes

3. **HTTP ellipsis merging**: Post-processing could have edge cases
   - **Mitigation**: Extensive unit tests, manual verification
   - **Rollback**: Easy - just remove normalization call

### High Risk Changes (Breaking)

4. **Exception location field**: Breaking change - field structure changed

   - **Mitigation**: Clear documentation, migration guide
   - **Rollback**: Easy - revert field definition

5. **Signal output restructuring**: Breaking change - output format changed
   - **Mitigation**: Clear documentation, migration guide, example scripts
   - **Rollback**: More difficult - requires keeping old export code

## Testing Strategy

### Unit Tests

- Test each parser modification independently
- Cover edge cases (unknown values, complex expressions, etc.)
- Verify backward compatibility (exception handler)
- Test normalization patterns (HTTP ellipsis)

### Integration Tests

- Run scanners on real codebases
- Compare old vs new output
- Verify information preservation
- Check readability improvements

### Regression Tests

- Ensure existing tests still pass (with modifications)
- No unexpected side effects in other scanners
- Performance remains acceptable

## Performance Considerations

- **Statement extraction** (Task 2): Minimal overhead (one AST walk per usage)
- **Ellipsis normalization** (Task 4): Single regex pass, negligible
- **Signal restructuring** (Task 5): Same data, different structure, no impact
- **Overall**: No measurable performance degradation expected

## Future Extensions

### Potential Improvements

1. **Unified output format**: Apply signal scanner approach to all scanners
2. **Configurable verbosity**: Let users choose context level (statement vs expression)
3. **Smart ellipsis**: Show partial URL when some parts are known
4. **Rich context**: Include surrounding code lines for better understanding

### Backward Compatibility Strategy

- Maintain old formats for 1-2 minor versions
- Add `--output-version` flag for explicit format selection
- Deprecation warnings when old formats accessed
- Clear migration documentation

## Design Decisions Confirmed

1. **Signal scanner format**: Direct breaking change, no transition flag needed
2. **Exception handler compatibility**: No backward compatibility, clean break
3. **Statement depth**: Stop at first statement (simpler)
4. **Version bump**: Minor version (output format not considered public API)
