# cyclomatic-complexity-scanner Specification Delta

## MODIFIED Requirements

### Requirement: Metadata Extraction - Implementation

The system SHALL extract comprehensive metadata for each high-complexity function, including signature, docstring, source code, and line counts.

#### Scenario: Extract function signature - IMPLEMENTED

- **WHEN** analyzing any function
- **THEN** the system SHALL capture the complete signature string
- **INCLUDING**: function name, all parameters with type hints, default values, and return type
- **EXAMPLE**: `"def process_user(user_data: dict, strict: bool = True) -> Result:"`
- **AND** store in `ComplexityResult.signature` field
- **AND** set to `None` if extraction fails

**Implementation Notes**:

- Use astroid AST to build signature string
- Handle `*args`, `**kwargs`, keyword-only, and position-only arguments
- Include async prefix for async functions
- Gracefully handle complex type hints

#### Scenario: Extract docstring description - IMPLEMENTED

- **WHEN** analyzing a function
- **THEN** the system SHALL extract the first line of the docstring
- **AND** store in `ComplexityResult.description` field
- **AND** strip leading/trailing whitespace
- **AND** set to `None` if no docstring exists

**Implementation Notes**:

- Use `node.doc_node` to access docstring
- Split on newline and take first line
- Handle empty docstrings as `None`

#### Scenario: Extract full source code - IMPLEMENTED

- **WHEN** analyzing any function
- **THEN** the system SHALL extract the complete source code
- **INCLUDING**: decorators, signature, docstring, all code lines
- **AND** preserve original indentation and formatting
- **AND** store in `ComplexityResult.code` field
- **AND** set to `None` if extraction fails

**Implementation Notes**:

- Reuse existing `extract_function_code()` utility
- Code already handles decorators and indentation
- Return `None` on any extraction failure

#### Scenario: Count comment lines - IMPLEMENTED

- **WHEN** analyzing function code
- **THEN** the system SHALL use Python's `tokenize` module to count COMMENT tokens
- **AND** count unique line numbers containing comments
- **AND** store in `ComplexityResult.comment_lines` field (default: 0)
- **AND** NOT count docstrings as comments
- **AND** NOT count `#` characters in string literals

**Implementation Notes**:

- Use `tokenize.generate_tokens()` on StringIO of source
- Collect line numbers where `token.type == tokenize.COMMENT`
- Handle TokenError gracefully (return 0)
- Docstrings are STRING tokens, not COMMENT tokens

#### Scenario: Calculate total code lines - IMPLEMENTED

- **WHEN** analyzing any function
- **THEN** the system SHALL calculate total lines as `end_line - line + 1`
- **INCLUDING**: decorators, signature, docstring, code, comments, blank lines
- **AND** store in `ComplexityResult.code_lines` field (default: 0)
- **AND** set to 0 if line numbers unavailable

**Implementation Notes**:

- Simple arithmetic from AST `lineno` and `end_lineno`
- Matches spec example: "Function spanning lines 45-98 has code_lines = 54"

### Requirement: CLI Command Naming - CORRECTED

The system SHALL provide the `scan-complexity-patterns` command as specified.

#### Scenario: Use correct command name - IMPLEMENTED

- **WHEN** user runs `upcast scan-complexity-patterns <path>`
- **THEN** the system SHALL execute the complexity scanner
- **AND** accept all standard options (--threshold, --include, --exclude, etc.)
- **AND** produce output with all metadata fields populated

**Migration Note**:

- Previous command name `scan-complexity` was incorrect per specification
- Changed to `scan-complexity-patterns` to match spec and naming convention
- Breaking change - users must update scripts and CI pipelines

### Requirement: Complete Output Structure - UPDATED

The system SHALL output results with all specified metadata fields.

#### Scenario: Full output structure - IMPLEMENTED

- **WHEN** scanner produces results
- **THEN** each `ComplexityResult` SHALL include:
  - `name`: Function name
  - `line`: Start line number
  - `end_line`: End line number
  - `complexity`: Cyclomatic complexity score
  - `severity`: Severity level (healthy, acceptable, warning, high_risk, critical)
  - `message`: Optional message about complexity
  - `description`: First line of docstring (or null)
  - `signature`: Complete function signature (or null)
  - `code`: Full source code (or null)
  - `comment_lines`: Number of comment lines
  - `code_lines`: Total lines in function
- **AND** output SHALL be grouped by module path
- **AND** format SHALL be valid YAML or JSON

**Example Output**:

```yaml
summary:
  total_count: 12
  files_scanned: 3
  high_complexity_count: 12
  by_severity:
    warning: 8
    high_risk: 3
    critical: 1

modules:
  app/services/user.py:
    - name: process_user_registration
      line: 45
      end_line: 78
      complexity: 16
      severity: high_risk
      message: "Complexity 16 exceeds threshold 11"
      description: "Handle user registration with validation and email"
      signature: "def process_user_registration(user_data: dict, strict: bool = True) -> Result:"
      comment_lines: 8
      code_lines: 34
      code: |
        def process_user_registration(user_data: dict, strict: bool = True) -> Result:
            """Handle user registration with validation and email."""
            if not user_data:
                raise ValueError("User data required")
            # Validate email format
            if "email" not in user_data:
                return Result.error("Email required")
            ...
```

## ADDED Requirements

### Requirement: Graceful Degradation

The system SHALL handle extraction failures gracefully without blocking analysis.

#### Scenario: Signature extraction failure

- **WHEN** signature extraction fails for any reason
- **THEN** the system SHALL set `signature: null`
- **AND** continue with other field extraction
- **AND** log warning if verbose mode enabled

#### Scenario: Comment counting failure

- **WHEN** tokenize module raises TokenError
- **THEN** the system SHALL set `comment_lines: 0`
- **AND** continue with analysis
- **AND** log warning if verbose mode enabled

#### Scenario: Code extraction failure

- **WHEN** source code cannot be extracted
- **THEN** the system SHALL skip the entire function
- **AND** NOT include in results
- **AND** log warning if verbose mode enabled

**Rationale**: Code is essential for complexity analysis; other fields can gracefully degrade to null/0.

## Implementation Status

All scenarios in this delta have been **IMPLEMENTED** as part of the `fix-scanner-missing-features` change proposal.

## Cross-References

- Original Spec: `openspec/specs/cyclomatic-complexity-scanner/spec.md`
- Proposal: `openspec/changes/fix-scanner-missing-features/proposal.md`
- Related Change: `2025-12-21-refactor-scanners-to-use-models` (introduced the issue)
