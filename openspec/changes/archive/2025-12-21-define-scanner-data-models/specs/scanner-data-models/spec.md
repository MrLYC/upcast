# Spec: Scanner Data Models

## Capability

**Name**: Scanner Data Models

**ID**: `scanner-data-models`

**Description**: Standardized Pydantic data models for all scanner outputs, enabling type-safe data exchange between scanners and future analyzer modules.

## Context

### Purpose

提供统一的、类型安全的数据模型来表示所有 scanner 的输出结果。这些模型:

1. 为 scanner 输出提供标准化结构
2. 支持类型检查和运行时验证
3. 便于未来的 analyzer 模块消费 scanner 结果
4. 提供清晰的 API 契约和文档

### Scope

- ✅ 定义所有 12 个 scanner 的 Pydantic 数据模型
- ✅ 提供基础模型类(`ScannerSummary`, `ScannerOutput[T]`)
- ✅ 组织模型到 `upcast/models/` 目录
- ❌ 不修改现有 scanner 的实现(由后续 change 处理)
- ❌ 不包含数据模型的单元测试(在 scanner 迁移时添加)

### Related Capabilities

- `common-utilities`: 提供基础工具类,模型将使用通用的 export 函数
- `cli-interface`: Scanner CLI 未来可以使用这些模型
- 未来的 `analyzer-framework`: 将基于这些模型构建

## Requirements

### NEW Requirements

#### R1: Base Model Classes

**ID**: `scanner-data-models-base`

**Description**: 提供所有 scanner 模型的基类

**Details**:

- 定义 `ScannerSummary(BaseModel)`:
  - 必需字段: `total_count: int`, `files_scanned: int`
  - 可选字段: `scan_duration_ms: int | None`
  - 使用 `extra="forbid"` 和 `frozen=True`
  - 所有计数字段使用 `Field(ge=0)` 约束
- 定义 `ScannerOutput[T](BaseModel, Generic[T])`:
  - 必需字段: `summary: ScannerSummary`, `results: T`
  - 可选字段: `metadata: dict[str, Any]`
  - 使用 `extra="allow"` 允许扩展元数据
  - 提供 `to_dict()` 方法用于向后兼容
- 位置: `upcast/models/base.py`

**Priority**: CRITICAL

**Validation**:

```python
from upcast.models.base import ScannerSummary, ScannerOutput

# Can create instances
summary = ScannerSummary(total_count=10, files_scanned=5)
assert summary.total_count == 10

# Type checking works
output: ScannerOutput[list[dict]] = ScannerOutput(
    summary=summary,
    results=[{"test": 1}]
)

# to_dict() works
data = output.to_dict()
assert isinstance(data, dict)
```

---

#### R2: Blocking Operations Models

**ID**: `scanner-data-models-blocking-ops`

**Description**: 阻塞操作扫描器的数据模型

**Details**:

- `BlockingOperation(BaseModel)`: 单个阻塞操作
  - 字段: file, line, column, category, operation, statement, function, class_name
- `BlockingOperationsSummary(ScannerSummary)`: 扩展 summary
  - 额外字段: `by_category: dict[str, int]`
- `BlockingOperationsOutput(ScannerOutput[dict[str, list[BlockingOperation]]])`: 完整输出
  - `results` 使用 `alias="operations"` 匹配现有输出
- 位置: `upcast/models/blocking_operations.py`

**Priority**: HIGH

**Validation**:

```python
from upcast.models.blocking_operations import BlockingOperationsOutput

output = BlockingOperationsOutput(...)
assert "operations" in output.to_dict()  # alias works
assert isinstance(output.results, dict)
```

---

#### R3: Concurrency Pattern Models

**ID**: `scanner-data-models-concurrency`

**Description**: 并发模式扫描器的数据模型

**Details**:

- `ConcurrencyUsage(BaseModel)`: 单个并发模式使用
- `ConcurrencyPatternSummary(ScannerSummary)`: 扩展 summary
  - 额外字段: `by_category: dict[str, int]`
- `ConcurrencyPatternOutput(ScannerOutput[dict[str, dict[str, list[ConcurrencyUsage]]]])`: 完整输出
  - 嵌套结构: category → pattern_type → usages
  - `results` 使用 `alias="concurrency_patterns"`
