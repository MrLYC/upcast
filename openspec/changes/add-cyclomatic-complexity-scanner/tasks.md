# Implementation Tasks - Cyclomatic Complexity Scanner

## Phase 1: Core Functionality

### Task 1.1: Implement Complexity Parser

- [ ] Create `upcast/cyclomatic_complexity_scanner/complexity_parser.py`
- [ ] Implement `ComplexityVisitor(ast.NodeVisitor)`:
  - [ ] Track base complexity = 1
  - [ ] Visit `If` nodes: +1 for if, +1 per elif
  - [ ] Visit `For` and `While` nodes: +1 each
  - [ ] Visit `ExceptHandler` nodes: +1 per handler
  - [ ] Visit `BoolOp` nodes: +1 per `and`/`or` operator
  - [ ] Visit `IfExp` nodes (ternary): +1 each
  - [ ] Visit comprehensions: +1 per `if` clause
  - [ ] Visit `Assert` nodes with conditions
- [ ] Implement `calculate_complexity(node: ast.FunctionDef) -> int`
- [ ] Test with known complexity examples

### Task 1.2: Implement Function Detection

- [ ] Extend `ComplexityVisitor` to detect functions:
  - [ ] Handle `FunctionDef` and `AsyncFunctionDef`
  - [ ] Track parent class for methods
  - [ ] Record function name, line, end_line
  - [ ] Extract signature as string
  - [ ] Extract first line of docstring
  - [ ] Set `is_async` and `is_method` flags
- [ ] Create `ComplexityResult` dataclass:
  - [ ] Fields: name, line, end_line, complexity, description, signature, is_async, is_method, class_name
- [ ] Parse full file and return list of results

### Task 1.3: Implement Severity Assignment

- [ ] Create `assign_severity(complexity: int) -> str` function:
  - [ ] Return "healthy" for ≤5
  - [ ] Return "acceptable" for 6-10
  - [ ] Return "warning" for 11-15
  - [ ] Return "high_risk" for 16-20
  - [ ] Return "critical" for >20
- [ ] Add `severity` field to `ComplexityResult`
- [ ] Test severity boundaries

### Task 1.4: Implement Threshold Filtering

- [ ] Create `filter_by_threshold(results, threshold=11)` function
- [ ] Filter results where `complexity >= threshold`
- [ ] Add unit tests for various thresholds

## Phase 2: File Handling and CLI

### Task 2.1: Implement Test File Exclusion

- [ ] Define default test patterns:
  - [ ] `tests/**`
  - [ ] `**/tests/**`
  - [ ] `test_*.py`
  - [ ] `*_test.py`
  - [ ] `**/test_*.py`
- [ ] Add `get_default_exclude_patterns()` function
- [ ] Add `--include-tests` flag to disable exclusions
- [ ] Test pattern matching

### Task 2.2: Implement Checker Class

- [ ] Create `upcast/cyclomatic_complexity_scanner/checker.py`
- [ ] Implement `ComplexityChecker` class:
  - [ ] `__init__(threshold, include_tests, include_patterns, exclude_patterns)`
  - [ ] `check_file(file_path) -> list[ComplexityResult]`:
    - [ ] Read file with encoding detection
    - [ ] Parse AST
    - [ ] Calculate complexity for all functions
    - [ ] Filter by threshold
    - [ ] Return results
  - [ ] `check_files(file_paths) -> dict[str, list[ComplexityResult]]`:
    - [ ] Process multiple files
    - [ ] Group by module path
    - [ ] Handle errors gracefully
- [ ] Add error handling for syntax/encoding issues

### Task 2.3: Implement CLI

- [ ] Create `upcast/cyclomatic_complexity_scanner/cli.py`
- [ ] Implement `scan_complexity` Click command:
  - [ ] Argument: `path` (file or directory)
  - [ ] Option: `--threshold` (default 11)
  - [ ] Option: `--include-tests` (flag)
  - [ ] Option: `--include` (multiple patterns)
  - [ ] Option: `--exclude` (multiple patterns)
  - [ ] Option: `-o/--output` (file path)
  - [ ] Option: `--format` (yaml/json)
  - [ ] Option: `-v/--verbose` (flag)
