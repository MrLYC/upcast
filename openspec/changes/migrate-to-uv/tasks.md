# Implementation Tasks

## 1. Prepare Migration

- [x] 1.1 Document current Poetry version and lock file hash
- [x] 1.2 Install UV locally for testing (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- [x] 1.3 Backup `poetry.lock` for reference

## 2. Update Project Configuration

- [x] 2.1 Update `pyproject.toml` build-system section to use `hatchling`
- [x] 2.2 Verify all dependencies are compatible with UV
- [x] 2.3 Remove `poetry.toml` file
- [x] 2.4 Generate `uv.lock` file with `uv lock`

## 3. Update Development Scripts

- [x] 3.1 Update `Makefile` to replace poetry commands with UV equivalents
  - [x] 3.1.1 `poetry install` → `uv sync`
  - [x] 3.1.2 `poetry run` → `uv run`
  - [x] 3.1.3 `poetry build` → `uv build`
  - [x] 3.1.4 `poetry publish` → `uv publish`
- [x] 3.2 Update `tox.ini` to use UV instead of Poetry

## 4. Update CI/CD Workflows

- [x] 4.1 Create new composite action `.github/actions/setup-uv-env/action.yml`
- [x] 4.2 Update `.github/workflows/main.yml` to use UV
  - [x] 4.2.1 Replace setup-poetry-env with setup-uv-env
  - [x] 4.2.2 Update cache keys to use `uv.lock` instead of `poetry.lock`
  - [x] 4.2.3 Update test and type-check commands
- [x] 4.3 Update `.github/workflows/on-release-main.yml` to use UV
  - [x] 4.3.1 Replace poetry commands with UV equivalents
  - [x] 4.3.2 Update version management approach

## 5. Test Migration

- [x] 5.1 Test local installation: `uv sync`
- [x] 5.2 Run all tests: `uv run pytest`
- [x] 5.3 Run type checking: `uv run mypy`
- [x] 5.4 Run pre-commit checks: `uv run pre-commit run -a`
- [x] 5.5 Test build: `uv build`
- [x] 5.6 Verify all Python versions (3.9-3.12) work with UV

## 6. Update Documentation

- [x] 6.1 Update `README.md` installation instructions
- [x] 6.2 Update `CONTRIBUTING.md` with UV setup instructions
- [x] 6.3 Document UV-specific commands and differences from Poetry
- [x] 6.4 Update any references to Poetry in documentation

## 7. Validation

- [x] 7.1 Verify CI passes on all Python versions
- [x] 7.2 Verify build artifacts are identical
- [x] 7.3 Test release workflow in a branch
- [x] 7.4 Confirm dependency resolution matches previous Poetry lock
