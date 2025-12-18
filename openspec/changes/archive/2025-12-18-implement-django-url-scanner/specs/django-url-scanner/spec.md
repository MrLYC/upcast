# django-url-scanner Specification

## ADDED Requirements

### Requirement: URL Pattern Detection

The system SHALL detect Django URL patterns by locating `urlpatterns` variables and parsing their contents.

#### Scenario: Detect urlpatterns variable

- **WHEN** scanning a Python file
- **THEN** the system SHALL identify assignment nodes where the target is `urlpatterns`
- **AND** use the module path of the file as the primary key
- **AND** parse the assigned value as a list/tuple of URL routes

**DIFF**: New requirement for Django URL scanner

#### Scenario: Parse path() function calls

- **WHEN** analyzing urlpatterns list
- **THEN** the system SHALL identify `path()` function calls
- **AND** extract the first positional argument as the URL pattern
- **AND** extract the second positional argument as the view reference
- **AND** extract the `name` keyword argument if present

**DIFF**: Support for Django's path() function

#### Scenario: Parse re_path() function calls

- **WHEN** analyzing urlpatterns list
- **THEN** the system SHALL identify `re_path()` function calls
- **AND** extract the regex pattern from the first argument
- **AND** extract named groups from the regex pattern
- **AND** store both raw pattern and extracted parameter names

**DIFF**: Support for regex-based URL patterns

### Requirement: View Resolution

The system SHALL resolve view references to their module paths and extract documentation.

#### Scenario: Resolve function view references

- **WHEN** a URL pattern references a function view
- **THEN** the system SHALL use astroid inference to resolve the function
- **AND** extract the full module path (e.g., `blog.views.index`)
- **AND** extract the function's docstring as description
- **AND** handle aliased imports correctly

**DIFF**: Function view resolution with docstring extraction

#### Scenario: Resolve class-based views

- **WHEN** a URL pattern references a class with `.as_view()`
- **THEN** the system SHALL resolve the class reference
- **AND** extract the class module path and name
- **AND** extract the class docstring as description
- **AND** record the `.as_view()` call

**DIFF**: CBV (Class-Based View) support

#### Scenario: Handle unresolvable views

- **WHEN** a view reference cannot be resolved via inference
- **THEN** the system SHALL record the view as `<unresolved>`
- **AND** log a warning in verbose mode
- **AND** continue processing other routes

**DIFF**: Graceful degradation for unresolvable references

#### Scenario: Resolve partial-wrapped views

- **WHEN** a view is wrapped with `functools.partial`
- **THEN** the system SHALL resolve the underlying function
- **AND** note that it's a partial application
- **AND** extract the base function's module and docstring

**DIFF**: Support for functools.partial views

#### Scenario: Handle conditional views

- **WHEN** a view is selected via ternary expression
- **THEN** the system SHALL record both possible views
- **AND** mark the route as conditional
- **AND** extract descriptions from both views if possible

**DIFF**: Support for conditional route patterns

### Requirement: Include Detection

The system SHALL detect and record include() references without expanding nested patterns.

#### Scenario: Detect include() calls

- **WHEN** a URL pattern uses `include()`
- **THEN** the system SHALL identify it as an include route
- **AND** extract the included module path
- **AND** NOT expand or scan the included module
- **AND** allow recursive analysis via module path reference

**DIFF**: Include detection for recursive URL analysis

#### Scenario: Extract namespace from include

- **WHEN** an include() call has a `namespace` keyword argument
- **THEN** the system SHALL extract the namespace value
- **AND** record it with the include route

**DIFF**: Namespace support for URL includes

#### Scenario: Handle inline include lists

- **WHEN** include() is passed a list of patterns directly
- **THEN** the system SHALL mark it as inline include
- **AND** note that patterns are defined inline (not in separate module)

**DIFF**: Support for inline URL pattern lists in include()

### Requirement: Path Converter Parsing

The system SHALL parse and document path converters used in URL patterns.

#### Scenario: Extract built-in converters

- **WHEN** a path pattern contains `<type:name>` syntax
- **THEN** the system SHALL extract the converter type (int, slug, uuid, path, str)
- **AND** extract the parameter name
- **AND** store in converters dictionary

**DIFF**: Built-in converter detection

#### Scenario: Extract custom converters

