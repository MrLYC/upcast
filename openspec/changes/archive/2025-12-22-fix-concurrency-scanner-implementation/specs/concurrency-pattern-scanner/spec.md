# Concurrency Pattern Scanner Specification Delta

## MODIFIED Requirements

### Requirement: Threading Pattern Detection

The system SHALL detect threading-based concurrency patterns including Thread creation and ThreadPoolExecutor usage.

#### Scenario: Detect threading.Thread creation

- **WHEN** scanning for thread-based concurrency
- **THEN** the system SHALL identify `threading.Thread()` instantiations
- **AND** extract the target function or callable from `target=` keyword argument
- **AND** extract thread name from `name=` keyword argument if specified
- **AND** store target and name in `details` field
- **AND** categorize under `threading.thread_creation`

**DIFF**: Now requires explicit extraction of target and name into details field

#### Scenario: Detect ThreadPoolExecutor creation

- **WHEN** scanning for thread pool patterns
- **THEN** the system SHALL identify `ThreadPoolExecutor()` instantiations
- **AND** extract the `max_workers` parameter value if present
- **AND** track the executor variable name for resolution
- **AND** store max_workers in `details` field
- **AND** categorize under `threading.thread_pool_executors`

**DIFF**: Now requires explicit max_workers extraction into details field

#### Scenario: Detect thread pool submit calls

- **WHEN** scanning for executor task submission
- **THEN** the system SHALL identify calls to `executor.submit()`
- **AND** resolve the executor variable to ThreadPoolExecutor using executor mapping
- **AND** extract the submitted function/callable from first positional argument
- **AND** store function in `details` field
- **AND** categorize under `threading.executor_submissions`

**DIFF**: Now requires using executor mapping to resolve executor type

### Requirement: Multiprocessing Pattern Detection

The system SHALL detect multiprocessing-based concurrency patterns including Process creation and ProcessPoolExecutor usage.

#### Scenario: Detect multiprocessing.Process creation

- **WHEN** scanning for process-based concurrency
- **THEN** the system SHALL identify `multiprocessing.Process()` instantiations
- **AND** extract the target function from `target=` keyword argument
- **AND** extract process name from `name=` keyword argument if specified
- **AND** store target and name in `details` field
- **AND** categorize under `multiprocessing.process_creation`

**DIFF**: Now requires explicit extraction of target and name into details field

#### Scenario: Detect ProcessPoolExecutor creation

- **WHEN** scanning for process pool patterns
- **THEN** the system SHALL identify `ProcessPoolExecutor()` instantiations
- **AND** extract the `max_workers` parameter value if present
- **AND** track the executor variable name for resolution
- **AND** store max_workers in `details` field
- **AND** categorize under `multiprocessing.process_pool_executors`

**DIFF**: Now requires explicit max_workers extraction into details field

#### Scenario: Detect process pool submit calls

- **WHEN** scanning for executor task submission
- **THEN** the system SHALL identify calls to `executor.submit()`
- **AND** resolve the executor variable to ProcessPoolExecutor using executor mapping
- **AND** extract the submitted function/callable from first positional argument
- **AND** store function in `details` field
- **AND** categorize under `multiprocessing.executor_submissions`

**DIFF**: Now requires using executor mapping to resolve executor type

### Requirement: Asyncio Pattern Detection

The system SHALL detect asyncio.create_task() patterns and extract meaningful coroutine information.

#### Scenario: Skip unknown coroutines

- **WHEN** analyzing an `asyncio.create_task()` call
- **AND** the coroutine argument cannot be resolved to a specific function name
- **THEN** the system SHALL skip this detection entirely by returning None from detector
- **AND** NOT output a record with `coroutine: "unknown"` in details
- **AND** maintain output cleanliness by excluding low-value results

**DIFF**: Now requires detector to return None instead of outputting unknown

#### Scenario: Successful coroutine detection

- **WHEN** analyzing an `asyncio.create_task()` call
- **AND** the coroutine argument can be resolved to a specific function name
- **THEN** the system SHALL output a complete pattern record
- **AND** include the resolved coroutine name in `details.coroutine` field
- **AND** store "create_task" in `api_call` field
- **AND** provide file/line location information

**DIFF**: Now requires storing coroutine in details field and api_call

### Requirement: Executor Bridge Pattern Detection

The system SHALL detect asyncio-executor bridge patterns using `loop.run_in_executor()`.

#### Scenario: Detect run_in_executor with ThreadPoolExecutor

- **WHEN** scanning for asyncio-thread bridges
- **THEN** the system SHALL identify `loop.run_in_executor()` calls
- **AND** resolve the first argument executor variable using executor mapping
- **AND** classify as ThreadPoolExecutor when mapping indicates thread executor
- **AND** extract the target function/callable from second argument
- **AND** store executor_type="ThreadPoolExecutor" and function in `details` field
- **AND** categorize under `threading.run_in_executor`

**DIFF**: Now requires using executor mapping and storing details

