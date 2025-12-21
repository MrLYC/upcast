# Tasks: Refactor Scanner Architecture

## Task Breakdown

### Phase 1: Foundation Setup

#### T1.1: Create Base Models

**Estimated Time**: 3 hours
**Priority**: P0 (Blocker)

- [ ] Create `upcast/common/models.py`
- [ ] Implement `ScannerSummary` base class with required fields
- [ ] Implement `ScannerOutput` generic base class
- [ ] Add type annotations and docstrings
- [ ] Write unit tests for base models (validation, serialization)
- [ ] Test Pydantic v2 compatibility

**Acceptance Criteria**:

- `ScannerSummary` validates required fields (total_count, files_scanned, scan_duration_ms)
- `ScannerOutput[T]` correctly enforces generic type parameter
- Models can be serialized to JSON and YAML
- Models reject extra fields in summary (frozen), allow extra in output

**Files Created**:

- `upcast/common/models.py`
- `tests/test_common/test_models.py`

---

#### T1.2: Create Abstract Base Scanner

**Estimated Time**: 4 hours
**Priority**: P0 (Blocker)

- [ ] Create `upcast/common/scanner_base.py`
- [ ] Implement `BaseScanner` abstract class with common methods
- [ ] Implement `get_files_to_scan()` with include/exclude pattern support
- [ ] Implement `should_scan_file()` filtering logic
- [ ] Add type hints and comprehensive docstrings
- [ ] Write unit tests for file discovery and filtering

**Acceptance Criteria**:

- `BaseScanner` cannot be instantiated directly (abstract)
- File discovery works with glob patterns (include/exclude)
- Subclasses must implement `scan()` and `scan_file()` methods
- File filtering correctly handles common patterns (`**/*.py`, `**/test_*.py`)

**Files Created**:

- `upcast/common/scanner_base.py`
- `tests/test_common/test_scanner_base.py`

---

#### T1.3: Create CLI Utilities

**Estimated Time**: 3 hours
**Priority**: P1 (High)

- [ ] Create `upcast/common/cli.py`
- [ ] Implement `create_scanner_parser()` function
- [ ] Implement `add_scanner_arguments()` with standard flags
- [ ] Implement `run_scanner_cli()` common execution logic
- [ ] Write unit tests for argument parsing

**Acceptance Criteria**:

- All standard arguments supported: `path`, `-o/--output`, `--format`, `--include`, `--exclude`, `-v/--verbose`, `--legacy-format`
- Argument validation works (e.g., invalid format choice)
- Help text is clear and consistent

**Files Created**:

- `upcast/common/cli.py`
- `tests/test_common/test_cli.py`

---

#### T1.4: Enhance Export Functions

**Estimated Time**: 3 hours
**Priority**: P1 (High)

- [ ] Update `upcast/common/export.py`
- [ ] Implement `export_scanner_output()` for Pydantic models
- [ ] Implement `export_legacy_format()` for backward compatibility
- [ ] Add metadata injection (scanner_name, version, timestamp)
- [ ] Write unit tests for export functions

**Acceptance Criteria**:

- `export_scanner_output()` handles both Pydantic models and dicts
- YAML and JSON export work correctly
- Legacy format transformation preserves old structure
- Metadata is correctly injected

**Files Modified**:

- `upcast/common/export.py`
  **Files Created**:
- `tests/test_common/test_export_enhanced.py`

---

### Phase 2: Pilot Scanner Migration (Signal Scanner)

#### T2.1: Create Signal Scanner Models

**Estimated Time**: 2 hours
**Priority**: P0 (Blocker for pilot)

- [ ] Define `SignalInfo` Pydantic model
- [ ] Define `SignalReceiver` Pydantic model
- [ ] Define `SignalSummary` extending `ScannerSummary`
- [ ] Define `SignalOutput` extending `ScannerOutput`
- [ ] Write model validation tests

**Acceptance Criteria**:

- All signal fields have proper types and validation rules
- Models serialize to expected YAML/JSON structure
- Invalid data raises `ValidationError`

**Files Created**:

- `upcast/scanners/signal.py` (models section)
- `tests/test_scanners/test_signal_models.py`

---

#### T2.2: Implement Signal Scanner

