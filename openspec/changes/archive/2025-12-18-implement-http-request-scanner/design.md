# Design: implement-http-request-scanner

## Architecture Overview

The HTTP Request Scanner follows the established scanner architecture pattern used by `env_var_scanner` and `exception_handler_scanner`, with AST-based analysis and structured output.

## Component Responsibilities

### 1. request_parser.py - Request Extraction

**Purpose**: Extract HTTP request details from astroid AST nodes

**Data Structures**:

```python
@dataclass
class HttpRequest:
    """Represents a single HTTP request call"""
    location: str              # "file.py:line"
    statement: str             # Original code statement
    library: str               # "requests" | "httpx" | "aiohttp" | etc.
    url: str                   # Extracted or inferred URL
    method: str                # "GET" | "POST" | etc.
    params: dict               # Query parameters
    headers: dict              # HTTP headers
    json_body: dict | None     # JSON request body
    data: dict | None          # Form data
    timeout: int | float | None  # Timeout value
    session_based: bool        # Whether called via session
    is_async: bool             # Whether using async/await
```

**Functions**:

- `detect_request_call(node: nodes.Call) -> str | None`: Identify library and pattern
- `extract_url(node: nodes.NodeNG) -> str`: Parse URL from argument (literal, f-string, concat)
- `extract_method(node: nodes.Call) -> str`: Determine HTTP method
- `extract_params(node: nodes.Call) -> dict`: Parse params/data/json kwargs
- `extract_headers(node: nodes.Call) -> dict`: Parse headers kwarg
- `extract_timeout(node: nodes.Call) -> int | float | None`: Parse timeout kwarg
- `is_session_call(node: nodes.Call) -> bool`: Detect session-based calls

### 2. checker.py - Request Aggregation

**Purpose**: Visit all files and aggregate HTTP requests by URL

**Class**: `HttpRequestChecker`

```python
class HttpRequestChecker:
    def __init__(self, base_path: Path):
        self.requests: dict[str, list[HttpRequest]] = {}  # URL -> requests
        self.base_path = base_path

    def check_file(self, file_path: Path) -> None:
        """Parse file and extract all HTTP requests"""

    def visit_call(self, node: nodes.Call) -> None:
        """Check if call is an HTTP request"""

    def get_requests_by_url(self) -> dict[str, list[HttpRequest]]:
        """Get requests grouped by URL"""

    def get_summary(self) -> dict:
        """Calculate summary statistics"""
```

### 3. export.py - Output Formatting

**Purpose**: Format aggregated requests into YAML/JSON

**Functions**:

- `format_request_output(requests: dict[str, list[HttpRequest]]) -> dict`: Convert to output structure
- `format_single_usage(request: HttpRequest) -> dict`: Format one usage entry
- Uses `common.export.export_to_yaml` and `common.export.export_to_json`

### 4. cli.py - Command-Line Interface

**Purpose**: CLI entry point with Click decorators

**Function**: `scan_http_requests(path, output, verbose, include, exclude, format)`

**Options**:

- Path argument (default=".")
- `-o/--output`: Output file path
- `-v/--verbose`: Enable verbose logging
- `--include`: File patterns to include
- `--exclude`: File patterns to exclude
- `--format`: Output format (yaml|json, default=yaml)

## Library-Specific Patterns

### requests Library

**Import patterns**:

```python
import requests
from requests import get, post
```

**Detection patterns**:

```python
# Module-level functions
requests.get(url, ...)
requests.post(url, ...)
requests.put(url, ...)
requests.delete(url, ...)
requests.patch(url, ...)
requests.head(url, ...)
requests.options(url, ...)

# Session methods
session.get(url, ...)
session.post(url, ...)
# ... etc
```

**Parameter extraction**:

- `url`: First positional arg or `url=` kwarg
- `params`: `params=` kwarg (dict)
- `headers`: `headers=` kwarg (dict)
- `json`: `json=` kwarg (dict)
- `data`: `data=` kwarg (dict or str)
- `timeout`: `timeout=` kwarg (int or float)

### httpx Library

**Import patterns**:

```python
import httpx
```

**Detection patterns**:

```python
# Sync
httpx.get(url, ...)
httpx.post(url, ...)
# ... etc

# Async
async with httpx.AsyncClient() as client:
    await client.get(url, ...)
```

**Parameter extraction**: Same as requests (compatible API)

### aiohttp Library

**Import patterns**:

```python
import aiohttp
```

**Detection patterns**:

```python
async with aiohttp.ClientSession() as session:
    async with session.get(url, ...) as resp:
        ...
```

**Parameter extraction**:

- `url`: First positional arg
- `params`: `params=` kwarg
- `headers`: `headers=` kwarg
- `json`: `json=` kwarg
- `data`: `data=` kwarg
- `timeout`: `timeout=` kwarg (aiohttp.ClientTimeout object or int)

### urllib3 Library

**Import patterns**:

```python
import urllib3
```

