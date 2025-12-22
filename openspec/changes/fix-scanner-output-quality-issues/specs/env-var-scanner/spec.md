# Env Var Scanner Specification Delta

## MODIFIED Requirements

### Requirement: Environment Variable Detection

The system SHALL detect environment variable access patterns using semantic AST analysis with astroid.

#### Scenario: Context-validated os.getenv() detection

- **WHEN** code uses `os.getenv('VAR_NAME')`
- **THEN** the system SHALL verify the string 'VAR_NAME' is used as argument to getenv()
- **AND** SHALL verify parent node context is a Call to os.getenv or equivalent
- **AND** SHALL identify "VAR_NAME" as an environment variable only if validation passes
- **AND** mark it as not required (has implicit None default)
- **AND** record the file location and statement

**Rationale**: Context validation prevents false positives from strings in unrelated contexts

**DIFF**: Added explicit context validation requirement

#### Scenario: Reject strings from non-env contexts

- **WHEN** string literal appears in source code
- **AND** string is not an argument to env access function
- **EXAMPLES**:
  - API endpoint: `api.post('/api/config/', {'key': 'A1'})`
  - Dict key access: `data['environment']`
  - Logging: `logger.info('Checking variable: %s', name)`
  - Configuration: `config = {'id': 123}`
- **THEN** the system SHALL NOT report these strings as environment variables
- **AND** SHALL skip them during extraction
- **AND** SHALL log debug message about context mismatch if verbose mode enabled

**Rationale**: Many strings in code look like env var names but are used in different contexts

**NEW**: Explicit requirement to filter non-env contexts

### Requirement: Django-environ Pattern Detection

The system SHALL detect and parse django-environ library patterns with type extraction.

#### Scenario: Context-validated env() method detection

- **WHEN** code uses `env.str('VAR_NAME')` or similar
- **THEN** the system SHALL verify 'VAR_NAME' is argument to env.\* method call
- **AND** SHALL verify the method is called on an `Env` instance from django-environ
- **AND** extract the type from the method name
- **AND** record the type as 'str', 'int', 'bool', etc.
- **AND** mark as required if no default provided

**Rationale**: Same context validation principle applied to django-environ patterns

**DIFF**: Added context validation for django-environ calls

## ADDED Requirements

### Requirement: Parent Node Context Validation

The system SHALL validate parent node context before reporting environment variables.

#### Scenario: Verify Call node ancestry

- **WHEN** extracting variable name from string literal
- **THEN** the system SHALL traverse AST upward to find parent Call node
- **AND** SHALL verify Call node is one of:
  - `os.getenv(string_arg)`
  - `os.environ.get(string_arg)`
  - `env(string_arg)` or `env.TYPE(string_arg)`
  - Other registered env access patterns
- **AND** SHALL verify string literal is the variable name argument (typically first arg)
- **AND** SHALL reject string if no matching Call pattern found

**Rationale**: AST structure provides reliable context information to filter false positives

#### Scenario: Handle subscript access context

- **WHEN** string appears in subscript: `os.environ['VAR_NAME']`
- **THEN** the system SHALL verify parent is Subscript node
- **AND** SHALL verify Subscript.value resolves to `os.environ`
- **AND** SHALL accept this as valid env var context
- **DIFF**: Dict subscript is valid env access pattern; other subscripts are not

#### Scenario: Log rejected strings in verbose mode

- **WHEN** string literal looks like env var name but fails context validation
- **AND** verbose mode is enabled
- **THEN** the system SHALL log debug message with:
  - String value
  - File and line location
  - Parent node type
  - Reason for rejection
- **AND** SHALL NOT output this string in results

**Rationale**: Debugging support helps understand and refine filter logic

## REMOVED Requirements

None - all requirements remain with enhanced validation.
