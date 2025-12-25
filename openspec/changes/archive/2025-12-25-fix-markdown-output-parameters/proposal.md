# Proposal: Fix Markdown Output Parameters

## Summary

Fix CLI commands that are missing markdown output parameters (`--markdown-language` and `--markdown-title`) introduced in a recent PR, causing integration test failures.

## Problem

A recent PR added markdown as an output format with language selection capability. However, not all scanner commands were updated to include the required `--markdown-language` and `--markdown-title` parameters, causing `TypeError` exceptions when running `make test-integration`.

Affected commands:

- `scan-blocking-operations`
- `scan-concurrency-patterns`
- `scan-django-models`
- `scan-django-settings`
- `scan-django-urls`
- `scan-exception-handlers`
- `scan-http-requests`
- `scan-metrics`
- `scan-signals`
- `scan-unit-tests`
- `scan-redis-usage`
- `scan-module-symbols`

## Solution

Add the missing Click decorators and function parameters to all scanner commands to support:

1. `--format` option with markdown choice
2. `--markdown-language` option (default: "en", choices: ["en", "zh"])
3. `--markdown-title` option (optional custom title)

Pass these parameters to `run_scanner_cli()` to enable consistent markdown output across all scanners.

## Impact

- **Users**: All scanner commands will support markdown output with language selection
- **Testing**: Integration tests will pass
- **Maintenance**: Consistent CLI interface across all scanners

## Alternatives Considered

1. **Remove markdown support**: Too drastic, loses new functionality
2. **Make parameters optional in run_scanner_cli**: Would require complex default handling
3. **Use Click context**: Adds unnecessary complexity

## Success Criteria

- [ ] All scanner commands accept `--format markdown`
- [ ] All commands accept `--markdown-language` and `--markdown-title`
- [ ] `make test-integration` passes without TypeErrors
- [ ] Markdown output works correctly for all scanners
