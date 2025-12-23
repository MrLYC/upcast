# HTTP Request Scanner Specification Delta

## MODIFIED Requirements

### Requirement: requests Library Detection

The system SHALL detect HTTP requests made via the requests library using astroid-based AST analysis.

#### Scenario: requests.post() with inferrable JSON parameters

- **WHEN** code uses `requests.post('https://api.example.com/login', json={'user': 'admin'})`
- **AND** json parameter is a literal dict or list
- **THEN** the system SHALL extract method as "POST"
- **AND** extract json_body as `{'user': 'admin'}`
- **AND** extract headers if present
- **AND** record all inferrable parameters

**Rationale**: Static literal values provide useful API contract information

**UNCHANGED**: Existing behavior for inferrable JSON bodies

#### Scenario: requests.post() with uninferrable JSON parameters

- **WHEN** code uses `requests.post(url, json=build_payload())` or `json=dynamic_var`
- **AND** json parameter value cannot be statically inferred
- **THEN** the system SHALL omit `json_body` field from output
- **AND** SHALL NOT output placeholder values like `{"<dynamic>": "..."}`
- **AND** SHALL include other inferrable parameters (url, method, headers, timeout)

**Rationale**: Omitting field is clearer than placeholder; users can check presence to determine if body was static

**DIFF**: Changed from outputting placeholder to omitting field entirely

### Requirement: Output Field Presence Semantics

The system SHALL use field presence/absence to indicate inference success.

#### Scenario: Optional json_body field

- **WHEN** outputting HTTP request usage
- **THEN** `json_body` field SHALL be optional in output model
- **AND** SHALL be present only when body content was successfully inferred
- **AND** SHALL be absent when inference failed or body is dynamic

**Rationale**: Field presence naturally expresses "we know this" vs "we don't know this"

**NEW**: Explicit optional field semantics

#### Scenario: Optional params field

- **WHEN** outputting HTTP request usage
- **THEN** `params` field SHALL follow same optional pattern
- **AND** SHALL be present only for inferrable query parameters
- **AND** SHALL be absent for dynamic or computed params

**Rationale**: Consistent optional field handling across all request parameters

**NEW**: Extends optional pattern to query params

#### Scenario: Optional headers field

- **WHEN** outputting HTTP request usage
- **THEN** `headers` field SHALL follow same optional pattern
- **AND** SHALL be present only for inferrable header dicts
- **AND** SHALL be absent for dynamic or session-based headers

**Rationale**: Complete consistency across all optional request components

**NEW**: Extends optional pattern to headers

## ADDED Requirements

### Requirement: Static Value Inference

The system SHALL attempt to infer static values from common patterns before marking as uninferrable.

#### Scenario: Infer from simple variable assignments

- **WHEN** json parameter is a variable reference
- **AND** variable is assigned a literal value earlier in same function
- **EXAMPLE**:
  ```python
  payload = {"action": "deploy", "env": "prod"}
  requests.post(url, json=payload)
  ```
- **THEN** the system SHOULD attempt to resolve payload value
- **AND** SHOULD include resolved value in json_body if successful
- **AND** SHALL omit field if resolution fails

**Rationale**: Simple data flow analysis can resolve common patterns without full static analysis

#### Scenario: Skip complex expressions

- **WHEN** json parameter involves:
  - Function calls
  - Comprehensions
  - Conditional expressions
  - Attribute access chains
- **THEN** the system SHALL skip inference
- **AND** SHALL omit json_body field
- **AND** SHALL NOT attempt complex static analysis

**Rationale**: Complex expressions are rarely inferrable without execution; better to omit than guess

## REMOVED Requirements

### Removed: Placeholder Value Output

#### Scenario: Output placeholder for uninferrable JSON (REMOVED)

- **REMOVED**: Requirement to output `{"<dynamic>": "..."}` for uninferrable bodies
- **Rationale**: Placeholders provide no useful information and clutter output

## MODIFIED Requirements

### Requirement: httpx Library Detection

The system SHALL detect HTTP requests made via the httpx library for both sync and async usage.

#### Scenario: httpx with parameters (updated)

- **WHEN** code uses `httpx.post('https://api.example.com', json={'data': 'value'})`
- **THEN** the system SHALL extract json_body as `{'data': 'value'}` if inferrable
- **AND** SHALL omit json_body if not inferrable (same as requests library)
- **AND** handle all parameters with same optional field pattern

**DIFF**: Updated to match new optional field behavior

### Requirement: aiohttp Library Detection

The system SHALL detect HTTP requests made via the aiohttp library for async usage.

#### Scenario: aiohttp with JSON data (updated)

- **WHEN** code uses `await session.post(url, json=data)`
- **THEN** the system SHALL apply same inference logic as requests
- **AND** SHALL omit json_body if data is not inferrable
- **AND** handle parameters consistently with other libraries

**DIFF**: Updated to match new optional field behavior
