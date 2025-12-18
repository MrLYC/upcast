# Tasks

## 1. Create Module Structure

- [ ] Create `upcast/concurrency_scanner/` directory
- [ ] Create `__init__.py` with public API exports
- [ ] Create `checker.py` for AST visitor
- [ ] Create `pattern_parser.py` for pattern detection logic
- [ ] Create `export.py` for YAML formatting
- [ ] Create `cli.py` for scanning orchestration

## 2. Implement Core Checker

- [ ] Implement `ConcurrencyChecker` class with AST visitor pattern
- [ ] Add `visit_module()` method to traverse AST nodes
- [ ] Set up pattern collection dictionaries grouped by type
- [ ] Implement context tracking (current file, function, class)
- [ ] Add error handling for parse failures

## 3. Implement Asyncio Pattern Detection

- [ ] Detect `async def` function definitions (`parse_async_function`)
- [ ] Detect `await` expressions (`parse_await_expression`)
- [ ] Detect `asyncio.gather()` calls (`parse_asyncio_gather`)
- [ ] Detect `asyncio.create_task()` calls (`parse_asyncio_create_task`)
- [ ] Detect `async with` context managers (`parse_async_context_manager`)
- [ ] Extract function/class context for each pattern
- [ ] Handle both `asyncio.X` and `from asyncio import X` forms

## 4. Implement Threading Pattern Detection

- [ ] Detect `threading.Thread()` instantiation (`parse_thread_creation`)
- [ ] Detect `ThreadPoolExecutor()` creation (`parse_thread_pool_executor`)
- [ ] Extract `max_workers` parameter when present
- [ ] Track executor variable names for later resolution
- [ ] Detect `thread_pool.submit()` calls (`parse_thread_pool_submit`)
- [ ] Handle both direct instantiation and `with` context manager forms

## 5. Implement Multiprocessing Pattern Detection

- [ ] Detect `multiprocessing.Process()` instantiation (`parse_process_creation`)
- [ ] Detect `ProcessPoolExecutor()` creation (`parse_process_pool_executor`)
- [ ] Extract `max_workers` parameter when present
- [ ] Track executor variable names for later resolution
- [ ] Detect `process_pool.submit()` calls (`parse_process_pool_submit`)

## 6. Implement Executor Bridge Detection

- [ ] Detect `loop.run_in_executor()` calls (`parse_run_in_executor`)
- [ ] Resolve executor variable to determine type (Thread vs Process)
- [ ] Extract target function/callable reference
- [ ] Handle both explicit loop references and `asyncio.get_running_loop()`
- [ ] Mark unresolved executors as `<unknown-executor>`

## 7. Implement Context Extraction

- [ ] Extract file path (relative to project root)
- [ ] Extract line numbers for each pattern
- [ ] Extract enclosing function name using `scope()`
- [ ] Extract enclosing class name (if any)
- [ ] Extract module path
- [ ] Handle nested functions and classes correctly

## 8. Implement Executor Resolution

- [ ] First pass: Collect all executor definitions (ThreadPoolExecutor, ProcessPoolExecutor)
- [ ] Build executor name-to-type mapping
- [ ] Second pass: Resolve `run_in_executor` calls using mapping
- [ ] Handle module-level vs function-level executor definitions
- [ ] Mark unresolved references appropriately

## 9. Implement Pattern Details Extraction

- [ ] Extract code snippet for each pattern (limited length)
- [ ] Simplify complex comprehensions in display
- [ ] Extract API call names (e.g., "asyncio.gather")
- [ ] Extract executor types for run_in_executor
- [ ] Format details string for readability

## 10. Implement YAML Export

- [ ] Create `format_concurrency_output()` function
- [ ] Group patterns by concurrency type (asyncio, threading, multiprocessing)
- [ ] Sub-group by pattern type (gather, executor, etc.)
- [ ] Format each pattern with file, line, function, details
- [ ] Use common export utilities for YAML generation
- [ ] Sort output for consistency

## 11. Implement CLI Integration

- [ ] Create `scan_concurrency()` function in `cli.py`
- [ ] Support path argument (file or directory)
- [ ] Add `-o/--output` option for output file
- [ ] Add `-v/--verbose` option for debug output
- [ ] Add `--include` and `--exclude` pattern options
- [ ] Add `--no-default-excludes` flag
- [ ] Integrate with common file collection utilities
- [ ] Return YAML string or write to file

## 12. Add Main CLI Command

- [ ] Add `scan-concurrency` command to `upcast/main.py`
- [ ] Wire up command-line options
- [ ] Add help text and examples
- [ ] Test command invocation

## 13. Create Test Fixtures

- [ ] Create `tests/test_concurrency_scanner/fixtures/` directory
- [ ] Create `asyncio_patterns.py` with asyncio examples
- [ ] Create `threading_patterns.py` with threading examples
- [ ] Create `multiprocessing_patterns.py` with multiprocessing examples
- [ ] Create `mixed_patterns.py` with multiple pattern types
- [ ] Create `complex_patterns.py` with edge cases
- [ ] Create `executor_bridge.py` with run_in_executor examples

## 14. Write Unit Tests

- [ ] Test `parse_async_function()` with various async def patterns
- [ ] Test `parse_await_expression()` with different await contexts
- [ ] Test `parse_asyncio_gather()` with different argument forms
- [ ] Test `parse_asyncio_create_task()` detection
- [ ] Test `parse_thread_pool_executor()` with max_workers extraction
- [ ] Test `parse_process_pool_executor()` detection
- [ ] Test `parse_run_in_executor()` with executor resolution
- [ ] Test context extraction (file, line, function, class)
- [ ] Test executor resolution mapping
- [ ] Test edge cases (nested, conditional, dynamic)

## 15. Write Integration Tests

- [ ] Test scanning `asyncio_patterns.py` fixture
- [ ] Test scanning `threading_patterns.py` fixture
- [ ] Test scanning `multiprocessing_patterns.py` fixture
- [ ] Test scanning `mixed_patterns.py` fixture
- [ ] Test scanning directory with multiple files
- [ ] Test YAML output format and structure
- [ ] Test pattern grouping by type
- [ ] Test include/exclude patterns
- [ ] Test verbose output

## 16. Write CLI Tests

- [ ] Test `scan-concurrency` command help
- [ ] Test scanning single file
- [ ] Test scanning directory
- [ ] Test output to file with `-o` option
- [ ] Test verbose mode with `-v`
- [ ] Test include patterns with `--include`
- [ ] Test exclude patterns with `--exclude`
- [ ] Test nonexistent path handling

## 17. Add Error Handling Tests

- [ ] Test handling of parse errors
- [ ] Test handling of missing files
- [ ] Test handling of unresolved executors
- [ ] Test handling of invalid pattern syntax
- [ ] Test graceful degradation

## 18. Documentation

- [ ] Add docstrings to all public functions
- [ ] Document pattern detection logic
- [ ] Document YAML output format
- [ ] Add usage examples to CLI help
- [ ] Document limitations and edge cases
- [ ] Update README if needed

## 19. Validate and Polish

- [ ] Run all tests (ensure 100% pass rate)
- [ ] Check code style with ruff
- [ ] Verify CLI integration
- [ ] Test on real project samples
- [ ] Validate YAML output format
- [ ] Review and improve error messages

## 20. Update OpenSpec

- [ ] Run `openspec validate implement-concurrency-scanner --strict`
- [ ] Address any validation issues
- [ ] Ensure all requirements have scenarios
- [ ] Ensure all tasks map to requirements
