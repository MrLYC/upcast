# django-settings-scanner Specification Delta

## MODIFIED Requirements

### Requirement: Settings Usage Context Extraction

The system SHALL extract complete statement context for Django settings usage, not just the settings attribute access.

#### Scenario: Extract full statement for assignments

- **WHEN** a settings value is used in an assignment like `debug = settings.DEBUG`
- **THEN** the `code` field SHALL contain the full assignment: `"debug = settings.DEBUG"`
- **AND** NOT just the attribute access: `"settings.DEBUG"`
- **AND** provide sufficient context to understand how the setting is used

#### Scenario: Extract full statement for conditionals

- **WHEN** a settings value is used in a conditional like `if settings.DEBUG: logger.setLevel(logging.DEBUG)`
- **THEN** the `code` field SHALL contain the full if statement
- **AND** include the condition and relevant body
- **AND** provide context about the conditional behavior

#### Scenario: Extract full statement for return statements

- **WHEN** a settings value is returned like `return settings.SITE_URL`
- **THEN** the `code` field SHALL contain `"return settings.SITE_URL"`
- **AND** NOT just `"settings.SITE_URL"`

#### Scenario: Extract full statement for expressions

- **WHEN** a settings value is used in an expression statement like `logger.info(settings.VERSION)`
- **THEN** the `code` field SHALL contain the full expression
- **AND** show the complete function call context

**Rationale**: Full statement context provides actionable information about how settings affect behavior. Just `settings.DEBUG` lacks context about usage patterns.

**Implementation Note**: Walk up AST from the settings attribute node to find the containing statement (Assign, Expr, Return, If, etc.), then extract that statement's source code.