**Estimated Time**: 4 hours
**Priority**: P0 (Blocker for pilot)

- [ ] Create `upcast/scanners/signal.py` (if not exists from T2.1)
- [ ] Move signal detection logic from old module
- [ ] Implement `SignalScanner` class extending `BaseScanner`
- [ ] Update logic to return `SignalOutput` instead of dict
- [ ] Add summary calculation logic

**Acceptance Criteria**:

- Scanner detects all signal types (built-in, custom, receivers)
- Output matches `SignalOutput` model structure
- Summary fields are correctly calculated
- All existing signal detection tests pass

**Files Created**:

- `upcast/scanners/signal.py` (complete implementation)

---

#### T2.3: Update Signal Scanner CLI

**Estimated Time**: 2 hours
**Priority**: P1 (High)

- [ ] Create `upcast/scanners/signal.py` CLI section
- [ ] Use common CLI utilities from `upcast/common/cli.py`
- [ ] Support both new and legacy output formats
- [ ] Update `upcast/main.py` to route to new scanner

**Acceptance Criteria**:

- CLI commands work: `upcast scan-signals path/`
- All CLI flags work: `-o`, `--format`, `--legacy-format`, etc.
- Output format matches design document examples

**Files Modified**:

- `upcast/scanners/signal.py` (add CLI)
- `upcast/main.py`

---

#### T2.4: Create Deprecation Wrapper

**Estimated Time**: 1 hour
**Priority**: P2 (Medium)

- [ ] Update `upcast/signal_scanner/__init__.py`
- [ ] Add imports from new location
- [ ] Add deprecation warnings using `warnings.warn()`
- [ ] Update tests to suppress deprecation warnings

**Acceptance Criteria**:

- Old import path `from upcast.signal_scanner import ...` works
- Deprecation warning is emitted with clear message
- Warning specifies new import path and removal version

**Files Modified**:

- `upcast/signal_scanner/__init__.py`

---

#### T2.5: Validate Pilot Scanner

**Estimated Time**: 2 hours
**Priority**: P0 (Blocker for next phase)

- [ ] Run all existing signal_scanner tests
- [ ] Add new validation tests (model, summary, etc.)
- [ ] Test backward compatibility (old imports, legacy format)
- [ ] Benchmark performance vs old implementation
- [ ] Update signal scanner documentation

**Acceptance Criteria**:

- All existing tests pass
- New validation tests pass
- Performance regression < 10%
- Backward compatibility verified

**Files Modified**:

- `tests/test_signal_scanner/` (update all test files)
  **Files Created**:
- `tests/test_scanners/test_signal.py` (new validation tests)

---

### Phase 3: Batch Scanner Migrations

#### Batch 1: Simple Scanners (No Existing Dataclass)

##### T3.1: Migrate Cyclomatic Complexity Scanner

**Estimated Time**: 4 hours
**Priority**: P1 (High)

- [ ] Create models in `upcast/scanners/cyclomatic_complexity.py`
- [ ] Migrate logic from `upcast/cyclomatic_complexity_scanner/`
- [ ] Update CLI to use common utilities
- [ ] Create deprecation wrapper
- [ ] Run tests and validate

**Files Created/Modified**: Similar pattern to signal scanner

---

##### T3.2: Migrate Django URL Scanner

**Estimated Time**: 4 hours
**Priority**: P1 (High)

- [ ] Create models in `upcast/scanners/django_url.py`
- [ ] Migrate logic from `upcast/django_url_scanner/`
- [ ] Update CLI
- [ ] Create deprecation wrapper
- [ ] Run tests and validate

---

##### T3.3: Migrate Unit Test Scanner

**Estimated Time**: 4 hours
**Priority**: P1 (High)

- [ ] Create models in `upcast/scanners/unit_test.py`
- [ ] Migrate logic from `upcast/unit_test_scanner/`
- [ ] Update CLI
- [ ] Create deprecation wrapper
- [ ] Run tests and validate

---

#### Batch 2: Medium Scanners (Partial Dataclass)

##### T3.4: Migrate Blocking Operation Scanner

**Estimated Time**: 5 hours
**Priority**: P1 (High)

