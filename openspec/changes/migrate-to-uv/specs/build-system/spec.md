# Build System Specification

## ADDED Requirements

### Requirement: UV Package Manager

The project SHALL use UV as the primary package manager for dependency management, installation, and publishing.

#### Scenario: Install dependencies

- **WHEN** a developer runs the install command
- **THEN** UV SHALL install all dependencies from `uv.lock`
- **AND** create a virtual environment in `.venv/`

#### Scenario: Add new dependency

- **WHEN** a developer adds a new dependency
- **THEN** UV SHALL update `pyproject.toml` with the dependency
- **AND** update `uv.lock` with resolved versions
- **AND** install the new dependency in the virtual environment

#### Scenario: Run command in virtual environment

- **WHEN** a developer executes a command with UV
- **THEN** UV SHALL run the command in the project's virtual environment
- **AND** ensure all project dependencies are available

### Requirement: Hatchling Build Backend

The project SHALL use Hatchling as the build backend for creating distribution packages.

#### Scenario: Build wheel package

- **WHEN** the build command is executed
- **THEN** Hatchling SHALL create a wheel file in `dist/`
- **AND** include all package files as specified in `pyproject.toml`

#### Scenario: Build source distribution

- **WHEN** the build command is executed
- **THEN** Hatchling SHALL create a source distribution in `dist/`
- **AND** include all source files and metadata

### Requirement: Dependency Locking

The project SHALL maintain a `uv.lock` file for reproducible dependency resolution.

#### Scenario: Lock dependencies

- **WHEN** dependencies are added or updated
- **THEN** UV SHALL generate or update `uv.lock`
- **AND** lock all transitive dependencies with exact versions
- **AND** include platform-specific dependency information

#### Scenario: Sync from lock file

- **WHEN** installing from a lock file
- **THEN** UV SHALL install exact versions specified in `uv.lock`
- **AND** ensure reproducible environments across machines

### Requirement: Python Version Support

The project SHALL support Python 3.9 through 3.12.

#### Scenario: Version compatibility

- **WHEN** the package is installed on Python 3.9-3.12
- **THEN** all dependencies SHALL be compatible
- **AND** all tests SHALL pass

#### Scenario: Version constraint enforcement

- **WHEN** installing on unsupported Python versions
- **THEN** UV SHALL report an error
- **AND** prevent installation

### Requirement: Mirror Configuration

The project SHALL support custom package index configuration for different regions.

#### Scenario: Use custom mirror

- **WHEN** UV is configured with a custom index URL
- **THEN** UV SHALL fetch packages from the specified mirror
- **AND** fall back to PyPI if packages are unavailable

#### Scenario: Chinese mirror for development

- **WHEN** developers use the JLU mirror configuration
- **THEN** UV SHALL prioritize the JLU mirror for package downloads
- **AND** improve download speeds in China

### Requirement: CI/CD Integration

The project SHALL use UV in all CI/CD workflows for consistent dependency management.

#### Scenario: GitHub Actions setup

- **WHEN** CI workflows run
- **THEN** UV SHALL be installed via official installation script
- **AND** cache the virtual environment for faster builds
- **AND** use `uv.lock` as the cache key

#### Scenario: Multi-version testing

- **WHEN** testing across Python versions
- **THEN** UV SHALL create separate virtual environments
- **AND** install appropriate dependencies for each version

### Requirement: Development Workflow

The project SHALL provide make commands that use UV for common development tasks.

#### Scenario: Run tests

- **WHEN** developer runs `make test`
- **THEN** UV SHALL execute pytest with coverage
- **AND** use the project's virtual environment

#### Scenario: Run code quality checks

- **WHEN** developer runs `make check`
- **THEN** UV SHALL execute pre-commit hooks and mypy
- **AND** report any issues found

#### Scenario: Build package

- **WHEN** developer runs `make build`
- **THEN** UV SHALL build wheel and source distributions
- **AND** place them in the `dist/` directory

### Requirement: Publishing

The project SHALL use UV to publish packages to PyPI.

#### Scenario: Publish release

- **WHEN** a release is created
- **THEN** UV SHALL build the package
- **AND** publish to PyPI using configured credentials
- **AND** verify the package was uploaded successfully

#### Scenario: Version management

- **WHEN** preparing a release
- **THEN** the version SHALL be updated in `pyproject.toml`
- **AND** the change SHALL be committed before building
