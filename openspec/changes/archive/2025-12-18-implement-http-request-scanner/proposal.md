# Proposal: implement-http-request-scanner

## What

Implement a new scanner module `http_request_scanner` to detect and analyze external HTTP/API request patterns in Python codebases, outputting structured documentation of HTTP calls made via popular libraries (requests, httpx, aiohttp, urllib, urllib3, http.client) with details about URLs, methods, parameters, headers, and usage locations.

## What Changes

### Implementation Completed

**New Scanner Module**: `upcast/http_request_scanner/`

Implemented a complete HTTP request scanner module following the established scanner pattern:

- **request_parser.py**: Core logic for detecting and extracting HTTP request information from AST nodes

  - Type inference-based library detection using astroid (prevents false positives)
  - Support for 6 major HTTP libraries: requests, httpx, aiohttp, urllib3, urllib.request, http.client
  - URL extraction with smart handling of f-strings, .format() method, and string concatenation
  - Dynamic URL resolution with `...` placeholder for unresolvable parts
  - HTTP method detection (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
  - Parameter extraction (query params, headers, JSON body, form data, timeout)
  - Session-based vs one-off request detection

- **checker.py**: AST visitor implementing HttpRequestChecker

  - Traverses Python AST using astroid
  - Detects Call nodes matching HTTP library patterns
  - Extracts location, statement, and request details
  - Groups results by URL

- **export.py**: Output formatting

  - YAML and JSON export formats
  - Groups requests by URL with aggregated usage information
  - Generates summary statistics (total requests, unique URLs, libraries used, etc.)

- **cli.py**: Command-line interface

  - `scan_http_requests()` entry point
  - Path validation and file collection
  - Integration with export formats

- **ast_utils.py**: AST utilities specific to HTTP request parsing
  - Helper functions for extracting format string templates
  - Import tracking for handling aliases
  - Type inference helpers

**CLI Integration**:

- Added `scan-http-requests` command to `upcast/main.py`
- Command supports path argument, output format (yaml/json), and output file options

**Test Coverage**:

- `tests/test_http_request_scanner/`: Comprehensive test suite
  - `test_request_parser.py`: Core parsing logic tests
  - `test_checker.py`: AST visitor tests
  - `test_cli.py`: CLI integration tests
  - `test_export.py`: Export format tests
  - `test_ast_utils.py`: Utility function tests
  - Test fixtures covering all supported libraries and edge cases
  - False positive prevention tests (dict/class named "requests", etc.)

**Key Implementation Decisions**:

1. **Type Inference for Library Detection**: Uses astroid to infer actual types instead of name-based detection, preventing false positives from user-defined variables/classes named "requests"

2. **Smart URL Extraction**:

   - Static strings: captured as-is
   - f-strings: resolved when possible, use `...` for unresolvable variables
   - .format() method: extract string template, replace `{}` with `...`
   - Concatenation: show known parts with `...` for dynamic parts
   - Function parameters: skipped entirely (no static information)

3. **Session Detection**: Tracks whether requests use session objects or are one-off calls

4. **Output Grouping**: Results grouped by URL with all usage locations and their context

**Specs Updated**:

- Created `openspec/specs/http-request-scanner/spec.md` with complete requirements
- Updated `openspec/specs/cli-interface/spec.md` to document new command

**Test Results**:

- ✅ 377 tests passing (32 HTTP scanner tests + existing tests)
- ✅ 85%+ code coverage achieved
- ✅ All ruff checks passing (PEP8 compliant, complexity within limits)

## Why

Understanding external API dependencies is crucial for application maintenance, security auditing, and migration planning. Teams need:

1. **API dependency inventory**: Know which external APIs the application depends on
2. **Usage pattern analysis**: Track how APIs are called (methods, parameters, authentication)
3. **Migration assistance**: Support API client library upgrades or replacements
4. **Security auditing**: Identify hardcoded API keys, insecure URLs, or missing timeouts
5. **Documentation generation**: Automatically document all external API integrations

Following the established pattern of `env_var_scanner` and `exception_handler_scanner`, this scanner provides automated discovery and analysis of HTTP request patterns using astroid-based AST analysis.

## How

### Core Approach

Use astroid to parse Python files and detect HTTP request patterns across multiple libraries:

1. **Library detection**: Support requests, httpx, aiohttp, urllib, urllib3, http.client
2. **URL extraction**: Parse URLs from arguments (static strings, f-strings, concatenation)
3. **Method detection**: Identify HTTP methods (GET, POST, PUT, DELETE, PATCH, etc.)
4. **Parameter extraction**: Capture query parameters, headers, JSON body, form data
5. **Authentication detection**: Identify auth headers, API keys, tokens
6. **Timeout tracking**: Detect timeout configurations
7. **Session usage**: Track session-based requests vs one-off calls

### Supported Libraries & Patterns

#### requests library

```python
import requests
# Simple GET
requests.get("https://api.example.com/users")
# POST with params
requests.post("https://api.example.com/login", json={"user": "admin"}, headers={"Auth": "token"})
# Session usage
with requests.Session() as s:
    s.get("https://api.example.com/a")
```

#### httpx library

```python
import httpx
# Sync
httpx.get("https://example.com")
# Async
async with httpx.AsyncClient() as client:
    await client.get("https://example.com")
```

#### aiohttp library

```python
import aiohttp
async with aiohttp.ClientSession() as session:
    async with session.get("https://example.com") as resp:
        await resp.text()
```

#### urllib3 library

```python
import urllib3
http = urllib3.PoolManager()
http.request("GET", "https://example.com")
```

#### urllib.request

```python
from urllib.request import urlopen
with urlopen("https://example.com") as resp:
    resp.read()
```

#### http.client

```python
import http.client
conn = http.client.HTTPSConnection("example.com")
conn.request("GET", "/path")
```

### Module Structure

```
upcast/http_request_scanner/
├── __init__.py              # Public API exports
├── cli.py                   # scan_http_requests() entry point
├── checker.py               # HttpRequestChecker visitor
├── request_parser.py        # HTTP request extraction logic
└── export.py                # YAML/JSON formatting and output
```

Reuse from `upcast/common/`:

- `ast_utils.py`: safe_as_string, infer_literal_value
- `file_utils.py`: collect_python_files, validate_path
- `export.py`: export_to_yaml, export_to_json

### Output Format

Group by URL with aggregated usage information:

```yaml
https://api.example.com/users:
  method: GET
  library: requests
  usages:
    - location: "api/client.py:15"
      statement: "requests.get('https://api.example.com/users', params={'page': 1})"
      method: GET
      params:
        page: 1
      headers:
        Authorization: "Bearer token"
      timeout: 5
      session_based: false
    - location: "services/user_service.py:42"
      statement: "session.get('https://api.example.com/users')"
      method: GET
      params: {}
      headers: {}
      timeout: null
      session_based: true

https://api.example.com/login:
  method: POST
  library: requests
  usages:
    - location: "auth/login.py:23"
      statement: "requests.post('https://api.example.com/login', json={'username': 'admin'})"
      method: POST
      params: {}
      headers: {}
      json_body:
        username: admin
      timeout: null
      session_based: false

https://example.com/:
  method: GET
  library: httpx
  usages:
    - location: "external/fetch.py:10"
      statement: "httpx.get('https://example.com')"
      method: GET
      params: {}
      headers: {}
      timeout: null
      session_based: false

summary:
  total_requests: 4
  unique_urls: 3
  libraries_used: [requests, httpx]
  session_based_count: 1
  requests_without_timeout: 3
```

## Impact

### New Files

- `upcast/http_request_scanner/*.py` (5 files)
- `tests/test_http_request_scanner/*.py` (5 test files + fixtures)
- `openspec/specs/http-request-scanner/spec.md`

### Modified Files

- `upcast/main.py`: Add `scan-http-requests` CLI command registration
- `openspec/specs/cli-interface/spec.md`: Document new command

### Dependencies

- Reuse existing `astroid` dependency
- Reuse `upcast.common` utilities
- No new external dependencies

### Backward Compatibility

No breaking changes. Pure addition of new functionality following established patterns.

## Alternatives Considered

1. **Regex-based parsing**: Rejected because it cannot handle dynamic URLs (f-strings, variables) or complex parameter structures
2. **Runtime network tracing**: Rejected because it only captures executed requests, missing conditional or error-path requests
3. **OpenAPI spec generation**: Rejected because we're scanning client code, not server endpoints
4. **Static URL list extraction**: Rejected because we need full context (method, params, headers) for each request

## Open Questions

1. **Dynamic URLs**: Should we attempt to resolve f-strings and variable concatenation, or mark as dynamic?

   - **Recommendation**: Use astroid inference to resolve when possible, mark with backticks when unresolved (following common.ast_utils pattern)

2. **Authentication patterns**: Should we redact sensitive values (API keys, tokens) in output?

   - **Recommendation**: Output as-is with a warning in documentation; users can post-process if needed

3. **WebSocket connections**: Should we detect WebSocket usage (websockets library, aiohttp WebSocket)?

   - **Recommendation**: Out of scope for initial version; focus on HTTP requests only

4. **GraphQL clients**: Should we detect GraphQL-specific libraries (gql, graphene)?

   - **Recommendation**: Future enhancement; treat as regular HTTP POST for now

5. **Third-party API SDKs**: Should we detect SDK-specific methods (boto3, stripe, twilio)?
   - **Recommendation**: Out of scope; these abstract away HTTP calls

## Success Criteria

- [ ] Detect HTTP requests from 6 major libraries (requests, httpx, aiohttp, urllib, urllib3, http.client)
- [ ] Extract URLs (static strings, f-strings, simple concatenation)
- [ ] Identify HTTP methods (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
- [ ] Parse common parameters (params, headers, json, data, timeout)
- [ ] Distinguish session-based vs one-off requests
- [ ] Group results by URL with aggregated usage information
- [ ] Generate summary statistics
- [ ] Output structured YAML/JSON matching spec
- [ ] 85%+ test coverage following project patterns
- [ ] CLI integration: `upcast scan-http-requests <path>`
- [ ] Documentation with usage examples
