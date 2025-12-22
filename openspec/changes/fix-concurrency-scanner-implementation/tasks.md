# Implementation Tasks

## Phase 1: Model Updates

### Task 1.1: Update ConcurrencyUsage model

- [ ] Add `function: str | None` field to ConcurrencyUsage
- [ ] Add `class_name: str | None` field to ConcurrencyUsage
- [ ] Add `details: dict[str, Any] | None` field to ConcurrencyUsage
- [ ] Add `api_call: str | None` field to ConcurrencyUsage
- [ ] Import `Any` type from typing
- [ ] Add field descriptions
- [ ] Run ruff check and fix any issues
- [ ] Verify all tests still pass

**Acceptance**: Model has 4 new optional fields, tests pass, no ruff errors

**Dependencies**: None
**Estimated effort**: 15 minutes

## Phase 2: Executor Mapping (First Pass)

### Task 2.1: Implement executor variable detector

- [ ] Create `_build_executor_mapping()` method
- [ ] Detect `ThreadPoolExecutor()` assignments
- [ ] Detect `ProcessPoolExecutor()` assignments
- [ ] Extract variable names from assignment targets
- [ ] Build dict mapping variable name to executor type
- [ ] Handle both module-level and function-level assignments
- [ ] Write unit test for executor mapping

**Acceptance**: Method returns correct mapping for test cases with thread/process executors

**Dependencies**: None
**Estimated effort**: 30 minutes

### Task 2.2: Integrate executor mapping into scan flow

- [ ] Call `_build_executor_mapping()` in scan() before pattern detection
- [ ] Pass mapping to pattern detection methods that need it
- [ ] Verify mapping works across module and function scopes

**Acceptance**: Executor mapping available during pattern detection

**Dependencies**: Task 2.1
**Estimated effort**: 10 minutes

## Phase 3: Context Extraction Utilities

### Task 3.1: Implement context extraction helper

- [ ] Create `_extract_context(node)` method
- [ ] Use `node.scope()` to get enclosing scope
- [ ] Extract function name if scope is FunctionDef
- [ ] Traverse parent scopes to find enclosing ClassDef
- [ ] Return tuple of (function_name, class_name)
- [ ] Write unit tests with nested functions and class methods

**Acceptance**: Helper correctly extracts function and class context

**Dependencies**: None
**Estimated effort**: 25 minutes

## Phase 4: Pattern Detectors

### Task 4.1: Implement Thread creation detector

- [ ] Create `_detect_thread_creation()` method
- [ ] Check if node is Call to threading.Thread
- [ ] Extract `target` keyword argument value
- [ ] Extract `name` keyword argument value if present
- [ ] Build details dict with target and name
- [ ] Extract context using helper
- [ ] Return ConcurrencyUsage with all fields
- [ ] Write unit test with Thread creation examples

**Acceptance**: Detector returns correct ConcurrencyUsage for Thread() calls

**Dependencies**: Task 1.1, 3.1
**Estimated effort**: 30 minutes

### Task 4.2: Implement ThreadPoolExecutor detector

- [ ] Create `_detect_threadpool_executor()` method
- [ ] Check if node is Call to ThreadPoolExecutor
- [ ] Extract `max_workers` keyword argument if present
- [ ] Build details dict with max_workers
- [ ] Extract context
- [ ] Return ConcurrencyUsage
- [ ] Write unit test

**Acceptance**: Detector returns correct ConcurrencyUsage for ThreadPoolExecutor() calls

**Dependencies**: Task 1.1, 3.1
**Estimated effort**: 20 minutes

### Task 4.3: Implement Process creation detector

- [ ] Create `_detect_process_creation()` method
- [ ] Check if node is Call to multiprocessing.Process
- [ ] Extract `target` and `name` keyword arguments
- [ ] Build details dict
- [ ] Extract context
- [ ] Return ConcurrencyUsage
- [ ] Write unit test

**Acceptance**: Detector returns correct ConcurrencyUsage for Process() calls

**Dependencies**: Task 1.1, 3.1
**Estimated effort**: 20 minutes

### Task 4.4: Implement ProcessPoolExecutor detector

- [ ] Create `_detect_processpool_executor()` method
- [ ] Check if node is Call to ProcessPoolExecutor
- [ ] Extract `max_workers` keyword argument
- [ ] Build details dict
- [ ] Extract context
- [ ] Return ConcurrencyUsage
- [ ] Write unit test

**Acceptance**: Detector returns correct ConcurrencyUsage for ProcessPoolExecutor() calls

**Dependencies**: Task 1.1, 3.1
**Estimated effort**: 20 minutes

### Task 4.5: Implement executor submit detector

- [ ] Create `_detect_executor_submit()` method accepting executor_mapping
- [ ] Check if node is Call to `<var>.submit()`
- [ ] Resolve executor variable using mapping
- [ ] Skip if executor not in mapping
- [ ] Extract submitted function from first arg
- [ ] Build details dict with function
- [ ] Determine category based on executor type
- [ ] Extract context
- [ ] Return ConcurrencyUsage
- [ ] Write unit tests with thread and process executors

