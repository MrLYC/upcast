## ADDED Requirements

### Requirement: Unit Test Detection

The system SHALL detect Python unit tests using pytest and unittest patterns through AST analysis.

#### Scenario: Detect pytest test functions

- **WHEN** scanning a Python file
- **THEN** the system SHALL identify functions starting with `test_`
- **AND** located in files matching `test*.py` or `*_test.py`
- **AND** extract the function name, location (file:line), and body

#### Scenario: Detect unittest test methods

- **WHEN** scanning a Python file containing unittest.TestCase subclasses
- **THEN** the system SHALL identify methods starting with `test_`
- **AND** extract the test class name and method name
- **AND** record the location (file:line)

#### Scenario: Skip non-test functions

- **WHEN** a function does not match test patterns
- **THEN** the system SHALL exclude it from output
- **AND** continue scanning other functions

### Requirement: Test Body Analysis

The system SHALL analyze test function bodies to extract assertions, calculate checksums, and identify dependencies.

#### Scenario: Count assert statements

- **WHEN** parsing a test function body
- **THEN** the system SHALL count all `assert` statements (pytest style)
- **AND** count all `self.assert*` method calls (unittest style)
- **AND** return the total assertion count

#### Scenario: Calculate function body MD5

- **WHEN** parsing a test function
- **THEN** the system SHALL normalize the function body (strip comments, normalize whitespace)
- **AND** calculate MD5 hash of the normalized body
- **AND** return the hash as a hex string
- **EXAMPLE**: `"9b8c0f0c7c1f3e4f2a4a9d3d8a8c2b1f"`

#### Scenario: Extract imports and references

- **WHEN** analyzing test function body
- **THEN** the system SHALL track all imported modules in the file
- **AND** identify all Name and Attribute nodes referencing imported symbols
- **AND** resolve full module paths for referenced objects

### Requirement: Test Target Resolution

The system SHALL identify which modules a test targets by matching referenced symbols against a root_modules list.

#### Scenario: Match against root modules

- **WHEN** given `root_modules = ["app", "mylib"]`
- **AND** a test imports and uses `app.math_utils.add`
- **THEN** the system SHALL mark `app.math_utils` as a test target
- **AND** record the imported symbol `add`

#### Scenario: Collect multiple targets

- **WHEN** a test uses symbols from multiple modules in root_modules
- **THEN** the system SHALL list all matching modules
- **AND** group symbols by module
- **EXAMPLE**:
  ```yaml
  targets:
    - module: app.math_utils
      symbols: [add, subtract]
    - module: app.validators
      symbols: [validate_email]
  ```

#### Scenario: Handle no matching targets

- **WHEN** a test does not use any symbols from root_modules
- **THEN** the system SHALL set `targets: []`
- **AND** still include the test in output

#### Scenario: Handle wildcard imports

- **WHEN** a test uses `from app.utils import *`
- **AND** references a symbol that could come from that module
- **THEN** the system SHALL include the module in targets
- **AND** mark symbols as `["*"]` if specific imports cannot be determined

### Requirement: Output Format

The system SHALL export test analysis results in structured YAML or JSON format grouped by file.

#### Scenario: YAML output structure

- **WHEN** exporting to YAML
- **THEN** the output SHALL be a mapping of file paths to test lists
- **AND** each test SHALL include: name, body_md5, assert_count, targets
- **EXAMPLE**:
  ```yaml
  tests/test_math_utils.py:
    - name: test_add_and_even
      body_md5: "9b8c0f0c7c1f3e4f2a4a9d3d8a8c2b1f"
      assert_count: 3
      targets:
        - module: app.math_utils
          symbols:
            - add
            - is_even
  ```

#### Scenario: JSON output format

- **WHEN** user specifies `--format json`
- **THEN** the system SHALL export the same structure in JSON
- **AND** use 2-space indentation
- **AND** ensure UTF-8 encoding

#### Scenario: Sort output consistently

- **WHEN** exporting test results
- **THEN** the system SHALL sort files alphabetically
- **AND** sort tests within each file by line number
- **AND** sort target modules alphabetically
- **AND** sort symbols within each module alphabetically

### Requirement: CLI Command Interface

The system SHALL provide a `scan-unit-tests` command accessible via `upcast` CLI.

#### Scenario: Basic usage

- **WHEN** user runs `upcast scan-unit-tests <path> --root-modules app`
- **THEN** the system SHALL scan the specified path for test files
- **AND** analyze tests with `app` as root module
- **AND** output results to stdout in YAML format

#### Scenario: Multiple root modules

- **WHEN** user runs `upcast scan-unit-tests <path> --root-modules app,mylib,utils`
- **THEN** the system SHALL accept comma-separated root module list
- **AND** match test targets against all specified modules

#### Scenario: Output to file

- **WHEN** user runs `upcast scan-unit-tests <path> -o output.yaml --root-modules app`
- **THEN** the system SHALL write results to the specified file
- **AND** create parent directories if needed

#### Scenario: JSON output format

- **WHEN** user runs `upcast scan-unit-tests <path> --format json --root-modules app`
- **THEN** the system SHALL output in JSON format

