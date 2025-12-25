# concurrency-pattern-scanner Specification Delta

## MODIFIED Requirements

### Requirement: Asyncio Pattern Detection

The system SHALL detect asyncio.create_task() patterns and extract meaningful coroutine information.

#### Scenario: Skip unknown coroutines

- **WHEN** analyzing an `asyncio.create_task()` call
- **AND** the coroutine argument cannot be resolved to a specific function
- **THEN** the system SHALL skip this detection entirely
- **AND** NOT output a record with `coroutine: "unknown"`
- **AND** maintain output cleanliness by excluding low-value results

**Rationale**: Outputting `coroutine: "unknown"` provides no actionable information and clutters results. Better to skip these entries.

#### Scenario: Successful coroutine detection

- **WHEN** analyzing an `asyncio.create_task()` call
- **AND** the coroutine argument can be resolved to a specific function
- **THEN** the system SHALL output a complete pattern record
- **AND** include the resolved coroutine name
- **AND** provide file/line location information
