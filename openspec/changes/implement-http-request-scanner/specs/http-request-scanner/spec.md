# http-request-scanner Specification

## Purpose

Detect and analyze external HTTP/API request patterns in Python codebases to provide structured documentation of API dependencies, usage patterns, and configuration.

## ADDED Requirements

### Requirement: requests Library Detection

The system SHALL detect HTTP requests made via the requests library using astroid-based AST analysis.

#### Scenario: requests.get() detection

- **WHEN** code uses `requests.get('https://api.example.com/users')`
- **THEN** the system SHALL identify this as an HTTP request
- **AND** extract library as "requests"
- **AND** extract method as "GET"
- **AND** extract URL as "https://api.example.com/users"
- **AND** record the file location and statement

#### Scenario: requests.post() with parameters

- **WHEN** code uses `requests.post('https://api.example.com/login', json={'user': 'admin'}, headers={'Auth': 'token'})`
- **THEN** the system SHALL extract method as "POST"
- **AND** extract json_body as `{'user': 'admin'}`
- **AND** extract headers as `{'Auth': 'token'}`
- **AND** record all parameters

#### Scenario: requests with query parameters

- **WHEN** code uses `requests.get('https://api.example.com/users', params={'page': 1, 'limit': 10})`
- **THEN** the system SHALL extract params as `{'page': 1, 'limit': 10}`
- **AND** record timeout as null if not specified

#### Scenario: requests with timeout

- **WHEN** code uses `requests.get('https://api.example.com', timeout=5)`
- **THEN** the system SHALL extract timeout as 5
- **AND** record this in the output

#### Scenario: Session-based requests

- **WHEN** code uses:
  ```python
  session = requests.Session()
  session.get('https://api.example.com/users')
  ```
- **THEN** the system SHALL mark session_based as true
- **AND** identify this as a session-based request

#### Scenario: Session with context manager

- **WHEN** code uses:
  ```python
  with requests.Session() as s:
      s.get('https://api.example.com/a')
  ```
- **THEN** the system SHALL detect the session context
- **AND** mark session_based as true

#### Scenario: Imported function detection

- **WHEN** code uses `from requests import get` and then `get('https://example.com')`
- **THEN** the system SHALL resolve the import through astroid
- **AND** detect it as a requests.get() call

### Requirement: httpx Library Detection

The system SHALL detect HTTP requests made via the httpx library for both sync and async usage.

#### Scenario: httpx.get() sync detection

- **WHEN** code uses `httpx.get('https://example.com')`
- **THEN** the system SHALL identify this as an HTTP request
- **AND** extract library as "httpx"
- **AND** extract method as "GET"
- **AND** mark is_async as false

#### Scenario: httpx AsyncClient detection

- **WHEN** code uses:
  ```python
  async with httpx.AsyncClient() as client:
      await client.get('https://example.com')
  ```
- **THEN** the system SHALL detect the async client usage
- **AND** mark is_async as true
- **AND** mark session_based as true

#### Scenario: httpx with parameters

- **WHEN** code uses `httpx.post('https://api.example.com', json={'data': 'value'})`
- **THEN** the system SHALL extract json_body as `{'data': 'value'}`
- **AND** handle parameters same as requests library

### Requirement: aiohttp Library Detection

The system SHALL detect HTTP requests made via the aiohttp library for async usage.

#### Scenario: aiohttp ClientSession detection

- **WHEN** code uses:
  ```python
  async with aiohttp.ClientSession() as session:
      async with session.get('https://example.com') as resp:
          await resp.text()
  ```
- **THEN** the system SHALL identify this as an HTTP request
- **AND** extract library as "aiohttp"
- **AND** mark is_async as true
- **AND** mark session_based as true

#### Scenario: aiohttp with parameters

- **WHEN** code uses `session.post('https://api.example.com', json={'key': 'value'}, headers={'Auth': 'token'})`
- **THEN** the system SHALL extract json_body and headers
- **AND** handle parameters similar to requests library

#### Scenario: aiohttp timeout handling

- **WHEN** code uses `session.get('https://example.com', timeout=10)`
- **THEN** the system SHALL extract timeout as 10
- **AND** handle aiohttp.ClientTimeout objects if present

### Requirement: urllib3 Library Detection

The system SHALL detect HTTP requests made via the urllib3 library.

#### Scenario: urllib3 PoolManager.request() detection

- **WHEN** code uses:
  ```python
  http = urllib3.PoolManager()
  http.request('GET', 'https://example.com')
  ```
- **THEN** the system SHALL identify this as an HTTP request
- **AND** extract library as "urllib3"
- **AND** extract method from first argument ("GET")
- **AND** extract URL from second argument

