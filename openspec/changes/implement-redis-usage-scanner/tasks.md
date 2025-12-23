# Tasks: implement-redis-usage-scanner

## Task List

### 1. 📋 Create Data Models

Create Pydantic models for Redis usage output in `upcast/models/redis_usage.py`.

**Deliverables:**

- `RedisUsageType` enum with 9 usage types
- `RedisConfig` model for configuration info
- `RedisUsage` model for individual usage records
- `RedisUsageSummary` extending `ScannerSummary`
- `RedisUsageOutput` extending `ScannerOutput`

**Validation:**

- All models have proper type annotations
- Fields have validation constraints
- Models serialize correctly to YAML/JSON

---

### 2. 🔍 Implement Configuration Scanner

Implement settings.py scanning to detect Redis configurations.

**Deliverables:**

- Method `_scan_settings_file()` to detect:
  - `CACHES` configuration (django-redis)
  - `SESSION_ENGINE` configuration
  - `CELERY_BROKER_URL` configuration
  - `CELERY_RESULT_BACKEND` configuration
  - `CHANNEL_LAYERS` configuration
- Extract connection URLs, client classes, options

**Validation:**

- Correctly parses dict-based configurations
- Handles string URLs and dict configs
- Extracts all relevant config fields

---

### 3. 🎯 Implement Cache API Usage Scanner

Scan for Django cache API usage in code.

**Deliverables:**

- Detect `cache.get()`, `cache.set()`, `cache.delete()` calls
- Detect `cache.lock()` for distributed locks
- Detect `from django.core.cache import cache`
- Extract timeout/TTL parameters

**Validation:**

- Identifies all cache API calls
- Correctly extracts method parameters
- Distinguishes lock usage from regular cache operations

---

### 4. 🚀 Implement Direct Redis Client Scanner

Scan for direct redis-py usage.

**Deliverables:**

- Detect `redis.Redis()` instantiation
- Detect `redis.StrictRedis()` usage
- Identify common operations (get, set, incr, zadd, etc.)
- Check for TTL/EXPIRE usage
- Flag operations without TTL as warnings

**Validation:**

- Detects all redis-py operations
- Correctly identifies operations without TTL
- Generates appropriate warnings

---

### 5. 📊 Implement Pattern Detection

Implement detection for advanced patterns.

**Deliverables:**

- Rate limiting pattern detection (DRF throttling)
- Feature flag pattern detection (cache-based)
- Connection pool configuration detection
- Key naming pattern analysis

**Validation:**

- Correctly identifies throttling configurations
- Detects feature flag usage patterns
- Extracts connection pool settings

---

### 6. 🏗️ Implement Main Scanner Class

Create `RedisUsageScanner` class extending `BaseScanner`.

**Deliverables:**

- `RedisUsageScanner` class in `upcast/scanners/redis_usage.py`
- Implements `scan()` method
- Aggregates results from all detection methods
- Generates summary with statistics and warnings

**Validation:**

- Scanner follows BaseScanner pattern
- Correctly aggregates all usage types
- Summary contains accurate counts and warnings

---

### 7. 🧪 Write Unit Tests

Create comprehensive test suite.

**Deliverables:**

- `tests/test_scanners/test_redis_usage.py`
- Test samples for each Redis usage type
- Tests for configuration detection
- Tests for API usage detection
- Tests for direct client detection
- Tests for warning generation
- Edge case tests (dynamic config, complex key patterns)

**Validation:**

- All tests pass
- Coverage ≥ 80%
- Edge cases covered

---

### 8. 🔗 Integrate with CLI

Add CLI command for the new scanner.

**Deliverables:**

- Add `scan-redis-usage` command in `upcast/main.py`
- Follow existing CLI patterns
- Support standard options (--output, --format, --include, --exclude)

**Validation:**

- Command appears in `upcast --help`
- Can scan example project successfully
- Output format is correct

---

### 9. 📝 Update Documentation

Update README and add example output.

**Deliverables:**

- Add scanner section in README.md
- Include usage examples
- Add key features list
- Create `example/scan-results/redis-usage.yaml` from blueking-paas scan

**Validation:**

- Documentation is clear and complete
- Example output is accurate
- Follows existing documentation style

---

### 10. ✅ Integration Testing

Run on real project and validate output.

**Deliverables:**

- Run on `example/blueking-paas` project
- Verify all Redis usages are detected
- Check warning accuracy
- Validate output quality

**Validation:**

- No false positives
- No major false negatives
- Warnings are actionable
- Output is useful for analysis

---

### 11. 📐 Create Spec Delta

Create specification for the new scanner.

**Deliverables:**

- `openspec/changes/implement-redis-usage-scanner/specs/redis-usage-scanner/spec.md`
- Define all requirements with scenarios
- Document detection patterns
- Specify output format

**Validation:**

- All requirements have scenarios
- Scenarios are testable
- Specification is complete

---

## Task Dependencies

```
1 (Models) → 6 (Scanner Class)
2 (Config Scanner) → 6 (Scanner Class)
3 (Cache API Scanner) → 6 (Scanner Class)
4 (Direct Client Scanner) → 6 (Scanner Class)
5 (Pattern Detection) → 6 (Scanner Class)
6 (Scanner Class) → 7 (Tests)
6 (Scanner Class) → 8 (CLI)
8 (CLI) → 9 (Documentation)
9 (Documentation) → 10 (Integration Testing)
```

## Parallelizable Work

- Tasks 2, 3, 4, 5 can be developed in parallel after Task 1
- Tasks 8 and 9 can be done in parallel after Task 6
- Task 11 (Spec) can be written alongside implementation

## Estimated Timeline

- **Phase 1**: Models + Config Scanner (Day 1)
- **Phase 2**: Cache API + Direct Client + Patterns (Day 2)
- **Phase 3**: Scanner Class + Tests (Day 3)
- **Phase 4**: CLI + Docs + Integration (Day 4)
- **Phase 5**: Spec + Polish (Day 5)
