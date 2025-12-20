# Migrate from Poetry to UV

## Why

Poetry has been a reliable tool for dependency management, but UV offers significantly faster dependency resolution, installation speed, and better compatibility with modern Python tooling. UV is built in Rust and provides superior performance while maintaining compatibility with standard `pyproject.toml` format. This migration will reduce CI/CD build times and improve developer experience.

## What Changes

- Replace Poetry with UV as the primary dependency management tool
- Update `pyproject.toml` to use UV-compatible build backend
- Migrate from `poetry.lock` to `uv.lock` for dependency locking
- Update GitHub Actions workflows to use UV instead of Poetry
- Modify Makefile commands to use UV CLI
- Update tox configuration to work with UV
- Update documentation and setup instructions

## Impact

- Affected specs: `build-system` (new capability)
- Affected code:
  - `pyproject.toml` - build system and dependency configuration
  - `poetry.toml` - to be removed
  - `.github/actions/setup-poetry-env/` - replace with UV setup
  - `.github/workflows/main.yml` - update CI commands
  - `.github/workflows/on-release-main.yml` - update release workflow
  - `Makefile` - replace poetry commands with UV equivalents
  - `tox.ini` - update to use UV for environment setup
- Breaking changes: None for users (package API unchanged)
- Developer workflow: Developers will need to install UV instead of Poetry
