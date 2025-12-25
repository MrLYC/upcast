# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Module Symbol Scanner**: New `scan-module-symbols` command for analyzing Python module imports and symbol definitions
  - Extracts import statements (import, from...import, from...import \*)
  - Tracks attribute access patterns on imported symbols
  - Extracts module-level variables, functions, and classes
  - Captures decorators, docstrings, and function signatures
  - Tracks symbol definition context (module, if, try, except blocks)
  - Computes body MD5 hashes for functions and classes
  - Supports filtering private symbols with `--include-private` option

### Changed

#### signal-scanner: New Flat List Output Format (Breaking Change)

**Migration Required**: The output structure has been simplified to match other scanners.

**Old Format:**

```yaml
post_save:
  type: django.signal
  receivers:
    - handler: users.signals.create_profile
      sender: User
```

**New Format:**

```yaml
signals:
  - signal: django.db.models.signals.post_save
    type: django
    category: model_signals
    receivers:
      - handler: users.signals.create_profile
        sender: User
```

**Migration Guide:**

- The top-level structure is now `signals: [...]` instead of signal names as keys
- Each signal entry includes: `signal`, `type`, `category`, `receivers`
- The full signal path is now in the `signal` field
- Signal categorization is explicit in the `category` field

**Why This Change:**

- Consistent with other scanner output formats
- Easier to iterate over all signals
- Better structured for programmatic processing

---

#### exception-handler-scanner: Structured Location Fields (Breaking Change)

**Migration Required**: The `location` string field has been split into structured fields.

**Old Format:**

```yaml
handlers:
  - location: api/views.py:45-52
    type: try-except
```

**New Format:**

```yaml
handlers:
  - file: api/views.py
    lineno: 45
    end_lineno: 52
    type: try-except
```

**Migration Guide:**

- Replace `location` parsing with direct field access:

  ```python
  # Old way (string parsing required)
  location = handler['location']  # "api/views.py:45-52"
  file, lines = location.split(':')
  start, end = lines.split('-')

  # New way (direct access)
  file = handler['file']
  start = handler['lineno']
  end = handler['end_lineno']
  ```

**Why This Change:**

- No string parsing required
- Type-safe integer line numbers
- Easier to filter/sort by file or line range

---

### Improved

#### concurrency-pattern-scanner: Skip Unknown Coroutines

- No longer outputs `asyncio.create_task()` patterns when the coroutine cannot be determined
- Reduces noise in scan results
- Results now only include actionable detections

**Example:**

```python
# This will no longer appear in output if coroutine_func cannot be resolved
asyncio.create_task(some_dynamic_coroutine())
```

---

#### django-settings-scanner: Full Statement Context

- The `code` field now shows the complete statement instead of just `settings.XXX`
- Provides better context for understanding how settings are used

**Example:**

```yaml
# Old output
code: settings.DEBUG

# New output
code: if settings.DEBUG: logger.setLevel(logging.DEBUG)
```

---

#### http-request-scanner: Cleaner URL Placeholders

- Consecutive `...` placeholders are now merged into a single `...`
- Reduces redundancy in URL patterns

**Example:**

```yaml
# Old output
url: https://api.example.com/... + ... + .../endpoint

# New output
url: https://api.example.com/.../endpoint
```