- [ ] Enhance existing `BlockingOperation` dataclass
- [ ] Create models in `upcast/scanners/blocking_operation.py`
- [ ] Migrate logic from `upcast/blocking_operation_scanner/`
- [ ] Update CLI
- [ ] Create deprecation wrapper
- [ ] Run tests and validate

---

##### T3.5: Migrate Concurrency Pattern Scanner

**Estimated Time**: 5 hours
**Priority**: P1 (High)

- [ ] Create models in `upcast/scanners/concurrency_pattern.py`
- [ ] Migrate logic from `upcast/concurrency_pattern_scanner/`
- [ ] Update CLI
- [ ] Create deprecation wrapper
- [ ] Run tests and validate

---

##### T3.6: Migrate Django Settings Scanner

**Estimated Time**: 5 hours
**Priority**: P1 (High)

- [ ] Create models in `upcast/scanners/django_settings.py`
- [ ] Migrate logic from `upcast/django_settings_scanner/`
- [ ] Update CLI
- [ ] Create deprecation wrapper
- [ ] Run tests and validate

---

##### T3.7: Migrate Environment Variable Scanner

**Estimated Time**: 5 hours
**Priority**: P1 (High)

- [ ] Enhance existing `EnvVarInfo` dataclass
- [ ] Create models in `upcast/scanners/env_var.py`
- [ ] Migrate logic from `upcast/env_var_scanner/`
- [ ] Update CLI
- [ ] Create deprecation wrapper
- [ ] Run tests and validate

---

##### T3.8: Migrate Prometheus Metrics Scanner

**Estimated Time**: 5 hours
**Priority**: P1 (High)

- [ ] Create models in `upcast/scanners/prometheus_metrics.py`
- [ ] Migrate logic from `upcast/prometheus_metrics_scanner/`
- [ ] Update CLI
- [ ] Create deprecation wrapper
- [ ] Run tests and validate

---

#### Batch 3: Complex Scanners (Full Dataclass)

##### T3.9: Migrate Exception Handler Scanner

**Estimated Time**: 6 hours
**Priority**: P1 (High)

- [ ] Enhance existing `ExceptionHandler` dataclass
- [ ] Create models in `upcast/scanners/exception_handler.py`
- [ ] Migrate logic from `upcast/exception_handler_scanner/`
- [ ] Update CLI
- [ ] Create deprecation wrapper
- [ ] Run tests and validate

---

##### T3.10: Migrate HTTP Request Scanner

**Estimated Time**: 6 hours
**Priority**: P1 (High)

- [ ] Enhance existing `HttpRequest` dataclass
- [ ] Create models in `upcast/scanners/http_request.py`
- [ ] Migrate logic from `upcast/http_request_scanner/`
- [ ] Update CLI (preserve recent URL normalization fixes)
- [ ] Create deprecation wrapper
- [ ] Run tests and validate (all 32 tests must pass)

**Special Notes**:

- Preserve `_normalize_url_placeholders()` logic from recent fixes
- Maintain all existing functionality (timeout detection, async detection, etc.)

---

##### T3.11: Migrate Django Model Scanner

**Estimated Time**: 8 hours
**Priority**: P1 (High)

- [ ] Create models in `upcast/scanners/django_model/__init__.py`
- [ ] Keep as package due to size (> 500 LOC)
- [ ] Migrate logic from `upcast/django_model_scanner/`
- [ ] Update CLI
- [ ] Create deprecation wrapper
- [ ] Run tests and validate

**Files Created**:

- `upcast/scanners/django_model/__init__.py`
- `upcast/scanners/django_model/models.py`
- `upcast/scanners/django_model/parser.py`
- `upcast/scanners/django_model/checker.py`
- `upcast/scanners/django_model/export.py`

---

### Phase 4: Documentation

#### T4.1: Create Documentation Structure

**Estimated Time**: 2 hours
**Priority**: P2 (Medium)

- [ ] Create `docs/scanners/` directory
- [ ] Create `docs/scanners/README.md` (overview)
- [ ] Create documentation template
- [ ] Set up auto-generation from Pydantic models

**Files Created**:

- `docs/scanners/README.md`
- `docs/scanners/_template.md`
- `scripts/generate_scanner_docs.py` (if auto-generating)

---

#### T4.2: Document All Scanners

