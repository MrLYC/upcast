## ADDED Requirements

### Requirement: Hybrid Migration Command Parity

The system SHALL preserve the public scanner command interface while scanner implementations migrate onto the hybrid pipeline.

#### Scenario: Keep scanner command surface stable during migration

- **WHEN** a scanner command adopts the hybrid pipeline internally
- **THEN** the command name, standard CLI options, and output format flags SHALL remain compatible with the existing CLI contract
- **AND** the migration SHALL NOT require users to switch to a new command group or alternate command name

#### Scenario: Preserve command-specific option behavior during migration

- **WHEN** validating a migrated scanner command
- **THEN** the system SHALL compare the legacy and migrated command behavior for command-specific options such as threshold, sensitivity, include-private, or scanner-specific verbose output
- **AND** unexpected output differences SHALL be treated as migration regressions until reviewed explicitly
