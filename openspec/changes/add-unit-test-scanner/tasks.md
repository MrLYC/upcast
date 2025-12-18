# Implementation Tasks

## 1. Specification

- [ ] 1.1 Create spec delta in `specs/unit-test-scanner/spec.md`
- [ ] 1.2 Define output format requirements and scenarios
- [ ] 1.3 Define test detection rules (pytest, unittest)
- [ ] 1.4 Define target resolution logic (root_modules matching)
- [ ] 1.5 Validate spec with `openspec validate add-unit-test-scanner --strict`

## 2. CLI Interface

- [ ] 2.1 Add `scan-unit-tests` command to `upcast/main.py`
- [ ] 2.2 Add CLI options: path, --root-modules, -o/--output, --format, --include, --exclude
- [ ] 2.3 Implement help text and examples
- [ ] 2.4 Test CLI with `upcast scan-unit-tests --help`

## 3. Core Implementation

- [ ] 3.1 Create `upcast/unit_test_scanner/__init__.py`
- [ ] 3.2 Implement `test_parser.py` with parse_test_function()
  - [ ] Extract function name, location, and body
  - [ ] Calculate MD5 of normalized function body
  - [ ] Count assert statements (pytest, unittest)
  - [ ] Extract imports and usage references
- [ ] 3.3 Implement `checker.py` with UnitTestChecker AST visitor
  - [ ] Detect pytest test functions (starts with test\_)
  - [ ] Detect unittest TestCase methods
  - [ ] Track imports and resolve module references
  - [ ] Match used symbols against root_modules
- [ ] 3.4 Implement target resolution in `test_parser.py`
  - [ ] Analyze function body for Name and Attribute nodes
  - [ ] Check if referenced modules match root_modules prefixes
  - [ ] Group targets by module path
- [ ] 3.5 Implement `export.py` with format_test_output()
  - [ ] Group tests by file
  - [ ] Sort by file path and line number
  - [ ] Use common.export functions

## 4. CLI Entry Point

- [ ] 4.1 Create `cli.py` with scan_unit_tests() function
- [ ] 4.2 Integrate with common.file_utils.collect_python_files()
- [ ] 4.3 Support --include and --exclude patterns
- [ ] 4.4 Handle single files and directories
- [ ] 4.5 Support output to file or stdout

## 5. Testing

- [ ] 5.1 Create `tests/test_unit_test_scanner/test_cli.py`
  - [ ] Test command registration
  - [ ] Test path validation
  - [ ] Test output file creation
- [ ] 5.2 Create `tests/test_unit_test_scanner/test_test_parser.py`
  - [ ] Test pytest function parsing
  - [ ] Test unittest method parsing
  - [ ] Test assert counting
  - [ ] Test MD5 calculation
  - [ ] Test target resolution
- [ ] 5.3 Create `tests/test_unit_test_scanner/test_checker.py`
  - [ ] Test AST visitor for test detection
  - [ ] Test import tracking
  - [ ] Test root_modules filtering
- [ ] 5.4 Create `tests/test_unit_test_scanner/test_export.py`
  - [ ] Test YAML output format
  - [ ] Test JSON output format
  - [ ] Test output sorting
- [ ] 5.5 Create `tests/test_unit_test_scanner/test_integration.py`
  - [ ] Test end-to-end with fixtures
  - [ ] Test with example from product context
  - [ ] Test multiple files
- [ ] 5.6 Create test fixtures in `tests/test_unit_test_scanner/fixtures/`

## 6. Documentation

- [ ] 6.1 Add docstrings to all public functions
- [ ] 6.2 Add module-level documentation
- [ ] 6.3 Update README if needed

## 7. Code Quality

- [ ] 7.1 Run `uv run ruff check` and fix issues
- [ ] 7.2 Run `uv run pytest` and ensure all tests pass
- [ ] 7.3 Verify PEP8 compliance
- [ ] 7.4 Review code for common utilities reuse

## 8. Validation

- [ ] 8.1 Test with example from product context
- [ ] 8.2 Verify output matches expected format
- [ ] 8.3 Test with multiple root_modules
- [ ] 8.4 Test with various pytest/unittest styles
