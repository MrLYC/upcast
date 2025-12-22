# concurrency-pattern-scanner Specification

## Purpose

TBD - created by archiving change implement-concurrency-scanner. Update Purpose after archive.

## Requirements

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

### Requirement: Executor Variable Resolution

The system SHALL resolve executor variables to determine their types for run_in_executor calls.

#### Scenario: Build executor type mapping

- **WHEN** scanning a module
- **THEN** the system SHALL perform a first pass to collect executor definitions
- **AND** build a mapping of variable names to executor types
- **AND** track both module-level and function-level executors

**DIFF**: Two-pass executor resolution

#### Scenario: Resolve executor in run_in_executor calls

- **WHEN** encountering a `run_in_executor` call
- **THEN** the system SHALL look up the executor variable name in the mapping
- **AND** determine if it's ThreadPoolExecutor or ProcessPoolExecutor
- **AND** use the resolved type for categorization

**DIFF**: Dynamic executor type resolution

#### Scenario: Handle unresolvable executor references

- **WHEN** executor variable cannot be found in mapping
- **THEN** the system SHALL mark the executor as `<unknown-executor>`
- **AND** include a note in the pattern details
- **AND** still record the usage for visibility

**DIFF**: Graceful handling of resolution failures

### Requirement: Pattern Details Extraction

The system SHALL extract detailed information about each concurrency pattern usage.

#### Scenario: Extract code snippet

- **WHEN** detecting a concurrency pattern
- **THEN** the system SHALL extract a simplified code snippet
- **AND** limit snippet length to avoid excessive output
- **AND** include the snippet in the `details` field

**DIFF**: Code snippet extraction

#### Scenario: Extract API call names

- **WHEN** pattern involves a specific API call
- **THEN** the system SHALL extract the API function name
- **AND** record it in the `api_call` field
- **AND** handle both direct calls and imported aliases

**DIFF**: API call tracking

#### Scenario: Simplify complex expressions

- **WHEN** pattern contains complex comprehensions or nested calls
- **THEN** the system SHALL simplify the expression for display
- **AND** preserve the essential pattern structure
- **AND** indicate simplification with ellipsis where appropriate

**DIFF**: Expression simplification for readability

### Requirement: YAML Output Formatting

The system SHALL generate structured YAML output grouped by concurrency category and pattern type.

#### Scenario: Group patterns by concurrency type

- **WHEN** generating output
- **THEN** the system SHALL create top-level categories for asyncio, threading, and multiprocessing
- **AND** group patterns within each category by specific pattern type
- **AND** maintain consistent structure across categories

**DIFF**: Hierarchical output structure

#### Scenario: Format pattern entries

- **WHEN** formatting individual patterns
- **THEN** the system SHALL include file, line, function, details fields
- **AND** include optional fields (class, api_call, executor_type) when available
- **AND** sort entries by file and line number for consistency

**DIFF**: Consistent pattern formatting

#### Scenario: Handle empty categories

- **WHEN** no patterns detected for a category
- **THEN** the system SHALL omit that category from output
- **AND** avoid empty dictionaries or null values
- **AND** maintain clean, minimal output

**DIFF**: Clean output for empty results

### Requirement: CLI Integration

The system SHALL provide a `scan-concurrency-patterns` command integrated with the main CLI.

#### Scenario: Add scan-concurrency-patterns command

- **WHEN** user needs to scan for Python concurrency patterns
- **THEN** the system SHALL provide `scan-concurrency-patterns` command
- **AND** accept a path argument (file or directory)
- **AND** follow standard CLI patterns from other scanners

**DIFF**: New CLI command for concurrency scanning

#### Scenario: Support standard CLI options

- **WHEN** running scan-concurrency-patterns
- **THEN** the system SHALL support `-o/--output` for file output
- **AND** support `-v/--verbose` for debug information
- **AND** support `--include` and `--exclude` for file filtering
- **AND** support `--no-default-excludes` flag

**DIFF**: Standard CLI option support

#### Scenario: Handle path validation

- **WHEN** invalid path provided
- **THEN** the system SHALL validate the path exists
- **AND** return clear error message for nonexistent paths
- **AND** exit gracefully without stack trace

**DIFF**: Path validation and error handling

### Requirement: Error Recovery

The system SHALL handle errors gracefully and continue scanning when possible.

#### Scenario: Handle parse errors

- **WHEN** a file has syntax errors or cannot be parsed
- **THEN** the system SHALL log a warning (if verbose)
- **AND** skip the problematic file
- **AND** continue scanning remaining files

**DIFF**: Graceful parse error handling

#### Scenario: Handle resolution failures

- **WHEN** executor type cannot be resolved
- **THEN** the system SHALL mark as unresolved
- **AND** include the pattern in output with marker
- **AND** continue processing other patterns

**DIFF**: Graceful resolution failure handling

#### Scenario: Handle I/O errors

- **WHEN** file read fails
- **THEN** the system SHALL log error message
- **AND** continue with next file
- **AND** return partial results if any files succeeded

**DIFF**: I/O error recovery

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
