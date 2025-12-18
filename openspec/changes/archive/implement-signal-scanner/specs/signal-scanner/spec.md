# signal-scanner Specification

## ADDED Requirements

### Requirement: Django Signal Detection

The system SHALL detect Django signal patterns including built-in signals, custom signals, and signal handlers.

#### Scenario: Detect @receiver decorator with single signal

- **WHEN** scanning a Python file containing `@receiver(post_save, sender=Model)`
- **THEN** the system SHALL identify the signal handler function
- **AND** extract the signal name (`post_save`)
- **AND** extract the sender model if specified
- **AND** record file path, line number, and function name
- **AND** categorize under `django.model_signals` or appropriate subcategory

**DIFF**: New requirement for Django @receiver decorator detection

#### Scenario: Detect @receiver decorator with multiple signals

- **WHEN** scanning decorators like `@receiver([post_save, pre_delete])`
- **THEN** the system SHALL identify all signals in the list
- **AND** create separate entries for each signal-handler pair
- **AND** preserve sender information for each

**DIFF**: Support multiple signals in single decorator

#### Scenario: Detect signal.connect() method calls

- **WHEN** scanning code with `signal_name.connect(handler_func)`
- **THEN** the system SHALL identify the signal name
- **AND** extract the handler function name
- **AND** detect sender parameter if provided
- **AND** record connection location (file, line)

**DIFF**: Support .connect() method pattern

#### Scenario: Detect custom signal definitions

- **WHEN** scanning assignments like `order_paid = Signal()`
- **THEN** the system SHALL identify custom signal names
- **AND** extract signal variable name
- **AND** record providing_args if specified (Django < 4.0)
- **AND** categorize under `django.custom_signals`

**DIFF**: Detect user-defined Django signals

#### Scenario: Classify Django built-in signals by category

- **WHEN** detecting signals like `post_save`, `pre_delete`, `m2m_changed`
- **THEN** the system SHALL categorize as `django.model_signals`
- **WHEN** detecting `request_started`, `request_finished`
- **THEN** categorize as `django.request_signals`
- **WHEN** detecting `pre_migrate`, `post_migrate`
- **THEN** categorize as `django.management_signals`

**DIFF**: Hierarchical grouping of Django signals by type

### Requirement: Celery Signal Detection

The system SHALL detect Celery signal patterns including task lifecycle signals and worker signals.

#### Scenario: Detect @signal.connect decorator

- **WHEN** scanning code with `@task_prerun.connect`
- **THEN** the system SHALL identify the Celery signal name
- **AND** extract the decorated handler function
- **AND** record file path, line number, and function context
- **AND** categorize under `celery.task_signals` or `celery.worker_signals`

**DIFF**: New requirement for Celery @connect decorator pattern

#### Scenario: Detect signal.connect() method calls

- **WHEN** scanning `task_failure.connect(handler_func)`
- **THEN** the system SHALL identify the signal name
- **AND** extract handler function reference
- **AND** record connection location

**DIFF**: Support Celery .connect() method pattern

#### Scenario: Classify Celery signals by category

- **WHEN** detecting `task_prerun`, `task_postrun`, `task_failure`, `task_retry`
- **THEN** categorize as `celery.task_signals`
- **WHEN** detecting `worker_ready`, `worker_shutdown`, `worker_process_init`
- **THEN** categorize as `celery.worker_signals`
- **WHEN** detecting `beat_init`, `beat_embedded_init`
- **THEN** categorize as `celery.beat_signals`

**DIFF**: Hierarchical grouping of Celery signals by type

### Requirement: Handler Context Extraction

The system SHALL extract contextual information about signal handlers to aid understanding of their purpose and location.

#### Scenario: Extract function-level handler context

- **WHEN** a signal handler is a module-level function
- **THEN** the system SHALL record:
  - Handler function name
  - Module path
  - Line number
  - Function parameters

**DIFF**: Basic handler context for standalone functions

#### Scenario: Extract method-level handler context

- **WHEN** a signal handler is a class method
- **THEN** the system SHALL additionally record:
  - Enclosing class name
  - Method type (instance/class/static)
  - Class module path

**DIFF**: Enhanced context for method-based handlers

#### Scenario: Extract nested function context