- 位置: `upcast/models/concurrency.py`

**Priority**: HIGH

---

#### R4: Complexity Analysis Models

**ID**: `scanner-data-models-complexity`

**Description**: 循环复杂度扫描器的数据模型

**Details**:

- `ComplexityResult(BaseModel)`: 单个函数的复杂度结果
  - 字段: name, line, end_line, complexity, severity, message
- `ComplexitySummary(ScannerSummary)`: 扩展 summary
  - 额外字段: `high_complexity_count: int`, `by_severity: dict[str, int]`
- `ComplexityOutput(ScannerOutput[dict[str, list[ComplexityResult]]])`: 完整输出
  - `results` 使用 `alias="modules"`
- 位置: `upcast/models/complexity.py`

**Priority**: HIGH

---

#### R5: Django Model Scanner Models

**ID**: `scanner-data-models-django-models`

**Description**: Django 模型扫描器的数据模型

**Details**:

- `DjangoField(BaseModel)`: 模型字段
- `DjangoRelationship(BaseModel)`: 关系字段
- `DjangoModel(BaseModel)`: 完整的模型定义
- `DjangoModelSummary(ScannerSummary)`: 扩展 summary
  - 额外字段: `total_models`, `total_fields`, `total_relationships`
- `DjangoModelOutput(ScannerOutput[dict[str, DjangoModel]])`: 完整输出
  - `results` 使用 `alias="models"`
- 位置: `upcast/models/django_models.py`

**Priority**: HIGH

---

#### R6: Django Settings Scanner Models

**ID**: `scanner-data-models-django-settings`

**Description**: Django 设置扫描器的数据模型

**Details**:

- `SettingsLocation(BaseModel)`: 设置使用位置
- `SettingsUsage(BaseModel)`: 设置使用信息
- `SettingDefinition(BaseModel)`: 设置定义
- `DynamicImport(BaseModel)`: 动态导入
- `SettingsModule(BaseModel)`: 设置模块
- `DjangoSettingsSummary(ScannerSummary)`: 扩展 summary
  - 额外字段: `total_settings`, `total_usages`
- 提供 3 种输出模型:
  - `DjangoSettingsUsageOutput`: 仅使用信息
  - `DjangoSettingsDefinitionOutput`: 仅定义信息
  - `DjangoSettingsCombinedOutput`: 组合输出
- 位置: `upcast/models/django_settings.py`

**Priority**: HIGH

**Notes**: 这是最复杂的模型,因为 scanner 支持 3 种不同的输出模式

---

#### R7: Django URL Scanner Models

**ID**: `scanner-data-models-django-urls`

**Description**: Django URL 模式扫描器的数据模型

**Details**:

- `UrlPattern(BaseModel)`: URL 模式
  - 支持多种类型: path, re_path, include, router_registration, dynamic
  - 字段: type, pattern, view_module, view_name, name, converters, etc.
- `UrlModule(BaseModel)`: URL 模块(包含 urlpatterns 列表)
- `DjangoUrlSummary(ScannerSummary)`: 扩展 summary
  - 额外字段: `total_modules`, `total_patterns`
- `DjangoUrlOutput(ScannerOutput[dict[str, UrlModule]])`: 完整输出
  - `results` 使用 `alias="url_modules"`
- 位置: `upcast/models/django_urls.py`

**Priority**: HIGH

---

#### R8: Environment Variable Scanner Models

**ID**: `scanner-data-models-env-vars`

**Description**: 环境变量扫描器的数据模型

**Details**:

- `EnvVarLocation(BaseModel)`: 环境变量访问位置
- `EnvVarInfo(BaseModel)`: 环境变量信息
  - 字段: name, required, default_value, locations
- `EnvVarSummary(ScannerSummary)`: 扩展 summary
  - 额外字段: `total_env_vars`, `required_count`, `optional_count`
- `EnvVarOutput(ScannerOutput[dict[str, EnvVarInfo]])`: 完整输出
  - `results` 使用 `alias="env_vars"`
- 位置: `upcast/models/env_vars.py`

**Priority**: HIGH

---

#### R9: Exception Handler Scanner Models

**ID**: `scanner-data-models-exceptions`

**Description**: 异常处理扫描器的数据模型

**Details**:

