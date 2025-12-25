# signal-scanner Specification Delta

## NEW Requirements

### Requirement: Signal Scanner Module Location Updated

Signal scanner SHALL be located at `upcast.scanners.signal` instead of `upcast.signal_scanner`.

#### Scenario: Import from new location

- **GIVEN** code needs signal scanner functionality
- **WHEN** importing signal scanner
- **THEN** the system SHALL use `from upcast.scanners.signal import scan_signals`
- **AND** provide same functionality as before

#### Scenario: Old import path deprecated

- **GIVEN** code using `from upcast.signal_scanner import scan_signals`
- **WHEN** the import executes
- **THEN** the system SHALL emit DeprecationWarning
- **AND** still work correctly (backward compatibility)
- **AND** warning SHALL indicate new path and removal version

---

### Requirement: Signal Scanner Output Structure Unified

Signal scanner output SHALL use `SignalOutput` Pydantic model with `summary`, `results`, and `metadata` instead of dict with `signals` key.

#### Scenario: New output has required structure

- **GIVEN** signal scanner run on a project
- **WHEN** inspecting output
- **THEN** the output SHALL be a `SignalOutput` instance
- **AND** SHALL have summary field with ScannerSummary type
- **AND** SHALL have results field with signals list
- **AND** SHALL have metadata field

#### Scenario: Summary contains base and signal-specific fields

- **GIVEN** signal scanner output
- **WHEN** accessing summary
- **THEN** summary SHALL have total_count, files_scanned, scan_duration_ms (base fields)
- **AND** MAY have built_in_signals, custom_signals, total_receivers (signal-specific fields)

#### Scenario: Results structure contains signals list

- **GIVEN** signal scanner output
- **WHEN** accessing results
- **THEN** results SHALL have "signals" key
- **AND** value SHALL be list of SignalInfo objects

---

## ADDED Requirements

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
