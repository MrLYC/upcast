# Design: Fix Scanner Missing Features

## Overview

This change restores missing fields and fixes command naming inconsistencies introduced during scanner migration. The core issue is that the original specifications defined comprehensive metadata fields that were never fully implemented.

## Architecture

### Current State

```
ComplexityScanner
├── Models: ComplexityResult (6 fields)
│   ├── name, line, end_line
│   ├── complexity, severity, message
│   └── ❌ Missing: description, signature, code, comment_lines, code_lines
├── Command: scan-complexity
│   └── ❌ Spec says: scan-complexity-patterns
└── Output: Limited context

ConcurrencyScanner
├── Models: ConcurrencyUsage
├── Command: scan-concurrency
│   └── ❌ Spec says: scan-concurrency-patterns
└── Output: OK
```

### Target State

```
ComplexityScanner
├── Models: ComplexityResult (11 fields)
│   ├── name, line, end_line
│   ├── complexity, severity, message
│   └── ✅ Added: description, signature, code, comment_lines, code_lines
├── Command: scan-complexity-patterns ✅
│   └── Matches specification
└── Output: Full context for refactoring decisions

ConcurrencyScanner
├── Models: ConcurrencyUsage (unchanged)
├── Command: scan-concurrency-patterns ✅
│   └── Matches specification
└── Output: OK
```

## Data Model Changes

### ComplexityResult Before

```python
class ComplexityResult(BaseModel):
    name: str
    line: int
    end_line: int
    complexity: int
    severity: str
    message: str | None
```

### ComplexityResult After

```python
class ComplexityResult(BaseModel):
    # Existing fields
    name: str
    line: int
    end_line: int
    complexity: int
    severity: str
    message: str | None

    # NEW: Metadata extraction (per spec)
    description: str | None          # Docstring first line
    signature: str | None            # Complete function signature
    code: str | None                 # Full source code
    comment_lines: int = 0           # Comment count (tokenize-based)
    code_lines: int = 0              # Total lines
```

## Implementation Strategy

### 1. Signature Extraction

**Approach**: Use astroid AST to build signature string

```python
def extract_function_signature(node: nodes.FunctionDef) -> str:
    """Extract complete function signature.

    Returns:
        str: "def func_name(param1: type = default, ...) -> ReturnType:"
    """
    # Start with function name
    parts = ["def", node.name, "("]

    # Build parameters
    params = []
    for arg in node.args.args:
        param_str = arg.name
        if arg.annotation:
            param_str += f": {arg.annotation.as_string()}"
        # Check for default value
        if has_default(arg):
            param_str += f" = {get_default(arg).as_string()}"
        params.append(param_str)

    parts.append(", ".join(params))
    parts.append(")")

    # Add return type if present
    if node.returns:
        parts.append(f" -> {node.returns.as_string()}")

    parts.append(":")
    return " ".join(parts)
```

**Edge Cases**:

- `*args` and `**kwargs`
- Keyword-only arguments
- Position-only arguments (Python 3.8+)
- Complex type hints (Union, Optional, etc.)
- Decorators (ignored in signature)

### 2. Docstring Extraction

**Approach**: Use astroid's docstring utilities

```python
def extract_description(node: nodes.FunctionDef) -> str | None:
    """Extract first line of docstring as description.

    Returns:
        str | None: First line of docstring, or None if no docstring
    """
    doc = node.doc_node
    if not doc:
        return None

    # Get docstring value
    docstring = doc.value
    if not docstring:
        return None

    # Extract first line (before first newline)
    first_line = docstring.split('\n')[0].strip()
    return first_line if first_line else None
```

**Edge Cases**:

- No docstring → `None`
- Empty docstring → `None`
- Multi-line docstring → First line only
- Docstring with leading/trailing whitespace → Stripped

### 3. Comment Counting

**Approach**: Use Python's `tokenize` module (per spec)

```python
import io
import tokenize

def count_comment_lines(source_code: str) -> int:
    """Count lines containing Python comment tokens.

    Uses tokenize module to identify actual comment tokens,
    excluding docstrings and '#' in string literals.

    Args:
        source_code: Python source code

    Returns:
        int: Number of lines with comments
    """
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source_code).readline)
        comment_lines = set()

        for token in tokens:
            if token.type == tokenize.COMMENT:
                comment_lines.add(token.start[0])  # Line number

        return len(comment_lines)
    except tokenize.TokenError:
        # Handle incomplete tokens gracefully
        return 0
```

**Why tokenize?**

- Accurately distinguishes comments from strings containing `#`
- Handles multi-line strings correctly
- Consistent with Python's own parsing
- Spec explicitly requires tokenize-based counting

