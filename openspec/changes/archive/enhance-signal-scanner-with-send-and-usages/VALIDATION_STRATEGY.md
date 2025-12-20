# Signal Send Validation Strategy

## Problem: False Positives from .send() Method

The `.send()` method is not unique to signals. Many Python objects have this method:

```python
# Email sending
from django.core.mail import EmailMessage
mail = EmailMessage(...)
mail.send()  # ❌ NOT a signal

# Message sending
from channels.layers import get_channel_layer
channel_layer.send('room', {'type': 'chat'})  # ❌ NOT a signal

# HTTP client
import requests
session = requests.Session()
session.send(request)  # ❌ NOT a signal

# Socket operations
import socket
sock = socket.socket()
sock.send(data)  # ❌ NOT a signal

# Celery tasks (different from signals)
from celery import current_app
current_app.send_task('tasks.process')  # ❌ NOT a signal (it's a task dispatch)
```

Without validation, naive detection would incorrectly identify all these as signal sends.

## Solution: Known Signals Whitelist

The scanner builds a whitelist of known signals from four sources:

### 1. Django Built-in Signal Imports

```python
from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.core.signals import request_finished
from django.dispatch import receiver

# These are tracked in django_imports set
# Any .send() call on these names is valid
post_save.send(sender=Order, instance=order)  # ✅ Valid
```

**Tracked Django signals:**

- Model signals: `pre_init`, `post_init`, `pre_save`, `post_save`, `pre_delete`, `post_delete`, `m2m_changed`
- Request signals: `request_started`, `request_finished`, `got_request_exception`
- Management signals: `pre_migrate`, `post_migrate`
- Test signals: `setting_changed`, `template_rendered`

### 2. Celery Built-in Signal Imports

```python
from celery.signals import task_prerun, task_postrun, task_failure

# These are tracked in celery_imports set
task_failure.send(sender='tasks.process_order', task_id='123')  # ✅ Valid
```

**Tracked Celery signals:**

- Task signals: `task_prerun`, `task_postrun`, `task_success`, `task_failure`, `task_retry`, `task_revoked`, `task_rejected`, `task_unknown`
- Worker signals: `worker_init`, `worker_ready`, `worker_process_init`, `worker_shutdown`, `worker_process_shutdown`
- Beat signals: `beat_init`, `beat_embedded_init`

### 3. Custom Signal Definitions

```python
from django.dispatch import Signal

# First pass collects these
order_paid = Signal()  # Tracked in custom_signals dict
payment_failed = Signal()

# Second/third pass can validate against them
order_paid.send(sender=Order, instance=order)  # ✅ Valid
```

### 4. Signals with Registered Receivers

```python
# If a signal has receivers, it's likely a valid signal
@receiver(some_signal)
def handler(sender, **kwargs):
    pass

# Even if we didn't catch the import, we know some_signal exists
# because it has a receiver
some_signal.send(sender=MyModel)  # ✅ Valid (has receiver)
```

## Validation Algorithm

```python
def is_valid_signal_send(call_node, context):
    """
    Validate that a .send() call is on an actual signal.

    Returns True only if the object calling .send() is in the
    known signals whitelist.
    """
    # Extract object name (e.g., "post_save" from "post_save.send(...)")
    signal_name = extract_signal_name_from_call(call_node)
    if not signal_name:
        return False

    # Check against all known signal sources
    if signal_name in context.django_imports:
        return True  # Django built-in signal

    if signal_name in context.celery_imports:
        return True  # Celery built-in signal

    if signal_name in context.custom_signals:
        return True  # User-defined custom signal

    if signal_name in context.known_signal_names_from_receivers:
        return True  # Signal has receivers, likely valid

    # Not in any known signals list - reject
    return False
```

## Examples: Valid vs Invalid

### ✅ Valid Signal Sends (Will Be Detected)

```python
from django.db.models.signals import post_save, pre_delete
from myapp.signals import order_paid, payment_failed
from celery.signals import task_sent

# Django built-in signals
post_save.send(sender=Order, instance=order, created=True)
post_save.send_robust(sender=Product, instance=product)
pre_delete.send(sender=User, instance=user)

# Custom signals
order_paid.send(sender=Order, instance=order, amount=100)
payment_failed.send(sender=Order, instance=order, error='timeout')

# Celery signals
task_sent.send(sender='tasks.process_order', task_id='abc123')
```

### ❌ Invalid Sends (Will Be Rejected)

