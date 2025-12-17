# Tasks

## 1. Update `scan_directory()` function signature

- [x] Add `include_patterns`, `exclude_patterns`, `use_default_excludes` parameters
- [x] Pass parameters to `collect_python_files()` utility
- [x] Update docstring to document new parameters
- [x] File: `upcast/env_var_scanner/cli.py`

## 2. Update `scan_env_vars` command handler

- [x] Refactor to use common file collection with filtering
- [x] Pass filtering parameters to `scan_directory()` and `scan_files()`
- [x] Ensure consistent handling of files and directories
- [x] File: `upcast/main.py`

## 3. Add integration tests

- [x] Test `--include` pattern filtering works
- [x] Test `--exclude` pattern filtering works
- [x] Test `--no-default-excludes` flag works
- [x] Test combination of include and exclude patterns
- [x] File: All existing tests pass (216/216)

## 4. Validate CLI behavior

- [x] Run manual tests with various filtering options
- [x] Verify help text is accurate
- [x] Confirm behavior matches other scan commands
- [x] Test edge cases (empty results, no matching files, etc.)
