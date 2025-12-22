# Implementation Tasks - Fix Scanner Missing Features

## Phase 1: Update Complexity Scanner Model (Est: 60 min)

### Task 1.1: Add Missing Fields to ComplexityResult Model (20 min)

**Goal**: Update the Pydantic model to include all fields from the original specification

**Steps**:

- [ ] Open `upcast/models/complexity.py`
- [ ] Add `description: str | None` field (docstring first line)
- [ ] Add `signature: str | None` field (complete function signature)
- [ ] Add `code: str | None` field (full source code)
- [ ] Add `comment_lines: int` field (default=0)
- [ ] Add `code_lines: int` field (default=0)
- [ ] Verify field descriptions match specification
- [ ] Run `uv run ruff check` to validate

**Acceptance**:

- Model includes all 5 new fields
- Field types and defaults are correct
- No ruff violations

### Task 1.2: Add Comment Counting Utility (20 min)

**Goal**: Create utility function to count comment lines using tokenize module

**Steps**:

- [ ] Check if `count_comment_lines()` already exists in `upcast/common/code_utils.py`
- [ ] If not, implement using Python's `tokenize` module
- [ ] Function should:
  - Accept source code as string
  - Use `tokenize.generate_tokens()` on StringIO
  - Count lines containing `tokenize.COMMENT` tokens
  - Return integer count
  - Handle tokenize errors gracefully
- [ ] Add docstring explaining tokenize-based counting
- [ ] Add unit test in `tests/test_common/test_code_utils.py`

**Acceptance**:

- Function counts actual comment tokens only
- Does not count docstrings as comments
- Does not count `#` in string literals
- Unit test validates behavior

### Task 1.3: Add Signature Extraction Utility (20 min)

**Goal**: Create or enhance utility to extract complete function signatures

**Steps**:

- [ ] Check if signature extraction exists in `upcast/common/code_utils.py`
- [ ] Implement `extract_function_signature(node: nodes.FunctionDef) -> str`:
  - Get function name from `node.name`
  - Build parameter list with types and defaults
  - Include return type annotation if present
  - Handle async functions
  - Format as valid Python signature string
- [ ] Add docstring with examples
- [ ] Add unit tests for various signature formats

**Acceptance**:

- Extracts complete signature including type hints
- Handles default values correctly
- Handles async functions
- Unit tests cover edge cases

## Phase 2: Update Complexity Scanner Implementation (Est: 90 min)

### Task 2.1: Extract New Fields in Scanner (40 min)

**Goal**: Update `ComplexityScanner._analyze_function()` to populate all new fields

**Steps**:

- [ ] Open `upcast/scanners/complexity.py`
- [ ] In `_analyze_function()` method:
  - Extract docstring using `node.doc_node` or `astroid.nodes.get_doc_node()`
  - Get first line as description (handle None case)
  - Call `extract_function_signature(node)` for signature
  - Call `extract_function_code(node)` for source (already exists)
  - Calculate `code_lines` from `end_line - line + 1`
  - Call `count_comment_lines(code)` if code exists
- [ ] Update `ComplexityResult` instantiation with all new fields
- [ ] Handle cases where extraction fails (set to None/0)

**Acceptance**:

- All fields populated in happy path
- Graceful fallback when extraction fails
- No exceptions on edge cases

### Task 2.2: Update Tests for New Fields (30 min)

**Goal**: Enhance existing tests to validate new fields

**Steps**:

- [ ] Open `tests/test_scanners/test_complexity.py`
- [ ] Find existing test functions
- [ ] Add assertions for new fields:
  - `assert result.description == expected_docstring_first_line`
  - `assert result.signature == expected_signature`
  - `assert result.code is not None`
  - `assert result.comment_lines >= 0`
  - `assert result.code_lines > 0`
- [ ] Create test fixture with:
  - Function with docstring
  - Function without docstring
  - Function with type hints
  - Function with comments
- [ ] Run tests: `uv run pytest tests/test_scanners/test_complexity.py -v`

**Acceptance**:

- All tests pass
- New fields validated in at least 3 test cases
- Coverage remains ≥80%

### Task 2.3: Manual Validation (20 min)

**Goal**: Test on real code to verify correctness

**Steps**:

- [ ] Run scanner on upcast's own codebase:
  ```bash
  uv run upcast scan-complexity upcast/scanners --threshold 5 -o /tmp/complexity.yaml
  ```
- [ ] Inspect output YAML:
  - Verify `description` matches docstrings
  - Verify `signature` is valid Python
  - Verify `code` contains full function
  - Verify `comment_lines` is reasonable
  - Verify `code_lines` matches file inspection
- [ ] Test edge cases manually:
  - Function without docstring
  - Async function
  - Method in class
- [ ] Document any issues found

**Acceptance**:

- Output matches manual inspection
- All fields present and accurate
- No obvious bugs

## Phase 3: Rename Commands (Est: 45 min)