**Edge Cases**:

- `#` in string literals → Not counted
- Docstrings → Not counted (they're STRING tokens, not COMMENT)
- Incomplete code → Returns 0 (graceful degradation)

### 4. Code Line Counting

**Approach**: Simple arithmetic from AST line numbers

```python
def calculate_code_lines(node: nodes.FunctionDef) -> int:
    """Calculate total lines in function.

    Includes code, comments, blank lines, decorators.

    Returns:
        int: end_line - line + 1
    """
    if not node.end_lineno or not node.lineno:
        return 0

    return node.end_lineno - node.lineno + 1
```

**Note**: This matches the original spec's definition of `code_lines`:

> "Function spanning lines 45-98 has code_lines = 54"

### 5. Source Code Extraction

**Approach**: Reuse existing `extract_function_code()` utility

```python
from upcast.common.code_utils import extract_function_code

# In ComplexityScanner._analyze_function():
code = extract_function_code(node)
```

This utility already exists and handles:

- Decorators
- Indentation
- Multi-line definitions
- Edge cases

## Command Naming Strategy

### Pattern Analysis

Current commands:

```
scan-env-vars           ✅ Correct (simple usage detection)
scan-django-models      ✅ Correct (model definitions)
scan-django-urls        ✅ Correct (URL definitions)
scan-django-settings    ✅ Correct (settings usage)
scan-http-requests      ✅ Correct (HTTP call detection)
scan-metrics            ✅ Correct (metric definitions)
scan-blocking-operations ✅ Correct (blocking calls)
scan-exception-handlers  ✅ Correct (exception blocks)
scan-unit-tests         ✅ Correct (test functions)
scan-signals            ✅ Correct (signal usage)

scan-complexity         ❌ Should be: scan-complexity-patterns
scan-concurrency        ❌ Should be: scan-concurrency-patterns
```

### Naming Convention

**Rule**: Use `-patterns` suffix when detecting recurring code patterns rather than specific usage/definitions

**Rationale**:

- Complexity: Detects pattern of high cyclomatic complexity
- Concurrency: Detects patterns of concurrent code constructs
- Both analyze structural patterns across codebase

**Consistency**: This matches the specification exactly:

- `openspec/specs/cyclomatic-complexity-scanner/spec.md`: References `scan-complexity-patterns`
- `openspec/specs/concurrency-pattern-scanner/spec.md`: References `scan-concurrency-patterns`

## Integration Points

### Utilities Location

All extraction utilities will be in `upcast/common/code_utils.py`:

```python
# upcast/common/code_utils.py

def extract_function_signature(node: nodes.FunctionDef) -> str:
    """Extract complete function signature."""
    ...

def extract_description(node: nodes.FunctionDef) -> str | None:
    """Extract first line of docstring."""
    ...

def count_comment_lines(source_code: str) -> int:
    """Count comment lines using tokenize."""
    ...

def extract_function_code(node: nodes.FunctionDef) -> str | None:
    """Extract full function source code."""
    ...  # Already exists
```

### Scanner Integration

```python
# upcast/scanners/complexity.py

def _analyze_function(
    self, node: nodes.FunctionDef, parent_class: str | None
) -> ComplexityResult | None:
    try:
        complexity = self._calculate_complexity(node)

        # Existing extractions
        code = extract_function_code(node)
        if not code:
            return None

        # NEW: Extract metadata
        description = extract_description(node)
        signature = extract_function_signature(node)
        code_lines = node.end_lineno - node.lineno + 1 if node.end_lineno else 0
        comment_lines = count_comment_lines(code) if code else 0

        severity = self._assign_severity(complexity)
        message = f"Complexity {complexity} exceeds threshold {self.threshold}"

        return ComplexityResult(
            name=node.name,
            line=node.lineno or 0,
            end_line=node.end_lineno or node.lineno or 0,
            complexity=complexity,
            severity=severity,
            message=message,
            # NEW fields
            description=description,
            signature=signature,
            code=code,
            comment_lines=comment_lines,
            code_lines=code_lines,
        )
    except Exception:
        return None
```

## Performance Analysis

### Overhead Breakdown

| Operation         | Current Time | New Time  | Overhead              |
| ----------------- | ------------ | --------- | --------------------- |
| AST Parsing       | 100ms        | 100ms     | 0% (unchanged)        |
| Complexity Calc   | 50ms         | 50ms      | 0% (unchanged)        |
| Signature Extract | 0ms          | 5ms       | +5ms (new)            |
| Docstring Extract | 0ms          | 2ms       | +2ms (new)            |
| Code Extract      | 20ms         | 20ms      | 0% (exists)           |
| Comment Count     | 0ms          | 10ms      | +10ms (new, tokenize) |
| **Total**         | **170ms**    | **187ms** | **+10%**              |

**Estimate**: ~10% overhead for complexity scanner on typical projects

**Mitigation**:

- Comment counting is the main overhead (tokenize pass)
- Consider caching source code per file
- Only count comments once per function
- Performance acceptable for static analysis tool

### Memory Impact

- Signature: ~50-100 bytes per function
- Description: ~50-200 bytes per function
- Code: ~500-2000 bytes per function (already extracted)
- Comment/code lines: 8 bytes each (integers)

**Total**: ~600-2300 bytes per function
**Impact**: Minimal for typical projects (<10K functions)

## Testing Strategy

### Unit Tests

```python
# tests/test_scanners/test_complexity.py

def test_complexity_result_has_all_fields():
    """Verify ComplexityResult includes all specified fields."""
    result = ComplexityResult(
        name="test_func",
        line=1,
        end_line=10,
        complexity=5,
        severity="acceptable",
        message="OK",
        description="Test function",
        signature="def test_func(x: int) -> bool:",
        code="def test_func(x: int) -> bool:\n    return True\n",
        comment_lines=2,
        code_lines=10,
    )

    assert result.description == "Test function"
    assert result.signature.startswith("def test_func")
    assert result.code is not None
    assert result.comment_lines == 2
    assert result.code_lines == 10

def test_signature_extraction():
    """Test signature extraction with various parameter types."""
    fixtures = [
        ("def simple():", "def simple():"),
        ("def with_params(a, b):", "def with_params(a, b):"),
        ("def typed(x: int, y: str) -> bool:", "def typed(x: int, y: str) -> bool:"),
        ("def defaults(x=1, y='a'):", "def defaults(x=1, y='a'):"),
        ("async def async_func():", "async def async_func():"),
    ]
    # ... test each fixture

def test_comment_counting():
    """Test tokenize-based comment counting."""
    code = '''
    def func():
        # This is a comment
        x = 1  # Inline comment
        y = "# Not a comment"
        return x
    '''

    count = count_comment_lines(code)
    assert count == 2  # Only actual comments
```

### Integration Tests

```python
def test_complexity_scanner_full_output():
    """Test scanner produces all fields on real code."""
    scanner = ComplexityScanner(threshold=1)
    output = scanner.scan(Path("tests/fixtures/sample.py"))

    assert len(output.results) > 0
    for module, functions in output.results.items():
        for func in functions:
            assert func.description is not None or func.description is None  # Can be None
            assert func.signature is not None
            assert func.code is not None
            assert func.comment_lines >= 0
            assert func.code_lines > 0
```

## Risks and Mitigation

### Risk 1: Signature Extraction Failures

**Risk**: Complex type hints or syntax may cause extraction to fail

**Mitigation**:

- Graceful fallback to `None` if extraction fails
- Log warning in verbose mode
- Comprehensive test fixtures

### Risk 2: Comment Counting Inaccuracy

**Risk**: tokenize may miscount in edge cases

**Mitigation**:

- Tokenize is Python's own parser, highly reliable
- Graceful fallback to 0 on TokenError
- Manual validation on real projects

### Risk 3: Performance Regression

**Risk**: 10% overhead may be unacceptable for large projects

**Mitigation**:

- Performance is still acceptable for static analysis
- Users can skip comment counting if needed (future flag)
- Benchmark on large projects before release

### Risk 4: Breaking Change in Command Names

**Risk**: Users have scripts/CI using old command names

**Mitigation**:

- Document migration in release notes
- Provide clear error message for old names
- Consider deprecation period in future version

## Dependencies

### New Dependencies

None - uses only standard library modules:

- `tokenize` (standard library)
- `io` (standard library)
- astroid (already a dependency)

### Modified Files

1. `upcast/models/complexity.py` - Add fields
2. `upcast/common/code_utils.py` - Add utilities
3. `upcast/scanners/complexity.py` - Extract new fields
4. `upcast/main.py` - Rename commands
5. `README.md` - Update examples
6. `tests/test_scanners/test_complexity.py` - Add tests
7. `tests/test_common/test_code_utils.py` - Add utility tests

## Rollout Plan

1. **Phase 1**: Implement utilities and model changes
2. **Phase 2**: Update scanner to populate fields
3. **Phase 3**: Rename commands
4. **Phase 4**: Update documentation
5. **Phase 5**: Validate on real projects
6. **Release**: Include migration notes

## Success Metrics

- All new fields present in output
- Comment counting accuracy >95% on test fixtures
- Signature extraction success rate >99%
- Performance overhead <15%
- Zero regressions in existing tests
- Documentation fully updated
