# 扫描器测试计划

本文档记录所有扫描器的详细测试计划和进度。

## 测试覆盖状态

| #   | 扫描器              | 文档 | 当前测试 | 目标测试   | 状态      | 优先级 |
| --- | ------------------- | ---- | -------- | ---------- | --------- | ------ |
| 1   | blocking_operations | ✅   | 52 行    | 33 个测试  | ⚠️ 待完成 | 🔴 高  |
| 2   | concurrency         | ✅   | 50 行    | 70+ 个测试 | ⚠️ 待完成 | 🔴 高  |
| 3   | django_urls         | ✅   | 59 行    | 54 个测试  | ⚠️ 待完成 | 🔴 高  |
| 4   | exceptions          | ✅   | 52 行    | 62 个测试  | ⚠️ 待完成 | 🔴 高  |
| 5   | metrics             | ✅   | 52 行    | 54 个测试  | ⚠️ 待完成 | 🔴 高  |
| 6   | unit_tests          | ✅   | 52 行    | 62 个测试  | ⚠️ 待完成 | 🔴 高  |
| 7   | logging             | ✅   | ~14KB    | +42 个测试 | ⚠️ 待增强 | 🟡 中  |
| 8   | redis_usage         | ✅   | ~6KB     | +46 个测试 | ⚠️ 待增强 | 🟡 中  |
| 9   | module_symbols      | ✅   | ~20KB    | +66 个测试 | ⚠️ 待增强 | 🟡 中  |
| 10  | complexity          | ✅   | 322 行   | -          | ✅ 完善   | 🟢 低  |
| 11  | django_models       | ✅   | 169 行   | -          | ✅ 完善   | 🟢 低  |
| 12  | django_settings     | ✅   | 253 行   | -          | ✅ 完善   | 🟢 低  |
| 13  | env_vars            | ✅   | 381 行   | -          | ✅ 完善   | 🟢 低  |
| 14  | http_requests       | ✅   | 395 行   | -          | ✅ 完善   | 🟢 低  |
| 15  | signals             | ✅   | 357 行   | -          | ✅ 完善   | 🟢 低  |

**总计新增测试：** ~489 个

---

## 1. blocking_operations (阻塞操作扫描器)

**文档：** `docs/scanners/blocking-operations.md`

### 测试目标

- 33 个测试
- 覆盖 4 个类别：time_based, synchronization, subprocess, database

### 测试文件结构

```
tests/test_blocking_operations_scanner/
├── __init__.py
├── conftest.py
├── fixtures/
│   ├── time_based_ops.py
│   ├── synchronization_ops.py
│   ├── subprocess_ops.py
│   ├── database_ops.py
│   ├── mixed_contexts.py
│   └── edge_cases.py
├── test_models.py (7 个测试)
├── test_integration.py (12 个测试)
├── test_categories.py (8 个测试)
└── test_edge_cases.py (6 个测试)
```

### 关键测试点

- ✅ time.sleep, asyncio.sleep 检测
- ✅ threading.Lock, asyncio.Lock, Semaphore 检测
- ✅ subprocess.call, multiprocessing.Process 检测
- ✅ Django select_for_update 检测
- ✅ timeout 参数提取
- ✅ function, class_name, block 上下文捕获
- ✅ summary.by_category 统计

### 状态

- [ ] fixtures 创建
- [ ] test_models.py
- [ ] test_integration.py
- [ ] test_categories.py
- [ ] test_edge_cases.py

---

## 2. concurrency (并发模式扫描器)

**文档：** `docs/scanners/concurrency-patterns.md`

### 测试目标

- 70+ 个测试
- 覆盖 4 个类别：threading, multiprocessing, asyncio, celery

### 测试文件结构

```
tests/test_concurrency_pattern_scanner/ (已存在，扩展)
├── fixtures/ (扩展)
│   ├── celery_patterns.py (新增)
│   ├── executor_patterns.py (新增)
│   ├── task_group_patterns.py (新增)
│   └── mixed_concurrency.py (新增)
├── test_models.py (8 个测试) (新增)
├── test_integration.py (20+ 个测试) (扩展)
├── test_threading_patterns.py (8 个测试) (新增)
├── test_multiprocessing_patterns.py (10 个测试) (新增)
├── test_asyncio_patterns.py (12 个测试) (新增)
├── test_celery_patterns.py (6 个测试) (新增)
└── test_edge_cases.py (8 个测试) (新增)
```

