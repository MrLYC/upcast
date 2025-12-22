# Implementation Tasks - Fix Scanner Missing Features

## Phase 1: Update Complexity Scanner Model (Est: 60 min)

### Task 1.1: Add Missing Fields to ComplexityResult Model (20 min)

**Goal**: Update the Pydantic model to include all fields from the original specification

**Steps**:

- [x] Open `upcast/models/complexity.py`
- [x] Add `description: str | None` field (docstring first line)
- [x] Add `signature: str | None` field (complete function signature)
- [x] Add `code: str | None` field (full source code)
- [x] Add `comment_lines: int` field (default=0)
- [x] Add `code_lines: int` field (default=0)
- [x] Verify field descriptions match specification
- [x] Run `uv run ruff check` to validate

**Acceptance**:

- Model includes all 5 new fields ✓
- Field types and defaults are correct ✓
- No ruff violations ✓

### Task 1.2: Add Comment Counting Utility (20 min)

**Goal**: Create utility function to count comment lines using tokenize module

**Steps**:

- [x] Check if `count_comment_lines()` already exists in `upcast/common/code_utils.py`
- [x] If not, implement using Python's `tokenize` module
- [x] Function should:
  - Accept source code as string
  - Use `tokenize.generate_tokens()` on StringIO
  - Count lines containing `tokenize.COMMENT` tokens
  - Return integer count
  - Handle tokenize errors gracefully
- [x] Add docstring explaining tokenize-based counting
- [x] Add unit test in `tests/test_common/test_code_utils.py`

**Acceptance**:

- Function counts actual comment tokens only ✓ (already existed)
- Does not count docstrings as comments ✓
- Does not count `#` in string literals ✓
- Unit test validates behavior ✓

### Task 1.3: Add Signature Extraction Utility (20 min)

**Goal**: Create or enhance utility to extract complete function signatures

**Steps**:

- [x] Check if signature extraction exists in `upcast/common/code_utils.py`
- [x] Implement `extract_function_signature(node: nodes.FunctionDef) -> str`:
  - Get function name from `node.name`
  - Build parameter list with types and defaults
  - Include return type annotation if present
  - Handle async functions
  - Format as valid Python signature string
- [x] Add docstring with examples
- [x] Add unit tests for various signature formats

**Acceptance**:

- Extracts complete signature including type hints ✓
- Handles default values correctly ✓
- Handles async functions ✓
- Unit tests cover edge cases ✓

## Phase 2: Update Complexity Scanner Implementation (Est: 90 min)

### Task 2.1: Extract New Fields in Scanner (40 min)

**Goal**: Update `ComplexityScanner._analyze_function()` to populate all new fields

**Steps**:

- [x] Open `upcast/scanners/complexity.py`
- [x] In `_analyze_function()` method:
  - Extract docstring using `node.doc_node` or `astroid.nodes.get_doc_node()`
  - Get first line as description (handle None case)
  - Call `extract_function_signature(node)` for signature
  - Call `extract_function_code(node)` for source (already exists)
  - Calculate `code_lines` from `end_line - line + 1`
  - Call `count_comment_lines(code)` if code exists
- [x] Update `ComplexityResult` instantiation with all new fields
- [x] Handle cases where extraction fails (set to None/0)

**Acceptance**:

- All fields populated in happy path ✓
- Graceful fallback when extraction fails ✓
- No exceptions on edge cases ✓

### Task 2.2: Update Tests for New Fields (30 min)

**Goal**: Enhance existing tests to validate new fields

**Steps**:

- [x] Open `tests/test_scanners/test_complexity.py`
- [x] Find existing test functions
- [x] Add assertions for new fields:
  - `assert result.description == expected_docstring_first_line`
  - `assert result.signature == expected_signature`
  - `assert result.code is not None`
  - `assert result.comment_lines >= 0`
  - `assert result.code_lines > 0`
- [x] Create test fixture with:
  - Function with docstring
  - Function without docstring
  - Function with type hints
  - Function with comments
- [x] Run tests: `uv run pytest tests/test_scanners/test_complexity.py -v`

**Acceptance**:

- All tests pass ✓ (12/12)
- New fields validated in at least 3 test cases ✓
- Coverage remains ≥80% ✓

### Task 2.3: Manual Validation (20 min)

**Goal**: Test on real code to verify correctness

**Steps**:

- [x] Run scanner on upcast's own codebase:
  ```bash
  uv run upcast scan-complexity-patterns upcast/scanners --threshold 5 -o /tmp/complexity.yaml
  ```
- [x] Inspect output YAML:
  - Verify `description` matches docstrings
  - Verify `signature` is valid Python
  - Verify `code` contains full function
  - Verify `comment_lines` is reasonable
  - Verify `code_lines` matches file inspection
- [x] Test edge cases manually:
  - Function without docstring
  - Async function
  - Method in class
- [x] Document any issues found

**Acceptance**:

- Output matches manual inspection ✓
- All fields present and accurate ✓
- No obvious bugs ✓

## Phase 3: Rename Commands (Est: 45 min)

### Task 3.1: Rename Complexity Command (15 min)

**Goal**: Update command name in main.py

**Steps**:

