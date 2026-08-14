## ADDED Requirements

### Requirement: Django View Scanner Command

The system SHALL provide a `scan-django-views` command following the existing scanner CLI conventions.

#### Scenario: Scan a Django project for views

- **WHEN** a user runs `upcast scan-django-views <path>`
- **THEN** the system SHALL scan eligible Python files under the path for Django/DRF views
- **AND** emit the typed Django-view report as YAML by default
- **AND** SHALL NOT change the behavior or output schema of `scan-django-urls`

#### Scenario: Use standard scanner options

- **WHEN** a user invokes `scan-django-views` with output, format, verbose, include, exclude, or no-default-excludes options
- **THEN** the command SHALL apply the same option semantics as other scanner commands
- **AND** support YAML, JSON, and the project-standard Markdown output format

#### Scenario: Explain command behavior through help text

- **WHEN** a user runs `upcast scan-django-views --help`
- **THEN** help text SHALL explain that discovery is semantic rather than filename-based
- **AND** provide examples for scanning a project and narrowing files with include/exclude patterns
