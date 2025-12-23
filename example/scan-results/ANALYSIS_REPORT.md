# Project Analysis Report

Generated from static code analysis scan results.

## Executive Summary

- **Total Files Scanned**: 8205
- **Total Findings**: 4246
- **Scan Types**: 13

## Code Quality Analysis

### Cyclomatic Complexity

- **High Complexity Functions**: 88
- **Files Analyzed**: 75
- **By Severity**:
  - Acceptable: 33
  - Critical: 2
  - High Risk: 10
  - Warning: 43

#### Top 5 Most Complex Functions

- **test_save** (Complexity: 21, Severity: critical)
  - File: `apiserver/paasng/tests/api/bkapp_model/test_bkapp_model.py:79`

- **test_integrated** (Complexity: 21, Severity: critical)
  - File: `apiserver/paasng/tests/paasng/platform/bkapp_model/entities_syncer/test_processes.py:37`

- **_migrate_single** (Complexity: 20, Severity: high_risk)
  - File: `apiserver/paasng/paasng/infras/iam/members/management/commands/migrate_bkpaas3_perm.py:144`
  - Description: 迁移单个应用权限数据

- **testlist_gen_cnative_process_specs** (Complexity: 20, Severity: high_risk)
  - File: `apiserver/paasng/tests/paas_wl/bk_app/processes/test_processes.py:35`

- **test_release_version** (Complexity: 18, Severity: high_risk)
  - File: `apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/test_integration.py:182`

### Blocking Operations

- **Total Operations**: 33
- **Files Scanned**: 21
- **By Category**:
  - Database: 5
  - Time Based: 28

**Recommendations:**
- Consider using async alternatives for blocking I/O operations
- Review time.sleep() calls in async contexts
- Optimize database queries with select_for_update()

## Architecture & Patterns

### Django Models

- **Total Models**: 167
- **Total Fields**: 684
- **Total Relationships**: 148
- **Files Scanned**: 167
- **Average Fields per Model**: 4.1

### Django URL Patterns

- **Total URL Patterns**: 533
- **URL Configuration Files**: 59
- **Path Patterns**: 99
- **Include Patterns**: 58

### Concurrency Patterns

- **Total Patterns**: 4
- **Files Scanned**: 4
- **By Category**:
  - Multiprocessing: 1
  - Threading: 3

**Note:** Consider using asyncio for I/O-bound operations to improve performance.

### Signal Usage

- **Total Signals**: 39
- **Files Scanned**: 2368
- **Django Receivers**: 54
- **Celery Receivers**: 1
- **Custom Signals Defined**: 20

## Infrastructure

### Environment Variables

- **Total Variables**: 9
- **Required Variables**: 6
- **Optional Variables**: 3

**Critical Required Variables:**
- `DATABASE_URL`
- `OAUTHLIB_INSECURE_TRANSPORT`
- `OAUTHLIB_RELAX_TOKEN_SCOPE`
- `PAAS_WL_CLUSTER_API_SERVER_URLS`
- `PAAS_WL_CLUSTER_ENABLED_HTTPS_BY_DEFAULT`
- `prometheus_multiproc_dir`

### Redis Usage

- **Total Usages**: 5
- **Files Scanned**: 3
- **By Category**:
  - Celery Broker: 1
  - Celery Result: 1
  - Direct Client: 3

### Prometheus Metrics

- **Total Metrics**: 42
- **Files Scanned**: 5
- **By Type**:
  - Counter: 7
  - Gauge: 33
  - Histogram: 2

### Django Settings

- **Total Settings References**: 474
- **Files Scanned**: 2368

## Testing & Reliability

### Unit Tests

- **Total Test Files**: 0
- **Total Tests**: 1607

### Exception Handlers

- **Total Handlers**: 1189
- **Files Scanned**: 422

## External Dependencies

### HTTP Requests

- **Total Requests**: 56
- **Unique URLs**: 8
- **Files Scanned**: 14
- **By Library**:
  - requests: 56

**Top External APIs:**
- `https://example.com/api` (3 calls)
- `https://example.com/api?BK_PASSWORD=123456&api_key=abcdef` (1 calls)