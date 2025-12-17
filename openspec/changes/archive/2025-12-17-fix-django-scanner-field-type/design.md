# Design: Fix Django Model Scanner Field Type and Model Filtering

## Context

The Django model scanner uses astroid for AST analysis. It currently extracts field information but loses important context by only storing short field names. The model filtering logic also doesn't properly handle Django's special model types (abstract and proxy).

## Solution

### 1. Fully Qualified Field Types

**Current behavior**:

```python
# For: field = models.CharField(max_length=100)
_extract_field_type(call) → "CharField"  # Just the name
```

**New behavior**:

```python
# For: field = models.CharField(max_length=100)
_extract_field_type(call) → "django.db.models.CharField"  # Full path

# For: field = CharField(max_length=100)  # Direct import
_extract_field_type(call) → "CharField"  # Still short if can't resolve
```

**Implementation approach**:

1. For `nodes.Attribute` pattern (e.g., `models.CharField`):
   - Use `astroid` inference on the `expr` (e.g., `models`)
   - Get the inferred module's qname
   - Combine: `{module_qname}.{attrname}`
2. For `nodes.Name` pattern (direct import):
   - Try to resolve through import statements
   - Use `node.infer()` to get qualified name
   - Fall back to short name if inference fails

**Why this approach**:

- Leverages astroid's existing type inference capabilities
- Consistent with how the scanner resolves other types
- Handles both common patterns (qualified and direct imports)
- Gracefully degrades to current behavior if inference fails

### 2. Abstract Field Location

**Current structure**:

```python
{
  "name": "BaseModel",
  "abstract": True,  # ❌ Duplicate
  "meta": {
    "abstract": True  # ✓ Authoritative
  }
}
```

**New structure**:

```python
{
  "name": "BaseModel",
  # No top-level abstract field
  "meta": {
    "abstract": True  # Single source of truth
  }
}
```

**Migration path**:

- Remove the assignment: `result["abstract"] = ...`
- Update internal code to read from meta
- Update tests to expect this structure

### 3. Model Filtering Logic

**Current logic** (simplified):

```python
if fields or relationships or abstract or meta:
    return result
return None
```

**Problems**:

- Keeps models with any Meta options (even trivial ones like ordering)
- Doesn't distinguish between abstract/proxy and regular empty models

**New logic**:

```python
is_abstract = result["meta"].get("abstract", False)
is_proxy = result["meta"].get("proxy", False)
has_content = bool(result["fields"] or result["relationships"])

if has_content or is_abstract or is_proxy:
    return result
return None
```

**Why this logic**:

- Abstract models must be preserved for field inheritance
- Proxy models must be preserved as they modify behavior
- Empty regular models serve no purpose (likely parsing errors)
- More explicit and easier to understand

## Trade-offs

### Field Type Length

- **Pro**: More precise, avoids naming conflicts
- **Con**: Longer output, more verbose
- **Decision**: Accept verbosity for accuracy

### Breaking Change

- **Pro**: Cleaner, more consistent structure
- **Con**: Breaks existing consumers expecting short names or top-level abstract
- **Decision**: Accept break, document in changelog

### Performance

- **Impact**: Minimal - inference is already used elsewhere
- **Measurement**: Run existing benchmarks

## Validation

1. Run full test suite
2. Check output on real Django projects
3. Verify no performance regression
4. Document breaking changes
