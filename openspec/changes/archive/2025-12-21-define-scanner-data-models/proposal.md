# Proposal: Define Scanner Data Models

## Metadata

- **Change ID**: `define-scanner-data-models`
- **Status**: PROPOSED
- **Created**: 2025-12-21
- **Author**: Assistant
- **Related Issues**: N/A

## Problem Statement

当前项目中有 12 个扫描器用于分析 Python 代码的各个方面(Django models、环境变量、HTTP 请求、并发模式等)。目前存在以下问题:

1. **数据格式不统一**: 虽然所有 scanner 都输出 `{summary: {...}, results: {...}}` 结构,但使用的是普通 dict,缺乏类型安全和验证
2. **缺乏复用性**: 每个 scanner 自己定义输出格式,没有共享的数据模型抽象
3. **不利于未来扩展**: 计划引入分析器(Analyzer)模块来处理 scanner 结果,但缺乏标准化的数据模型会增加集成难度
4. **维护困难**: 输出结构分散在各个 scanner 的 export.py 中,难以统一管理和演进

当前只有 `upcast/scanners/signals.py` 使用了新的 Pydantic 模型架构(`SignalOutput`, `SignalSummary`, `SignalInfo`),作为成功的示范。其他 11 个旧 scanner 仍使用 dict-based 输出。

## Proposed Solution

### 核心方案

1. **创建 `upcast/models/` 目录**:按功能组织所有 scanner 的 Pydantic 数据模型,便于 scanner 和未来的 analyzer 共享使用

2. **定义标准化数据模型**:为所有 12 个 scanner 定义完整的 Pydantic 模型,遵循以下模式:

   ```python
   class XxxScanSummary(ScannerSummary):
       """扩展基础 summary,添加 scanner 特定的统计字段"""
       ...

   class XxxResult(BaseModel):
       """具体的扫描结果项"""
       ...

   class XxxOutput(ScannerOutput[list[XxxResult] | dict[str, XxxResult]]):
       """完整的扫描器输出"""
       summary: XxxScanSummary
       results: ...  # 类型取决于具体 scanner
   ```

3. **向后兼容策略**:

   - 新模型使用 Pydantic 对象作为主要输出格式
   - 调用者可以通过 `.model_dump()` 或 `.to_dict()` 转换为 dict
   - 不破坏现有的 export 函数签名(在后续迁移阶段才修改实现)

4. **目录组织**:
   ```
   upcast/models/
   ├── __init__.py                # 导出所有模型
   ├── base.py                    # 已有的 ScannerSummary, ScannerOutput(从 common/models.py 移动)
   ├── blocking_operations.py     # BlockingOperationsScanOutput, BlockingOperationsSummary, etc.
   ├── concurrency.py             # ConcurrencyPatternOutput, ConcurrencyPattern, etc.
   ├── complexity.py              # ComplexityOutput, ComplexityResult, etc.
   ├── django_models.py     # DjangoModelOutput, DjangoModel, DjangoField, etc.
   ├── django_settings.py   # DjangoSettingsOutput, SettingsDefinition, SettingsUsage, etc.
   ├── django_urls.py       # DjangoUrlOutput, UrlPattern, etc.
   ├── env_vars.py          # EnvVarOutput, EnvVarInfo, etc.
   ├── exceptions.py        # ExceptionHandlerOutput, ExceptionHandler, ExceptClause, etc.
   ├── http_requests.py     # HttpRequestOutput, HttpRequest, etc.
   ├── metrics.py           # PrometheusMetricOutput, MetricInfo, MetricUsage, etc.
   ├── signals.py           # SignalOutput, SignalInfo, SignalUsage, etc.(从 scanners/signals.py 移动)
   └── unit_tests.py        # UnitTestOutput, UnitTestInfo, TargetModule, etc.
   ```

### 设计原则

