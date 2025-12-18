# Proposal: implement-exception-handler-scanner

## What

Implement a new scanner module `exception_handler_scanner` to detect and analyze exception handling patterns in Python codebases, outputting structured YAML documentation of try/except/else/finally blocks with detailed information about exception types, logging practices, and control flow patterns.

## Why

Exception handling is critical for application reliability and debugging, but exception handling patterns are often inconsistent and poorly documented across codebases. Teams need:

1. **Exception handling inventory**: Know what exceptions are caught, where, and how they're handled
2. **Logging compliance validation**: Track which exceptions are logged and at what severity levels
3. **Control flow analysis**: Understand how exceptions affect program flow (pass, return, raise, etc.)
4. **Statistical insights**: Quantify exception handling patterns across the codebase
5. **Maintenance assistance**: Support refactoring and debugging with structured exception data

Following the established pattern of `concurrency_pattern_scanner` and `prometheus_metrics_scanner`, this scanner provides automated discovery and analysis of exception handling patterns using astroid-based AST analysis.

## How

### Core Approach

Use astroid to parse Python files and detect exception handling patterns:

1. **Try block structure**: Detect try/except/else/finally blocks
2. **Exception type extraction**: Parse exception types in each except clause (including bare except)
3. **Logging counting**: Count logging calls by level (debug, info, warning, error, exception, critical)
4. **Control flow counting**: Count occurrences of pass, return, break, continue, raise statements
5. **Block metrics**: Count lines of code in try/except/else/finally sections

### Module Structure

```
upcast/exception_handler_scanner/
├── __init__.py              # Public API exports
├── cli.py                   # scan_exception_handlers() entry point
├── checker.py               # ExceptionHandlerChecker visitor
├── handler_parser.py        # Exception handler extraction logic
└── export.py                # YAML formatting and output
```

Reuse from `upcast/common/`:

- `ast_utils.py`: safe_as_string, get_qualified_name
- `file_utils.py`: collect_python_files, validate_path
- `export.py`: export_to_yaml, export_to_json

### Output Format

```yaml
exception_handlers:
  - location: "api/views.py:15-23"
    try_lines: 5
    except_clauses:
      - line: 20
        exception_types: [ValueError, KeyError]
        lines: 3
        # Logging counts by level
        log_debug_count: 0
        log_info_count: 0
        log_warning_count: 0
        log_error_count: 1
        log_exception_count: 0
        log_critical_count: 0
        # Control flow counts
        pass_count: 0
        return_count: 0
        break_count: 0
        continue_count: 0
        raise_count: 0
    else_clause:
      line: 23
      lines: 1
    finally_clause: null

  - location: "core/utils.py:42-48"
    try_lines: 3
    except_clauses:
      - line: 45
        exception_types: [] # bare except
        lines: 1
        log_debug_count: 0
        log_info_count: 0
        log_warning_count: 0
        log_error_count: 0
        log_exception_count: 0
        log_critical_count: 0
        pass_count: 1
        return_count: 0
        break_count: 0
        continue_count: 0
        raise_count: 0
    else_clause: null
    finally_clause: null

  - location: "service/processor.py:102-115"
    try_lines: 8
    except_clauses:
      - line: 110
        exception_types: [Exception]
        lines: 2
        log_debug_count: 0
        log_info_count: 0
        log_warning_count: 0
        log_error_count: 0
        log_exception_count: 1
        log_critical_count: 0
        pass_count: 0
        return_count: 1
        break_count: 0
        continue_count: 0
        raise_count: 0
      - line: 112
        exception_types: [KeyboardInterrupt]
        lines: 1
        log_debug_count: 0
        log_info_count: 0
        log_warning_count: 0
        log_error_count: 0
        log_exception_count: 0
        log_critical_count: 0
        pass_count: 0
        return_count: 0
        break_count: 0
        continue_count: 0
        raise_count: 1
    else_clause: null
    finally_clause:
      line: 114
      lines: 2

summary:
  total_try_blocks: 3
  total_except_clauses: 4
  bare_excepts: 1
  except_with_pass: 1
  except_with_return: 1
  except_with_raise: 1
  total_log_calls: 2
  except_without_logging: 2
```

## Impact

### New Files

- `upcast/exception_handler_scanner/*.py` (5 files)
- `tests/test_exception_handler_scanner/*.py` (5 test files + fixtures)
- `openspec/specs/exception-handler-scanner/spec.md`

### Modified Files

- `upcast/main.py`: Add `scan-exception-handlers` CLI command registration
- `README.md`: Document new scanner capability

### Dependencies

- Reuse existing `astroid` dependency (already in project)
- Reuse `upcast.common` utilities (file_utils, ast_utils, export)
- No new external dependencies

### Backward Compatibility

No breaking changes. Pure addition of new functionality following established patterns.

## Alternatives Considered

1. **Regex-based parsing**: Rejected because it cannot handle nested try/except blocks or complex control flow
2. **Runtime tracing**: Rejected because it only captures executed paths, missing unused exception handlers
3. **pylint/flake8 integration**: Rejected because we need structured data output, not just warnings
4. **Static type checking integration**: Rejected because exception handling is often untyped

## Open Questions

1. **Nested try blocks**: Should we track nesting depth and parent/child relationships?
2. **Exception chaining**: Should we detect `raise ... from` patterns?
3. **Context managers**: Should we track exception suppression via `__exit__` methods?
4. **Async exception handling**: Should we handle asyncio exception patterns differently?
5. **Custom exception classes**: Should we track user-defined exception hierarchies?

**Recommendation**: Start with basic patterns (try/except structure, logging, control flow) and extend based on user feedback. Focus on anti-pattern detection first.

## Success Criteria

- [ ] Detect all try/except/else/finally blocks
- [ ] Extract exception types from each except clause (including bare except)
- [ ] Count logging calls by level (debug, info, warning, error, exception, critical)
- [ ] Count control flow statements (pass, return, break, continue, raise)
- [ ] Calculate line counts for try/except/else/finally sections
- [ ] Generate summary statistics (total blocks, bare excepts, logging coverage)
- [ ] Output structured YAML matching examples
- [ ] 85%+ test coverage following project patterns
- [ ] CLI integration: `upcast scan-exception-handlers <path>`
- [ ] Documentation with usage examples
