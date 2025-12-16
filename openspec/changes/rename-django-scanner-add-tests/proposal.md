# Rename django_scanner and Add Unit Tests

## Why

The current module name `django_scanner` is misleading as it suggests it scans all Django components, when it specifically focuses on Django models. Additionally, the module lacks comprehensive unit tests to ensure reliability and maintainability.

## What Changes

- Rename `upcast/django_scanner/` directory to `upcast/django_model_scanner/`
- Update all imports from `upcast.django_scanner` to `upcast.django_model_scanner`
- Update CLI command and documentation references
- Add comprehensive unit test suite covering:
  - Module path calculation and root finding logic
  - Field type extraction with full module paths
  - Base class extraction with full module paths
  - Abstract model inheritance and field merging
  - Meta class parsing
  - YAML export formatting
  - Edge cases and error handling

## Impact

- **Affected specs**: django-model-scanner
- **Affected code**:
  - All files in `upcast/django_scanner/` (rename to `upcast/django_model_scanner/`)
  - `upcast/main.py` (imports and CLI command)
  - `tests/test_django_model.py` (imports)
  - `openspec/changes/archive/2025-12-16-reimplement-django-scanner/` (historical reference, no changes needed)
- **Breaking change**: Module import path changes from `upcast.django_scanner` to `upcast.django_model_scanner`
- **User impact**: Users importing the module directly will need to update their imports
