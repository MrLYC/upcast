# Tasks: implement-exception-handler-scanner

## Implementation Tasks

### Phase 1: Foundation (Core Infrastructure)

- [ ] **Create module structure**: Create `upcast/exception_handler_scanner/` directory with `__init__.py`, `cli.py`, `checker.py`, `handler_parser.py`, `export.py`

  - Establishes basic module layout following project conventions
  - Defines public API exports in `__init__.py`
  - Reuses common utilities from `upcast.common`

- [ ] **Define data structures**: Create dataclasses in `handler_parser.py`:

  - `ExceptionClause`: exception_types, line, lines, log_debug_count, log_info_count, log_warning_count, log_error_count, log_exception_count, log_critical_count, pass_count, return_count, break_count, continue_count, raise_count
  - `ExceptionHandler`: location, file, start_line, end_line, try_lines, except_clauses, else_clause, finally_clause
  - `BlockInfo`: line, lines (for else/finally blocks)
  - Use dataclasses following patterns from other scanners

- [ ] **Create test structure**: Set up `tests/test_exception_handler_scanner/` with:

  - `__init__.py`
  - `test_handler_parser.py` (tests for parsing logic)
  - `test_checker.py` (tests for aggregation)
  - `test_cli.py` (tests for CLI)
  - `test_export.py` (tests for YAML output)
  - `fixtures/` directory

- [ ] **Create basic test fixtures**: Add to `fixtures/`:
  - `simple_try_except.py`: Basic try/except patterns
  - `control_flow_patterns.py`: Various control flow statements (pass, return, break, continue, raise)
  - `logging_patterns.py`: Various logging levels and formats
  - `complex_handlers.py`: Nested try blocks, multiple except clauses

### Phase 2: Parser Layer (Exception Handler Extraction)

- [ ] **Implement try block detection**: Create `handler_parser.py` with:

  - `parse_try_block(node: nodes.Try) -> ExceptionHandler`
  - Extract try block location and line count
  - Identify file path and line range
  - Initialize handler structure

- [ ] **Implement except clause parsing**: Add to `handler_parser.py`:

  - `parse_except_clause(handler: nodes.ExceptHandler) -> ExceptionClause`
  - Extract exception types (handle Name, Tuple, bare except)
  - Calculate except block line count
  - Extract location information

- [ ] **Implement exception type extraction**: Add helper function:

  - `extract_exception_types(handler: nodes.ExceptHandler) -> list[str]`
  - Handle single exception: `except ValueError:`
  - Handle tuple of exceptions: `except (ValueError, KeyError):`
  - Handle bare except: `except:`
  - Use `get_qualified_name()` from common.ast_utils

- [ ] **Test exception handler parsing**: Write tests in `test_handler_parser.py`
  - Test single exception type extraction
  - Test multiple exception types (tuple)
  - Test bare except detection
  - Test line count calculation
  - Test location formatting
  - Verify with `uv run pytest tests/test_exception_handler_scanner/test_handler_parser.py`

### Phase 3: Logging Counting

- [ ] **Implement logging counting**: Add to `handler_parser.py`:

  - `count_logging_calls(body: list[nodes.NodeNG]) -> dict[str, int]`
  - Scan except block body for logging calls
  - Count calls by level: debug, info, warning, error, exception, critical
  - Return dictionary with counts for each level
  - Initialize all counters to 0

- [ ] **Handle logging patterns**: Support various logging styles:

  - `logger.error()`, `logger.exception()`, `logging.error()`
  - `self.logger.error()`, `cls.logger.error()`
  - Module-level logger: `LOG.error()`, `LOGGER.error()`
  - Check both direct calls and attribute access chains

- [ ] **Test logging counting**: Extend `test_handler_parser.py`
  - Test error level counting
  - Test exception level counting
  - Test all six log levels (debug, info, warning, error, exception, critical)
  - Test various logger variable names
  - Test multiple calls in same except block
  - Test no logging case (all counts = 0)
  - Verify with fixtures/logging_patterns.py

### Phase 4: Control Flow Counting

- [ ] **Implement control flow counting**: Add to `handler_parser.py`:

  - `count_control_flow(body: list[nodes.NodeNG]) -> dict[str, int]`
  - Count Pass nodes
  - Count Return nodes
  - Count Break nodes
  - Count Continue nodes
  - Count Raise nodes
  - Return dictionary with counts for each type
  - Initialize all counters to 0

- [ ] **Test control flow counting**: Extend `test_handler_parser.py`
  - Test pass counting
  - Test return counting
  - Test raise counting
  - Test break and continue counting
  - Test multiple statements in same except block
  - Test with fixtures/control_flow_patterns.py
  - Verify all counts are accurate

### Phase 5: Else and Finally Clause Support

- [ ] **Implement else clause parsing**: Add to `handler_parser.py`:

  - `parse_else_clause(node: nodes.Try) -> BlockInfo | None`
  - Check if `node.orelse` exists and is non-empty
  - Calculate line count
  - Extract line number

- [ ] **Implement finally clause parsing**: Add to `handler_parser.py`:

  - `parse_finally_clause(node: nodes.Try) -> BlockInfo | None`
  - Check if `node.finalbody` exists and is non-empty
  - Calculate line count
  - Extract line number

