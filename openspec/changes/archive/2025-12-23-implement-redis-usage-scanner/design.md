# Design: implement-redis-usage-scanner

## Architecture Overview

Redis 使用扫描器采用模块化设计，分为配置检测、API 使用检测和模式识别三个主要模块。

```
RedisUsageScanner
├── Configuration Detection
│   ├── Cache Backend (CACHES)
│   ├── Session Storage (SESSION_ENGINE)
│   ├── Celery Broker/Result
│   └── Django Channels (CHANNEL_LAYERS)
├── API Usage Detection
│   ├── Django Cache API
│   ├── Cache Lock API
│   └── Direct redis-py calls
└── Pattern Recognition
    ├── Rate Limiting
    ├── Feature Flags
    └── Key Management
```

## Detection Strategy

### 1. 配置检测 (Configuration Detection)

**目标**: 从 settings.py 提取 Redis 配置

**实现方式**:

- 使用 AST 解析 settings 文件
- 查找特定的配置变量 (CACHES, SESSION_ENGINE, etc.)
- 提取配置字典的键值对
- 识别 Redis 连接 URL 和选项

**关键模式**:

```python
# Pattern 1: django-redis cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        ...
    }
}

# Pattern 2: Session backend
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Pattern 3: Celery
CELERY_BROKER_URL = "redis://localhost:6379/2"

# Pattern 4: Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        ...
    }
}
```

**技术细节**:

- 使用 `astroid` 解析 AST
- 处理字典赋值语句
- 支持多层嵌套字典
- 提取字符串和数字字面量

### 2. API 使用检测 (API Usage Detection)

**目标**: 识别代码中对 Redis API 的调用

**检测分类**:

#### 2.1 Django Cache API

```python
# Import detection
from django.core.cache import cache
from django.core.cache import caches

# Usage patterns
cache.get(key)
cache.set(key, value, timeout)
cache.delete(key)
cache.get_or_set(key, default)
cache.incr(key)
```

**实现**:

- 检测 `cache` 对象的方法调用
- 提取方法名和参数
- 识别 timeout 参数

#### 2.2 Distributed Lock

```python
# Lock patterns
with cache.lock(key, timeout=10):
    ...

lock = cache.lock(key)
lock.acquire()
lock.release()
```

**实现**:

- 识别 `cache.lock()` 调用
- 提取 key 和 timeout
- 区分 context manager 和显式 acquire/release

#### 2.3 Direct redis-py

```python
# Import detection
import redis
from redis import Redis, StrictRedis

# Instance creation
r = redis.Redis(host='localhost', port=6379, db=0)

# Operations
r.get(key)
r.set(key, value, ex=3600)  # with TTL
r.incr(key)
r.zadd(key, mapping)
r.expire(key, seconds)
```

**实现**:

- 检测 redis 模块导入
- 识别 Redis/StrictRedis 实例化
- 追踪实例变量的方法调用
- 检查是否有 TTL 参数 (ex, px, expire)
- 标记没有 TTL 的 set 操作为警告

### 3. 模式识别 (Pattern Recognition)

#### 3.1 Rate Limiting

**Django REST Framework Throttling**:

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

**实现**:

- 检测 REST_FRAMEWORK 配置
- 提取 throttle class 和 rate
- 识别自定义 throttle 类

#### 3.2 Feature Flags

**Common patterns**:

```python
# Pattern 1: Direct cache check
if cache.get("feature:new_ui"):
    ...

# Pattern 2: Default value
enabled = cache.get("feature:beta", False)
```

**实现**:

- 识别 cache.get() 用于布尔判断
- key 匹配 "feature:" 或 "flag:" 前缀
- 标记为 feature_flag 类型

#### 3.3 Key Management

**识别 key 管理问题**:

```python
# Anti-pattern 1: No TTL
r.set("user:data", value)  # ❌ Warning

# Anti-pattern 2: Complex key concatenation
r.get(f"{prefix}:{module}:{id}:{suffix}")  # ❌ Hard to manage

# Good practice: With TTL
r.set("user:data", value, ex=3600)  # ✅ OK
```

