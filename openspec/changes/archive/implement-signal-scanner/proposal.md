# Proposal: Implement Signal Scanner

## Why

Django and Celery signal patterns are common in Python applications for handling events and lifecycle hooks. Developers need visibility into signal usage to:

- Understand signal-driven architecture and event flow
- Identify potential performance bottlenecks (blocking operations in signals)
- Track signal handler registration and dependencies
- Audit signal usage for migration or refactoring efforts
- Detect anti-patterns like heavy processing in Django signals

Currently, there is no automated way to scan and collect signal definitions and handlers across a codebase. This change introduces a signal scanner that detects and reports both Django and Celery signal patterns.

## What Changes

This change introduces a new `signal-scanner` capability that detects:

1. **Django Signals**

   - Built-in signals (request_started, post_save, pre_delete, etc.)
   - Custom signals (django.dispatch.Signal)
   - Signal handlers using @receiver decorator
   - Signal handlers using .connect() method

2. **Celery Signals**

   - Task lifecycle signals (task_prerun, task_postrun, task_failure, task_retry)
   - Worker signals (worker_ready, worker_shutdown)
   - Signal handlers using @signal.connect decorator
   - Signal handlers using .connect() method

3. **Output Format**
   - Groups signals by framework (django/celery)
   - Lists signal names with their handlers
   - Includes file location, line number, and handler function context
   - Exports to YAML format

The implementation follows the established scanner architecture pattern used in other scanners (django-model-scanner, env-var-scanner, concurrency-scanner).

## Specs

- [signal-scanner](specs/signal-scanner/spec.md) - NEW: Signal detection and parsing
- [cli-interface](specs/cli-interface/spec.md) - MODIFIED: Add scan-signals command

## Related Changes

- Uses patterns from `concurrency-scanner` for AST-based pattern detection
- Follows CLI interface conventions from `cli-interface` spec
- Leverages `common-utilities` for shared AST and export functionality
