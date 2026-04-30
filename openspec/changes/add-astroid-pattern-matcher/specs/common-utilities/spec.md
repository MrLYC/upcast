## ADDED Requirements

### Requirement: Astroid Pattern Matcher

The system SHALL provide an astroid-powered pattern matcher for common utilities that combines structural AST matching with semantic inference-aware predicates.

#### Scenario: Match inferred builtin type

- **WHEN** a caller matches an astroid node with a structural pattern and a rule requiring builtin type `str`, `int`, `float`, `bool`, `None`, `list`, `dict`, or `tuple`
- **THEN** the system SHALL evaluate the match using the node's inferred builtin type
- **AND** return a successful match only when the inferred builtin type satisfies the rule

#### Scenario: Match inferability

- **WHEN** a caller provides a rule with `inferable: true` or `inferable: false`
- **THEN** the system SHALL determine whether the node has at least one non-`Uninferable` inference result
- **AND** use that determination to accept or reject the match

#### Scenario: Match qualified-name patterns

- **WHEN** a caller provides a rule that constrains inferred qualified names by exact, prefix, or suffix path
- **THEN** the system SHALL evaluate inferred qualified names for the node
- **AND** accept the match when any inferred qualified name satisfies the configured path constraint

#### Scenario: Match negative predicates

- **WHEN** a caller provides a nested `not` rule for the current node or a named capture
- **THEN** the system SHALL reject matches that satisfy the nested rule
- **AND** preserve matches that do not satisfy the nested rule

#### Scenario: Match nested child subpatterns

- **WHEN** a caller provides a `has` rule containing a child pattern and optional child rule
- **THEN** the system SHALL search descendant nodes below the current match target
- **AND** accept the outer match only when at least one descendant satisfies the child pattern and child rule

### Requirement: Astroid Pattern Matcher API Shape

The system SHALL expose a minimal shared API for matching a single node and searching within a root node.

#### Scenario: Match a single node

- **WHEN** a caller invokes `match(node, pattern, rule=None)`
- **THEN** the system SHALL return a match result when the node satisfies the pattern and rule
- **AND** otherwise return no match

#### Scenario: Find matches in a root node

- **WHEN** a caller invokes `find_matches(root, pattern, rule=None)`
- **THEN** the system SHALL search descendant nodes within the root
- **AND** return all successful match results in traversal order

#### Scenario: Return named captures

- **WHEN** a structural pattern includes supported metavariables such as `$NAME`
- **THEN** the system SHALL include the resolved capture mapping in the match result
- **AND** preserve the matched astroid nodes for downstream analysis

### Requirement: Astroid Pattern Matcher Scope Limits

The system SHALL document and enforce a constrained v1 matcher scope.

#### Scenario: Restrict sequence capture support

- **WHEN** a caller uses `$$$NAME`
- **THEN** the system SHALL only support it in natural AST list fields where sequence capture is unambiguous
- **AND** reject unsupported sequence-capture positions with a clear error

#### Scenario: Defer unsupported ast-grep features

- **WHEN** a caller expects full ast-grep compatibility, CST-backed execution, or pattern-embedded semantic predicates
- **THEN** the system SHALL document those features as out of scope for v1
- **AND** avoid silently emulating unsupported behavior