**实现**:

- 检测 set 操作是否有 TTL
- 分析 key 的复杂度
- 给出规范建议

## Data Models

### RedisUsageType Enum

```python
class RedisUsageType(str, Enum):
    CACHE_BACKEND = "cache_backend"
    SESSION_STORAGE = "session_storage"
    CELERY_BROKER = "celery_broker"
    CELERY_RESULT = "celery_result"
    CHANNELS = "channels"
    DISTRIBUTED_LOCK = "distributed_lock"
    DIRECT_CLIENT = "direct_client"
    RATE_LIMITING = "rate_limiting"
    FEATURE_FLAGS = "feature_flags"
```

### RedisConfig Model

```python
class RedisConfig(BaseModel):
    """Redis configuration details."""
    backend: str | None = None
    location: str | None = None
    client_class: str | None = None
    db: int | None = None
    host: str | None = None
    port: int | None = None
    options: dict[str, Any] = Field(default_factory=dict)
```

### RedisUsage Model

```python
class RedisUsage(BaseModel):
    """Individual Redis usage record."""
    type: RedisUsageType
    file: str
    line: int
    library: str | None = None
    operation: str | None = None
    statement: str | None = None
    config: RedisConfig | None = None
    has_ttl: bool | None = None
    timeout: int | None = None
    pattern: str | None = None
    warning: str | None = None
```

## Warning System

扫描器会生成以下类型的警告：

| Warning Type         | Description             | Severity |
| -------------------- | ----------------------- | -------- |
| `no_ttl`             | Set 操作未指定 TTL      | High     |
| `no_connection_pool` | 未配置连接池            | Medium   |
| `shared_db`          | Cache 和其他功能共用 DB | Medium   |
| `complex_key`        | Key 拼接过于复杂        | Low      |
| `no_key_prefix`      | 未使用 key 前缀         | Low      |

## Implementation Phases

### Phase 1: Core Infrastructure (Day 1)

- Data models
- Base scanner structure
- Configuration detection

### Phase 2: API Detection (Day 2)

- Django cache API detection
- Direct redis-py detection
- Lock pattern detection

### Phase 3: Pattern Recognition (Day 3)

- Rate limiting detection
- Feature flag detection
- Warning generation

### Phase 4: Integration & Testing (Day 4-5)

- CLI integration
- Unit tests
- Documentation
- Real-world validation

## Testing Strategy

### Unit Tests

1. **Configuration Detection Tests**

   - Test CACHES parsing
   - Test SESSION_ENGINE parsing
   - Test Celery config parsing
   - Test Channels config parsing

2. **API Usage Tests**

   - Test cache.get/set detection
   - Test cache.lock detection
   - Test redis-py detection
   - Test TTL parameter extraction

3. **Pattern Recognition Tests**
   - Test rate limiting detection
   - Test feature flag detection
   - Test warning generation

### Integration Tests

- Run on `example/blueking-paas` project
- Validate output completeness
- Check for false positives/negatives

## Performance Considerations

- **File Filtering**: 优先扫描 settings/ 和常见配置文件
- **Lazy Parsing**: 只解析包含 Redis 相关导入的文件
- **Caching**: 缓存导入信息避免重复解析
- **Parallel Processing**: 可并行扫描不同文件（未来优化）

## Edge Cases

1. **Dynamic Configuration**: `CACHES = get_cache_config()` → 标记为 dynamic
2. **Conditional Config**: `if DEBUG: CACHES = ...` → 记录条件
3. **Complex Key**: `f"{a}:{b}:{c}"` → 简化为 `...`
4. **Indirect Usage**: 第三方库内部使用 → 标记为 indirect（超出范围）

## Extension Points

未来可扩展的功能：

1. **Connection Pool Analysis**: 分析连接池配置的合理性
2. **Key Pattern Statistics**: 统计 key 前缀和模式分布
3. **Redis Version Compatibility**: 检查使用的命令与 Redis 版本的兼容性
4. **Performance Recommendations**: 基于使用模式给出性能优化建议
5. **Migration Guidance**: 为 Redis 迁移提供指导
