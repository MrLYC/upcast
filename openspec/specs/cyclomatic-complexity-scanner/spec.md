# cyclomatic-complexity-scanner Specification

## Purpose

TBD - created by archiving change add-cyclomatic-complexity-scanner. Update Purpose after archive.

## Requirements

### Requirement: Cyclomatic Complexity Calculation

The system SHALL calculate cyclomatic complexity for all function and method definitions using AST analysis.

#### Scenario: Calculate complexity for simple function

- **WHEN** analyzing a function with no control flow statements
- **THEN** the system SHALL report complexity of 1 (base complexity)
- **AND** include function name, location, and signature

#### Scenario: Count if statements

- **WHEN** analyzing a function containing `if` statements
- **THEN** the system SHALL add 1 to complexity for each `if` statement
- **AND** add 1 for each `elif` clause
- **AND** NOT count `else` clauses without additional conditions

#### Scenario: Count loop statements

- **WHEN** analyzing a function with `for` or `while` loops
- **THEN** the system SHALL add 1 to complexity for each loop
- **AND** count nested loops independently
- **AND** include `async for` loops

#### Scenario: Count exception handlers

- **WHEN** analyzing a function with try/except blocks
- **THEN** the system SHALL add 1 for each `except` handler
- **AND** NOT count the `try` or `finally` blocks
- **AND** handle multiple exception types per handler

#### Scenario: Count boolean operators

- **WHEN** analyzing conditions with `and` or `or` operators
- **THEN** the system SHALL add 1 for each boolean operator
- **EXAMPLE**: `if a and b or c:` adds 3 (if + and + or)
- **AND** count operators in `while` conditions
- **AND** count operators in `assert` statements

#### Scenario: Count comprehension conditions

- **WHEN** analyzing list/dict/set comprehensions with `if` clauses
- **THEN** the system SHALL add 1 for each conditional
- **EXAMPLE**: `[x for x in items if x > 0]` adds 1
- **AND** count nested comprehensions independently

#### Scenario: Count ternary expressions

- **WHEN** analyzing ternary expressions `a if condition else b`
- **THEN** the system SHALL add 1 for each ternary
- **AND** count boolean operators in the condition separately

#### Scenario: Handle nested functions

- **WHEN** analyzing a function containing nested function definitions
- **THEN** the system SHALL calculate complexity for each function independently
- **AND** NOT add nested function's complexity to parent
- **AND** report both if they exceed threshold

#### Scenario: Handle class methods

- **WHEN** analyzing class methods
- **THEN** the system SHALL calculate complexity same as functions
- **AND** record the parent class name
- **AND** set `is_method` flag to true
- **AND** include `self` or `cls` parameters in signature

#### Scenario: Handle async functions

