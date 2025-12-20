# Design: Cyclomatic Complexity Scanner

## Overview

This document details the technical design for the cyclomatic complexity scanner, which analyzes Python code to identify functions with high complexity that may need refactoring.

## Architecture

### Component Structure

```
upcast/cyclomatic_complexity_scanner/
├── __init__.py
├── checker.py           # Main orchestration
├── complexity_parser.py # AST analysis and complexity calculation
├── cli.py              # Command-line interface
└── export.py           # Output formatting
```

### Data Flow

```
1. CLI Entry
   ↓
2. File Collection (common utilities)
   ↓
3. For each file:
   - Parse AST
   - Visit function/method nodes
   - Calculate complexity
   - Filter by threshold
   ↓
4. Aggregate Results
   - Group by module
   - Calculate statistics
   ↓
5. Export (YAML/JSON)
```

## Core Algorithm: Complexity Calculation

### Decision Point Counting

Cyclomatic complexity M = E - N + 2P where:

- E = number of edges in control flow graph
- N = number of nodes
- P = number of connected components (always 1 for a function)

**Simplified counting approach:**
M = 1 + number of decision points

### Decision Points

| Construct                        | Count          | Example                       |
| -------------------------------- | -------------- | ----------------------------- |
| `if` statement                   | +1             | `if condition:`               |
| `elif` clause                    | +1             | `elif other:`                 |
| `for` loop                       | +1             | `for x in items:`             |
| `while` loop                     | +1             | `while running:`              |
| `except` handler                 | +1 per handler | `except ValueError:`          |
| `and` operator                   | +1             | `if a and b:`                 |
| `or` operator                    | +1             | `if a or b:`                  |
| List comprehension with if       | +1             | `[x for x in items if x > 0]` |
| Ternary expression               | +1             | `a if condition else b`       |
| Boolean operators in assignments | +1 per op      | `x = a and b or c`            |

