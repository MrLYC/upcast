# Model Cleanup Specification

## REMOVED Requirements

### Requirement: Field Aliases for Backward Compatibility

Field aliases in Pydantic models SHALL be removed as they are no longer needed after migration completion.

#### Scenario: Remove alias from blocking operations model

**GIVEN** the file `upcast/models/blocking_operations.py`
**WHEN** the model definition is updated
**THEN** the line `results: dict[str, list[BlockingOperation]] = Field(..., alias="operations", ...)`
**SHALL** be changed to `results: dict[str, list[BlockingOperation]] = Field(..., description=...)`
**AND** the `alias="operations"` parameter SHALL be removed

#### Scenario: Remove alias from complexity model

**GIVEN** the file `upcast/models/complexity.py`
**WHEN** the model definition is updated
**THEN** the `alias="modules"` parameter SHALL be removed from the `results` field

#### Scenario: Remove alias from concurrency model

**GIVEN** the file `upcast/models/concurrency.py`
**WHEN** the model definition is updated
**THEN** the `alias="concurrency_patterns"` parameter SHALL be removed from the `results` field

#### Scenario: Remove alias from django models model

**GIVEN** the file `upcast/models/django_models.py`
**WHEN** the model definition is updated
**THEN** the `alias="models"` parameter SHALL be removed from the `results` field

#### Scenario: Remove aliases from django settings model

**GIVEN** the file `upcast/models/django_settings.py`
**WHEN** the model definitions are updated
**THEN** the `alias="settings"` parameter SHALL be removed from `DjangoSettingsUsageOutput.results`
**AND** the `alias="definitions"` parameter SHALL be removed from `DjangoSettingsDefinitionOutput.results`

#### Scenario: Remove alias from django urls model

**GIVEN** the file `upcast/models/django_urls.py`
**WHEN** the model definition is updated
**THEN** the `alias="url_modules"` parameter SHALL be removed from the `results` field

#### Scenario: Remove alias from env vars model

**GIVEN** the file `upcast/models/env_vars.py`
**WHEN** the model definition is updated
**THEN** the `alias="env_vars"` parameter SHALL be removed from the `results` field

#### Scenario: Remove alias from exceptions model

**GIVEN** the file `upcast/models/exceptions.py`
**WHEN** the model definition is updated
**THEN** the `alias="exception_handlers"` parameter SHALL be removed from the `results` field

#### Scenario: Remove alias from http requests model

**GIVEN** the file `upcast/models/http_requests.py`
**WHEN** the model definition is updated
**THEN** the `alias="requests"` parameter SHALL be removed from the `results` field

#### Scenario: Remove alias from metrics model

**GIVEN** the file `upcast/models/metrics.py`
**WHEN** the model definition is updated
**THEN** the `alias="metrics"` parameter SHALL be removed from the `results` field

#### Scenario: Remove alias from unit tests model

**GIVEN** the file `upcast/models/unit_tests.py`
**WHEN** the model definition is updated
**THEN** the `alias="tests"` parameter SHALL be removed from the `results` field

## ADDED Requirements

### Requirement: Consistent Field Naming

All scanner output models SHALL use the field name `results` without aliases.

#### Scenario: Model field naming convention

**GIVEN** any scanner output model (e.g., `EnvVarOutput`, `DjangoModelOutput`)
**WHEN** the model is inspected
**THEN** the main data field SHALL be named `results`
**AND** SHALL NOT have any `alias` parameter
**AND** SHALL have a descriptive `description` parameter

**Example**:

```python
class EnvVarOutput(ScannerOutput[dict[str, EnvVarInfo]]):
    """Output from environment variable scanner."""

    summary: EnvVarSummary
    results: dict[str, EnvVarInfo] = Field(
        ...,
        description="Environment variables keyed by name"
    )
```

#### Scenario: Scanner code uses results field

**GIVEN** a scanner implementation (e.g., `EnvVarScanner`)
**WHEN** the scanner creates output
**THEN** it SHALL use the field name `results`
**AND** SHALL NOT reference any old alias names

**Example**:

```python
def scan(self, path: Path) -> EnvVarOutput:
    env_vars = self._scan_files(...)
    return EnvVarOutput(
        summary=...,
        results=env_vars  # Use 'results', not alias
    )
```

#### Scenario: Test code uses results field

**GIVEN** any test accessing scanner output
**WHEN** the test accesses the data
**THEN** it SHALL use `output.results`
**AND** SHALL NOT use any old alias names

**Example**:

```python
def test_scanner_output():
    result = scanner.scan(path)
    assert len(result.results) == expected_count  # Use 'results'
    assert "VAR_NAME" in result.results            # Use 'results'
```

### Requirement: Migration Validation

After removing aliases, all existing functionality SHALL continue to work.

#### Scenario: All tests pass after alias removal

**GIVEN** all field aliases have been removed
**WHEN** the complete test suite is executed
**THEN** all tests SHALL pass without modification
**AND** no test SHALL reference old alias names

#### Scenario: CLI commands work after alias removal

**GIVEN** all field aliases have been removed
**WHEN** any `upcast scan-*` command is executed
**THEN** the output SHALL be in correct format
**AND** the `results` field SHALL contain expected data
**AND** no errors SHALL occur

#### Scenario: Code quality checks pass

**GIVEN** all field aliases have been removed
**WHEN** ruff and pre-commit checks are executed
**THEN** all checks SHALL pass
**AND** no new linting errors SHALL appear
