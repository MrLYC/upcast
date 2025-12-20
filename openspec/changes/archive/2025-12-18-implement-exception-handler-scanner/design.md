# Design: implement-exception-handler-scanner

## Architecture Overview

This scanner follows the established pattern of other scanners in the project (concurrency_pattern_scanner, prometheus_metrics_scanner) with a focus on exception handling pattern detection.

## Component Design

### 1. Handler Parser (`handler_parser.py`)

**Responsibility**: Low-level AST node parsing and data extraction

**Key Functions**:

- `parse_try_block(node: nodes.Try) -> ExceptionHandler`: Main entry point for processing try blocks
- `parse_except_clause(handler: nodes.ExceptHandler) -> ExceptionClause`: Parse individual except clauses
- `extract_exception_types(handler: nodes.ExceptHandler) -> list[str]`: Extract exception type names
- `count_logging_calls(body: list[nodes.NodeNG]) -> dict[str, int]`: Count logging calls by level
- `count_control_flow(body: list[nodes.NodeNG]) -> dict[str, int]`: Count control flow statements

**Data Structures**:

```python
@dataclass
class ExceptionClause:
    line: int
    exception_types: list[str]
    lines: int
    # Logging counts by level
    log_debug_count: int
    log_info_count: int
    log_warning_count: int
    log_error_count: int
    log_exception_count: int
    log_critical_count: int
    # Control flow counts
    pass_count: int
    return_count: int
    break_count: int
    continue_count: int
    raise_count: int

@dataclass
class BlockInfo:
    line: int
    lines: int

@dataclass
class ExceptionHandler:
    location: str  # "file.py:15-23"
    file: str
    start_line: int
    end_line: int
    try_lines: int
    except_clauses: list[ExceptionClause]
    else_clause: BlockInfo | None
    finally_clause: BlockInfo | None
```

### 2. Checker (`checker.py`)

**Responsibility**: AST traversal and aggregation

**Key Methods**:

- `visit_try(self, node: nodes.Try)`: Visit each try block using astroid visitor pattern
- `check_file(self, file_path: Path)`: Parse and visit a single file
- `get_handlers(self) -> list[ExceptionHandler]`: Return all collected handlers
- `get_summary(self) -> dict`: Calculate statistics

**Traversal Strategy**:

- Use astroid's visitor pattern (inherit from nodes.NodeVisitor)
- Visit all Try nodes in the AST
- Delegate parsing to handler_parser functions
- Collect results in a list

### 3. Export (`export.py`)

**Responsibility**: Output formatting

**Key Functions**:

- `format_handler_output(handlers: list[ExceptionHandler]) -> dict`: Convert to output structure
- Reuse `common.export.export_to_yaml()` and `export_to_json()`
- Format optional fields as null when absent

### 4. CLI (`cli.py`)

**Responsibility**: Command-line interface and orchestration

**Key Function**:

```python
@click.command()
@click.argument("path", type=click.Path(exists=True), required=False, default=".")
@click.option("-o", "--output", type=click.Path(), help="Output YAML file path")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option("--include", multiple=True, help="File patterns to include")
@click.option("--exclude", multiple=True, help="File patterns to exclude")
def scan_exception_handlers(...)
```

**Orchestration Flow**:

1. Validate path using `common.file_utils.validate_path()`
2. Collect Python files using `common.file_utils.collect_python_files()`
3. Create ExceptionHandlerChecker instance
4. Process each file with `checker.check_file()`
5. Get results and summary
6. Export to YAML/JSON using export functions

## Key Design Decisions

### 1. Anti-pattern Detection Logic

Counting Instead of Detection

**Decision**: Use counters for logging and control flow instead of boolean flags or lists

**Rationale**:

- More quantitative data: know exactly how many times each pattern occurs
- Simpler data structure: no need for lists of strings
- Easier to aggregate: sum counters across except clauses
- No subjective interpretation: just count occurrences

**Implementation**:

- Logging: `log_debug_count`, `log_info_count`, `log_warning_count`, `log_error_count`, `log_exception_count`, `log_critical_count`
- Control flow: `pass_count`, `return_count`, `break_count`, `continue_count`, `raise_count`
- All counters initialized to 0

### 2. No Anti-pattern Flagging

and count by logging level
**Decision**: Do NOT flag or classify exception handling as "anti-patterns"

**Rationale**:

- Static analysis cannot understand business logic and context
- What appears as "swallowing" may be intentional behavior
- Better to provide data and let users interpret
- Avoid false positives and subjective judgments

**Alternative Approach**:

- Provide raw statistics (bare excepts count, pass count, logging count)
- Users can query data to find patterns they care about
- Documentation can suggest patterns to watch for

### 3

**Decision**: Use pattern matching on Call nodes with logging method names

**Patterns to detect**:

- Increment appropriate level counter for each call

**Edge Cases**:

- False positives possible with non-logger objects having these methods
- Trade-off: Prefer false positives over false negatives (better to over-count)

### 4ogger.error()

LOG.error()
LOGGER.error()

```

**Implementation**:
- Check if Call node's func is Attribute
- Check if attribute name is in: debug, info, warning, error, exception, critical
- Walk up the attribute chain to find logger variable name
- Accept common logger names: logger, log, LOG, LOGGER, _logger

**Edge Cases**:
- False positives possible with non-logger objects having these methods
- Trade-off: Prefer false positives over false negatives (better to over-detect logging)

### 3. Line Count Calculation

**Decision**: Use astroid's node.lineno for accurate line counting

**Approach**:
- Try block: count from first statement to last statement in body
- Except clause: count from except line to last statement in handler body
- Else/finally: count statements in respective bodies

**Limitation**:
- Does not count blank lines or comments within blocks
- Acceptable trade-off for implementation simplicity
5
### 4. Nested Try Blocks

**Decision**: Treat each try block independently, no parent/child tracking

**Rationale**:
- Simplifies data structure and implstatistical analysis
- Can be added later if needed based on user feedback

### 6
### 5. Reuse of Common Utilities

**Decision**: Maximize reuse of `upcast.common` modules

**Reused Components**:
- `common.ast_utils`: safe_as_string, get_qualified_name for exception type resolution
- `common.file_utils`: validate_path, collect_python_files, find_package_root
- `common.export`: export_to_yaml, export_to_json, sort_dict_recursive
- `common.patterns`: match_patterns, should_exclude, DEFAULT_EXCLUDES

**Benefits**:
- Consistent behavior across all scanners
- Reduced code duplication
- Proven utility functions

## Testing Strategy

### Unit Tests (`test_handler_parser.py`)
- Test individual parsing functions in isolation
- Use minimal code snippets as input
- Verify data structure output

### Integration Tests (`test_checker.py`)
- Test full file processing
- Use fixture files with realistic patterns
- Verify aggregation and summary statistics

### CLI Tests (`test_cli.py`)
- Test command-line interface
- Test file filtering and output options
- Verify error handling

### Fixture Files
- `simple_try_except.py`: Basic patterns
- `antipatterns.py`: Swallowing patterns
- `logging_patterns.py`: Various logging styles
- `complex_handlers.py`: Nested and multi-clause patterns
- `mixed_patterns.py`: Comprehensive test case

## Performance Considerations

### Scalability
- Single-pass AST traversal per file (efficient)
- Memory usage: O(n) where n = number of exception handlers
- No global state, parallelizable if needed in future

### Optimization Opportunities
- Skip non-.py files early
- Use generator for file collection to reduce memory
- Could cache parsed ASTs if rescanning (future enhancement)

## Future Enhancements (Out of Scope)

1. **Exception chaining analysis**: Detect `raise ... from` patterns
2. **Nesting depth tracking**: Track parent/child relationships for nested try blocks
3. **Custom exception hierarchy**: Map user-defined exception classes
4. **Context manager exception suppression**: Detect `__exit__` methods that suppress
5. **Async exception patterns**: Special handling for asyncio.CancelledError, etc.
6. **Exception type coverage**: Track which exception types are caught vs raised
```