### Task 3.1: Rename Complexity Command (15 min)

**Goal**: Update command name in main.py

**Steps**:

- [ ] Open `upcast/main.py`
- [ ] Find `@main.command(name="scan-complexity")`
- [ ] Change to `@main.command(name="scan-complexity-patterns")`
- [ ] Rename function from `scan_complexity_cmd` to `scan_complexity_patterns_cmd`
- [ ] Update docstring if it mentions command name
- [ ] Keep implementation identical

**Acceptance**:

- Command renamed successfully
- Function still works identically
- No ruff violations

### Task 3.2: Rename Concurrency Command (15 min)

**Goal**: Update concurrency command name

**Steps**:

- [ ] In `upcast/main.py`
- [ ] Find `@main.command(name="scan-concurrency")`
- [ ] Change to `@main.command(name="scan-concurrency-patterns")`
- [ ] Rename function from `scan_concurrency_cmd` to `scan_concurrency_patterns_cmd`
- [ ] Update docstring if needed
- [ ] Keep implementation identical

**Acceptance**:

- Command renamed successfully
- No functional changes
- No ruff violations

### Task 3.3: Test Renamed Commands (15 min)

**Goal**: Verify commands work with new names

**Steps**:

- [ ] Test complexity command:
  ```bash
  uv run upcast scan-complexity-patterns --help
  uv run upcast scan-complexity-patterns . --threshold 20
  ```
- [ ] Test concurrency command:
  ```bash
  uv run upcast scan-concurrency-patterns --help
  uv run upcast scan-concurrency-patterns .
  ```
- [ ] Verify old names no longer work:
  ```bash
  uv run upcast scan-complexity --help  # Should fail
  uv run upcast scan-concurrency --help  # Should fail
  ```
- [ ] Check output format is unchanged

**Acceptance**:

- New command names work correctly
- Old names are removed
- Help text displays correctly
- Output format unchanged

## Phase 4: Update Documentation (Est: 30 min)

### Task 4.1: Update README.md (20 min)

**Goal**: Change all command references to new names

**Steps**:

- [ ] Open `README.md`
- [ ] Search for `scan-complexity` (without -patterns)
- [ ] Replace with `scan-complexity-patterns`
- [ ] Search for `scan-concurrency` (without -patterns)
- [ ] Replace with `scan-concurrency-patterns`
- [ ] Update example outputs to show new fields:
  - Add `description` field
  - Add `signature` field
  - Add `code` field
  - Add `comment_lines` field
  - Add `code_lines` field
- [ ] Verify all code blocks are valid YAML
- [ ] Check markdown formatting with prettier

**Acceptance**:

- All references updated
- Example outputs show new fields
- No broken markdown
- Prettier passes

### Task 4.2: Update Specifications (10 min)

**Goal**: Mark implementation as complete in specs

**Steps**:

- [ ] Open `openspec/specs/cyclomatic-complexity-scanner/spec.md`
- [ ] Verify all requirements are now satisfied:
  - Signature extraction ✓
  - Docstring extraction ✓
  - Code extraction ✓
  - Comment counting ✓
  - Code line counting ✓
- [ ] Add note about implementation completion
- [ ] Check if any other spec references need updates

**Acceptance**:

- Specs reflect current implementation
- No outdated information remains

## Phase 5: Quality Assurance (Est: 30 min)

### Task 5.1: Run Full Test Suite (10 min)

**Goal**: Ensure no regressions

**Steps**:

- [ ] Run all tests: `uv run pytest tests/ -v`
- [ ] Check coverage: `uv run pytest tests/ --cov=upcast --cov-report=term-missing`
- [ ] Verify coverage ≥80%
- [ ] Check for any new failures
- [ ] Check for any reduced coverage

**Acceptance**:

- All 251+ tests pass
- Coverage ≥80%
- No new failures

### Task 5.2: Run Linting and Formatting (10 min)

**Goal**: Ensure code quality standards

**Steps**:

- [ ] Run ruff check: `uv run ruff check`
- [ ] Fix any violations
- [ ] Run ruff format: `uv run ruff format`
- [ ] Verify no changes needed after format
- [ ] Check pre-commit would pass

**Acceptance**:

- No ruff violations
- Code properly formatted
- Pre-commit ready

### Task 5.3: Integration Testing (10 min)

**Goal**: Test on real projects

**Steps**:

- [ ] Test on wagtail project:
  ```bash
  uv run upcast scan-complexity-patterns ~/github/wagtail --threshold 15 -o /tmp/wagtail-complexity.yaml
  ```
- [ ] Inspect output:
  - Verify all fields present
  - Check signature quality
  - Check description accuracy
  - Check code extraction
  - Verify comment/code line counts
- [ ] Test on another project (e.g., upcast itself)
- [ ] Document any issues

**Acceptance**:

- Output looks correct on real projects
- All fields populated properly
- No obvious bugs or issues

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