- **WHEN** a signal handler is defined inside another function
- **THEN** the system SHALL record:
  - Handler function name
  - Enclosing function name
  - Nested depth indicator

**DIFF**: Context for nested handler functions

### Requirement: Signal Import Tracking

The system SHALL track signal imports to correctly resolve signal names and handle import aliases.

#### Scenario: Track standard Django signal imports

- **WHEN** scanning `from django.db.models.signals import post_save, pre_delete`
- **THEN** the system SHALL build import mapping:
  - `post_save` → `django.db.models.signals.post_save`
  - `pre_delete` → `django.db.models.signals.pre_delete`

**DIFF**: Qualified name resolution for Django signals

#### Scenario: Track aliased imports

- **WHEN** scanning `from celery.signals import task_prerun as prerun`
- **THEN** the system SHALL map alias to qualified name:
  - `prerun` → `celery.signals.task_prerun`
- **AND** resolve handlers using alias correctly

**DIFF**: Support import aliases

#### Scenario: Track wildcard imports

- **WHEN** scanning `from django.db.models.signals import *`
- **THEN** the system SHALL mark module as having wildcard import
- **AND** attempt best-effort signal resolution
- **AND** warn about ambiguous signal names if verbose mode enabled

**DIFF**: Partial support for wildcard imports with warnings

### Requirement: Signal Usage Aggregation

The system SHALL aggregate signal usage by signal name and provide summary statistics.

#### Scenario: Group handlers by signal name

- **WHEN** multiple handlers are registered to the same signal
- **THEN** the system SHALL group handlers under signal name:
  ```yaml
  django:
    model_signals:
      post_save:
        - handler: on_order_save
          file: app/signals.py
          line: 10
        - handler: log_save
          file: app/logging.py
          line: 25
  ```

**DIFF**: Handler aggregation by signal name

#### Scenario: Count handlers per signal

- **WHEN** outputting results
- **THEN** the system SHALL include handler count per signal
- **AND** sort signals by handler count (descending) when verbose mode

**DIFF**: Summary statistics for signal usage

#### Scenario: Detect unused custom signals

- **WHEN** a custom signal is defined but has no handlers
- **THEN** the system SHALL flag it as `unused_custom_signal`
- **AND** include in separate section of output if verbose mode

**DIFF**: Identify orphan signal definitions

### Requirement: YAML Output Format

The system SHALL export signal scan results in hierarchical YAML format grouped by framework and signal type.

#### Scenario: Export Django signals to YAML

- **WHEN** exporting Django signal results
- **THEN** the output SHALL follow structure:
  ```yaml
  django:
    model_signals:
      post_save:
        - handler: function_name
          sender: ModelName
          file: relative/path.py
          line: 42
          context:
            type: function|method|nested
            class: ClassName # if method
    request_signals:
      request_started:
        - handler: on_request
          file: middleware.py
          line: 10
    custom_signals:
      order_paid:
        - handler: process_payment
          file: services.py
          line: 55
  ```

**DIFF**: Hierarchical YAML structure for Django signals

#### Scenario: Export Celery signals to YAML

- **WHEN** exporting Celery signal results
- **THEN** the output SHALL follow structure:
  ```yaml
  celery:
    task_signals:
      task_prerun:
        - handler: task_start
          file: tasks.py
          line: 15
      task_failure:
        - handler: task_fail
          file: monitoring.py
          line: 30
    worker_signals:
      worker_ready:
        - handler: on_worker_start
          file: worker.py
          line: 8
  ```

**DIFF**: Hierarchical YAML structure for Celery signals

#### Scenario: Export mixed Django and Celery signals

- **WHEN** a codebase uses both Django and Celery signals
- **THEN** the output SHALL include both top-level sections
- **AND** keep frameworks separate for clarity

**DIFF**: Combined output format

### Requirement: File Discovery and Filtering

The system SHALL support file pattern filtering to scope signal scanning to relevant Python files.

#### Scenario: Scan with include pattern

- **WHEN** user specifies `--include "**/signals.py"`
- **THEN** the system SHALL only scan files matching the pattern
- **AND** use common file collection utilities

**DIFF**: Include pattern support

#### Scenario: Scan with exclude pattern

