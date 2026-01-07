# 阻塞操作扫描器 (blocking-operations)

## 概述

阻塞操作扫描器用于识别 Python 代码中可能导致线程或进程阻塞的操作。它能够检测睡眠调用、锁操作、子进程调用、数据库操作等潜在的性能瓶颈。

该扫描器对于以下场景特别有用：

- 识别异步代码中的同步阻塞操作
- 性能优化和瓶颈分析
- 审查并发安全性
- 检测可能的死锁风险
- 改进响应时间

## 使用方法

```bash
upcast scan-blocking-operations [OPTIONS] [PATH]
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
upcast scan-blocking-operations .

# 保存结果到文件
upcast scan-blocking-operations ./src --output blocking.yaml

# 输出为 JSON 格式
upcast scan-blocking-operations ./app --format json --verbose
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

| 字段名           | 类型             | 必填 | 说明                 |
| ---------------- | ---------------- | ---- | -------------------- |
| total_count      | integer          | 是   | 阻塞操作总数         |
| by_category      | map[string, int] | 是   | 按类别统计的操作数量 |
| files_scanned    | integer          | 是   | 扫描的文件总数       |
| scan_duration_ms | integer          | 是   | 扫描耗时（毫秒）     |

### results 字段

`results` 是一个对象，每个键对应一种阻塞操作类别，值为该类别下的阻塞操作列表：

| 字段名          | 类型                     | 说明                                                                    |
| --------------- | ------------------------ | ----------------------------------------------------------------------- |
| time_based      | array[BlockingOperation] | 时间相关的阻塞操作（time.sleep 或者 asyncio.sleep 等）                  |
| synchronization | array[BlockingOperation] | 同步原语（锁、信号量等）                                                |
| subprocess      | array[BlockingOperation] | 子进程调用（subprocess 或者 multiprocessing 等）                        |
| database        | array[BlockingOperation] | 数据库操作（如 django 中使用 select_for_update 等这类明显会阻塞的操作） |

#### 阻塞操作对象（BlockingOperation）

| 字段名     | 类型         | 必填 | 说明                                                                                   |
| ---------- | ------------ | ---- | -------------------------------------------------------------------------------------- |
| operation  | string       | 是   | 命中的 API/方法名（如 `time.sleep`, `QuerySet.select_for_update`，可用代码推导真实值） |
| timeout    | integer/null | 否   | 超时时间（如果适用，可用代码推导真实值）                                               |
| file       | string       | 是   | 文件路径                                                                               |
| line       | integer      | 是   | 行号                                                                                   |
| statement  | string       | 是   | 完整的语句                                                                             |
| function   | string/null  | 是   | 所在函数名（模块级语句可能为 `null`）                                                  |
| class_name | string/null  | 是   | 所在类名（非类作用域可能为 `null`）                                                    |
| block      | string/null  | 是   | 所在代码块名称（如 `if`、`for`、`while` 等）                                           |

## 示例

以下是扫描结果的完整示例：

```yaml
metadata:
  scanner_name: blocking-operations
  command_args:
    - scan-blocking-operations
    - --format yaml
    - ./src
summary:
  total_count: 4
  by_category:
    database: 3
    time_based: 1
    synchronization: 1
    subprocess: 1
  files_scanned: 12
  scan_duration_ms: 153
