# Proposal: Refactor Scanner Architecture

## Why

The current scanner implementation has several issues that affect maintainability, consistency, and user experience:

### 1. Inconsistent Command Naming

- `scan-env-vars` - uses scan prefix
- `analyze-django-models` - uses analyze prefix
- `scan-prometheus-metrics-cmd` - uses scan prefix with -cmd suffix
- `scan-django-settings-cmd` - uses scan prefix with -cmd suffix

This naming inconsistency confuses users and makes the CLI feel unpolished.

### 2. Code Duplication

Multiple functions are duplicated across scanners:

- `_collect_python_files()` - exists in 3 different files with slight variations
- `_validate_path()` - duplicated in multiple scanners
- `export_to_yaml()` - 4 different implementations
- AST utility functions (`infer_literal_value`, `safe_as_string`, `infer_type_from_value`) - duplicated across scanners

### 3. Missing Features

- No support for file include/exclude patterns (whitelist/blacklist)
- No `description` field extraction from model docstrings (django-model-scanner)
- Inconsistent handling of inference failures
- YAML output fields are not sorted consistently
- Types lack full module paths in some scanners
- File paths are not consistently relative to scan root
- Python package root detection is not standardized

### 4. Inference Handling

- When astroid inference fails, values/types are not marked distinctly
- Failed inferences should wrap values in backticks ``and set type to`unknown`
- Type inference is scattered across modules with no unified approach

## What Changes

### 1. Unified Command Naming

Standardize all commands to use `scan-*` pattern:

- `scan-env-vars` ✅ (already correct)
- `scan-django-models` (rename from `analyze-django-models`)
- `scan-prometheus-metrics` (rename from `scan-prometheus-metrics-cmd`, remove -cmd suffix)
- `scan-django-settings` (rename from `scan-django-settings-cmd`, remove -cmd suffix)

### 2. Shared Utility Module

Create `upcast/common/` package with:

- **File Discovery**: `file_utils.py` with unified `collect_python_files()`, `validate_path()`, `find_package_root()`
- **AST Inference**: `ast_utils.py` with shared `infer_literal_value()`, `infer_type_with_fallback()`, `safe_as_string()`, `get_qualified_name()`
- **Export**: `export.py` with unified YAML/JSON export functions
- **Filtering**: `patterns.py` for include/exclude pattern matching

### 3. File Pattern Support

Add CLI options to all scan commands:

- `--include` - glob patterns for files to include
- `--exclude` - glob patterns for files to exclude
- Default excludes: `venv/`, `__pycache__/`, `build/`, `dist/`, `.tox/`, `.pytest_cache/`, `node_modules/`

### 4. Enhanced Django Model Scanner

- Extract `description` field from class docstrings (strip whitespace)
- Use unified inference functions
- Sort YAML output fields

### 5. Unified Inference Handling

All scanners SHALL:

- Wrap failed literal inferences in backticks: `` `expression` ``
- Set type to `unknown` when inference fails
- Include full module paths for types (e.g., `django.db.models.CharField`)
- Use relative paths from scan root for all file references
- Detect Python package root via `__init__.py` presence

### 6. Sorted YAML Output

All scanners SHALL:

- Sort top-level keys alphabetically
- Sort nested collections (e.g., `usages`, `locations`, `fields`)
- Use consistent field ordering within records

## Impact

### Breaking Changes

- Command name changes may break existing scripts/CI pipelines
- YAML field ordering changes (content identical, order different)

### Migration Path

- Old command names deprecated with warnings for 2 releases
- Documentation updated with migration guide
- CLI help text shows old→new command mapping

### Benefits

- **Consistency**: Unified naming and behavior across all scanners
- **Maintainability**: Shared code reduces duplication, easier to fix bugs
- **Flexibility**: File pattern support enables targeted scanning
- **Clarity**: Failed inferences clearly marked with backticks and `unknown` type
- **Quality**: Sorted output and full type paths improve readability

### Risks

- Breaking changes require user communication
- Refactoring may introduce regressions (mitigated by comprehensive tests)
- Shared utilities need careful design to support all scanner needs

## Open Questions

1. Should we maintain command aliases for backward compatibility?
2. What should be the deprecation timeline for old commands?
3. Should `--include`/`--exclude` use glob or regex patterns?
4. How to handle inference failures in nested structures (lists, dicts)?