- **WHEN** a path pattern uses a custom converter
- **THEN** the system SHALL record the converter name
- **AND** NOT attempt to resolve converter class
- **AND** let users define converter types separately

**DIFF**: Custom converter name recording

### Requirement: DRF Router Support

The system SHALL detect Django REST Framework router configurations and ViewSet registrations.

#### Scenario: Detect router instances

- **WHEN** scanning code containing router creation
- **THEN** the system SHALL identify `DefaultRouter()`, `SimpleRouter()` instances
- **AND** track the variable name assigned to the router

**DIFF**: DRF router detection

#### Scenario: Track ViewSet registrations

- **WHEN** code calls `router.register(prefix, ViewSetClass, basename=name)`
- **THEN** the system SHALL record the registration
- **AND** extract prefix, ViewSet class, and basename
- **AND** resolve ViewSet module path
- **AND** NOT expand router-generated URL patterns

**DIFF**: ViewSet registration tracking

#### Scenario: Record router.urls reference

- **WHEN** urlpatterns includes `router.urls`
- **THEN** the system SHALL mark it as router-generated routes
- **AND** reference back to the router registrations

**DIFF**: Router URL inclusion tracking

### Requirement: ViewSet Action Mapping

The system SHALL parse ViewSet action mappings in .as_view() calls.

#### Scenario: Parse action mapping dictionary

- **WHEN** a ViewSet uses `.as_view({"get": "list", "post": "create"})`
- **THEN** the system SHALL extract the HTTP method to action mapping
- **AND** record each mapping (get→list, post→create)
- **AND** associate with the ViewSet class

**DIFF**: ViewSet action mapping extraction

### Requirement: Output Format

The system SHALL export URL patterns in structured YAML format grouped by module.

#### Scenario: Group by urlpatterns module

- **WHEN** exporting results
- **THEN** the system SHALL use the module path containing urlpatterns as the key
- **AND** nest all routes under that module
- **AND** support multiple modules with their own urlpatterns

**DIFF**: Module-based grouping structure

#### Scenario: Format route entries

- **WHEN** formatting each route
- **THEN** the output SHALL include:
  - `pattern`: URL pattern string
  - `view_module`: Full module path of view (if resolved)
  - `view_name`: Function or class name
  - `name`: Django route name (if specified)
  - `description`: Extracted docstring (if available)
  - `converters`: Dict of parameter converters (if any)

**DIFF**: Comprehensive route metadata structure

#### Scenario: Format include entries

- **WHEN** formatting an include route
- **THEN** the output SHALL include:
  - `pattern`: URL prefix pattern
  - `include_module`: Included module path
  - `namespace`: Namespace (if specified)
- **AND** omit view_module and view_name

**DIFF**: Special format for include routes

#### Scenario: Format router entries

- **WHEN** formatting router registrations
- **THEN** the output SHALL include:
  - `router_type`: Router class name
  - `registrations`: List of ViewSet registrations with prefix and basename

**DIFF**: Router registration structure

### Requirement: CLI Integration

The system SHALL provide a command-line interface following project conventions.

#### Scenario: Provide scan-django-urls command

- **WHEN** user runs `upcast scan-django-urls <path>`
- **THEN** the system SHALL scan the path for Django URL patterns
- **AND** output results to stdout in YAML format by default

**DIFF**: New CLI command

#### Scenario: Support standard filtering options

- **WHEN** invoking scan-django-urls
- **THEN** the system SHALL support:
  - `-o, --output FILE` - Write to file
  - `-v, --verbose` - Enable detailed logging
  - `--include PATTERN` - Include file patterns
  - `--exclude PATTERN` - Exclude file patterns
  - `--no-default-excludes` - Disable default exclusions

**DIFF**: Consistent with other scanner commands

### Requirement: Error Handling

The system SHALL handle errors gracefully and continue scanning when possible.

#### Scenario: Continue on parse errors

- **WHEN** parsing a URL pattern fails
- **THEN** the system SHALL log the error in verbose mode
- **AND** continue processing other patterns
- **AND** include a summary of errors in output

**DIFF**: Resilient scanning behavior

#### Scenario: Handle import errors

- **WHEN** a view module cannot be imported
- **THEN** the system SHALL mark the view as unresolved
- **AND** include the import error in verbose output
- **AND** continue scanning

**DIFF**: Graceful handling of missing imports
