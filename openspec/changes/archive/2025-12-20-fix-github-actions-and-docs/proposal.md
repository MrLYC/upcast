# Proposal: Fix GitHub Actions and Update Documentation

## What Changes

Fix GitHub Actions CI/CD pipeline to match local pre-commit configuration and enhance project documentation:

1. **Update GitHub Actions Configuration**:

   - Upgrade ruff version in pre-commit-config.yaml to match pyproject.toml
   - Migrate ruff configuration in pyproject.toml to new `lint` section format
   - Ensure all pre-commit hooks pass in CI
   - Add comprehensive unit test execution in CI

2. **Enhance README Documentation**:
   - Update scanner count if needed (currently shows 12 scanners)
   - Add cyclomatic complexity scanner documentation (recently added)
   - Ensure all scanner commands are documented with examples
   - Verify all Quick Start examples work correctly

## Why

**Problem**:

- GitHub Actions failing due to ruff version/configuration mismatch
- Pre-commit configuration uses ruff v0.5.2 but pyproject.toml has newer format
- Ruff deprecation warnings: "top-level linter settings are deprecated"
- README may be outdated after adding new cyclomatic complexity scanner
- CI/CD pipeline doesn't run unit tests consistently

**Impact**:

- Cannot merge develop branch to main
- Contributors get confusing error messages
- Documentation doesn't reflect current capabilities
- Users cannot discover new features

**Benefits**:

1. **CI/CD Reliability**: Green builds, confident merges
2. **Developer Experience**: Consistent checks locally and in CI
3. **User Discovery**: Up-to-date documentation helps users find features
4. **Quality Assurance**: Unit tests run automatically in CI

## How

### 1. Fix Pre-commit Configuration

Update `.pre-commit-config.yaml`:

- Keep ruff-pre-commit at v0.5.2 (or update to latest compatible version)
- Ensure hooks configuration matches what runs locally

### 2. Migrate Ruff Configuration

Update `pyproject.toml`:

```toml
# OLD (deprecated)
[tool.ruff]
select = [...]
ignore = [...]
per-file-ignores = {...}

# NEW (recommended)
[tool.ruff]
target-version = "py39"
line-length = 120

[tool.ruff.lint]
select = [...]
ignore = [...]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]
```

### 3. Update GitHub Actions Workflow

Ensure `.github/workflows/main.yml`:

- Runs `make check` which includes pre-commit
- Runs `uv run pytest` with coverage for all Python versions
- Uploads coverage reports
- Uses consistent uv and Python versions

### 4. Enhance README

**Scanner Documentation**:

- Verify all 12 scanners are documented
- Add cyclomatic-complexity-scanner section (if not present)
- Update Quick Start examples
- Ensure command syntax matches actual CLI

**Structure**:

- Keep existing organization (Quick Start, Common Options, Scanners by category)
- Add new scanner in "Code Quality Scanners" section
- Include example output and key features

## Impact

### Users Affected

- All contributors (CI passes consistently)
- All users (accurate documentation)
- Maintainers (easier to review PRs)

### Migration Required

- None (configuration and documentation changes only)

### Breaking Changes

- None

### Performance Considerations

- GitHub Actions may take slightly longer with full test suite
- No runtime impact on upcast itself

## Alternatives Considered

### Alternative 1: Keep Old Ruff Configuration

**Pros**: No changes needed
**Cons**: Deprecation warnings, eventual breakage
**Decision**: Migrate now to avoid future issues

### Alternative 2: Remove Ruff from Pre-commit

**Pros**: Simpler pre-commit setup
**Cons**: Lose automatic code quality checks
**Decision**: Keep ruff, fix configuration

### Alternative 3: Minimal README Update

**Pros**: Less work
**Cons**: Users can't discover new features
**Decision**: Complete documentation update

## Open Questions

None - this is a straightforward configuration and documentation fix.

## Success Criteria

1. **CI Passes**:

   - [x] All pre-commit hooks pass in GitHub Actions
   - [x] No ruff deprecation warnings
   - [x] Unit tests run successfully for Python 3.9, 3.10, 3.11, 3.12
   - [x] Coverage reports upload correctly
   - [x] mypy type checking passes

2. **Local Development**:

   - [x] `make check` passes locally
   - [x] `make test` passes locally (617 tests)
   - [x] `uv run pre-commit run --all-files` passes
   - [x] `uv run mypy` passes

3. **Documentation**:

   - [x] README accurately lists all scanners
   - [x] Cyclomatic complexity scanner documented
   - [x] All example commands work
   - [x] Quick Start section up-to-date

4. **Validation**:
   - [ ] Successfully merge develop to main (pending user action)
   - [ ] No CI failures on main branch (pending merge)
   - [ ] README renders correctly on GitHub