#### Scenario: urllib3 with fields parameter

- **WHEN** code uses `http.request('GET', 'https://example.com', fields={'param': 'value'})`
- **THEN** the system SHALL extract params as `{'param': 'value'}`
- **AND** map fields kwarg to params

#### Scenario: urllib3 with headers

- **WHEN** code uses `http.request('POST', 'https://api.example.com', headers={'Auth': 'token'})`
- **THEN** the system SHALL extract headers as `{'Auth': 'token'}`

### Requirement: urllib.request Detection

The system SHALL detect HTTP requests made via urllib.request module.

#### Scenario: urlopen() with direct URL

- **WHEN** code uses `urlopen('https://example.com')`
- **THEN** the system SHALL identify this as an HTTP request
- **AND** extract library as "urllib.request"
- **AND** extract URL as "https://example.com"
- **AND** default method to "GET"

#### Scenario: urlopen() with Request object

- **WHEN** code uses:
  ```python
  req = Request('https://example.com', headers={'User-Agent': 'MyApp'})
  urlopen(req)
  ```
- **THEN** the system SHALL parse the Request object
- **AND** extract URL from Request constructor
- **AND** extract headers from Request constructor

### Requirement: http.client Detection

The system SHALL detect HTTP requests made via http.client module.

#### Scenario: HTTPSConnection.request() detection

- **WHEN** code uses:
  ```python
  conn = http.client.HTTPSConnection('example.com')
  conn.request('GET', '/path')
  ```
- **THEN** the system SHALL identify this as an HTTP request
- **AND** extract library as "http.client"
- **AND** reconstruct URL as "https://example.com/path"
- **AND** extract method as "GET"

#### Scenario: HTTPConnection for HTTP

- **WHEN** code uses `http.client.HTTPConnection('example.com')`
- **THEN** the system SHALL reconstruct URL with "http://" scheme

#### Scenario: http.client with headers

- **WHEN** code uses `conn.request('POST', '/api', headers={'Content-Type': 'application/json'})`
- **THEN** the system SHALL extract headers from the headers parameter

### Requirement: URL Resolution

The system SHALL resolve URLs using astroid inference with fallback to unresolved markers.

#### Scenario: Static string URL

- **WHEN** code uses `requests.get('https://api.example.com/users')`
- **THEN** the system SHALL extract URL as "https://api.example.com/users"
- **AND** return the literal string value

#### Scenario: F-string URL with constants

- **WHEN** code uses:
  ```python
  API_BASE = 'https://api.example.com'
  requests.get(f'{API_BASE}/users')
  ```
- **THEN** the system SHALL use astroid inference to resolve API_BASE
- **AND** evaluate the f-string to "https://api.example.com/users"

#### Scenario: String concatenation with constants

- **WHEN** code uses:
  ```python
  BASE_URL = 'https://api.example.com'
  requests.get(BASE_URL + '/users')
  ```
- **THEN** the system SHALL use astroid inference to resolve BASE_URL
- **AND** evaluate the concatenation to "https://api.example.com/users"

#### Scenario: .format() with constants

- **WHEN** code uses `requests.get('{}/users'.format(API_BASE))` where API_BASE is a constant
- **THEN** the system SHALL resolve the format string
- **AND** return the evaluated URL

#### Scenario: Unresolvable dynamic URL

- **WHEN** code uses:
  ```python
  def fetch(endpoint):
      requests.get(f'https://api.example.com/{endpoint}')
  ```
- **THEN** the system SHALL fail to resolve the URL statically
- **AND** wrap the expression in backticks: `` `f'https://api.example.com/{endpoint}'` ``
- **AND** include this in the output with backtick marker

#### Scenario: URL resolution using common utilities

- **WHEN** resolving any URL
- **THEN** the system SHALL use `common.ast_utils.infer_literal_value()`
- **AND** follow the backtick wrapping pattern for unresolved values

### Requirement: Parameter Extraction

The system SHALL extract HTTP request parameters including query params, headers, body data, and timeout.

#### Scenario: Query parameters extraction

- **WHEN** code uses `params={'page': 1, 'limit': 10}` kwarg
- **THEN** the system SHALL extract params as a dictionary
- **AND** use astroid inference to resolve dict literals
- **AND** handle nested values

#### Scenario: Headers extraction

- **WHEN** code uses `headers={'Authorization': 'Bearer token', 'Content-Type': 'application/json'}` kwarg
- **THEN** the system SHALL extract headers as a dictionary
- **AND** preserve all header names and values

#### Scenario: JSON body extraction

- **WHEN** code uses `json={'username': 'admin', 'password': '***'}` kwarg
- **THEN** the system SHALL extract json_body as a dictionary
- **AND** record as-is (no redaction in this version)

