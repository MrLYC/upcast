# Implementation Design

## Architecture

### Two-Pass Scanning Strategy

**Pass 1: Build Executor Mapping**

- Scan all assignments and function definitions
- Build mapping: `variable_name -> executor_type` (ThreadPoolExecutor | ProcessPoolExecutor)
- Store at both module and function scope levels

**Pass 2: Pattern Detection**

- Detect all concurrency patterns using dedicated detectors
- Use executor mapping to resolve `run_in_executor()` calls
- Extract context (function, class) for each pattern
- Extract pattern-specific details

### Pattern Detector Design

Each detector is a focused method that:

1. Checks if node matches pattern (e.g., `isinstance(Call)` + function name check)
2. Extracts pattern-specific details (target, max_workers, etc.)
3. Resolves dynamic references (executor variables, coroutine names)
4. Returns None if pattern incomplete/unresolvable (for asyncio.create_task with unknown coroutine)

### Context Extraction Strategy

Use Astroid's scope navigation:

```python
def _extract_context(node):
    scope = node.scope()
    function = scope.name if isinstance(scope, FunctionDef) else None

    # Find enclosing class
    class_name = None
    parent = scope.parent
    while parent:
        if isinstance(parent, ClassDef):
            class_name = parent.name
            break
        parent = parent.parent

    return function, class_name
```

## Data Flow

```
File -> Parse -> Pass 1 (Build Executor Map) -> Pass 2 (Detect Patterns) -> Aggregate -> Output
                                                         ↓
                                        [Thread, Process, Executor, create_task, run_in_executor, ...]
                                                         ↓
                                        Extract Context + Details
                                                         ↓
                                        ConcurrencyUsage with full info
```

## Pattern Detection Logic

### Thread Creation

```python
if isinstance(node, Call) and _is_thread_init(node):
    target = _extract_keyword_arg(node, 'target')
    name = _extract_keyword_arg(node, 'name')
    details = {'target': target, 'name': name}
```

### asyncio.create_task

```python
if isinstance(node, Call) and _is_create_task(node):
    coro = _resolve_coroutine(node.args[0])
    if coro == 'unknown':
        return None  # Skip per spec
    details = {'coroutine': coro}
```

### run_in_executor

```python
if isinstance(node, Call) and _is_run_in_executor(node):
    executor_var = _get_executor_arg(node)
    executor_type = executor_map.get(executor_var, '<unknown-executor>')
    func = _extract_function_arg(node)
    details = {'executor_type': executor_type, 'function': func}
```

## Model Updates

### ConcurrencyUsage

Add fields:

- `function: str | None` - enclosing function name
- `class_name: str | None` - enclosing class name
- `details: dict[str, Any] | None` - pattern-specific info
- `api_call: str | None` - specific API called (e.g., "create_task")

Keep existing:

- `file`, `line`, `column`, `pattern`, `statement`

## Testing Strategy

1. **Unit tests** for each detector method with mock AST nodes
2. **Integration tests** with real Python code snippets covering:
   - Thread/Process creation with target functions
   - Executor creation with max_workers
   - executor.submit() resolution
   - asyncio.create_task() with known/unknown coroutines
   - run_in_executor() with resolved/unresolved executors
   - Nested functions and class methods for context extraction
3. **Regression tests** ensuring no false positives on non-concurrency code

## Error Handling

- Parse errors: Log and skip file (existing behavior)
- Unresolvable executor: Mark as `<unknown-executor>`, include in output
- Unknown coroutine in create_task: Skip pattern entirely (per spec)
- Missing imports: Pattern won't match, no false positives

## Performance Considerations

- Two-pass adds overhead but necessary for correctness
- Executor mapping typically small (< 100 entries)
- Context extraction reuses Astroid's scope infrastructure
- Overall impact: ~20-30% slower but within acceptable range for accuracy gain
