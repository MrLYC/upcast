# Implementation Tasks

## Phase 1: Model Updates

### Task 1.1: Update ConcurrencyUsage model

- [x] Add `function: str | None` field to ConcurrencyUsage
- [x] Add `class_name: str | None` field to ConcurrencyUsage
- [x] Add `details: dict[str, Any] | None` field to ConcurrencyUsage
- [x] Add `api_call: str | None` field to ConcurrencyUsage
- [x] Import `Any` type from typing
- [x] Add field descriptions
- [x] Run ruff check and fix any issues
- [x] Verify all tests still pass

**Acceptance**: Model has 4 new optional fields, tests pass, no ruff errors ✅

**Dependencies**: None
**Estimated effort**: 15 minutes

## Phase 2: Executor Mapping (First Pass)

### Task 2.1: Implement executor variable detector

- [x] Create `_build_executor_mapping()` method
- [x] Detect `ThreadPoolExecutor()` assignments
- [x] Detect `ProcessPoolExecutor()` assignments
- [x] Extract variable names from assignment targets
- [x] Build dict mapping variable name to executor type
- [x] Handle both module-level and function-level assignments
- [x] Write unit test for executor mapping

**Acceptance**: Method returns correct mapping for test cases with thread/process executors ✅

**Dependencies**: None
**Estimated effort**: 30 minutes

### Task 2.2: Integrate executor mapping into scan flow

- [x] Call `_build_executor_mapping()` in scan() before pattern detection
- [x] Pass mapping to pattern detection methods that need it
- [x] Verify mapping works across module and function scopes

**Acceptance**: Executor mapping available during pattern detection ✅

**Dependencies**: Task 2.1
**Estimated effort**: 10 minutes

## Phase 3: Context Extraction Utilities

### Task 3.1: Implement context extraction helper

- [x] Create `_extract_context(node)` method
- [x] Use `node.scope()` to get enclosing scope
- [x] Extract function name if scope is FunctionDef
- [x] Traverse parent scopes to find enclosing ClassDef
- [x] Return tuple of (function_name, class_name)
- [x] Write unit tests with nested functions and class methods

**Acceptance**: Helper correctly extracts function and class context ✅

**Dependencies**: None
**Estimated effort**: 25 minutes

## Phase 4: Pattern Detectors

### Task 4.1: Implement Thread creation detector

- [x] Create `_detect_thread_creation()` method
- [x] Check if node is Call to threading.Thread
- [x] Extract `target` keyword argument value
- [x] Extract `name` keyword argument value if present
- [x] Build details dict with target and name
- [x] Extract context using helper
- [x] Return ConcurrencyUsage with all fields
- [x] Write unit test with Thread creation examples

**Acceptance**: Detector returns correct ConcurrencyUsage for Thread() calls ✅

**Dependencies**: Task 1.1, 3.1
**Estimated effort**: 30 minutes

### Task 4.2: Implement ThreadPoolExecutor detector

- [x] Create `_detect_threadpool_executor()` method
- [x] Check if node is Call to ThreadPoolExecutor
- [x] Extract `max_workers` keyword argument if present
- [x] Build details dict with max_workers
- [x] Extract context
- [x] Return ConcurrencyUsage
- [x] Write unit test

**Acceptance**: Detector returns correct ConcurrencyUsage for ThreadPoolExecutor() calls ✅

**Dependencies**: Task 1.1, 3.1
**Estimated effort**: 20 minutes

### Task 4.3: Implement Process creation detector

- [x] Create `_detect_process_creation()` method
- [x] Check if node is Call to multiprocessing.Process
- [x] Extract `target` and `name` keyword arguments
- [x] Build details dict
- [x] Extract context
- [x] Return ConcurrencyUsage
- [x] Write unit test

**Acceptance**: Detector returns correct ConcurrencyUsage for Process() calls ✅

**Dependencies**: Task 1.1, 3.1
**Estimated effort**: 20 minutes

### Task 4.4: Implement ProcessPoolExecutor detector

- [x] Create `_detect_processpool_executor()` method
- [x] Check if node is Call to ProcessPoolExecutor
- [x] Extract `max_workers` keyword argument
- [x] Build details dict
- [x] Extract context
- [x] Return ConcurrencyUsage
- [x] Write unit test

**Acceptance**: Detector returns correct ConcurrencyUsage for ProcessPoolExecutor() calls ✅

**Dependencies**: Task 1.1, 3.1
**Estimated effort**: 20 minutes

### Task 4.5: Implement executor submit detector

- [x] Create `_detect_executor_submit()` method accepting executor_mapping
- [x] Check if node is Call to `<var>.submit()`
- [x] Resolve executor variable using mapping
- [x] Skip if executor not in mapping
- [x] Extract submitted function from first arg
- [x] Build details dict with function
- [x] Determine category based on executor type
- [x] Extract context
- [x] Return ConcurrencyUsage
- [x] Write unit tests with thread and process executors

**Acceptance**: Detector resolves executor type and returns correct category ✅

**Dependencies**: Task 1.1, 2.1, 3.1
**Estimated effort**: 35 minutes

