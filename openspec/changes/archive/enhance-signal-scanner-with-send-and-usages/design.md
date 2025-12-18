# Design: Enhance Signal Scanner with Send Detection and Usage Tracking

## Overview

增强 signal scanner 以支持信号发送检测和统一的 usage 追踪模式，提供完整的信号生命周期视图。

## Architecture Changes

### Data Structures

#### New: SignalUsage Dataclass

```python
@dataclass
class SignalUsage:
    """Represents a single usage of a signal (send or receive)."""

    file: str          # Relative path from project root
    line: int          # Line number (1-based)
    column: int        # Column number (0-based)
    pattern: str       # Usage pattern type
    code: str          # Source code snippet
    sender: str | None = None  # Sender if specified
```

**Pattern types:**

- `"receiver_decorator"`: @receiver(signal, sender=Model)
- `"connect_method"`: signal.connect(handler)
- `"celery_connect_decorator"`: @signal.connect
- `"send_method"`: signal.send(sender=...)
- `"send_robust_method"`: signal.send_robust(sender=...)

#### Updated: Signal Data Structure

**Before:**

```python
{
  "django": {
    "model_signals": {
      "post_save": [
        {
          "handler": "order_created",
          "file": "handlers.py",
          "line": 10,
          "sender": "Order"
        }
      ]
    }
  }
}
```

**After:**

```python
{
  "django": {
    "model_signals": {
      "post_save": {
        "receivers": [  # Handler registrations
          {
            "handler": "order_created",
            "file": "handlers.py",
            "line": 10,
            "sender": "Order",
            "pattern": "receiver_decorator"
          }
        ],
        "senders": [  # Signal send calls
          {
            "file": "views.py",
            "line": 25,
            "sender": "Order",
            "pattern": "send_method"
          }
        ],
        "usages": [  # All usages (receivers + senders)
          {
            "file": "handlers.py",
            "line": 10,
            "column": 0,
            "pattern": "receiver_decorator",
            "code": "@receiver(post_save, sender=Order)",
            "sender": "Order"
          },
          {
            "file": "views.py",
            "line": 25,
            "column": 4,
            "pattern": "send_method",
            "code": "post_save.send(sender=Order, instance=order)",
            "sender": "Order"
          }
        ]
      }
    }
  }
}
```

### New Detection Patterns

#### Django Signal Send

```python
# Pattern 1: Direct send
post_save.send(sender=Order, instance=order, created=True)

# Pattern 2: send_robust
post_save.send_robust(sender=Order, instance=order)

# Pattern 3: Custom signal send
order_paid.send(sender=Order, instance=order)
```

**AST Pattern:**

- Node type: `nodes.Call`
- Func: `nodes.Attribute` with attr `"send"` or `"send_robust"`
- Value: signal name that MUST be in known signals list

**Known Signals Validation:**

To avoid false positives (e.g., `mail.send()`, `message.send()`), the system validates that the object calling `.send()` is actually a signal:

1. **Django built-in signals**: Check if name is in `django_imports` (e.g., `post_save`, `request_finished`)
2. **Celery built-in signals**: Check if name is in `celery_imports` (e.g., `task_sent`, `worker_ready`)
3. **Custom signals**: Check if name is in `custom_signals` dict (from first pass)
4. **Signal instances**: Check if name matches any signal referenced by receivers (from second pass)

**Example - Valid signal send:**

```python
from django.db.models.signals import post_save
from myapp.signals import order_paid

post_save.send(sender=Order, instance=order)  # ✅ Valid: in django_imports
order_paid.send(sender=Order, instance=order)  # ✅ Valid: in custom_signals
```

**Example - Not a signal send:**

```python
mail.send()  # ❌ Invalid: not in any known signals
client.send(data)  # ❌ Invalid: not in any known signals
message.send()  # ❌ Invalid: not in any known signals
```

#### Celery Signal Send

```python
# Pattern: Celery signal send
task_sent.send(sender='tasks.process_order', **kwargs)
```

**AST Pattern:**

- Node type: `nodes.Call`
- Func: `nodes.Attribute` with attr `"send"`
- Value: Celery signal name (requires import tracking)

## Component Changes

### 1. signal_parser.py

**New Functions:**