#### Scenario: Form data extraction

- **WHEN** code uses `data={'field1': 'value1', 'field2': 'value2'}` kwarg
- **THEN** the system SHALL extract data as a dictionary

#### Scenario: Timeout extraction

- **WHEN** code uses `timeout=5` kwarg
- **THEN** the system SHALL extract timeout as 5 (integer)
- **AND** support float values like `timeout=2.5`

#### Scenario: Missing optional parameters

- **WHEN** code does not provide params, headers, json, data, or timeout
- **THEN** the system SHALL record:
  - params as empty dict `{}`
  - headers as empty dict `{}`
  - json_body as null
  - data as null
  - timeout as null

### Requirement: Session Detection

The system SHALL identify session-based requests vs one-off requests.

#### Scenario: requests.Session() detection

- **WHEN** code uses:
  ```python
  session = requests.Session()
  session.get('https://example.com')
  ```
- **THEN** the system SHALL infer type of `session` variable
- **AND** identify it as requests.Session
- **AND** mark session_based as true

#### Scenario: httpx.Client() detection

- **WHEN** code uses:
  ```python
  client = httpx.Client()
  client.get('https://example.com')
  ```
- **THEN** the system SHALL identify client as httpx.Client
- **AND** mark session_based as true

#### Scenario: aiohttp.ClientSession() detection

- **WHEN** code uses `async with aiohttp.ClientSession() as session:`
- **THEN** the system SHALL identify session as aiohttp.ClientSession
- **AND** mark session_based as true

#### Scenario: One-off module-level calls

- **WHEN** code uses `requests.get()` directly without Session
- **THEN** the system SHALL mark session_based as false

### Requirement: Result Aggregation by URL

The system SHALL aggregate all HTTP requests grouped by URL across the entire codebase.

#### Scenario: Single URL, multiple locations

- **WHEN** `https://api.example.com/users` is accessed in 3 different files
- **THEN** the system SHALL create one entry for this URL
- **AND** list all 3 usages with complete context
- **AND** include location, statement, parameters for each usage

#### Scenario: Same URL, different methods

- **WHEN** `https://api.example.com/users` is accessed with GET and POST
- **THEN** the system SHALL group under the same URL
- **AND** record different methods in individual usages
- **AND** set primary method as the most common one

#### Scenario: Same URL, different libraries

- **WHEN** `https://example.com` is accessed via requests and httpx
- **THEN** the system SHALL group under the same URL
- **AND** record different libraries in individual usages
- **AND** set primary library as the most common one

#### Scenario: Usage sorting

- **WHEN** recording usages for a URL
- **THEN** each usage SHALL include location in format: `"path/to/file.py:line"`
- **AND** use relative paths from project root
- **AND** sort usages by file path, then line number

### Requirement: YAML Output Format

The system SHALL export aggregated results in structured YAML format optimized for human readability.

#### Scenario: Basic URL entry structure

- **WHEN** exporting HTTP requests
- **THEN** each URL SHALL be a top-level key
- **AND** include `method` (primary method)
- **AND** include `library` (primary library)
- **AND** include `usages` list with each usage containing:
  - `location`: file path and line number
  - `statement`: the actual code statement
  - `method`: HTTP method for this specific usage
  - `params`: query parameters (dict)
  - `headers`: HTTP headers (dict)
  - `json_body`: JSON request body (dict or null)
  - `data`: form data (dict or null)
  - `timeout`: timeout value (number or null)
  - `session_based`: boolean
  - `is_async`: boolean

#### Scenario: Summary section

- **WHEN** exporting HTTP requests
- **THEN** the output SHALL include a `summary` section with:
  - `total_requests`: total count of all requests
  - `unique_urls`: count of unique URLs
  - `libraries_used`: list of unique library names
  - `session_based_count`: count of session-based requests
  - `requests_without_timeout`: count of requests with null timeout
  - `async_requests`: count of async requests

#### Scenario: YAML formatting

- **WHEN** generating YAML output
- **THEN** the system SHALL use 2-space indentation
- **AND** use block style for lists and dicts
- **AND** preserve Unicode characters
- **AND** sort URLs alphabetically

#### Scenario: Empty field handling

- **WHEN** optional fields are not present
- **THEN** the system SHALL output:
  - `params: {}` (empty dict, not null)
  - `headers: {}` (empty dict, not null)
  - `json_body: null` (nullable field)
  - `data: null` (nullable field)
  - `timeout: null` (nullable field)

#### Scenario: Example output

