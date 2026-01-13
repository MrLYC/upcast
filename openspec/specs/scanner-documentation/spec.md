# scanner-documentation Specification

## Purpose

为 upcast 的每个扫描器提供一致、可维护、且与实际输出一致的文档规范，包括统一的文档结构、字段类型/必填性说明，以及引用 `example/scan-results/` 的真实示例，降低用户理解与集成成本。

## Requirements

### Requirement: Comprehensive Scanner Documentation Structure

Each scanner MUST have a dedicated documentation file in `docs/scanners/` that follows a standardized structure to ensure consistency and completeness across all scanner documentation.

#### Scenario: User needs detailed field explanation for scanner output

**Given** a user has run a scanner command and obtained YAML/JSON output
**When** the user wants to understand what each field means
**Then** they can refer to `docs/scanners/<scanner-name>.md` to find:

- Overview of the scanner's purpose
- Command usage examples
- Complete field reference with types, required/optional status, and value semantics
- Real-world output examples

#### Scenario: Developer adds new scanner or modifies existing one

**Given** a developer is adding a new scanner or changing an existing scanner's output
**When** they need to document the changes
**Then** they follow the standardized documentation template that includes:

- Overview section
- Command Usage section
- Output Format section with metadata and results structure
- Field Reference section with detailed field descriptions
- Examples section referencing actual output from `example/scan-results/`
- Notes section for special cases

### Requirement: Documentation Index and Navigation

The `docs/` directory MUST have a clear entry point that helps users discover and navigate to specific scanner documentation.

#### Scenario: User discovers available scanner documentation

**Given** a user wants to understand what documentation is available
**When** they open `docs/README.md`
**Then** they see:

- A list of all 15 scanners with brief descriptions
- Links to individual scanner documentation files
- Explanation of common options (--include, --exclude, --format, --output, etc.)
- General concepts applicable to all scanners

#### Scenario: User navigates from main README to detailed docs

**Given** a user is reading the main project README.md
**When** they want more detailed information about scanner output formats
**Then** they can follow a link to `docs/README.md` which provides comprehensive documentation structure

### Requirement: Field Documentation Accuracy

All field descriptions in scanner documentation MUST accurately reflect the actual implementation and output format.

#### Scenario: Field documentation matches actual output

**Given** a scanner produces specific output fields
**When** documentation is written for that scanner
**Then** every field in the actual output (from `example/scan-results/*.yaml`) is documented with:

- Field name (exact match with output)
- Data type (string, integer, boolean, list, object, etc.)
- Required or optional status
- Default value (if applicable)
- Possible values or value range
- Semantic meaning and usage context

#### Scenario: Documentation references real examples

**Given** each scanner has example output in `example/scan-results/`
**When** documentation includes examples
**Then** examples either:

- Directly reference the example file path
- Copy snippets from actual example files
- Maintain consistency with actual scanner behavior

### Requirement: Documentation Maintenance Guidelines

Documentation MUST be maintainable and kept in sync with code changes.

#### Scenario: Scanner implementation changes trigger documentation updates

**Given** a scanner's output format or behavior changes
**When** the code is updated
**Then** the corresponding documentation in `docs/scanners/<scanner-name>.md` must be updated to reflect:

- New fields added
- Fields removed or deprecated
- Changed field types or semantics
- Updated examples

#### Scenario: Documentation validation in CI/CD

**Given** the project has CI/CD pipelines
**When** documentation is committed
**Then** automated checks verify:

- All scanner files have corresponding documentation
- Documentation structure follows the template
- Links are valid and not broken
- Examples reference existing files

### Requirement: Scanner-Specific Field Documentation

Each scanner type has unique output characteristics that MUST be thoroughly documented.

#### Scenario: Django scanner documentation includes Django-specific concepts

**Given** Django-related scanners (models, settings, urls)
**When** their documentation is written
**Then** it includes:

- Django framework concepts (models, fields, relationships, Meta classes, etc.)
- Django-specific field types and their parameters
- Common Django patterns and conventions

#### Scenario: Concurrency scanner documentation explains pattern categories

**Given** concurrency-pattern-scanner detects multiple concurrency types
**When** documentation is written
**Then** it clearly explains:

- Threading patterns and their characteristics
- Multiprocessing patterns and use cases
- Asyncio patterns and async/await detection
- How each category is identified in code

#### Scenario: Complexity scanner documentation explains metrics

**Given** complexity-pattern-scanner calculates cyclomatic complexity
**When** documentation is written
**Then** it explains:

- What cyclomatic complexity measures
- How the threshold parameter affects output
- What complexity scores indicate
- When refactoring might be needed
