# Tasks: Fix Django Model Scanner Field Type and Model Filtering

**Status**: Planning

## Task List

1. **Update field type extraction to return fully qualified names**

   - Modify `_extract_field_type()` in `model_parser.py`
   - Add type inference logic for `nodes.Attribute` case
   - Return full module path (e.g., `django.db.models.CharField`)
   - Add fallback to short name if inference fails
   - **Validation**: Unit tests verify full qualified names in output

2. **Remove redundant abstract field from model dict**

   - Remove `result["abstract"] = result["meta"].get("abstract", False)` line from `parse_model()`
   - Update `merge_abstract_fields()` to read from `model["meta"].get("abstract", False)`
   - Search and update any other code referencing `model["abstract"]`
   - **Validation**: Run all existing tests to ensure no breakage

3. **Fix model filtering logic for empty models**

   - Update the return logic in `parse_model()`
   - Check for `meta.abstract == True` OR `meta.proxy == True`
   - Return None only when: no fields AND no relationships AND not abstract AND not proxy
   - **Validation**: Unit tests for empty, abstract, proxy, and hybrid models

4. **Add comprehensive test coverage**

   - Test field type returns fully qualified names
   - Test abstract field only in meta (not top-level)
   - Test proxy model preservation
   - Test empty non-abstract/non-proxy model filtering
   - Test abstract model with no fields is preserved
   - Test proxy model with no fields is preserved
   - **Validation**: `pytest tests/test_django_model_scanner/ -v` passes with new tests

5. **Update spec requirements**
   - Add scenario for fully qualified field type extraction
   - Add scenario for proxy model handling
   - Update abstract model handling to clarify meta-only storage
   - **Validation**: `openspec validate fix-django-scanner-field-type --strict` passes

## Dependencies

- Tasks 1-3 can be done in parallel
- Task 4 depends on tasks 1-3 (tests verify the changes)
- Task 5 should be done after implementation is complete

## Testing Strategy

- Run unit tests after each change to catch regressions early
- Add new test cases before or alongside implementation (TDD approach)
- Verify output format matches expected structure
- Test edge cases: aliased imports, indirect inheritance, missing Meta class
