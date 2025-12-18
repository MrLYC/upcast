# Tasks: implement-http-request-scanner

## Implementation Tasks

### Phase 1: Foundation (Core Infrastructure)

- [x] **Create module structure**: Create `upcast/http_request_scanner/` directory with `__init__.py`, `cli.py`, `checker.py`, `request_parser.py`, `export.py`

  - Establishes basic module layout following project conventions
  - Defines public API exports in `__init__.py`
  - Reuses common utilities from `upcast.common`

- [x] **Define data structures**: Create dataclass in `request_parser.py`:

  - `HttpRequest`: location, statement, library, url, method, params, headers, json_body, data, timeout, session_based, is_async
  - Use dataclass following patterns from other scanners
  - Include proper type hints for all fields

- [x] **Create test structure**: Set up `tests/test_http_request_scanner/` with:

  - `__init__.py`
  - `test_request_parser.py` (tests for parsing logic)
  - `test_checker.py` (tests for aggregation)
  - `test_cli.py` (tests for CLI)
  - `test_export.py` (tests for output formatting)
  - `test_integration.py` (end-to-end tests)
  - `fixtures/` directory

- [x] **Create test fixtures**: Add to `fixtures/`:
  - `requests_patterns.py`: requests library usage patterns
  - `httpx_patterns.py`: httpx sync/async patterns
  - `aiohttp_patterns.py`: aiohttp async patterns
  - `urllib_patterns.py`: urllib3 and urllib.request patterns
  - `http_client_patterns.py`: http.client patterns
  - `dynamic_urls.py`: F-strings and concatenation examples
  - `mixed_libraries.py`: Multiple libraries in one file

### Phase 2: requests Library Support

- [x] **Implement requests detection**: Add to `request_parser.py`:

  - `detect_requests_call(node: nodes.Call) -> bool`: Identify requests library calls
  - Handle `requests.get`, `requests.post`, etc.
  - Handle `session.get`, `session.post` (Session methods)
  - Handle imported functions: `from requests import get`

- [x] **Extract URL from requests calls**: Add helper:

  - `extract_url_from_requests(node: nodes.Call) -> str`: Parse first positional arg or `url=` kwarg
  - Use `infer_literal_value()` from common.ast_utils
  - Handle f-strings and string concatenation
  - Fall back to backtick-wrapped expression if unresolvable

- [x] **Extract method from requests calls**: Add helper:

  - `extract_method_from_requests(node: nodes.Call) -> str`: Determine method from function name
  - Map `requests.get` → "GET", `requests.post` → "POST", etc.
  - Handle session methods the same way

- [x] **Extract parameters from requests calls**: Add helpers:

  - `extract_params_kwarg(node: nodes.Call) -> dict`: Parse `params=` kwarg
  - `extract_headers_kwarg(node: nodes.Call) -> dict`: Parse `headers=` kwarg
  - `extract_json_kwarg(node: nodes.Call) -> dict | None`: Parse `json=` kwarg
  - `extract_data_kwarg(node: nodes.Call) -> dict | None`: Parse `data=` kwarg
  - `extract_timeout_kwarg(node: nodes.Call) -> int | float | None`: Parse `timeout=` kwarg
  - Use astroid inference to resolve dict literals

- [x] **Detect session-based requests calls**: Add helper:

  - `is_requests_session_call(node: nodes.Call) -> bool`: Check if called via requests.Session()
  - Infer type of base object in attribute access
  - Check if type is `requests.Session` or `requests.sessions.Session`

- [x] **Test requests library support**: Write tests in `test_request_parser.py`
  - Test simple GET/POST detection
  - Test URL extraction (literal strings)
  - Test parameter extraction (params, headers, json, data, timeout)
  - Test session-based detection
  - Test imported function detection
  - Verify with `uv run pytest tests/test_http_request_scanner/test_request_parser.py::test_requests*`

### Phase 3: httpx Library Support

- [x] **Implement httpx detection**: Add to `request_parser.py`:

  - `detect_httpx_call(node: nodes.Call) -> bool`: Identify httpx library calls
  - Handle `httpx.get`, `httpx.post`, etc.
  - Handle `client.get`, `client.post` (Client methods)
  - Handle async client methods
  - Handle imported functions

