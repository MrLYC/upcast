# Project Analysis Report

Generated from static code analysis scan results.

## Executive Summary

- **Total Files Scanned**: 8205
- **Total Findings**: 4246
- **Scan Types**: 13

## Code Quality Analysis

### Cyclomatic Complexity

- **High Complexity Functions**: 88
- **By Severity**:
  - Acceptable: 33
  - Critical: 2
  - High Risk: 10
  - Warning: 43

#### Top 5 Most Complex Functions

- **test_save** (Complexity: 21, apiserver/paasng/tests/api/bkapp_model/test_bkapp_model.py)

- **test_integrated** (Complexity: 21, apiserver/paasng/tests/paasng/platform/bkapp_model/entities_syncer/test_processes.py)

- **_migrate_single** (Complexity: 20, apiserver/paasng/paasng/infras/iam/members/management/commands/migrate_bkpaas3_perm.py)
  - 迁移单个应用权限数据

- **testlist_gen_cnative_process_specs** (Complexity: 20, apiserver/paasng/tests/paas_wl/bk_app/processes/test_processes.py)

- **test_release_version** (Complexity: 18, apiserver/paasng/tests/paasng/bk_plugins/pluginscenter/test_integration.py)

### Blocking Operations

- **Total Operations**: 33
- **By Category**:
  - Database: 5
  - Time Based: 28

## Architecture & Patterns

### Django Models

- **Total Models**: 167
- **Total Fields**: 684
- **Total Relationships**: 148

### Django URL Patterns

- **Total URL Patterns**: 533
- **URL Configuration Files**: 59

### Concurrency Patterns

- **Total Patterns**: 4
- **By Category**:
  - Multiprocessing: 1
  - Threading: 3

### Signal Usage

- **Total Signals**: 39
- **Django Receivers**: 54
- **Celery Receivers**: 1

## Infrastructure

### Environment Variables

- **Total Variables**: 9
- **Required Variables**: 6
- **Optional Variables**: 3

### Redis Usage

- **Total Usages**: 5
- **By Category**:
  - Celery Broker: 1
  - Celery Result: 1
  - Direct Client: 3

### Prometheus Metrics

- **Total Metrics**: 42
- **By Type**:
  - Counter: 7
  - Gauge: 33
  - Histogram: 2

### Django Settings

- **Total Settings**: 474
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
- **By Library**:
  - requests: 56