```python
def parse_signal_send(
    node: nodes.Call,
    django_imports: set[str],
    celery_imports: set[str],
    custom_signals: dict[str, Any],
    root_path: str | None,
    file_path: str,
) -> SignalUsage | None:
    """Parse signal.send() or signal.send_robust() call.

    Returns:
        SignalUsage object with pattern "send_method" or "send_robust_method"
    """
    pass

def _is_signal_send_call(
    node: nodes.Call,
    django_imports: set[str],
    celery_imports: set[str],
    custom_signals: dict[str, Any],
    known_signal_names: set[str],  # NEW: from receivers
) -> tuple[str, str] | None:
    """Check if a Call node is a signal send.

    Validates that the object calling .send() is a known signal to avoid
    false positives like mail.send(), message.send(), etc.

    Args:
        node: The Call AST node
        django_imports: Django signal names from imports
        celery_imports: Celery signal names from imports
        custom_signals: Custom signal definitions
        known_signal_names: Signal names extracted from receivers

    Returns:
        (signal_name, method_type) tuple or None
        method_type is "send" or "send_robust"
        Returns None if not a valid signal send
    """
    # Extract signal name from node.func.value
    signal_name = _extract_signal_name(node)
    if not signal_name:
        return None

    # Validate against known signals
    if signal_name not in django_imports and \
       signal_name not in celery_imports and \
       signal_name not in custom_signals and \
       signal_name not in known_signal_names:
        # Not a known signal - likely mail.send(), etc.
        return None

    # Extract method type
    method = node.func.attrname
    if method not in ('send', 'send_robust'):
        return None

    return (signal_name, method)
```

**Modified Functions:**

所有现有的 `parse_*` 函数需要返回 `SignalUsage` 对象而不是 dict：

```python
def parse_receiver_decorator(...) -> list[SignalUsage]:
    """Return list of SignalUsage objects."""
    pass

def parse_signal_connect_method(...) -> SignalUsage | None:
    """Return SignalUsage object."""
    pass
```

### 2. checker.py

**Updated Fields:**

```python
class SignalChecker:
    def __init__(self, ...):
        # Changed from list[dict] to dict with receivers/senders/usages
        self.signals: dict[str, dict[str, dict[str, dict[str, list]]]] = {
            "django": {},
            "celery": {},
        }
```

**New Methods:**

```python
def _collect_signal_sends(self, module: nodes.Module) -> None:
    """Collect signal send/send_robust calls (new third pass)."""
    # Build known signal names from receivers (for validation)
    known_signal_names = self._get_known_signal_names()

    for call_node in module.nodes_of_class(nodes.Call):
        usage = parse_signal_send(
            call_node,
            self.django_imports,
            self.celery_imports,
            self.custom_signals,
            known_signal_names,  # NEW: pass known signals
            self.root_path,
            module.file,
        )
        if usage:
            self._register_send(usage)

def _get_known_signal_names(self) -> set[str]:
    """Extract all signal names from collected receivers.

    This helps validate send calls by creating a whitelist of signals
    that actually have receivers, reducing false positives.
    """
    known = set()
    for framework in self.signals.values():
        for category in framework.values():
            if isinstance(category, dict):
                known.update(category.keys())
    return known
```

**Modified Methods:**

```python
def visit_module(self, module: nodes.Module) -> None:
    """Three-pass scanning:
    1. Collect imports and custom signals
    2. Collect signal handlers (receivers)
    3. Collect signal sends (NEW)
    """
    self._collect_imports(module)
    self._collect_custom_signals(module)
    self._collect_signal_handlers(module)
    self._collect_signal_sends(module)  # NEW

def _register_handler(self, framework, category, signal_name, usage):
    """Register a signal usage as receiver."""
    # Initialize structure if needed
    if signal_name not in self.signals[framework][category]:
        self.signals[framework][category][signal_name] = {
            "receivers": [],
            "senders": [],
            "usages": [],
        }

    # Add to receivers and usages
    self.signals[framework][category][signal_name]["receivers"].append(
        self._usage_to_receiver_dict(usage)
    )
    self.signals[framework][category][signal_name]["usages"].append(
        dataclasses.asdict(usage)
    )

def _register_send(self, usage: SignalUsage):
    """Register a signal send call (NEW)."""
    # Similar to _register_handler but for senders
    pass
```

