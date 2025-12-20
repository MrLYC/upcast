# Implementation Tasks - Cyclomatic Complexity Scanner

## Phase 1: Core Functionality

### Task 1.1: Implement Complexity Parser

- [x] Create `upcast/cyclomatic_complexity_scanner/complexity_parser.py`
- [x] Implement `ComplexityVisitor(ast.NodeVisitor)`:
  - [x] Track base complexity = 1
  - [x] Visit `If` nodes: +1 for if, +1 per elif
  - [x] Visit `For` and `While` nodes: +1 each
  - [x] Visit `ExceptHandler` nodes: +1 per handler
  - [x] Visit `BoolOp` nodes: +1 per `and`/`or` operator
  - [x] Visit `IfExp` nodes (ternary): +1 each
  - [x] Visit comprehensions: +1 per `if` clause
  - [x] Visit `Assert` nodes with conditions
- [x] Implement `calculate_complexity(node: ast.FunctionDef) -> int`
- [x] Test with known complexity examples

### Task 1.2: Implement Function Detection

- [x] Extend `ComplexityVisitor` to detect functions:
  - [x] Handle `FunctionDef` and `AsyncFunctionDef`
  - [x] Track parent class for methods
  - [x] Record function name, line, end_line
  - [x] Extract signature as string
  - [x] Extract first line of docstring
  - [x] Set `is_async` and `is_method` flags
  - [x] Extract complete function source code
  - [x] Count comment lines (lines starting with `#`)
  - [x] Calculate total code lines (end_line - line + 1)
- [x] Create `ComplexityResult` dataclass:
  - [x] Fields: name, line, end_line, complexity, description, signature, is_async, is_method, class_name
  - [x] Add: code (full source), comment_lines, code_lines
- [x] Add helper functions to `upcast/common/code_utils.py`:
  - [x] `extract_function_code(node: nodes.FunctionDef) -> str` - uses `node.as_string()`
  - [x] `count_comment_lines(source_code: str) -> int` - uses `tokenize` module
  - [x] `get_code_lines(node: nodes.FunctionDef) -> int` - calculate from line range
- [x] Parse full file and return list of results

### Task 1.3: Implement Severity Assignment

- [x] Create `assign_severity(complexity: int) -> str` function:
  - [x] Return "healthy" for ≤5
  - [x] Return "acceptable" for 6-10
  - [x] Return "warning" for 11-15
  - [x] Return "high_risk" for 16-20
  - [x] Return "critical" for >20
- [x] Add `severity` field to `ComplexityResult`
- [x] Test severity boundaries

### Task 1.4: Implement Threshold Filtering

- [x] Create `filter_by_threshold(results, threshold=11)` function
- [x] Filter results where `complexity >= threshold`
- [x] Add unit tests for various thresholds

## Phase 2: File Handling and CLI

### Task 2.0: Implement Common Code Utilities

- [x] Create `upcast/common/code_utils.py` if not exists
- [x] Implement `extract_function_code(node: nodes.FunctionDef) -> str`:
  - [x] Use `node.as_string()` to get complete source
  - [x] Handle errors gracefully
- [x] Implement `count_comment_lines(source_code: str) -> int`:
  - [x] Use Python's `tokenize` module
  - [x] Count lines with COMMENT tokens
  - [x] Use set to avoid counting same line multiple times
  - [x] Handle tokenization errors
- [x] Implement `get_code_lines(node: nodes.FunctionDef) -> int`:
  - [x] Calculate `end_lineno - lineno + 1`
  - [x] Handle missing end_lineno
- [x] Add unit tests for code utilities:
  - [x] Test with simple function
  - [x] Test with comments in strings
  - [x] Test with multi-line strings
  - [x] Test with decorators

### Task 2.1: Implement Test File Exclusion

- [x] Define default test patterns:
  - [x] `tests/**`
  - [x] `**/tests/**`
  - [x] `test_*.py`
  - [x] `*_test.py`
  - [x] `**/test_*.py`
- [x] Add `get_default_exclude_patterns()` function
- [x] Add `--include-tests` flag to disable exclusions
- [x] Test pattern matching

### Task 2.2: Implement Checker Class

- [x] Create `upcast/cyclomatic_complexity_scanner/checker.py`
- [x] Implement `ComplexityChecker` class:
  - [x] `__init__(threshold, include_tests, include_patterns, exclude_patterns)`
  - [x] `check_file(file_path) -> list[ComplexityResult]`:
    - [x] Read file with encoding detection
    - [x] Parse AST
    - [x] Calculate complexity for all functions
    - [x] Filter by threshold
    - [x] Return results
  - [x] `check_files(file_paths) -> dict[str, list[ComplexityResult]]`:
    - [x] Process multiple files
    - [x] Group by module path
    - [x] Handle errors gracefully
- [x] Add error handling for syntax/encoding issues

### Task 2.3: Implement CLI