#### Scenario: File filtering with include

- **WHEN** user runs `upcast scan-unit-tests <path> --include "tests/*.py" --root-modules app`
- **THEN** the system SHALL only scan files matching the glob pattern
- **AND** use `common.file_utils.collect_python_files()` with include option

#### Scenario: File filtering with exclude

- **WHEN** user runs `upcast scan-unit-tests <path> --exclude "*/integration/*" --root-modules app`
- **THEN** the system SHALL skip files matching the exclude pattern

#### Scenario: Verbose mode

- **WHEN** user runs `upcast scan-unit-tests <path> -v --root-modules app`
- **THEN** the system SHALL enable debug logging
- **AND** show file processing details and target resolution steps

#### Scenario: Missing root-modules argument

- **WHEN** user runs `upcast scan-unit-tests <path>` without `--root-modules`
- **THEN** the system SHALL show error message
- **AND** explain that `--root-modules` is required
- **AND** exit with non-zero status

### Requirement: Common Utilities Integration

The system SHALL use shared common utilities for consistency with other scanners.

#### Scenario: Use common file discovery

- **WHEN** collecting Python files to scan
- **THEN** the system SHALL use `common.file_utils.collect_python_files()`
- **AND** respect include/exclude patterns
- **AND** apply default exclude patterns

#### Scenario: Use common AST inference

- **WHEN** inferring values or types from AST nodes
- **THEN** the system SHALL use `common.ast_utils.infer_value_with_fallback()`
- **AND** use `common.ast_utils.get_qualified_name()` for module resolution

#### Scenario: Use common export functions

- **WHEN** exporting to YAML or JSON
- **THEN** the system SHALL use `common.export.export_to_yaml()` or equivalent
- **AND** benefit from consistent sorting and formatting

### Requirement: Test Case Location Tracking

The system SHALL track the precise location of each test case for IDE navigation and reporting.

#### Scenario: Record line number

- **WHEN** detecting a test function
- **THEN** the system SHALL record the line number where the function is defined
- **AND** include it in output as `location: "file.py:line"`

#### Scenario: Handle nested test classes

- **WHEN** a unittest TestCase contains multiple test methods
- **THEN** the system SHALL record each method's line number separately
- **AND** include class name in test identification

### Requirement: Assertion Detection Coverage

The system SHALL detect assertions from multiple testing frameworks and styles.

#### Scenario: Detect pytest plain assert

- **WHEN** test contains `assert x == y`
- **THEN** the system SHALL count it as one assertion

#### Scenario: Detect unittest assertions

- **WHEN** test contains `self.assertEqual(x, y)`
- **THEN** the system SHALL count it as one assertion
- **AND** recognize all unittest assert methods (assertTrue, assertFalse, assertIn, etc.)

#### Scenario: Detect pytest raises

- **WHEN** test contains `with pytest.raises(Exception):`
- **THEN** the system SHALL count it as one assertion

#### Scenario: Handle multiple assertions

- **WHEN** test contains multiple assert statements
- **THEN** the system SHALL count each one separately
- **EXAMPLE**: Test with 3 asserts → `assert_count: 3`

### Requirement: Error Handling

The system SHALL handle parsing errors gracefully and continue scanning other files.

#### Scenario: Handle syntax errors

- **WHEN** a test file contains syntax errors
- **THEN** the system SHALL log a warning with file path and error
- **AND** skip that file
- **AND** continue scanning remaining files

#### Scenario: Handle import resolution failures

- **WHEN** unable to resolve an imported module
- **THEN** the system SHALL use `` `module_name` `` (backtick wrapped) as fallback
- **AND** still include the test in output
- **AND** log warning in verbose mode

#### Scenario: Handle invalid paths

- **WHEN** user provides nonexistent path
- **THEN** the system SHALL show clear error message
- **AND** exit with status code 1

### Requirement: Body Normalization for MD5

The system SHALL normalize test function bodies before hashing to ignore cosmetic changes.

#### Scenario: Strip comments

- **WHEN** calculating MD5
- **THEN** the system SHALL remove all comment lines
- **AND** remove inline comments

#### Scenario: Normalize whitespace

- **WHEN** calculating MD5
- **THEN** the system SHALL normalize indentation to consistent spacing
- **AND** strip trailing whitespace
- **AND** ensure consistent line endings (LF)

#### Scenario: Preserve semantic content

- **WHEN** normalizing function body
- **THEN** the system SHALL preserve all code statements
- **AND** preserve string literals exactly
- **AND** preserve operator spacing

### Requirement: Module Path Resolution

The system SHALL resolve relative imports to absolute module paths for accurate target matching.

#### Scenario: Resolve relative imports

- **WHEN** test file contains `from . import utils`
- **THEN** the system SHALL resolve `.` to the package path
- **AND** convert to absolute module path
- **EXAMPLE**: In `tests/test_math.py` → `tests.utils`

#### Scenario: Use package root detection

- **WHEN** resolving module paths
- **THEN** the system SHALL use `common.file_utils.find_package_root()`
- **AND** build fully qualified module names
