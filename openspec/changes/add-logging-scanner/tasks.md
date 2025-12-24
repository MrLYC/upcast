# Implementation Tasks

## Phase 1: Core Infrastructure

### Task 1.1: Create Data Models

- [ ] Create `upcast/models/logging.py`
- [ ] Define `LogCall` model with all fields (logger_name, lineno, level, message, args, type, has_sensitive, sensitive_patterns)
- [ ] Define `FileLoggingInfo` model with separate lists per library
- [ ] Define `LoggingSummary` model with comprehensive statistics
- [ ] Define `LoggingOutput` model extending ScannerOutput
- [ ] Add comprehensive docstrings
- [ ] Validate with Pydantic constraints (ge=1 for line numbers, etc.)

**Validation**: All models pass Pydantic validation, serialize to JSON correctly

### Task 1.2: Create Scanner Base

- [ ] Create `upcast/scanners/logging_scanner.py`
- [ ] Define `LoggingScanner` class extending `BaseScanner[LoggingOutput]`
- [ ] Implement `scan()` method skeleton
- [ ] Implement `scan_file()` method skeleton
- [ ] Add file discovery using `get_files_to_scan()`
- [ ] Return properly structured `LoggingOutput`

**Validation**: Scanner can be instantiated and run on empty directory

## Phase 2: Standard Library Detection

### Task 2.1: Logger Creation Detection

- [ ] Detect `logging.getLogger()` calls
- [ ] Extract logger name argument (if provided)
- [ ] Handle `__name__` references
- [ ] Handle no-argument calls (root logger)
- [ ] Track logger variable assignments
- [ ] Handle aliased imports (`from logging import getLogger as get_log`)

**Validation**: Unit tests detect all getLogger patterns, correctly track variable names

### Task 2.2: Module Path Resolution

- [ ] Implement `_resolve_module_path()` method
- [ ] Detect package root (first-level `__init__.py`)
- [ ] Convert file path to dotted module path
- [ ] Handle `__name__` → module path conversion
- [ ] Handle `__main__` → module path conversion
- [ ] Cache resolution results per file

**Validation**: Correctly resolves module paths for nested packages, handles edge cases

### Task 2.3: Log Method Call Detection

- [ ] Detect `logger.debug()` calls
- [ ] Detect `logger.info()` calls
- [ ] Detect `logger.warning()` / `logger.warn()` calls
- [ ] Detect `logger.error()` calls
- [ ] Detect `logger.critical()` / `logger.fatal()` calls
- [ ] Match calls to tracked logger variables
- [ ] Handle `self.logger.*` patterns
- [ ] Handle `cls.logger.*` patterns

**Validation**: All log level methods detected, instance/class attributes work

## Phase 3: Message Analysis

### Task 3.1: Message Extraction

- [ ] Extract string literal messages
- [ ] Handle multi-line strings
- [ ] Handle concatenated strings
- [ ] Extract complete message even with line breaks
- [ ] Preserve message formatting

**Validation**: Messages extracted exactly as written in source

### Task 3.2: Format Type Detection

- [ ] Detect plain string type
- [ ] Detect percent-style formatting (`"User %s" % name`)
- [ ] Detect f-string formatting (`f"User {name}"`)
- [ ] Detect str.format() calls (`"User {}".format(name)`)
- [ ] Record correct type in LogCall.type field

**Validation**: Format types correctly identified for all styles

### Task 3.3: Argument Extraction

- [ ] Extract positional arguments after message
- [ ] Extract variable names from arguments
- [ ] Extract variables from f-string expressions
- [ ] Extract arguments from format() calls
- [ ] Handle complex expressions (method calls, attributes)
- [ ] Record arguments as list of strings

**Validation**: Arguments correctly extracted for all format types

## Phase 4: Sensitive Data Detection

### Task 4.1: Keyword Pattern Matching

- [ ] Define sensitive keyword list (password, token, api_key, secret, ssn, credit_card, private_key)
- [ ] Compile regex patterns for efficient matching
- [ ] Scan message strings for keywords
- [ ] Scan argument variable names for keywords
- [ ] Set `has_sensitive` flag when matches found
- [ ] Record matched patterns in `sensitive_patterns` list

**Validation**: Correctly flags known sensitive patterns, no false negatives on test cases

### Task 4.2: Format Pattern Detection

- [ ] Detect JWT token patterns (eyJ...)
- [ ] Detect API key patterns (length/format-based)
- [ ] Detect Base64-encoded strings
- [ ] Detect private key headers (-----BEGIN)
- [ ] Add patterns to sensitive_patterns list

**Validation**: Detects formatted secrets in messages

### Task 4.3: False Positive Reduction

- [ ] Exclude generic terms (user, name, id, value)
- [ ] Require word boundaries for keyword matching
- [ ] Make sensitivity configurable via scanner options
- [ ] Document common false positive scenarios

**Validation**: Low false positive rate on known-safe test files

## Phase 5: Multi-Library Support

### Task 5.1: Loguru Detection

- [ ] Detect `from loguru import logger`
- [ ] Handle loguru's method calls (same as logging)
- [ ] Categorize under `loguru` in FileLoggingInfo
- [ ] Resolve logger_name from module path (loguru has single global logger)

**Validation**: Loguru calls correctly detected and categorized

### Task 5.2: Structlog Detection

- [ ] Detect `import structlog`
- [ ] Detect `structlog.get_logger()` calls
- [ ] Handle structlog's method calls
- [ ] Categorize under `structlog` in FileLoggingInfo

