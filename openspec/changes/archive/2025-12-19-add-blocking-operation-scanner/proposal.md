# Proposal: Add Blocking Operation Scanner

## Overview

This change introduces a new scanner to detect blocking operations that may cause performance issues in Python applications. The scanner will identify common anti-patterns that block the execution thread, particularly problematic in async/concurrent contexts.

## Problem Statement

Blocking operations can significantly degrade application performance, especially in:

- Async applications where blocking calls prevent the event loop from processing other tasks
- Web applications where blocking operations in request handlers reduce throughput
- Concurrent systems where blocking primitives cause contention

Currently, there's no automated way to identify these anti-patterns across a codebase.

## Proposed Solution

Create a new `blocking-operation-scanner` that uses AST analysis to detect:

1. **Time-based blocking**: `time.sleep()` calls
2. **Database locking**: Django ORM `select_for_update()` calls
3. **Synchronization primitives**: `threading.Lock().acquire()` and similar blocking lock operations
4. **Subprocess operations**: `subprocess.run()`, `Popen.wait()`, `Popen.communicate()`
5. **Other blocking patterns**: File I/O operations, network calls without timeouts

The scanner will:

- Use astroid for semantic analysis
- Extract location, context, and blocking duration (when available)
- Categorize operations by type
- Output results in YAML/JSON format
- Follow the established scanner architecture pattern

## Scope

### In Scope

- Detection of explicit blocking operations listed above
- Location and context extraction
- CLI interface following upcast conventions
- File filtering support (include/exclude patterns)
- YAML/JSON export
- Basic unit tests and integration tests

### Out of Scope

- Runtime performance measurement
- Automatic refactoring suggestions
- Detection of all possible blocking operations (focus on common anti-patterns)
- Static analysis of third-party library internals

## Impact Analysis

### Benefits

- Identify performance bottlenecks early in development
- Enforce async-safe coding patterns
- Improve code review efficiency
- Document blocking operations for performance optimization

### Risks

- False positives in legitimate blocking use cases (e.g., CLI tools)
- May require significant code changes if many anti-patterns are found

## Dependencies

- Existing common utilities (`upcast.common`)
- astroid for AST analysis
- CLI framework (Click)

## Success Criteria

1. Scanner successfully detects all specified blocking patterns
2. Output format consistent with other scanners
3. CLI interface matches upcast conventions
4. Test coverage ≥90%
5. Performance: scan 1000 files in <10 seconds

## Alternatives Considered

1. **Runtime profiling**: Rejected - requires code execution, not static analysis
2. **Linter integration**: Rejected - want standalone tool that integrates with existing scanner suite
3. **Extending concurrency scanner**: Rejected - blocking operations are conceptually different from concurrency patterns

## Implementation Notes

Follow the established scanner architecture:

- `operation_parser.py`: Core AST analysis and pattern matching
- `checker.py`: AST traversal and operation collection
- `export.py`: YAML/JSON formatting
- `cli.py`: Command-line interface

Reuse common utilities:

- `upcast.common.file_utils`: File discovery and filtering
- `upcast.common.patterns`: Glob pattern matching
- `upcast.common.ast_utils`: AST inference helpers
- `upcast.common.export`: Consistent output formatting
