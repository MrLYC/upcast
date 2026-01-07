# Prometheus 监控指标扫描器 (metrics)

## 概述

Prometheus 监控指标扫描器用于分析 Python 代码中的 Prometheus 指标定义。它能够检测 Counter、Gauge、Histogram、Summary 等指标类型，提取指标名称、标签、帮助文本等信息。

该扫描器对于以下场景特别有用：

- 生成监控指标文档
- 审查指标命名规范
- 识别重复或冲突的指标
- 监控覆盖度分析
- 指标标准化

## 命令使用

```bash
upcast scan-metrics [OPTIONS] [PATH]
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
upcast scan-metrics .

# 保存结果到文件
upcast scan-metrics ./src --output metrics.yaml

# 输出为 JSON 格式
upcast scan-metrics ./app --format json

# 仅扫描监控相关文件
upcast scan-metrics . --include "**/metrics.py" --include "**/monitoring/**"
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
| total_metrics    | integer              | 是   | 指标总数             |
| by_type          | map[string, integer] | 是   | 按指标类型分组的数量 |
| files_scanned    | integer              | 是   | 扫描的文件总数       |
| scan_duration_ms | integer              | 是   | 扫描耗时（毫秒）     |
| total_count      | integer              | 是   | 指标总数             |

### results 字段

`results` 是一个字典，键为指标名称，值为指标详细信息。

#### 指标对象

| 字段名           | 类型              | 必填 | 说明                                                   |
| ---------------- | ----------------- | ---- | ------------------------------------------------------ |
| name             | string            | 是   | 指标名称                                               |
| type             | string            | 是   | 指标类型（`Counter`, `Gauge`, `Histogram`, `Summary`） |
| help             | string            | 是   | 帮助文本（描述指标用途）                               |
| labels           | array[string]     | 是   | 标签名称列表                                           |
| namespace        | string/null       | 是   | 命名空间前缀（未设置为 `null`）                        |
| subsystem        | string/null       | 是   | 子系统前缀（未设置为 `null`）                          |
| unit             | string/null       | 是   | 单位（未设置为 `null`）                                |
| metric_name      | string            | 是   | 推导的完整指标名称（包含命名空间和子系统）             |
| buckets          | array/null        | 是   | 桶边界（仅 Histogram；未显示设置为 `null`）            |
| custom_collector | boolean           | 是   | 是否为自定义收集器                                     |
| definitions      | array[Definition] | 是   | 指标定义位置列表                                       |
| usages           | array[Usage]      | 是   | 使用位置列表                                           |

#### 定义对象（Definition）

| 字段名    | 类型    | 必填 | 说明         |
| --------- | ------- | ---- | ------------ |
| file      | string  | 是   | 文件路径     |
| line      | integer | 是   | 行号         |
| statement | string  | 是   | 完整定义语句 |

#### 使用对象（Usage）

| 字段名    | 类型    | 必填 | 说明     |
| --------- | ------- | ---- | -------- |
| file      | string  | 是   | 文件路径 |
| line      | integer | 是   | 行号     |
| statement | string  | 是   | 完整语句 |

## 使用示例

以下是扫描结果的示例：

```yaml
metadata:
  scanner_name: prometheus_metrics_scanner
  command_args:
    - scan-metrics
    - ./src
    - --format
    - yaml
    - --include
    - "**/metrics.py"

summary:
  total_metrics: 5
  by_type:
    Counter: 1
    Gauge: 1
    Histogram: 1
    Summary: 1
    CustomCollector: 1
  files_scanned: 6
  scan_duration_ms: 428
  total_count: 5

