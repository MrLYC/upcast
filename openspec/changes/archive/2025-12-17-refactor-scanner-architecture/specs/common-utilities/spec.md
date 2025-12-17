# common-utilities Specification

## ADDED Requirements

### Requirement: Unified File Discovery

The system SHALL provide a unified file discovery utility that all scanners can use to collect Python files with consistent filtering behavior.

#### Scenario: Collect Python files from directory

- **WHEN** given a directory path
- **THEN** the system SHALL recursively find all `*.py` files
- **AND** exclude default patterns (venv/, **pycache**/, build/, dist/, .tox/, node_modules/)
- **AND** return absolute paths sorted alphabetically

#### Scenario: Collect Python files from single file

- **WHEN** given a single `.py` file path
- **THEN** the system SHALL return that file in a list
- **AND** validate the file exists and is readable

#### Scenario: Apply include patterns

- **WHEN** user provides `--include` patterns
- **THEN** the system SHALL only include files matching at least one include pattern
- **AND** use glob pattern matching (not regex)
- **AND** match patterns relative to scan root

#### Scenario: Apply exclude patterns

- **WHEN** user provides `--exclude` patterns
- **THEN** the system SHALL exclude files matching any exclude pattern
- **AND** apply default excludes unless disabled with `--no-default-excludes`
- **AND** exclude patterns take precedence over include patterns

### Requirement: Python Package Root Detection

The system SHALL detect Python package root by locating `__init__.py` files to enable correct module path resolution.

#### Scenario: Find package root by walking up

- **WHEN** given a path inside a Python package
- **THEN** the system SHALL walk up parent directories
- **AND** stop at the first directory without `__init__.py`
- **AND** return the last directory that HAD `__init__.py` as package root

#### Scenario: Fallback when no package found

- **WHEN** no `__init__.py` files found in parent chain
- **THEN** the system SHALL return the original path as fallback
- **AND** log a warning in verbose mode

#### Scenario: Handle nested packages

- **WHEN** multiple nested packages exist
- **THEN** the system SHALL return the outermost package root
- **EXAMPLE**: `/project/src/myapp/__init__.py` → return `/project/src/myapp/`

### Requirement: Unified AST Inference with Fallback

The system SHALL provide unified astroid inference functions with explicit fallback markers for failed inferences.

#### Scenario: Successful value inference

- **WHEN** astroid successfully infers a literal value
- **THEN** the system SHALL return (value, True)
- **AND** value SHALL be the Python literal (str, int, bool, float, None, list, dict)

#### Scenario: Failed value inference with backtick marker

- **WHEN** astroid inference fails or returns Uninferable
- **THEN** the system SHALL return (`` `expression` ``, False)
- **AND** wrap the original AST expression in backticks
- **AND** preserve the expression string for debugging

#### Scenario: Successful type inference

- **WHEN** astroid successfully infers a type
- **THEN** the system SHALL return the fully qualified type name
- **EXAMPLE**: `django.db.models.CharField` not just `CharField`

#### Scenario: Failed type inference with unknown marker

- **WHEN** type inference fails
- **THEN** the system SHALL return `"unknown"` as type
- **AND** log failure in verbose mode

### Requirement: Unified Export with Sorted Output

The system SHALL provide unified YAML/JSON export functions with consistent field sorting.

#### Scenario: Export to YAML with sorted keys

- **WHEN** exporting data to YAML
- **THEN** the system SHALL sort top-level dictionary keys alphabetically
- **AND** sort nested dictionaries recursively
- **AND** sort list elements where applicable (e.g., usages by file/line)
- **AND** use UTF-8 encoding with 2-space indentation

#### Scenario: Export to JSON with sorted keys

- **WHEN** exporting data to JSON
- **THEN** the system SHALL sort keys alphabetically at all levels
- **AND** use 2-space indentation for readability
- **AND** ensure UTF-8 encoding

#### Scenario: Consistent collection sorting

- **WHEN** exporting collections like usages or locations
- **THEN** the system SHALL sort by primary key (file path)
- **AND** then by secondary key (line number)
- **AND** then by tertiary key (column number) if applicable

### Requirement: Qualified Name Resolution

The system SHALL resolve fully qualified names for types and classes using astroid's semantic analysis.

#### Scenario: Get qualified name from astroid node

- **WHEN** given an astroid ClassDef or FunctionDef node
- **THEN** the system SHALL return the fully qualified name
- **EXAMPLE**: Node for `CharField` → `"django.db.models.fields.CharField"`

#### Scenario: Handle inference failures for qualified names

- **WHEN** qualified name cannot be determined
- **THEN** the system SHALL return `` `node.as_string()` `` wrapped in backticks
- **AND** avoid raising exceptions

### Requirement: Path Validation

The system SHALL validate input paths before scanning and provide clear error messages.

#### Scenario: Validate existing path

- **WHEN** given a path that exists
- **THEN** the system SHALL return a Path object
- **AND** verify it's either a file or directory

#### Scenario: Reject nonexistent path

- **WHEN** given a path that doesn't exist
- **THEN** the system SHALL raise FileNotFoundError
- **AND** include the invalid path in error message

#### Scenario: Reject invalid path type

- **WHEN** given a path that is neither file nor directory (e.g., socket, device)
- **THEN** the system SHALL raise ValueError
- **AND** explain that only files and directories are supported
