## ADDED Requirements

### Requirement: Typed Queue Usage Output

Queue usage findings SHALL use Pydantic models compatible with the common `ScannerOutput` and `ScannerSummary` contracts.

#### Scenario: Serialize queue parameters

- **WHEN** a queue usage finding is serialized
- **THEN** it SHALL include typed source location, framework, operation, parameter evidence, and hardcoding status
- **AND** summary counts SHALL be non-negative and consistent with the result collection
