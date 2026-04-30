## ADDED Requirements

### Requirement: Scanner Migration Parity Verification

The system SHALL verify scanner-command migration through old-vs-new comparisons at the public CLI boundary.

#### Scenario: Compare legacy and migrated scanner output

- **WHEN** a scanner command is migrated to the hybrid pipeline
- **THEN** the system SHALL compare legacy and migrated behavior through `upcast.main:main`
- **AND** the comparison SHALL cover exit code, default YAML output, JSON/file output, and normalized result content

#### Scenario: Run command-specific parity checks

- **WHEN** validating a migrated scanner command that has unique options or side effects
- **THEN** the system SHALL include command-specific parity checks for those options or side effects
- **AND** the comparison SHALL document any intentional differences before the migration is accepted
