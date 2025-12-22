# CLI Consolidation Specification

## REMOVED Requirements

### Requirement: Duplicate CLI Commands

Duplicate CLI commands with `-new` suffix SHALL be removed after migration.

#### Scenario: Remove scan-django-models duplicate

**GIVEN** both `scan-django-models` and `scan-django-models-new` commands exist
**WHEN** the migration is complete
**THEN** only `scan-django-models` SHALL remain
**AND** it SHALL use the new `DjangoModelScanner` implementation
**AND** the old implementation SHALL be removed

#### Scenario: Remove scan-django-urls duplicate

**GIVEN** both `scan-django-urls` and `scan-django-urls-new` commands exist
**WHEN** the migration is complete
**THEN** only `scan-django-urls` SHALL remain
**AND** it SHALL use the new `DjangoUrlScanner` implementation

#### Scenario: Remove scan-django-settings duplicate

**GIVEN** both `scan-django-settings` and `scan-django-settings-new` commands exist
**WHEN** the migration is complete
**THEN** only `scan-django-settings` SHALL remain
**AND** it SHALL use the new `DjangoSettingsScanner` implementation

#### Scenario: Remove scan-unit-tests duplicate

**GIVEN** two `scan-unit-tests` command definitions exist in main.py
**WHEN** the migration is complete
**THEN** only one `scan-unit-tests` SHALL remain
**AND** it SHALL use the new `UnitTestScanner` implementation

### Requirement: Old Module Imports

Imports from old scanner modules SHALL be removed from main.py.

#### Scenario: Remove django_model_scanner imports

**GIVEN** the file `upcast/main.py`
**WHEN** the migration is complete
**THEN** no import from `upcast.django_model_scanner` SHALL exist
**AND** `DjangoModelScanner` SHALL be imported from `upcast.scanners`

#### Scenario: Remove django_url_scanner imports

**GIVEN** the file `upcast/main.py`
**WHEN** the migration is complete
**THEN** no import from `upcast.django_url_scanner` SHALL exist
**AND** `DjangoUrlScanner` SHALL be imported from `upcast.scanners`

#### Scenario: Remove django_settings_scanner imports

**GIVEN** the file `upcast/main.py`
**WHEN** the migration is complete
**THEN** no import from `upcast.django_settings_scanner` SHALL exist
**AND** `DjangoSettingsScanner` SHALL be imported from `upcast.scanners`

#### Scenario: Remove unit_test_scanner imports

**GIVEN** the file `upcast/main.py`
**WHEN** the migration is complete
**THEN** no import from `upcast.unit_test_scanner` SHALL exist
**AND** `UnitTestScanner` SHALL be imported from `upcast.scanners`

## ADDED Requirements

### Requirement: Unified Scanner Import

All scanners SHALL be imported from the unified `upcast.scanners` module.

#### Scenario: Single import block for all scanners

**GIVEN** the file `upcast/main.py`
**WHEN** the CLI commands are defined
**THEN** all scanner classes SHALL be imported from `upcast.scanners` in a single import block
**AND** the import SHALL include all 12 scanners

**Example**:

```python
from upcast.scanners import (
    BlockingOperationsScanner,
    ComplexityScanner,
    ConcurrencyScanner,
    DjangoModelScanner,
    DjangoSettingsScanner,
    DjangoUrlScanner,
    EnvVarScanner,
    ExceptionHandlerScanner,
    HttpRequestsScanner,
    MetricsScanner,
    SignalScanner,
    UnitTestScanner,
)
```

### Requirement: Consistent CLI Command Pattern

All CLI commands SHALL follow the same implementation pattern using new scanners.

#### Scenario: CLI command uses run_scanner_cli

**GIVEN** any scanner command in main.py
**WHEN** the command is executed
**THEN** it SHALL use `run_scanner_cli` helper function
**AND** it SHALL instantiate the scanner with appropriate parameters
**AND** it SHALL handle errors using `handle_scan_error`

**Example**:

```python
@main.command(name="scan-django-models")
@click.option("-o", "--output", type=click.Path(), help="Output file path")
@click.option("--format", type=click.Choice(["yaml", "json"]), default="yaml")
@click.option("-v", "--verbose", is_flag=True)
@click.argument("path", type=click.Path(exists=True), default=".")
def scan_django_models_cmd(output, format, verbose, path, **kwargs):
    """Scan Django model files."""
    try:
        scanner = DjangoModelScanner(verbose=verbose, ...)
        run_scanner_cli(scanner, path, output, format, verbose=verbose)
    except Exception as e:
        from upcast.common.cli import handle_scan_error
        handle_scan_error(e, verbose=verbose)
```

#### Scenario: No duplicate command names

**GIVEN** all CLI commands in main.py
**WHEN** the commands are registered
**THEN** each command name SHALL be unique
**AND** no command SHALL have a `-new` suffix
**AND** no two commands SHALL perform the same function

### Requirement: Backward Compatible CLI Interface

CLI commands SHALL maintain backward compatibility for users.

#### Scenario: Command names unchanged

**GIVEN** a user script using `upcast scan-django-models`
**WHEN** the migration is complete
**THEN** the command SHALL still work with the same name
**AND** the output format SHALL remain compatible
**AND** the command options SHALL remain the same or be backward compatible

#### Scenario: Output format compatibility

**GIVEN** a scanner command
**WHEN** executed with `--format yaml`
**THEN** the output SHALL be valid YAML
**AND** the structure SHALL be compatible with previous versions
**AND** the field names SHALL match Pydantic model definitions

**Example output structure**:

```yaml
summary:
  total_count: 10
  files_scanned: 5
  scan_duration_ms: 150
results:
  # Scanner-specific results using 'results' field
```

## MODIFIED Requirements

None - this change removes old code and consolidates CLI, no existing specs modified.