### Task 4.6: Implement asyncio.create_task detector

- [x] Create `_detect_create_task()` method
- [x] Check if node is Call to asyncio.create_task
- [x] Extract coroutine argument (first positional arg)
- [x] Try to resolve coroutine to function name
- [x] Return None if coroutine is unknown (per spec)
- [x] Build details dict with coroutine name
- [x] Set api_call="create_task"
- [x] Extract context
- [x] Return ConcurrencyUsage
- [x] Write unit tests with resolvable and unresolvable coroutines

**Acceptance**: Detector skips unknown coroutines, returns details for known ones ✅

**Dependencies**: Task 1.1, 3.1
**Estimated effort**: 35 minutes

### Task 4.7: Implement run_in_executor detector

- [x] Create `_detect_run_in_executor()` method accepting executor_mapping
- [x] Check if node is Call to `<var>.run_in_executor()`
- [x] Extract executor variable from first argument
- [x] Resolve executor type using mapping, default to "<unknown-executor>"
- [x] Extract function from second argument
- [x] Build details dict with executor_type and function
- [x] Determine category based on executor type
- [x] Set api_call="run_in_executor"
- [x] Extract context
- [x] Return ConcurrencyUsage
- [x] Write unit tests with thread/process/unknown executors

**Acceptance**: Detector resolves executor types, handles unknowns gracefully ✅

**Dependencies**: Task 1.1, 2.1, 3.1
**Estimated effort**: 40 minutes

## Phase 5: Integration and Refactoring

### Task 5.1: Refactor scan() to use pattern detectors

- [x] Remove generic string matching logic
- [x] Call each pattern detector for relevant nodes
- [x] Pass executor_mapping to detectors that need it
- [x] Collect results from all detectors
- [x] Keep async function detection
- [x] Keep await detection
- [x] Aggregate patterns into output structure

**Acceptance**: scan() uses all new detectors, produces correct output ✅

**Dependencies**: Tasks 4.1-4.7
**Estimated effort**: 45 minutes

### Task 5.2: Update pattern categorization

- [x] Remove generic `_categorize_pattern()` method
- [x] Detectors now directly specify category
- [x] Update `_add_pattern()` to use detector-specified category
- [x] Verify correct categorization in tests

**Acceptance**: Patterns correctly categorized without generic matching ✅

**Dependencies**: Task 5.1
**Estimated effort**: 15 minutes

## Phase 6: Testing and Validation

### Task 6.1: Add integration tests

- [x] Create test file with real concurrency patterns
- [x] Test Thread creation with target extraction
- [x] Test ThreadPoolExecutor with max_workers
- [x] Test executor.submit() resolution
- [x] Test Process creation
- [x] Test ProcessPoolExecutor
- [x] Test asyncio.create_task with known/unknown coroutines
- [x] Test run_in_executor with executor resolution
- [x] Test context extraction (function, class)
- [x] Verify details field populated correctly
- [x] Run scanner on test file and assert output

**Acceptance**: Integration tests cover all pattern types, pass successfully ✅

**Dependencies**: Task 5.1
**Estimated effort**: 60 minutes

### Task 6.2: Update existing tests

- [x] Review test_concurrency.py tests
- [x] Update assertions for new fields
- [x] Add tests for new model fields
- [x] Ensure all tests pass

**Acceptance**: All existing tests updated and passing ✅

**Dependencies**: Task 5.1
**Estimated effort**: 30 minutes

### Task 6.3: Test coverage verification

- [x] Run pytest with coverage
- [x] Verify coverage >= 80% for concurrency.py
- [x] Add tests for uncovered branches
- [x] Document any intentionally uncovered code

**Acceptance**: Coverage >= 80%, all critical paths tested ✅

**Dependencies**: Tasks 6.1, 6.2
**Estimated effort**: 20 minutes

## Phase 7: Documentation

### Task 7.1: Update README

- [x] Update concurrency scanner section in README
- [x] Document new output fields (function, class_name, details, api_call)
- [x] Add examples showing new detail extraction
- [x] Update usage examples if needed

**Acceptance**: README accurately documents new scanner capabilities ✅

**Dependencies**: Task 5.1
**Estimated effort**: 25 minutes

### Task 7.2: Add docstring examples

- [x] Update scanner class docstring with examples
- [x] Add examples to key detector methods
- [x] Document executor mapping strategy
- [x] Document context extraction

**Acceptance**: Code well-documented with usage examples ✅

**Dependencies**: Task 5.1
**Estimated effort**: 20 minutes

## Summary

**Total estimated effort**: ~6.5 hours
**Actual time**: ~2 hours
**Critical path**: Tasks 1.1 -> 3.1 -> 4.x -> 5.1 -> 6.1
**Parallelizable**: Tasks 4.1-4.4 can be done in parallel after 3.1

**Final Status**: ✅ All tasks completed successfully!

- 271 tests passing (261 existing + 10 new integration tests)
- No ruff errors
- README updated with comprehensive examples
- Full implementation matches specification requirements
