# Tasks: Implement Signal Scanner

## Module Structure & Setup

- [ ] Create `upcast/signal_scanner/` directory
- [ ] Create `upcast/signal_scanner/__init__.py` with exports
- [ ] Create `tests/test_signal_scanner/` directory
- [ ] Create `tests/test_signal_scanner/__init__.py`
- [ ] Create `tests/test_signal_scanner/fixtures/` directory

## Core Detection - Django Signals

- [ ] Create `upcast/signal_scanner/checker.py` with `SignalChecker` class
- [ ] Implement `visit_module()` method for two-pass scanning
- [ ] Implement `_collect_signal_definitions()` for custom signals (first pass)
- [ ] Implement `_collect_signal_handlers()` for handlers (second pass)
- [ ] Create `upcast/signal_scanner/signal_parser.py`
- [ ] Implement `parse_receiver_decorator()` - detect @receiver patterns
- [ ] Implement `parse_signal_connect_method()` - detect .connect() calls
- [ ] Implement `parse_custom_signal_definition()` - detect Signal() assignments
- [ ] Implement Django signal categorization logic (model/request/management signals)

## Core Detection - Celery Signals

- [ ] Implement `parse_celery_connect_decorator()` - detect @signal.connect
- [ ] Implement `parse_celery_connect_method()` - detect Celery .connect() calls
- [ ] Implement Celery signal categorization logic (task/worker/beat signals)

## Handler Context & Import Tracking

- [ ] Implement handler context extraction using `upcast.common.ast_utils.get_enclosing_scope()`
- [ ] Add function-level context extraction (name, parameters)
- [ ] Add method-level context extraction (class name, method type)
- [ ] Add nested function context handling
- [ ] Implement import tracking for Django signals
- [ ] Implement import tracking for Celery signals
- [ ] Handle import aliases correctly
- [ ] Add wildcard import detection with warnings

## Aggregation & Output

- [ ] Create `upcast/signal_scanner/export.py`
- [ ] Implement `format_signal_output()` - group by framework and signal type
- [ ] Implement handler aggregation by signal name
- [ ] Implement handler count statistics
- [ ] Implement unused custom signal detection
- [ ] Implement `export_to_yaml()` with hierarchical structure
- [ ] Test YAML output format matches specification

## CLI Interface

- [ ] Create `upcast/signal_scanner/cli.py`
- [ ] Implement `scan_signals()` command with Click decorators
- [ ] Add `--output` option for file export
- [ ] Add `--verbose` option for detailed output
- [ ] Add `--include` option for file patterns (repeatable)
- [ ] Add `--exclude` option for file patterns (repeatable)
- [ ] Add `--no-default-excludes` flag
- [ ] Implement file collection using `upcast.common.file_utils`
- [ ] Add stdout summary output (signal counts by framework)
- [ ] Write comprehensive help text with examples
- [ ] Integrate into `upcast/main.py` as `scan-signals` subcommand

## Test Fixtures

- [ ] Create `tests/test_signal_scanner/fixtures/django_signals.py`
  - @receiver with single signal
  - @receiver with multiple signals
  - .connect() method calls
  - Various sender specifications
- [ ] Create `tests/test_signal_scanner/fixtures/celery_signals.py`
  - @signal.connect decorator patterns
  - .connect() method calls
  - Task signals (prerun, postrun, failure, retry)
  - Worker signals
- [ ] Create `tests/test_signal_scanner/fixtures/custom_signals.py`
  - Custom Signal() definitions
  - Custom signals with handlers
  - Unused custom signals
- [ ] Create `tests/test_signal_scanner/fixtures/mixed_signals.py`
  - Combined Django and Celery patterns
  - Class methods as handlers
  - Nested function handlers
  - Import aliases

## Unit Tests

- [ ] Create `tests/test_signal_scanner/test_signal_parser.py`
- [ ] Test `parse_receiver_decorator()` with various patterns
- [ ] Test `parse_signal_connect_method()` for both frameworks
- [ ] Test `parse_custom_signal_definition()` with different Signal() forms
- [ ] Test `parse_celery_connect_decorator()`
- [ ] Test handler context extraction for functions, methods, nested
- [ ] Test import tracking and alias resolution
- [ ] Target: 12-15 unit tests covering all parsing functions

## Integration Tests

- [ ] Create `tests/test_signal_scanner/test_integration.py`
- [ ] Test end-to-end Django signal scanning
- [ ] Test end-to-end Celery signal scanning
- [ ] Test mixed framework scanning
- [ ] Test handler aggregation by signal name
- [ ] Test import resolution with aliases
- [ ] Test custom signal detection and unused signal flagging
- [ ] Test multiple files with cross-references
- [ ] Test empty file handling
- [ ] Target: 8-10 integration tests

## CLI Tests

- [ ] Create `tests/test_signal_scanner/test_cli.py`
- [ ] Test basic scan command execution
- [ ] Test `--output` option creates file
- [ ] Test `--verbose` option shows details
- [ ] Test `--include` pattern filtering
- [ ] Test `--exclude` pattern filtering
- [ ] Test `--no-default-excludes` flag
- [ ] Test multiple include/exclude patterns
- [ ] Test error handling for nonexistent paths
- [ ] Test YAML output format validation
- [ ] Test stdout summary format
- [ ] Target: 10-12 CLI tests

## Validation & Documentation

- [ ] Run `uv run pytest tests/test_signal_scanner/ -v` - ensure all pass
- [ ] Run `uv run ruff check upcast/signal_scanner/` - fix all issues
- [ ] Run `uv run pre-commit run --all-files` - ensure clean
- [ ] Test manual command: `uv run upcast scan-signals .`
- [ ] Test manual command with options: `uv run upcast scan-signals . -o signals.yaml -v`
- [ ] Verify YAML output structure matches examples
- [ ] Update OpenSpec tasks.md with completion status

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
