# Tasks: Define Scanner Data Models

## Overview

本文档列出实现"定义 Scanner 数据模型"所需的具体任务。

## Task Breakdown

### Phase 1: Setup (准备工作)

#### Task 1.1: 创建目录结构

- [ ] 创建 `upcast/models/` 目录
- [ ] 创建 `upcast/models/__init__.py`

**Estimated effort**: 5 minutes

#### Task 1.2: 移动 base 模型

- [ ] 将 `upcast/common/models.py` 的内容移动到 `upcast/models/base.py`
- [ ] 在 `upcast/common/models.py` 中添加 deprecation warning 和 re-export
- [ ] 更新 `upcast/common/export.py` 从新位置导入

**Estimated effort**: 15 minutes

**Dependencies**: Task 1.1

### Phase 2: Define Scanner Models (定义模型)

#### Task 2.1: Blocking Operations Models

- [ ] 创建 `upcast/models/blocking_ops.py`
- [ ] 定义 `BlockingOperation(BaseModel)`
- [ ] 定义 `BlockingOperationsSummary(ScannerSummary)`
- [ ] 定义 `BlockingOperationsOutput(ScannerOutput[...])`
- [ ] 添加完整的类型注解和文档字符串

**Estimated effort**: 30 minutes

**Dependencies**: Task 1.2

#### Task 2.2: Concurrency Pattern Models

- [ ] 创建 `upcast/models/concurrency.py`
- [ ] 定义 `ConcurrencyUsage(BaseModel)`
- [ ] 定义 `ConcurrencyPatternSummary(ScannerSummary)`
- [ ] 定义 `ConcurrencyPatternOutput(ScannerOutput[...])`
- [ ] 添加完整的类型注解和文档字符串

**Estimated effort**: 30 minutes

**Dependencies**: Task 1.2

#### Task 2.3: Complexity Models

- [ ] 创建 `upcast/models/complexity.py`
- [ ] 定义 `ComplexityResult(BaseModel)`
- [ ] 定义 `ComplexitySummary(ScannerSummary)`
- [ ] 定义 `ComplexityOutput(ScannerOutput[...])`
- [ ] 添加完整的类型注解和文档字符串

**Estimated effort**: 25 minutes

**Dependencies**: Task 1.2

#### Task 2.4: Django Model Scanner Models

- [ ] 创建 `upcast/models/django_models.py`
- [ ] 定义 `DjangoField(BaseModel)`
- [ ] 定义 `DjangoRelationship(BaseModel)`
- [ ] 定义 `DjangoModel(BaseModel)`
- [ ] 定义 `DjangoModelSummary(ScannerSummary)`
- [ ] 定义 `DjangoModelOutput(ScannerOutput[...])`
- [ ] 添加完整的类型注解和文档字符串

**Estimated effort**: 45 minutes

**Dependencies**: Task 1.2

#### Task 2.5: Django Settings Scanner Models

- [ ] 创建 `upcast/models/django_settings.py`
- [ ] 定义 `SettingsLocation(BaseModel)`
- [ ] 定义 `SettingsUsage(BaseModel)`
- [ ] 定义 `SettingDefinition(BaseModel)`
- [ ] 定义 `DynamicImport(BaseModel)`
- [ ] 定义 `SettingsModule(BaseModel)`
- [ ] 定义 `DjangoSettingsSummary(ScannerSummary)`
- [ ] 定义 `DjangoSettingsUsageOutput(ScannerOutput[...])`
- [ ] 定义 `DjangoSettingsDefinitionOutput(ScannerOutput[...])`
- [ ] 定义 `DjangoSettingsCombinedOutput(BaseModel)`
- [ ] 添加完整的类型注解和文档字符串

**Estimated effort**: 60 minutes (最复杂,有多种输出格式)

**Dependencies**: Task 1.2

#### Task 2.6: Django URL Scanner Models

- [ ] 创建 `upcast/models/django_urls.py`
- [ ] 定义 `UrlPattern(BaseModel)`
- [ ] 定义 `UrlModule(BaseModel)`
- [ ] 定义 `DjangoUrlSummary(ScannerSummary)`
- [ ] 定义 `DjangoUrlOutput(ScannerOutput[...])`
- [ ] 添加完整的类型注解和文档字符串

**Estimated effort**: 35 minutes

**Dependencies**: Task 1.2

