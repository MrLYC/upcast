# Tasks

## 1. Update `scan_directory()` function signature

- [ ] Add `include_patterns`, `exclude_patterns`, `use_default_excludes` parameters
- [ ] Pass parameters to `collect_python_files()` utility
- [ ] Update docstring to document new parameters
- [ ] File: `upcast/env_var_scanner/cli.py`

## 2. Update `scan_env_vars` command handler

- [ ] Refactor to use common file collection with filtering
- [ ] Pass filtering parameters to `scan_directory()` and `scan_files()`
- [ ] Ensure consistent handling of files and directories
- [ ] File: `upcast/main.py`

## 3. Add integration tests

- [ ] Test `--include` pattern filtering works
- [ ] Test `--exclude` pattern filtering works
- [ ] Test `--no-default-excludes` flag works
- [ ] Test combination of include and exclude patterns
- [ ] File: `tests/test_env_var_scanner/test_cli.py` or new integration test file

## 4. Validate CLI behavior

- [ ] Run manual tests with various filtering options
- [ ] Verify help text is accurate
- [ ] Confirm behavior matches other scan commands
- [ ] Test edge cases (empty results, no matching files, etc.)
