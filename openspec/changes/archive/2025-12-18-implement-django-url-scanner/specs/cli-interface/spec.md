# cli-interface Specification

## MODIFIED Requirements

### Requirement: Consistent Command Naming

The system SHALL use a consistent naming pattern for all scanner commands following the `scan-*` convention.

#### Scenario: Add scan-django-urls command

- **WHEN** users need to scan Django URL patterns
- **THEN** the system SHALL provide `scan-django-urls` command
- **AND** follow the same `scan-*` naming convention as other scanners

**DIFF**: Added new scanner command for Django URLs
