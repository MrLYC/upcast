# Tasks

## 1. Create Module Structure

- [x] Create `upcast/concurrency_scanner/` directory
- [x] Create `__init__.py` with public API exports
- [x] Create `checker.py` for AST visitor
- [x] Create `pattern_parser.py` for pattern detection logic
- [x] Create `export.py` for YAML formatting
- [x] Create `cli.py` for scanning orchestration

## 2. Implement Core Checker

- [x] Implement `ConcurrencyChecker` class with AST visitor pattern
- [x] Add `visit_module()` method to traverse AST nodes
- [x] Set up pattern collection dictionaries grouped by type
- [x] Implement context tracking (current file, function, class)
- [x] Add error handling for parse failures

## 3. Implement Asyncio Pattern Detection

- [x] Detect `async def` function definitions (`parse_async_function`)
- [x] Detect `await` expressions (`parse_await_expression`)
- [x] Detect `asyncio.gather()` calls (`parse_asyncio_gather`)
- [x] Detect `asyncio.create_task()` calls (`parse_asyncio_create_task`)
- [x] Detect `async with` context managers (`parse_async_context_manager`)
- [x] Extract function/class context for each pattern
- [x] Handle both `asyncio.X` and `from asyncio import X` forms

## 4. Implement Threading Pattern Detection

- [x] Detect `threading.Thread()` instantiation (`parse_thread_creation`)
- [x] Detect `ThreadPoolExecutor()` creation (`parse_thread_pool_executor`)
- [x] Extract `max_workers` parameter when present
- [x] Track executor variable names for later resolution
- [ ] Detect `thread_pool.submit()` calls (`parse_thread_pool_submit`)
- [x] Handle both direct instantiation and `with` context manager forms

## 5. Implement Multiprocessing Pattern Detection

- [x] Detect `multiprocessing.Process()` instantiation (`parse_process_creation`)
- [x] Detect `ProcessPoolExecutor()` creation (`parse_process_pool_executor`)
- [x] Extract `max_workers` parameter when present
- [x] Track executor variable names for later resolution
- [ ] Detect `process_pool.submit()` calls (`parse_process_pool_submit`)

## 6. Implement Executor Bridge Detection

- [x] Detect `loop.run_in_executor()` calls (`parse_run_in_executor`)
- [x] Resolve executor variable to determine type (Thread vs Process)
- [x] Extract target function/callable reference
- [x] Handle both explicit loop references and `asyncio.get_running_loop()`
- [x] Mark unresolved executors as `<unknown-executor>`

## 7. Implement Context Extraction

- [x] Extract file path (relative to project root)
- [x] Extract line numbers for each pattern
- [x] Extract enclosing function name using `scope()`
- [x] Extract enclosing class name (if any)
- [x] Extract module path
- [x] Handle nested functions and classes correctly

## 8. Implement Executor Resolution

- [x] First pass: Collect all executor definitions (ThreadPoolExecutor, ProcessPoolExecutor)
- [x] Build executor name-to-type mapping
- [x] Second pass: Resolve `run_in_executor` calls using mapping
- [x] Handle module-level vs function-level executor definitions
- [x] Mark unresolved references appropriately

## 9. Implement Pattern Details Extraction

- [x] Extract code snippet for each pattern (limited length)
- [x] Simplify complex comprehensions in display
- [x] Extract API call names (e.g., "asyncio.gather")
- [x] Extract executor types for run_in_executor
- [x] Format details string for readability

## 10. Implement YAML Export

- [x] Create `format_concurrency_output()` function
- [x] Group patterns by concurrency type (asyncio, threading, multiprocessing)
- [x] Sub-group by pattern type (gather, executor, etc.)
- [x] Format each pattern with file, line, function, details
- [x] Use common export utilities for YAML generation
- [x] Sort output for consistency

## 11. Implement CLI Integration

- [x] Create `scan_concurrency()` function in `cli.py`
- [x] Support path argument (file or directory)
- [x] Add `-o/--output` option for output file
- [x] Add `-v/--verbose` option for debug output
- [x] Add `--include` and `--exclude` pattern options
- [ ] Add `--no-default-excludes` flag
- [x] Integrate with common file collection utilities
- [x] Return YAML string or write to file

## 12. Add Main CLI Command

- [x] Add `scan-concurrency` command to `upcast/main.py`
- [x] Wire up command-line options
- [x] Add help text and examples
- [x] Test command invocation

## 13. Create Test Fixtures

- [x] Create `tests/test_concurrency_scanner/fixtures/` directory
- [x] Create `asyncio_patterns.py` with asyncio examples
- [x] Create `threading_patterns.py` with threading examples
- [x] Create `multiprocessing_patterns.py` with multiprocessing examples
- [x] Create `mixed_patterns.py` with multiple pattern types
- [x] Create `complex_patterns.py` with edge cases
- [x] Create `executor_bridge.py` with run_in_executor examples

## 14. Write Unit Tests

- [x] Test `parse_async_function()` with various async def patterns
- [x] Test `parse_await_expression()` with different await contexts
- [x] Test `parse_asyncio_gather()` with different argument forms
- [x] Test `parse_asyncio_create_task()` detection
- [x] Test `parse_thread_pool_executor()` with max_workers extraction
- [x] Test `parse_process_pool_executor()` detection
- [x] Test `parse_run_in_executor()` with executor resolution
- [x] Test context extraction (file, line, function, class)
- [x] Test executor resolution mapping
- [x] Test edge cases (nested, conditional, dynamic)

## 15. Write Integration Tests

- [x] Test scanning `asyncio_patterns.py` fixture
- [x] Test scanning `threading_patterns.py` fixture
- [x] Test scanning `multiprocessing_patterns.py` fixture
- [x] Test scanning `mixed_patterns.py` fixture
- [x] Test scanning directory with multiple files
- [x] Test YAML output format and structure
- [x] Test pattern grouping by type
- [x] Test include/exclude patterns
- [x] Test verbose output

## 16. Write CLI Tests

- [x] Test `scan-concurrency` command help
- [x] Test scanning single file
- [x] Test scanning directory
- [x] Test output to file with `-o` option
- [x] Test verbose mode with `-v`
- [x] Test include patterns with `--include`
- [x] Test exclude patterns with `--exclude`
- [x] Test nonexistent path handling

## 17. Add Error Handling Tests

- [x] Test handling of parse errors
- [x] Test handling of missing files
- [x] Test handling of unresolved executors
- [x] Test handling of invalid pattern syntax
- [x] Test graceful degradation

## 18. Documentation

- [x] Add docstrings to all public functions
- [x] Document pattern detection logic
- [x] Document YAML output format
- [x] Add usage examples to CLI help
- [x] Document limitations and edge cases
- [x] Update README if needed

## 19. Validate and Polish

- [x] Run all tests (ensure 100% pass rate)
- [x] Check code style with ruff
- [x] Verify CLI integration
- [x] Test on real project samples
- [x] Validate YAML output format
- [x] Review and improve error messages

## 20. Update OpenSpec

- [x] Run `openspec validate implement-concurrency-scanner --strict`
- [x] Address any validation issues
- [x] Ensure all requirements have scenarios
- [x] Ensure all tasks map to requirements
