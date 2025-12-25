# Logging Scanner Design

## Architecture Overview

The logging scanner follows the established upcast scanner architecture pattern:

```
LoggingScanner (extends BaseScanner)
    ↓
Uses astroid for AST analysis
    ↓
Outputs LoggingOutput (Pydantic model)
```

## Data Models

### Output Structure

```python
LoggingOutput:
  summary: LoggingSummary
  results: dict[str, FileLoggingInfo]  # keyed by file path

FileLoggingInfo:
  logging: list[LogCall]     # stdlib logging
  loguru: list[LogCall]      # loguru
  structlog: list[LogCall]   # structlog
  django: list[LogCall]      # django.utils.log

LogCall:
  logger_name: str           # resolved logger name (module path or 'root')
  lineno: int                # line number
  level: str                 # debug/info/warning/error/critical
  message: str               # complete message string
  args: list[str]            # additional arguments
  type: str                  # 'string' | 'fstring' | 'percent' | 'format'
  has_sensitive: bool        # flag for potential sensitive data
  sensitive_patterns: list[str]  # matched sensitive patterns
```

### Summary Statistics

```python
LoggingSummary:
  total_log_calls: int
  files_scanned: int
  scan_duration_ms: int
  by_library: dict[str, int]      # counts per library
  by_level: dict[str, int]        # counts per level
  sensitive_calls: int            # calls with sensitive data
```

## Detection Strategy

### 1. Logger Resolution

**Standard Library (`logging`)**:

```python
import logging
logger = logging.getLogger(__name__)  # → resolve to module path
logger = logging.getLogger()          # → 'root'
logger = logging.getLogger('myapp')   # → 'myapp'
```

**Module Path Resolution**:

- Extract `__name__` from getLogger calls
- Map file path to package structure
- Find first-level `__init__.py` as package root
- Convert to dotted path (e.g., `myapp.services.auth`)

**Loguru**:

```python
from loguru import logger
logger.info("message")  # → logger_name from module path
```

**Structlog**:

```python
import structlog
logger = structlog.get_logger()  # → logger_name from module path
```

**Django**:

```python
import logging
logger = logging.getLogger(__name__)  # same as stdlib
```

### 2. Log Call Detection

**Patterns to Detect**:

1. **Direct method calls**:

   ```python
   logger.info("User logged in")
   logger.debug("Value: %s", value)
   logger.error("Failed", exc_info=True)
   ```

2. **Conditional logging**:

   ```python
   if logger.isEnabledFor(logging.DEBUG):
       logger.debug("Debug info")
   ```

3. **Logger accessed via attributes**:

   ```python
   self.logger.info("Message")
   cls.logger.warning("Warning")
   ```

4. **Module-level logging**:
   ```python
   logging.info("Direct call")  # → root logger
   ```

### 3. Message Extraction

**String Types**:

1. **Plain string**: `"User %s logged in"`
2. **f-string**: `f"User {user} logged in"`
3. **Percent formatting**: `"User %s" % user`
4. **str.format()**: `"User {}".format(user)`

**Argument Extraction**:

- Positional args after message
- Keyword args (extra dict)
- Handle variable arguments (`*args`)

### 4. Sensitive Information Detection

**Patterns to Flag**:

1. **Keywords in message**:

   - password, passwd, pwd
   - token, api_key, secret
   - ssn, credit_card
   - email, phone (in certain contexts)

2. **Common sensitive formats**:

   - Base64-encoded strings
   - JWT tokens (eyJ pattern)
   - API keys (specific length/format)
   - Private keys (-----BEGIN)

3. **Variable names in args**:
   - `logger.info("Key: %s", api_key)` → flag `api_key`

**Exclusions**:

- Generic terms like "user", "name" (too many false positives)
- Constant strings (not variables)
- Logging function names themselves

## Implementation Strategy

### Phase 1: Core Detection (stdlib logging)

1. Detect `logging.getLogger()` calls
2. Track logger variable assignments
3. Detect method calls on logger instances
4. Extract message and level
5. Basic logger name resolution

### Phase 2: Message Analysis

1. Extract complete message strings
2. Identify string format type
3. Extract arguments
4. Handle multi-line messages

### Phase 3: Sensitive Data Detection

1. Build sensitive keyword patterns
2. Scan messages for patterns
3. Analyze argument names
4. Generate warnings with matched patterns

### Phase 4: Multi-Library Support

1. Add loguru detection
2. Add structlog detection
3. Add django logging detection
4. Normalize output format

### Phase 5: Advanced Patterns

1. Indirect logger access (self.logger)
2. Conditional logging detection
3. Custom log levels
4. Logger hierarchies

## Edge Cases

1. **Dynamic logger names**: `getLogger(f"module.{name}")` → record as-is
2. **Multiple loggers per file**: Track separately
3. **Aliased imports**: `from logging import getLogger as get_log`
4. **Logger inheritance**: Track parent-child relationships
5. **Unicode in messages**: Handle encoding properly

## Testing Strategy

### Unit Tests

- Logger name resolution (root, **name**, custom)
- Each logging library detection
- Message type identification
- Sensitive pattern matching
- Argument extraction

### Integration Tests

- Real-world Python files with mixed logging
- Django project patterns
- Loguru-based projects
- Edge cases (dynamic names, conditionals)

### Test Fixtures

```python
# stdlib_logging.py - standard library patterns
# loguru_logging.py - loguru patterns
# structlog_logging.py - structlog patterns
# django_logging.py - Django patterns
# sensitive_logging.py - sensitive data test cases
# complex_logging.py - edge cases
```

## Performance Considerations

- **AST Parsing**: Reuse astroid parsing from BaseScanner
- **Pattern Matching**: Compile regex patterns once
- **Memory**: Stream processing for large codebases
- **Caching**: Cache module path resolution per file

## Security Considerations

- **False Positives**: Sensitive detection should be configurable
- **Output Safety**: Don't include actual sensitive values in report
- **Pattern Updates**: Allow custom sensitive patterns via config
