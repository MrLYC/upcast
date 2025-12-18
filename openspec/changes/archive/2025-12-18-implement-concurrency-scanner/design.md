# Design: Concurrency Scanner

## Architecture Overview

The concurrency scanner follows the established project pattern of AST-based static analysis, reusing common utilities for file handling and output formatting.

```
┌─────────────────┐
│  CLI Entry      │
│ (scan-concurrency)│
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│  File Collection    │
│ (common.file_utils) │
└────────┬────────────┘
         │
         ▼
┌──────────────────────┐
│  ConcurrencyChecker  │
│  (AST Visitor)       │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  Pattern Parser      │
│  (pattern_parser.py) │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  YAML Export         │
│  (export.py)         │
└──────────────────────┘
```

## Core Components

### 1. ConcurrencyChecker (checker.py)

AST visitor that traverses Python modules and delegates pattern detection to specialized parsers.

**Responsibilities**:

- Visit module nodes using astroid
- Track current file/module context
- Collect detected patterns
- Group patterns by category

**Key Methods**:

```python
class ConcurrencyChecker:
    def __init__(self, root_path: str | None = None, verbose: bool = False)
    def visit_module(self, module: nodes.Module) -> None
    def get_patterns(self) -> dict[str, list[dict]]
```

### 2. Pattern Parser (pattern_parser.py)

Contains detection logic for each concurrency pattern type.

**Pattern Categories**:

#### Asyncio Patterns

- `parse_async_function(node)` - Detect `async def`
- `parse_await_expression(node)` - Detect `await` calls
- `parse_asyncio_gather(node)` - Detect `asyncio.gather()`
- `parse_asyncio_create_task(node)` - Detect `asyncio.create_task()`
- `parse_async_context_manager(node)` - Detect `async with`

#### Threading Patterns

- `parse_thread_creation(node)` - Detect `threading.Thread()`
- `parse_thread_pool_executor(node)` - Detect `ThreadPoolExecutor()`
- `parse_thread_pool_submit(node)` - Detect `thread_pool.submit()`

#### Multiprocessing Patterns

- `parse_process_creation(node)` - Detect `multiprocessing.Process()`
- `parse_process_pool_executor(node)` - Detect `ProcessPoolExecutor()`
- `parse_process_pool_submit(node)` - Detect `process_pool.submit()`

#### Executor Bridge Patterns

- `parse_run_in_executor(node)` - Detect `loop.run_in_executor()`

**Each parser returns**:

```python
{
    "pattern_type": "asyncio_gather",
    "file": "views.py",
    "line": 15,
    "function": "report_view",
    "details": "await asyncio.gather(*[...])",
    "api_call": "asyncio.gather",
}
```

### 3. Export Module (export.py)

Formats detected patterns into structured YAML output, grouped by concurrency category.

**Grouping Strategy**:

```yaml
asyncio:
  async_functions:
    - [functions defined with async def]
  gather_patterns:
    - [asyncio.gather() calls]
  task_creation:
    - [asyncio.create_task() calls]
  await_expressions:
    - [standalone await calls]

threading:
  thread_creation:
    - [threading.Thread() instantiations]
  thread_pool_executors:
    - [ThreadPoolExecutor definitions]
  executor_submissions:
    - [thread_pool.submit() calls]
  run_in_executor:
    - [loop.run_in_executor with ThreadPoolExecutor]

multiprocessing:
  process_creation:
    - [multiprocessing.Process() instantiations]
  process_pool_executors:
    - [ProcessPoolExecutor definitions]
  executor_submissions:
    - [process_pool.submit() calls]
  run_in_executor:
    - [loop.run_in_executor with ProcessPoolExecutor]
```

## Pattern Detection Details

### Asyncio Detection

#### Async Function Definitions

```python
# Detect this pattern
async def fetch_data(url):
    return await client.get(url)
```

AST pattern: `nodes.AsyncFunctionDef`

#### Asyncio.gather

```python
# Detect this pattern
results = await asyncio.gather(
    fetch(url1),
    fetch(url2),
    fetch(url3)
)
```

AST pattern:

- `nodes.Call` with func matching `asyncio.gather`
- Check both `asyncio.gather` and `from asyncio import gather`

