# Upcast Scanner Documentation

本文档提供了 Upcast 所有扫描器的详细规则说明和字段参考。每个扫描器都有独立的文档页面，详细解释输出格式和字段含义。

## 扫描器列表

Upcast 提供 15 个专业的静态代码分析扫描器，用于分析 Python 项目的各个方面：

### Django 框架扫描器

| 扫描器          | 命令                   | 说明                                     | 文档                                              |
| --------------- | ---------------------- | ---------------------------------------- | ------------------------------------------------- |
| Django Models   | `scan-django-models`   | 分析 Django 模型定义、字段、关系和元数据 | [django-models.md](scanners/django-models.md)     |
| Django Settings | `scan-django-settings` | 扫描 Django 配置定义和使用               | [django-settings.md](scanners/django-settings.md) |
| Django URLs     | `scan-django-urls`     | 分析 Django URL 配置和路由               | [django-urls.md](scanners/django-urls.md)         |

### 通用代码分析扫描器

| 扫描器                | 命令                  | 说明                                               | 文档                                            |
| --------------------- | --------------------- | -------------------------------------------------- | ----------------------------------------------- |
| Environment Variables | `scan-env-vars`       | 检测环境变量使用                                   | [env-vars.md](scanners/env-vars.md)             |
| Logging               | `scan-logging`        | 分析日志调用（logging, loguru, structlog, Django） | [logging.md](scanners/logging.md)               |
| HTTP Requests         | `scan-http-requests`  | 检测 HTTP 请求（requests, httpx, aiohttp）         | [http-requests.md](scanners/http-requests.md)   |
| Module Symbols        | `scan-module-symbols` | 提取模块导入和符号定义                             | [module-symbols.md](scanners/module-symbols.md) |

### 运行时行为分析扫描器

| 扫描器               | 命令                        | 说明                                                | 文档                                                        |
| -------------------- | --------------------------- | --------------------------------------------------- | ----------------------------------------------------------- |
| Blocking Operations  | `scan-blocking-operations`  | 识别阻塞操作（sleep, 锁, 数据库查询）               | [blocking-operations.md](scanners/blocking-operations.md)   |
| Concurrency Patterns | `scan-concurrency-patterns` | 分析并发模式（threading, multiprocessing, asyncio） | [concurrency-patterns.md](scanners/concurrency-patterns.md) |
| Exception Handlers   | `scan-exception-handlers`   | 分析异常处理结构                                    | [exception-handlers.md](scanners/exception-handlers.md)     |

### 专项分析扫描器

| 扫描器                | 命令                       | 说明                             | 文档                                                      |
| --------------------- | -------------------------- | -------------------------------- | --------------------------------------------------------- |
| Cyclomatic Complexity | `scan-complexity-patterns` | 计算函数圈复杂度                 | [complexity-patterns.md](scanners/complexity-patterns.md) |
| Prometheus Metrics    | `scan-metrics`             | 检测 Prometheus 指标定义         | [metrics.md](scanners/metrics.md)                         |
| Redis Usage           | `scan-redis-usage`         | 分析 Redis 使用模式              | [redis-usage.md](scanners/redis-usage.md)                 |
| Signals               | `scan-signals`             | 分析 Django 和 Celery 信号       | [signals.md](scanners/signals.md)                         |
| Unit Tests            | `scan-unit-tests`          | 检测单元测试（pytest, unittest） | [unit-tests.md](scanners/unit-tests.md)                   |

## 通用选项

所有扫描器都支持以下通用命令行选项：

### 文件过滤选项

```bash
# 包含特定模式的文件
--include "app/**"              # 包含 app 目录下的所有文件
--include "core/**"             # 可以多次使用

# 排除特定模式的文件
--exclude "tests/**"            # 排除 tests 目录
--exclude "migrations/**"       # 排除 Django migrations
--exclude "**/*_test.py"        # 排除测试文件

# 禁用默认排除规则
--no-default-excludes          # 不排除 venv/, build/, dist/ 等
```

**默认排除模式**（使用 `--no-default-excludes` 可禁用）：

- `venv/`, `.venv/`, `env/` - 虚拟环境
- `__pycache__/`, `*.pyc` - Python 缓存
- `.git/`, `.svn/` - 版本控制
- `build/`, `dist/`, `*.egg-info/` - 构建产物
- `node_modules/` - Node.js 依赖
- `migrations/` - Django 数据库迁移

### 输出选项

```bash
# 输出到文件
-o <file>, --output <file>     # 保存结果到文件

# 输出格式
--format yaml                   # YAML 格式（默认）
--format json                   # JSON 格式
--format markdown               # Markdown 格式

# Markdown 选项
--markdown-language en          # 英文（默认）
--markdown-language zh          # 中文
--markdown-title "标题"         # 自定义标题
```

