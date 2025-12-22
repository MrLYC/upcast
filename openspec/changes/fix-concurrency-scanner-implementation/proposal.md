# Fix Concurrency Scanner Implementation

## Problem

The current `concurrency.py` scanner implementation uses simple string matching and does not conform to the detailed requirements in `concurrency-pattern-scanner` specification. Key gaps:

1. **Pattern Detection Too Simplistic**: Current implementation just checks if pattern keywords exist in function names, missing crucial distinctions like:

   - Thread creation vs ThreadPoolExecutor creation vs submit() calls
   - Process creation vs ProcessPoolExecutor creation vs submit() calls
   - asyncio.create_task() with coroutine resolution vs generic asyncio calls

2. **Missing Context Extraction**: Spec requires extracting function and class context for each pattern, but implementation doesn't capture this.

3. **No Executor Variable Resolution**: Spec requires two-pass analysis to resolve executor types for `run_in_executor()` calls, but implementation doesn't detect this pattern at all.

4. **Missing run_in_executor Detection**: Spec explicitly requires detecting `loop.run_in_executor()` with executor type resolution, completely missing in implementation.

5. **No Detailed Information Extraction**: Spec requires extracting:

   - Target functions/callables for Thread/Process
   - max_workers for executors
   - Coroutine names for asyncio.create_task()
     Current implementation only captures generic statement strings.

6. **Unknown Coroutine Handling**: Spec requires skipping `asyncio.create_task()` calls where coroutine cannot be resolved, but implementation would include them.

## Proposed Solution

Reimplement the scanner with:

1. **Pattern-Specific Detectors**: Create dedicated detection methods for each pattern type:

   - `_detect_thread_creation()` - threading.Thread()
   - `_detect_threadpool_executor()` - ThreadPoolExecutor()
   - `_detect_executor_submit()` - executor.submit()
   - `_detect_process_creation()` - multiprocessing.Process()
   - `_detect_processpool_executor()` - ProcessPoolExecutor()
   - `_detect_create_task()` - asyncio.create_task() with coroutine resolution
   - `_detect_run_in_executor()` - loop.run_in_executor() with executor type resolution

2. **Two-Pass Scanning**:

   - First pass: Build executor variable mapping (name -> type)
   - Second pass: Detect patterns and resolve executor references

3. **Context Extraction**: For each pattern:

   - Extract enclosing function name using `node.scope()`
   - Extract enclosing class name if inside method
   - Store in pattern output

4. **Detail Extraction**: Based on pattern type:

   - Thread/Process: Extract target callable
   - Executors: Extract max_workers parameter
   - create_task: Extract and resolve coroutine name, skip if unknown
   - run_in_executor: Resolve executor type, mark `<unknown-executor>` if unresolved

5. **Enhanced Output Model**: Update `ConcurrencyUsage` to include:
   - `function: str | None` - enclosing function
   - `class_name: str | None` - enclosing class
   - `details: dict[str, Any] | None` - pattern-specific details (target, max_workers, executor_type, etc.)
   - `api_call: str | None` - specific API method called

## Impact

- Breaks existing output format (adds new fields to ConcurrencyUsage)
- Provides much more detailed and actionable information
- Aligns implementation with specification requirements
- Improves pattern categorization accuracy

## Alternatives Considered

1. **Keep simple string matching**: Rejected - doesn't meet spec requirements
2. **Partial implementation**: Rejected - would leave spec violations
3. **Update spec to match implementation**: Rejected - spec is correct and more useful

## Dependencies

- Requires updating `upcast/models/concurrency.py` to add new fields
- May require test updates for new output format