- **WHEN** user specifies `--exclude "**/tests/**"`
- **THEN** the system SHALL skip test files
- **AND** apply default exclusions (venv, migrations, **pycache**)

**DIFF**: Exclude pattern support

#### Scenario: Respect no-default-excludes flag

- **WHEN** user specifies `--no-default-excludes`
- **THEN** the system SHALL scan all Python files including migrations
- **AND** disable default exclusion patterns

**DIFF**: Optional default exclusion bypass

### Requirement: Signal Scanner CLI

The system SHALL provide a CLI command following standard scanner interface conventions.

#### Scenario: Basic scan command

- **WHEN** user runs `upcast scan-signals /path/to/project`
- **THEN** the system SHALL scan all Python files in path
- **AND** print summary to stdout
- **AND** display signal counts by framework

**DIFF**: New scan-signals command

#### Scenario: Export to file

- **WHEN** user runs `upcast scan-signals . -o signals.yaml`
- **THEN** the system SHALL write YAML output to signals.yaml
- **AND** print confirmation message

**DIFF**: File export option

#### Scenario: Verbose output

- **WHEN** user runs `upcast scan-signals . --verbose`
- **THEN** the system SHALL show:
  - Files being scanned
  - Handler counts per signal
  - Unused custom signals
  - Import resolution warnings

**DIFF**: Verbose mode with detailed output

#### Scenario: CLI help text with examples

- **WHEN** user runs `upcast scan-signals --help`
- **THEN** the help SHALL include:
  - Description: "Scan for Django and Celery signal usage"
  - Options: -o, -v, --include, --exclude, --no-default-excludes
  - Examples:
    ```
    upcast scan-signals .
    upcast scan-signals /app --include "**/signals/**"
    upcast scan-signals . -o signals.yaml --verbose
    ```

**DIFF**: Comprehensive help documentation

### Requirement: Module Structure

The system SHALL organize signal scanner implementation following established patterns.

#### Scenario: Module organization

- **WHEN** implementing signal scanner
- **THEN** the structure SHALL be:
  ```
  upcast/signal_scanner/
  ├── __init__.py          # exports: scan_signals, SignalChecker
  ├── checker.py           # SignalChecker class (AST visitor)
  ├── signal_parser.py     # parse_* functions for each pattern
  ├── export.py            # format_signal_output, export_to_yaml
  └── cli.py               # scan_signals command with Click
  ```

**DIFF**: Standard scanner module structure

#### Scenario: Use common utilities

- **WHEN** implementing signal scanner
- **THEN** the system SHALL reuse:
  - `upcast.common.ast_utils` for node inference and context
  - `upcast.common.file_utils` for file collection
  - `upcast.common.export` for YAML formatting patterns

**DIFF**: Leverage existing common utilities

### Requirement: Unit Test Coverage

The system SHALL include comprehensive test coverage for signal detection patterns.

#### Scenario: Test fixtures for Django signals

- **WHEN** writing tests
- **THEN** create fixture files:
  - `django_signals.py` - @receiver patterns, .connect() patterns
  - `custom_signals.py` - custom Signal() definitions
  - `mixed_django.py` - combined patterns, edge cases

**DIFF**: Django signal test fixtures

#### Scenario: Test fixtures for Celery signals

- **WHEN** writing tests
- **THEN** create fixture files:
  - `celery_signals.py` - @connect, .connect() patterns
  - `mixed_celery.py` - task and worker signals combined

**DIFF**: Celery signal test fixtures

#### Scenario: Unit tests for parsing functions

- **WHEN** testing signal_parser.py
- **THEN** create tests for each parse function:
  - `test_parse_receiver_decorator`
  - `test_parse_signal_connect_decorator`
  - `test_parse_connect_method`
  - `test_parse_custom_signal_definition`

**DIFF**: Comprehensive unit test suite

#### Scenario: Integration tests for end-to-end scanning

- **WHEN** testing checker.py
- **THEN** verify:
  - Complete file scanning
  - Handler aggregation
  - Framework grouping
  - Import resolution

**DIFF**: End-to-end integration tests

#### Scenario: CLI tests

- **WHEN** testing cli.py
- **THEN** verify:
  - Command execution
  - Option handling (--output, --verbose, --include, --exclude)
  - File output
  - Error handling

**DIFF**: CLI interface tests
