# Fix Django Model Scanner Field Type and Model Filtering

## Why

The current `django_model_scanner` has three issues affecting accuracy and usability:

1. **Incomplete field type information**: `_extract_field_type()` returns only the short field name (e.g., `CharField`) instead of the fully qualified name (e.g., `django.db.models.fields.CharField`). This loses important module context and makes it harder to distinguish between Django fields and custom field classes with the same name.

2. **Redundant abstract field**: `parse_model()` duplicates the `abstract` flag both in the top-level model dict and inside `meta`, creating confusion about the single source of truth. The Meta class is the authoritative source for this information.

3. **Incorrect model filtering**: The logic for skipping empty models doesn't properly check for `proxy` models. Proxy models should be preserved (like abstract models) even without fields, since they modify model behavior without defining new fields.

These issues reduce the scanner's accuracy and create inconsistent output.

## What Changes

**Field Type Extraction**:

- Modify `_extract_field_type()` to return fully qualified field type when available
- For `nodes.Attribute` pattern (e.g., `models.CharField`), infer the module path through astroid type inference
- Return format: `django.db.models.fields.CharField` instead of just `CharField`
- Fall back to short name if full path cannot be resolved

**Abstract Flag Handling**:

- Remove the top-level `abstract` field from the model dictionary
- Keep `abstract` only within the `meta` dictionary where it belongs
- Update all code that references `model["abstract"]` to use `model["meta"].get("abstract", False)`

**Model Filtering Logic**:

- Update `parse_model()` to return `None` for truly empty models
- Keep models that have:
  - Any fields, OR
  - Any relationships, OR
  - `meta.abstract == True`, OR
  - `meta.proxy == True`
- Skip only models with no fields, no relationships, and not abstract/proxy

**Test Coverage**:

- Add tests for fully qualified field types
- Add tests for proxy model handling
- Add tests for abstract field in meta only
- Verify empty model filtering logic

## Impact

- **Affected specs**: `django-model-scanner` spec needs updates to field type and model filtering requirements
- **Affected code**:
  - `upcast/django_model_scanner/model_parser.py`: Update `_extract_field_type()`, `parse_model()`, `merge_abstract_fields()`
  - `upcast/django_model_scanner/checker.py`: Update references to abstract field
  - Tests: Add comprehensive test coverage
- **Breaking change**: Output format changes for field types (now includes full module path)
- **User impact**:
  - More precise field type information
  - Cleaner model metadata structure
  - Correct handling of proxy models
