# Tasks for Reimplement Environment Variable Scanner

## Phase 1: Core Infrastructure (Parallel with Phase 2)

### 1. Create module structure

- [ ] Create `upcast/env_var_scanner/` directory
- [ ] Create `__init__.py` with public API exports
- [ ] Create `ast_utils.py` for AST helper functions
- [ ] Create `env_var_parser.py` for parsing logic
- [ ] Create `checker.py` for visitor pattern implementation
- [ ] Create `cli.py` for scanning orchestration
- [ ] Create `export.py` for YAML output formatting

**Validation**: Module structure exists and imports work

### 2. Implement AST utilities

- [ ] Implement `is_env_var_call()` to detect environment variable access patterns
- [ ] Implement `infer_type_from_value()` to infer types from default values
- [ ] Implement `infer_literal_value()` to extract literal values from AST nodes
- [ ] Implement `resolve_string_concat()` to handle string concatenation for env var names
- [ ] Add tests for AST utility functions

**Validation**: All AST utilities have unit tests and pass

## Phase 2: Pattern Detection (Parallel with Phase 1)

### 3. Implement os module pattern detection

- [ ] Detect `os.getenv(name)` and `os.getenv(name, default)`
- [ ] Detect `os.environ[name]` (required pattern)
- [ ] Detect `os.environ.get(name)` and `os.environ.get(name, default)`
- [ ] Handle aliased imports (`from os import getenv`)
- [ ] Add tests for os module patterns

**Validation**: Tests verify all os module patterns are detected correctly

### 4. Implement django-environ pattern detection

- [ ] Detect `env(name)` and `env.TYPE(name)`
- [ ] Detect `env(name, default=value)` and `env.TYPE(name, default=value)`
- [ ] Handle Env class instantiation with schema
- [ ] Parse type from method name (`.str()`, `.int()`, `.bool()`, etc.)
- [ ] Add tests for django-environ patterns

**Validation**: Tests verify django-environ patterns with type inference

### 5. Implement type inference

- [ ] Infer type from cast wrapper (e.g., `int(os.getenv(...))`)
- [ ] Infer type from default value literals
- [ ] Infer type from django-environ method names
- [ ] Handle multiple type occurrences (list of types)
- [ ] Add tests for type inference

**Validation**: Tests verify type inference from various sources

## Phase 3: Aggregation and Export

### 6. Implement result aggregation

- [ ] Create `EnvVarUsage` model with name, types, defaults, locations, statements
- [ ] Aggregate multiple usages by environment variable name
- [ ] Collect all types across all usages
- [ ] Collect all default values across all usages
- [ ] Collect all locations (file:line) across all usages
- [ ] Determine required status (true if any usage is required)
- [ ] Add tests for aggregation logic

**Validation**: Tests verify correct aggregation of multiple usages

### 7. Implement YAML export

- [ ] Format aggregated results as YAML
- [ ] Structure: variable name as key, with types/defaults/locations as values
- [ ] Use readable formatting (block style, proper indentation)
- [ ] Handle empty lists gracefully
- [ ] Add tests for YAML export formatting

**Validation**: Tests verify YAML output format and readability

## Phase 4: CLI and Integration

### 8. Implement CLI command

- [ ] Add `scan-env-vars` command to `upcast/main.py`
- [ ] Support directory and file path arguments
- [ ] Support `-o/--output` for file output
- [ ] Support `-v/--verbose` for detailed logging
- [ ] Support `--format` option (yaml, json)
- [ ] Add error handling for invalid paths
- [ ] Add tests for CLI command

**Validation**: Manual testing and CLI tests pass

### 9. Add comprehensive documentation

- [ ] Document CLI usage in README
- [ ] Add examples of output format
- [ ] Document supported patterns
- [ ] Document type inference behavior
- [ ] Add migration guide from old env_var module

**Validation**: Documentation is complete and accurate

## Phase 5: Testing and Validation

### 10. Integration testing

- [ ] Create test fixtures with real-world Python files
- [ ] Test scanning Python projects with mixed patterns
- [ ] Test handling of edge cases (missing imports, syntax errors)
- [ ] Test aggregation across multiple files
- [ ] Verify output matches expected format

**Validation**: All integration tests pass

### 11. Performance testing

- [ ] Benchmark scanning large codebases
- [ ] Compare performance with old implementation
- [ ] Optimize bottlenecks if needed

**Validation**: Performance is acceptable for typical projects

## Phase 6: Deprecation Plan (Future)

### 12. Maintain backward compatibility

- [ ] Keep old `find_env_vars` command working
- [ ] Add deprecation warning to old command
- [ ] Update documentation to recommend new command

**Validation**: Old command still works with deprecation notice

## Dependencies and Parallelization

- **Phase 1 and Phase 2** can be done in parallel (different developers)
- **Phase 3** depends on Phase 1 and Phase 2 completion
- **Phase 4** depends on Phase 3 completion
- **Phase 5** should be done incrementally throughout all phases
- **Phase 6** can be planned but executed in a future release

## Success Criteria

- [ ] All unit tests pass (target: >90% coverage)
- [ ] Integration tests pass with real-world examples
- [ ] Output format is clear and useful
- [ ] CLI is intuitive and well-documented
- [ ] Performance is acceptable (< 5 seconds for typical projects)
- [ ] New implementation validated via `openspec validate`