### 关键测试点

- ✅ threading.Thread, ThreadPoolExecutor
- ✅ multiprocessing.Process, Pool, ProcessPoolExecutor
- ✅ async def, await, asyncio.create_task, gather
- ✅ celery task.delay, apply_async, retry
- ✅ target 信息提取
- ✅ details 字段
- ✅ summary.by_category 统计

### 状态

- [ ] fixtures 扩展
- [ ] test_models.py
- [ ] test_integration.py 扩展
- [ ] test_threading_patterns.py
- [ ] test_multiprocessing_patterns.py
- [ ] test_asyncio_patterns.py
- [ ] test_celery_patterns.py
- [ ] test_edge_cases.py

---

## 3. django_urls (Django URL 扫描器)

**文档：** `docs/scanners/django-urls.md`

### 测试目标

- 54 个测试
- 覆盖 3 个类型：path, re_path, include

### 测试文件结构

```
tests/test_django_urls_scanner/ (新建)
├── __init__.py
├── conftest.py
├── fixtures/
│   ├── path_patterns.py
│   ├── re_path_patterns.py
│   ├── include_patterns.py
│   ├── drf_router_patterns.py
│   ├── converters_patterns.py
│   ├── namespace_patterns.py
│   ├── conditional_urls.py
│   └── nested_includes.py
├── test_models.py (10 个测试)
├── test_integration.py (18 个测试)
├── test_path_types.py (6 个测试)
├── test_converters.py (6 个测试)
├── test_drf_routers.py (6 个测试)
└── test_edge_cases.py (8 个测试)
```

### 关键测试点

- ✅ path(), re_path(), include() 检测
- ✅ view_name, name, namespace 提取
- ✅ URL converters (<int:id>, <str:slug>) 提取
- ✅ DRF router 检测 (DefaultRouter, SimpleRouter)
- ✅ basename 提取
- ✅ block 上下文 (if, try)
- ✅ nested includes

### 状态

- [ ] 目录创建
- [ ] fixtures 创建
- [ ] test_models.py
- [ ] test_integration.py
- [ ] test_path_types.py
- [ ] test_converters.py
- [ ] test_drf_routers.py
- [ ] test_edge_cases.py

---

## 4. exceptions (异常处理扫描器)

**文档：** `docs/scanners/exception-handlers.md`

### 测试目标

- 62 个测试
- 覆盖 try-except-else-finally 完整结构

### 测试文件结构

```
tests/test_exceptions_scanner/ (新建)
├── __init__.py
├── conftest.py
├── fixtures/
│   ├── simple_try_except.py
│   ├── multiple_except_clauses.py
│   ├── try_else_finally.py
│   ├── nested_exceptions.py
│   ├── bare_except.py
│   ├── exception_logging.py
│   ├── control_flow.py
│   ├── pass_only_except.py
│   └── exception_contexts.py
├── test_models.py (10 个测试)
├── test_integration.py (20 个测试)
├── test_exception_types.py (8 个测试)
├── test_control_flow.py (6 个测试)
├── test_logging_detection.py (8 个测试)
└── test_edge_cases.py (10 个测试)
```

### 关键测试点

- ✅ try-except-else-finally 检测
- ✅ 多个 except 子句
- ✅ bare except (空异常列表)
- ✅ 异常类型提取
- ✅ raise, return, break, continue, pass 计数
- ✅ 日志级别计数 (debug, info, warning, error, critical, exception)
- ✅ nested_exceptions 标记
- ✅ 行数统计

### 状态

- [ ] 目录创建
- [ ] fixtures 创建
- [ ] test_models.py
- [ ] test_integration.py
- [ ] test_exception_types.py
- [ ] test_control_flow.py
- [ ] test_logging_detection.py
- [ ] test_edge_cases.py

---

## 5. metrics (Prometheus 指标扫描器)

**文档：** `docs/scanners/metrics.md`

### 测试目标

- 54 个测试
- 覆盖 4 种指标类型：Counter, Gauge, Histogram, Summary

### 测试文件结构

