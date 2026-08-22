# 队列使用扫描器（queue-usage）

## 概述

`scan-queue-usage` 是一个静态 AST 扫描器，用于盘点 Python 项目中的队列构造、发送、消费和配置调用。它展示队列相关参数，并逐个判断参数是否写死在源码中。

扫描过程不会导入项目依赖、启动 worker 或连接 broker，因此结果代表源码证据，不代表运行时队列状态。

## 命令用法

```bash
upcast scan-queue-usage [OPTIONS] [PATH]
```

示例：

```bash
# 扫描当前项目
upcast scan-queue-usage .

# 输出 JSON 文件
upcast scan-queue-usage ./src --format json --output queue-usage.json

# 只扫描业务目录并排除测试
upcast scan-queue-usage . --include "app/**" --exclude "tests/**"
```

支持标准选项：`-o/--output`、`--format`、`-v/--verbose`、`--include`、`--exclude`、`--no-default-excludes` 和 Markdown 输出选项。

## 支持的队列类别

| 类别         | 框架/库                               | 典型 API                                                           |
| ------------ | ------------------------------------- | ------------------------------------------------------------------ |
| `in_process` | `queue`、`asyncio`、`multiprocessing` | `Queue()`、`put()`、`get()`、`maxsize`                             |
| `task_queue` | Celery、RQ、Dramatiq、Huey            | `apply_async()`、`send_task()`、`enqueue()`、`send()`              |
| `redis`      | redis-py List/Stream                  | `lpush()`、`brpop()`、`xadd()`、`xreadgroup()`、`xack()`           |
| `kafka`      | kafka-python、confluent-kafka         | `KafkaProducer`、`KafkaConsumer`、`send()`、`produce()`、`poll()`  |
| `rabbitmq`   | Pika、Kombu                           | `queue_declare()`、`basic_publish()`、`basic_consume()`、`Queue()` |

扫描器要求存在导入证据或已确认的构造对象绑定，不会因为变量名叫 `Queue` 就直接认定它是队列。

## 输出结构

```yaml
metadata:
  scanner_name: queue-usage
  static_analysis: true

summary:
  total_count: 2
  total_usages: 2
  files_scanned: 1
  scan_duration_ms: 3
  by_category:
    in_process: 2
  by_framework:
    queue: 2
  hardcoded_parameters: 2
  dynamic_parameters: 1
  unknown_parameters: 0

results:
  in_process:
    - category: in_process
      framework: queue
      operation: construct
      file: app/worker.py
      line: 4
      column: 8
      statement: "Queue(maxsize=100)"
      parameters:
        - name: maxsize
          expression: "100"
          value: 100
          source_kind: literal
          hardcoded: true
      hardcoding_status: fully_hardcoded
```

### 主要字段

| 字段                | 说明                                                                                    |
| ------------------- | --------------------------------------------------------------------------------------- |
| `category`          | 队列大类：`in_process`、`task_queue`、`redis`、`kafka`、`rabbitmq`                      |
| `framework`         | 具体实现，例如 `celery`、`rq`、`kafka-python`、`pika`                                   |
| `operation`         | 构造调用为 `construct`，其他调用保留实际 API 名，如 `put`、`send_task`、`basic_publish` |
| `parameters`        | 队列相关参数列表                                                                        |
| `expression`        | 参数在源码中的表达式；明显敏感值会脱敏                                                  |
| `value`             | 可以静态推导出的值；无法推导时为 `null`                                                 |
| `source_kind`       | `literal`、`static_constant`、`configuration`、`runtime`、`expression` 或 `unknown`     |
| `hardcoded`         | 参数是否写死：`true`、`false` 或 `null`（无法判断）                                     |
| `hardcoding_status` | 当前调用的聚合状态：`fully_hardcoded`、`partially_hardcoded`、`dynamic` 或 `unknown`    |

### 写死判定

- 字面量或能解析为字面量的常量：`hardcoded: true`。
- 环境变量、配置属性和运行时输入：`hardcoded: false`。
- 无法确认来源的复杂表达式：`hardcoded: null`。
- 判定以参数为单位，同一个调用可以同时包含写死参数和动态参数。

密码、token、secret、credential 等参数，以及包含 URL 用户信息的连接字符串，其静态值和参数表达式会输出为 `<redacted>`。

## 边界说明

该命令只报告源码中的队列使用点，不报告以下运行时指标：队列深度、Kafka lag、吞吐量、消费延迟、RabbitMQ unacked 数、worker 健康状态或实际重试次数。需要这些数据时，应接入对应 broker、worker 或应用的运行时监控指标。
