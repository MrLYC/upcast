# Redis 使用扫描器 (redis-usage)

## 概述

Redis 使用扫描器用于分析 Django 项目中的 Redis 使用模式。它能够检测缓存配置、Session 存储、Celery broker/result backend、Django Channels、分布式锁、直接 redis-py 使用等场景。

该扫描器对于以下场景特别有用：

- 审查 Redis 使用情况
- 识别缓存策略
- 分析 Redis 配置
- 优化 Redis 使用
- 迁移和架构规划

## 命令使用

```bash
upcast scan-redis-usage [OPTIONS] [PATH]
```

### 参数

- `PATH` - 要扫描的 Python 文件或目录路径（可选，默认为当前目录 `.`）

### 选项

- `-o, --output PATH` - 输出文件路径
- `-v, --verbose` - 启用详细输出
- `--format [yaml|json|markdown]` - 输出格式（默认：yaml）
- `--markdown-language [en|zh]` - Markdown 输出语言（默认：zh）
- `--markdown-title TEXT` - Markdown 输出标题
- `--include PATTERN` - 包含的文件模式（可多次指定）
- `--exclude PATTERN` - 排除的文件模式（可多次指定）
- `--no-default-excludes` - 禁用默认排除模式

### 使用示例

```bash
# 扫描当前目录
upcast scan-redis-usage .

# 启用详细模式
upcast scan-redis-usage ./myproject -v

# 保存结果到文件
upcast scan-redis-usage ./src -o redis.yaml

# 输出为 JSON 格式
upcast scan-redis-usage ./app --format json
```

## 字段说明

### metadata 字段

存放扫描命令的参数和配置信息。

| 字段名       | 类型          | 必填 | 说明               |
| ------------ | ------------- | ---- | ------------------ |
| scanner_name | string        | 是   | 扫描器名称         |
| command_args | array[string] | 否   | 扫描命令的参数列表 |

### summary 字段

`summary` 包含扫描统计信息。

| 字段名           | 类型                 | 必填 | 说明                 |
| ---------------- | -------------------- | ---- | -------------------- |
| total_usages     | integer              | 是   | Redis 使用总数       |
| categories       | map[string, integer] | 是   | 按类别统计的使用数量 |
| files_scanned    | integer              | 是   | 扫描的文件总数       |
| scan_duration_ms | integer              | 是   | 扫描耗时（毫秒）     |
| total_count      | integer              | 是   | Redis 使用总数       |

### results 字段

`results` 是一个对象，健为推导的 Redis 键的模式（无法推导的部位使用 `...`），值为对应的使用对象列表。

#### Redis 使用对象

| 字段名    | 类型                | 必填 | 说明                                                                |
| --------- | ------------------- | ---- | ------------------------------------------------------------------- |
| type      | string              | 是   | 使用类型（如 `cache_backend`, `redis_client`，`redis_pipeline` 等） |
| key       | string/null         | 是   | 推导出的Redis 键名                                                  |
| file      | string              | 是   | 文件路径                                                            |
| line      | integer             | 是   | 行号                                                                |
| statement | string              | 是   | 完整语句                                                            |
| library   | string              | 是   | 使用的库（`redis`, `django_redis`, `redis-py` 等）                  |
| operation | string/null         | 是   | 操作类型（`get`, `set`, `delete` 等；未识别为 `null`）              |
| args      | array[string]       | 否   | 操作参数列表                                                        |
| kwargs    | map[string, string] | 否   | 操作关键字参数                                                      |

## 使用示例

以下是扫描结果的示例：

```yaml
metadata:
  scanner_name: redis-usage
  command_args:
    - scan-redis-usage
    - /path/to/project
    - --format
    - yaml

summary:
  total_usages: 8
  categories:
    cache_backend: 2
    celery_broker: 1
    celery_result: 1
    redis_client: 2
    redis_pipeline: 1
    distributed_lock: 1
  files_scanned: 45
  scan_duration_ms: 1234
  total_count: 8

results:
  "cache:view:...":
    - type: cache_backend
      key: "cache:view:{home}"
      file: myapp/views.py
      line: 15
      statement: "cache.get(f'cache:view:{home}')"
      library: django_redis
      operation: null
      args:
        - "f'cache:view:{home}'"
      kwargs: {}
    - type: cache_backend
      key: "cache:view:{profile}"
      file: myapp/views.py
      line: 28
      statement: "cache.set(f'cache:view:{profile}', data, 300)"
      library: django_redis
      operation: set
      args:
        - "'cache:view:profile'"
        - "data"
        - "300"
      kwargs: {}
  "user:session:abc123":
    - type: redis_client
      key: "user:session:abc123"
      file: myapp/auth.py
      line: 42
      statement: "redis_client.get(f'user:session:{session_id}')"
      library: redis
      operation: get
      args:
        - "f'user:session:{session_id}'"
      kwargs: {}

  "metrics:api_calls":
    - type: redis_client
      key: "metrics:api_calls"
      file: myapp/metrics.py
      line: 67
      statement: "redis_client.incr('metrics:api_calls')"
      library: redis
      operation: incr
      args:
        - "'metrics:api_calls'"
      kwargs: {}
```

## 注意事项

1. **使用类型说明**：

   **cache_backend（缓存后端）**：

   - Django CACHES 配置
   - django-redis 后端
   - `cache.get()`, `cache.set()` 等
   - 用于视图缓存、模板片段缓存等

   **redis_client（直接客户端）**：

   - 直接使用 Redis 客户端
   - `client.get()`, `client.set()` 等
   - 自定义缓存逻辑

2. **键名识别**：`key` 字段记录 Redis 键名模式：

   - 如果能推导出具体键名，则显示具体名称
   - 如果有变量部分，则使用通配符 `...` 表示，如 `f"user:profile:{user_id}"` 显示为 `user:profile:...`
   - 如果有连续的变量部分，则使用单个 `...` 表示，如 `f"session:{user_id}{session_id}"` 显示为 `session:...`

3. **库识别** - `library` 字段标识使用的库：

   - `redis` - redis-py
   - `django_redis` - django-redis
   - `aioredis` - 异步 Redis 客户端
   - `redis-py-cluster` - Redis 集群客户端

4. **操作类型** - `operation` 识别常见操作：

   - `get` - 获取值
   - `set` - 设置值
   - `delete` - 删除键
   - `incr` / `decr` - 计数器操作
   - `expire` - 设置过期时间
   - `lpush` / `rpush` - 列表操作
   - `sadd` - 集合操作
   - `zadd` - 有序集合操作
   - `hset` / `hget` - 哈希操作
   - `hgetall` - 获取哈希所有字段
