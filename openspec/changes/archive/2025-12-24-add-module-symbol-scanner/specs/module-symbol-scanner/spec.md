# Module Symbol Scanner

## ADDED Requirements

### Requirement: Extract Module Import Information

The scanner MUST extract all import statements from Python modules, including:

- Complete module imports (`import xxx`)
- Selective symbol imports (`from xxx import yyy`)
- Star imports (`from xxx import *`)

For each import, the scanner MUST track:

- The module path being imported
- The block context where the import occurs (module, if, try, except, function, class)
- Attributes accessed on imported symbols

#### Scenario: Extract standard imports

**Given** a Python file with various import statements:

```python
import os
import sys
from pathlib import Path
from typing import Optional, List
from utils import helper
```

**When** the module symbol scanner processes the file

**Then** the output contains:

- `imported_modules`: {"os": {...}, "sys": {...}}
- `imported_symbols`: {"Path": {module_path: "pathlib", ...}, "Optional": {...}, "List": {...}, "helper": {...}}

#### Scenario: Extract conditional imports

**Given** a Python file with conditional imports:

```python
if sys.platform == "win32":
    import winreg
else:
    import pwd
```

**When** the module symbol scanner processes the file

**Then** the output tracks block context:

- `imported_modules.winreg.blocks` includes "if"
- `imported_modules.pwd.blocks` includes "if"

#### Scenario: Extract star imports

**Given** a Python file with star imports:

```python
from typing import *
```

**When** the module symbol scanner processes the file

**Then** the output contains:

- `star_imported`: [{"module_path": "typing", "blocks": ["module"]}]

#### Scenario: Extract dynamic imports via importlib

**Given** a Python file with dynamic imports using importlib:

```python
import importlib

# Dynamic module import
module = importlib.import_module("some.module")

# Dynamic symbol import
mod = importlib.import_module("package.module")
symbol = getattr(mod, "SomeClass")
```

**When** the module symbol scanner processes the file

**Then** the scanner:

- Detects `importlib` as an imported module
- MAY attempt to extract the module path from string literals in `import_module()` calls on a best-effort basis
- Records these as dynamic imports with limited static analysis support
- Notes: Full dynamic import analysis is out of scope; the scanner provides basic detection only

---

### Requirement: Track Attribute Access Patterns

The scanner MUST analyze how imported symbols are used by tracking attribute accesses.

#### Scenario: Track simple attribute access

**Given** a Python file:

```python
import os
path = os.path.join("a", "b")
```

**When** the module symbol scanner processes the file

**Then** the output contains:

- `imported_modules.os.attributes` includes "path"

#### Scenario: Track symbol attribute access

**Given** a Python file:

```python
from pathlib import Path
p = Path.home()
```

**When** the module symbol scanner processes the file

**Then** the output contains:

- `imported_symbols.Path.attributes` includes "home"

---

### Requirement: Extract Module-Level Variables

The scanner MUST extract module-level variable definitions, excluding private variables (starting with `_`) by default.

For each variable, the scanner MUST extract:

- Module path
- Assignment statement source code
- Value representation (for simple types)
- Block context
- Attributes accessed on the variable

#### Scenario: Extract public variables

**Given** a Python file:

```python
DEBUG = True
MAX_RETRIES = 3
API_URL = "https://api.example.com"
_private_var = "internal"
```

**When** the module symbol scanner processes the file

**Then** the output contains:

- `variables.DEBUG`: {value: "True", statement: "DEBUG = True", ...}
- `variables.MAX_RETRIES`: {value: "3", ...}
- `variables.API_URL`: {value: "\"https://api.example.com\"", ...}
- `variables` does NOT include "\_private_var" (unless --include-private is used)

#### Scenario: Extract variables in conditional blocks

**Given** a Python file:

```python
if PRODUCTION:
    DATABASE_URL = "prod-db"
else:
    DATABASE_URL = "dev-db"
```

**When** the module symbol scanner processes the file

**Then** the output tracks block context:

- `variables.DATABASE_URL.blocks` includes "if"

---

### Requirement: Extract Module-Level Functions

The scanner MUST extract module-level function definitions, excluding private functions by default.

For each function, the scanner MUST extract:

- Function signature (with type annotations)
- Docstring
- Body MD5 hash
- Decorators (name, args, kwargs)
- Block context
- Attributes accessed on the function

#### Scenario: Extract public functions

**Given** a Python file:

```python
def helper(arg1: int, arg2: str) -> bool:
    """A helper function."""
    return True

def _internal():
    pass
```

**When** the module symbol scanner processes the file

**Then** the output contains:

- `functions.helper`: {signature: "def helper(arg1: int, arg2: str) -> bool", docstring: "A helper function.", ...}
- `functions` does NOT include "\_internal"

#### Scenario: Extract decorated functions

**Given** a Python file:

```python
@decorator
@another_decorator(arg1, kwarg="value")
def decorated_func():
    pass
```

**When** the module symbol scanner processes the file