#### Task 2.7: Environment Variable Scanner Models

- [ ] 创建 `upcast/models/env_vars.py`
- [ ] 定义 `EnvVarLocation(BaseModel)`
- [ ] 定义 `EnvVarInfo(BaseModel)`
- [ ] 定义 `EnvVarSummary(ScannerSummary)`
- [ ] 定义 `EnvVarOutput(ScannerOutput[...])`
- [ ] 添加完整的类型注解和文档字符串

**Estimated effort**: 30 minutes

**Dependencies**: Task 1.2

#### Task 2.8: Exception Handler Scanner Models

- [ ] 创建 `upcast/models/exceptions.py`
- [ ] 定义 `ExceptClause(BaseModel)`
- [ ] 定义 `ElseClause(BaseModel)`
- [ ] 定义 `FinallyClause(BaseModel)`
- [ ] 定义 `ExceptionHandler(BaseModel)`
- [ ] 定义 `ExceptionHandlerSummary(ScannerSummary)`
- [ ] 定义 `ExceptionHandlerOutput(ScannerOutput[...])`
- [ ] 添加完整的类型注解和文档字符串

**Estimated effort**: 40 minutes

**Dependencies**: Task 1.2

#### Task 2.9: HTTP Request Scanner Models

- [ ] 创建 `upcast/models/http_requests.py`
- [ ] 定义 `HttpRequestUsage(BaseModel)`
- [ ] 定义 `HttpRequestInfo(BaseModel)`
- [ ] 定义 `HttpRequestSummary(ScannerSummary)`
- [ ] 定义 `HttpRequestOutput(ScannerOutput[...])`
- [ ] 添加完整的类型注解和文档字符串

**Estimated effort**: 30 minutes

**Dependencies**: Task 1.2

#### Task 2.10: Prometheus Metrics Scanner Models

- [ ] 创建 `upcast/models/metrics.py`
- [ ] 定义 `MetricUsage(BaseModel)`
- [ ] 定义 `MetricInfo(BaseModel)`
- [ ] 定义 `PrometheusMetricSummary(ScannerSummary)`
- [ ] 定义 `PrometheusMetricOutput(ScannerOutput[...])`
- [ ] 添加完整的类型注解和文档字符串

**Estimated effort**: 35 minutes

**Dependencies**: Task 1.2

#### Task 2.11: Signal Scanner Models

- [ ] 创建 `upcast/models/signals.py`
- [ ] 从 `upcast/scanners/signals.py` 复制模型定义:
  - `SignalUsage(BaseModel)`
  - `SignalInfo(BaseModel)`
  - `SignalSummary(ScannerSummary)`
  - `SignalOutput(ScannerOutput[...])`
- [ ] 确保文档字符串完整

**Estimated effort**: 20 minutes (已有实现,只需移动)

**Dependencies**: Task 1.2

#### Task 2.12: Unit Test Scanner Models

- [ ] 创建 `upcast/models/unit_tests.py`
- [ ] 定义 `TargetModule(BaseModel)`
- [ ] 定义 `UnitTestInfo(BaseModel)`
- [ ] 定义 `UnitTestSummary(ScannerSummary)`
- [ ] 定义 `UnitTestOutput(ScannerOutput[...])`
- [ ] 添加完整的类型注解和文档字符串

**Estimated effort**: 30 minutes

**Dependencies**: Task 1.2

### Phase 3: Integration (集成)

#### Task 3.1: 更新 models/**init**.py

- [ ] 从所有模型文件导入类
- [ ] 定义 `__all__` 列表
- [ ] 添加模块级文档字符串

**Estimated effort**: 20 minutes

**Dependencies**: Tasks 2.1-2.12

#### Task 3.2: 更新 scanners/signals.py

- [ ] 修改 import 语句,从 `upcast.models.signals` 导入模型
- [ ] 删除 signals.py 中的模型定义
- [ ] 确保功能不变

**Estimated effort**: 15 minutes

**Dependencies**: Task 2.11, Task 3.1

#### Task 3.3: 更新 common/scanner_base.py

- [ ] 修改 import 从 `upcast.models.base` 导入
- [ ] 确保泛型类型仍然正确

**Estimated effort**: 10 minutes

**Dependencies**: Task 1.2

### Phase 4: Quality Assurance (质量保证)

#### Task 4.1: 代码检查

