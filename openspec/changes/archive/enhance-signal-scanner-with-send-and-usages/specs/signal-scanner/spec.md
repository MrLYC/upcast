# signal-scanner Specification (Delta)

## MODIFIED Requirements

### Requirement: Signal Usage Tracking

The system SHALL track all signal usages (both sending and receiving) using a unified Usage pattern.

#### Scenario: Record signal receiver as usage

- **WHEN** detecting a signal receiver via @receiver or .connect()
- **THEN** the system SHALL create a SignalUsage object
- **AND** set pattern to "receiver_decorator" or "connect_method"
- **AND** record file path (relative to project root)
- **AND** record line number and column offset
- **AND** extract source code snippet
- **AND** add usage to signal's usages list

**DIFF**: Modified to use Usage pattern instead of simple handler dict

#### Scenario: Record signal send as usage

- **WHEN** detecting a signal.send() or signal.send_robust() call
- **THEN** the system SHALL create a SignalUsage object
- **AND** set pattern to "send_method" or "send_robust_method"
- **AND** record file path, line, column
- **AND** extract source code snippet including sender parameter
- **AND** add usage to signal's usages list

**DIFF**: Added send detection and usage tracking

#### Scenario: Organize usages by signal

- **WHEN** collecting usages for a signal
- **THEN** the system SHALL group by framework (django/celery)
- **AND** group by category (model_signals/task_signals/etc)
- **AND** group by signal name
- **AND** provide separate lists for receivers, senders, and all usages

**DIFF**: Added structured organization with receivers/senders/usages

## ADDED Requirements

### Requirement: Signal Send Validation

The system SHALL validate that .send() calls are on actual signals to prevent false positives from other objects with send methods.

#### Scenario: Build known signals whitelist

- **WHEN** collecting signal sends in third pass
- **THEN** the system SHALL first build a known signals set containing:
  - All signal names from django_imports (e.g., post_save, pre_delete)
  - All signal names from celery_imports (e.g., task_sent, worker_ready)
  - All custom signal names from custom_signals dict
  - All signal names that have registered receivers
- **AND** use this whitelist to validate send calls

**DIFF**: New validation whitelist requirement

#### Scenario: Validate send call against whitelist

- **WHEN** detecting a potential `.send()` or `.send_robust()` call
- **THEN** the system SHALL extract the object name calling send
- **AND** check if object name exists in known signals whitelist
- **AND** if NOT in whitelist, SHALL reject and not record as signal send
- **AND** if in whitelist, SHALL proceed with SignalUsage creation

**DIFF**: Strict validation to prevent false positives

#### Scenario: Handle ambiguous cases

- **WHEN** a signal is imported with an alias (e.g., `from signals import post_save as ps`)
- **THEN** the system SHALL track the alias in imports
- **AND** validate send calls using the alias name
- **WHEN** a variable holds a signal reference (e.g., `sig = post_save`)
- **THEN** the system MAY NOT detect the send if variable not tracked
- **AND** this is acceptable to avoid false positives

**DIFF**: Conservative approach prioritizing precision over recall

### Requirement: Signal Send Detection

The system SHALL detect signal send operations for both Django and Celery signals.

#### Scenario: Detect Django signal.send() call

- **WHEN** scanning code containing `signal_name.send(sender=Model, **kwargs)`
- **THEN** the system SHALL validate signal_name is a known signal
- **AND** check signal_name exists in django_imports OR custom_signals OR known receivers
- **AND** reject if signal_name not in any known signals list (avoid false positives)
- **AND** identify the signal name only if validated
- **AND** extract the sender parameter if provided
- **AND** record file path and line number
- **AND** extract the full send call code snippet
- **AND** categorize under appropriate signal category
- **AND** add to signal's senders list

**DIFF**: New requirement for Django signal send detection with validation

#### Scenario: Reject non-signal send calls

