# Design: Scanner Architecture Refactoring

## Context

The upcast project has grown to include 4 different scanners (env-var, django-models, django-settings, prometheus-metrics), each implementing similar functionality independently. This has led to code duplication, inconsistent behaviors, and difficulty maintaining the codebase.

## Goals

- Reduce code duplication by extracting common functionality
- Standardize CLI interface and behavior across scanners
- Improve inference reliability with unified fallback handling
- Enable flexible file filtering for all scanners
- Maintain backward compatibility during transition

## Non-Goals

- Changing scanner detection logic (patterns stay the same)
- Rewriting scanners from scratch
- Adding new scanner types
- Changing output formats (YAML/JSON structure unchanged except sorting)

## Decisions

### 1. Common Module Structure

**Decision**: Create `upcast/common/` package with 4 modules

**Structure**:

```
upcast/common/
├── __init__.py
├── file_utils.py      # File discovery, validation, package root detection
├── ast_utils.py       # Shared astroid inference helpers
├── export.py          # Unified YAML/JSON export
└── patterns.py        # Include/exclude pattern matching
```

**Rationale**:

- Clear separation of concerns
- Easy to import specific utilities
- Allows gradual migration of scanners
- Can be tested independently

**Trade-offs**:

- Adds new module, increases project structure complexity
- Need to ensure utilities are generic enough for all scanners
- Alternative: Put in existing `upcast/__init__.py` - rejected because it mixes concerns

### 2. Inference Fallback Strategy

**Decision**: Unified fallback with explicit markers

**Rules**:

1. Try astroid inference first
2. On `InferenceError` or `Uninferable`:
   - For values: wrap in backticks `` `node.as_string()` ``
   - For types: return `"unknown"`
3. Log failed inferences in verbose mode
4. Include original expression for debugging

**Implementation**:

```python
def infer_value_with_fallback(node: nodes.NodeNG) -> tuple[Any, bool]:
    """Infer value from node with fallback.

    Returns:
        (value, success): Tuple of inferred value and success flag
    """
    try:
        inferred = next(node.infer())
        if inferred is astroid.Uninferable:
            return f"`{node.as_string()}`", False
        if isinstance(inferred, nodes.Const):
            return inferred.value, True
        return f"`{node.as_string()}`", False
    except (astroid.InferenceError, StopIteration):
        return f"`{node.as_string()}`", False
```

**Rationale**:

- Backticks visually distinguish failed inferences
- `unknown` type is unambiguous
- Preserves original expression for manual inspection
- Success flag allows logging/metrics

### 3. File Pattern Matching

**Decision**: Use glob patterns (not regex)

**CLI Options**:

```bash
--include "*.py"           # Include pattern (can be repeated)
--exclude "*/tests/*"      # Exclude pattern (can be repeated)
--exclude-defaults         # Disable default excludes
```

**Default Excludes**:

- `venv/`, `env/`, `.venv/`, `virtualenv/`
- `__pycache__/`, `*.pyc`
- `build/`, `dist/`, `.egg-info/`
- `.tox/`, `.pytest_cache/`, `.mypy_cache/`
- `node_modules/`

**Matching Logic**:

1. Check default excludes (unless disabled)
2. Check custom excludes
3. Check includes (defaults to `**/*.py`)
4. Path matching is relative to scan root

**Rationale**:

- Glob patterns are familiar (used by .gitignore, shell)
- Easier for users than regex
- Sufficient for file path matching
- Standard library `pathlib.Path.match()` support

**Alternative Considered**: Regex patterns - rejected for complexity

### 4. Package Root Detection

**Decision**: Look for `__init__.py` in parent directories

**Algorithm**:

```python
def find_package_root(start_path: Path) -> Path:
    """Find Python package root by locating __init__.py."""
    current = start_path if start_path.is_dir() else start_path.parent

    # Walk up until we find a dir WITHOUT __init__.py
    while current.parent != current:
        if not (current / "__init__.py").exists():
            # Found root - it's the first dir without __init__.py
            # or the last dir WITH __init__.py
            for child in current.iterdir():
                if child.is_dir() and (child / "__init__.py").exists():
                    return child
            return current
        current = current.parent

    return start_path  # Fallback to original path
```

**Rationale**:

- `__init__.py` is the standard Python package marker
- Walking up finds the outermost package
- Handles nested packages correctly
- Fallback prevents errors

### 5. Command Naming Migration

**Decision**: Deprecate old names with warnings, support for 2 releases

**Implementation**:

```python
@main.command(name="analyze-django-models", deprecated=True)
def analyze_django_models_deprecated(...):
    """DEPRECATED: Use 'scan-django-models' instead."""
    click.echo("Warning: 'analyze-django-models' is deprecated, use 'scan-django-models'", err=True)
    return scan_django_models(...)

@main.command(name="scan-django-models")
def scan_django_models(...):
    """Scan Django models in Python files."""
    ...
```

**Timeline**:

- Release 1: Add new commands, deprecation warnings
- Release 2: Warnings mention removal in next release
- Release 3: Remove old commands

**Rationale**:

- Gives users time to migrate
- Clear communication via warnings
- Backward compatibility maintained
- Standard deprecation practice

## Implementation Plan

### Phase 1: Common Utilities

1. Create `upcast/common/` package
2. Implement `file_utils.py` with tests
3. Implement `ast_utils.py` with unified inference functions
4. Implement `patterns.py` for file filtering
5. Implement `export.py` for YAML/JSON output

### Phase 2: Migrate Scanners

1. Update env-var scanner to use common utilities
2. Update django-models scanner (add description extraction)
3. Update django-settings scanner
4. Update prometheus-metrics scanner
5. Remove duplicated code from each scanner

### Phase 3: CLI Updates

1. Rename commands with deprecation warnings
2. Add `--include`/`--exclude` options to all commands
3. Update documentation and examples
4. Update README with migration guide

### Phase 4: Testing & Validation

1. Add integration tests for file filtering
2. Add tests for inference fallback behavior
3. Verify YAML output sorting
4. Performance testing with large codebases

## Risks & Mitigations

### Risk: Breaking Changes

**Mitigation**: Deprecation warnings, gradual migration, clear documentation

### Risk: Shared Code Complexity

**Mitigation**: Comprehensive tests, clear documentation, gradual refactoring

### Risk: Performance Regression

**Mitigation**: Benchmark tests, profiling, optimization if needed

### Risk: Scanner-Specific Edge Cases

**Mitigation**: Keep scanner-specific logic in scanner modules, only extract truly common code

## Migration Guide

### For Users

**Old Command**:

```bash
upcast analyze-django-models myproject/
```

**New Command**:

```bash
upcast scan-django-models myproject/
```

**With File Filtering**:

```bash
upcast scan-django-models myproject/ --exclude "*/migrations/*" --exclude "*/tests/*"
```

### For Developers

**Before**:

```python
from upcast.django_model_scanner.ast_utils import infer_literal_value

value = infer_literal_value(node)
```

**After**:

```python
from upcast.common.ast_utils import infer_value_with_fallback

value, success = infer_value_with_fallback(node)
if not success:
    logger.debug(f"Failed to infer: {value}")
```

## Open Decisions

1. **Should we extract `checker.py` base class?** - Scanners have different checker needs, probably not
2. **Should common utilities be in separate package?** - No, keep in upcast for simplicity
3. **How to handle scanner-specific AST utilities?** - Keep in scanner modules, only extract truly common functions
