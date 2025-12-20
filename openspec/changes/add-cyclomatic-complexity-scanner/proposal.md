# Proposal: Add Cyclomatic Complexity Scanner

## What Changes

Add a new cyclomatic complexity scanner that analyzes Python functions and methods to identify code with high complexity that may need refactoring.

**Capabilities:**

- Scan all Python files (excluding test files)
- Calculate cyclomatic complexity for each function/method
- Filter functions exceeding configurable threshold (default: 11)
- Output results organized by module path
- Provide complexity assessment with severity levels

**Output Structure:**

```yaml
summary:
  total_functions: 150
  high_complexity_count: 12
  by_severity:
    warning: 8 # 11-15
    high_risk: 3 # 16-20
    critical: 1 # >20

modules:
  app/services/user.py:
    - name: process_user_registration
      line: 45
      end_line: 78
      complexity: 16
      severity: high_risk
      description: "Handle user registration with validation and email"
      signature: "def process_user_registration(user_data: dict, strict: bool = True) -> Result:"
      comment_lines: 8
      code_lines: 34
      code: |
        def process_user_registration(user_data: dict, strict: bool = True) -> Result:
            """Handle user registration with validation and email."""
            if not user_data:
                raise ValueError("User data required")

            # Validate email format
            if "email" not in user_data:
                return Result.error("Email required")
            ...
  app/utils/parser.py:
    - name: parse_complex_input
      line: 89
      end_line: 135
      complexity: 23
      severity: critical
      description: "Parse and validate complex nested input"
      signature: "def parse_complex_input(data, options=None, strict=False):"
      comment_lines: 12
      code_lines: 47
      code: |
        def parse_complex_input(data, options=None, strict=False):
            """Parse and validate complex nested input."""
            if not data:
                return None

            # Multiple nested conditions and loops
            if isinstance(data, dict):
                for key, value in data.items():
                    if key.startswith('_'):
                        continue
            ...
```

## Why

**Problem:**
High cyclomatic complexity is a strong indicator of code that is:

- Hard to understand and maintain
- Prone to bugs
- Difficult to test thoroughly
- Costly to modify

Currently, developers must manually identify complex functions or rely on external tools that aren't integrated into the Upcast analysis workflow.

**Benefits:**

1. **Proactive Quality Control**: Identify maintenance hotspots before they cause problems
2. **Refactoring Prioritization**: Data-driven decisions on what to refactor first
3. **Code Review Support**: Automated complexity checks in CI/CD pipelines
4. **Technical Debt Tracking**: Measure complexity trends over time
5. **Consistent with Existing Scanners**: Follows established Upcast patterns

**Complexity Guidelines:**

- ≤ 5: Very healthy, minimal attention needed
- 6-10: Acceptable, monitor readability
- 11-15: Warning zone, refactoring recommended
- 16-20: High risk, significant maintenance cost
- \> 20: Critical, design issues likely

## How

### Architecture

Follow the established scanner pattern used by other Upcast scanners:

1. **Parser Module** (`complexity_parser.py`):

   - Use AST visitor pattern to traverse function/method definitions
   - Calculate cyclomatic complexity using decision point counting
   - Extract function metadata (name, line, docstring, signature)

2. **Checker Module** (`checker.py`):

   - Orchestrate file scanning
   - Apply threshold filtering
   - Aggregate results by module
   - Use common utilities for source code extraction
   - Use tokenize-based comment counting for accuracy

3. **CLI Module** (`cli.py`):

   - Provide `scan-complexity` command
   - Support standard filtering options (include/exclude patterns)
   - Accept configurable threshold parameter
   - Integrate with Upcast main CLI

4. **Export Module** (`export.py`):
   - Format results in YAML/JSON
   - Include severity categorization
   - Provide summary statistics

### Cyclomatic Complexity Calculation

Count decision points in control flow:

- `if` statements: +1
- `elif` clauses: +1 each
- `else` with nested conditions: +1
- `for` loops: +1
- `while` loops: +1
- `except` handlers: +1 each
- Boolean operators in conditions: +1 per `and`/`or`
- Comprehensions with conditions: +1
- Ternary expressions: +1

Base complexity: 1 (single entry point)

### Test Exclusion Strategy

Exclude files matching these patterns:

- `tests/**`
- `test_*.py`
- `*_test.py`
- `**/test_*.py`
- `**/tests/**`

Allow override with `--include-tests` flag.

### Integration Points

1. **Main CLI**: Add command to `upcast/main.py`
2. **Common Utilities**: Reuse `collect_python_files()` for file discovery
3. **Export Utilities**: Reuse YAML/JSON formatting helpers
4. **File Filtering**: Reuse pattern matching utilities

## Impact

### Users Affected

- All Upcast users gain new static analysis capability
- Particularly valuable for teams with large Python codebases

### Migration Required

- None (additive change only)

### Breaking Changes

- None

### Performance Considerations

- AST parsing performance: ~1000 files/second (similar to other scanners)
- Negligible memory overhead (streaming file processing)
- Suitable for CI/CD pipelines

## Alternatives Considered

### Alternative 1: Use External Tool (radon, mccabe)

**Pros:**

- Mature, well-tested libraries
- Widely used in Python ecosystem

**Cons:**

- Additional dependency
- Different output format (requires adapter)
- Less control over implementation
- Inconsistent with Upcast's self-contained approach

**Decision:** Implement internally for consistency and control

### Alternative 2: Include All Functions (No Threshold)

**Pros:**

- Complete visibility

**Cons:**

- Overwhelming output for large codebases
- Most functions (typically 80%+) have low complexity
- Harder to focus on actionable items

**Decision:** Default threshold of 11, configurable

### Alternative 3: Only Warn, Don't Output Details

**Pros:**

- Simpler implementation

**Cons:**

- Less actionable (no context for refactoring)
- Doesn't fit Upcast's detailed analysis model

**Decision:** Provide full details (name, location, docstring, code snippet)

## Open Questions

None. The implementation follows well-established patterns from existing scanners.

## Success Criteria

1. **Functional Requirements:**

   - [ ] Correctly calculate cyclomatic complexity for all Python function types
   - [ ] Filter based on configurable threshold
   - [ ] Exclude test files by default
   - [ ] Output in YAML and JSON formats
   - [ ] Organize results by module path

2. **Quality Requirements:**

   - [ ] Unit test coverage ≥ 90%
   - [ ] Integration tests with real-world code samples
   - [ ] Documentation with usage examples
   - [ ] Follows Upcast scanner patterns

3. **Performance Requirements:**

   - [ ] Scan 1000+ file projects in < 10 seconds
   - [ ] Memory usage scales linearly with file count

4. **Validation:**
   - [ ] Compare results with `radon cc` on sample projects (accuracy check)
   - [ ] Test on Upcast's own codebase
   - [ ] Verify test file exclusion works correctly
