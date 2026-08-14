## ADDED Requirements

### Requirement: Internal Django Route Reference Index

The system SHALL provide reusable internal utilities for connecting resolved Django view symbols to direct URL and DRF Router evidence.

#### Scenario: Index direct URL targets

- **WHEN** a URLconf contains a supported direct `path()` or `re_path()` target
- **THEN** the index SHALL preserve the target expression, resolved module/symbol identity when available, pattern, and source location
- **AND** distinguish a resolved target from an unresolved expression

#### Scenario: Index Router registration and mount evidence

- **WHEN** a supported DRF Router has registrations and a `.urls` mount
- **THEN** the index SHALL associate registrations with their mount evidence by Router variable identity
- **AND** preserve prefix, basename, Router type, ViewSet target, and source locations

#### Scenario: Preserve uncertain Router evidence

- **WHEN** a Router registration, target, or mount cannot be fully resolved
- **THEN** the index SHALL retain the raw expression and explicit status
- **AND** SHALL NOT fabricate a generated route URL or endpoint reachability conclusion