- [x] **Extract httpx parameters**: Reuse requests extraction functions:

  - httpx has compatible API with requests
  - Use same functions: `extract_params_kwarg`, `extract_headers_kwarg`, etc.
  - Only difference: async detection

- [x] **Detect async httpx calls**: Add helper:

  - `is_async_httpx_call(node: nodes.Call) -> bool`: Check if inside async function
  - Traverse up AST to find enclosing FunctionDef
  - Check if FunctionDef has `is_async` flag

- [x] **Detect httpx client-based calls**: Add helper:

  - `is_httpx_client_call(node: nodes.Call) -> bool`: Check if called via Client/AsyncClient
  - Similar to session detection for requests

- [x] **Test httpx library support**: Extend `test_request_parser.py`
  - Test sync httpx detection
  - Test async httpx detection
  - Test client-based detection
  - Test parameter extraction
  - Verify with fixtures/httpx_patterns.py

### Phase 4: aiohttp Library Support

- [x] **Implement aiohttp detection**: Add to `request_parser.py`:

  - `detect_aiohttp_call(node: nodes.Call) -> bool`: Identify aiohttp library calls
  - Handle `session.get`, `session.post` where session is ClientSession
  - Must be inside async function (aiohttp is async-only)

- [x] **Extract URL from aiohttp calls**: Add helper:

  - `extract_url_from_aiohttp(node: nodes.Call) -> str`: Parse first positional arg
  - Same as requests (first arg or `url=` kwarg)

- [x] **Extract method from aiohttp calls**: Add helper:

  - `extract_method_from_aiohttp(node: nodes.Call) -> str`: From method name
  - Map `session.get` → "GET", etc.

- [x] **Extract aiohttp parameters**: Add specific helpers if needed:

  - Most parameters compatible with requests API
  - Special handling for `timeout` (can be aiohttp.ClientTimeout object)
  - For simplicity, extract as numeric value if possible

- [x] **Test aiohttp library support**: Extend `test_request_parser.py`
  - Test async ClientSession detection
  - Test URL and method extraction
  - Test parameter extraction
  - Test timeout handling
  - Verify with fixtures/aiohttp_patterns.py

### Phase 5: urllib3 Library Support

- [x] **Implement urllib3 detection**: Add to `request_parser.py`:

  - `detect_urllib3_call(node: nodes.Call) -> bool`: Identify urllib3 calls
  - Handle `http.request(method, url)` where http is PoolManager
  - Check for attribute access pattern: `something.request(...)`

- [x] **Extract URL and method from urllib3**: Add helpers:

  - `extract_url_from_urllib3(node: nodes.Call) -> str`: Second positional arg
  - `extract_method_from_urllib3(node: nodes.Call) -> str`: First positional arg
  - Note: Order is reversed from requests (method first, URL second)

- [x] **Extract urllib3 parameters**: Add helpers:

  - `extract_fields_kwarg(node: nodes.Call) -> dict`: Parse `fields=` kwarg (query params)
  - Reuse `extract_headers_kwarg` (same name)
  - Parse `body=` kwarg as data

- [x] **Test urllib3 library support**: Extend `test_request_parser.py`
  - Test PoolManager.request() detection
  - Test method and URL extraction (reversed order)
  - Test fields and headers extraction
  - Verify with fixtures/urllib_patterns.py

### Phase 6: urllib.request and http.client Support

- [x] **Implement urllib.request detection**: Add to `request_parser.py`:

  - `detect_urlopen_call(node: nodes.Call) -> bool`: Identify urlopen calls
  - Handle `urlopen(url)` and `urlopen(Request(...))`
  - Parse URL from Request object if used

- [x] **Extract URL from urllib.request**: Add helper:

  - `extract_url_from_urlopen(node: nodes.Call) -> str`: Parse first arg
  - If arg is Request object, recursively parse Request constructor
  - If arg is string, return directly