1. **类型安全**: 使用 Pydantic v2 提供运行时验证和类型提示
2. **可扩展性**: 基类使用 `extra="allow"` 允许 scanner 特定的元数据
3. **一致性**: 所有 summary 继承 `ScannerSummary`,所有 output 继承 `ScannerOutput[T]`
4. **文档化**: 每个字段使用 `Field(description=...)` 提供清晰的文档
5. **验证约束**: 使用 Pydantic 的验证器(如 `ge=0` 确保计数非负)

## Benefits

1. **类型安全**: 编译时和运行时类型检查,减少错误
2. **数据验证**: 自动验证输出数据的完整性和正确性
3. **更好的 IDE 支持**: 类型提示带来更好的自动补全和重构能力
4. **便于集成**: 未来的 Analyzer 模块可以直接使用这些模型,无需解析 dict
5. **统一维护**: 所有数据模型集中管理,便于演进和文档化
6. **向后兼容**: 通过 `.model_dump()` 保持与现有代码的兼容

## Risks and Mitigations

### Risk 1: 模型定义工作量大

**Mitigation**:

- 已有 11 个 scanner 的 export.py 作为参考,结构清晰
- signals.py 已有成功的 Pydantic 模型实现作为模板
- 本提案只定义模型,不涉及 scanner 实现迁移

### Risk 2: 可能影响现有 scanner 性能

**Mitigation**:

- Pydantic v2 性能已大幅提升,接近原生 Python
- 模型定义不会立即影响现有 scanner(仍使用 dict)
- 可以在后续逐步迁移时进行性能测试

### Risk 3: 模型设计可能不够通用

**Mitigation**:

- 基于现有 11 个 scanner 的实际输出结构设计
- 使用 `extra="allow"` 允许扩展
- 在设计阶段充分考虑未来 Analyzer 的需求

## Alternatives Considered

### Alternative 1: 保持现状,使用 dict

**Rejected because**:

- 缺乏类型安全,容易出错
- 不利于 Analyzer 集成
- 维护困难

### Alternative 2: 模型分散在各 scanner 目录

**Rejected because**:

- 不利于 Analyzer 复用这些模型
- 增加模块间的耦合
- 不便于统一管理

### Alternative 3: 使用 dataclasses 而非 Pydantic

**Rejected because**:

- 缺乏数据验证
- 缺乏 JSON/YAML 序列化支持
- Pydantic 已被 signals.py 采用,保持一致性

## Implementation Scope

### In Scope

- 为所有 12 个 scanner 定义完整的 Pydantic 数据模型
- 创建 `upcast/models/` 目录并组织模型文件
- 从 `upcast/common/models.py` 移动基类到 `upcast/models/base.py`
- 从 `upcast/scanners/signals.py` 提取模型到 `upcast/models/signals.py`
- 为每个模型编写完整的类型注解和文档字符串
- 更新 `upcast/models/__init__.py` 导出所有模型

### Out of Scope

- 修改现有 scanner 的实现(将在后续 change 中进行)
- 修改现有 scanner 的 CLI 或 export 函数
- 实现 Analyzer 模块(将在后续 change 中进行)
- 编写数据模型的单元测试(在实际使用时再添加)

## Success Criteria

1. ✅ `upcast/models/` 目录创建,包含 13 个模型文件
2. ✅ 所有 12 个 scanner 都有对应的 Pydantic 模型定义
3. ✅ 所有模型继承自 `ScannerOutput` 和 `ScannerSummary`
4. ✅ 所有字段都有类型注解和描述文档
5. ✅ 代码通过 ruff 和 mypy 检查
6. ✅ 模型可以成功导入: `from upcast.models import *`
7. ✅ 现有测试不受影响(因为不修改 scanner 实现)

## Open Questions

1. ~~是否需要为模型编写单元测试?~~ → 暂不需要,等实际使用时再添加
2. ~~是否需要提供模型的使用示例?~~ → 在设计文档中提供
3. ~~如何处理复杂的嵌套结构(如 django_settings 的多种输出格式)?~~ → 使用 Union 类型或多个模型