- [x] Open `upcast/main.py`
- [x] Find `@main.command(name="scan-complexity")`
- [x] Change to `@main.command(name="scan-complexity-patterns")`
- [x] Rename function from `scan_complexity_cmd` to `scan_complexity_patterns_cmd`
- [x] Update docstring if it mentions command name
- [x] Keep implementation identical

**Acceptance**:

- Command renamed successfully ✓
- Function still works identically ✓
- No ruff violations ✓

### Task 3.2: Rename Concurrency Command (15 min)

**Goal**: Update concurrency command name

**Steps**:

- [x] In `upcast/main.py`
- [x] Find `@main.command(name="scan-concurrency")`
- [x] Change to `@main.command(name="scan-concurrency-patterns")`
- [x] Rename function from `scan_concurrency_cmd` to `scan_concurrency_patterns_cmd`
- [x] Update docstring if needed
- [x] Keep implementation identical

**Acceptance**:

- Command renamed successfully ✓
- No functional changes ✓
- No ruff violations ✓

### Task 3.3: Test Renamed Commands (15 min)

**Goal**: Verify commands work with new names

**Steps**:

- [x] Test complexity command:
  ```bash
  uv run upcast scan-complexity-patterns --help
  uv run upcast scan-complexity-patterns . --threshold 20
  ```
- [x] Test concurrency command:
  ```bash
  uv run upcast scan-concurrency-patterns --help
  uv run upcast scan-concurrency-patterns .
  ```
- [x] Verify old names no longer work:
  ```bash
  uv run upcast scan-complexity --help  # Should fail
  uv run upcast scan-concurrency --help  # Should fail
  ```
- [x] Check output format is unchanged

**Acceptance**:

- New command names work correctly ✓
- Old names are removed ✓
- Help text displays correctly ✓
- Output format unchanged ✓

## Phase 4: Update Documentation (Est: 30 min)

### Task 4.1: Update README.md (20 min)

**Goal**: Change all command references to new names

**Steps**:

- [x] Open `README.md`
- [x] Search for `scan-complexity` (without -patterns)
- [x] Replace with `scan-complexity-patterns`
- [x] Search for `scan-concurrency` (without -patterns)
- [x] Replace with `scan-concurrency-patterns`
- [x] Update example outputs to show new fields:
  - Add `description` field
  - Add `signature` field
  - Add `code` field
  - Add `comment_lines` field
  - Add `code_lines` field
- [x] Verify all code blocks are valid YAML
- [x] Check markdown formatting with prettier

**Acceptance**:

- All references updated ✓
- Example outputs show new fields ✓
- No broken markdown ✓
- Prettier passes ✓

### Task 4.2: Update Specifications (10 min)

**Goal**: Mark implementation as complete in specs

**Steps**:

- [x] Open `openspec/specs/cyclomatic-complexity-scanner/spec.md`
- [x] Verify all requirements are now satisfied:
  - Signature extraction ✓
  - Docstring extraction ✓
  - Code extraction ✓
  - Comment counting ✓
  - Code line counting ✓
- [x] Add note about implementation completion
- [x] Check if any other spec references need updates

**Acceptance**:

- Specs reflect current implementation ✓
- No outdated information remains ✓

## Phase 5: Quality Assurance (Est: 30 min)

### Task 5.1: Run Full Test Suite (10 min)

**Goal**: Ensure no regressions

**Steps**:

- [x] Run all tests: `uv run pytest tests/ -v`
- [x] Check coverage: `uv run pytest tests/ --cov=upcast --cov-report=term-missing`
- [x] Verify coverage ≥80%
- [x] Check for any new failures
- [x] Check for any reduced coverage

**Acceptance**:

- All 253+ tests pass ✓
- Coverage ≥80% ✓
- No new failures ✓

### Task 5.2: Run Linting and Formatting (10 min)

**Goal**: Ensure code quality standards

**Steps**:

- [x] Run ruff check: `uv run ruff check`
- [x] Fix any violations
- [x] Run ruff format: `uv run ruff format`
- [x] Verify no changes needed after format
- [x] Check pre-commit would pass

**Acceptance**:

- No ruff violations in our code ✓
- Code properly formatted ✓
- Pre-commit ready ✓

### Task 5.3: Integration Testing (10 min)

**Goal**: Test on real projects

**Steps**:

- [x] Test on upcast itself:
  ```bash
  uv run upcast scan-complexity-patterns upcast/scanners/complexity.py --threshold 5
  ```
- [x] Inspect output:
  - Verify all fields present
  - Check signature quality
  - Check description accuracy
  - Check code extraction
  - Verify comment/code line counts
- [x] Test on another project (e.g., upcast itself)
- [x] Document any issues

**Acceptance**:

- Output looks correct on real projects ✓
- All fields populated properly ✓
- No obvious bugs or issues ✓

## Summary

**Total Estimated Time**: 255 minutes (≈4.25 hours)

**Dependencies**:

- Phase 2 depends on Phase 1 (needs model and utilities)
- Phase 5 depends on all previous phases (validates everything)

**Validation Checkpoints**:

- After Phase 1: Model and utilities pass unit tests
- After Phase 2: Scanner produces new fields correctly
- After Phase 3: Commands work with new names
- After Phase 4: Documentation is accurate
- After Phase 5: All quality checks pass

**Rollback Plan**:
If issues are discovered:

1. Revert model changes
2. Revert scanner changes
3. Revert command renames
4. Revert documentation
5. Create new proposal addressing issues
