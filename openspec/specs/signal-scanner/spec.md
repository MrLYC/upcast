# signal-scanner Specification

## Purpose

TBD - created by archiving change improve-scanner-output-quality. Update Purpose after archive.

## Requirements

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

### Requirement: Strongly Typed Signal Models

The signal scanner SHALL use Pydantic models for all output components with proper type validation.

#### Scenario: SignalInfo model validates signal data

- **GIVEN** signal information from code analysis
- **WHEN** creating SignalInfo instance
- **THEN** the system SHALL validate required fields (name, type, file, line)
- **AND** SHALL enforce type field values (built-in, custom)
- **AND** SHALL reject invalid data

#### Scenario: SignalReceiver model validates receiver data

- **GIVEN** signal receiver information
- **WHEN** creating SignalReceiver instance
- **THEN** the system SHALL validate function, file, line fields
- **AND** SHALL ensure line is positive integer

#### Scenario: SignalSummary includes scanner-specific metrics

- **GIVEN** signal scanning complete
- **WHEN** creating SignalSummary
- **THEN** summary SHALL include built_in_signals count
- **AND** SHALL include custom_signals count
- **AND** SHALL include total_receivers count
- **AND** SHALL include base fields (total_count, files_scanned)

---

### Requirement: Signal Output Serialization Support

The signal scanner output SHALL be serializable to JSON and YAML formats with round-trip compatibility.

#### Scenario: Serialize to JSON

- **GIVEN** a SignalOutput instance
- **WHEN** calling output.to_json()
- **THEN** the system SHALL produce valid JSON string
- **AND** JSON SHALL contain summary, results, metadata

#### Scenario: Deserialize from JSON

- **GIVEN** JSON string from serialized SignalOutput
- **WHEN** calling SignalOutput.model_validate_json(json_str)
- **THEN** the system SHALL reconstruct SignalOutput instance
- **AND** reconstructed output SHALL equal original

#### Scenario: Serialize to dict for YAML

- **GIVEN** a SignalOutput instance
- **WHEN** calling output.to_dict()
- **THEN** the system SHALL produce dict with proper structure
- **AND** dict SHALL be YAML-serializable