### 3. export.py

**Updated Functions:**

```python
def format_signal_output(results: dict[str, Any]) -> dict[str, Any]:
    """Format with new structure (receivers/senders/usages)."""
    # Update to handle new nested structure
    # Optionally provide --simple mode for backward compatibility
    pass
```

**Output Format Options:**

1. **Default (Full) Mode**: 包含 receivers, senders, usages
2. **Simple Mode** (`--simple`): 仅 receivers（向后兼容）
3. **Send Only Mode** (`--send-only`): 仅 senders（用于分析信号触发点）

## Key Decisions

### Decision 1: Strict Signal Validation to Prevent False Positives

**Problem:** Many Python objects have `.send()` methods (email, messages, sockets, HTTP clients, etc.), not just signals. Naive detection would create many false positives.

**Solution:** Build a "known signals whitelist" from multiple sources:

1. **Import tracking**: Django signals from `from django.db.models.signals import post_save`
2. **Custom definitions**: User-defined signals like `order_paid = Signal()`
3. **Receiver references**: Signals that have registered handlers
4. **Celery imports**: Celery signals from `from celery.signals import task_sent`

**Validation Algorithm:**

```python
def is_valid_signal_send(call_node, known_signals):
    """Only accept .send() calls on known signals."""
    signal_name = extract_signal_name(call_node)

    # Must be in one of these sources
    if signal_name in django_imports:
        return True  # e.g., post_save.send()
    if signal_name in celery_imports:
        return True  # e.g., task_sent.send()
    if signal_name in custom_signals:
        return True  # e.g., order_paid.send()
    if signal_name in known_signal_names_from_receivers:
        return True  # Signal has receivers, likely valid

    return False  # Reject: mail.send(), client.send(), etc.
```

**Examples:**

✅ **Valid signal sends (will be detected):**

```python
from django.db.models.signals import post_save
from myapp.signals import order_paid

post_save.send(sender=Order, instance=order)  # In django_imports
order_paid.send(sender=Order)  # In custom_signals
```

❌ **Non-signal sends (will be rejected):**

```python
from django.core.mail import EmailMessage

mail = EmailMessage(...)
mail.send()  # 'mail' not in known signals - REJECTED

import requests
client = requests.Session()
client.send(request)  # 'client' not in known signals - REJECTED

from channels.layers import get_channel_layer
channel_layer.send('room', {'type': 'message'})  # REJECTED
```

**Trade-offs:**

- ➕ **High precision**: Very few false positives
- ➕ **Clear semantics**: Only tracks actual signals
- ➖ **May miss edge cases**: Dynamic signal references, heavy aliasing
- ➖ **Requires import tracking**: Depends on first pass accuracy

**Mitigation for missed cases:**

- Document that signals should be imported directly for detection
- Provide verbose mode to show rejected .send() calls
- User can add custom patterns via configuration (future enhancement)

### Decision 2: Three-Pass Scanning

**Rationale:**

- Pass 1: Collect imports and custom signals
- Pass 2: Collect receivers
- Pass 3: Collect sends

**Trade-offs:**

- ➕ Clear separation of concerns
- ➕ Can reference custom_signals when detecting sends
- ➖ Three passes through AST (minimal performance impact)

**Alternative:** Single-pass with deferred resolution

- More complex state management
- Harder to debug

### Decision 2: Unified Usage Structure

**Rationale:**

- Consistent with django-settings-scanner
- Easier to analyze all usage points
- Supports future enhancements (e.g., usage statistics)

**Trade-offs:**

- ➕ Consistent data model across scanners
- ➕ Rich contextual information
- ➖ Breaking change to output format

**Mitigation:** Provide `--simple` flag for backward compatibility

### Decision 3: Separate Receivers and Senders Lists

**Rationale:**

- Users often care about one or the other
- Easier to answer "where is this signal sent?" vs "who handles this signal?"
- Cleaner than filtering usages by pattern

**Trade-offs:**

- ➕ Better UX for common queries
- ➕ Clear semantic distinction
- ➖ Some data duplication (also in usages list)

**Justification:** Duplication is minimal and improves usability significantly

