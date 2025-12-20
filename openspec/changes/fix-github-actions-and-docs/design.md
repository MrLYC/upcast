# Design: Fix GitHub Actions and Update Documentation

## Overview

This is a configuration and documentation maintenance change with no architectural impact. The work focuses on aligning CI/CD configuration with local development tools and ensuring documentation accuracy.

## Architecture Impact

**None** - This change only updates:

- Configuration files (pyproject.toml, .pre-commit-config.yaml)
- Documentation (README.md)
- CI workflow definitions (.github/workflows/main.yml)

No code changes to the upcast library itself.

## Configuration Migration Strategy

### Ruff Configuration Format

**Current (Deprecated)**:

```toml
[tool.ruff]
select = ["E", "F", ...]
ignore = ["E501", ...]
per-file-ignores = {"tests/*" = ["S101"]}
```

**Target (New Format)**:

```toml
[tool.ruff]
target-version = "py39"
line-length = 120
fix = true

[tool.ruff.lint]
select = ["E", "F", ...]
ignore = ["E501", ...]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]
"tests/test_cyclomatic_complexity_scanner/fixtures/*" = ["TRY301", "TRY300", "SIM102"]
```

**Migration Path**:

1. Create new `[tool.ruff.lint]` section
2. Move `select`, `ignore` to lint section
3. Rename `per-file-ignores` section
4. Keep top-level settings (target-version, line-length, fix)
5. Test locally before committing

## Documentation Structure

README.md organization:

```
# upcast
├── Quick Start (4 example commands)
├── Installation
├── Common Options
├── Django Scanners (3 scanners)
│   ├── scan-django-models
│   ├── scan-django-settings
│   └── scan-django-url
├── Code Analysis Scanners (5 scanners)
│   ├── scan-env-vars
│   ├── scan-prometheus-metrics
│   ├── scan-concurrency-patterns
│   ├── scan-signals
│   └── scan-unit-tests
├── HTTP & Exception Scanners (2 scanners)
│   ├── scan-http-requests
│   └── scan-exception-handlers
├── Code Quality Scanners (2 scanners) ← ADD cyclomatic-complexity here
│   ├── scan-blocking-operations
│   └── scan-complexity ← NEW
└── Architecture
```

## Testing Strategy

### Local Validation

1. `make check` - runs pre-commit hooks
2. `make test` - runs pytest with coverage
3. `uv run pre-commit run --all-files` - explicit pre-commit check

### CI Validation

1. GitHub Actions runs on push to develop
2. Tests run for Python 3.9, 3.10, 3.11, 3.12
3. Coverage uploads to codecov for Python 3.11

### Documentation Validation

1. Test each Quick Start example manually
2. Verify README renders correctly on GitHub
3. Ensure all command syntax matches CLI help

## Rollback Plan

If changes cause issues:

1. **Configuration issues**: Revert pyproject.toml and .pre-commit-config.yaml
2. **CI failures**: Revert .github/workflows/main.yml
3. **Documentation**: Revert README.md

All changes are in version control and easily reversible.

## Dependencies

**External**:

- ruff-pre-commit (currently v0.5.2)
- uv (for package management)
- pre-commit (for hook management)

**Internal**:

- All scanner modules in upcast/
- Existing test suite
- Makefile commands

## Success Metrics

1. **Zero CI failures** on develop branch
2. **Zero deprecation warnings** from ruff
3. **100% passing tests** for all Python versions
4. **Accurate documentation** - all examples work
5. **Clean merge** to main branch

## Risk Assessment

**Low Risk** because:

- Only configuration and documentation changes
- No code logic modifications
- Easy to test locally before pushing
- Easy to revert if problems occur
- No user-facing behavior changes

**Potential Issues**:

- Ruff version incompatibility (mitigated by testing locally)
- Breaking changes in ruff rules (mitigated by checking release notes)
- Documentation examples out of sync (mitigated by manual testing)