- [ ] 运行 `ruff check upcast/models/`
- [ ] 修复所有 linting 错误
- [ ] 运行 `ruff format upcast/models/`

**Estimated effort**: 20 minutes

**Dependencies**: Task 3.1

#### Task 4.2: 类型检查

- [ ] 运行 `mypy upcast/models/`
- [ ] 修复所有类型错误

**Estimated effort**: 30 minutes

**Dependencies**: Task 4.1

#### Task 4.3: 测试验证

- [ ] 运行现有测试套件: `uv run pytest`
- [ ] 确保所有测试通过(应该通过,因为没修改 scanner 实现)
- [ ] 验证 signals scanner 的测试仍然通过

**Estimated effort**: 15 minutes

**Dependencies**: Task 3.2

#### Task 4.4: 导入测试

- [ ] 创建简单脚本测试所有模型可以成功导入
- [ ] 测试: `from upcast.models import *`
- [ ] 测试向后兼容导入: `from upcast.common.models import ScannerOutput`

**Estimated effort**: 10 minutes

**Dependencies**: Task 3.1

### Phase 5: Documentation (文档)

#### Task 5.1: 更新 README

- [ ] 在 README.md 中添加"Data Models"部分
- [ ] 说明 `upcast/models/` 的用途
- [ ] 提供简单的使用示例

**Estimated effort**: 20 minutes

**Dependencies**: Task 4.3

#### Task 5.2: 添加模型使用示例

- [ ] 在 `upcast/models/__init__.py` 的 docstring 中添加使用示例
- [ ] 展示如何创建模型实例
- [ ] 展示如何转换为 dict

**Estimated effort**: 15 minutes

**Dependencies**: Task 3.1

## Execution Order

**建议的执行顺序**:

1. Phase 1 (Setup): Tasks 1.1 → 1.2
2. Phase 2 (Models): Tasks 2.1-2.12 可以并行或按任意顺序
   - 建议先做 Task 2.11 (Signal Models),因为已有实现
   - 然后做简单的: 2.3, 2.7, 2.9
   - 最后做复杂的: 2.4, 2.5, 2.6, 2.8
3. Phase 3 (Integration): Tasks 3.1 → 3.2, 3.3
4. Phase 4 (QA): Tasks 4.1 → 4.2 → 4.3 → 4.4
5. Phase 5 (Docs): Tasks 5.1, 5.2 可以并行

## Total Estimated Effort

- Phase 1: 20 minutes
- Phase 2: 6 hours (各个模型定义)
- Phase 3: 45 minutes
- Phase 4: 1 hour 15 minutes
- Phase 5: 35 minutes

**Total: ~8.5 hours**

## Success Criteria Checklist

- [ ] `upcast/models/` 目录创建,包含 13 个文件(base.py + 12 个 scanner 模型文件)
- [ ] 所有 12 个 scanner 都有对应的完整 Pydantic 模型定义
- [ ] 所有模型继承自 `ScannerOutput` 和 `ScannerSummary`
- [ ] 所有字段都有类型注解和 `Field(description=...)`
- [ ] `ruff check` 和 `mypy` 无错误
- [ ] `from upcast.models import *` 成功
- [ ] `from upcast.common.models import ScannerOutput` 仍然有效(向后兼容)
- [ ] 所有现有测试通过 (701/701)
- [ ] signals scanner 测试通过(验证模型移动后功能正常)

## Risk Management

### Risk: 模型定义与实际输出不匹配

**Mitigation**:

- 每个模型都基于对应 scanner 的 export.py 实际输出
- 在 Task 4.4 中添加导入测试,确保结构正确

### Risk: 向后兼容性破坏

**Mitigation**:

- 保留 `upcast/common/models.py` 并 re-export
- Task 4.3 运行所有测试确保没有破坏

### Risk: 时间估算不准确

**Mitigation**:

- 估算包含了 buffer
- 如果超时,可以分多次完成
- Phase 2 的任务可以增量完成

## Notes

- 本阶段**不修改** scanner 的实现代码
- 本阶段**不修改** scanner 的 export 函数
- 本阶段**不修改** scanner 的 CLI
- 本阶段**不添加**单元测试(等 scanner 迁移时再加)
- 本阶段只定义数据模型,为未来的 scanner 迁移和 Analyzer 开发奠定基础
