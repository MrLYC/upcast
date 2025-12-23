# redis-usage-scanner Specification

## Purpose

Provide comprehensive static analysis of Redis usage patterns in Django projects, including configuration detection, API usage tracking, and best practice validation.

## ADDED Requirements

### Requirement: Django Cache Backend Detection

The system SHALL detect Django cache configurations using Redis as the backend.

#### Scenario: django-redis cache backend

- **WHEN** settings contain:
  ```python
  CACHES = {
      "default": {
          "BACKEND": "django_redis.cache.RedisCache",
          "LOCATION": "redis://127.0.0.1:6379/1",
          "OPTIONS": {
              "CLIENT_CLASS": "django_redis.client.DefaultClient",
          }
      }
  }
  ```
- **THEN** the system SHALL identify this as `cache_backend` usage
- **AND** extract backend as "django_redis.cache.RedisCache"
- **AND** extract location as "redis://127.0.0.1:6379/1"
- **AND** extract client_class as "django_redis.client.DefaultClient"
- **AND** record the file and line number

#### Scenario: Multiple cache backends

- **WHEN** settings define multiple CACHES entries
- **THEN** the system SHALL detect each cache backend separately
- **AND** identify which ones use Redis
- **AND** record cache alias names

---

### Requirement: Session Storage Detection

The system SHALL detect when Django uses Redis for session storage.

#### Scenario: Cache-based session backend

- **WHEN** settings contain `SESSION_ENGINE = "django.contrib.sessions.backends.cache"`
- **THEN** the system SHALL identify this as `session_storage` usage
- **AND** extract the session engine value
- **AND** extract SESSION_CACHE_ALIAS if specified

#### Scenario: Cache-DB hybrid session

- **WHEN** settings contain `SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"`
- **THEN** the system SHALL identify this as `session_storage` with fallback to DB
- **AND** record the hybrid nature in the output

---

### Requirement: Celery Broker Detection

The system SHALL detect Celery configurations using Redis as the message broker.

#### Scenario: Celery broker URL

- **WHEN** settings contain `CELERY_BROKER_URL = "redis://127.0.0.1:6379/2"`
- **THEN** the system SHALL identify this as `celery_broker` usage
- **AND** extract the broker URL
- **AND** parse host, port, and db from the URL

#### Scenario: Legacy Celery configuration

- **WHEN** settings use `BROKER_URL` instead of `CELERY_BROKER_URL`
- **THEN** the system SHALL still detect it as Celery broker
- **AND** note the legacy configuration style

---

### Requirement: Celery Result Backend Detection

The system SHALL detect Celery result backend configurations using Redis.

#### Scenario: Celery result backend

- **WHEN** settings contain `CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/3"`
- **THEN** the system SHALL identify this as `celery_result` usage
- **AND** extract the result backend URL
- **AND** check for result expiration settings

#### Scenario: Missing result TTL

- **WHEN** Celery result backend is configured without `CELERY_RESULT_EXPIRES`
- **THEN** the system SHALL generate a warning about potential memory issues
- **AND** recommend setting an expiration time

---

### Requirement: Django Channels Detection

The system SHALL detect Django Channels configurations using Redis for channel layers.

#### Scenario: channels-redis configuration

- **WHEN** settings contain:
  ```python
  CHANNEL_LAYERS = {
      "default": {
          "BACKEND": "channels_redis.core.RedisChannelLayer",
          "CONFIG": {
              "hosts": [("127.0.0.1", 6379)],
          },
      },
  }
  ```
- **THEN** the system SHALL identify this as `channels` usage
- **AND** extract the backend class
- **AND** extract host and port from CONFIG

---

### Requirement: Django Cache API Usage Detection

The system SHALL detect usage of Django's cache API in application code.

#### Scenario: cache.get() detection

- **WHEN** code contains `cache.get('user:123')`
- **THEN** the system SHALL identify this as cache API usage
- **AND** extract the operation as "get"
- **AND** record the file and line number

#### Scenario: cache.set() with timeout

- **WHEN** code contains `cache.set('key', 'value', timeout=3600)`
- **THEN** the system SHALL extract operation as "set"
- **AND** extract timeout as 3600
- **AND** record has_ttl as true

#### Scenario: cache.set() without timeout

- **WHEN** code contains `cache.set('key', 'value')`
- **THEN** the system SHALL extract operation as "set"
- **AND** record has_ttl as false
- **AND** generate a warning about missing TTL

---

### Requirement: Distributed Lock Detection

The system SHALL detect distributed lock patterns using Redis.

#### Scenario: cache.lock() context manager

- **WHEN** code contains:
  ```python
  with cache.lock("order:123", timeout=10):
      process_order()
  ```
- **THEN** the system SHALL identify this as `distributed_lock` usage
- **AND** extract lock key as "order:123"
- **AND** extract timeout as 10
- **AND** record pattern as "cache_lock"