- **WHEN** analyzing `async def` functions
- **THEN** the system SHALL calculate complexity using same rules
- **AND** set `is_async` flag to true
- **AND** count `await` expressions as complexity +0 (they don't add branching)

#### Scenario: Handle decorated functions

- **WHEN** analyzing functions with decorators like `@property`, `@staticmethod`
- **THEN** the system SHALL calculate complexity ignoring decorators
- **AND** include decorator information in metadata
- **AND** treat all decorated functions equally

### Requirement: Threshold Filtering

The system SHALL filter results based on configurable complexity threshold to focus on high-complexity functions.

#### Scenario: Apply default threshold

- **WHEN** scanning without explicit threshold
- **THEN** the system SHALL use default threshold of 11
- **AND** only report functions with complexity ≥ 11

#### Scenario: Apply custom threshold

- **WHEN** user specifies `--threshold N`
- **THEN** the system SHALL only report functions with complexity ≥ N
- **AND** accept any positive integer value
- **AND** reject invalid values with clear error message

#### Scenario: Report zero results

- **WHEN** no functions exceed the threshold
- **THEN** the system SHALL output empty results with summary
- **AND** indicate zero high-complexity functions found
- **AND** still show total functions analyzed

### Requirement: Severity Categorization

The system SHALL categorize functions by complexity severity to prioritize refactoring efforts.

#### Scenario: Assign severity levels

- **WHEN** calculating complexity
- **THEN** the system SHALL assign severity based on these ranges:
  - healthy: complexity ≤ 5
  - acceptable: 6 ≤ complexity ≤ 10
  - warning: 11 ≤ complexity ≤ 15
  - high_risk: 16 ≤ complexity ≤ 20
  - critical: complexity > 20
- **AND** include severity in output for each function

#### Scenario: Aggregate by severity

- **WHEN** generating summary statistics
- **THEN** the system SHALL count functions in each severity level
- **AND** only include levels that have non-zero counts
- **AND** exclude "healthy" and "acceptable" from reported counts (below threshold)

### Requirement: Test File Exclusion

The system SHALL exclude test files by default to focus on production code.

#### Scenario: Exclude test files by pattern

- **WHEN** scanning with default settings
- **THEN** the system SHALL exclude files matching:
  - `tests/**`
  - `**/tests/**`
  - `test_*.py`
  - `*_test.py`
  - `**/test_*.py`
- **AND** not analyze functions in excluded files

#### Scenario: Include tests with flag

- **WHEN** user specifies `--include-tests` flag
- **THEN** the system SHALL scan test files
- **AND** apply same complexity calculation rules
- **AND** include test functions in output

#### Scenario: Custom exclusion overrides

- **WHEN** user provides `--exclude` patterns
- **THEN** test exclusions SHALL still apply
- **AND** custom exclusions SHALL be additional
- **AND** `--no-default-excludes` SHALL disable test exclusions

### Requirement: Source Code Extraction

The system SHALL extract the complete source code for each high-complexity function.

#### Scenario: Extract full function code

- **WHEN** analyzing a high-complexity function
- **THEN** the system SHALL extract the complete source code from def to end
- **INCLUDING**: decorators, docstring, all code lines, comments
- **AND** preserve original indentation and formatting

#### Scenario: Count total code lines

- **WHEN** extracting function code
- **THEN** the system SHALL count total lines (code + comments + blank)
- **AND** report as `code_lines` field
- **EXAMPLE**: Function spanning lines 45-98 has code_lines = 54

#### Scenario: Count comment lines

- **WHEN** analyzing function body
- **THEN** the system SHALL use Python's `tokenize` module to identify COMMENT tokens
- **AND** count unique line numbers containing comments
- **AND** NOT count docstrings as comments
- **AND** correctly handle comments inside strings (not counted)
- **AND** report as `comment_lines` field
- **EXAMPLE**: Function with 8 comment lines has comment_lines = 8

#### Scenario: Handle multi-line strings

- **WHEN** function contains multi-line strings that aren't docstrings
- **THEN** treat them as code, NOT comments
- **AND** tokenize module correctly distinguishes comments from strings

#### Scenario: Handle comments in strings

- **WHEN** function contains `#` characters inside string literals
- **THEN** those SHALL NOT be counted as comments
- **AND** only actual Python comment tokens are counted
- **EXAMPLE**: `message = "Use # for comments"  # This is a comment` counts as 1 comment line

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

### Requirement: Module-Based Organization

The system SHALL organize results by module path to facilitate navigation and review.

#### Scenario: Group by module

- **WHEN** generating output
- **THEN** functions SHALL be grouped under their module path as keys
- **AND** modules SHALL be sorted alphabetically
- **AND** functions within each module SHALL be sorted by line number

#### Scenario: Use relative paths

- **WHEN** scanning from a directory
- **THEN** module paths SHALL be relative to scan root
- **AND** use forward slashes as separators
- **EXAMPLE**: `app/services/user.py` not `/absolute/path/app/services/user.py`

#### Scenario: Handle single file scans

- **WHEN** scanning a single file directly
- **THEN** use filename as module key
- **AND** make path relative to current directory if possible

### Requirement: Summary Statistics

The system SHALL provide summary statistics to give overview of codebase complexity.

#### Scenario: Calculate overall statistics

- **WHEN** generating output
- **THEN** summary SHALL include:
  - Total functions scanned
  - Count of high-complexity functions
  - Breakdown by severity level
  - Number of files analyzed
- **AND** place summary at top of output

#### Scenario: Calculate per-module statistics

- **WHEN** a module has multiple high-complexity functions
- **THEN** optionally include module-level rollup:
  - Function count in module
  - Average complexity
  - Highest complexity function

### Requirement: YAML Output Format

The system SHALL export results in structured YAML format for human readability.

#### Scenario: YAML structure

- **WHEN** exporting to YAML (default)
- **THEN** output SHALL have structure:

  ```yaml
  summary:
    total_functions_scanned: N
    high_complexity_count: M
    by_severity:
      warning: X
      high_risk: Y
      critical: Z
    files_analyzed: K

  modules:
    path/to/module.py:
      - name: function_name
        line: N
        end_line: M
        complexity: X
        severity: level
        description: "..."
        signature: "..."
        is_async: bool
        is_method: bool
        class_name: str | null
        comment_lines: N
        code_lines: M
        code: |
          def function_name(...):
              # Function implementation
              ...
  ```

#### Scenario: YAML formatting

- **WHEN** generating YAML
- **THEN** use 2-space indentation
- **AND** use block style for lists and dicts
- **AND** preserve Unicode characters
- **AND** sort keys alphabetically

### Requirement: JSON Output Format Support

The system SHALL support JSON output as alternative to YAML.

#### Scenario: JSON format option

- **WHEN** user specifies `--format json`
- **THEN** output same structure as YAML in JSON format
- **AND** use 2-space indentation
- **AND** ensure ASCII-safe encoding

#### Scenario: Format consistency

- **WHEN** comparing YAML and JSON outputs
- **THEN** both SHALL have identical data structure
- **AND** be convertible between formats without data loss

### Requirement: CLI Interface

The system SHALL provide command-line interface following Upcast conventions.

#### Scenario: Basic scan command

- **WHEN** user runs `upcast scan-complexity <path>`
- **THEN** the system SHALL scan all Python files in path
- **AND** output results to stdout in YAML format
- **AND** use default threshold of 11

#### Scenario: Custom threshold

- **WHEN** user specifies `--threshold N`
- **THEN** the system SHALL only report functions with complexity ≥ N
- **EXAMPLE**: `upcast scan-complexity . --threshold 15`

#### Scenario: Output to file

- **WHEN** user specifies `-o <file>` or `--output <file>`
- **THEN** write results to specified file path
- **AND** create parent directories if needed
- **AND** still print summary to stderr with `--verbose`

#### Scenario: Include/exclude patterns

- **WHEN** user provides `--include` or `--exclude` patterns
- **THEN** apply glob pattern matching to filter files
- **AND** allow multiple patterns
- **EXAMPLE**: `--exclude "migrations/**" --exclude "admin.py"`

#### Scenario: Verbose output

- **WHEN** user specifies `--verbose` or `-v`
- **THEN** print progress messages to stderr:
  - Files being scanned
  - High-complexity functions found
  - Summary statistics
- **AND** keep structured output on stdout clean

### Requirement: Error Handling

The system SHALL handle errors gracefully without crashing.

#### Scenario: Syntax errors in source

- **WHEN** encountering Python file with syntax errors
- **THEN** log warning with file and line number
- **AND** skip the file
- **AND** continue processing other files

#### Scenario: Encoding issues

- **WHEN** encountering file with unsupported encoding
- **THEN** try fallback encodings (utf-8, latin-1, cp1252)
- **AND** log warning if all fail
- **AND** skip the file

#### Scenario: Permission errors

- **WHEN** file cannot be read due to permissions
- **THEN** log error with filename
- **AND** skip the file
- **AND** continue processing

#### Scenario: No files found

- **WHEN** no Python files match the scan criteria
- **THEN** output empty results with zero counts
- **AND** log informational message
- **AND** exit with code 0 (not an error)

### Requirement: Performance

The system SHALL process large codebases efficiently.

#### Scenario: Scan performance

- **WHEN** scanning codebase with 1000+ files
- **THEN** complete in under 10 seconds
- **AND** use streaming processing (no large memory buffers)
- **AND** scale linearly with file count

#### Scenario: Memory usage

- **WHEN** processing any codebase
- **THEN** memory usage SHALL scale linearly with file count
- **AND** not exceed 500MB for 10,000 files
- **AND** release AST after processing each file

### Requirement: Integration with Upcast CLI

The system SHALL integrate seamlessly with existing Upcast command structure.

#### Scenario: Register command

- **WHEN** Upcast CLI initializes
- **THEN** `scan-complexity` command SHALL be available
- **AND** appear in `upcast --help`
- **AND** follow same option conventions as other scanners

#### Scenario: Share common utilities

- **WHEN** implementing scanner
- **THEN** reuse `collect_python_files()` for file discovery
- **AND** reuse YAML/JSON export utilities
- **AND** reuse path normalization helpers
- **AND** reuse logging configuration

#### Scenario: Consistent output format

- **WHEN** comparing with other scanners
- **THEN** output structure SHALL follow same patterns:
  - Summary section with statistics
  - Detailed results organized logically
  - Metadata included consistently
- **AND** use same YAML/JSON formatting conventions

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