- [x] **Implement http.client detection**: Add to `request_parser.py`:

  - `detect_http_client_call(node: nodes.Call) -> bool`: Identify conn.request() calls
  - Need to track HTTPConnection/HTTPSConnection instances
  - Extract host from connection constructor
  - Extract path from request() call
  - Reconstruct full URL

- [x] **Extract URL from http.client**: Add helper:

  - `extract_url_from_http_client(node: nodes.Call) -> str`: Reconstruct URL
  - Track connection object: `conn = http.client.HTTPSConnection("example.com")`
  - Track request call: `conn.request("GET", "/path")`
  - Combine: `https://example.com/path` or `http://example.com/path`
  - This requires tracking assignments (more complex)

- [x] **Test urllib.request and http.client support**: Extend `test_request_parser.py`
  - Test urlopen detection with direct URL
  - Test urlopen with Request object
  - Test http.client connection + request pattern
  - Test URL reconstruction for http.client
  - Verify with fixtures

### Phase 7: URL Resolution and Inference

- [x] **Implement URL inference**: Add to `request_parser.py`:

  - `resolve_url(node: nodes.NodeNG) -> str`: Resolve URL using astroid inference
  - Handle string literals (direct return)
  - Handle f-strings with constants
  - Handle string concatenation with constants
  - Handle .format() calls
  - Use `common.ast_utils.infer_literal_value()` with fallback

- [x] **Handle dynamic URLs**: Add fallback logic:

  - When inference fails, wrap in backticks: `` `expression` ``
  - Follow common.ast_utils pattern for unresolvable values
  - Include original AST string representation

- [x] **Test URL resolution**: Write tests in `test_request_parser.py`
  - Test static string URLs
  - Test f-string URLs with constants
  - Test concatenation with constants
  - Test .format() URLs
  - Test unresolvable dynamic URLs (runtime variables)
  - Verify backtick wrapping for dynamic cases
  - Use fixtures/dynamic_urls.py

### Phase 8: Checker Layer (Aggregation)

- [x] **Implement HttpRequestChecker**: Create `checker.py` with:

  - `__init__(self, base_path: Path)`: Initialize with requests dict
  - `visit_call(self, node: nodes.Call) -> None`: Check each call node
  - `check_file(self, file_path: Path) -> None`: Process single file
  - `get_requests_by_url(self) -> dict[str, list[HttpRequest]]`: Return grouped requests
  - `get_summary(self) -> dict`: Calculate statistics

- [x] **Implement call detection logic**: In `visit_call`:

  - Try each library's detection function
  - If match found, extract full HttpRequest
  - Add to self.requests dict grouped by URL
  - Handle multiple libraries in same file

- [x] **Implement summary statistics**: Add to `get_summary`:

  - Count total_requests
  - Count unique_urls (len of dict keys)
  - List libraries_used (unique library names)
  - Count session_based_count
  - Count requests_without_timeout
  - Count async_requests

- [x] **Test checker aggregation**: Write `test_checker.py`
  - Test single-file processing for each library
  - Test multi-file aggregation
  - Test grouping by URL
  - Test summary statistics calculation
  - Test handling of mixed libraries
  - Verify with `uv run pytest tests/test_http_request_scanner/test_checker.py`

### Phase 9: Export Layer (Output Formatting)

- [x] **Implement YAML export functions**: Create `export.py` with:

  - `format_request_output(requests_by_url: dict) -> dict`: Convert to output structure
  - `format_single_usage(request: HttpRequest) -> dict`: Format one usage entry
  - Use `common.export.export_to_yaml` and `export_to_json`
  - Follow formatting standards (2-space indent, UTF-8)

- [x] **Implement output structure**: Format as:

  - Top level: Dict with URLs as keys
  - Each URL entry: `method`, `library`, `usages` list
  - Each usage: `location`, `statement`, `method`, `params`, `headers`, `json_body`, `data`, `timeout`, `session_based`
  - Add `summary` section at top level

- [x] **Handle optional fields**: Format rules:

  - `json_body`: null if not present
  - `data`: null if not present
  - `timeout`: null if not specified
  - `params`: empty dict {} if none
  - `headers`: empty dict {} if none