- [x] Create `upcast/cyclomatic_complexity_scanner/cli.py`
- [x] Implement `scan_complexity` Click command:
  - [x] Argument: `path` (file or directory)
  - [x] Option: `--threshold` (default 11)
  - [x] Option: `--include-tests` (flag)
  - [x] Option: `--include` (multiple patterns)
  - [x] Option: `--exclude` (multiple patterns)
  - [x] Option: `-o/--output` (file path)
  - [x] Option: `--format` (yaml/json)
  - [x] Option: `-v/--verbose` (flag)
- [x] Integrate with `collect_python_files()`
- [x] Apply file filtering
- [x] Call checker and generate results

### Task 2.4: Implement Export

- [x] Create `upcast/cyclomatic_complexity_scanner/export.py`
- [x] Implement `format_results(results, format='yaml')`:
  - [x] Calculate summary statistics:
    - [x] total_functions_scanned
    - [x] high_complexity_count
    - [x] by_severity counts
    - [x] files_analyzed
  - [x] Organize modules dict
  - [x] Sort modules and functions
  - [x] Convert to YAML or JSON
- [x] Reuse common export utilities
- [x] Handle empty results gracefully

## Phase 3: Testing and Documentation

### Task 3.1: Unit Tests

- [x] Create `tests/test_cyclomatic_complexity_scanner/`
- [x] Test `test_complexity_calculation.py`:
  - [x] Test base complexity (simple function)
  - [x] Test if/elif counting
  - [x] Test loop counting
  - [x] Test exception handler counting
  - [x] Test boolean operator counting
  - [x] Test ternary expressions
  - [x] Test comprehensions
  - [x] Test nested functions (independent)
- [x] Test `test_function_detection.py`:
  - [x] Test regular functions
  - [x] Test async functions
  - [x] Test class methods
  - [x] Test static/class methods
  - [x] Test nested functions
  - [x] Test signature extraction
  - [x] Test docstring extraction
- [x] Test `test_severity.py`:
  - [x] Test all severity levels
  - [x] Test boundary conditions
- [x] Test `test_threshold.py`:
  - [x] Test default threshold
  - [x] Test custom thresholds
  - [x] Test zero results case

### Task 3.2: Integration Tests

- [x] Test `test_file_exclusion.py`:
  - [x] Test default test exclusions
  - [x] Test --include-tests flag
  - [x] Test custom patterns
- [ ] Test `test_cli.py`:
  - [ ] Test basic scan
  - [ ] Test with options
  - [ ] Test output to file
  - [ ] Test format selection
  - [ ] Test verbose mode
- [x] Test `test_export.py`:
  - [x] Test YAML format
  - [x] Test JSON format
  - [x] Test summary statistics
  - [x] Test empty results
- [ ] Test `test_error_handling.py`:
  - [ ] Test syntax errors
  - [ ] Test encoding issues
  - [ ] Test permission errors
  - [ ] Test no files found

### Task 3.3: Fixtures

- [x] Create `tests/test_cyclomatic_complexity_scanner/fixtures/`:
  - [x] `simple.py`: Known low complexity
  - [x] `complex.py`: Known high complexity functions
  - [x] `edge_cases.py`: Nested functions, async, methods
  - [ ] `syntax_error.py`: Invalid Python
- [x] Document expected complexity values

### Task 3.4: Documentation

- [x] Update `README.md`:
  - [x] Add scanner overview
  - [x] Add usage examples
  - [x] Add complexity guidelines
  - [x] Add severity level descriptions
  - [x] Add example output
- [x] Add docstrings to all public functions
- [x] Add type hints throughout

## Phase 4: Integration and Polish

### Task 4.1: CLI Integration

- [x] Update `upcast/main.py`:
  - [x] Import `scan_complexity` command
  - [x] Register in CLI group
- [x] Verify `upcast --help` shows new command
- [x] Test end-to-end workflow

### Task 4.2: Performance Testing

- [ ] Test on large codebase (1000+ files)
- [ ] Verify < 10 second completion
- [ ] Monitor memory usage
- [ ] Optimize if needed

### Task 4.3: Code Quality

- [x] Run ruff check, ensure compliance
- [x] Run unit tests: `uv run pytest tests/test_cyclomatic_complexity_scanner/`
- [x] Run integration tests
- [x] Verify 100% pass rate (65/65 tests passed)

### Task 4.4: Final Validation

- [ ] Run `openspec validate add-cyclomatic-complexity-scanner --strict`
- [ ] Fix any specification violations
- [ ] Update tasks.md with completion status
- [ ] Archive change to openspec

## Success Criteria

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] CLI help text is clear
- [ ] Output format matches examples
- [ ] Performance targets met
- [ ] Code passes ruff check
- [ ] Documentation is complete
- [ ] OpenSpec validation passes

## Estimated Effort

- Phase 1: 4-6 hours (core algorithm)
- Phase 2: 4-6 hours (file handling, CLI)
- Phase 3: 6-8 hours (comprehensive testing)
- Phase 4: 2-3 hours (integration, polish)
- **Total: 16-23 hours**