**Estimated Time**: 12 hours (1 hour per scanner)
**Priority**: P2 (Medium)

For each scanner, create `docs/scanners/{scanner-name}.md`:

- [ ] Blocking Operation Scanner
- [ ] Concurrency Pattern Scanner
- [ ] Cyclomatic Complexity Scanner
- [ ] Django Model Scanner
- [ ] Django Settings Scanner
- [ ] Django URL Scanner
- [ ] Environment Variable Scanner
- [ ] Exception Handler Scanner
- [ ] HTTP Request Scanner
- [ ] Prometheus Metrics Scanner
- [ ] Signal Scanner
- [ ] Unit Test Scanner

**Each document includes**:

- Purpose and use cases
- Usage examples
- Output schema (auto-generated from Pydantic)
- Field descriptions and value rules
- Code examples (input → output)
- Implementation notes

**Files Created**:

- `docs/scanners/blocking-operation.md`
- `docs/scanners/concurrency-pattern.md`
- `docs/scanners/cyclomatic-complexity.md`
- `docs/scanners/django-model.md`
- `docs/scanners/django-settings.md`
- `docs/scanners/django-url.md`
- `docs/scanners/env-var.md`
- `docs/scanners/exception-handler.md`
- `docs/scanners/http-request.md`
- `docs/scanners/prometheus-metrics.md`
- `docs/scanners/signal.md`
- `docs/scanners/unit-test.md`

---

#### T4.3: Create Migration Guide

**Estimated Time**: 3 hours
**Priority**: P2 (Medium)

- [ ] Create `docs/migration/v0.5-to-v1.0.md`
- [ ] Document all breaking changes
- [ ] Provide import path migration examples
- [ ] Document output format changes with examples
- [ ] Explain `--legacy-format` flag usage
- [ ] Provide timeline for deprecation removal

**Files Created**:

- `docs/migration/v0.5-to-v1.0.md`

---

#### T4.4: Update Main README

**Estimated Time**: 2 hours
**Priority**: P2 (Medium)

- [ ] Update README.md with new import examples
- [ ] Add link to scanner documentation
- [ ] Update installation instructions (Pydantic dependency)
- [ ] Update CLI command examples
- [ ] Add migration notice for users on old versions

**Files Modified**:

- `README.md`

---

### Phase 5: Cleanup & Final Validation

#### T5.1: Update All Internal Imports

**Estimated Time**: 4 hours
**Priority**: P1 (High)

- [ ] Search for all `from upcast.*_scanner import` in codebase
- [ ] Update to `from upcast.scanners.* import`
- [ ] Update test imports
- [ ] Update `upcast/main.py` scanner registration

**Acceptance Criteria**:

- No internal code uses old import paths
- All imports use new `upcast.scanners.*` paths
- `grep -r "from upcast\..*_scanner" upcast/` returns 0 results (except deprecated wrappers)

---

#### T5.2: Remove Legacy Export Functions

**Estimated Time**: 2 hours
**Priority**: P2 (Medium)

- [ ] Remove old `format_*_output()` functions from `*_scanner/export.py`
- [ ] Ensure all CLI commands use new `export_scanner_output()`
- [ ] Update tests to use new export functions

**Acceptance Criteria**:

- All scanners use unified export functions
- No duplicate export logic exists
- All tests pass with new export functions

---

#### T5.3: Comprehensive Test Sweep

**Estimated Time**: 6 hours
**Priority**: P0 (Blocker for release)

- [ ] Run full test suite: `uv run pytest`
- [ ] Verify all 617+ tests pass
- [ ] Run type checking: `uv run mypy upcast/`
- [ ] Run linting: `uv run ruff check`
- [ ] Run pre-commit hooks: `pre-commit run --all-files`
- [ ] Fix any issues found

**Acceptance Criteria**:

- All tests pass (including new validation tests)
- No type errors
- No lint errors
- Pre-commit checks pass

---

#### T5.4: Performance Benchmarking

**Estimated Time**: 3 hours
**Priority**: P1 (High)

- [ ] Create benchmark script for all scanners
- [ ] Benchmark old vs new implementation
- [ ] Document performance results
- [ ] Investigate any regressions > 10%
- [ ] Optimize hot paths if needed