results:
  http_requests_total:
    name: http_requests_total
    type: Counter
    help: "HTTP requests total count by method and status"
    labels:
      - method
      - status
      - endpoint
    namespace: myapp
    subsystem: api
    unit: total
    metric_name: myapp_api_http_requests_total
    buckets: null
    custom_collector: false
    definitions:
      - file: src/metrics/http.py
        line: 8
        statement: "REQUEST_COUNTER = Counter('http_requests_total', 'HTTP requests total count by method and status', ['method', 'status', 'endpoint'], namespace='myapp', subsystem='api')"
    usages:
      - file: src/middleware/metrics.py
        line: 12
        statement: "REQUEST_COUNTER = Counter('http_requests_total', 'HTTP requests total count by method and status', ['method', 'status', 'endpoint'])"
      - file: src/handlers/api.py
        line: 45
        statement: "REQUEST_COUNTER.labels(method='GET', status='200', endpoint='/users').inc()"
      - file: src/handlers/api.py
        line: 78
        statement: "REQUEST_COUNTER.labels(method='POST', status='201', endpoint='/users').inc()"

  memory_usage_bytes:
    name: memory_usage_bytes
    type: Gauge
    help: "Current memory usage in bytes"
    labels:
      - process_type
    namespace: system
    subsystem: null
    unit: bytes
    metric_name: system_memory_usage_bytes
    buckets: null
    custom_collector: false
    definitions:
      - file: src/monitoring/collectors.py
        line: 25
        statement: "MEMORY_GAUGE = Gauge('memory_usage_bytes', 'Current memory usage in bytes', ['process_type'], namespace='system')"
    usages:
      - file: src/monitoring/collectors.py
        line: 28
        statement: "MEMORY_GAUGE = Gauge('memory_usage_bytes', 'Current memory usage in bytes', ['process_type'])"
      - file: src/monitoring/reporters.py
        line: 92
        statement: "MEMORY_GAUGE.labels(process_type='worker').set(current_memory)"

  api_response_time_seconds:
    name: api_response_time_seconds
    type: Histogram
    help: "API endpoint response time distribution"
    labels:
      - method
      - endpoint
      - status
    namespace: api
    subsystem: gateway
    unit: seconds
    metric_name: api_gateway_api_response_time_seconds
    buckets:
      - 0.005
      - 0.01
      - 0.025
      - 0.05
      - 0.1
      - 0.25
      - 0.5
      - 1.0
      - 2.5
      - 5.0
    custom_collector: false
    definitions:
      - file: src/middleware/timing.py
        line: 12
        statement: "RESPONSE_TIME = Histogram('api_response_time_seconds', 'API endpoint response time distribution', ['method', 'endpoint', 'status'], namespace='api', subsystem='gateway', buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0])"
    usages:
      - file: src/middleware/timing.py
        line: 15
        statement: "RESPONSE_TIME = Histogram('api_response_time_seconds', 'API endpoint response time distribution', ['method', 'endpoint', 'status'], buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0])"
      - file: src/middleware/timing.py
        line: 68
        statement: "RESPONSE_TIME.labels(method=request.method, endpoint=request.path, status=response.status_code).observe(elapsed_time)"

  task_processing_duration:
    name: task_processing_duration
    type: Summary
    help: "Task processing duration quantiles (P50, P95, P99)"
    labels:
      - task_type
      - status
    namespace: null
    subsystem: null
    unit: seconds
    metric_name: task_processing_duration
    buckets: null
    custom_collector: false
    definitions:
      - file: src/workers/task_manager.py
        line: 31
        statement: "TASK_DURATION = Summary('task_processing_duration', 'Task processing duration quantiles (P50, P95, P99)', ['task_type', 'status'])"
    usages:
      - file: src/workers/task_manager.py
        line: 34
        statement: "TASK_DURATION = Summary('task_processing_duration', 'Task processing duration quantiles (P50, P95, P99)', ['task_type', 'status'])"
      - file: src/workers/task_executor.py
        line: 112
        statement: "TASK_DURATION.labels(task_type=task.type, status='completed').observe(execution_time)"

  db_pool_connections_active:
    name: db_pool_connections_active
    type: Gauge
    help: "Number of active database connections in the pool"
    labels:
      - db_name
      - pool_name
    namespace: app
    subsystem: database
    unit: null
    metric_name: app_database_db_pool_connections_active
    buckets: null
    custom_collector: true
    definitions:
      - file: src/db/monitoring.py
        line: 48
        statement: "g = GaugeMetricFamily('db_pool_connections_active', 'Number of active database connections in the pool', labels=['db_name', 'pool_name'])"
    usages:
      - file: src/db/monitoring.py
        line: 76
        statement: "g.add_metric([db.name, pool.name], pool.checked_out())"
