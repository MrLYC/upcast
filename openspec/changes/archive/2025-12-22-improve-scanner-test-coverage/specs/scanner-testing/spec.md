# Scanner Testing Specification

## ADDED Requirements

### Requirement: Comprehensive Test Coverage

Each scanner in `upcast/scanners/` SHALL have comprehensive test coverage to ensure correctness and prevent regressions.

#### Scenario: Test suite structure

**GIVEN** a scanner module (e.g., `upcast/scanners/env_vars.py`)
**WHEN** the corresponding test file is created (e.g., `tests/test_scanners/test_env_vars.py`)
**THEN** the test file SHALL contain:

- Model validation tests for all Pydantic models
- Scanner integration tests with realistic fixtures
- Edge case tests (empty input, malformed code, errors)
- Output structure verification tests

#### Scenario: Model validation tests

**GIVEN** a Pydantic model used by a scanner (e.g., `EnvVarInfo`)
**WHEN** the model validation tests are executed
**THEN** the tests SHALL verify:

- Valid model creation with all required fields
- Optional field handling
- Field constraints (e.g., `line >= 1`)
- Validation errors for invalid data
- Model serialization/deserialization

**Example**:

```python
def test_valid_env_var_info():
    info = EnvVarInfo(
        name="DATABASE_URL",
        file="app/config.py",
        line=10,
        pattern="os.getenv"
    )
    assert info.name == "DATABASE_URL"
    assert info.line == 10

def test_env_var_info_validates_line_number():
    with pytest.raises(ValidationError):
        EnvVarInfo(name="VAR", file="test.py", line=0)
```

#### Scenario: Scanner integration tests

**GIVEN** a scanner class (e.g., `EnvVarScanner`)
**WHEN** integration tests are executed with test fixtures
**THEN** the tests SHALL:

- Create temporary test files with known patterns
- Execute scanner.scan() on the test files
- Verify the output structure matches the Pydantic model
- Verify all expected patterns are detected
- Verify counts and summaries are correct

**Example**:

```python
def test_scanner_detects_patterns(tmp_path):
    # Create test file
    test_file = tmp_path / "test.py"
    test_file.write_text("""
import os
db_url = os.getenv('DATABASE_URL')
api_key = os.environ.get('API_KEY')
    """)

    # Scan
    scanner = EnvVarScanner()
    result = scanner.scan(tmp_path)

    # Verify
    assert isinstance(result, EnvVarOutput)
    assert len(result.results) == 2
    assert "DATABASE_URL" in result.results
    assert "API_KEY" in result.results
```

#### Scenario: Edge case handling

**GIVEN** a scanner
**WHEN** edge case tests are executed
**THEN** the tests SHALL verify:

- Empty directory returns valid output with zero results
- Files with no matching patterns return empty results
- Malformed code does not crash the scanner
- Error handling for unparseable files

### Requirement: Coverage Target

The test suite SHALL achieve at least 80% code coverage for all scanner modules.

#### Scenario: Verify coverage threshold

**GIVEN** all scanner test files are implemented
**WHEN** coverage is measured with `pytest --cov=upcast/scanners`
**THEN** the overall coverage SHALL be >= 80%
**AND** each individual scanner file SHALL have >= 70% coverage

#### Scenario: Coverage report

**GIVEN** tests are executed with coverage
**WHEN** the coverage report is generated
**THEN** the report SHALL show:

- Overall coverage percentage
- Per-file coverage breakdown
- Lines not covered (for manual review)
- Branch coverage statistics

### Requirement: Test Consistency

All scanner tests SHALL follow the same structure and patterns for maintainability.

#### Scenario: Test file structure

**GIVEN** any scanner test file in `tests/test_scanners/`
**WHEN** the file is reviewed
**THEN** it SHALL follow this structure:

1. Imports section
2. Model validation test class(es)
3. Scanner integration test class
4. Helper fixtures (if needed)

**Example structure**:

```python
"""Tests for XxxScanner."""
import pytest
from upcast.scanners.xxx import XxxScanner, XxxInfo, XxxOutput

class TestXxxInfoModel:
    """Tests for XxxInfo Pydantic model."""

    def test_valid_xxx_info(self):
        ...

    def test_xxx_info_validation(self):
        ...

class TestXxxScannerIntegration:
    """Integration tests for XxxScanner."""

    def test_scanner_detects_patterns(self, tmp_path):
        ...

    def test_scanner_handles_empty_input(self, tmp_path):
        ...
```

#### Scenario: Test naming conventions

**GIVEN** a test method
**WHEN** the test is named
**THEN** the name SHALL:

- Start with `test_`
- Describe what is being tested
- Use snake_case
- Be descriptive and clear

#### Scenario: Test isolation

**GIVEN** any test method
**WHEN** the test is executed
**THEN** the test SHALL:

- Not depend on other tests
- Use fixtures or setup methods for dependencies
- Clean up temporary resources
- Not modify global state
