# 信号扫描器 (signals)

## 概述

信号扫描器用于分析 Python 代码中的 Django 和 Celery 信号使用。它能够检测信号定义、信号接收器、信号发送等模式，帮助理解应用的事件驱动架构。

该扫描器对于以下场景特别有用：

- 理解应用的事件流
- 审查信号使用模式
- 识别潜在的性能问题
- 生成信号文档
- 重构和优化

## 命令使用

```bash
upcast scan-signals [OPTIONS] [PATH]
```

### 参数

- `PATH` - 要扫描的 Python 文件或目录路径（可选，默认为当前目录 `.`）

### 选项

- `-o, --output PATH` - 输出文件路径（YAML 或 JSON）
- `--format [yaml|json|markdown]` - 输出格式（默认：yaml）
- `--markdown-language [en|zh]` - Markdown 输出语言（默认：zh）
- `--markdown-title TEXT` - Markdown 输出标题
- `-v, --verbose` - 启用详细输出
- `--include PATTERN` - 包含的文件模式（可多次指定）
- `--exclude PATTERN` - 排除的文件模式（可多次指定）
- `--no-default-excludes` - 禁用默认排除模式

### 使用示例

```bash
# 扫描当前目录
upcast scan-signals

# 扫描特定目录并输出详细信息
upcast scan-signals ./src -v

# 保存结果到 YAML 文件
upcast scan-signals ./src -o signals.yaml

# 保存结果到 JSON 文件
upcast scan-signals ./src -o signals.json --format json

# 仅扫描 signals 相关文件
upcast scan-signals ./src --include "**/signals/**"

# 排除测试文件
upcast scan-signals ./src --exclude "**/tests/**"
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

| 字段名                 | 类型    | 必填 | 说明                   |
| ---------------------- | ------- | ---- | ---------------------- |
| total_count            | integer | 是   | 信号总数               |
| django_receivers       | integer | 是   | Django 信号接收器数量  |
| django_senders         | integer | 是   | Django 信号发送者数量  |
| celery_receivers       | integer | 是   | Celery 信号接收器数量  |
| celery_senders         | integer | 是   | Celery 信号发送者数量  |
| custom_signals_defined | integer | 是   | 自定义信号定义数量     |
| unused_custom_signals  | integer | 是   | 未使用的自定义信号数量 |
| files_scanned          | integer | 是   | 扫描的文件总数         |
| scan_duration_ms       | integer | 是   | 扫描耗时（毫秒）       |

### results 字段

`results` 是一个数组，每个元素代表一个信号（或一类信号）及其接收器信息。

#### 信号对象

| 字段名    | 类型                  | 必填 | 说明                                               |
| --------- | --------------------- | ---- | -------------------------------------------------- |
| category  | string                | 是   | 信号类别（如 `model_signals`, `other_signals` 等） |
| type      | string                | 是   | 信号来源类型（示例中为 `django`）                  |
| signal    | string                | 是   | 信号名称（如 `post_save`, `post_appenv_deploy`）   |
| senders   | array[SignalSender]   | 是   | 发送者列表（示例中为空数组）                       |
| receivers | array[SignalReceiver] | 是   | 接收器列表                                         |

#### 发送者对象（SignalSender）

| 字段名    | 类型        | 必填 | 说明                     |
| --------- | ----------- | ---- | ------------------------ |
| file      | string      | 是   | 文件路径                 |
| lineno    | integer     | 是   | 行号                     |
| statement | string/null | 否   | 定义发送者的完整代码语句 |

#### 接收器对象（SignalReceiver）

| 字段名    | 类型        | 必填 | 说明                            |
| --------- | ----------- | ---- | ------------------------------- |
| file      | string      | 是   | 文件路径                        |
| lineno    | integer     | 是   | 行号                            |
| handler   | string      | 是   | 处理器函数名                    |
| sender    | string/null | 否   | 指定的发送者（未指定为 `null`） |
| statement | string/null | 否   | 定义接收器的完整代码语句        |

## 使用示例

以下是扫描结果的示例：

```yaml
metadata:
  scanner_name: signal
  command_args:
    - scan-signals
    - /path/to/project
    - --format
    - yaml

summary:
  total_count: 12
  django_receivers: 5
  django_senders: 3
  celery_receivers: 2
  celery_senders: 1
  custom_signals_defined: 2
  unused_custom_signals: 1
  files_scanned: 45
  scan_duration_ms: 1234

results:
  - category: django_signal
    type: django
    signal: post_save
    senders: []
    receivers:
      - file: myapp/signals.py
        lineno: 12
        handler: on_user_created
        sender: User
        statement: "@receiver(post_save, sender=User)"
      - file: myapp/handlers.py
        lineno: 78
        handler: send_welcome_email
        sender: User
        statement: "post_save.connect(send_welcome_email, sender=User)"

  - category: django_signal
    type: django
    signal: request_finished
    senders: []
    receivers:
      - file: myapp/middleware.py
        lineno: 33
        handler: log_request_metrics
        statement: "request_finished.connect(log_request_metrics)"

  - category: celery_signal
    type: celery
    signal: task_postrun
    senders: []
    receivers:
      - file: myapp/celery_handlers.py
        lineno: 18
        handler: update_task_status
        statement: "task_postrun.connect(update_task_status)"
      - file: myapp/monitoring.py
        lineno: 95
        handler: record_task_metrics
        statement: "task_postrun.connect(record_task_metrics)"

  - category: django_signal
    type: custom
    signal: order_completed
    status: ""
    senders:
      - file: myapp/signals.py
        lineno: 45
        statement: "order_completed = Signal(providing_args=['order_id'])"
    receivers:
      - file: myapp/signals.py
        lineno: 67
        handler: trigger_fulfillment
        statement: "order_completed.connect(trigger_fulfillment)"
```

## 注意事项

1. **信号类别**：

   **model_signals（模型信号）** - Django ORM 模型生命周期：

   - `pre_save` - 模型保存前
   - `post_save` - 模型保存后
   - `pre_delete` - 模型删除前
   - `post_delete` - 模型删除后
   - `m2m_changed` - 多对多关系变化

   **request_signals（请求信号）** - Django 请求处理：

   - `request_started` - 请求开始
   - `request_finished` - 请求结束
   - `got_request_exception` - 请求异常

   **celery_signals（Celery 信号）** - Celery 任务：

   - `task_prerun` - 任务执行前
   - `task_postrun` - 任务执行后
   - `task_failure` - 任务失败
   - `task_success` - 任务成功

   **custom_signals（自定义信号）** - 应用自定义：

   - 用户自定义的 `Signal()` 实例
   - 特定业务逻辑的事件

2. **发送者（Sender）**：

   - 模型信号通常指定模型类作为发送者
   - `sender=None` 表示接收所有发送者的信号
   - 具体发送者限制信号触发范围，提高性能

3. **接收器装饰器** - Django 提供两种注册方式：

   ```python
   # 装饰器方式
   @receiver(post_save, sender=MyModel)
   def my_handler(sender, instance, **kwargs):
       pass

   # 显式连接
   post_save.connect(my_handler, sender=MyModel)
   ```
