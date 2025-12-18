# Implementation Tasks

## Phase 1: Core Infrastructure

- [x] Create module structure `upcast/blocking_operation_scanner/`
- [x] Create `__init__.py` with module exports
- [x] Define data structures for blocking operations (dataclasses)

## Phase 2: Pattern Detection

- [x] Implement `operation_parser.py` with blocking pattern detection:
  - [x] `time.sleep()` detection
  - [x] Django ORM `select_for_update()` detection
  - [x] `threading.Lock().acquire()` detection
  - [x] `subprocess.run()` detection
  - [x] `Popen.wait()` detection
  - [x] `Popen.communicate()` detection
- [x] Handle import variants (e.g., `from time import sleep`)
- [x] Extract operation context (function name, class, module)
- [x] Extract blocking duration when available (e.g., `time.sleep(5)`)

## Phase 3: AST Checker

- [x] Implement `checker.py` with AST traversal
- [x] Integrate with `operation_parser.py`
- [x] Handle method chaining (e.g., `Lock().acquire()`)
- [x] Collect all blocking operations per file

## Phase 4: Export and CLI

- [x] Implement `export.py`:
  - [x] Format operations by category
  - [x] Support YAML output
  - [x] Support JSON output
  - [x] Use relative file paths
- [x] Implement `cli.py`:
  - [x] Add `scan-blocking-operations` command
  - [x] Support file filtering (include/exclude)
  - [x] Support output format selection
  - [x] Support verbose logging
- [x] Register command in `upcast/main.py`

## Phase 5: Testing

- [x] Create test fixtures with blocking operation examples
- [x] Unit tests for `operation_parser.py`:
  - [x] Test each blocking pattern detection
  - [x] Test import variant handling
  - [x] Test duration extraction
- [x] Unit tests for `checker.py`:
  - [x] Test file scanning
  - [x] Test operation collection
- [x] Unit tests for `export.py`:
  - [x] Test YAML formatting
  - [x] Test JSON formatting
- [x] Integration tests:
  - [x] Test CLI with various options
  - [x] Test end-to-end scanning
  - [x] Test file filtering
- [x] Ensure test coverage ≥90%

## Phase 6: Documentation and Polish

- [x] Update README.md with usage examples
- [x] Add command to CLI help text
- [x] Run pre-commit hooks and fix issues
- [x] Verify all tests pass
- [ ] Performance testing (scan 1000 files) - deferred for post-implementation

## Validation Checklist

- [x] All blocking patterns detected correctly
- [x] Output format matches other scanners
- [x] CLI follows upcast conventions
- [x] File filtering works correctly
- [x] Code passes ruff checks
- [x] Test coverage ≥90% (26/26 tests passing)
- [x] Documentation complete
