# signal-scanner Specification Delta

## MODIFIED Requirements

### Requirement: Signal Output Format Standardization

The system SHALL use a flat list output format consistent with other scanner commands instead of nested dictionaries.

#### Scenario: Flat list structure

- **WHEN** outputting detected signals
- **THEN** the system SHALL use a top-level `signals` key with a list value
- **AND** each signal SHALL be a dictionary in the list
- **AND** NOT use nested dictionaries by signal type and name

**Output Format**:

```yaml
signals:
  - signal: django.db.models.signals.post_save
    category: model_signals
    type: django
    receivers:
      - handler: handle_post_save
        file: app/handlers.py
        lineno: 10

  - signal: myapp.signals.custom_signal
    category: custom_signals
    type: django
    receivers:
      - handler: process_custom_signal
        file: app/handlers.py
        lineno: 25
```

#### Scenario: Consistency with other scanners

- **GIVEN** the new flat list format
- **WHEN** comparing with http-request-scanner or exception-handler-scanner output
- **THEN** the structure SHALL follow similar patterns
- **AND** use a top-level key with list of records
- **AND** enable consistent iteration/processing across scanners

#### Scenario: Signal categorization

- **WHEN** outputting a signal
- **THEN** include a `category` field (e.g., "model_signals", "custom_signals")
- **AND** include a `type` field (e.g., "django")
- **AND** include the full qualified `signal` name
- **AND** provide sufficient metadata for filtering/grouping

**Rationale**: Nested dict structure differs from other scanners and makes iteration more complex. Flat list is easier to process programmatically and more consistent with project patterns.

**Breaking Change**: Existing tools parsing signal-scanner output will need updates. The structure changes significantly from nested dicts to a flat list.
