# Implementation Tasks

## Task List

- [ ] **Update HttpRequestUsage model**

  - Remove `location: str` field
  - Add `file: str` field
  - Add `line: int | None` field (with `ge=1` constraint)
  - Update docstring
  - File: `upcast/models/http_requests.py`

- [ ] **Update MetricUsage model**

  - Remove `location: str` field
  - Add `file: str` field
  - Add `line: int | None` field (with `ge=1` constraint)
  - Update docstring
  - File: `upcast/models/metrics.py`

- [ ] **Update HTTP request scanner**

  - Parse location string to extract file and line
  - Pass `file=` and `line=` instead of `location=` when creating `HttpRequestUsage`
  - Handle edge cases (no line number, invalid format)
  - File: `upcast/scanners/http_requests.py`

- [ ] **Update Prometheus metrics scanner**

  - Parse location string to extract file and line
  - Pass `file=` and `line=` instead of `location=` when creating `MetricUsage`
  - Handle edge cases (no line number, invalid format)
  - File: `upcast/scanners/prometheus_metrics.py`

- [ ] **Update HTTP request tests**

  - Update test fixtures to use `file` and `line` fields
  - Update assertions checking location to check `file` and `line` separately
  - Verify scanner output structure
  - Files: `tests/test_http_request_scanner/`

- [ ] **Update Prometheus metrics tests**

  - Update test fixtures to use `file` and `line` fields
  - Update assertions checking location to check `file` and `line` separately
  - Verify scanner output structure
  - Files: `tests/test_prometheus_metrics_scanner/`

- [ ] **Regenerate example outputs**

  - Run `upcast scan-http-requests example/blueking-paas --format yaml > example/scan-results/http-requests.yaml`
  - Run `upcast scan-prometheus-metrics example/blueking-paas --format yaml > example/scan-results/metrics.yaml`
  - Verify outputs have `file` and `line` fields (no `location`)

- [ ] **Run full test suite**

  - Run `uv run pytest tests/ -x`
  - Verify all 285+ tests pass
  - Check for any remaining `location` references

- [ ] **Run integration tests**

  - Test on actual codebase
  - Verify output quality
  - Check JSON and YAML formats

- [ ] **Validate with OpenSpec**
  - Run `openspec validate split-location-field --strict`
  - Address any validation issues

## Dependencies

None - tasks can be done in parallel except:

- Model updates must be done before scanner updates
- Scanner updates must be done before test updates
- All code changes must be done before regenerating examples

## Testing Strategy

1. Unit tests verify model structure
2. Scanner tests verify parsing logic
3. Integration tests verify end-to-end output
4. Example outputs serve as regression tests
