# Proposal: Remove root_path from Scanner Metadata

## Status

- **State**: draft
- **Created**: 2025-12-23
- **Owner**: AI Agent

## Why

The `root_path` field in scanner metadata exposes absolute file system paths in scanner outputs, which creates several issues:

1. **Portability**: Outputs contain machine-specific paths like `/Users/liuyicong/github/upcast/example/blueking-paas`, making results not portable across environments
2. **Privacy**: Exposes local directory structure and usernames in scan results
3. **Inconsistency**: Not all scanners include `root_path` in metadata
4. **Limited value**: The field provides little value since file paths in results are already relative to the scan root

Currently affected scanners:

- `scan-env-vars` - includes `root_path` in metadata
- `scan-signals` - includes `root_path` in metadata

Other scanners do not include this field, showing it's not essential for scanner functionality.

## What Changes

### Remove root_path from Metadata

1. **Environment Variable Scanner** (`upcast/scanners/env_vars.py`):

   - Remove `root_path` from metadata dictionary
   - Keep `scanner_name` field

2. **Signal Scanner** (`upcast/scanners/signals.py`):
   - Remove `root_path` from metadata dictionary
   - Keep `scanner_name` field

### Update Example Outputs

Update example scan results to reflect the change:

- `example/scan-results/env-vars.yaml`
- `example/scan-results/signals.yaml`

## Success Criteria

- [x] `root_path` removed from env-vars scanner metadata
- [x] `root_path` removed from signals scanner metadata
- [x] Example outputs updated
- [ ] All tests pass
- [ ] Integration tests produce clean outputs without root_path

## Out of Scope

- Changes to other scanners (they don't use root_path)
- Changes to data models (metadata is flexible dict)
- Changes to file path handling in results (paths remain relative)

## Non-Breaking Change

This is a non-breaking change because:

- `metadata` is a flexible dictionary field
- Users parsing outputs don't depend on specific metadata fields
- File paths in `results` section remain unchanged
- Scanner functionality is not affected