- `ExceptClause(BaseModel)`: except 子句
  - 包含大量统计字段(log counts, control flow counts)
- `ElseClause(BaseModel)`: else 子句
- `FinallyClause(BaseModel)`: finally 子句
- `ExceptionHandler(BaseModel)`: 完整的 try-except 块
- `ExceptionHandlerSummary(ScannerSummary)`: 扩展 summary
  - 额外字段: `total_handlers`, `total_except_clauses`
- `ExceptionHandlerOutput(ScannerOutput[list[ExceptionHandler]])`: 完整输出
  - `results` 使用 `alias="exception_handlers"`
- 位置: `upcast/models/exceptions.py`

**Priority**: HIGH

---

#### R10: HTTP Request Scanner Models

**ID**: `scanner-data-models-http-requests`

**Description**: HTTP 请求扫描器的数据模型

**Details**:

- `HttpRequestUsage(BaseModel)`: 单个 HTTP 请求使用
  - 字段: location, statement, method, params, headers, json_body, data, timeout, session_based, is_async
- `HttpRequestInfo(BaseModel)`: HTTP 请求信息
  - 字段: method, library, usages
- `HttpRequestSummary(ScannerSummary)`: 扩展 summary
  - 额外字段: `total_requests`, `unique_urls`, `by_library: dict[str, int]`
- `HttpRequestOutput(ScannerOutput[dict[str, HttpRequestInfo]])`: 完整输出
  - `results` 使用 `alias="requests"`
- 位置: `upcast/models/http_requests.py`

**Priority**: HIGH

---

#### R11: Prometheus Metrics Scanner Models

**ID**: `scanner-data-models-metrics`

**Description**: Prometheus 指标扫描器的数据模型

**Details**:

- `MetricUsage(BaseModel)`: 指标使用
- `MetricInfo(BaseModel)`: 指标信息
  - 字段: name, type, help, labels, namespace, subsystem, unit, custom_collector, buckets, usages
- `PrometheusMetricSummary(ScannerSummary)`: 扩展 summary
  - 额外字段: `total_metrics`, `by_type: dict[str, int]`
- `PrometheusMetricOutput(ScannerOutput[dict[str, MetricInfo]])`: 完整输出
  - `results` 使用 `alias="metrics"`
- 位置: `upcast/models/metrics.py`

**Priority**: HIGH

---

#### R12: Signal Scanner Models

**ID**: `scanner-data-models-signals`

**Description**: 信号扫描器的数据模型(从 scanners/signals.py 移动)

**Details**:

- `SignalUsage(BaseModel)`: 信号使用
- `SignalInfo(BaseModel)`: 信号信息
- `SignalSummary(ScannerSummary)`: 扩展 summary
  - 额外字段: django_receivers, django_senders, celery_receivers, celery_senders, custom_signals_defined, unused_custom_signals
- `SignalOutput(ScannerOutput[list[SignalInfo]])`: 完整输出
- 位置: `upcast/models/signals.py` (从 `upcast/scanners/signals.py` 提取)
- `upcast/scanners/signals.py` 修改为从新位置导入模型

**Priority**: CRITICAL (已有实现,需要移动)

---

#### R13: Unit Test Scanner Models

**ID**: `scanner-data-models-unit-tests`

**Description**: 单元测试扫描器的数据模型

**Details**:

- `TargetModule(BaseModel)`: 测试目标模块
- `UnitTestInfo(BaseModel)`: 单元测试信息
  - 字段: name, file, line_range, body_md5, assert_count, targets
- `UnitTestSummary(ScannerSummary)`: 扩展 summary
  - 额外字段: `total_tests`, `total_files`, `total_assertions`
- `UnitTestOutput(ScannerOutput[dict[str, list[UnitTestInfo]]])`: 完整输出
  - `results` 使用 `alias="tests"`
- 位置: `upcast/models/unit_tests.py`

**Priority**: HIGH

---

#### R14: Model Module Organization

**ID**: `scanner-data-models-module-structure`

**Description**: 模型模块的组织和导出

**Details**:

- `upcast/models/__init__.py` 必须:
  - 从所有子模块导入所有公共类
  - 定义完整的 `__all__` 列表
  - 包含模块级文档字符串,说明用途和使用方式
  - 提供简单的使用示例
