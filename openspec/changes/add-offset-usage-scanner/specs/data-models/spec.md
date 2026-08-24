## ADDED Requirements

### Requirement: Typed Offset Usage Output

The scanner SHALL expose Pydantic models for parameter evidence, offset findings, summary counts, and the complete scanner output.

#### Scenario: Output follows shared scanner shape

- **WHEN** the scanner returns results
- **THEN** the output SHALL include `summary`, `results`, and `metadata`
- **AND** the summary SHALL include the shared total count, files scanned, and scan duration fields

#### Scenario: Parameter evidence is explicit

- **WHEN** an offset, limit, page, or page-size expression is available
- **THEN** the model SHALL preserve its source expression, best-effort static value, source kind, and nullable hardcoded status

#### Scenario: Findings are grouped predictably

- **WHEN** findings are serialized
- **THEN** results SHALL be grouped by a stable pattern/category key and sorted deterministically by source location
