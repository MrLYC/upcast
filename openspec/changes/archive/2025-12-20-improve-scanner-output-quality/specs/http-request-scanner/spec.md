# http-request-scanner Specification Delta

## ADDED Requirements

### Requirement: URL Placeholder Normalization

The system SHALL merge consecutive ellipsis placeholders in URLs to reduce redundancy and improve readability.

#### Scenario: Merge consecutive placeholders

- **WHEN** constructing a URL with multiple unresolvable parts
- **AND** these parts result in consecutive `...` placeholders like `"... + ..."`
- **THEN** the system SHALL normalize to a single `...`
- **AND** produce cleaner output like `"https://example.com/..."`
- **AND** NOT output `"https://example.com/... + ..."`

#### Scenario: Preserve intermediate known parts

- **WHEN** constructing a URL like `"... + /api/ + ..."`
- **THEN** the system SHALL preserve the known `/api/` part
- **AND** only merge consecutive unknown parts
- **AND** output `"... + /api/ + ..."`

#### Scenario: Single placeholder unchanged

- **WHEN** a URL has only one `...` placeholder
- **THEN** the system SHALL keep it unchanged
- **AND** NOT modify URLs without consecutive placeholders

**Implementation**: Apply regex pattern `r'\.\.\.(\s*\+\s*\.\.\.)+` to replace multiple consecutive `... + ...` with a single `...`.

**Rationale**: Multiple adjacent `...` convey the same meaning as a single `...` but add noise. Single placeholder is cleaner and more readable.