- **WHEN** scanning code containing `.send()` on non-signal objects
- **THEN** the system SHALL validate the object is a known signal
- **AND** if object name not in django_imports, celery_imports, custom_signals, or known receivers
- **THEN** the system SHALL NOT create a SignalUsage
- **AND** SHALL NOT add to senders list

**Examples of rejected patterns:**

- `mail.send()` - email sending, not a signal
- `message.send()` - message sending, not a signal
- `client.send(data)` - network sending, not a signal
- `socket.send()` - socket operation, not a signal

**DIFF**: New validation requirement to prevent false positives

#### Scenario: Detect Django signal.send_robust() call

- **WHEN** scanning code containing `signal_name.send_robust(sender=Model, **kwargs)`
- **THEN** the system SHALL identify the signal name
- **AND** extract the sender parameter if provided
- **AND** record with pattern "send_robust_method"
- **AND** distinguish from regular send in usage pattern

**DIFF**: New requirement for send_robust detection

#### Scenario: Detect Celery signal.send() call

- **WHEN** scanning code containing `celery_signal.send(sender='task_name', **kwargs)`
- **THEN** the system SHALL identify the Celery signal name
- **AND** extract the sender parameter
- **AND** record file location
- **AND** categorize under appropriate Celery signal category
- **AND** add to signal's senders list

**DIFF**: New requirement for Celery signal send detection

#### Scenario: Detect custom signal send

- **WHEN** scanning send calls on custom Signal() instances
- **THEN** the system SHALL resolve signal name from custom_signals tracking
- **AND** detect send calls on the custom signal variable
- **AND** record as custom signal send
- **AND** include in signal's senders and usages lists

**DIFF**: Support custom signal send detection

### Requirement: SignalUsage Data Structure

The system SHALL use a unified SignalUsage data structure for all signal usage tracking.

#### Scenario: Create SignalUsage for receiver

- **WHEN** detecting a signal receiver
- **THEN** the SignalUsage SHALL contain:
  - file: relative path from project root
  - line: 1-based line number
  - column: 0-based column offset
  - pattern: "receiver_decorator" or "connect_method"
  - code: source code snippet
  - sender: sender value if specified, else None

**DIFF**: Standardized usage structure

#### Scenario: Create SignalUsage for send

- **WHEN** detecting a signal send
- **THEN** the SignalUsage SHALL contain:
  - file: relative path from project root
  - line: 1-based line number
  - column: 0-based column offset
  - pattern: "send_method" or "send_robust_method"
  - code: source code snippet including full call
  - sender: sender parameter value

**DIFF**: Send usage structure matching receiver pattern

### Requirement: Three-Pass Scanning

The system SHALL use a three-pass scanning strategy to collect all signal information.

#### Scenario: Execute three-pass scan

- **WHEN** scanning a Python module
- **THEN** the system SHALL execute in order:
  1. First pass: collect imports and custom signal definitions
  2. Second pass: collect signal receivers (@receiver, .connect)
  3. Third pass: collect signal sends (.send, .send_robust)
- **AND** each pass MAY reference data from previous passes

**DIFF**: Added third pass for send detection

#### Scenario: Resolve signal names across passes

- **WHEN** detecting a send call on a signal
- **THEN** the system SHALL check django_imports for built-in signals
- **AND** check celery_imports for Celery signals
- **AND** check custom_signals from first pass for custom signals
- **AND** correctly categorize based on signal type

**DIFF**: Cross-pass data dependencies for accurate detection

### Requirement: Structured Output with Receivers and Senders

The system SHALL organize output to separate receivers from senders while maintaining all usages.

#### Scenario: Format signal output with receivers and senders

- **WHEN** generating output for a signal
- **THEN** the output SHALL include:
  - receivers: list of handler registrations
  - senders: list of send call sites
  - usages: combined list of all usages (receivers + senders)
- **AND** each list SHALL be sorted by file path then line number

**DIFF**: Structured output replacing flat handler list

