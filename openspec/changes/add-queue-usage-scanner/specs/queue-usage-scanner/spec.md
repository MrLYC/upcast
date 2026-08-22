## ADDED Requirements

### Requirement: Queue Usage CLI

The system SHALL provide a `scan-queue-usage` command using the standard scanner path, output, format, include, exclude, and verbose options.

#### Scenario: Scan a project

- **WHEN** the user runs `upcast scan-queue-usage <path>`
- **THEN** the command SHALL emit YAML by default
- **AND** the output SHALL contain `summary`, `results`, and `metadata`

#### Scenario: Write JSON output

- **WHEN** the user supplies `--format json --output <file>`
- **THEN** the command SHALL write valid JSON to the requested file
- **AND** the existing scanner output wrapper SHALL be preserved

### Requirement: Supported Queue Categories

The scanner SHALL detect statically confirmed usage in the following categories: in-process queues (`queue`, `asyncio`, and `multiprocessing`), task queues (Celery, RQ, Dramatiq, and Huey), Redis List/Stream APIs, Kafka clients, and RabbitMQ/Kombu APIs.

#### Scenario: Recognize imported queue APIs

- **WHEN** a supported API is imported directly or through a module alias
- **THEN** the scanner SHALL emit a finding with the concrete framework, category, operation, source location, and statement
- **AND** it SHALL NOT classify an unrelated same-name API without import evidence

### Requirement: Parameter and Hardcoding Evidence

Each queue finding SHALL expose relevant parameters with the original expression, best-effort static value, source kind, and parameter-level `hardcoded` status.

#### Scenario: Literal queue parameter

- **WHEN** a queue name, capacity, topic, routing key, or equivalent parameter is a literal or resolvable literal constant
- **THEN** its parameter record SHALL set `hardcoded` to `true`

#### Scenario: Configuration or runtime queue parameter

- **WHEN** a parameter comes from an environment/configuration lookup or function/runtime input
- **THEN** its parameter record SHALL set `hardcoded` to `false` or `unknown` according to whether the source is known dynamic or unresolved
- **AND** the scanner SHALL preserve the source expression

#### Scenario: Mixed parameters

- **WHEN** one finding contains both literal and dynamic parameters
- **THEN** each parameter SHALL retain its own status
- **AND** the finding SHALL expose an aggregate hardcoding status without replacing parameter-level evidence

### Requirement: Stable and Safe Output

The scanner SHALL produce deterministic results and SHALL NOT expose obvious credential values captured from queue connection parameters.

#### Scenario: Credential-bearing connection

- **WHEN** a connection parameter contains a password, token, secret, or URL userinfo
- **THEN** the output SHALL redact its static value and expression value
- **AND** retain the parameter name and source location

#### Scenario: Static-analysis boundary

- **WHEN** the scanner completes
- **THEN** summary counts SHALL describe source findings only
- **AND** the output SHALL not claim runtime queue depth, lag, throughput, latency, or consumer health
