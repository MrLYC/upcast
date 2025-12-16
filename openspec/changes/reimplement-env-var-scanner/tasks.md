# Tasks for Reimplement Environment Variable Scanner

## Phase 1: Core Infrastructure (Parallel with Phase 2)

### 1. Create module structure

- [x] Create `upcast/env_var_scanner/` directory
- [x] Create `__init__.py` with public API exports
- [x] Create `ast_utils.py` for AST helper functions
- [x] Create `env_var_parser.py` for parsing logic
- [x] Create `checker.py` for visitor pattern implementation
- [x] Create `cli.py` for scanning orchestration
- [x] Create `export.py` for YAML output formatting

**Validation**: Module structure exists and imports work ✅

### 2. Implement AST utilities

- [x] Implement `is_env_var_call()` to detect environment variable access patterns
- [x] Implement `infer_type_from_value()` to infer types from default values
- [x] Implement `infer_literal_value()` to extract literal values from AST nodes
- [x] Implement `resolve_string_concat()` to handle string concatenation for env var names
- [x] Add tests for AST utility functions

**Validation**: All AST utilities have unit tests and pass ✅ (17/17 tests passing)

## Phase 2: Pattern Detection (Parallel with Phase 1)

### 3. Implement os module pattern detection

- [x] Detect `os.getenv(name)` and `os.getenv(name, default)`
- [x] Detect `os.environ[name]` (required pattern)
- [x] Detect `os.environ.get(name)` and `os.environ.get(name, default)`
- [x] Handle aliased imports (`from os import getenv`)
- [x] Add tests for os module patterns

**Validation**: Tests verify all os module patterns are detected correctly ✅

### 4. Implement django-environ pattern detection

- [x] Detect `env(name)` and `env.TYPE(name)`
- [x] Detect `env(name, default=value)` and `env.TYPE(name, default=value)`
- [x] Handle Env class instantiation with schema
- [x] Parse type from method name (`.str()`, `.int()`, `.bool()`, etc.)
- [x] Add tests for django-environ patterns

**Validation**: Tests verify django-environ patterns with type inference ✅

### 5. Implement type inference

- [x] Infer type from cast wrapper (e.g., `int(os.getenv(...))`)
- [x] Infer type from default value literals
- [x] Infer type from django-environ method names
- [x] Handle multiple type occurrences (list of types)
- [x] Add tests for type inference

**Validation**: Tests verify type inference from various sources ✅

## Phase 3: Aggregation and Export

### 6. Implement result aggregation

- [x] Create `EnvVarUsage` model with name, types, defaults, locations, statements
- [x] Aggregate multiple usages by environment variable name
- [x] Collect all types across all usages
- [x] Collect all default values across all usages
- [x] Collect all locations (file:line) across all usages
- [x] Determine required status (true if any usage is required)
- [x] Add tests for aggregation logic

**Validation**: Tests verify correct aggregation of multiple usages ✅

### 7. Implement YAML export

- [x] Format aggregated results as YAML
- [x] Structure: variable name as key, with types/defaults/locations as values
- [x] Use readable formatting (block style, proper indentation)
- [x] Handle empty lists gracefully
- [x] Add tests for YAML export formatting

**Validation**: Tests verify YAML output format and readability ✅

## Phase 4: CLI and Integration

### 8. Implement CLI command

- [x] Add `scan-env-vars` command to `upcast/main.py`
- [x] Support directory and file path arguments
- [x] Support `-o/--output` for file output
- [x] Support `-v/--verbose` for detailed logging
- [x] Support `--format` option (yaml, json)
- [x] Add error handling for invalid paths
- [x] Add tests for CLI command

**Validation**: Manual testing and CLI tests pass ✅

### 9. Add comprehensive documentation

- [x] Document CLI usage in README
- [x] Add examples of output format
- [x] Document supported patterns
- [x] Document type inference behavior
- [x] Add migration guide from old env_var module

**Validation**: Documentation is complete and accurate ✅

## Phase 5: Testing and Validation

### 10. Integration testing

- [x] Create test fixtures with real-world Python files
- [x] Test scanning Python projects with mixed patterns
- [x] Test handling of edge cases (missing imports, syntax errors)
- [x] Test aggregation across multiple files
- [x] Verify output matches expected format

**Validation**: All integration tests pass ✅ (27/27 tests passing, 198 total suite passing)

### 11. Performance testing

- [x] Benchmark scanning large codebases
- [x] Compare performance with old implementation
- [x] Optimize bottlenecks if needed

**Validation**: Performance is acceptable for typical projects ✅ (< 0.3s for test fixtures)

## Phase 6: Deprecation Plan (Future)

### 12. Maintain backward compatibility

- [x] Keep old `find_env_vars` command working
- [x] Add deprecation warning to old command
- [x] Update documentation to recommend new command

**Validation**: Old command still works with deprecation notice ✅

## Dependencies and Parallelization

- **Phase 1 and Phase 2** ✅ Complete
- **Phase 3** ✅ Complete
- **Phase 4** ✅ Complete
- **Phase 5** ✅ Complete
- **Phase 6** ✅ Complete

## Success Criteria

- [x] All unit tests pass (target: >90% coverage) ✅ 27 env_var_scanner tests + 198 total
- [x] Integration tests pass with real-world examples ✅
- [x] Output format is clear and useful ✅ (YAML and JSON both working)
- [x] CLI is intuitive and well-documented ✅ (scan-env-vars command working)
- [x] Performance is acceptable (< 5 seconds for typical projects) ✅
- [x] New implementation validated via `openspec validate` ✅
