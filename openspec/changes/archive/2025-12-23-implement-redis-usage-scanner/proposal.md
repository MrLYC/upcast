# Proposal: implement-redis-usage-scanner

## Problem Statement

Django 项目中 Redis 的使用方式多样且复杂，包括缓存、会话存储、Celery 队列、分布式锁、实时通信等多个场景。目前缺乏工具来系统性地分析项目中 Redis 的使用模式、配置方式和潜在问题。开发者需要手动检查代码来了解：

- Redis 在哪些地方被使用
- 使用了哪些 Redis 功能和模式
- 是否存在不规范的使用（如缺少 TTL、key 管理混乱）
- 不同使用场景是否正确配置

## Proposed Solution

实现一个 Redis 使用扫描器 (`scan-redis-usage`)，通过静态分析识别 Django 项目中所有 Redis 使用方式，分类汇总并提供规范性建议。

### 扫描范围

扫描器将识别以下 9 种主要的 Redis 使用模式：

1. **Cache Backend** - Django cache 配置和使用
2. **Session Storage** - Django session 使用 Redis
3. **Celery Broker** - Celery 任务队列
4. **Celery Result Backend** - Celery 任务结果存储
5. **Django Channels** - Channel Layer 配置
6. **Distributed Lock** - 分布式锁实现
7. **Direct Redis Client** - 直接使用 redis-py
8. **Rate Limiting** - 限流实现
9. **Feature Flags** - 配置开关存储

### 检测方式

- **配置检测**: 扫描 settings.py 中的 Redis 配置
- **代码使用检测**: 扫描代码中的 Redis API 调用
- **模式识别**: 识别常见的使用模式和反模式

### 输出格式

```yaml
summary:
  total_usages: 25
  categories:
    cache_backend: 1
    session_storage: 1
    celery_broker: 1
    celery_result: 1
    channels: 0
    distributed_lock: 3
    direct_client: 15
    rate_limiting: 2
    feature_flags: 1
  files_scanned: 45
  scan_duration_ms: 320
  warnings:
    - "Direct Redis usage without TTL in cache/manager.py:45"
    - "No connection pool configuration for direct Redis client"

results:
  cache_backend:
    - type: cache_backend
      library: django_redis
      file: settings/base.py
      line: 120
      config:
        backend: django_redis.cache.RedisCache
        location: redis://127.0.0.1:6379/1
        client_class: django_redis.client.DefaultClient

  session_storage:
    - type: session_storage
      file: settings/base.py
      line: 145
      config:
        engine: django.contrib.sessions.backends.cache
        cache_alias: default

  celery_broker:
    - type: celery_broker
      file: settings/celery.py
      line: 15
      config:
        broker_url: redis://127.0.0.1:6379/2

  distributed_lock:
    - type: distributed_lock
      file: services/order.py
      line: 67
      pattern: cache_lock
      statement: "with cache.lock('order:123', timeout=10):"
      timeout: 10

  direct_client:
    - type: direct_client
      file: utils/counter.py
      line: 23
      library: redis
      operation: incr
      statement: "r.incr('counter')"
      has_ttl: false
      warning: "No TTL specified for key"

    - type: direct_client
      file: services/ranking.py
      line: 45
      library: redis
      operation: zadd
      statement: "r.zadd('rank', {'user1': 100})"
      has_ttl: false

  rate_limiting:
    - type: rate_limiting
      file: api/throttling.py
      line: 12
      framework: drf
      config:
        throttle_class: UserRateThrottle
        rate: "100/min"
```

## Benefits

1. **可见性**: 全面了解项目中 Redis 的使用情况
2. **规范检查**: 识别不规范使用（缺少 TTL、key 冲突风险等）
3. **迁移辅助**: 为 Redis 迁移或重构提供清晰的依赖关系
4. **性能优化**: 识别潜在的性能问题（连接池配置、过度使用等）
5. **文档生成**: 自动生成 Redis 使用文档

## Risks & Mitigations

| Risk                    | Mitigation                                      |
| ----------------------- | ----------------------------------------------- |
| 动态配置难以检测        | 标记为 `dynamic_config`，提供部分信息           |
| 复杂的 key 拼接难以解析 | 保留原始语句，使用 `...` 占位符                 |
| 第三方库的间接使用      | 重点关注直接使用，第三方库使用标记为 `indirect` |
| 配置分散在多个文件      | 扫描所有 settings 文件和配置模块                |

## Scope

### In Scope

- Django settings 中的 Redis 配置检测
- Django cache API 使用检测
- Celery Redis 配置检测
- django-redis 使用检测
- redis-py 直接使用检测
- Django Channels Redis 配置检测
- 分布式锁模式识别
- 常见反模式识别（无 TTL、key 冲突等）

### Out of Scope

- Redis 服务器性能分析
- 运行时 key 统计
- Redis 数据内容分析
- Redis 集群拓扑分析
- 非 Django 框架的 Redis 使用

## Success Criteria

- [ ] 正确识别 9 种主要 Redis 使用模式
- [ ] 准确提取配置信息（location, db, client_class 等）
- [ ] 识别常见反模式并给出警告
- [ ] 输出格式清晰，易于理解
- [ ] 在 blueking-paas 示例项目上测试通过
- [ ] 单元测试覆盖率 ≥ 80%
- [ ] README 文档完整，包含使用示例

## Dependencies

- 依赖现有的 `upcast.common` 工具包
- 依赖 `BaseScanner` 基类
- 需要创建新的 Pydantic 模型 (`upcast.models.redis_usage`)

## Estimated Effort

- Scanner 实现: 2-3 天
- 测试编写: 1 天
- 文档更新: 0.5 天
- 集成验证: 0.5 天

**Total**: 4-5 天
