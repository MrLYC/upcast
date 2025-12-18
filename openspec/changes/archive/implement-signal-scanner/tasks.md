# Tasks: Implement Signal Scanner

## Module Structure & Setup

- [x] Create `upcast/signal_scanner/` directory
- [x] Create `upcast/signal_scanner/__init__.py` with exports
- [x] Create `tests/test_signal_scanner/` directory
- [x] Create `tests/test_signal_scanner/__init__.py`
- [x] Create `tests/test_signal_scanner/fixtures/` directory

## Core Detection - Django Signals

- [x] Create `upcast/signal_scanner/checker.py` with `SignalChecker` class
- [x] Implement `visit_module()` method for two-pass scanning
- [x] Implement `_collect_signal_definitions()` for custom signals (first pass)
- [x] Implement `_collect_signal_handlers()` for handlers (second pass)
- [x] Create `upcast/signal_scanner/signal_parser.py`
- [x] Implement `parse_receiver_decorator()` - detect @receiver patterns
- [x] Implement `parse_signal_connect_method()` - detect .connect() calls
- [x] Implement `parse_custom_signal_definition()` - detect Signal() assignments
- [x] Implement Django signal categorization logic (model/request/management signals)

## Core Detection - Celery Signals

- [x] Implement `parse_celery_connect_decorator()` - detect @signal.connect
- [x] Implement `parse_celery_connect_method()` - detect Celery .connect() calls
- [x] Implement Celery signal categorization logic (task/worker/beat signals)

## Handler Context & Import Tracking

- [x] Implement handler context extraction using `upcast.common.ast_utils.get_enclosing_scope()`
- [x] Add function-level context extraction (name, parameters)
- [x] Add method-level context extraction (class name, method type)
- [x] Add nested function context handling
- [x] Implement import tracking for Django signals
- [x] Implement import tracking for Celery signals
- [x] Handle import aliases correctly
- [x] Add wildcard import detection with warnings

## Aggregation & Output

- [x] Create `upcast/signal_scanner/export.py`
- [x] Implement `format_signal_output()` - group by framework and signal type
- [x] Implement handler aggregation by signal name
- [x] Implement handler count statistics
- [x] Implement unused custom signal detection
- [x] Implement `export_to_yaml()` with hierarchical structure
- [x] Test YAML output format matches specification

## CLI Interface

- [x] Create `upcast/signal_scanner/cli.py`
- [x] Implement `scan_signals()` command with Click decorators
- [x] Add `--output` option for file export
- [x] Add `--verbose` option for detailed output
- [x] Add `--include` option for file patterns (repeatable)
- [x] Add `--exclude` option for file patterns (repeatable)
- [x] Add `--no-default-excludes` flag
- [x] Implement file collection using `upcast.common.file_utils`
- [x] Add stdout summary output (signal counts by framework)
- [x] Write comprehensive help text with examples
- [x] Integrate into `upcast/main.py` as `scan-signals` subcommand

## Test Fixtures

- [x] Create `tests/test_signal_scanner/fixtures/django_signals.py`
  - @receiver with single signal
  - @receiver with multiple signals
  - .connect() method calls
  - Various sender specifications
- [x] Create `tests/test_signal_scanner/fixtures/celery_signals.py`
  - @signal.connect decorator patterns
  - .connect() method calls
  - Task signals (prerun, postrun, failure, retry)
  - Worker signals
- [x] Create `tests/test_signal_scanner/fixtures/custom_signals.py`
  - Custom Signal() definitions
  - Custom signals with handlers
  - Unused custom signals
- [x] Create `tests/test_signal_scanner/fixtures/mixed_signals.py`
  - Combined Django and Celery patterns
  - Class methods as handlers
  - Nested function handlers
  - Import aliases

## Unit Tests

- [x] Create `tests/test_signal_scanner/test_signal_parser.py`
- [x] Test `parse_receiver_decorator()` with various patterns
- [x] Test `parse_signal_connect_method()` for both frameworks
- [x] Test `parse_custom_signal_definition()` with different Signal() forms
- [x] Test `parse_celery_connect_decorator()`
- [x] Test handler context extraction for functions, methods, nested
- [x] Test import tracking and alias resolution
- [x] Target: 12-15 unit tests covering all parsing functions

## Integration Tests

- [x] Create `tests/test_signal_scanner/test_integration.py`
- [x] Test end-to-end Django signal scanning
- [x] Test end-to-end Celery signal scanning
- [x] Test mixed framework scanning
- [x] Test handler aggregation by signal name
- [x] Test import resolution with aliases
- [x] Test custom signal detection and unused signal flagging
- [x] Test multiple files with cross-references
- [x] Test empty file handling
- [x] Target: 8-10 integration tests

## CLI Tests

- [x] Create `tests/test_signal_scanner/test_cli.py`
- [x] Test basic scan command execution
- [x] Test `--output` option creates file
- [x] Test `--verbose` option shows details
- [x] Test `--include` pattern filtering
- [x] Test `--exclude` pattern filtering
- [x] Test `--no-default-excludes` flag
- [x] Test multiple include/exclude patterns
- [x] Test error handling for nonexistent paths
- [x] Test YAML output format validation
- [x] Test stdout summary format
- [x] Target: 10-12 CLI tests

## Validation & Documentation

- [x] Run `uv run pytest tests/test_signal_scanner/ -v` - ensure all pass (35/35 tests passing)
- [x] Run `uv run ruff check upcast/signal_scanner/` - fix all issues (code quality verified)
- [x] Run `uv run pre-commit run --all-files` - ensure clean
- [x] Test manual command: `uv run upcast scan-signals .`
- [x] Test manual command with options: `uv run upcast scan-signals . -o signals.yaml -v`
- [x] Verify YAML output structure matches examples
- [x] Update OpenSpec tasks.md with completion status

## Notes

**Dependencies:**

- Requires `upcast.common.ast_utils` for context extraction
- Requires `upcast.common.file_utils` for file collection
- Requires `upcast.common.export` utilities for YAML formatting

**Test Targets:**

- Total tests: ~35-40 tests
- Pattern: 12-15 unit + 8-10 integration + 10-12 CLI + 3-5 export tests

**Implementation Order:**

1. Module structure and Django signal detection first (highest value)
2. Celery signal detection second
3. Advanced features (import tracking, context) third
4. CLI and tests throughout (parallel with implementation)
5. Final validation and integration last

**Parallelizable Work:**

- Fixture creation can happen alongside parser implementation
- Unit tests can be written as each parse function is completed
- CLI tests can be written after CLI interface is stable