```python
from django.core.mail import EmailMessage, send_mail
from channels.layers import get_channel_layer
from requests import Session
import socket

# Email sending
mail = EmailMessage(subject='Test', body='Hello', to=['user@example.com'])
mail.send()  # REJECTED: 'mail' not in known signals

# Channel layer
channel = get_channel_layer()
channel.send('room_name', {'type': 'chat.message'})  # REJECTED: 'channel' not in known signals

# HTTP requests
session = Session()
session.send(request)  # REJECTED: 'session' not in known signals

# Sockets
sock = socket.socket()
sock.send(b'data')  # REJECTED: 'sock' not in known signals

# Message brokers (not signals)
from kombu import Connection
conn = Connection('amqp://localhost')
producer.send({'key': 'value'})  # REJECTED: 'producer' not in known signals
```

## Edge Cases

### Case 1: Signal with Alias

```python
from django.db.models.signals import post_save as ps

ps.send(sender=Order)  # ✅ Detected if alias tracked in imports
```

**Status**: Will be detected if import tracking handles aliases correctly.

### Case 2: Variable Reference

```python
from django.db.models.signals import post_save

signal = post_save  # Variable assignment
signal.send(sender=Order)  # ❓ May not be detected
```

**Status**: May not be detected (conservative approach). This is acceptable to avoid false positives.

**Recommendation**: Use signals directly, not through variable references:

```python
post_save.send(sender=Order)  # ✅ Preferred
```

### Case 3: Dynamic Signal Selection

```python
from django.db.models.signals import post_save, pre_delete

signals = [post_save, pre_delete]
for sig in signals:
    sig.send(sender=Order)  # ❓ May not be detected
```

**Status**: May not be detected (too complex for static analysis).

### Case 4: Signal Method Reference

```python
from django.db.models.signals import post_save

send_func = post_save.send
send_func(sender=Order)  # ❓ May not be detected
```

**Status**: May not be detected (requires data flow analysis).

## Trade-offs

### Precision vs Recall

**High Precision (chosen approach):**

- ➕ Very few false positives
- ➕ Clear and trustworthy results
- ➖ May miss complex edge cases

**High Recall (alternative):**

- ➕ Catches more signal sends
- ➖ Many false positives (mail.send, etc.)
- ➖ Confusing and unreliable results

**Decision**: Prioritize precision over recall. Better to miss a few edge cases than to pollute results with false positives.

## Future Enhancements

1. **Verbose Mode**: Show rejected .send() calls

   ```bash
   $ upcast scan-signals path/ --verbose-validation

   Rejected send calls:
   - mail.send() at views.py:45 (not in known signals)
   - client.send() at api.py:123 (not in known signals)
   ```

2. **Custom Signal Patterns**: Allow user configuration

   ```yaml
   # .upcast.yaml
   signal_scanner:
     additional_signal_names:
       - my_custom_signal
       - legacy_signal
   ```

3. **Data Flow Analysis**: Track variable assignments (advanced)
   ```python
   sig = post_save
   sig.send(...)  # Could be detected with data flow analysis
   ```

## Testing Strategy

### Unit Tests

- Test validation with known Django signals ✅
- Test validation with known Celery signals ✅
- Test validation with custom signals ✅
- Test rejection of non-signal .send() calls ✅
- Test import alias handling ✅

### Integration Tests

- Test full scan with mixed signal and non-signal sends ✅
- Verify no false positives from email, channels, requests ✅
- Verify detection of all valid signal types ✅

### Test Fixtures

Create `tests/test_signal_scanner/fixtures/send_validation.py`:

```python
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from myapp.signals import order_paid

def valid_signal_sends():
    # Should be detected
    post_save.send(sender=Order, instance=order)
    order_paid.send(sender=Order, instance=order)

def invalid_sends():
    # Should NOT be detected
    mail = EmailMessage()
    mail.send()

    import requests
    requests.Session().send(request)
```

## Documentation

### User Guide

Add to signal scanner documentation:

> **Note on .send() Detection**
>
> The scanner only detects `.send()` calls on known signals to avoid false positives.
> A signal is "known" if it is:
>
> - Imported from django.db.models.signals, django.core.signals, etc.
> - Imported from celery.signals
> - Defined as `Signal()` in your codebase
> - Referenced by a registered receiver
>
> For best results, import signals directly rather than storing them in variables:
>
> ```python
> # ✅ Good - will be detected
> from django.db.models.signals import post_save
> post_save.send(sender=Order)
>
> # ⚠️ May not be detected
> signal = post_save
> signal.send(sender=Order)
> ```

## Summary

The validation strategy ensures high-quality results by:

1. ✅ Building a comprehensive whitelist of known signals
2. ✅ Validating every .send() call against this whitelist
3. ✅ Rejecting calls on non-signal objects (mail, requests, etc.)
4. ✅ Providing clear and trustworthy scan results
5. ✅ Prioritizing precision over recall

This approach prevents false positives while maintaining good coverage of real signal usage patterns.