```

### 示例说明

上述示例展示了五种不同的指标类型和场景覆盖：

1. **Counter（计数器）** - `http_requests_total`

   - 包含完整的命名空间（namespace）和子系统（subsystem）前缀
   - 有多个标签维度（method、status、endpoint）
   - 演示多个使用位置（在不同文件和行号的调用）
   - 演示标准指标定义和使用模式

2. **Gauge（仪表盘）** - `memory_usage_bytes`

   - 仅有命名空间前缀，无子系统前缀
   - 简化的标签配置（单一标签）
   - 展示实时状态值的监控
   - 演示命名空间存在但子系统为 null 的场景

3. **Histogram（直方图）** - `api_response_time_seconds`

   - 完整的命名空间和子系统前缀组合
   - 完整的桶配置（buckets），展示自定义分布范围
   - 多个标签维度支持
   - 适用于延迟和分布观察

4. **Summary（摘要）** - `task_processing_duration`

   - 命名空间和子系统都为 null 的场景
   - 无桶配置（buckets 为 null）
   - 在客户端计算分位数（P50、P95、P99）
   - 用于性能指标统计

5. **CustomCollector（自定义收集器）** - `db_pool_connections_active`
   - `custom_collector: true` 标识自定义收集逻辑
   - 命名空间和子系统都有值的完整场景
   - 使用 `Collector` 接口动态生成指标值
   - 演示多标签的自定义指标（db_name、pool_name）
   - 适用于需要在采集时动态计算的场景（如连接池大小、资源使用统计等）

**metadata** 字段涵盖：

- 扫描器标识
- 完整的命令参数列表

**summary** 字段统计：

- 各类型指标数量分布（包含 CustomCollector 类型）
- 扫描的文件总数
- 扫描耗时（毫秒）
- 指标总数

## 注意事项

1. **指标类型**：

   **Counter（计数器）**：

   - 只能增加的累计指标
   - 用于计数事件、请求等
   - 方法：`inc()`, `count_exceptions()`
   - 示例：请求总数、错误总数

   **Gauge（仪表盘）**：

   - 可增可减的指标
   - 用于当前状态、资源使用等
   - 方法：`set()`, `inc()`, `dec()`, `set_to_current_time()`
   - 示例：当前温度、内存使用量

   **Histogram（直方图）**：

   - 观察值的分布
   - 自动计算总和、计数、分位数
   - 配置桶（buckets）定义分布范围
   - 方法：`observe()`
   - 示例：请求耗时、响应大小

   **Summary（摘要）**：

   - 类似 Histogram，但在客户端计算分位数
   - 方法：`observe()`
   - 示例：请求延迟的 P50、P95、P99

2. **命名约定** - Prometheus 指标命名建议：

   - 使用小写和下划线：`http_requests_total`
   - 包含单位后缀：`_seconds`, `_bytes`, `_total`
   - 命名空间前缀：`myapp_http_requests_total`
   - 完整的指标名称格式：`[namespace_][subsystem_]name[_unit]`

3. **自定义收集器** - `custom_collector` 标识是否使用自定义收集逻辑：

   - 标准指标通过 `inc()`, `set()` 等方法更新
   - 自定义收集器在抓取时动态生成指标值
   - 支持 `Metric` 和 `MetricFamily` 对象定义来识别指标
   - 定义位置指实例化指标的代码行
   - 使用位置指实际添加或更新指标的代码行
