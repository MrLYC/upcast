# Proposal: Fix CLI Parameter Handling

## Why

The `scan-env-vars` command currently accepts file filtering options (`--include`, `--exclude`, `--no-default-excludes`) but does not pass them to the underlying scanner functions. This means:

1. Users who specify `--include` or `--exclude` patterns expect filtering behavior, but it has no effect
2. The `--no-default-excludes` flag is ignored, making it impossible to scan files in default-excluded directories
3. This violates the CLI interface specification which requires all scan commands to support file pattern filtering

**Current Behavior:**

```bash
# These options are silently ignored:
upcast scan-env-vars --include "*/settings.py" --exclude "*/tests/*.py" myproject/
```

The command accepts these parameters in its signature but never passes them to `scan_directory()` or `scan_files()`.

**Impact:**

- User confusion when filtering doesn't work as expected
- Inconsistent behavior across scan commands (other commands properly handle these options)
- Violation of the cli-interface specification

## What Changes

### Fix `scan-env-vars` Command

Update the `scan_env_vars` command in `upcast/main.py` to:

1. Pass `include`, `exclude`, and `no_default_excludes` parameters to scanner functions
2. Refactor to use common file collection with filtering before scanning
3. Handle both single files and directories consistently

### Update `env_var_scanner` Functions

Modify `upcast/env_var_scanner/cli.py`:

1. Add filtering parameters to `scan_directory()` function signature
2. Pass filtering options to `collect_python_files()` utility
3. Update function documentation

## Impact

### Breaking Changes

None - this is a bug fix that enables existing, documented functionality.

### Benefits

- **Consistency**: `scan-env-vars` behaves like other scan commands
- **Correctness**: Options work as documented and expected
- **Usability**: Users can properly filter files during scanning

### Risks

Minimal - changes are localized to the env-var-scanner CLI and main command handler. All other scanners already implement this correctly.

## Open Questions

None - the implementation pattern is already established in other scan commands.