- [ ] **Test else/finally parsing**: Extend `test_handler_parser.py`
  - Test try/except/else structure
  - Test try/except/finally structure
  - Test try/except/else/finally structure
  - Test None when clauses absent
  - Verify line counts

### Phase 6: Checker Layer (Aggregation)

- [ ] **Implement ExceptionHandlerChecker**: Create `checker.py` with:

  - `__init__(self, base_path: Path)`: Initialize with handlers list
  - `visit_try(self, node: nodes.Try) -> None`: Visit each try block
  - `check_file(self, file_path: Path) -> None`: Process single file
  - `get_handlers(self) -> list[ExceptionHandler]`: Return all handlers
  - `get_summary(self) -> dict`: Calculate statistics

- [ ] **Implement summary statistics**: Add to `checker.py`:

  - Count total try blocks
  - Count total except clauses
  - Count except clauses with logging (any level > 0)
  - Count except clauses with pass statements
  - Count bare except clauses (empty exception_types)

- [ ] **Create complex test fixtures**: Add `fixtures/mixed_patterns.py`

  - Mix try/except/else/finally
  - Multiple except clauses per try
  - Nested try blocks
  - Various logging and control flow combinations

- [ ] **Test checker aggregation**: Write `test_checker.py`
  - Test single-file processing
  - Test multi-file aggregation
  - Test summary statistics calculation
  - Test nested try block handling
  - Verify with `uv run pytest tests/test_exception_handler_scanner/test_checker.py`

### Phase 7: Export Layer (YAML Output)

- [ ] **Implement YAML export functions**: Create `export.py` with:

  - `format_handler_output(handlers: list[ExceptionHandler]) -> dict`: Convert to output structure
  - `format_exception_clause(clause: ExceptionClause) -> dict`: Format except clause
  - Use common.export functions: export_to_yaml, export_to_json
  - Follow formatting standards (2-space indent, UTF-8)

- [ ] **Implement output formatting**: Handle structure:

  - Format exception_handlers list with all fields
  - Include summary section with statistics
  - Sort handlers by location
  - Format optional fields (else_clause, finally_clause can be null)

- [ ] **Test YAML export**: Write `test_export.py`
  - Test output structure matches spec examples
  - Test all required and optional fields (including all count fields)
  - Test null handling for else/finally
  - Test log level counts
  - Test control flow counts
  - Test summary section
  - Verify with `uv run pytest tests/test_exception_handler_scanner/test_export.py`

### Phase 8: CLI Layer (Integration)

- [ ] **Implement CLI entry point**: Create `cli.py` with:

  - `scan_exception_handlers(path: str, output: str | None, verbose: bool, include: tuple, exclude: tuple) -> None`
  - Use common.file_utils.validate_path() and collect_python_files()
  - Orchestrate ExceptionHandlerChecker
  - Call export functions
  - Error handling and verbose logging

- [ ] **Add filtering options**: Support CLI flags:

  - `--include`: File patterns to include
  - `--exclude`: File patterns to exclude
  - Use common.patterns functions for filtering
  - Follow patterns from other scanners

- [ ] **Implement Click command decorator**: Add CLI decorators:

  - `@click.command()`
  - Path argument with default="."
  - `-o/--output` option
  - `-v/--verbose` flag
  - `--include` multiple option
  - `--exclude` multiple option
  - Follow CLI patterns from concurrency_pattern_scanner

- [ ] **Test CLI functions**: Write `test_cli.py`
  - Test directory scanning
  - Test single file scanning
  - Test output to stdout vs file
  - Test verbose mode
  - Test include/exclude patterns
  - Test error handling (nonexistent path)
  - Verify with `uv run pytest tests/test_exception_handler_scanner/test_cli.py`

### Phase 9: Integration & Documentation

- [ ] **Add CLI integration to main**: Update `upcast/main.py`

  - Register `scan-exception-handlers` command
  - Wire up to `scan_exception_handlers()` function
  - Add command docstring with examples
  - Follow pattern from other scanner commands

- [ ] **Update CLI interface spec**: Modify `openspec/specs/cli-interface/spec.md`

  - Add scenario for scan-exception-handlers command
  - Document standard options support
  - Add to consistent command naming requirement

- [ ] **Run full test suite**: Execute all tests

  - `uv run pytest tests/test_exception_handler_scanner/ -v`
  - Verify 85%+ test coverage
  - Fix any failing tests

- [ ] **Update README**: Document new scanner capability

  - Add usage examples for CLI
  - Show sample output YAML with count fields
  - Explain logging and control flow counting
  - Link to spec document

- [ ] **Validate code quality**: Ensure compliance
  - Run `uv run ruff check upcast/exception_handler_scanner/`
  - Fix any linting issues
  - Run pre-commit hooks
  - Verify PEP8 compliance

## Validation Checkpoints

After each phase:

1. Run relevant tests: `uv run pytest tests/test_exception_handler_scanner/`
2. Check code style: `uv run ruff check upcast/exception_handler_scanner/`
3. Verify no regressions: `uv run pytest`

Final validation:

1. End-to-end test with real project containing exception handlers
2. Verify YAML output matches spec examples
3. Check test coverage: `uv run pytest --cov=upcast.exception_handler_scanner --cov-report=term-missing`
4. Run OpenSpec validation: `uv run openspec validate implement-exception-handler-scanner --strict`
