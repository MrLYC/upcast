# Design: Signal Scanner

## Overview

The signal scanner detects Django and Celery signal patterns in Python codebases using AST analysis. It identifies signal definitions, handler registrations, and usage patterns.

## Architecture

### Components

```
upcast/signal_scanner/
├── __init__.py           # Public API exports
├── checker.py            # AST visitor for signal detection
├── signal_parser.py      # Pattern parsing functions
├── export.py             # YAML output formatting
└── cli.py                # CLI command interface
```

### Design Patterns

**Pattern Detection Strategy:**

1. **Two-pass scanning** (similar to concurrency-scanner):
   - First pass: collect custom signal definitions
   - Second pass: match handlers to signals
2. **Framework grouping**: Separate Django and Celery patterns
3. **Handler resolution**: Track both @decorator and .connect() patterns

**AST Node Types:**

- `FunctionDef` with `@receiver` or `@signal.connect` decorators
- `Call` nodes for `.connect()` method calls
- `Assign` nodes for custom signal definitions (`Signal()` instances)
- `ImportFrom` nodes to track signal imports

## Key Decisions

### 1. Framework Separation

**Decision:** Group signals by framework (django/celery) in output

**Rationale:**

- Different frameworks have different signal semantics
- Users typically work with one framework at a time
- Easier to understand signal usage per framework

**Trade-offs:**

- Slightly more complex grouping logic
- - Clear separation of concerns
- - Better user experience

### 2. Handler Context Extraction

**Decision:** Include function context (class, enclosing function) for handlers

**Rationale:**

- Signal handlers can be methods, nested functions, or standalone functions
- Context helps understand handler purpose and lifecycle
- Consistent with other scanner patterns (django-model-scanner)

**Implementation:**

- Use common utilities `get_enclosing_scope()` from `upcast.common.ast_utils`
- Extract function/class names and line numbers

### 3. Custom Signal Detection

**Decision:** Detect custom Django signals (django.dispatch.Signal instances)

**Rationale:**

- Custom signals are first-class citizens in Django
- Users need to track custom event definitions
- Helps understand application-specific event flow

**Pattern:**

```python
# Detect assignments like:
order_paid = Signal()
order_paid = Signal(providing_args=['order', 'user'])
```

### 4. Signal Name Resolution

**Decision:** Infer signal names from import tracking and qualified names

**Rationale:**

- Signals can be imported with aliases
- Handlers may reference signals via different names
- Need accurate mapping between handlers and signals

**Strategy:**

- Track imports: `from django.db.models.signals import post_save`
- Track aliases: `from celery.signals import task_prerun as prerun`
- Use qualified names for disambiguation

## Implementation Phases

### Phase 1: Core Detection (MVP)

- Detect @receiver decorator patterns (Django)
- Detect @signal.connect decorator patterns (Celery)
- Basic signal name extraction
- YAML export with framework grouping

### Phase 2: Advanced Patterns

- Detect .connect() method calls
- Custom signal definitions
- Import alias tracking
- Handler context extraction

### Phase 3: CLI and Integration

- CLI command `scan-signals`
- Standard options (--output, --verbose, --include, --exclude)
- Main CLI integration
- Documentation and examples

## Non-Goals

- **Runtime signal analysis**: Only static analysis via AST
- **Signal execution tracing**: Not tracking actual signal sends
- **Performance profiling**: Not measuring signal handler performance
- **Django/Celery version compatibility**: Assume modern versions (3.2+/5.0+)

## Testing Strategy

### Test Fixtures

- `tests/test_signal_scanner/fixtures/django_signals.py` - Django patterns
- `tests/test_signal_scanner/fixtures/celery_signals.py` - Celery patterns
- `tests/test_signal_scanner/fixtures/custom_signals.py` - Custom signals
- `tests/test_signal_scanner/fixtures/mixed_signals.py` - Combined patterns

### Test Coverage

- Unit tests for each parsing function (signal_parser.py)
- Integration tests for end-to-end scanning (test_integration.py)
- CLI tests (test_cli.py)
- Edge cases: nested handlers, dynamic registration, aliases

## Migration Path

No migration needed - this is a new scanner. However:

- Follows established scanner architecture conventions
- Reuses common utilities (ast_utils, file_utils, export)
- CLI interface consistent with other scanners

## References

- Django Signals Documentation: https://docs.djangoproject.com/en/stable/topics/signals/
- Celery Signals Documentation: https://docs.celeryq.dev/en/stable/userguide/signals.html
- Related Scanners: django-model-scanner, concurrency-scanner, django-settings-scanner