- 支持: `from upcast.models import BlockingOperationsOutput, DjangoModelOutput, ...`

**Priority**: CRITICAL

**Validation**:

```python
# All imports work
from upcast.models import (
    ScannerSummary,
    ScannerOutput,
    BlockingOperationsOutput,
    DjangoModelOutput,
    # ... all 12 scanner outputs
)

# Wildcard import works
from upcast.models import *
```

---

#### R15: Backward Compatibility

**ID**: `scanner-data-models-backward-compat`

**Description**: 保持与现有代码的向后兼容性

**Details**:

- `upcast/common/models.py` 保留,但从 `upcast/models/base` re-export:

  ```python
  # upcast/common/models.py
  """Backward compatibility shim for scanner models.

  New code should import from upcast.models instead.
  """
  from upcast.models.base import ScannerSummary, ScannerOutput

  __all__ = ["ScannerSummary", "ScannerOutput"]
  ```

- `upcast/common/export.py` 修改导入路径:
  ```python
  from upcast.models.base import ScannerOutput  # 改为从新位置导入
  ```
- `upcast/common/scanner_base.py` 修改导入路径:
  ```python
  from upcast.models.base import ScannerOutput  # 改为从新位置导入
  ```

**Priority**: CRITICAL

**Validation**:

```python
# Old imports still work
from upcast.common.models import ScannerSummary, ScannerOutput

# New imports work
from upcast.models import ScannerSummary, ScannerOutput
from upcast.models.base import ScannerSummary, ScannerOutput
```

---

#### R16: Type Annotations and Documentation

**ID**: `scanner-data-models-docs`

**Description**: 所有模型必须有完整的类型注解和文档

**Details**:

- 每个类必须有 docstring 说明其用途
- 每个字段必须有类型注解
- 复杂字段必须使用 `Field(description=...)` 提供文档
- 数值字段必须使用适当的约束(如 `ge=0` for counts, `ge=1` for line numbers)
- 可选字段使用 `| None` 和 `default=None`

**Priority**: CRITICAL

**Validation**:

- `mypy upcast/models/` 无错误
- `ruff check upcast/models/` 无错误
- 所有公共 API 都有文档字符串

---

## Design Decisions

### D1: 为什么创建新的 `upcast/models/` 目录?

**Decision**: 创建独立的 `upcast/models/` 目录,而不是分散在各个 scanner 中

**Rationale**:

- 未来的 Analyzer 模块需要导入这些模型
- 集中管理便于维护和演进
- 清晰的模块边界,符合关注点分离原则

**Alternatives considered**:

- 模型分散在 scanner 目录: 增加 analyzer 的依赖复杂度
- 模型放在 common/: common 已经有很多工具类,职责不清晰

### D2: 为什么使用 Field alias?

**Decision**: 使用 `Field(alias="operations")` 来匹配现有的输出字段名

**Rationale**:

- Pydantic 推荐使用 `results` 作为泛型字段名
- 现有输出使用 scanner 特定的名称(如 "operations", "models")
- Alias 允许内部使用标准名称,输出时使用兼容名称

**Example**:

```python
class BlockingOperationsOutput(ScannerOutput[dict[str, list[BlockingOperation]]]):
    results: dict[str, list[BlockingOperation]] = Field(..., alias="operations")

output = BlockingOperationsOutput(...)
output.results  # 内部访问
output.to_dict()  # {"operations": [...]}  # 输出使用 alias
```

### D3: 为什么 Django Settings 需要 3 个 Output 模型?

**Decision**: 提供 `DjangoSettingsUsageOutput`, `DjangoSettingsDefinitionOutput`, `DjangoSettingsCombinedOutput`

**Rationale**:

- Django settings scanner 支持 3 种扫描模式:
  1. 仅扫描使用(usages only)
  2. 仅扫描定义(definitions only)
  3. 同时扫描(combined)
- 每种模式的输出结构不同,需要不同的模型
- 使用 Union 或 Optional 会导致类型不明确

### D4: 为什么不立即迁移 scanner 实现?

**Decision**: 本 change 只定义模型,不修改 scanner 实现

**Rationale**:

- 降低 change 的复杂度和风险
- 允许分阶段验证(模型定义 → 单个 scanner 迁移 → 所有 scanner 迁移)
- 模型定义完成后,可以并行进行多个 scanner 的迁移工作
- 便于 code review 和验证

