# Tasks

## Phase 1: 准备工作

- [x] 创建 `docs/` 目录结构
  - 创建 `docs/scanners/` 子目录
  - 创建 `docs/README.md` 文档索引
  - 验证: 目录结构创建成功

## Phase 2: 编写通用文档

- [x] 编写 `docs/README.md`
  - 添加文档总览
  - 列出所有扫描器及其简介
  - 说明通用选项(--include, --exclude, --format, --output 等)
  - 添加各扫描器文档的链接索引
  - 验证: 索引完整,链接正确

## Phase 3: Django 相关扫描器文档

- [x] 编写 `docs/scanners/django-models.md`

  - 分析 `example/scan-results/django-models.yaml` 输出结构
  - 参考 `upcast/scanners/django_models.py` 实现
  - 说明所有字段含义(name, module, bases, fields, relationships, meta 等)
  - 验证: 字段覆盖完整

- [x] 编写 `docs/scanners/django-settings.md`

  - 分析 `example/scan-results/django-settings.yaml`
  - 参考 `upcast/scanners/django_settings.py`
  - 说明 definitions 和 usages 两种模式
  - 验证: 覆盖所有使用模式

- [x] 编写 `docs/scanners/django-urls.md`
  - 分析 `example/scan-results/django-urls.yaml`
  - 参考 `upcast/scanners/django_url.py`
  - 说明 URL 模式识别规则
  - 验证: 字段说明准确

## Phase 4: 通用分析扫描器文档

- [x] 编写 `docs/scanners/env-vars.md`

  - 分析 `example/scan-results/env-vars.yaml`
  - 参考 `upcast/scanners/env_var.py`
  - 说明环境变量检测规则(os.environ, os.getenv 等)
  - 验证: 覆盖所有检测模式

- [x] 编写 `docs/scanners/logging.md`

  - 分析 `example/scan-results/logging.yaml`
  - 参考 `upcast/scanners/logging.py`
  - 说明支持的日志库(logging, loguru, structlog, django)
  - 验证: 字段说明完整

- [x] 编写 `docs/scanners/http-requests.md`

  - 分析 `example/scan-results/http-requests.yaml`
  - 参考 `upcast/scanners/http_requests.py`
  - 说明支持的 HTTP 库(requests, httpx, aiohttp)
  - 验证: 覆盖所有 HTTP 模式

- [x] 编写 `docs/scanners/module-symbols.md`
  - 分析 `example/scan-results/module-symbols.yaml`
  - 参考 `upcast/scanners/module_symbol.py`
  - 说明 imports 和 symbols 结构
  - 验证: 字段覆盖完整

## Phase 5: 运行时行为扫描器文档

- [x] 编写 `docs/scanners/blocking-operations.md`

  - 分析 `example/scan-results/blocking-operations.yaml`
  - 参考 `upcast/scanners/blocking_operations.py`
  - 说明各类阻塞操作分类(database, subprocess, synchronization, time_based)
  - 验证: 分类说明清晰

- [x] 编写 `docs/scanners/concurrency-patterns.md`

  - 分析 `example/scan-results/concurrency-patterns.yaml`
  - 参考 `upcast/scanners/concurrency.py`
  - 说明并发模式分类(threading, multiprocessing, asyncio)
  - 验证: 字段说明准确

- [x] 编写 `docs/scanners/exception-handlers.md`
  - 分析 `example/scan-results/exception-handlers.yaml`
  - 参考 `upcast/scanners/exception_handler.py`
  - 说明异常处理结构
  - 验证: 覆盖所有字段

## Phase 6: 专项扫描器文档

- [x] 编写 `docs/scanners/complexity-patterns.md`

  - 分析 `example/scan-results/complexity-patterns.yaml`
  - 参考 `upcast/scanners/complexity.py`
  - 说明圈复杂度计算规则
  - 验证: threshold 参数说明清晰

- [x] 编写 `docs/scanners/metrics.md`

  - 分析 `example/scan-results/metrics.yaml`
  - 参考 `upcast/scanners/metrics.py`
  - 说明 Prometheus 指标类型(Counter, Gauge, Histogram, Summary)
  - 验证: 字段说明完整

- [x] 编写 `docs/scanners/redis-usage.md`

  - 分析 `example/scan-results/redis-usage.yaml`
  - 参考 `upcast/scanners/redis_usage.py`
  - 说明 Redis 使用场景分类
  - 验证: 覆盖所有场景

- [x] 编写 `docs/scanners/signals.md`

  - 分析 `example/scan-results/signals.yaml`
  - 参考 `upcast/scanners/signals.py`
  - 说明 Django 和 Celery 信号处理
  - 验证: 字段说明准确

- [x] 编写 `docs/scanners/unit-tests.md`
  - 分析 `example/scan-results/unit-tests.yaml`
  - 参考 `upcast/scanners/unit_test.py`
  - 说明测试检测规则(pytest, unittest)
  - 验证: 覆盖所有字段

## Phase 7: 质量保证

- [x] 检查文档一致性

  - 确保所有文档遵循统一的结构规范
  - 检查示例代码和输出的准确性
  - 验证所有链接有效
  - 验证: 文档结构一致,无错误链接

- [x] 更新主 README

  - 在 README.md 中添加指向 docs/ 的链接
  - 说明用户可以在 docs/scanners/ 找到详细文档
  - 验证: 链接正确,说明清晰

- [x] 运行文档生成测试(如适用)
  - 如果有文档构建流程,验证构建成功
  - 检查生成的文档格式正确
  - 验证: 文档可正常访问

## 依赖关系

- Phase 2 依赖 Phase 1
- Phase 3-6 可以并行执行,但都依赖 Phase 1
- Phase 7 依赖所有前置阶段完成

## 验收标准

- [x] 所有 15 个扫描器都有对应的文档文件
- [x] 每个文档都包含完整的字段说明
- [x] 文档示例与实际输出一致
- [x] `docs/README.md` 索引完整
- [x] 主 README.md 包含文档链接
- [x] 所有链接都可访问
- [x] 文档格式统一,符合 Markdown 规范