### 其他选项

```bash
-v, --verbose                   # 详细输出，显示调试信息
```

## 输出格式

所有扫描器的输出都遵循统一的结构：

```yaml
metadata:
  # 扫描器元数据（可选）
  scanner_name: <scanner_name>
  # 其他元数据字段...

results:
  # 扫描结果
  # 具体结构因扫描器而异，详见各扫描器文档
```

### YAML 格式

```bash
upcast scan-env-vars . -o results.yaml
```

### JSON 格式

```bash
upcast scan-env-vars . --format json -o results.json
```

### Markdown 格式

```bash
upcast scan-env-vars . --format markdown -o report.md
```

## 使用示例

### 基础扫描

```bash
# 扫描当前目录的环境变量
upcast scan-env-vars .

# 扫描指定项目
upcast scan-django-models /path/to/django/project

# 输出到文件
upcast scan-logging ./src -o logging-report.yaml
```

### 文件过滤

```bash
# 只扫描特定目录
upcast scan-http-requests . --include "app/**" --include "core/**"

# 排除测试文件
upcast scan-complexity-patterns . --exclude "tests/**" --exclude "**/*_test.py"

# 组合使用
upcast scan-metrics . \
  --include "src/**" \
  --exclude "**/*_test.py" \
  --exclude "migrations/**"
```

### 多格式输出

```bash
# JSON 格式
upcast scan-unit-tests ./tests --format json -o tests.json

# Markdown 报告（中文）
upcast scan-blocking-operations . \
  --format markdown \
  --markdown-language zh \
  --markdown-title "阻塞操作分析报告" \
  -o report.md
```

## 真实示例

项目的 [`example/scan-results/`](../example/scan-results/) 目录包含基于 [blueking-paas 项目](https://github.com/TencentBlueKing/blueking-paas) 的真实扫描输出示例。

每个扫描器都有对应的示例文件：

- [`blocking-operations.yaml`](../example/scan-results/blocking-operations.yaml)
- [`complexity-patterns.yaml`](../example/scan-results/complexity-patterns.yaml)
- [`concurrency-patterns.yaml`](../example/scan-results/concurrency-patterns.yaml)
- [`django-models.yaml`](../example/scan-results/django-models.yaml)
- [`django-settings.yaml`](../example/scan-results/django-settings.yaml)
- [`django-urls.yaml`](../example/scan-results/django-urls.yaml)
- [`env-vars.yaml`](../example/scan-results/env-vars.yaml)
- [`exception-handlers.yaml`](../example/scan-results/exception-handlers.yaml)
- [`http-requests.yaml`](../example/scan-results/http-requests.yaml)
- [`logging.yaml`](../example/scan-results/logging.yaml)
- [`metrics.yaml`](../example/scan-results/metrics.yaml)
- [`module-symbols.yaml`](../example/scan-results/module-symbols.yaml)
- [`redis-usage.yaml`](../example/scan-results/redis-usage.yaml)
- [`signals.yaml`](../example/scan-results/signals.yaml)
- [`unit-tests.yaml`](../example/scan-results/unit-tests.yaml)

## 扫描器文档结构

每个扫描器的详细文档都遵循统一的结构：

1. **Overview** - 扫描器概述和使用场景
2. **Command Usage** - 命令行使用说明和选项
3. **Output Format** - 输出结构说明
4. **Field Reference** - 完整的字段参考
   - 字段名称
   - 数据类型
   - 必填/可选
   - 取值范围
   - 字段含义
5. **Examples** - 实际输出示例
6. **Notes** - 特殊说明和注意事项

## 下一步

选择您感兴趣的扫描器，查看其详细文档：

- 分析 Django 项目？从 [django-models.md](scanners/django-models.md) 开始
- 检查环境变量？查看 [env-vars.md](scanners/env-vars.md)
- 优化代码复杂度？参考 [complexity-patterns.md](scanners/complexity-patterns.md)
- 分析并发模式？阅读 [concurrency-patterns.md](scanners/concurrency-patterns.md)

## 技术文档

除了扫描器文档外，我们还提供以下技术文档：

- **[类型推导机制](type-inference.md)** - Upcast 静态类型和值推导系统的详细说明
  - 推导能力分级（可推导/部分推导/不可推导）
  - 核心 API 使用指南
  - 支持的 Python 语法覆盖
  - 实际应用场景和最佳实践

## 相关资源

- [主 README](../README.md) - 项目概述和快速开始
- [示例输出](../example/scan-results/) - 真实扫描结果
- [GitHub 仓库](https://github.com/mrlyc/upcast) - 源代码和问题追踪
