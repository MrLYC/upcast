# Proposal: Implement Concurrency Pattern Scanner

## Overview

Create a static code analysis tool to scan Python projects and identify concurrency patterns including asyncio coroutines, threading, and multiprocessing usage. The scanner will detect where and how concurrent execution is used, categorize patterns, and output a structured report grouped by concurrency type.

## Motivation

Modern Python applications increasingly use multiple concurrency models (asyncio, threading, multiprocessing) to handle I/O-bound and CPU-bound tasks. Understanding concurrency usage across a codebase is critical for:

- **Performance optimization**: Identify opportunities to improve concurrent execution
- **Debugging**: Locate potential race conditions or deadlock scenarios
- **Architecture review**: Understand concurrency patterns and their distribution
- **Refactoring**: Make informed decisions when migrating between concurrency models
- **Documentation**: Generate accurate documentation of concurrent behavior

Without automated scanning, developers must manually grep through code or rely on incomplete mental models, leading to missed patterns and architectural blind spots.

## Goals

### Primary Goals

1. **Pattern Detection**: Accurately detect major Python concurrency patterns:

   - Asyncio coroutines (`async def`, `await`, `asyncio.gather`, `asyncio.create_task`)
   - Threading (`threading.Thread`, `ThreadPoolExecutor`, `concurrent.futures`)
   - Multiprocessing (`multiprocessing.Process`, `ProcessPoolExecutor`)
   - Executor patterns (`loop.run_in_executor`)

2. **Structured Output**: Generate YAML output grouped by concurrency pattern type with:

   - Pattern category (asyncio, threading, multiprocessing)
   - File location and line numbers
   - Function/class context
   - Specific API usage (e.g., `asyncio.gather`, `ThreadPoolExecutor`)

3. **CLI Integration**: Add `scan-concurrency` command following project patterns

### Non-Goals

- Runtime behavior analysis or performance profiling
- Deadlock or race condition detection (static analysis limitations)
- Automatic refactoring or optimization suggestions
- Support for third-party concurrency libraries beyond standard library

## Technical Approach

### Architecture

Follow established scanner pattern in the project:

```
upcast/concurrency_scanner/
├── __init__.py          # Public API
├── checker.py           # AST visitor (ConcurrencyChecker)
├── pattern_parser.py    # Pattern detection logic
├── cli.py               # CLI entry point (scan_concurrency)
└── export.py            # YAML formatting
```

### Detection Strategy

Use `astroid` for AST analysis to detect:

1. **Asyncio Patterns**:

   - `async def` function definitions
   - `await` expressions
   - `asyncio.gather()`, `asyncio.create_task()` calls
   - `asyncio.run()` entry points
   - Async context managers (`async with`)

2. **Threading Patterns**:

   - `threading.Thread` instantiation
   - `ThreadPoolExecutor` usage
   - `thread_pool.submit()` calls
   - `loop.run_in_executor(thread_pool, ...)`

3. **Multiprocessing Patterns**:
   - `multiprocessing.Process` instantiation
   - `ProcessPoolExecutor` usage
   - `process_pool.submit()` calls
   - `loop.run_in_executor(process_pool, ...)`

### Output Format

```yaml
asyncio:
  gather_patterns:
    - file: views.py
      line: 15
      function: report_view
      usage: asyncio.gather
      details: "await asyncio.gather(*[async_fetch(u) for u in urls])"

threading:
  executor_patterns:
    - file: views.py
      line: 20
      function: report_view
      usage: run_in_executor
      executor_type: ThreadPoolExecutor
      details: "loop.run_in_executor(thread_pool, lambda: ...)"

multiprocessing:
  executor_patterns:
    - file: views.py
      line: 26
      function: report_view
      usage: run_in_executor
      executor_type: ProcessPoolExecutor
      details: "loop.run_in_executor(process_pool, cpu_task, ...)"
```

## Implementation Plan

### Phase 1: Core Scanner (MVP)

1. Create module structure
2. Implement `ConcurrencyChecker` AST visitor
3. Detect basic asyncio patterns (async def, await)
4. Detect ThreadPoolExecutor and ProcessPoolExecutor instantiation
5. Basic YAML export

### Phase 2: Pattern Enrichment

1. Detect `asyncio.gather`, `asyncio.create_task`
2. Detect `loop.run_in_executor` usage
3. Extract function context and line numbers
4. Enhance output with pattern details

### Phase 3: CLI Integration

1. Add `scan-concurrency` command to main CLI
2. Support standard options (--output, --include, --exclude)
3. Add tests and documentation

## Success Criteria

1. **Accuracy**: Correctly identify concurrency patterns in test fixtures
2. **Coverage**: Detect all major concurrency APIs in example code
3. **Usability**: Generate clear, actionable YAML output
4. **Integration**: CLI works consistently with other scanners
5. **Testing**: 100% test coverage for pattern detection logic

## Open Questions

### Pattern Coverage

**Q**: Should we detect older patterns like `threading.Lock`, `Queue`, or `Event`?
**Recommendation**: Start with execution patterns (Thread, Executor), add synchronization primitives in v2 if needed.

**Q**: Should we detect `asyncio.sleep()` or other low-level asyncio APIs?
**Recommendation**: Focus on structural patterns (async def, gather, create_task) initially.

### Output Granularity

**Q**: Should we extract the actual function/lambda being executed?
**Recommendation**: Yes for executors where practical, extract target function name/code snippet.

**Q**: How to handle complex comprehensions like `[async_fetch(u) for u in urls]`?
**Recommendation**: Extract the pattern but show simplified representation in details.

### Executor Resolution

**Q**: How to handle executor variables defined far from usage?
**Recommendation**: Track module-level executor assignments, mark as `<unknown>` if resolution fails.

## Impact

### Benefits

- **Visibility**: Clear view of concurrency usage across codebase
- **Consistency**: Follows established scanner patterns
- **Automation**: Eliminates manual code review for concurrency patterns
- **Extensibility**: Foundation for future concurrency analysis tools

### Risks

- **Pattern Evolution**: New asyncio/threading APIs may require updates
- **Complex Resolution**: Executor variable tracking across modules may be incomplete
- **False Positives**: Comments or strings containing keywords might be detected

### Breaking Changes

None - this is a new feature with no impact on existing functionality.

## Alternatives Considered

### 1. Runtime Profiling

**Rejected**: Requires running code, can't analyze dead code or conditional patterns.

### 2. Regex-based Search

**Rejected**: Can't handle complex cases, poor accuracy, no context awareness.

### 3. Third-party Tools (e.g., pylint plugins)

**Rejected**: Doesn't integrate with project architecture, limited output customization.

## Dependencies

- `astroid` (already in project)
- `upcast.common.file_utils` for file collection
- `upcast.common.export` for YAML formatting
- Standard CLI patterns from existing scanners