**Acceptance Criteria**:

- Performance regression < 10% for all scanners
- Benchmark results documented
- Any outliers explained and addressed

**Files Created**:

- `scripts/benchmark_scanners.py`
- `docs/performance/v1.0-benchmarks.md`

---

#### T5.5: Update OpenSpec Specs

**Estimated Time**: 4 hours
**Priority**: P0 (Blocker for release)

- [ ] Create spec deltas for all affected capabilities
- [ ] Update scanner-specific specs with new requirements
- [ ] Create new specs: `scanner-architecture`, `scanner-output-models`
- [ ] Run `openspec validate --strict`
- [ ] Fix validation errors

**Files Created**:

- `openspec/changes/refactor-scanner-architecture/specs/*/spec.md` (deltas)
- `openspec/specs/scanner-architecture/spec.md` (new)
- `openspec/specs/scanner-output-models/spec.md` (new)

---

#### T5.6: Final Review & Release Prep

**Estimated Time**: 3 hours
**Priority**: P0 (Blocker for release)

- [ ] Review all changes against design document
- [ ] Verify success criteria are met
- [ ] Update CHANGELOG.md
- [ ] Tag release: `v1.0.0`
- [ ] Archive OpenSpec change: `openspec archive refactor-scanner-architecture`

**Acceptance Criteria**:

- All tasks completed
- All success criteria verified
- CHANGELOG complete
- OpenSpec change archived

---

## Timeline Estimate

### Week 1: Foundation + Pilot (33 hours)

- Phase 1: Foundation Setup (13 hours)
- Phase 2: Pilot Scanner Migration (13 hours)
- Buffer: 7 hours

### Week 2-3: Batch Migrations (60 hours)

- Batch 1: Simple Scanners (12 hours)
- Batch 2: Medium Scanners (25 hours)
- Batch 3: Complex Scanners (20 hours)
- Buffer: 3 hours

### Week 4: Documentation (19 hours)

- T4.1: Structure (2 hours)
- T4.2: Scanner Docs (12 hours)
- T4.3: Migration Guide (3 hours)
- T4.4: README Update (2 hours)

### Week 5: Cleanup & Validation (22 hours)

- T5.1: Update Imports (4 hours)
- T5.2: Remove Legacy Code (2 hours)
- T5.3: Test Sweep (6 hours)
- T5.4: Benchmarking (3 hours)
- T5.5: Update Specs (4 hours)
- T5.6: Release Prep (3 hours)

**Total Estimated Time**: 134 hours (~3.5 weeks full-time, ~5 weeks part-time)

---

## Dependencies

**Task Dependencies**:

```
T1.1 → T1.2 → T2.1 → T2.2 → T2.3 → T2.5 → [Phase 3]
T1.3 → T2.3
T1.4 → T2.3

T2.5 → T3.1, T3.2, T3.3
T3.1, T3.2, T3.3 → T3.4, T3.5, T3.6, T3.7, T3.8
T3.4-T3.8 → T3.9, T3.10, T3.11

T3.11 → T4.1 → T4.2 → T4.3 → T4.4
T3.11 → T5.1 → T5.2 → T5.3 → T5.4 → T5.5 → T5.6
```

**Critical Path**: T1.1 → T1.2 → T2.1 → T2.2 → T2.5 → T3.11 → T5.3 → T5.6

---

## Risk Items

**High Risk Tasks**:

- T3.11: Django Model Scanner migration (largest, most complex)
- T5.3: Comprehensive test sweep (many potential issues)
- T3.10: HTTP Request Scanner (recent changes, must preserve fixes)

**Mitigation**:

- Allocate extra buffer time for high-risk tasks
- Do T3.11 last in Batch 3 (most learning by then)
- Thoroughly review T3.10 to preserve URL normalization logic

---

## Progress Tracking

Create GitHub issue for this change with task checkboxes, update after completing each task.

**Milestones**:

1. ✅ Foundation Complete (T1.1-T1.4)
2. ✅ Pilot Validated (T2.1-T2.5)
3. ✅ All Scanners Migrated (T3.1-T3.11)
4. ✅ Documentation Complete (T4.1-T4.4)
5. ✅ Ready for Release (T5.1-T5.6)
