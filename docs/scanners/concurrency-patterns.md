# 并发模式扫描器 (concurrency-patterns)

## 概述

并发模式扫描器用于分析 Python 代码中的并发和并行模式。它能够检测线程、多进程、异步IO（asyncio）、以及 Celery 任务的使用模式。

该扫描器对于以下场景特别有用：

- 审查并发策略
- 识别潜在的并发问题
- 优化并发性能
- 分析任务队列使用
- 并发模式文档化

## 命令用法

```bash
upcast scan-concurrency-patterns [OPTIONS] [PATH]
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
upcast scan-concurrency-patterns .

# 保存结果到文件
upcast scan-concurrency-patterns ./src --output concurrency.yaml

# 输出为 JSON 格式
upcast scan-concurrency-patterns ./app --format json
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

| 字段名           | 类型             | 必填 | 说明                     |
| ---------------- | ---------------- | ---- | ------------------------ |
| total_count      | integer          | 是   | 并发模式总数             |
| by_category      | map[string, int] | 是   | 按类别统计的并发模式数量 |
| files_scanned    | integer          | 否   | 扫描的文件总数           |
| scan_duration_ms | integer          | 否   | 扫描耗时（毫秒）         |

### results 字段

`results` 是一个对象，包含以下并发类型：

| 字段名          | 类型                                   | 说明             |
| --------------- | -------------------------------------- | ---------------- |
| threading       | map[string, array[ConcurrencyPattern]] | 线程相关模式     |
| multiprocessing | map[string, array[ConcurrencyPattern]] | 多进程相关模式   |
| asyncio         | map[string, array[ConcurrencyPattern]] | asyncio 相关模式 |
| celery          | map[string, array[ConcurrencyPattern]] | Celery 相关模式  |

每个并发类型下的子键为具体检测到的模式名称，值为该模式的并发模式对象列表。

#### 并发模式对象（ConcurrencyPattern）

| 字段名     | 类型        | 必填 | 说明                                                         |
| ---------- | ----------- | ---- | ------------------------------------------------------------ |
| pattern    | string      | 是   | 模式类型（如 `thread_creation`，可用代码推导来识别）         |
| file       | string      | 是   | 文件路径                                                     |
| line       | integer     | 是   | 行号                                                         |
| column     | integer     | 是   | 列号                                                         |
| statement  | string      | 是   | 完整语句                                                     |
| block      | string/null | 是   | 所在代码块名称（模块级语句可能为 `null`）                    |
| function   | string/null | 是   | 所在函数名（模块级语句可能为 `null`）                        |
| class_name | string/null | 是   | 所在类名（非类作用域可能为 `null`）                          |
| api_call   | string/null | 是   | API 调用名称（未解析到时为 `null`）                          |
| details    | object/null | 是   | 额外详情（不同 pattern 的结构可能不同；示例中包含 `target`） |

## 示例

以下是扫描结果的示例：

```yaml
metadata: {}
results:
  asyncio: {}
  celery: {}
  multiprocessing:
    process_creation:
      - api_call: null
        class_name: Cluster
        column: 24
        details:
          target: Sentinel
        file: svc-rabbitmq/tasks/management/commands/worker.py
        function: __init__
        line: 115
        pattern: process_creation
        statement:
          Process(target=Sentinel, args=(self.cluster_id, self.stop_event,
          self.start_event, self.broker, self.timeout))

  threading:
    thread_creation:
      - api_call: null
        class_name: ParallelChainedGenerator
        column: 19
        details:
          target: self._consume_gen
        file: apiserver/paasng/paas_wl/bk_app/processes/watch.py
        function: start
        line: 185
        pattern: thread_creation
        statement: threading.Thread(target=self._consume_gen, args=(gen, ))

      - api_call: null
        class_name: TestBareGitRepoController
        column: 12
        details:
          target: httpd.serve_forever
        file: apiserver/paasng/tests/paasng/platform/sourcectl/test_bare_git.py
        function: test_anonymize_url
        line: 83
        pattern: thread_creation
        statement: threading.Thread(target=httpd.serve_forever)

    thread_pool_executor:
      - api_call: null
        class_name: null
        column: 17
        details: null
        file: apiserver/paasng/paasng/platform/smart_app/services/dispatch.py
        function: dispatch_package_to_modules
        line: 74
        pattern: thread_pool_executor
        statement: ThreadPoolExecutor()

summary:
  by_category:
    multiprocessing: 1
    threading: 3
  files_scanned: 4
  scan_duration_ms: 10856
  total_count: 4