```
tests/test_prometheus_metrics_scanner/ (已存在，扩展)
├── fixtures/ (扩展)
│   ├── counter_metrics.py (新增)
│   ├── gauge_metrics.py (新增)
│   ├── histogram_metrics.py (新增)
│   ├── summary_metrics.py (新增)
│   ├── metric_with_labels.py (新增)
│   ├── metric_with_namespace.py (新增)
│   ├── metric_usage_patterns.py (新增)
│   └── mixed_metrics.py (已有)
├── test_models.py (12 个测试) (新增)
├── test_integration.py (20 个测试) (扩展)
├── test_metric_types.py (8 个测试) (新增)
├── test_metric_naming.py (6 个测试) (新增)
└── test_edge_cases.py (8 个测试) (新增)
```

### 关键测试点

- ✅ Counter, Gauge, Histogram, Summary 检测
- ✅ name, type, help, labels 提取
- ✅ namespace, subsystem, unit 提取
- ✅ metric_name 完整名称构建
- ✅ Histogram buckets 提取
- ✅ custom_collector 标记
- ✅ definitions 和 usages 列表
- ✅ 使用方法检测 (.inc(), .set(), .observe())

### 状态

- [ ] fixtures 扩展
- [ ] test_models.py
- [ ] test_integration.py 扩展
- [ ] test_metric_types.py
- [ ] test_metric_naming.py
- [ ] test_edge_cases.py

---

## 6. unit_tests (单元测试扫描器)

**文档：** `docs/scanners/unit-tests.md`

### 测试目标

- 62 个测试
- 支持 pytest 和 unittest

### 测试文件结构

```
tests/test_unit_tests_scanner/ (新建)
├── __init__.py
├── conftest.py
├── fixtures/
│   ├── pytest_tests.py
│   ├── unittest_tests.py
│   ├── test_with_fixtures.py
│   ├── test_with_parametrize.py
│   ├── test_with_imports.py
│   ├── test_assertions.py
│   ├── test_classes.py
│   └── mixed_tests.py
├── test_models.py (10 个测试)
├── test_integration.py (22 个测试)
├── test_pytest_detection.py (8 个测试)
├── test_unittest_detection.py (6 个测试)
├── test_target_inference.py (8 个测试)
└── test_edge_cases.py (8 个测试)
```

### 关键测试点

- ✅ pytest test\_\* 函数检测
- ✅ unittest TestCase 类检测
- ✅ assert 语句计数
- ✅ body_md5 计算
- ✅ line_range 提取
- ✅ targets 推断 (基于导入)
- ✅ root_modules 选项
- ✅ exclude_modules 选项
- ✅ 参数化测试检测

### 状态

- [ ] 目录创建
- [ ] fixtures 创建
- [ ] test_models.py
- [ ] test_integration.py
- [ ] test_pytest_detection.py
- [ ] test_unittest_detection.py
- [ ] test_target_inference.py
- [ ] test_edge_cases.py

---

## 7. logging (日志扫描器) - 增强

**文档：** `docs/scanners/logging.md`

### 测试目标

- +42 个新测试
- 当前已有基础测试

### 新增测试文件

```
tests/test_logging_scanner/ (扩展)
├── test_models.py (8 个测试) (新增)
├── test_libraries.py (8 个测试) (新增)
├── test_message_types.py (6 个测试) (新增)
├── test_sensitive_data.py (6 个测试) (新增)
├── test_block_detection.py (6 个测试) (新增)
└── test_edge_cases.py (8 个测试) (新增)
```

### 关键测试点

- ✅ 标准 logging, loguru, structlog, Django 日志
- ✅ 日志级别检测
- ✅ 消息类型 (string, fstring, format, percent, template)
- ✅ 敏感信息检测 (password, token, api_key)
- ✅ logger_name 解析
- ✅ args 提取
- ✅ block 上下文
- ✅ summary 统计

### 状态

- [ ] test_models.py
- [ ] test_libraries.py
- [ ] test_message_types.py
- [ ] test_sensitive_data.py
- [ ] test_block_detection.py
- [ ] test_edge_cases.py

---

## 8. redis_usage (Redis 使用扫描器) - 增强

**文档：** `docs/scanners/redis-usage.md`

### 测试目标

- +46 个新测试
- 当前只有 key_inference 测试

### 新增测试文件

```
tests/test_redis_usage_scanner/ (扩展)
├── fixtures/ (新增)
│   ├── cache_backend.py
│   ├── celery_broker.py
│   ├── redis_client.py
│   ├── redis_pipeline.py
│   ├── distributed_lock.py
│   ├── redis_operations.py
│   └── mixed_usage.py
├── test_models.py (8 个测试) (新增)
├── test_integration.py (18 个测试) (新增)
├── test_operations.py (12 个测试) (新增)
└── test_edge_cases.py (8 个测试) (新增)
```

