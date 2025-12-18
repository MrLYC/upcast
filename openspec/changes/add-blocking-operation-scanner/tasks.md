# Implementation Tasks

## Phase 1: Core Infrastructure

- [ ] Create module structure `upcast/blocking_operation_scanner/`
- [ ] Create `__init__.py` with module exports
- [ ] Define data structures for blocking operations (dataclasses)

## Phase 2: Pattern Detection

- [ ] Implement `operation_parser.py` with blocking pattern detection:
  - [ ] `time.sleep()` detection
  - [ ] Django ORM `select_for_update()` detection
  - [ ] `threading.Lock().acquire()` detection
  - [ ] `subprocess.run()` detection
  - [ ] `Popen.wait()` detection
  - [ ] `Popen.communicate()` detection
- [ ] Handle import variants (e.g., `from time import sleep`)
- [ ] Extract operation context (function name, class, module)
- [ ] Extract blocking duration when available (e.g., `time.sleep(5)`)

## Phase 3: AST Checker

- [ ] Implement `checker.py` with AST traversal
- [ ] Integrate with `operation_parser.py`
- [ ] Handle method chaining (e.g., `Lock().acquire()`)
- [ ] Collect all blocking operations per file

## Phase 4: Export and CLI

- [ ] Implement `export.py`:
  - [ ] Format operations by category
  - [ ] Support YAML output
  - [ ] Support JSON output
  - [ ] Use relative file paths
- [ ] Implement `cli.py`:
  - [ ] Add `scan-blocking-operations` command
  - [ ] Support file filtering (include/exclude)
  - [ ] Support output format selection
  - [ ] Support verbose logging
- [ ] Register command in `upcast/main.py`

## Phase 5: Testing

- [ ] Create test fixtures with blocking operation examples
- [ ] Unit tests for `operation_parser.py`:
  - [ ] Test each blocking pattern detection
  - [ ] Test import variant handling
  - [ ] Test duration extraction
- [ ] Unit tests for `checker.py`:
  - [ ] Test file scanning
  - [ ] Test operation collection
- [ ] Unit tests for `export.py`:
  - [ ] Test YAML formatting
  - [ ] Test JSON formatting
- [ ] Integration tests:
  - [ ] Test CLI with various options
  - [ ] Test end-to-end scanning
  - [ ] Test file filtering
- [ ] Ensure test coverage ≥90%

## Phase 6: Documentation and Polish

- [ ] Update README.md with usage examples
- [ ] Add command to CLI help text
- [ ] Run pre-commit hooks and fix issues
- [ ] Verify all tests pass
- [ ] Performance testing (scan 1000 files)

## Validation Checklist

- [ ] All blocking patterns detected correctly
- [ ] Output format matches other scanners
- [ ] CLI follows upcast conventions
- [ ] File filtering works correctly
- [ ] Code passes ruff checks
- [ ] Test coverage ≥90%
- [ ] Documentation complete