```

## 说明

1. **并发类型**：注意要使用代码推导的能力来正确识别调用的对象的模块和类型，以避免同名导致的误报。例如，`Thread` 可能是 `xxxx.Thread` 或其他自定义类，仅当确认是 `threading.Thread` 时才算作线程创建模式。

   **threading（线程）**：

- `threading.Thread(target=..., args=..., kwargs=..., daemon=...).start()` - 直接创建并启动线程（可先创建再调用 `.start()`）
- `class MyThread(Thread): ...; MyThread(...).start()` - 子类化 Thread 并在 `run()` 中实现逻辑后启动
- `threading.Timer(interval, func, args/kwargs).start()` - 延迟启动的线程
- `concurrent.futures.ThreadPoolExecutor(max_workers=...)` - 创建线程池（支持别名导入，如 `ThreadPoolExecutor as TPE`）
- `executor.submit(fn, *args, **kwargs)` - 线程池提交单个任务
- `executor.map(fn, iterable, ...)` - 线程池批量提交任务
- `with ThreadPoolExecutor(...) as executor:` - 上下文管理线程池生命周期
- `executor.shutdown(wait=...)` - 显式关闭线程池并等待任务结束
- `multiprocessing.dummy.Pool` / `multiprocessing.pool.ThreadPool` - 线程池的等价实现

  **multiprocessing（多进程）**：

- `multiprocessing.Process(target=..., args=..., kwargs=..., daemon=...).start()` / `join(timeout=...)` / `terminate()` - 直接创建、启动、等待或终止子进程（可先创建再 `.start()`）
- `multiprocessing.set_start_method("spawn"|"fork"|"forkserver")` / `multiprocessing.get_context(...)` - 配置/获取启动方式上下文
- `multiprocessing.Pool(processes=...)` - 经典进程池（支持别名导入，如 `Pool as P`）
- `pool.map(fn, iterable)` / `pool.imap(fn, iterable)` / `pool.imap_unordered(fn, iterable)` - 进程池批量映射任务
- `pool.apply(fn, args, kwargs)` / `pool.apply_async(fn, args, kwargs)` - 进程池提交单个任务（同步/异步）
- `pool.starmap(fn, iterable)` / `pool.starmap_async(fn, iterable)` - 进程池多参数映射
- `with Pool(...) as pool:` / `pool.close(); pool.join()` / `pool.terminate()` - 上下文管理或显式收尾
- `concurrent.futures.ProcessPoolExecutor(max_workers=...)` - 创建进程池执行器
- `executor.submit(fn, *args, **kwargs)` / `executor.map(fn, iterable, ...)` - 进程池提交/映射任务
- `with ProcessPoolExecutor(...) as executor:` / `executor.shutdown(wait=...)` - 上下文管理与关闭
- `multiprocessing.Queue()` / `multiprocessing.JoinableQueue()` / `multiprocessing.SimpleQueue()` - 进程间队列通信
- `multiprocessing.Pipe(duplex=...)` - 进程间管道通信
- `multiprocessing.Manager()` / `manager.list()` / `manager.dict()` / `manager.Namespace()` / `manager.Value()` / `manager.Array()` - 共享对象代理
- `multiprocessing.Lock()` / `RLock()` / `Semaphore()` / `BoundedSemaphore()` / `Event()` / `Condition()` / `Barrier()` - 进程级同步原语
- `multiprocessing.Value(typecode, ...)` / `multiprocessing.Array(typecode, ...)` / `multiprocessing.shared_memory.SharedMemory(...)` - 共享内存与原始缓冲区

  **asyncio（异步 IO）**：

- `await <awaitable>` - 在协程内等待其他协程/异步对象
- `asyncio.run(coro)` / `loop.run_until_complete(coro)` - 事件循环入口运行协程
- `asyncio.create_task(coro)` / `loop.create_task(coro)` / `asyncio.ensure_future(coro)` - 创建任务
- `asyncio.TaskGroup()` / `async with TaskGroup() as tg:` / `tg.create_task(...)` - 任务分组（Python 3.11+）
- `asyncio.gather(*coros, return_exceptions=...)` - 并发收集多个协程结果
- `asyncio.wait(tasks, return_when=FIRST_COMPLETED|FIRST_EXCEPTION|ALL_COMPLETED)` / `asyncio.as_completed(tasks)` - 等待任务集合
- `asyncio.to_thread(fn, *args, **kwargs)` - 在线程中执行同步函数并返回可等待对象
- `asyncio.sleep()` / `asyncio.timeout()` / `asyncio.wait_for(coro, timeout)` - 异步睡眠与超时控制
- `asyncio.Lock()` / `Semaphore()` / `BoundedSemaphore()` / `Event()` / `Condition()` / `Queue()` / `LifoQueue()` / `PriorityQueue()` - 异步同步原语与队列
- `asyncio.open_connection()` / `asyncio.start_server()` - 基于流的异步网络 I/O

  **celery（任务队列）**：

- `task.delay(*args, **kwargs)` - 快捷异步调用任务
- `task.apply_async(args, kwargs, countdown=..., eta=..., expires=..., priority=..., queue=..., routing_key=..., retry=..., retry_policy=...)` - 带调度/路由/重试参数的异步调用
- `task.retry(exc=..., countdown=..., max_retries=...)` - 在任务内部触发重试
- `group(tasks)` / `chain(tasks)` / `chord(header, body)` - 任务编排（并行、串行、回调）
- `task.map(iterable)` / `task.starmap(iterable_of_args)` - 任务批量映射
- `signature("task_name", args/kwargs)` / `sig.apply_async(...)` - 使用签名/Canvas 构造任务
- `app.add_periodic_task(...)` / `app.conf.beat_schedule` - 定时任务/周期任务配置

3. **target 追踪**：

- 对于线程和进程创建，`details.target` 字段记录了传递给 `target` 参数的可调用对象，有助于理解线程/进程的执行逻辑。
- 对于 celery 任务，`details.target` 记录了任务函数或方法的名称。
