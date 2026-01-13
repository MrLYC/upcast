# Create Scanner Documentation

## Why

目前项目虽然提供了 15 个扫描命令,并且在 README.md 中有基本的使用说明,但缺少详细的输出格式说明和字段解释文档。这导致:

1. **用户理解困难**: 用户看到扫描结果的 YAML 输出后,不清楚每个字段的具体含义和取值规则
2. **文档分散**: 扫描规则和字段说明分散在代码实现中,没有统一的文档参考
3. **维护成本高**: 新增或修改扫描器时,缺少规范的文档结构来指导文档更新
4. **集成困难**: 下游工具或服务集成 upcast 扫描结果时,需要阅读源代码才能理解数据结构

通过在 `docs/` 目录下为每个扫描器创建详细的规则文档,可以:

- 提供清晰的字段说明和取值语义
- 建立统一的文档规范
- 降低用户学习成本
- 方便下游工具集成

## What Changes

### 新增文档文件

在 `docs/scanners/` 目录下为每个扫描器创建独立的文档文件:

1. `blocking-operations.md` - 阻塞操作扫描器
2. `complexity-patterns.md` - 复杂度模式扫描器
3. `concurrency-patterns.md` - 并发模式扫描器
4. `django-models.md` - Django 模型扫描器
5. `django-settings.md` - Django 配置扫描器
6. `django-urls.md` - Django URL 扫描器
7. `env-vars.md` - 环境变量扫描器
8. `exception-handlers.md` - 异常处理器扫描器
9. `http-requests.md` - HTTP 请求扫描器
10. `logging.md` - 日志扫描器
11. `metrics.md` - Prometheus 指标扫描器
12. `module-symbols.md` - 模块符号扫描器
13. `redis-usage.md` - Redis 使用扫描器
14. `signals.md` - 信号扫描器
15. `unit-tests.md` - 单元测试扫描器

### 文档结构规范

每个文档应包含以下标准章节:

1. **Overview** - 扫描器概述和用途
2. **Command Usage** - 命令行使用说明
3. **Output Format** - 输出格式说明
4. **Field Reference** - 详细的字段参考
   - 顶层结构说明
   - metadata 字段说明
   - results 字段说明
   - 每个字段的类型、必填性、取值范围、默认值等
5. **Examples** - 实际示例(引用 example/scan-results 中的真实输出)
6. **Notes** - 特殊说明和注意事项

### 文档索引

创建 `docs/README.md` 作为文档入口,包含:

- 扫描器列表和简介
- 各扫描器文档的链接
- 通用概念说明(如文件过滤选项等)

## Non-Goals

- 不修改现有的 README.md 主要内容结构
- 不改变扫描器的实现逻辑或输出格式
- 不涉及新功能开发