**Acceptance**: Detector resolves executor type and returns correct category

**Dependencies**: Task 1.1, 2.1, 3.1
**Estimated effort**: 35 minutes

### Task 4.6: Implement asyncio.create_task detector

- [ ] Create `_detect_create_task()` method
- [ ] Check if node is Call to asyncio.create_task
- [ ] Extract coroutine argument (first positional arg)
- [ ] Try to resolve coroutine to function name
- [ ] Return None if coroutine is unknown (per spec)
- [ ] Build details dict with coroutine name
- [ ] Set api_call="create_task"
- [ ] Extract context
- [ ] Return ConcurrencyUsage
- [ ] Write unit tests with resolvable and unresolvable coroutines

**Acceptance**: Detector skips unknown coroutines, returns details for known ones

**Dependencies**: Task 1.1, 3.1
**Estimated effort**: 35 minutes

### Task 4.7: Implement run_in_executor detector

- [ ] Create `_detect_run_in_executor()` method accepting executor_mapping
- [ ] Check if node is Call to `<var>.run_in_executor()`
- [ ] Extract executor variable from first argument
- [ ] Resolve executor type using mapping, default to "<unknown-executor>"
- [ ] Extract function from second argument
- [ ] Build details dict with executor_type and function
- [ ] Determine category based on executor type
- [ ] Set api_call="run_in_executor"
- [ ] Extract context
- [ ] Return ConcurrencyUsage
- [ ] Write unit tests with thread/process/unknown executors

**Acceptance**: Detector resolves executor types, handles unknowns gracefully

**Dependencies**: Task 1.1, 2.1, 3.1
**Estimated effort**: 40 minutes

## Phase 5: Integration and Refactoring

### Task 5.1: Refactor scan() to use pattern detectors

- [ ] Remove generic string matching logic
- [ ] Call each pattern detector for relevant nodes
- [ ] Pass executor_mapping to detectors that need it
- [ ] Collect results from all detectors
- [ ] Keep async function detection
- [ ] Keep await detection
- [ ] Aggregate patterns into output structure

**Acceptance**: scan() uses all new detectors, produces correct output

**Dependencies**: Tasks 4.1-4.7
**Estimated effort**: 45 minutes

### Task 5.2: Update pattern categorization

- [ ] Remove generic `_categorize_pattern()` method
- [ ] Detectors now directly specify category
- [ ] Update `_add_pattern()` to use detector-specified category
- [ ] Verify correct categorization in tests

**Acceptance**: Patterns correctly categorized without generic matching

**Dependencies**: Task 5.1
**Estimated effort**: 15 minutes

## Phase 6: Testing and Validation

### Task 6.1: Add integration tests

- [ ] Create test file with real concurrency patterns
- [ ] Test Thread creation with target extraction
- [ ] Test ThreadPoolExecutor with max_workers
- [ ] Test executor.submit() resolution
- [ ] Test Process creation
- [ ] Test ProcessPoolExecutor
- [ ] Test asyncio.create_task with known/unknown coroutines
- [ ] Test run_in_executor with executor resolution
- [ ] Test context extraction (function, class)
- [ ] Verify details field populated correctly
- [ ] Run scanner on test file and assert output

**Acceptance**: Integration tests cover all pattern types, pass successfully

**Dependencies**: Task 5.1
**Estimated effort**: 60 minutes

### Task 6.2: Update existing tests

- [ ] Review test_concurrency.py tests
- [ ] Update assertions for new fields
- [ ] Add tests for new model fields
- [ ] Ensure all tests pass

**Acceptance**: All existing tests updated and passing

**Dependencies**: Task 5.1
**Estimated effort**: 30 minutes

### Task 6.3: Test coverage verification

- [ ] Run pytest with coverage
- [ ] Verify coverage >= 80% for concurrency.py
- [ ] Add tests for uncovered branches
- [ ] Document any intentionally uncovered code

**Acceptance**: Coverage >= 80%, all critical paths tested

**Dependencies**: Tasks 6.1, 6.2
**Estimated effort**: 20 minutes

## Phase 7: Documentation

### Task 7.1: Update README

- [ ] Update concurrency scanner section in README
- [ ] Document new output fields (function, class_name, details, api_call)
- [ ] Add examples showing new detail extraction
- [ ] Update usage examples if needed

**Acceptance**: README accurately documents new scanner capabilities

**Dependencies**: Task 5.1
**Estimated effort**: 25 minutes

### Task 7.2: Add docstring examples

- [ ] Update scanner class docstring with examples
- [ ] Add examples to key detector methods
- [ ] Document executor mapping strategy
- [ ] Document context extraction

**Acceptance**: Code well-documented with usage examples

**Dependencies**: Task 5.1
**Estimated effort**: 20 minutes

## Summary

**Total estimated effort**: ~6.5 hours
**Critical path**: Tasks 1.1 -> 3.1 -> 4.x -> 5.1 -> 6.1
**Parallelizable**: Tasks 4.1-4.4 can be done in parallel after 3.1
