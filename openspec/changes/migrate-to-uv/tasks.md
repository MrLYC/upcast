# Implementation Tasks

## 1. Prepare Migration

- [ ] 1.1 Document current Poetry version and lock file hash
- [ ] 1.2 Install UV locally for testing (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- [ ] 1.3 Backup `poetry.lock` for reference

## 2. Update Project Configuration

- [ ] 2.1 Update `pyproject.toml` build-system section to use `hatchling`
- [ ] 2.2 Verify all dependencies are compatible with UV
- [ ] 2.3 Remove `poetry.toml` file
- [ ] 2.4 Generate `uv.lock` file with `uv lock`

## 3. Update Development Scripts

- [ ] 3.1 Update `Makefile` to replace poetry commands with UV equivalents
  - [ ] 3.1.1 `poetry install` → `uv sync`
  - [ ] 3.1.2 `poetry run` → `uv run`
  - [ ] 3.1.3 `poetry build` → `uv build`
  - [ ] 3.1.4 `poetry publish` → `uv publish`
- [ ] 3.2 Update `tox.ini` to use UV instead of Poetry

## 4. Update CI/CD Workflows

- [ ] 4.1 Create new composite action `.github/actions/setup-uv-env/action.yml`
- [ ] 4.2 Update `.github/workflows/main.yml` to use UV
  - [ ] 4.2.1 Replace setup-poetry-env with setup-uv-env
  - [ ] 4.2.2 Update cache keys to use `uv.lock` instead of `poetry.lock`
  - [ ] 4.2.3 Update test and type-check commands
- [ ] 4.3 Update `.github/workflows/on-release-main.yml` to use UV
  - [ ] 4.3.1 Replace poetry commands with UV equivalents
  - [ ] 4.3.2 Update version management approach

## 5. Test Migration

- [ ] 5.1 Test local installation: `uv sync`
- [ ] 5.2 Run all tests: `uv run pytest`
- [ ] 5.3 Run type checking: `uv run mypy`
- [ ] 5.4 Run pre-commit checks: `uv run pre-commit run -a`
- [ ] 5.5 Test build: `uv build`
- [ ] 5.6 Verify all Python versions (3.9-3.12) work with UV

## 6. Update Documentation

- [ ] 6.1 Update `README.md` installation instructions
- [ ] 6.2 Update `CONTRIBUTING.md` with UV setup instructions
- [ ] 6.3 Document UV-specific commands and differences from Poetry
- [ ] 6.4 Update any references to Poetry in documentation

## 7. Validation

- [ ] 7.1 Verify CI passes on all Python versions
- [ ] 7.2 Verify build artifacts are identical
- [ ] 7.3 Test release workflow in a branch
- [ ] 7.4 Confirm dependency resolution matches previous Poetry lock