**Detection patterns**:

```python
http = urllib3.PoolManager()
http.request(method, url, ...)
http.request("GET", url, fields=...)
```

**Parameter extraction**:

- `method`: First positional arg (string)
- `url`: Second positional arg
- `fields`: `fields=` kwarg (dict for query params)
- `headers`: `headers=` kwarg (dict)
- `body`: `body=` kwarg
- `timeout`: `timeout=` kwarg

### urllib.request

**Import patterns**:

```python
from urllib.request import urlopen, Request
import urllib.request
```

**Detection patterns**:

```python
urlopen(url)
urlopen(Request(url, headers=...))
```

**Parameter extraction**:

- `url`: First positional arg (string or Request object)
- If Request object: parse url, headers from Request constructor

### http.client

**Import patterns**:

```python
import http.client
```

**Detection patterns**:

```python
conn = http.client.HTTPSConnection(host)
conn.request(method, url, ...)
```

**Parameter extraction**:

- Host from HTTPSConnection/HTTPConnection constructor
- `method`: First positional arg to request()
- `url`: Second positional arg (path)
- `body`: Third positional arg or `body=` kwarg
- `headers`: `headers=` kwarg (dict)
- Reconstruct full URL: `https://{host}{path}` or `http://{host}{path}`

## URL Resolution Strategy

### Static Strings

```python
requests.get("https://api.example.com/users")
# → url: "https://api.example.com/users"
```

### F-strings with Constants

```python
API_BASE = "https://api.example.com"
requests.get(f"{API_BASE}/users")
# → Use astroid inference to resolve API_BASE
# → url: "https://api.example.com/users"
```

### String Concatenation

```python
BASE_URL = "https://api.example.com"
requests.get(BASE_URL + "/users")
# → Use astroid inference to resolve
# → url: "https://api.example.com/users"
```

### Unresolvable Dynamic URLs

```python
def fetch(endpoint):
    requests.get(f"https://api.example.com/{endpoint}")
# → Cannot resolve at static analysis time
# → url: "`https://api.example.com/{endpoint}`" (backtick-wrapped)
```

**Implementation**: Use `common.ast_utils.infer_literal_value()` with fallback to backtick wrapping

## Session Detection

**Session-based patterns**:

- requests: `session.get()` where session is `requests.Session()`
- httpx: `client.get()` where client is `httpx.Client()` or `httpx.AsyncClient()`
- aiohttp: `session.get()` where session is `aiohttp.ClientSession()`

**Detection strategy**:

1. Check if call is attribute access (e.g., `session.get`)
2. Attempt to infer type of base object (session/client)
3. Check if type matches known session classes
4. Set `session_based: true` if match found

## Aggregation Strategy

**Grouping**: By URL (after resolution)

**Per-URL data**:

- Primary method (most common method for this URL)
- Primary library (most common library for this URL)
- List of all usages with full details

**Sorting**:

- URLs: Alphabetically
- Usages within URL: By location (file path, then line number)

## Error Handling

**Unparseable files**: Skip with debug log message (follow checker.py pattern)

**Unresolvable URLs**: Mark with backticks in output

**Missing parameters**: Represent as `null` or empty dict in output

**Type inference failures**: Fall back to string representation

## Testing Strategy

### Test Fixtures

Create realistic test files in `tests/test_http_request_scanner/fixtures/`:

1. `requests_patterns.py`: requests library patterns (simple, session, parameters)
2. `httpx_patterns.py`: httpx sync and async patterns
3. `aiohttp_patterns.py`: aiohttp async patterns
4. `urllib_patterns.py`: urllib3, urllib.request patterns
5. `http_client_patterns.py`: http.client patterns
6. `mixed_libraries.py`: Multiple libraries in same file
7. `dynamic_urls.py`: F-strings, concatenation, unresolvable

### Test Coverage

- **test_request_parser.py**: Test each library's pattern detection
- **test_checker.py**: Test file processing and aggregation
- **test_export.py**: Test YAML/JSON output formatting
- **test_cli.py**: Test CLI options and error handling
- **test_integration.py**: End-to-end tests with fixtures

**Target**: 85%+ coverage

## Performance Considerations

**File filtering**: Use `common.file_utils.collect_python_files()` with include/exclude patterns

**AST parsing**: Reuse astroid's caching where possible

**Large codebases**: Process files sequentially (no premature parallelization)

**Memory**: Store only essential data in HttpRequest objects

## Future Extensions

Potential enhancements not in initial scope:

1. **Retry patterns**: Detect retry decorators (@retry, tenacity)
2. **Circuit breakers**: Detect circuit breaker patterns
3. **Rate limiting**: Detect rate limiting decorators
4. **API version detection**: Parse version from URLs (/v1/, /v2/)
5. **Credential detection**: Highlight hardcoded credentials with warnings
6. **Response handling**: Track response processing patterns
7. **Error handling**: Link to exception_handler_scanner for HTTP error handling