```yaml
summary:
  total_requests: 4
  unique_urls: 3
  libraries_used: [requests, httpx]
  session_based_count: 1
  requests_without_timeout: 3
  async_requests: 1

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
      data: null
      timeout: null
      session_based: false
      is_async: false

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
      json_body: null
      data: null
      timeout: 5
      session_based: false
      is_async: false
    - location: "services/user_service.py:42"
      statement: "session.get('https://api.example.com/users')"
      method: GET
      params: {}
      headers: {}
      json_body: null
      data: null
      timeout: null
      session_based: true
      is_async: false

https://example.com/:
  method: GET
  library: httpx
  usages:
    - location: "external/fetch.py:10"
      statement: "await client.get('https://example.com')"
      method: GET
      params: {}
      headers: {}
      json_body: null
      data: null
      timeout: null
      session_based: true
      is_async: true
```

### Requirement: JSON Output Format Support

The system SHALL support JSON output format as an alternative to YAML.

#### Scenario: JSON format option

- **WHEN** user specifies `--format json`
- **THEN** the system SHALL output in JSON format
- **AND** use the same structure as YAML
- **AND** use 2-space indentation
- **AND** ensure proper UTF-8 encoding

#### Scenario: JSON vs YAML structure consistency

- **WHEN** outputting in either format
- **THEN** both formats SHALL have identical data structure
- **AND** be convertible between formats without data loss

### Requirement: CLI Interface

The system SHALL provide a command-line interface for scanning projects and files.

#### Scenario: Basic directory scanning

- **WHEN** user runs `upcast scan-http-requests <path>`
- **THEN** the system SHALL scan all Python files in the directory
- **AND** detect all HTTP requests
- **AND** output aggregated results to stdout

#### Scenario: Output to file

- **WHEN** user runs `upcast scan-http-requests <path> -o output.yaml`
- **THEN** the system SHALL write results to output.yaml
- **AND** create parent directories if needed

#### Scenario: Include patterns

- **WHEN** user runs `upcast scan-http-requests <path> --include "*/api/*.py"`
- **THEN** the system SHALL only scan files matching the pattern
- **AND** use glob pattern matching

#### Scenario: Exclude patterns

- **WHEN** user runs `upcast scan-http-requests <path> --exclude "*/tests/*.py"`
- **THEN** the system SHALL skip files matching the pattern

#### Scenario: Format selection

- **WHEN** user runs `upcast scan-http-requests <path> --format json`
- **THEN** the system SHALL output in JSON format instead of YAML

#### Scenario: Verbose output

- **WHEN** user runs `upcast scan-http-requests <path> -v`
- **THEN** the system SHALL enable debug logging
- **AND** show file processing progress

### Requirement: Error Handling

The system SHALL handle errors gracefully with informative messages.

#### Scenario: Unparseable file

- **WHEN** a Python file cannot be parsed by astroid
- **THEN** the system SHALL skip the file
- **AND** log a debug message with the file path
- **AND** continue processing other files

#### Scenario: Nonexistent path

- **WHEN** user provides a path that doesn't exist
- **THEN** the system SHALL raise FileNotFoundError
- **AND** include the invalid path in error message

#### Scenario: Permission error

- **WHEN** a file cannot be read due to permissions
- **THEN** the system SHALL skip the file
- **AND** log a warning message

### Requirement: Unit Test Coverage

The system SHALL include comprehensive unit tests covering all core functionality.

#### Scenario: Library detection tests

- **WHEN** running tests for library detection
- **THEN** tests SHALL verify each library's patterns
- **AND** cover requests, httpx, aiohttp, urllib3, urllib.request, http.client
- **AND** test both sync and async variants

#### Scenario: URL resolution tests

- **WHEN** running tests for URL resolution
- **THEN** tests SHALL verify static strings
- **AND** verify f-string resolution
- **AND** verify concatenation resolution
- **AND** verify unresolvable dynamic URLs (backtick wrapping)

#### Scenario: Parameter extraction tests

- **WHEN** running tests for parameter extraction
- **THEN** tests SHALL verify params, headers, json_body, data, timeout
- **AND** test with and without each parameter
- **AND** test nested structures

#### Scenario: Aggregation tests

- **WHEN** running tests for aggregation
- **THEN** tests SHALL verify grouping by URL
- **AND** verify sorting of usages
- **AND** verify summary statistics

#### Scenario: Test organization

- **WHEN** organizing the test suite
- **THEN** tests SHALL be in `tests/test_http_request_scanner/`
- **AND** separated into modules:
  - `test_request_parser.py`
  - `test_checker.py`
  - `test_cli.py`
  - `test_export.py`
  - `test_integration.py`
- **AND** use pytest fixtures for common test setup
- **AND** include realistic test fixtures in `fixtures/` directory
