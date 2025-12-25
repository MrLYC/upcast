# Changelog: Remove root_path from Scanner Metadata

## Summary

Successfully removed the `root_path` field from scanner metadata for both environment variable and signal scanners. This change improves portability and privacy of scanner outputs while maintaining full functionality.

## Changes Made

### Code Changes

1. **Environment Variable Scanner** ([upcast/scanners/env_vars.py](upcast/scanners/env_vars.py))

   - Removed `root_path` from metadata dictionary
   - Metadata now only contains `scanner_name`

2. **Signal Scanner** ([upcast/scanners/signals.py](upcast/scanners/signals.py))
   - Removed `root_path` from metadata dictionary
   - Metadata now only contains `scanner_name`

### Output Updates

3. **Example Outputs**
   - Regenerated [example/scan-results/env-vars.yaml](example/scan-results/env-vars.yaml)
   - Regenerated [example/scan-results/signals.yaml](example/scan-results/signals.yaml)
   - Both files now have clean metadata without `root_path`

### Test Updates

4. **Test Files**
   - Updated [tests/test_scanners/test_signal.py](tests/test_scanners/test_signal.py)
   - Removed assertion checking for `root_path` in metadata
   - All tests now pass (285/285)

## Validation Results

- ✅ All unit tests pass: 285/285 tests passed
- ✅ Code quality checks pass (ruff check)
- ✅ Example outputs verified clean
- ✅ Metadata structure consistent across scanners

## Impact

**Positive:**

- Scanner outputs are now portable across different environments
- No exposure of local directory structures or usernames
- Consistent metadata structure across all scanners

**Neutral:**

- This is a non-breaking change
- Scanner functionality remains unchanged
- File paths in results section remain relative

## Date

- **Started**: 2025-12-23
- **Completed**: 2025-12-23
