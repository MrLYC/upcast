# Tasks: fix-env-var-scanner-defaults

## Implementation Tasks

### Phase 1: Update Data Structures

- [ ] **Update EnvVarUsage dataclass**: Change `default: Optional[str]` to `default: Optional[Any]` in `upcast/env_var_scanner/env_var_parser.py`

  - Location: Line ~25
  - Add import: `from typing import Any` if not present
  - Update type annotation only - no logic changes

- [ ] **Update EnvVarInfo dataclass**: Change `defaults: list[str]` to `defaults: list[Any]`
  - Location: Line ~36
  - Update type annotation only

### Phase 2: Remove String Conversions

- [ ] **Remove str() wrappers in parse_env_var_usage()**: Update all lines that assign to `default` variable
  - **Line ~104**: `default = str(infer_literal_value(default_node))` → `default = infer_literal_value(default_node)`
  - **Line ~109**: Same pattern for getenv without default case (if applicable)
  - **Line ~118**: Same pattern for environ.get
  - **Line ~123**: Same pattern for django-environ keyword default
  - **Line ~131**: Same pattern for django-environ positional default
  - **Line ~141**: Same pattern for env() keyword default
  - **Line ~151**: Same pattern for env() positional default
  - **Line ~162**: Same pattern for 'or' expression default
  - **Line ~172**: Same pattern for type conversion wrapper
  - Test after each change: `uv run pytest tests/test_env_var_scanner/test_integration.py -v`

### Phase 3: Filter Dynamic Defaults

- [ ] **Update add_usage() method**: Add filtering logic in `EnvVarInfo.add_usage()`
  - Location: `upcast/env_var_scanner/env_var_parser.py` around line 47
  - Replace current logic:
    ```python
    if usage.default and usage.default not in self.defaults:
        self.defaults.append(usage.default)
    ```
  - With filtered logic:
    ```python
    if usage.default is not None:
        # Skip dynamic expressions (wrapped in backticks)
        if not (isinstance(usage.default, str) and usage.default.startswith('`') and usage.default.endswith('`')):
            if usage.default not in self.defaults:
                self.defaults.append(usage.default)
    ```
  - Note: Changed `if usage.default` to `if usage.default is not None` to handle falsy defaults like `False`, `0`, `""`

### Phase 4: Update Tests

- [ ] **Update existing test assertions**: Fix tests that expect string defaults

  - File: `tests/test_env_var_scanner/test_integration.py`
  - Search for assertions like `assert 'False' in env_vars['VAR'].defaults`
  - Replace with: `assert False in env_vars['VAR'].defaults`
  - Run: `uv run pytest tests/test_env_var_scanner/ -v`

- [ ] **Add type preservation tests**: Create new test cases in `test_integration.py`

  - Test boolean defaults: `os.getenv('DEBUG', False)` → defaults contains `False` (bool)
  - Test integer defaults: `os.getenv('PORT', 8000)` → defaults contains `8000` (int)
  - Test float defaults: `os.getenv('TIMEOUT', 3.14)` → defaults contains `3.14` (float)
  - Test None defaults: `os.getenv('KEY', None)` → defaults contains `None`
  - Test string defaults: `os.getenv('URL', 'http://localhost')` → defaults contains string
  - Create test fixture file: `tests/test_env_var_scanner/fixtures/typed_defaults.py`

- [ ] **Add dynamic default filtering tests**: Create test cases for backtick exclusion
  - Test single dynamic default: `os.getenv('VAR1', os.getenv('VAR2', ''))` → defaults is empty `[]`
  - Test mixed defaults: Multiple usages with static + dynamic → only static in defaults
  - Test all dynamic: All usages have dynamic defaults → defaults is empty `[]`
  - Create test fixture: `tests/test_env_var_scanner/fixtures/dynamic_defaults.py`

### Phase 5: Validation and Documentation

- [ ] **Verify export formats**: Check YAML/JSON output correctness

  - Run scanner on test fixtures
  - Verify YAML renders: `false` (not `'False'`), `0` (not `'0'`), `null` (not `'None'`)
  - Verify JSON renders: `false`, `0`, `null` (not strings)
  - Check: `uv run upcast scan-env-vars tests/test_env_var_scanner/fixtures/typed_defaults.py`

- [ ] **Update README examples**: If README shows scanner output, update examples

  - File: `README.md`
  - Search for environment variable scanner examples
  - Update to show typed defaults instead of string defaults

- [ ] **Run full test suite**: Ensure no regressions

  - Command: `uv run pytest tests/test_env_var_scanner/ -v`
  - Fix any failing tests
  - Ensure all tests pass

- [ ] **Check code quality**: Run linting and formatting

  - Command: `uv run ruff check upcast/env_var_scanner/`
  - Command: `uv run ruff format upcast/env_var_scanner/`
  - Fix any issues

- [ ] **Validate OpenSpec**: Ensure proposal is correct
  - Command: `openspec validate fix-env-var-scanner-defaults --strict`
  - Fix any validation errors
  - Ensure all requirements have scenarios

## Validation Checkpoints

After each phase:

1. Run relevant tests: `uv run pytest tests/test_env_var_scanner/ -k <test_pattern> -v`
2. Check for type errors: `uv run mypy upcast/env_var_scanner/` (if configured)
3. Verify manually: `uv run upcast scan-env-vars <test-file>` and inspect output

Final validation:

1. All tests pass: `uv run pytest tests/test_env_var_scanner/ -v`
2. No regressions: `uv run pytest tests/ -v`
3. Code quality: `uv run ruff check upcast/env_var_scanner/`
4. OpenSpec valid: `openspec validate fix-env-var-scanner-defaults --strict`
5. Manual smoke test: Scan a real project and verify output quality
