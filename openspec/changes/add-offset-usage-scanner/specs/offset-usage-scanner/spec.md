## ADDED Requirements

### Requirement: Detect Common Offset-Producing Statements

The system SHALL provide a static scanner that identifies common Django ORM and Django REST Framework source patterns that can generate SQL offset pagination.

#### Scenario: QuerySet slice with offset

- **GIVEN** a Python file imports or uses a Django QuerySet expression
- **WHEN** the expression is sliced as `queryset[offset:offset + limit]` or an equivalent computed slice
- **THEN** the scanner SHALL report a `queryset_slice` finding
- **AND** preserve the lower and upper slice expressions

#### Scenario: Django Paginator page retrieval

- **GIVEN** a `django.core.paginator.Paginator` is constructed with a query-like object
- **WHEN** code calls `page()` or `get_page()` on that paginator
- **THEN** the scanner SHALL report an `indirect_pagination` finding
- **AND** include the configured page size and requested page expression when available

#### Scenario: DRF offset-capable pagination

- **GIVEN** code declares or configures `PageNumberPagination` or `LimitOffsetPagination`
- **WHEN** the scanner analyzes the class, view, or `REST_FRAMEWORK` setting
- **THEN** the scanner SHALL report the pagination declaration as an indirect offset finding
- **AND** distinguish page-number pagination from limit/offset pagination

#### Scenario: Raw SQL offset

- **GIVEN** code passes SQL text to `QuerySet.raw()`, `RawSQL`, or a database cursor execution API
- **WHEN** the statically inferable SQL contains `OFFSET` or a `LIMIT`/`OFFSET` pagination clause
- **THEN** the scanner SHALL report a `raw_sql` finding
- **AND** preserve whether the SQL and its offset/limit values are static or dynamic

#### Scenario: Exclude non-offset lookalikes

- **GIVEN** code slices an ordinary Python list or tuple, or declares DRF `CursorPagination`
- **WHEN** the scanner analyzes the code
- **THEN** it SHALL NOT report the expression as an offset usage

### Requirement: Report Offset Evidence and Risk Context

Each finding SHALL include its relative source file, line, column, statement, pattern, framework, operation, and any available offset, limit, page, or page-size parameter evidence.

#### Scenario: Static and dynamic parameter evidence

- **GIVEN** an offset-related expression is a literal or resolvable constant
- **WHEN** the scanner builds the finding
- **THEN** the corresponding parameter SHALL be marked `hardcoded: true`
- **AND** dynamic configuration, request, or function input SHALL be marked `hardcoded: false`
- **AND** unresolved or mixed expressions SHALL be marked `hardcoded: null`

#### Scenario: Aggregate finding classification

- **WHEN** a finding contains multiple parameter values
- **THEN** the scanner SHALL expose whether the usage is direct SQL offset, direct QuerySet slicing, or indirect pagination
- **AND** it SHALL preserve `unknown` when the static evidence cannot determine the eventual offset

### Requirement: Static-Only Safe Analysis

The scanner SHALL parse source code without importing application modules, initializing Django, executing queries, or connecting to a database.

#### Scenario: Dependencies unavailable

- **GIVEN** the scanned project does not have Django or DRF installed in the scanner environment
- **WHEN** the user runs `scan-offset-usage`
- **THEN** the scanner SHALL still complete using source/import evidence only

#### Scenario: Runtime limits are explicit

- **WHEN** results are serialized
- **THEN** the output or documentation SHALL state that findings do not prove runtime SQL, query-plan cost, or actual database latency
