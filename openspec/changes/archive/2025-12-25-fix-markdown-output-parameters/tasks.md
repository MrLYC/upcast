# Implementation Tasks

## 1. Add Markdown Parameters to Missing Commands

- [ ] 1.1 Add parameters to `scan-blocking-operations`

  - Add `--format` option with markdown choice
  - Add `--markdown-language` option
  - Add `--markdown-title` option
  - Update function signature
  - Pass parameters to `run_scanner_cli()`

- [ ] 1.2 Add parameters to `scan-concurrency-patterns`

  - Same parameter additions as above

- [ ] 1.3 Add parameters to `scan-django-models`

  - Same parameter additions as above

- [ ] 1.4 Add parameters to `scan-django-settings`

  - Same parameter additions as above

- [ ] 1.5 Add parameters to `scan-django-urls`

  - Same parameter additions as above

- [ ] 1.6 Add parameters to `scan-exception-handlers`

  - Same parameter additions as above

- [ ] 1.7 Add parameters to `scan-http-requests`

  - Same parameter additions as above

- [ ] 1.8 Add parameters to `scan-metrics`

  - Same parameter additions as above

- [ ] 1.9 Add parameters to `scan-signals`

  - Same parameter additions as above

- [ ] 1.10 Add parameters to `scan-unit-tests`

  - Same parameter additions as above

- [ ] 1.11 Add parameters to `scan-redis-usage`

  - Same parameter additions as above

- [ ] 1.12 Add parameters to `scan-module-symbols`
  - Same parameter additions as above

## 2. Verify Django Field Parameters Fix

- [ ] 2.1 Regenerate all scanner results with `make test-integration`

  - Verify no TypeErrors occur
  - Check all YAML files are generated

- [ ] 2.2 Verify Django models output
  - Check that `type` field is not duplicated in `parameters`
  - Verify field parameters only contain actual field arguments

## 3. Testing and Validation

- [ ] 3.1 Run integration tests

  - Execute `make test-integration`
  - Verify all scanners complete successfully
  - Commit updated scan results if they changed

- [ ] 3.2 Test markdown output

  - Run at least one scanner with `--format markdown`
  - Test with `--markdown-language zh`
  - Test with `--markdown-title "Custom Title"`

- [ ] 3.3 Run unit tests

  - Execute `uv run pytest`
  - Verify no regressions

- [ ] 3.4 Run pre-commit hooks
  - Execute `uv run pre-commit run --all-files`
  - Fix any code quality issues