**Note:** `else` without additional conditions does not add complexity (it's the alternative path of the preceding `if`).

### Code Extraction and Comment Counting

**Extract Function Source (using astroid):**

```python
def extract_function_code(node: nodes.FunctionDef) -> str:
    """Extract complete function source code using astroid.

    Args:
        node: Astroid FunctionDef node

    Returns:
        Complete function source code including decorators
    """
    return node.as_string()
```

**Count Comment Lines (using tokenize module):**

```python
import tokenize
import io

def count_comment_lines(source_code: str) -> int:
    """Count comment lines using Python's tokenize module.

    This is more accurate than string matching as it properly handles:
    - Comments inside strings
    - Multi-line strings vs actual comments
    - Different comment styles

    Args:
        source_code: Function source code

    Returns:
        Number of comment lines (lines with # comments)
    """
    comment_count = 0
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source_code).readline)
        comment_lines = set()

        for token in tokens:
            if token.type == tokenize.COMMENT:
                comment_lines.add(token.start[0])

        comment_count = len(comment_lines)
    except tokenize.TokenError:
        # Fallback to 0 if tokenization fails
        pass

    return comment_count
```

**Note:** These utilities will be abstracted to `upcast/common/code_utils.py` for reuse across scanners.

### Implementation Using AST Visitor

```python
class ComplexityVisitor(ast.NodeVisitor):
    """Calculate cyclomatic complexity by counting decision points."""

    def __init__(self):
        self.complexity = 1  # Base complexity

    def visit_If(self, node):
        # Count if + elif branches
        self.complexity += 1
        # Count boolean operators in condition
        self.complexity += count_bool_ops(node.test)
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        # Count if clause in comprehension handled elsewhere
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.complexity += count_bool_ops(node.test)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)

    # ... other visit methods
```

### Handling Edge Cases

1. **Nested Functions/Lambdas:**

   - Calculate separately
   - Don't add to parent's complexity
   - Report independently if they exceed threshold

2. **Class Methods:**

   - Treat same as standalone functions
   - Include in module's function list

3. **Property Decorators:**

   - Treat as regular methods
   - Include `@property`, `@setter`, `@classmethod`, `@staticmethod`

4. **Async Functions:**

   - Same rules apply
   - `async for`, `async with` count as decision points

5. **Generator Expressions:**
   - `if` clauses count as +1
   - Nested comprehensions count individually

## Data Models

### ComplexityResult

```python
@dataclass
class ComplexityResult:
    """Result for a single function/method."""
    name: str                    # Function name
    module: str                  # Module path
    line: int                    # Starting line number
    end_line: int               # Ending line number
    complexity: int             # Calculated complexity
    severity: str               # warning/high_risk/critical
    description: str | None     # Docstring first line
    signature: str              # Function signature
    is_async: bool             # Whether it's async def
    is_method: bool            # Whether it's a class method
    class_name: str | None     # Parent class if method
```

### Severity Levels

```python
def get_severity(complexity: int) -> str:
    """Determine severity level based on complexity."""
    if complexity <= 5:
        return "healthy"
    elif complexity <= 10:
        return "acceptable"
    elif complexity <= 15:
        return "warning"
    elif complexity <= 20:
        return "high_risk"
    else:
        return "critical"
```

## File Filtering

### Default Exclusions

When `use_default_excludes=True` (default):

```python
DEFAULT_TEST_PATTERNS = [
    "**/test_*.py",
    "**/tests/**",
    "**/*_test.py",
    "test_*.py",
    "tests/**",
]
```

### Custom Filtering

Users can override with:

- `--include "pattern"`: Only scan matching files
- `--exclude "pattern"`: Skip matching files
- `--include-tests`: Disable test exclusion
- `--no-default-excludes`: Scan everything

## Output Format

### YAML Structure

```yaml
summary:
  total_functions_scanned: 1250
  high_complexity_count: 23
  by_severity:
    warning: 15 # 11-15
    high_risk: 6 # 16-20
    critical: 2 # >20
  files_analyzed: 87

modules:
  app/services/user_service.py:
    - name: process_registration
      line: 45
      end_line: 98
      complexity: 16
      severity: high_risk
      description: "Process user registration with validation"
      signature: "def process_registration(user_data: dict, options: dict = None)"
      is_async: false
      is_method: false
      class_name: null

  app/utils/parser.py:
    - name: parse_input
      line: 120
      end_line: 187
      complexity: 23
      severity: critical
      description: "Parse complex nested input structure"
      signature: "def parse_input(data, schema=None, strict=True)"
      is_async: false
      is_method: false
      class_name: null
```

### Summary Statistics

Calculate and include:

- Total functions analyzed
- Number exceeding threshold
- Breakdown by severity
- Files with high complexity
- Average complexity across codebase

## Performance Optimization

### Strategies

1. **Lazy Evaluation:**

   - Only calculate complexity for functions, not entire module
   - Skip files with no function definitions early

2. **Parallel Processing:**

   - Process files independently
   - Can use multiprocessing for large codebases (future enhancement)

3. **Caching:**

   - Consider caching results for unchanged files (future enhancement)
   - Would require file hash tracking

4. **Memory Management:**
   - Stream results rather than holding all in memory
   - Process and discard ASTs after analysis

### Expected Performance

Based on other Upcast scanners:

- Parsing: ~1000 files/second
- Complexity calculation: Negligible overhead (~10% of parse time)
- Output formatting: Constant time per result

For 5000-file codebase:

- Scan time: ~5-7 seconds
- Memory: ~100-200MB peak

## Error Handling

### Syntax Errors

```python
try:
    tree = ast.parse(source_code)
except SyntaxError as e:
    logger.warning(f"Syntax error in {file_path}:{e.lineno}: {e.msg}")
    continue  # Skip file
```

### Encoding Issues

Use robust file reading:

```python
def read_file_safe(path: Path) -> str:
    """Read file with encoding fallback."""
    for encoding in ['utf-8', 'latin-1', 'cp1252']:
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Cannot decode {path}")
```

### Missing Docstrings

Handle gracefully:

```python
description = ast.get_docstring(node) or None
```

## Testing Strategy

### Unit Tests

1. **Complexity Calculation:**

   - Test each decision point type
   - Test nested structures
   - Test edge cases (empty functions, single-line functions)
   - Verify count accuracy against known examples

2. **Filtering:**

   - Test threshold filtering
   - Test test file exclusion
   - Test include/exclude patterns

3. **Output Formatting:**
   - Verify YAML structure
   - Verify JSON structure
   - Test empty results
   - Test large result sets

### Integration Tests

1. **Real Code Analysis:**

   - Scan Upcast's own codebase
   - Compare with manual complexity counts
   - Validate against `radon cc` for accuracy

2. **End-to-End CLI:**
   - Test all CLI options
   - Test error handling
   - Test output file writing

### Test Fixtures

Create test files with known complexity:

```python
# tests/fixtures/complexity_samples.py

def simple_function():  # Complexity: 1
    return True

def with_if(x):  # Complexity: 2
    if x > 0:
        return True
    return False

def complex_function(data, options=None):  # Complexity: 15
    if not data:
        return None

    result = []
    for item in data:
        if item.valid and (item.type == 'A' or item.type == 'B'):
            if options and options.get('strict'):
                try:
                    value = process(item)
                except ValueError:
                    value = default
                except TypeError:
                    value = None
            else:
                value = item.value

            if value is not None:
                result.append(value)

    return result if result else None
```

## Implementation Phases

### Phase 1: Core Functionality (MVP)

- [ ] Basic complexity calculation
- [ ] AST visitor implementation
- [ ] Threshold filtering
- [ ] Module-organized output
- [ ] Basic CLI command

### Phase 2: Robustness

- [ ] Test file exclusion
- [ ] Include/exclude patterns
- [ ] Error handling
- [ ] YAML/JSON export

### Phase 3: Polish

- [ ] Summary statistics
- [ ] Severity categorization
- [ ] Documentation
- [ ] Integration tests

### Phase 4: Future Enhancements (Optional)

- [ ] Parallel file processing
- [ ] Caching for incremental scans
- [ ] Trend tracking over time
- [ ] Integration with code review tools