#### Scenario: Detect run_in_executor with ProcessPoolExecutor

- **WHEN** scanning for asyncio-process bridges
- **THEN** the system SHALL identify `loop.run_in_executor()` calls
- **AND** resolve the first argument executor variable using executor mapping
- **AND** classify as ProcessPoolExecutor when mapping indicates process executor
- **AND** extract the target function/callable from second argument
- **AND** store executor_type="ProcessPoolExecutor" and function in `details` field
- **AND** categorize under `multiprocessing.run_in_executor`

**DIFF**: Now requires using executor mapping and storing details

#### Scenario: Handle unresolved executors

- **WHEN** executor type cannot be determined from mapping
- **THEN** the system SHALL mark executor as `<unknown-executor>` in details
- **AND** still record the run_in_executor usage
- **AND** include in output with unknown executor marker in `details.executor_type`

**DIFF**: Now stores in details field instead of pattern string

### Requirement: Context Extraction

The system SHALL extract contextual information for each detected concurrency pattern.

#### Scenario: Extract function context

- **WHEN** pattern appears inside a function
- **THEN** the system SHALL extract the enclosing function name using node.scope()
- **AND** include it in the pattern output in `function` field
- **AND** handle nested functions correctly by using immediate parent scope

**DIFF**: Now requires storing in dedicated `function` field

#### Scenario: Extract class context

- **WHEN** pattern appears inside a class method
- **THEN** the system SHALL extract the enclosing class name by traversing scope parents
- **AND** include it in the pattern output in `class_name` field
- **AND** combine with function name to show full context

**DIFF**: Now requires storing in dedicated `class_name` field

## ADDED Requirements

### Requirement: Two-Pass Scanning

The system SHALL use a two-pass scanning approach to enable executor type resolution.

#### Scenario: First pass builds executor mapping

- **WHEN** beginning to scan a module
- **THEN** the system SHALL perform a first pass over all nodes
- **AND** identify executor variable assignments (ThreadPoolExecutor, ProcessPoolExecutor)
- **AND** build a mapping of variable names to executor types
- **AND** track executors at both module-level and function-level scope

**Rationale**: Enables resolving executor references in submit() and run_in_executor() calls

#### Scenario: Second pass detects patterns with resolution

- **WHEN** performing pattern detection
- **THEN** the system SHALL use the executor mapping to resolve executor variables
- **AND** detect all concurrency patterns with full context
- **AND** extract pattern-specific details using the mapping

**Rationale**: Pattern detection needs executor type information from first pass

### Requirement: Enhanced Output Model

The system SHALL provide detailed pattern information through enhanced output fields.

#### Scenario: Store pattern-specific details

- **WHEN** outputting a detected pattern
- **THEN** the system SHALL include a `details` field containing pattern-specific information
- **AND** populate details based on pattern type:
  - Thread/Process creation: `{target: str, name: str | None}`
  - Executor creation: `{max_workers: int | None}`
  - Executor submit: `{function: str}`
  - create_task: `{coroutine: str}`
  - run_in_executor: `{executor_type: str, function: str}`

**Rationale**: Provides actionable information beyond generic statement strings

#### Scenario: Store function and class context

- **WHEN** outputting a detected pattern
- **THEN** the system SHALL include `function` field with enclosing function name or None
- **AND** include `class_name` field with enclosing class name or None
- **AND** enable users to understand where patterns occur in codebase structure

**Rationale**: Context helps understand concurrency usage patterns and potential issues

#### Scenario: Store API call information

- **WHEN** pattern involves a specific API method
- **THEN** the system SHALL include `api_call` field with method name
- **AND** use for patterns like "create_task", "submit", "run_in_executor"
- **AND** enable filtering and analysis by API method

**Rationale**: Distinguishes similar patterns using different APIs

## Implementation Notes

### Executor Mapping Structure

```python
executor_mapping: dict[str, str] = {
    'pool': 'ThreadPoolExecutor',
    'executor': 'ProcessPoolExecutor',
    # ... variable_name -> executor_type
}
```

### ConcurrencyUsage Model Updates

Add fields:

- `function: str | None = Field(None, ...)` - enclosing function
- `class_name: str | None = Field(None, ...)` - enclosing class
- `details: dict[str, Any] | None = Field(None, ...)` - pattern-specific info
- `api_call: str | None = Field(None, ...)` - API method called

### Pattern Detector Methods

Each pattern type needs a dedicated detector:

- `_detect_thread_creation(node) -> ConcurrencyUsage | None`
- `_detect_threadpool_executor(node) -> ConcurrencyUsage | None`
- `_detect_executor_submit(node, executor_mapping) -> ConcurrencyUsage | None`
- `_detect_process_creation(node) -> ConcurrencyUsage | None`
- `_detect_processpool_executor(node) -> ConcurrencyUsage | None`
- `_detect_create_task(node) -> ConcurrencyUsage | None`
- `_detect_run_in_executor(node, executor_mapping) -> ConcurrencyUsage | None`