## Dependencies

### Inbound

- `common-utilities`: 使用 `export_scanner_output()` 函数
- Pydantic v2: 所有模型基于 Pydantic BaseModel

### Outbound

本 capability 不依赖其他 capability,它是基础设施

### Future

- `analyzer-framework` (未来): 将使用这些模型作为输入
- `scanner-implementation` (后续 change): 各个 scanner 迁移到使用这些模型

## Implementation Notes

### File Organization

```
upcast/models/
├── __init__.py                # 导出所有模型,150+ lines
├── base.py                    # 基础类,80 lines
├── blocking_operations.py     # 50 lines
├── concurrency.py             # 50 lines
├── complexity.py         # 45 lines
├── django_models.py      # 90 lines
├── django_settings.py    # 150 lines (最复杂)
├── django_urls.py        # 80 lines
├── env_vars.py           # 60 lines
├── exceptions.py         # 100 lines
├── http_requests.py      # 70 lines
├── metrics.py            # 80 lines
├── signals.py            # 120 lines
└── unit_tests.py         # 60 lines

Total: ~1185 lines
```

### Code Quality Requirements

- 所有文件必须通过 `ruff check --fix`
- 所有文件必须通过 `mypy --strict`
- 所有模型必须有 docstring
- 所有字段必须有类型注解
- 使用 `Field(description=...)` 为复杂字段提供文档

## Testing Strategy

### Unit Tests (后续添加)

在 scanner 迁移时为每个模型添加单元测试:

```python
# tests/test_models/test_blocking_operations.py
def test_blocking_operations_output_creation():
    """Test creating BlockingOperationsOutput."""
    output = BlockingOperationsOutput(
        summary=BlockingOperationsSummary(
            total_count=1,
            files_scanned=1,
            by_category={"time_based": 1}
        ),
        results={"time_based": [BlockingOperation(...)]}
    )
    assert output.summary.total_count == 1

def test_blocking_operations_output_to_dict():
    """Test to_dict() uses alias."""
    output = BlockingOperationsOutput(...)
    data = output.to_dict()
    assert "operations" in data  # alias works
    assert "results" not in data
```

### Integration Tests (后续添加)

验证模型与实际 scanner 输出匹配:

```python
def test_blocking_operations_model_matches_scanner_output():
    """Verify model structure matches scanner output."""
    # Run scanner
    from upcast.blocking_operation_scanner.export import format_operations_output
    legacy_output = format_operations_output(...)

    # Create model
    model = BlockingOperationsOutput(...)
    model_output = model.to_dict()

    # Compare structures
    assert set(legacy_output.keys()) == set(model_output.keys())
```

## Validation Criteria

- [ ] All 13 files created in `upcast/models/`
- [ ] All models inherit from `ScannerSummary` or `ScannerOutput`
- [ ] All fields have type annotations and descriptions
- [ ] `from upcast.models import *` succeeds
- [ ] `upcast/common/models.py` deleted and imports updated
- [ ] `ruff check upcast/models/` passes
- [ ] `mypy upcast/models/` passes
- [ ] All existing tests pass (701/701)
- [ ] Signals scanner still works after model extraction

## Migration Path

### Phase 1: Define Models (This Spec)

1. Create `upcast/models/` directory
2. Define all 12 scanner models
3. Move base models from `common/models.py`
4. Update imports in `common/` modules

### Phase 2: Update Signal Scanner (Next Change)

1. Update `scanners/signals.py` to import from `models/signals.py`
2. Remove model definitions from `scanners/signals.py`
3. Verify tests pass

### Phase 3: Migrate Other Scanners (Future Changes)

1. One scanner at a time
2. Update export functions to use Pydantic models
3. Add model-specific tests
4. Verify backward compatibility

## Open Questions

- ~~Should we add validation tests now or later?~~ → Later, during scanner migration
- ~~How to handle scanner-specific metadata?~~ → Use `extra="allow"` in ScannerOutput
- ~~Should models be frozen?~~ → Summary frozen, Output not frozen (allows metadata updates)

## References

- Pydantic documentation: https://docs.pydantic.dev/
- Existing implementation: `upcast/scanners/signals.py`
- Scanner exports: `upcast/*_scanner/export.py`