results:
  database:
    - category: database
      class_name: ClusterManager
      function: switch_default_cluster
      file: apiserver/paasng/paas_wl/infras/cluster/models.py
      line: 216
      column: 35
      operation: self.select_for_update
      statement: self.select_for_update()
      block: null
      timeout: null
    - category: database
      class_name: ResourcePoolProvider
      function: create
      file: apiserver/paasng/paasng/accessories/services/providers/base.py
      line: 72
      column: 16
      operation: PreCreatedInstance.objects.select_for_update
      statement: PreCreatedInstance.objects.select_for_update()
      block: null
      timeout: null
    - category: database
      class_name: Application
      function: get_module_with_lock
      file: apiserver/paasng/paasng/platform/applications/models.py
      line: 363
      column: 15
      operation: self.modules.select_for_update
      statement: self.modules.select_for_update()
      block: null
      timeout: null
  time_based:
    - category: time_based
      class_name: WaitPodDelete
      function: wait
      file: apiserver/paasng/paas_wl/bk_app/deploy/app_res/controllers.py
      line: 95
      column: 12
      operation: time.sleep
      statement: time.sleep(0.5)
      block: for
      timeout: 0.5
  synchronization:
    - category: synchronization
      class_name: MyLockClass
      function: acquire_lock
      file: apiserver/paasng/paas_wl/utils/lock.py
      line: 42
      column: 8
      operation: self.lock.acquire
      statement: self.lock.acquire(timeout=2)
      block: if
      timeout: 2
  subprocess:
    - category: subprocess
      class_name: null
      function: run_command
      file: apiserver/paasng/paas_wl/utils/subproc.py
      line: 10
      column: 4
      operation: subprocess.run
      statement: subprocess.run(["ls", "-l"])
      block: null
      timeout: null
```

## 说明

该扫描器使用静态代码分析技术，结合预定义的阻塞操作模式列表，识别代码中的潜在阻塞操作，会在以下情况下进行类型推导，以提高检测准确性：

- 遇到类似 `from time import sleep as tsleep` 的导入语句时，能够识别 `tsleep()` 为 `time.sleep()`。
- 识别类方法调用中的阻塞操作，如 `self.lock.acquire()`。
- 识别通过变量调用的阻塞操作，如 `fn = time.sleep; fn()`。
- 识别调用 `Model.objects.select_for_update()` 这类 ORM 操作，并确认 Model 是 Django 模型类。

特别说明：阻塞操作对象的 `operation` 字段记录了推导出的 API/方法名，便于用户快速定位和理解阻塞操作的具体实现，而 `statement` 字段则提供了原始的代码语句上下文。

**time_based（时间相关）**：

- `time.sleep()` - 线程睡眠
- `asyncio.sleep()` - 异步睡眠（在同步上下文中使用会阻塞）
- `gevent.sleep()` - gevent 协程睡眠
- `eventlet.sleep()` - eventlet 协程睡眠

**synchronization（同步原语）**：

- `Lock.acquire()` - 获取锁
- `RLock.acquire()` - 获取递归锁
- `Semaphore.acquire()` - 获取信号量
- `Event.wait()` - 等待事件
- `Condition.wait()` - 等待条件变量

**subprocess（子进程）**：

- `subprocess.run()` - 运行子进程
- `subprocess.call()` - 调用子进程
- `subprocess.check_output()` - 执行并获取输出
- `subprocess.check_call()` - 执行并检查返回码
- `subprocess.Popen.wait()` - 等待子进程完成
- `subprocess.Popen.communicate()` - 与子进程通信并等待完成
- `os.popen()` - 打开子进程管道
- `os.system()` - 执行系统命令
- `multiprocessing.Process.join()` - 等待子进程完成
- `multiprocessing.Process.start()` - 启动子进程
- `multiprocessing.Pool.apply()` - 进程池调用
- `multiprocessing.Pool.map()` - 进程池映射调用
- `multiprocessing.Pool.apply_async()` - 进程池异步调用
- `multiprocessing.Pool.map_async()` - 进程池异步映射调用

**database（数据库）**：

- `QuerySet.select_for_update()` - 数据库行锁
- 其他可能阻塞的 ORM 操作

**外部请求**：

- `requests.get()` - 类似阻塞的 HTTP 请求，包含 POST、PUT、DELETE 等方法
- `requests.session.get()` - 类似阻塞的 HTTP 请求，包含 POST、PUT、DELETE 等方法
- `requests.request()` - 类似阻塞的 HTTP 请求
- `urllib.request.urlopen()` - 打开 URL（可能阻塞，视网络状况而定）
- `http.client.HTTPConnection.request()` - 发送 HTTP 请求（可能阻塞，视网络状况而定）