### 关键测试点

- ✅ cache_backend, celery_broker, redis_client 等类型
- ✅ 库识别 (redis, django_redis, aioredis)
- ✅ 操作类型 (get, set, delete, incr, lpush, sadd, zadd, hset, etc.)
- ✅ key 模式推断 (... 表示变量部分)
- ✅ args, kwargs 提取
- ✅ 按 key 模式分组

### 状态

- [ ] fixtures 创建
- [ ] test_models.py
- [ ] test_integration.py
- [ ] test_operations.py
- [ ] test_edge_cases.py

---

## 9. module_symbols (模块符号扫描器) - 增强

**文档：** `docs/scanners/module-symbols.md`

### 测试目标

- +66 个新测试
- 当前有基础测试

### 新增测试文件

```
tests/test_module_symbol_scanner/ (扩展)
├── fixtures/ (扩展)
│   ├── decorators_advanced.py (新增)
│   ├── async_functions.py (新增)
│   ├── class_inheritance.py (新增)
│   ├── type_hints.py (新增)
│   ├── private_symbols.py (新增)
│   └── conditional_imports.py (新增)
├── test_decorators.py (10 个测试) (新增)
├── test_function_detection.py (10 个测试) (新增)
├── test_class_detection.py (12 个测试) (新增)
├── test_variable_detection.py (8 个测试) (新增)
├── test_import_detection.py (10 个测试) (新增)
├── test_private_symbols.py (6 个测试) (新增)
└── test_edge_cases.py (10 个测试) (新增)
```

### 关键测试点

- ✅ import, from import, star import 检测
- ✅ 函数、类、变量定义检测
- ✅ 装饰器提取 (name, call, args, kwargs)
- ✅ async 函数检测
- ✅ 类继承、方法、属性检测
- ✅ 函数签名、docstring 提取
- ✅ body_md5 计算
- ✅ block 上下文
- ✅ --include-private 选项

### 状态

- [ ] fixtures 扩展
- [ ] test_decorators.py
- [ ] test_function_detection.py
- [ ] test_class_detection.py
- [ ] test_variable_detection.py
- [ ] test_import_detection.py
- [ ] test_private_symbols.py
- [ ] test_edge_cases.py

---

## 实施时间线

| 阶段 | 任务                     | 预计时间 | 状态      |
| ---- | ------------------------ | -------- | --------- |
| 0    | 创建公共 fixtures 和文档 | 1 小时   | ⚠️ 进行中 |
| 1    | blocking_operations      | 2-3 小时 | ⏳ 待开始 |
| 2    | concurrency              | 4-5 小时 | ⏳ 待开始 |
| 3    | django_urls              | 3-4 小时 | ⏳ 待开始 |
| 4    | exceptions               | 3-4 小时 | ⏳ 待开始 |
| 5    | metrics                  | 3-4 小时 | ⏳ 待开始 |
| 6    | unit_tests               | 3-4 小时 | ⏳ 待开始 |
| 7    | logging (增强)           | 2-3 小时 | ⏳ 待开始 |
| 8    | redis_usage (增强)       | 2-3 小时 | ⏳ 待开始 |
| 9    | module_symbols (增强)    | 3-4 小时 | ⏳ 待开始 |

**总计：** ~25-34 小时

---

## 成功标准

每个扫描器的测试应满足：

- ✅ 覆盖文档中的所有特性
- ✅ 模型测试通过率 100%
- ✅ 集成测试通过率 100%
- ✅ 代码覆盖率 > 85%
- ✅ 包含边界情况和错误处理
- ✅ 清晰的测试名称和文档字符串
- ✅ 独立运行（不依赖其他测试）

---

## 测试运行命令

```bash
# 运行特定扫描器的所有测试
pytest tests/test_<scanner>_scanner/ -v

# 运行并查看覆盖率
pytest tests/test_<scanner>_scanner/ --cov=upcast.scanners.<scanner> --cov-report=term-missing

# 运行所有新增测试
pytest tests/test_*_scanner/ -v

# 运行所有测试
pytest tests/ -v
```

---

最后更新：2026-01-08