## Testing Strategy

### New Test Fixtures

Create `tests/test_signal_scanner/fixtures/signal_sends.py`:

```python
from django.db.models.signals import post_save
from myapp.signals import order_paid

def create_order(request):
    order = Order.objects.create(...)
    # Send built-in signal
    post_save.send(sender=Order, instance=order, created=True)

    # Send custom signal
    order_paid.send(sender=Order, instance=order)

def update_order(order):
    order.save()
    # Send robust
    post_save.send_robust(sender=Order, instance=order, created=False)
```

Create `tests/test_signal_scanner/fixtures/celery_sends.py`:

```python
from celery.signals import task_sent

def dispatch_task():
    # Send Celery signal
    task_sent.send(sender='tasks.process_order', task_id='123')
```

### New Tests

- `test_parse_signal_send()`: Unit test for send parsing
- `test_parse_signal_send_robust()`: Unit test for send_robust
- `test_detect_django_signal_sends()`: Integration test
- `test_detect_celery_signal_sends()`: Integration test
- `test_signal_usage_tracking()`: Verify usages list completeness
- `test_backward_compatibility()`: Verify --simple flag works

### Modified Tests

Update existing tests to expect new data structure:

- `test_integration.py`: Update assertions for receivers/senders/usages
- `test_export.py`: Update YAML output expectations
- `test_cli.py`: Add tests for new CLI flags

## Migration Guide

### For Users

**Old Output:**

```yaml
django:
  model_signals:
    post_save:
      - handler: order_created
        file: handlers.py
        line: 10
```

**New Output:**

```yaml
django:
  model_signals:
    post_save:
      receivers:
        - handler: order_created
          file: handlers.py
          line: 10
      senders:
        - file: views.py
          line: 25
      usages:
        - file: handlers.py
          line: 10
          pattern: receiver_decorator
        - file: views.py
          line: 25
          pattern: send_method
```

**Backward Compatibility:**

```bash
# Use old format
upcast scan-signals path/ --simple

# New default behavior
upcast scan-signals path/
```

## Performance Considerations

### AST Traversal

- **Current**: Two passes through AST
- **New**: Three passes through AST
- **Impact**: ~20-30% increase in scanning time (acceptable for typical codebases)

**Optimization Opportunities:**

1. Cache AST nodes for reuse across passes
2. Use specialized node filters (e.g., only Call nodes for send detection)
3. Skip send detection if not needed (future: `--receivers-only` flag)

### Memory Usage

- **Additional data**: ~100-200 bytes per usage
- **Typical codebase**: 50-200 signal usages
- **Total impact**: <50KB additional memory (negligible)

## Documentation Updates

### CLI Help

```bash
$ upcast scan-signals --help

Scan for Django and Celery signal usage.

Detects:
  • Signal receivers (@receiver, .connect())
  • Signal sends (.send(), .send_robust())
  • Custom signal definitions

Options:
  --simple          Use simplified output (receivers only, backward compatible)
  --receivers-only  Only detect receivers, skip send detection
  --senders-only    Only detect senders, skip receiver detection
```

### Examples

Add example showing send detection:

```bash
# Full scan (receivers + senders)
$ upcast scan-signals src/ -v

# Only find where signals are sent
$ upcast scan-signals src/ --senders-only -o sends.yaml

# Backward compatible mode
$ upcast scan-signals src/ --simple
```

## Risks & Mitigation

| Risk                              | Probability | Impact | Mitigation                                   |
| --------------------------------- | ----------- | ------ | -------------------------------------------- |
| Breaking changes affect users     | Medium      | High   | Provide --simple flag, migration guide       |
| Performance regression            | Low         | Medium | Benchmark and optimize, add --receivers-only |
| False positives in send detection | Medium      | Low    | Strict import tracking, add tests            |
| Complexity increase               | Medium      | Medium | Clear code documentation, refactor if needed |

## Future Enhancements

1. **Signal flow visualization**: Generate graphs showing send→receive relationships
2. **Usage statistics**: Frequency analysis, unused signal detection
3. **Performance profiling**: Integration with runtime profiling tools
4. **Dead signal detection**: Find signals that are only sent or only received
5. **Signal documentation**: Extract docstrings from handlers