#### Run in Executor

```python
# Detect and classify executor type
loop = asyncio.get_running_loop()
result = await loop.run_in_executor(
    thread_pool,  # <- Resolve to ThreadPoolExecutor
    blocking_func,
    arg1, arg2
)
```

AST pattern:

- `nodes.Call` with attr `run_in_executor`
- First arg should resolve to executor variable
- Use type inference to determine ThreadPoolExecutor vs ProcessPoolExecutor

### Threading Detection

#### ThreadPoolExecutor Creation

```python
# Detect executor definitions
executor = ThreadPoolExecutor(max_workers=5)
with ThreadPoolExecutor(max_workers=10) as pool:
    ...
```

AST pattern:

- `nodes.Call` with func matching `ThreadPoolExecutor`
- Extract `max_workers` argument if present
- Track variable name for later resolution

### Multiprocessing Detection

Similar patterns to threading, but checking for `ProcessPoolExecutor` and `multiprocessing.Process`.

## Executor Resolution Strategy

**Challenge**: `run_in_executor` references a variable that was defined elsewhere.

```python
# Definition (module level)
thread_pool = ThreadPoolExecutor(max_workers=5)

# Usage (inside function)
await loop.run_in_executor(thread_pool, func)
```

**Solution**:

1. First pass: Collect all executor definitions with their types
2. Store mapping: `{"thread_pool": "ThreadPoolExecutor", "process_pool": "ProcessPoolExecutor"}`
3. Second pass: When encountering `run_in_executor`, look up executor variable name in mapping
4. If not found, mark as `<unknown-executor>`

## Context Extraction

For each pattern, extract:

1. **File Location**: Relative path from project root
2. **Line Number**: Line where pattern occurs
3. **Function Context**: Name of enclosing function (if any)
4. **Class Context**: Name of enclosing class (if any)
5. **Module Context**: Full module path

Use astroid's `parent` and `scope()` methods to walk up the tree.

## Edge Cases & Limitations

### Dynamic Imports

```python
# Hard to detect
module = importlib.import_module("asyncio")
module.gather(...)
```

**Handling**: Skip - requires runtime information

### String Code Execution

```python
# Cannot detect
exec("await asyncio.gather(...)")
```

**Handling**: Skip - beyond static analysis scope

### Conditional Patterns

```python
if USE_MULTIPROCESSING:
    executor = ProcessPoolExecutor()
else:
    executor = ThreadPoolExecutor()
```

**Handling**: Report both, note conditional usage

### Nested Functions

```python
async def outer():
    async def inner():
        await something()
```

**Handling**: Report both with proper nesting context

## Performance Considerations

1. **Single Pass**: Parse each file once, collect all patterns
2. **Lazy Loading**: Only parse files matching include/exclude patterns
3. **Error Recovery**: Continue scanning on parse errors
4. **Memory**: Stream file processing, don't load all files into memory

## Testing Strategy

### Unit Tests

- Test each pattern parser independently
- Mock AST nodes for each pattern type
- Verify correct data extraction

### Integration Tests

- Test fixtures with real Python code
- Verify end-to-end scanning and output
- Test edge cases (nested, conditional, etc.)

### Test Fixtures

Create `tests/test_concurrency_scanner/fixtures/`:

- `asyncio_patterns.py` - All asyncio patterns
- `threading_patterns.py` - Threading patterns
- `multiprocessing_patterns.py` - Multiprocessing patterns
- `mixed_patterns.py` - Multiple pattern types
- `complex_patterns.py` - Edge cases

## Error Handling

1. **Parse Errors**: Log warning, continue with next file
2. **Resolution Failures**: Mark as `<unresolved>`, include in output
3. **Invalid Patterns**: Skip silently (avoid false positives)
4. **I/O Errors**: Log error, stop gracefully

## Future Enhancements

1. **Pattern Metrics**: Count occurrences, identify hotspots
2. **Cross-references**: Link executor definitions to their usage sites
3. **Dependency Graph**: Show call chains for concurrent functions
4. **Performance Hints**: Suggest optimizations based on patterns
5. **Synchronization Primitives**: Detect locks, events, queues
