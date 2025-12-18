# concurrency-pattern-scanner Specification

## Purpose

TBD - created by archiving change implement-concurrency-scanner. Update Purpose after archive.

## Requirements

### Requirement: Asyncio Pattern Detection

The system SHALL detect asyncio-based concurrency patterns including async functions, await expressions, and asyncio API calls.

#### Scenario: Detect async function definitions

- **WHEN** scanning a Python file containing `async def` functions
- **THEN** the system SHALL identify each async function definition
- **AND** extract the function name, file path, and line number
- **AND** categorize it under `asyncio.async_functions`

**DIFF**: New requirement for detecting asyncio coroutines

#### Scenario: Detect await expressions

- **WHEN** scanning async functions
- **THEN** the system SHALL identify `await` expressions
- **AND** extract the awaited expression details
- **AND** record the enclosing function context
- **AND** categorize under `asyncio.await_expressions`

**DIFF**: Detect await usage patterns

#### Scenario: Detect asyncio.gather patterns

- **WHEN** scanning for concurrent execution patterns
- **THEN** the system SHALL identify `asyncio.gather()` calls
- **AND** extract the list of concurrent tasks
- **AND** handle both `asyncio.gather` and `from asyncio import gather` forms
- **AND** categorize under `asyncio.gather_patterns`

**DIFF**: Detect gather-based concurrent execution

#### Scenario: Detect asyncio.create_task patterns

- **WHEN** scanning for task creation
- **THEN** the system SHALL identify `asyncio.create_task()` calls
- **AND** extract the coroutine being scheduled
- **AND** categorize under `asyncio.task_creation`

**DIFF**: Detect task-based concurrency

#### Scenario: Detect async context managers

- **WHEN** scanning for async resource management
- **THEN** the system SHALL identify `async with` statements
- **AND** extract the async context manager expression
- **AND** categorize under `asyncio.async_context_managers`

**DIFF**: Detect async with patterns

### Requirement: Threading Pattern Detection

The system SHALL detect threading-based concurrency patterns including Thread creation and ThreadPoolExecutor usage.

#### Scenario: Detect threading.Thread creation

- **WHEN** scanning for thread-based concurrency
- **THEN** the system SHALL identify `threading.Thread()` instantiations
- **AND** extract the target function or callable
- **AND** extract thread name if specified
- **AND** categorize under `threading.thread_creation`

**DIFF**: Detect manual thread creation

#### Scenario: Detect ThreadPoolExecutor creation

- **WHEN** scanning for thread pool patterns
- **THEN** the system SHALL identify `ThreadPoolExecutor()` instantiations
- **AND** extract the `max_workers` parameter if present
- **AND** track the executor variable name for resolution
- **AND** categorize under `threading.thread_pool_executors`

**DIFF**: Detect thread pool executor definitions

#### Scenario: Detect thread pool submit calls

- **WHEN** scanning for executor task submission
- **THEN** the system SHALL identify calls to `executor.submit()`
- **AND** resolve the executor variable to ThreadPoolExecutor
- **AND** extract the submitted function/callable
- **AND** categorize under `threading.executor_submissions`

**DIFF**: Detect thread pool task submissions

### Requirement: Multiprocessing Pattern Detection

The system SHALL detect multiprocessing-based concurrency patterns including Process creation and ProcessPoolExecutor usage.

#### Scenario: Detect multiprocessing.Process creation

- **WHEN** scanning for process-based concurrency
- **THEN** the system SHALL identify `multiprocessing.Process()` instantiations
- **AND** extract the target function or callable
- **AND** extract process name if specified
- **AND** categorize under `multiprocessing.process_creation`

**DIFF**: Detect manual process creation

#### Scenario: Detect ProcessPoolExecutor creation

- **WHEN** scanning for process pool patterns
- **THEN** the system SHALL identify `ProcessPoolExecutor()` instantiations
- **AND** extract the `max_workers` parameter if present
- **AND** track the executor variable name for resolution
- **AND** categorize under `multiprocessing.process_pool_executors`

**DIFF**: Detect process pool executor definitions

#### Scenario: Detect process pool submit calls

- **WHEN** scanning for executor task submission
- **THEN** the system SHALL identify calls to `executor.submit()`
- **AND** resolve the executor variable to ProcessPoolExecutor
- **AND** extract the submitted function/callable
- **AND** categorize under `multiprocessing.executor_submissions`

**DIFF**: Detect process pool task submissions

### Requirement: Executor Bridge Pattern Detection

The system SHALL detect asyncio-executor bridge patterns using `loop.run_in_executor()`.

#### Scenario: Detect run_in_executor with ThreadPoolExecutor

- **WHEN** scanning for asyncio-thread bridges
- **THEN** the system SHALL identify `loop.run_in_executor()` calls
- **AND** resolve the first argument to determine executor type
- **AND** classify as ThreadPoolExecutor when applicable
- **AND** extract the target function/callable
- **AND** categorize under `threading.run_in_executor`

**DIFF**: Detect asyncio-threading bridges

#### Scenario: Detect run_in_executor with ProcessPoolExecutor

- **WHEN** scanning for asyncio-process bridges
- **THEN** the system SHALL identify `loop.run_in_executor()` calls
- **AND** resolve the first argument to determine executor type
- **AND** classify as ProcessPoolExecutor when applicable
- **AND** extract the target function/callable
- **AND** categorize under `multiprocessing.run_in_executor`

**DIFF**: Detect asyncio-multiprocessing bridges

#### Scenario: Handle unresolved executors

- **WHEN** executor type cannot be determined statically
- **THEN** the system SHALL mark executor as `<unknown-executor>`
- **AND** still record the run_in_executor usage
- **AND** include in output with unknown executor marker

**DIFF**: Handle dynamic executor resolution

### Requirement: Context Extraction

The system SHALL extract contextual information for each detected concurrency pattern.

#### Scenario: Extract file location and line number

- **WHEN** detecting any concurrency pattern
- **THEN** the system SHALL record the file path (relative to project root)
- **AND** record the line number where the pattern appears
- **AND** include both in the pattern output

**DIFF**: Location tracking for all patterns

#### Scenario: Extract function context

- **WHEN** pattern appears inside a function
- **THEN** the system SHALL extract the enclosing function name
- **AND** include it in the pattern output as `function` field
- **AND** handle nested functions correctly

**DIFF**: Function context extraction

#### Scenario: Extract class context

- **WHEN** pattern appears inside a class method
- **THEN** the system SHALL extract the enclosing class name
- **AND** include it in the pattern output as `class` field
- **AND** combine with function name (e.g., `ClassName.method_name`)

**DIFF**: Class context extraction

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
