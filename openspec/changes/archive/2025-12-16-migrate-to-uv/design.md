# Design Document: Poetry to UV Migration

## Context

The project currently uses Poetry 1.7.1 for dependency management, packaging, and publishing. While Poetry has served well, UV offers substantial performance improvements and better integration with modern Python tooling. UV is developed by Astral (the creators of Ruff) and is designed to be a drop-in replacement for pip, pip-tools, and similar tools while being significantly faster.

**Current Stack:**

- Poetry 1.7.1 for dependency management
- `poetry.lock` for dependency locking
- `poetry-core` as build backend
- Custom Poetry setup action in GitHub workflows
- Python 3.9-3.12 support

**Constraints:**

- Must maintain support for Python 3.9-3.12
- Must preserve existing dependency versions where possible
- Must maintain PyPI publishing capability
- Cannot break existing user installations (package API unchanged)

## Goals / Non-Goals

**Goals:**

- Reduce CI/CD build times through faster dependency resolution
- Simplify dependency management tooling
- Improve developer experience with faster local installs
- Maintain compatibility with standard `pyproject.toml` format
- Preserve all existing development workflows (testing, linting, type checking)

**Non-Goals:**

- Changing the project's public API or functionality
- Modifying the package's runtime dependencies
- Restructuring the project layout
- Implementing UV-specific features beyond dependency management

## Decisions

### Build Backend: Hatchling

**Decision:** Replace `poetry-core` with `hatchling` as the build backend.

**Rationale:**

- UV recommends `hatchling` for modern Python projects
- Hatchling is PEP 517/518 compliant and widely supported
- Simpler configuration than Poetry's build system
- Better integration with UV ecosystem
- Used by major projects like Ruff and UV itself

**Alternatives Considered:**

- `setuptools`: More traditional, but heavier and slower
- `flit`: Simpler, but less feature-rich than hatchling
- `pdm-backend`: Good option, but less ecosystem adoption than hatchling

### Dependency Lock File: uv.lock

**Decision:** Replace `poetry.lock` with `uv.lock`.

**Rationale:**

- UV's lock file format is more efficient and faster to resolve
- Better handling of platform-specific dependencies
- Supports lockfile v1 and v2 formats
- Compatible with pip-tools and other standard Python tooling

### Version Management

**Decision:** Use UV's built-in version management instead of Poetry's dynamic versioning.

**Rationale:**

- UV provides `uv version` command for updating version in `pyproject.toml`
- Simpler workflow without Poetry's plugin ecosystem
- Direct edit of `pyproject.toml` is more transparent

**Alternative:** Could use `bump2version` or similar tools, but UV's built-in support is sufficient.

### GitHub Actions Setup

**Decision:** Create a new composite action `setup-uv-env` to replace `setup-poetry-env`.

**Rationale:**

- Maintains the existing pattern of reusable actions
- UV installation is simpler than Poetry (single curl command)
- Caching strategy similar to Poetry (cache `.venv` directory)
- Easier to maintain than inline setup in each workflow

### Mirror Configuration

**Decision:** Migrate Poetry's mirror configuration to UV's index configuration.

**Rationale:**

- Poetry uses `[[tool.poetry.source]]` for mirrors
- UV uses `tool.uv.index` or environment variables
- Keep the JLU mirror configuration for Chinese users
- UV supports multiple indexes with priority ordering

## Technical Approach

### Configuration Mapping

```toml
# FROM (Poetry)
[tool.poetry.source]
name = "my_mirror"
url = "https://mirrors.jlu.edu.cn/pypi/web/simple"
priority = "primary"

# TO (UV)
[tool.uv]
index-url = "https://mirrors.jlu.edu.cn/pypi/web/simple"
```

### Command Mapping

| Poetry              | UV              | Notes                     |
| ------------------- | --------------- | ------------------------- |
| `poetry install`    | `uv sync`       | Installs all dependencies |
| `poetry add pkg`    | `uv add pkg`    | Add new dependency        |
| `poetry remove pkg` | `uv remove pkg` | Remove dependency         |
| `poetry run cmd`    | `uv run cmd`    | Run command in venv       |
| `poetry build`      | `uv build`      | Build distribution        |
| `poetry publish`    | `uv publish`    | Publish to PyPI           |
| `poetry lock`       | `uv lock`       | Update lock file          |
| `poetry show`       | `uv pip list`   | List dependencies         |

### CI/CD Workflow Changes

**Caching Strategy:**

```yaml
# Poetry cache key
key: venv-${{ runner.os }}-${{ inputs.python-version }}-${{ hashFiles('poetry.lock') }}

# UV cache key
key: venv-${{ runner.os }}-${{ inputs.python-version }}-${{ hashFiles('uv.lock') }}
```

**Setup Steps:**

```yaml
# Poetry setup (3 steps)
1. Install Poetry via curl
2. Add Poetry to PATH
3. Configure virtualenv in-project

# UV setup (1 step)
1. Install UV via curl (includes automatic PATH setup)
```

## Risks / Trade-offs

### Risk: UV Stability

**Risk:** UV is relatively new (first stable release in 2024) compared to Poetry.

**Mitigation:**

- UV is backed by Astral, a well-funded company with strong track record (Ruff)
- Large adoption in the ecosystem (used by major projects)
- Pin specific UV version in CI to prevent unexpected changes

### Risk: Ecosystem Compatibility

**Risk:** Some tools may have better Poetry integration than UV support.

**Mitigation:**

- UV maintains compatibility with standard Python packaging tools
- Most tools work with `pyproject.toml` and don't require specific tool support
- Tox has good UV support through native package installer

### Risk: Lock File Differences

**Risk:** UV's dependency resolution may differ from Poetry's.

**Mitigation:**

- Carefully review `uv.lock` after generation
- Test all functionality with new dependencies
- Document any dependency version changes
- Keep `poetry.lock` in git history for reference

### Trade-off: Tooling Simplicity vs Features

**Trade-off:** UV is more minimalist than Poetry (no plugin system, simpler configuration).

**Analysis:**

- Pro: Simpler mental model, fewer moving parts
- Pro: Faster, more focused tool
- Con: Less extensibility
- Verdict: For this project, simplicity is preferred over extensibility

## Migration Plan

### Phase 1: Preparation (Low Risk)

1. Document current state
2. Install UV locally
3. Test UV with current `pyproject.toml`

### Phase 2: Configuration Update (Medium Risk)

1. Update `pyproject.toml` build system
2. Generate `uv.lock`
3. Remove `poetry.toml`
4. Test local development workflow

### Phase 3: CI/CD Update (High Risk)

1. Create new `setup-uv-env` action
2. Update workflows incrementally
3. Test with draft PRs before merging

### Phase 4: Documentation (Low Risk)

1. Update README
2. Update CONTRIBUTING
3. Update any developer documentation

### Rollback Strategy

If critical issues arise:

1. Revert workflow changes
2. Restore `setup-poetry-env` action
3. Use `poetry.lock` from git history
4. Document issues for future retry

**Rollback is safe because:**

- Package API is unchanged
- Git history preserves all previous configuration
- No irreversible changes to PyPI or external systems

## Open Questions

None at this time. All technical decisions are resolved.

## References

- [UV Documentation](https://docs.astral.sh/uv/)
- [UV GitHub Repository](https://github.com/astral-sh/uv)
- [Hatchling Documentation](https://hatch.pypa.io/latest/)
- [PEP 517 - Build Backend Interface](https://peps.python.org/pep-0517/)
- [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/)