**Then** the output contains:

- `functions.decorated_func.decorators`: [
  {name: "decorator", args: [], kwargs: {}},
  {name: "another_decorator", args: ["arg1"], kwargs: {"kwarg": "\"value\""}}
  ]

#### Scenario: Compute function body MD5

**Given** two functions with identical signatures but different bodies

**When** the module symbol scanner processes both functions

**Then** the `body_md5` values are different

---

### Requirement: Extract Module-Level Classes

The scanner MUST extract module-level class definitions, excluding private classes by default.

For each class, the scanner MUST extract:

- Docstring
- Body MD5 hash
- Base classes
- Class attributes (names only)
- Methods (names only)
- Decorators
- Block context
- Attributes accessed on the class

#### Scenario: Extract simple classes

**Given** a Python file:

```python
class MyClass:
    """A simple class."""
    attr1 = "value"

    def method1(self):
        pass

    def method2(self):
        pass

class _PrivateClass:
    pass
```

**When** the module symbol scanner processes the file

**Then** the output contains:

- `classes.MyClass`: {docstring: "A simple class.", attributes: ["attr1"], methods: ["method1", "method2"], bases: [], ...}
- `classes` does NOT include "\_PrivateClass"

#### Scenario: Extract classes with base classes

**Given** a Python file:

```python
class Child(Parent1, Parent2):
    pass
```

**When** the module symbol scanner processes the file

**Then** the output contains:

- `classes.Child.bases`: ["Parent1", "Parent2"]

#### Scenario: Extract decorated classes

**Given** a Python file:

```python
from dataclasses import dataclass

@dataclass
class Config:
    name: str
    value: int
```

**When** the module symbol scanner processes the file

**Then** the output contains:

- `classes.Config.decorators`: [{name: "dataclass", args: [], kwargs: {}}]

---

### Requirement: Provide Summary Statistics

The scanner MUST provide a summary section with:

- `total_modules`: Number of modules scanned
- `total_imports`: Total number of imports (all types)
- `total_symbols`: Total number of symbols (variables + functions + classes)
- `files_scanned`: Number of files scanned
- `scan_duration_ms`: Scan duration in milliseconds

#### Scenario: Generate summary statistics

**Given** a project with 10 Python files, containing:

- 50 total imports
- 30 variables
- 40 functions
- 30 classes

**When** the module symbol scanner processes the project

**Then** the summary contains:

- `total_modules`: 10
- `total_imports`: 50
- `total_symbols`: 100 (30 + 40 + 30)
- `files_scanned`: 10

---

### Requirement: CLI Integration

The scanner MUST provide a CLI command `scan-module-symbols` that:

- Accepts a path argument (file or directory)
- Supports standard file filtering options (--exclude-dirs, --include-files, --exclude-files)
- Supports output format options (--output-format, --output-file)
- Supports a --include-private flag to include private symbols

#### Scenario: Scan with default options

**Given** a project directory at `/path/to/project`

**When** the user runs:

```bash
uv run upcast scan-module-symbols /path/to/project
```

**Then** the scanner:

- Scans all .py files in the directory
- Excludes private symbols
- Outputs to stdout in YAML format

#### Scenario: Scan with file filtering

**Given** a project directory with test files

**When** the user runs:

```bash
uv run upcast scan-module-symbols --exclude-files "test_*.py" /path/to/project
```

**Then** the scanner excludes files matching "test\_\*.py"

#### Scenario: Include private symbols

**Given** a project with private symbols

**When** the user runs:

```bash
uv run upcast scan-module-symbols --include-private /path/to/project
```

**Then** the scanner includes symbols starting with "\_"

---

### Requirement: Scanner Registration

The scanner MUST be registered in the main CLI application so it can be invoked via the `scan-module-symbols` command.

#### Scenario: Scanner is registered

**Given** the module symbol scanner implementation

**When** the application starts

**Then** the scanner is registered in `main.py` with the command name "scan-module-symbols"

---

### Requirement: Data Model Validation

All data models MUST use Pydantic v2 for validation and serialization.

#### Scenario: Models validate correctly

**Given** valid scanner output data

**When** the data is deserialized into data models

**Then** no validation errors occur

#### Scenario: Models reject invalid data

**Given** invalid scanner output data (e.g., missing required fields)

**When** the data is deserialized into data models

**Then** Pydantic validation errors are raised

---

### Requirement: Test Coverage

The scanner implementation MUST have:

- Unit tests covering all core functionality
- Integration tests using real project samples
- Overall test coverage ≥ 80%

#### Scenario: Unit tests pass

**Given** the scanner implementation

**When** unit tests are run

**Then** all tests pass

#### Scenario: Coverage meets threshold

**Given** the scanner implementation with tests

**When** coverage is measured

**Then** coverage is ≥ 80%

#### Scenario: Integration tests pass

**Given** a real project (e.g., example/blueking-paas)

**When** the scanner is run on the project

**Then** the scan completes successfully and produces valid output