**Validation**: Structlog calls correctly detected and categorized

### Task 5.3: Django Logging Detection

- [ ] Detect Django logging patterns (uses stdlib logging)
- [ ] Detect Django-specific loggers (e.g., `django.request`)
- [ ] Categorize appropriately based on logger name
- [ ] Handle Django logger name conventions

**Validation**: Django logging correctly identified

## Phase 6: Advanced Patterns

### Task 6.1: Conditional Logging

- [ ] Detect `if logger.isEnabledFor(level):` patterns
- [ ] Track log calls within conditional blocks
- [ ] Mark calls as conditional in metadata
- [ ] Handle nested conditionals

**Validation**: Conditional logging detected and marked

### Task 6.2: Module-Level Logging

- [ ] Detect direct `logging.info()` calls (no getLogger)
- [ ] Resolve to root logger
- [ ] Handle module-level logger usage patterns

**Validation**: Module-level calls detected correctly

### Task 6.3: Logger in Exception Context

- [ ] Detect log calls within try/except blocks
- [ ] Note exception handling context in metadata
- [ ] Handle logging.exception() specially

**Validation**: Exception context noted appropriately

## Phase 7: CLI Integration

### Task 7.1: Add CLI Command

- [ ] Add `scan-logging` command to `upcast/main.py`
- [ ] Wire up LoggingScanner
- [ ] Support JSON/YAML output
- [ ] Add command to CLI help

**Validation**: Command runs successfully from CLI

### Task 7.2: Command Options

- [ ] Add `--include-private` option for private methods
- [ ] Add `--min-level` option to filter by log level
- [ ] Add `--check-sensitive` flag (enabled by default)
- [ ] Add `--library` filter option

**Validation**: All options work as expected

## Phase 8: Testing

### Task 8.1: Unit Tests - Models

- [ ] Test all Pydantic models validate correctly
- [ ] Test model serialization to JSON/YAML
- [ ] Test constraint validation (line numbers >= 1, etc.)
- [ ] Create `tests/test_logging_scanner/test_models.py`

**Validation**: 100% coverage on models, all validations work

### Task 8.2: Unit Tests - Detection

- [ ] Test logger creation detection
- [ ] Test each log level method
- [ ] Test message extraction
- [ ] Test argument extraction
- [ ] Test format type detection
- [ ] Create `tests/test_logging_scanner/test_detection.py`

**Validation**: All detection patterns covered

### Task 8.3: Unit Tests - Sensitive Data

- [ ] Test each sensitive keyword
- [ ] Test format pattern detection
- [ ] Test false positive scenarios
- [ ] Test configurable sensitivity
- [ ] Create `tests/test_logging_scanner/test_sensitive.py`

**Validation**: Sensitive detection accuracy verified

### Task 8.4: Integration Tests

- [ ] Create test fixtures for each library
- [ ] Test complete scanning workflow
- [ ] Test multi-library files
- [ ] Test real-world file patterns
- [ ] Create `tests/test_logging_scanner/test_integration.py`

**Validation**: End-to-end tests pass on realistic code

### Task 8.5: Test Fixtures

- [ ] Create `tests/test_logging_scanner/fixtures/stdlib_logging.py`
- [ ] Create `fixtures/loguru_logging.py`
- [ ] Create `fixtures/structlog_logging.py`
- [ ] Create `fixtures/django_logging.py`
- [ ] Create `fixtures/sensitive_logging.py`
- [ ] Create `fixtures/complex_patterns.py`

**Validation**: Fixtures cover all scenarios from specs

## Phase 9: Documentation

### Task 9.1: Update README

- [ ] Add logging scanner to feature list
- [ ] Add usage example
- [ ] Document output format
- [ ] Add sensitive detection notes

**Validation**: Documentation clear and accurate

### Task 9.2: Add Examples

- [ ] Add example scan output to `example/scan-results/`
- [ ] Run scanner on example project
- [ ] Document interesting findings

**Validation**: Examples helpful for users

## Phase 10: Quality and Polish

### Task 10.1: Code Quality

- [ ] Run ruff check and fix issues
- [ ] Ensure 80%+ test coverage
- [ ] Add type hints throughout
- [ ] Add comprehensive docstrings

**Validation**: ruff clean, coverage meets threshold

### Task 10.2: Performance Testing

- [ ] Test on large codebase (1000+ files)
- [ ] Measure scan duration
- [ ] Profile memory usage
- [ ] Optimize if needed

**Validation**: Meets performance requirements from specs

### Task 10.3: OpenSpec Validation

- [ ] Run `openspec validate add-logging-scanner --strict`
- [ ] Fix any validation errors
- [ ] Ensure all requirements have scenarios
- [ ] Update specs if needed

**Validation**: Strict validation passes

## Dependencies

- **Phase 2** depends on **Phase 1** (models must exist)
- **Phase 3** depends on **Phase 2** (detection must work)
- **Phase 4** can be parallel with **Phase 3**
- **Phase 5** depends on **Phase 2** (core detection patterns)
- **Phase 6** depends on **Phase 2-3** (builds on core)
- **Phase 7** depends on **Phase 2-6** (scanner must be functional)
- **Phase 8** can start early, runs parallel with implementation
- **Phase 9-10** are final polish steps

## Parallelization Opportunities

- **Models + Detection** can be developed in parallel (separate files)
- **Sensitive detection** can be implemented independently
- **Multi-library support** each library can be done separately
- **Tests** can be written alongside implementation
- **Documentation** can be drafted early
