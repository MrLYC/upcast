## ADDED Requirements

### Requirement: Hybrid Structural and Semantic Scan Pipeline

The system SHALL provide a shared hybrid scan pipeline that composes structural candidate location, CST-to-astroid mapping, semantic verification, and finding projection for Python scanners.

#### Scenario: Execute a single-round hybrid scan

- **WHEN** a scanner invokes the hybrid pipeline with a locate stage, mapping stage, semantic filters, and a projection stage
- **THEN** the system SHALL execute the stages in order: `locate -> map -> semantic filter -> project`
- **AND** structural candidate discovery SHALL be performed before semantic verification
- **AND** the pipeline SHALL return stable, ordered findings

#### Scenario: Reuse existing shared utilities

- **WHEN** the hybrid pipeline performs structural or semantic work
- **THEN** the system SHALL reuse shared common utilities such as CST/AST mapping and astroid inference helpers
- **AND** the pipeline SHALL NOT duplicate the existing responsibilities of the CST mapper or astroid matcher

### Requirement: Hybrid Pipeline Decision States

The system SHALL preserve semantic verification outcomes as `confirmed`, `rejected`, or `unknown` rather than collapsing all failures into a boolean result.

#### Scenario: Confirm a semantic match

- **WHEN** structural candidates map successfully and semantic predicates are satisfied
- **THEN** the system SHALL mark the semantic decision as `confirmed`
- **AND** include supporting evidence for the decision

#### Scenario: Reject a semantic match

- **WHEN** structural candidates map successfully but semantic predicates do not hold
- **THEN** the system SHALL mark the semantic decision as `rejected`
- **AND** preserve the candidate context for debugging

#### Scenario: Preserve unknown semantic result

- **WHEN** semantic verification cannot be completed because mapping or inference is inconclusive
- **THEN** the system SHALL mark the semantic decision as `unknown`
- **AND** record the reason or failure context instead of treating it as `rejected`

### Requirement: Internal Typed Pipeline Configuration

The system SHALL expose the hybrid pipeline through an internal typed configuration model for scanner/core usage in v1.

#### Scenario: Configure a pipeline through typed internal stages

- **WHEN** scanner code defines a v1 hybrid pipeline
- **THEN** the system SHALL accept a typed internal pipeline specification for locate, map, semantic filter, and project stages
- **AND** validate the stage shape before execution

#### Scenario: Exclude public rule-engine scope from v1

- **WHEN** documenting or validating the v1 hybrid pipeline
- **THEN** the system SHALL treat YAML-only rule engines, arbitrary user-defined scripting, and general multi-round pipeline chaining as out of scope
- **AND** describe those capabilities as deferred work rather than supported behavior

### Requirement: Hybrid Pipeline Verification Coverage

The system SHALL verify the v1 hybrid pipeline with core unit tests, focused integration tests, and one end-to-end acceptance example.

#### Scenario: Verify the pipeline core contracts

- **WHEN** validating the v1 hybrid pipeline implementation
- **THEN** the system SHALL cover typed config validation, structural candidates, semantic decisions, and stable result ordering with unit tests

#### Scenario: Verify structural-to-semantic integration

- **WHEN** validating the interaction between structural matching and semantic verification
- **THEN** the system SHALL include focused integration tests that exercise locate, map, and semantic filtering together

#### Scenario: Verify Pydantic model discovery acceptance case

- **WHEN** validating the v1 end-to-end workflow
- **THEN** the system SHALL include an acceptance test for discovering Pydantic models through the hybrid pipeline
- **AND** the final finding SHALL preserve enough evidence to explain why a class was selected

### Requirement: Hybrid Pipeline Scanner Adoption

The system SHALL support incremental adoption of the hybrid pipeline across existing scanner commands without replacing the current CLI framework.

#### Scenario: Adopt hybrid pipeline behind existing scanner commands

- **WHEN** a scanner command migrates to the hybrid pipeline
- **THEN** the command SHALL continue to execute through the existing CLI/scanner architecture
- **AND** the migration SHALL preserve the current public command surface and output contract unless an intentional change is explicitly approved

#### Scenario: Preserve mapping ambiguity during scanner adoption

- **WHEN** structural location succeeds but CST-to-astroid mapping is inconclusive for a candidate required by downstream semantic verification
- **THEN** the system SHALL preserve that candidate as internal `unknown` evidence rather than silently discarding it
- **AND** the system SHALL retain enough reason context to explain the ambiguity during debugging or parity review
