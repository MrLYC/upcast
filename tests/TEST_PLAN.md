# Follow-up Scanner Regression Matrix

本文件只记录 **2026-04-22 follow-up scanner improvements** 的后续执行矩阵。
目标不是重新规划全部测试体系，而是把本轮尚未落地、但已判断为有价值的改进项，收敛成可逐项执行的 TDD 入口。

关联执行计划：`docs/plans/2026-04-22-scanner-follow-up-improvements.md`

## 执行规则

- 一次只做一个 task。
- 每个 task 都必须先写失败测试，再写最小实现。
- 每个 task 绿灯后立即提交，再开始下一项。
- 非同一 scanner 的改动不得混入同一提交。
- `complexity.comment_lines` 只有在 red test 可稳定复现时才执行。

## 回归矩阵

| Task | Scanner         | 改进摘要                                                                     | Target test file(s)                                                                                                                                                                                                                                                           | Target fixture file                                                         | 关键断言                                                                                                                                                 | Schema changes       |
| ---- | --------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- |
| 1    | planning        | 建立剩余建议的回归矩阵与 fixture inventory                                   | `tests/TEST_PLAN.md`                                                                                                                                                                                                                                                          | N/A                                                                         | 每个 deferred item 都映射到唯一 test 入口与 fixture 落点                                                                                                 | No                   |
| 2    | http_requests   | 排除 `requests_mock` 等 mock 注册调用；识别真实 `httpx` / `aiohttp` 请求模式 | `tests/test_http_request_scanner/test_edge_cases.py`<br>`tests/test_http_request_scanner/test_scanner_integration.py`<br>`tests/test_http_request_scanner/test_url_patterns.py`                                                                                               | `tests/test_http_request_scanner/fixtures/mock_vs_real_requests.py`         | mock 注册不应产生请求结果；真实 `httpx.Client` / `httpx.AsyncClient` / 可静态识别的 `aiohttp.ClientSession` 调用应被扫描到                               | No                   |
| 3    | concurrency     | 为并发扫描器补上 Celery task / invocation 覆盖                               | `tests/test_concurrency_pattern_scanner/test_edge_cases.py`<br>`tests/test_concurrency_pattern_scanner/test_integration.py`<br>`tests/test_concurrency_integration.py`                                                                                                        | `tests/test_concurrency_pattern_scanner/fixtures/celery_patterns.py`        | `@shared_task`、`@app.task`、`.delay()`、`.apply_async()` 能落入 `celery` bucket，且不影响 threading / multiprocessing / asyncio 分类                    | No                   |
| 4    | logging         | 提升敏感字段识别；修正 `logger_name` 与 message template 提取                | `tests/test_logging_scanner/test_edge_cases.py`<br>`tests/test_logging_scanner/test_logger_names.py`<br>`tests/test_logging_scanner/test_scanner.py`                                                                                                                          | `tests/test_logging_scanner/fixtures/sensitive_logging_patterns.py`         | `headers/token/password/cookie/auth/secret` 命中敏感检测；`logging.getLogger("name")` 解析出正确 logger_name；`.format()` / `%` 保留模板串而非完整表达式 | No                   |
| 5    | redis_usage     | 扩展 Redis / cache 操作覆盖并修正 TTL 语义                                   | `tests/test_redis_usage_scanner/test_operations.py`<br>`tests/test_redis_usage_scanner/test_edge_cases.py`<br>`tests/test_redis_usage_scanner/test_config_detection.py`                                                                                                       | `tests/test_redis_usage_scanner/fixtures/ttl_patterns.py`                   | `cache.add/delete_many/clear/touch/incr/decr` 等操作被识别；动态 TTL 不再被误判为 missing TTL；仅在现有模型可承载时扩展配置识别                          | Possibly additive    |
| 6    | django_urls     | 丰富 URL 输出：`file` / `line` / `view` / `converter` / `full_path`          | `tests/test_django_urls_scanner/test_models.py`<br>`tests/test_django_urls_scanner/test_edge_cases.py`<br>`tests/test_django_urls_scanner/test_converters.py`<br>`tests/test_django_urls_scanner/test_integration.py`<br>`tests/test_django_urls_scanner/test_drf_routers.py` | `tests/test_django_urls_scanner/fixtures/nested_urls.py`                    | 路由项带 `file` 与 `line`；可静态解析时带 view 信息；`<int:pk>` 等 converter 被提取；嵌套 `include()` 生成完整 `full_path`                               | Yes                  |
| 7    | module_symbols  | 把 methods / function args 从扁平字符串提升为结构化元数据                    | `tests/test_module_symbol_scanner/test_classes.py`<br>`tests/test_module_symbol_scanner/test_functions.py`<br>`tests/test_module_symbol_scanner/test_models.py`<br>`tests/test_module_symbol_scanner/test_integration.py`                                                     | `tests/test_module_symbol_scanner/fixtures/rich_symbols.py`                 | method 至少包含 `line`、`args`、decorators；函数参数被提取；现有 imports / variables / relative imports 行为不回退                                       | Yes                  |
| 8    | unit_tests      | 为单测扫描器补充 class / fixture / mark / parametrize 结构                   | `tests/test_unit_test_scanner/test_edge_cases.py`<br>`tests/test_unit_test_scanner/test_targets.py`<br>`tests/test_unit_test_scanner/test_assertions.py`<br>`tests/test_unit_test_scanner/test_integration.py`<br>`tests/test_unit_test_scanner/test_models.py`               | `tests/test_unit_test_scanner/fixtures/test_structure_patterns.py`          | 能识别 `class TestXxx`、`@pytest.fixture`、`pytest.mark.*`、`pytest.mark.parametrize`；已有 `assert_count` / targets 行为保持                            | Yes                  |
| 9    | django_settings | 在有界范围内提升标准 settings 与 tuple/list comment 处理精度                 | `tests/test_django_settings_scanner/test_edge_cases.py`<br>`tests/test_django_settings_scanner/test_integration.py`<br>`tests/test_django_settings_scanner/test_type_inference.py`<br>`tests/test_django_settings_scanner/test_models.py`                                     | `tests/test_django_settings_scanner/fixtures/standard_settings.py`          | `ROOT_URLCONF`、`TEMPLATES`、`WSGI_APPLICATION`、`ALLOWED_HOSTS`、`STATIC_URL`、`MEDIA_URL` 被正确识别；tuple/list 中注释不再产出 `null` 噪声            | Possibly additive    |
| 10   | signals         | 提升 signal sender 与 custom signal definition 检测                          | `tests/test_signals_scanner/test_integration.py`<br>`tests/test_signals_scanner/test_models.py`                                                                                                                                                                               | `tests/test_signals_scanner/fixtures/custom_signal_patterns.py`             | `.send()` / `.send_robust()` 的 signal usage 被识别；`Signal()` 定义被识别；非 signal 对象的普通 `.send()` 不应误报                                      | Possibly additive    |
| 11   | complexity      | 仅在可稳定复现时修复 `comment_lines` 丢失                                    | `tests/test_cyclomatic_complexity_scanner/test_code_utils.py`<br>`tests/test_cyclomatic_complexity_scanner/test_scanner_integration.py`<br>`tests/test_scanners/test_complexity.py`                                                                                           | `tests/test_cyclomatic_complexity_scanner/fixtures/comment_preservation.py` | 新增 red test 必须先证明 comment_lines 当前确实丢失；若无法复现，则本 task 终止并不实现                                                                  | No unless reproduced |

## 推荐执行顺序

1. Task 1：先固定回归矩阵与执行边界。
2. Task 2-5：先做高 ROI、低耦合的精度修复（HTTP / Concurrency / Logging / Redis）。
3. Task 6-8：再做需要模型扩展的 schema enrichments（Django URLs / Module Symbols / Unit Tests）。
4. Task 9-10：最后做高风险但仍有价值的 bounded improvements（Django Settings / Signals）。
5. Task 11：仅在复现成功后进入实现。

## 提交边界

- Task 1 为文档提交，只包含：
  - `tests/TEST_PLAN.md`
  - `docs/plans/2026-04-22-scanner-follow-up-improvements.md`
- Task 2-11 各自单独提交。
- 测试文件与对应实现必须在同一提交中。

## 完成定义

某一 task 只有在满足以下条件后才算完成：

1. 新增测试先 red，并且失败原因正确。
2. 最小实现后目标测试转绿。
3. 扩面到该 scanner 的 focused suite 后仍为绿。
4. 工作树只剩下该 task 对应改动。
5. 已提交，再开始下一项。