#### Scenario: Export receivers list

- **WHEN** exporting receivers list for a signal
- **THEN** each receiver entry SHALL include:
  - handler: function/method name
  - file: relative file path
  - line: line number
  - sender: sender filter if specified
  - pattern: detection pattern type

**DIFF**: Enhanced receiver information

#### Scenario: Export senders list

- **WHEN** exporting senders list for a signal
- **THEN** each sender entry SHALL include:
  - file: relative file path
  - line: line number
  - sender: sender parameter from send call
  - pattern: "send_method" or "send_robust_method"

**DIFF**: New senders list in output

#### Scenario: Export usages list

- **WHEN** exporting usages list for a signal
- **THEN** each usage entry SHALL include:
  - file: relative file path
  - line: line number
  - column: column offset
  - pattern: usage pattern type
  - code: source code snippet
  - sender: sender value if applicable

**DIFF**: Detailed usage list with code context

### Requirement: Backward Compatibility

The system SHALL provide backward compatible output format via command-line flag.

#### Scenario: Use simple output mode

- **WHEN** running scan-signals with --simple flag
- **THEN** the system SHALL output only receivers in flat list format
- **AND** omit senders and usages lists
- **AND** maintain compatibility with pre-enhancement output format

**DIFF**: Backward compatibility for existing users

#### Scenario: Default to enhanced output

- **WHEN** running scan-signals without --simple flag
- **THEN** the system SHALL output enhanced format with receivers/senders/usages
- **AND** provide complete signal lifecycle view

**DIFF**: New default behavior with opt-in to old format

## MODIFIED Requirements (continued)

### Requirement: Signal Scanner CLI

The system SHALL provide CLI interface for signal scanning with send detection options.

#### Scenario: Display send detection in help

- **WHEN** running `upcast scan-signals --help`
- **THEN** help text SHALL mention:
  - Detection of receivers (@receiver, .connect)
  - Detection of senders (.send, .send_robust)
  - Custom signal definitions
  - --simple flag for backward compatibility

**DIFF**: Updated help text for new capabilities

#### Scenario: Show sender statistics in summary

- **WHEN** running scan-signals with -v/--verbose
- **THEN** summary SHALL display:
  - Total receivers count
  - Total senders count (NEW)
  - Signals with no receivers (NEW: receive-only signals)
  - Signals with no senders (NEW: send-only signals)
  - Custom signals defined

**DIFF**: Enhanced summary with send statistics

## MODIFIED Requirements (Test Coverage)

### Requirement: Test Fixtures

The system SHALL provide test fixtures covering send and receive patterns.

#### Scenario: Provide signal send fixtures

- **WHEN** testing signal send detection
- **THEN** fixtures SHALL include:
  - Django signal.send() calls with various sender types
  - Django signal.send_robust() calls
  - Celery signal.send() calls
  - Custom signal send calls
  - Mixed send and receive patterns in same file

**DIFF**: Added send pattern fixtures

## Implementation Notes

### Import Tracking Requirements

- Must track signal imports in first pass
- Send detection requires matching send calls to known signals
- Custom signals must be defined before send calls can be detected

### Performance Considerations

- Third pass should filter for Call nodes only
- Reuse parsed module AST across passes
- Typical overhead: 20-30% increase in scan time

### Data Structure Migration

Old format (flat list):

```python
signals["django"]["model_signals"]["post_save"] = [handler1, handler2]
```

New format (structured):

```python
signals["django"]["model_signals"]["post_save"] = {
    "receivers": [handler1, handler2],
    "senders": [send1, send2],
    "usages": [usage1, usage2, usage3, usage4],
}
```

### Pattern Type Mapping

- `"receiver_decorator"` ← @receiver(signal)
- `"connect_method"` ← signal.connect(handler)
- `"celery_connect_decorator"` ← @signal.connect
- `"send_method"` ← signal.send()
- `"send_robust_method"` ← signal.send_robust()