- [ ] Integrate with `collect_python_files()`
- [ ] Apply file filtering
- [ ] Call checker and generate results

### Task 2.4: Implement Export

- [ ] Create `upcast/cyclomatic_complexity_scanner/export.py`
- [ ] Implement `format_results(results, format='yaml')`:
  - [ ] Calculate summary statistics:
    - [ ] total_functions_scanned
    - [ ] high_complexity_count
    - [ ] by_severity counts
    - [ ] files_analyzed
  - [ ] Organize modules dict
  - [ ] Sort modules and functions
  - [ ] Convert to YAML or JSON
- [ ] Reuse common export utilities
- [ ] Handle empty results gracefully

## Phase 3: Testing and Documentation

### Task 3.1: Unit Tests

- [ ] Create `tests/test_cyclomatic_complexity_scanner/`
- [ ] Test `test_complexity_calculation.py`:
  - [ ] Test base complexity (simple function)
  - [ ] Test if/elif counting
  - [ ] Test loop counting
  - [ ] Test exception handler counting
  - [ ] Test boolean operator counting
  - [ ] Test ternary expressions
  - [ ] Test comprehensions
  - [ ] Test nested functions (independent)
- [ ] Test `test_function_detection.py`:
  - [ ] Test regular functions
  - [ ] Test async functions
  - [ ] Test class methods
  - [ ] Test static/class methods
  - [ ] Test nested functions
  - [ ] Test signature extraction
  - [ ] Test docstring extraction
- [ ] Test `test_severity.py`:
  - [ ] Test all severity levels
  - [ ] Test boundary conditions
- [ ] Test `test_threshold.py`:
  - [ ] Test default threshold
  - [ ] Test custom thresholds
  - [ ] Test zero results case

### Task 3.2: Integration Tests

- [ ] Test `test_file_exclusion.py`:
  - [ ] Test default test exclusions
  - [ ] Test --include-tests flag
  - [ ] Test custom patterns
- [ ] Test `test_cli.py`:
  - [ ] Test basic scan
  - [ ] Test with options
  - [ ] Test output to file
  - [ ] Test format selection
  - [ ] Test verbose mode
- [ ] Test `test_export.py`:
  - [ ] Test YAML format
  - [ ] Test JSON format
  - [ ] Test summary statistics
  - [ ] Test empty results
- [ ] Test `test_error_handling.py`:
  - [ ] Test syntax errors
  - [ ] Test encoding issues
  - [ ] Test permission errors
  - [ ] Test no files found

### Task 3.3: Fixtures

- [ ] Create `tests/test_cyclomatic_complexity_scanner/fixtures/`:
  - [ ] `simple.py`: Known low complexity
  - [ ] `complex.py`: Known high complexity functions
  - [ ] `edge_cases.py`: Nested functions, async, methods
  - [ ] `syntax_error.py`: Invalid Python
- [ ] Document expected complexity values

### Task 3.4: Documentation

- [ ] Update `README.md`:
  - [ ] Add scanner overview
  - [ ] Add usage examples
  - [ ] Add complexity guidelines
  - [ ] Add severity level descriptions
  - [ ] Add example output
- [ ] Add docstrings to all public functions
- [ ] Add type hints throughout

## Phase 4: Integration and Polish

### Task 4.1: CLI Integration

- [ ] Update `upcast/main.py`:
  - [ ] Import `scan_complexity` command
  - [ ] Register in CLI group
- [ ] Verify `upcast --help` shows new command
- [ ] Test end-to-end workflow

### Task 4.2: Performance Testing

- [ ] Test on large codebase (1000+ files)
- [ ] Verify < 10 second completion
- [ ] Monitor memory usage
- [ ] Optimize if needed

### Task 4.3: Code Quality

- [ ] Run ruff check, ensure compliance
- [ ] Run unit tests: `uv run pytest tests/test_cyclomatic_complexity_scanner/`
- [ ] Run integration tests
- [ ] Verify 100% pass rate

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
