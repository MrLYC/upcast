## ADDED Requirements

### Requirement: Queue Scanner Uses Common Architecture

The queue usage scanner SHALL extend `BaseScanner`, use the shared Python file filtering behavior, and return the common summary/results/metadata wrapper.

#### Scenario: Apply file filters

- **WHEN** `scan-queue-usage` receives include or exclude patterns
- **THEN** the scanner SHALL apply them through the common file collection path
- **AND** findings outside the selected files SHALL be omitted