- [x] **Test YAML export**: Write `test_export.py`
  - Test output structure matches spec examples
  - Test all required and optional fields
  - Test null handling for optional fields
  - Test summary section
  - Test JSON format option
  - Verify with `uv run pytest tests/test_http_request_scanner/test_export.py`

### Phase 10: CLI Layer (Integration)

- [x] **Implement CLI entry point**: Create `cli.py` with:

  - `scan_http_requests(path, output, verbose, include, exclude, format)`: Main function
  - Use `common.file_utils.validate_path()` and `collect_python_files()`
  - Orchestrate HttpRequestChecker
  - Call export functions
  - Error handling and verbose logging

- [x] **Add Click command decorator**: Add CLI decorators:

  - `@click.command()`
  - Path argument with default="."
  - `-o/--output` option for output file
  - `-v/--verbose` flag for debug logging
  - `--include` multiple option for file patterns
  - `--exclude` multiple option for file patterns
  - `--format` option for yaml/json (default=yaml)
  - Follow CLI patterns from other scanners

- [x] **Test CLI functions**: Write `test_cli.py`
  - Test directory scanning
  - Test single file scanning
  - Test output to stdout vs file
  - Test verbose mode
  - Test include/exclude patterns
  - Test format option (yaml vs json)
  - Test error handling (nonexistent path)
  - Use Click's CliRunner for testing
  - Verify with `uv run pytest tests/test_http_request_scanner/test_cli.py`

### Phase 11: Integration Tests

- [x] **Write end-to-end tests**: Create `test_integration.py`

  - Test full scan of fixtures directory
  - Test output correctness for each library
  - Test URL grouping across multiple files
  - Test summary statistics accuracy
  - Test CLI integration with real fixtures
  - Verify complete workflow

- [x] **Test mixed library scenarios**: Add tests for:

  - Multiple libraries in same file
  - Same URL accessed via different libraries
  - Same URL with different methods
  - Dynamic vs static URL resolution

- [x] **Verify test coverage**: Run coverage analysis
  - `uv run pytest tests/test_http_request_scanner/ --cov=upcast.http_request_scanner --cov-report=term-missing`
  - Ensure 85%+ coverage
  - Add tests for any uncovered code paths

### Phase 12: Integration & Documentation

- [x] **Add CLI integration to main**: Update `upcast/main.py`

  - Register `scan-http-requests` command
  - Wire up to `scan_http_requests()` function
  - Add command docstring with examples
  - Follow pattern from other scanner commands

- [x] **Create CLI interface spec delta**: Add `openspec/changes/implement-http-request-scanner/specs/cli-interface/spec.md`

  - Document scan-http-requests command
  - Specify all CLI options
  - Add scenarios for common use cases
  - Mark as ADDED requirement

- [x] **Create http-request-scanner spec**: Add `openspec/changes/implement-http-request-scanner/specs/http-request-scanner/spec.md`

  - Document all requirements
  - Add scenarios for each library
  - Document URL resolution behavior
  - Document output format
  - Include examples

- [x] **Run full test suite**: Execute all tests

  - `uv run pytest tests/test_http_request_scanner/ -v`
  - `uv run pytest` (ensure no regressions)
  - Fix any failing tests

- [x] **Validate code quality**: Ensure compliance

  - Run `uv run ruff check upcast/http_request_scanner/`
  - Fix any linting issues
  - Run pre-commit hooks
  - Verify PEP8 compliance

- [x] **Update README**: Document new scanner capability
  - Add usage examples for CLI
  - Show sample output YAML
  - Explain supported libraries
  - Document URL resolution behavior
  - Link to spec document

## Validation Checkpoints

After each phase:

1. Run relevant tests: `uv run pytest tests/test_http_request_scanner/`
2. Check code style: `uv run ruff check upcast/http_request_scanner/`
3. Verify no regressions: `uv run pytest`

Final validation:

1. End-to-end test with real project containing HTTP requests
2. Verify YAML output matches spec examples
3. Check test coverage: `uv run pytest --cov=upcast.http_request_scanner --cov-report=term-missing`
4. Run OpenSpec validation: `openspec validate implement-http-request-scanner --strict`
