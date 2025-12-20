# Proposal: fix-env-var-scanner-defaults

## What Changes

Fix environment variable scanner's `defaults` field to preserve actual value types instead of converting everything to strings, and exclude dynamic statement defaults that are already captured in usages.

## Why

The current implementation has two issues that reduce data quality:

1. **Type Coercion Problem**: All default values are converted to strings, losing type information. For example:

   - `False` becomes `'False'` (string instead of boolean)
   - `0` becomes `'0'` (string instead of integer)
   - This makes it harder for downstream tools to correctly interpret and validate configuration

2. **Redundant Statement Defaults**: When a default value is a complex expression (e.g., `` `os.getenv('OTHER_VAR', '')` ``), it appears in the `defaults` list wrapped in backticks. This is redundant because:
   - The full statement is already captured in the `usages[].statement` field
   - Backtick-wrapped expressions are not useful as "default values" for configuration documentation
   - They clutter the defaults list and make it harder to understand actual configuration options

Example of current problematic output:

```yaml
BKAPP_BUSINESS_DIAGNOSIS:
  defaults:
    - "False" # Should be: false (boolean)
  required: false
  types:
    - bool

BKAPP_CMDB_URL:
  defaults:
    - "`os.getenv('BK_CC_HOST', '')`" # Redundant - already in usages
  required: false
  types: []
  usages:
    - location: kingeye/fusion/config/default.py:373
      statement: os.getenv('BKAPP_CMDB_URL', os.getenv('BK_CC_HOST', ''))
```

Expected output after fix:

```yaml
BKAPP_BUSINESS_DIAGNOSIS:
  defaults:
    - false # Preserved as boolean
  required: false
  types:
    - bool

BKAPP_CMDB_URL:
  defaults: [] # No dynamic defaults - see statement in usages
  required: false
  types: []
  usages:
    - location: kingeye/fusion/config/default.py:373
      statement: os.getenv('BKAPP_CMDB_URL', os.getenv('BK_CC_HOST', ''))
```

## How

### Core Changes

1. **Preserve Type Information**:

   - Change `EnvVarUsage.default` from `Optional[str]` to `Optional[Any]`
   - Update `infer_literal_value()` to return actual typed values (bool, int, float, str, None) instead of string representations
   - Remove `str()` wrapper in `env_var_parser.py` when storing default values

2. **Filter Dynamic Defaults**:
   - When adding defaults to `EnvVarInfo.defaults` list, check if the value is wrapped in backticks (indicating it's a dynamic expression)
   - Skip adding defaults that start with `` ` `` to the defaults list
   - These statements remain available in `usage.default` for individual usage inspection

### Implementation Details

**File: `upcast/env_var_scanner/env_var_parser.py`**

- Change `EnvVarUsage.default: Optional[str]` to `Optional[Any]`
- Change `EnvVarInfo.defaults: list[str]` to `list[Any]`
- Remove `str()` conversion when assigning default values (lines 104, 109, 118, 123, 131, 141, 151, 162, 172)
- Update `add_usage()` to filter backtick-wrapped defaults:
  ```python
  if usage.default is not None:
      # Skip dynamic expressions (wrapped in backticks)
      if not (isinstance(usage.default, str) and usage.default.startswith('`') and usage.default.endswith('`')):
          if usage.default not in self.defaults:
              self.defaults.append(usage.default)
  ```

**File: `upcast/env_var_scanner/ast_utils.py`**

- `infer_literal_value()` already returns typed values via `infer_value_with_fallback()` - no changes needed
- Verify that backtick wrapping happens in `upcast/common/ast_utils.py` for uninferrable values

**File: `upcast/env_var_scanner/export.py`**

- No changes needed - YAML/JSON export will automatically handle typed values correctly

### Testing Strategy

Add test cases to verify:

1. Boolean defaults (`False`, `True`) are preserved as booleans
2. Integer defaults (`0`, `42`) are preserved as integers
3. Float defaults (`3.14`) are preserved as floats
4. String defaults (`'text'`) remain strings
5. None defaults are preserved as None/null
6. Dynamic expression defaults (backtick-wrapped) are excluded from defaults list
7. Complex nested defaults (e.g., `os.getenv()` calls) don't pollute the defaults list

## Impact

### Changed Behavior

- **YAML/JSON output**: `defaults` field will now contain actual typed values instead of string representations
- **Breaking change**: Tools consuming the output must handle typed values instead of expecting all strings
- **Benefit**: More accurate representation of configuration, better type validation support

### Modified Files

- `upcast/env_var_scanner/env_var_parser.py`: Type annotations and default filtering
- `tests/test_env_var_scanner/test_integration.py`: New test cases for type preservation
- `openspec/specs/env-var-scanner/spec.md`: Updated requirements for default value handling

### Backward Compatibility

**Potentially breaking**: Existing tools that expect all defaults to be strings will need updates. However, this is a quality improvement that brings the output closer to the actual code semantics.

Migration path for consumers:

- Previously: `default == 'False'` (string comparison)
- After fix: `default == False` (boolean comparison) or `default is False`

## Alternatives Considered

1. **Keep string representation, add separate `defaults_typed` field**:

   - Rejected: Adds complexity and duplication
   - Better to fix the existing field to be correct

2. **Add a flag to control output format**:

   - Rejected: Adds unnecessary configuration complexity
   - The typed output is always more correct

3. **Only fix type coercion, keep dynamic defaults**:
   - Rejected: Dynamic defaults are still redundant and confusing
   - Both issues should be fixed together

## Open Questions

None - implementation path is clear.

## Success Criteria

- [ ] `defaults` field contains actual Python types (bool, int, float, str, None), not string representations
- [ ] Dynamic expression defaults (backtick-wrapped) are excluded from `defaults` list
- [ ] All existing tests pass with updated assertions
- [ ] New tests verify type preservation and dynamic default filtering
- [ ] Documentation updated to reflect typed defaults
- [ ] `openspec validate fix-env-var-scanner-defaults --strict` passes