#### Scenario: Explicit lock acquire/release

- **WHEN** code contains:
  ```python
  lock = cache.lock("resource")
  lock.acquire()
  # ... do work ...
  lock.release()
  ```
- **THEN** the system SHALL identify this as distributed lock usage
- **AND** note the explicit acquire/release pattern

---

### Requirement: Direct redis-py Usage Detection

The system SHALL detect direct usage of the redis-py library.

#### Scenario: Redis client instantiation

- **WHEN** code contains `r = redis.Redis(host='localhost', port=6379, db=0)`
- **THEN** the system SHALL identify this as `direct_client` usage
- **AND** extract library as "redis"
- **AND** extract connection parameters

#### Scenario: Redis SET operation with TTL

- **WHEN** code contains `r.set('key', 'value', ex=3600)`
- **THEN** the system SHALL extract operation as "set"
- **AND** extract TTL parameter (ex=3600)
- **AND** record has_ttl as true

#### Scenario: Redis SET operation without TTL

- **WHEN** code contains `r.set('key', 'value')`
- **THEN** the system SHALL extract operation as "set"
- **AND** record has_ttl as false
- **AND** generate warning "No TTL specified for key"

#### Scenario: Redis INCR operation

- **WHEN** code contains `r.incr('counter')`
- **THEN** the system SHALL extract operation as "incr"
- **AND** record has_ttl as false
- **AND** generate warning about missing TTL for counter

#### Scenario: Redis ZADD for ranking

- **WHEN** code contains `r.zadd('leaderboard', {'user1': 100})`
- **THEN** the system SHALL extract operation as "zadd"
- **AND** identify the pattern as ranking/leaderboard

---

### Requirement: Rate Limiting Detection

The system SHALL detect rate limiting configurations using Redis.

#### Scenario: DRF throttling configuration

- **WHEN** settings contain:
  ```python
  REST_FRAMEWORK = {
      "DEFAULT_THROTTLE_CLASSES": [
          "rest_framework.throttling.UserRateThrottle",
      ],
      "DEFAULT_THROTTLE_RATES": {
          "user": "100/min",
      }
  }
  ```
- **THEN** the system SHALL identify this as `rate_limiting` usage
- **AND** extract throttle class
- **AND** extract rate as "100/min"
- **AND** note that this uses Redis cache backend

---

### Requirement: Feature Flag Detection

The system SHALL detect feature flag patterns using Redis cache.

#### Scenario: Boolean feature flag check

- **WHEN** code contains `if cache.get("feature:new_ui"):`
- **THEN** the system SHALL identify this as `feature_flags` usage
- **AND** extract feature flag key
- **AND** record the pattern as boolean check

#### Scenario: Feature flag with default

- **WHEN** code contains `enabled = cache.get("feature:beta", False)`
- **THEN** the system SHALL identify this as feature flag
- **AND** extract default value as False

---

### Requirement: Warning Generation for Best Practices

The system SHALL generate warnings for common Redis anti-patterns.

#### Scenario: SET without TTL warning

- **WHEN** detecting `cache.set()` or `r.set()` without timeout/TTL
- **THEN** the system SHALL generate warning with severity "High"
- **AND** message "No TTL specified for key"

#### Scenario: Shared DB warning

- **WHEN** multiple Redis usage types use the same DB number
- **THEN** the system SHALL generate warning about potential key conflicts
- **AND** recommend using separate DBs for different purposes

#### Scenario: No connection pool warning

- **WHEN** detecting direct Redis() instantiation without connection pool
- **THEN** the system SHALL generate warning with severity "Medium"
- **AND** recommend using connection pooling

---

### Requirement: Output Format and Aggregation

The system SHALL produce structured output grouped by usage type.

#### Scenario: Summary statistics

- **WHEN** scanning is complete
- **THEN** output.summary SHALL contain:
  - total_usages: total count of Redis usages
  - categories: count per usage type
  - files_scanned: number of files analyzed
  - scan_duration_ms: scan time in milliseconds
  - warnings: list of generated warnings

#### Scenario: Results grouped by type

- **WHEN** multiple usages are detected
- **THEN** output.results SHALL group usages by type (cache_backend, session_storage, etc.)
- **AND** each usage SHALL include file, line, statement, and extracted parameters

---

### Requirement: Dynamic Configuration Handling

The system SHALL handle dynamic Redis configurations gracefully.

#### Scenario: Function-based configuration

- **WHEN** settings contain `CACHES = get_redis_config()`
- **THEN** the system SHALL identify this as dynamic configuration
- **AND** record the function call
- **AND** mark config fields as "dynamic"

#### Scenario: Environment-based configuration

- **WHEN** settings contain `CELERY_BROKER_URL = os.getenv('REDIS_URL')`
- **THEN** the system SHALL extract the environment variable name
- **AND** note that the actual value is runtime-dependent
