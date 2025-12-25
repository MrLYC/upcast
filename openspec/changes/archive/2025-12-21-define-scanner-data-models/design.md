# Design: Define Scanner Data Models

## Overview

本设计文档详细说明如何为所有 12 个 scanner 定义标准化的 Pydantic 数据模型。设计基于现有 scanner 的输出结构,参考 `upcast/scanners/signals.py` 的成功实践,为未来的 Analyzer 模块奠定基础。

## Architecture

### Directory Structure

```
upcast/
├── models/                          # 新建:集中的数据模型目录
│   ├── __init__.py                 # 导出所有模型
│   ├── base.py                     # 基础模型(从 common/models.py 移动)
│   ├── blocking_operations.py      # 阻塞操作模型
│   ├── concurrency.py              # 并发模式模型
│   ├── complexity.py               # 复杂度模型
│   ├── django_models.py            # Django 模型扫描模型
│   ├── django_settings.py          # Django 设置模型
│   ├── django_urls.py              # Django URL 模型
│   ├── env_vars.py                 # 环境变量模型
│   ├── exceptions.py               # 异常处理模型
│   ├── http_requests.py            # HTTP 请求模型
│   ├── metrics.py                  # Prometheus 指标模型
│   ├── signals.py                  # 信号模型(从 scanners/signals.py 提取)
│   └── unit_tests.py               # 单元测试模型
├── common/
│   ├── export.py                   # 更新导入路径
│   └── scanner_base.py             # 更新导入路径
└── scanners/
    └── signals.py                  # 保留,但从 models/signals.py 导入模型
```

### Base Model Hierarchy

```
BaseModel (Pydantic)
├── ScannerSummary                   # 所有 summary 的基类
│   ├── BlockingOperationsSummary
│   ├── ConcurrencyPatternSummary
│   ├── ComplexitySummary
│   ├── DjangoModelSummary
│   ├── DjangoSettingsSummary
│   ├── DjangoUrlSummary
│   ├── EnvVarSummary
│   ├── ExceptionHandlerSummary
│   ├── HttpRequestSummary
│   ├── PrometheusMetricSummary
│   ├── SignalSummary
│   └── UnitTestSummary
└── ScannerOutput[T]                 # 所有输出的泛型基类
    ├── BlockingOperationsOutput
    ├── ConcurrencyPatternOutput
    ├── ComplexityOutput
    ├── DjangoModelOutput
    ├── DjangoSettingsOutput
    ├── DjangoUrlOutput
    ├── EnvVarOutput
    ├── ExceptionHandlerOutput
    ├── HttpRequestOutput
    ├── PrometheusMetricOutput
    ├── SignalOutput
    └── UnitTestOutput
```

## Detailed Design

### 1. Base Models (`upcast/models/base.py`)

从 `upcast/common/models.py` 移动,保持不变:

```python
"""Base Pydantic models for scanner outputs."""

from typing import Any, Generic, TypeVar
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")

class ScannerSummary(BaseModel):
    """Base summary model for all scanners."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    total_count: int = Field(ge=0, description="Total items found")
    files_scanned: int = Field(ge=0, description="Number of files scanned")
    scan_duration_ms: int | None = Field(None, ge=0, description="Scan duration in milliseconds")

class ScannerOutput(BaseModel, Generic[T]):
    """Base output model for all scanners."""
    model_config = ConfigDict(extra="allow")

    summary: ScannerSummary
    results: T
    metadata: dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for export."""
        return self.model_dump(mode="python", exclude_none=True)
```

### 2. Scanner-Specific Models

#### 2.1 Blocking Operations (`upcast/models/blocking_operations.py`)

基于 `upcast/blocking_operation_scanner/export.py` 的输出结构:

```python
"""Data models for blocking operations scanner."""

from pydantic import BaseModel, Field
from upcast.models.base import ScannerSummary, ScannerOutput

class BlockingOperation(BaseModel):
    """A single blocking operation detected."""
    file: str = Field(..., description="File path")
    line: int = Field(..., ge=1, description="Line number")
    column: int = Field(default=0, ge=0, description="Column number")
    category: str = Field(..., description="Operation category")
    operation: str = Field(..., description="Operation name")
    statement: str | None = Field(None, description="Code statement")
    function: str | None = Field(None, description="Containing function")
    class_name: str | None = Field(None, description="Containing class")

class BlockingOperationsSummary(ScannerSummary):
    """Summary statistics for blocking operations."""
    by_category: dict[str, int] = Field(
        default_factory=dict,
        description="Count by category (time_based, database, synchronization, subprocess)"
    )

class BlockingOperationsOutput(ScannerOutput[dict[str, list[BlockingOperation]]]):
    """Complete output from blocking operations scanner."""
    summary: BlockingOperationsSummary
    results: dict[str, list[BlockingOperation]] = Field(
        ...,
        alias="operations",
        description="Operations grouped by category"
    )
```

**设计说明**:

- `results` 字段使用 `dict[str, list[BlockingOperation]]` 匹配现有的分类结构
- 使用 `alias="operations"` 保持与现有输出字段名的一致性
- `total_count` 在 summary 中计算所有操作总数

#### 2.2 Concurrency Patterns (`upcast/models/concurrency.py`)

基于 `upcast/concurrency_pattern_scanner/export.py`:

```python
"""Data models for concurrency pattern scanner."""

from pydantic import BaseModel, Field
from upcast.models.base import ScannerSummary, ScannerOutput

class ConcurrencyUsage(BaseModel):
    """A single usage of a concurrency pattern."""
    file: str
    line: int = Field(ge=1)
    column: int = Field(default=0, ge=0)
    pattern: str = Field(..., description="Pattern type")
    statement: str | None = None
    context: dict | None = None

class ConcurrencyPatternSummary(ScannerSummary):
    """Summary statistics for concurrency patterns."""
    by_category: dict[str, int] = Field(
        default_factory=dict,
        description="Count by category (threading, multiprocessing, asyncio, celery)"
    )

class ConcurrencyPatternOutput(ScannerOutput[dict[str, dict[str, list[ConcurrencyUsage]]]]):
    """Complete output from concurrency pattern scanner."""
    summary: ConcurrencyPatternSummary
    results: dict[str, dict[str, list[ConcurrencyUsage]]] = Field(
        ...,
        alias="concurrency_patterns",
        description="Patterns grouped by category and type"
    )
```

#### 2.3 Complexity (`upcast/models/complexity.py`)

基于 `upcast/cyclomatic_complexity_scanner/export.py`:

```python
"""Data models for cyclomatic complexity scanner."""

from pydantic import BaseModel, Field
from upcast.models.base import ScannerSummary, ScannerOutput

class ComplexityResult(BaseModel):
    """Complexity result for a single function."""
    name: str = Field(..., description="Function name")
    line: int = Field(ge=1)
    end_line: int = Field(ge=1)
    complexity: int = Field(ge=0, description="Cyclomatic complexity score")
    severity: str = Field(..., description="Severity level (warning, high_risk, critical)")
    message: str | None = None

class ComplexitySummary(ScannerSummary):
    """Summary statistics for complexity analysis."""
    high_complexity_count: int = Field(ge=0, description="Functions above threshold")
    by_severity: dict[str, int] = Field(
        default_factory=dict,
        description="Count by severity level"
    )

class ComplexityOutput(ScannerOutput[dict[str, list[ComplexityResult]]]):
    """Complete output from complexity scanner."""
    summary: ComplexitySummary
    results: dict[str, list[ComplexityResult]] = Field(
        ...,
        alias="modules",
        description="Results grouped by module path"
    )
```

#### 2.4 Django Models (`upcast/models/django_models.py`)

基于 `upcast/django_model_scanner/export.py`:

```python
"""Data models for Django model scanner."""

from pydantic import BaseModel, Field
from upcast.models.base import ScannerSummary, ScannerOutput

class DjangoField(BaseModel):
    """A field in a Django model."""
    name: str
    type: str = Field(..., description="Field type (e.g., CharField, ForeignKey)")
    parameters: dict = Field(default_factory=dict, description="Field parameters")
    line: int = Field(ge=1)

class DjangoRelationship(BaseModel):
    """A relationship field in a Django model."""
    type: str = Field(..., description="Relationship type (ForeignKey, ManyToMany, etc)")
    to: str = Field(..., description="Target model")
    field: str = Field(..., description="Field name")
    related_name: str | None = None
    on_delete: str | None = None

class DjangoModel(BaseModel):
    """A Django model definition."""
    name: str = Field(..., description="Model class name")
    module: str = Field(..., description="Module path")
    bases: list[str] = Field(default_factory=list, description="Base classes")
    fields: dict[str, DjangoField] = Field(default_factory=dict)
    relationships: list[DjangoRelationship] = Field(default_factory=list)
    meta: dict | None = Field(None, description="Meta class options")
    line: int = Field(ge=1)

class DjangoModelSummary(ScannerSummary):
    """Summary statistics for Django models."""
    total_models: int = Field(ge=0)
    total_fields: int = Field(ge=0)
    total_relationships: int = Field(ge=0)

class DjangoModelOutput(ScannerOutput[dict[str, DjangoModel]]):
    """Complete output from Django model scanner."""
    summary: DjangoModelSummary
    results: dict[str, DjangoModel] = Field(
        ...,
        alias="models",
        description="Models keyed by qualified name (app.models.ModelName)"
    )
```

#### 2.5 Django Settings (`upcast/models/django_settings.py`)

基于 `upcast/django_settings_scanner/export.py` (有多种输出格式):

```python
"""Data models for Django settings scanner."""

from pydantic import BaseModel, Field
from upcast.models.base import ScannerSummary, ScannerOutput

class SettingsLocation(BaseModel):
    """A location where a setting is used."""
    file: str
    line: int = Field(ge=1)
    column: int = Field(default=0, ge=0)
    pattern: str = Field(..., description="Usage pattern")
    code: str | None = None

class SettingsUsage(BaseModel):
    """Usage information for a setting variable."""
    count: int = Field(ge=0, description="Number of usages")
    locations: list[SettingsLocation] = Field(default_factory=list)

class SettingDefinition(BaseModel):
    """A setting definition in a settings module."""
    value: Any | None = Field(None, description="Static value")
    statement: str | None = Field(None, description="Dynamic assignment statement")
    lineno: int = Field(ge=1)
    overrides: str | None = Field(None, description="Module path this overrides")

class DynamicImport(BaseModel):
    """A dynamic import in settings module."""
    pattern: str
    base_module: str | None = None
    file: str
    line: int = Field(ge=1)

class SettingsModule(BaseModel):
    """A Django settings module."""
    definitions: dict[str, SettingDefinition] = Field(default_factory=dict)
    star_imports: list[str] = Field(default_factory=list, description="From X import * statements")
    dynamic_imports: list[DynamicImport] = Field(default_factory=list)

class DjangoSettingsSummary(ScannerSummary):
    """Summary statistics for Django settings."""
    total_settings: int = Field(ge=0, description="Number of unique settings")
    total_usages: int = Field(ge=0, description="Total usage count")

class DjangoSettingsUsageOutput(ScannerOutput[dict[str, SettingsUsage]]):
    """Output for settings usage scan."""
    summary: DjangoSettingsSummary
    results: dict[str, SettingsUsage] = Field(..., alias="settings")

class DjangoSettingsDefinitionOutput(ScannerOutput[dict[str, SettingsModule]]):
    """Output for settings definition scan."""
    summary: DjangoSettingsSummary
    results: dict[str, SettingsModule] = Field(..., alias="definitions")

class DjangoSettingsCombinedOutput(BaseModel):
    """Combined output for both definitions and usages."""
    definitions: dict[str, SettingsModule]
    usages: dict[str, SettingsUsage]
```

**设计说明**: Django settings scanner 有 3 种输出格式(usages only, definitions only, combined),因此提供 3 个不同的 Output 模型。

#### 2.6 Django URLs (`upcast/models/django_urls.py`)

基于 `upcast/django_url_scanner/export.py`:

```python
"""Data models for Django URL scanner."""

from pydantic import BaseModel, Field
from upcast.models.base import ScannerSummary, ScannerOutput

class UrlPattern(BaseModel):
    """A Django URL pattern."""
    type: str = Field(..., description="Pattern type (path, re_path, include, etc)")
    pattern: str | None = Field(None, description="URL pattern string")
    view_module: str | None = None
    view_name: str | None = None
    include_module: str | None = None
    namespace: str | None = None
    name: str | None = None
    converters: list[str] = Field(default_factory=list)
    named_groups: list[str] = Field(default_factory=list)
    viewset_module: str | None = None
    viewset_name: str | None = None
    basename: str | None = None
    router_type: str | None = None
    is_partial: bool = False
    is_conditional: bool = False
    description: str | None = None
    note: str | None = Field(None, description="For dynamic patterns")

class UrlModule(BaseModel):
    """URL patterns in a module."""
    urlpatterns: list[UrlPattern]

class DjangoUrlSummary(ScannerSummary):
    """Summary statistics for Django URLs."""
    total_modules: int = Field(ge=0)
    total_patterns: int = Field(ge=0)

class DjangoUrlOutput(ScannerOutput[dict[str, UrlModule]]):
    """Complete output from Django URL scanner."""
    summary: DjangoUrlSummary
    results: dict[str, UrlModule] = Field(..., alias="url_modules")
```

#### 2.7 Environment Variables (`upcast/models/env_vars.py`)

基于 `upcast/env_var_scanner/export.py`:

```python
"""Data models for environment variable scanner."""

from pydantic import BaseModel, Field
from upcast.models.base import ScannerSummary, ScannerOutput

class EnvVarLocation(BaseModel):
    """A location where an environment variable is accessed."""
    file: str
    line: int = Field(ge=1)
    column: int = Field(default=0, ge=0)
    pattern: str = Field(..., description="Access pattern")
    code: str | None = None

class EnvVarInfo(BaseModel):
    """Information about an environment variable."""
    name: str = Field(..., description="Environment variable name")
    required: bool = Field(..., description="Whether variable is required")
    default_value: str | None = Field(None, description="Default value if provided")
    locations: list[EnvVarLocation] = Field(default_factory=list)

class EnvVarSummary(ScannerSummary):
    """Summary statistics for environment variables."""
    total_env_vars: int = Field(ge=0)
    required_count: int = Field(ge=0)
    optional_count: int = Field(ge=0)

class EnvVarOutput(ScannerOutput[dict[str, EnvVarInfo]]):
    """Complete output from environment variable scanner."""
    summary: EnvVarSummary
    results: dict[str, EnvVarInfo] = Field(..., alias="env_vars")
```

#### 2.8 Exception Handlers (`upcast/models/exceptions.py`)

基于 `upcast/exception_handler_scanner/export.py`:

```python
"""Data models for exception handler scanner."""

from pydantic import BaseModel, Field
from upcast.models.base import ScannerSummary, ScannerOutput

class ExceptClause(BaseModel):
    """An except clause in a try-except block."""
    line: int = Field(ge=1)
    exception_types: list[str] = Field(default_factory=list)
    lines: int = Field(ge=0, description="Number of lines in clause")
    log_debug_count: int = Field(default=0, ge=0)
    log_info_count: int = Field(default=0, ge=0)
    log_warning_count: int = Field(default=0, ge=0)
    log_error_count: int = Field(default=0, ge=0)
    log_exception_count: int = Field(default=0, ge=0)
    log_critical_count: int = Field(default=0, ge=0)
    pass_count: int = Field(default=0, ge=0)
    return_count: int = Field(default=0, ge=0)
    break_count: int = Field(default=0, ge=0)
    continue_count: int = Field(default=0, ge=0)
    raise_count: int = Field(default=0, ge=0)

class ElseClause(BaseModel):
    """An else clause in a try-except block."""
    line: int = Field(ge=1)
    lines: int = Field(ge=0)

class FinallyClause(BaseModel):
    """A finally clause in a try-except block."""
    line: int = Field(ge=1)
    lines: int = Field(ge=0)

class ExceptionHandler(BaseModel):
    """A complete try-except block."""
    file: str
    lineno: int = Field(ge=1, description="Start line")
    end_lineno: int = Field(ge=1, description="End line")
    try_lines: int = Field(ge=0, description="Number of lines in try block")
    except_clauses: list[ExceptClause]
    else_clause: ElseClause | None = None
    finally_clause: FinallyClause | None = None

class ExceptionHandlerSummary(ScannerSummary):
    """Summary statistics for exception handlers."""
    total_handlers: int = Field(ge=0)
    total_except_clauses: int = Field(ge=0)

class ExceptionHandlerOutput(ScannerOutput[list[ExceptionHandler]]):
    """Complete output from exception handler scanner."""
    summary: ExceptionHandlerSummary
    results: list[ExceptionHandler] = Field(..., alias="exception_handlers")
```

#### 2.9 HTTP Requests (`upcast/models/http_requests.py`)

基于 `upcast/http_request_scanner/export.py`:

```python
"""Data models for HTTP request scanner."""

from pydantic import BaseModel, Field
from upcast.models.base import ScannerSummary, ScannerOutput

class HttpRequestUsage(BaseModel):
    """A single HTTP request usage."""
    location: str = Field(..., description="file:line format")
    statement: str = Field(..., description="Request statement")
    method: str = Field(..., description="HTTP method")
    params: dict | None = None
    headers: dict | None = None
    json_body: dict | None = None
    data: Any | None = None
    timeout: float | int | None = None
    session_based: bool = Field(default=False)
    is_async: bool = Field(default=False)

class HttpRequestInfo(BaseModel):
    """Information about HTTP requests to a URL."""
    method: str = Field(..., description="Primary HTTP method")
    library: str = Field(..., description="Primary library (requests, httpx, etc)")
    usages: list[HttpRequestUsage]

class HttpRequestSummary(ScannerSummary):
    """Summary statistics for HTTP requests."""
    total_requests: int = Field(ge=0, description="Total number of requests")
    unique_urls: int = Field(ge=0, description="Number of unique URLs")
    by_library: dict[str, int] = Field(default_factory=dict)

class HttpRequestOutput(ScannerOutput[dict[str, HttpRequestInfo]]):
    """Complete output from HTTP request scanner."""
    summary: HttpRequestSummary
    results: dict[str, HttpRequestInfo] = Field(..., alias="requests")
```

#### 2.10 Prometheus Metrics (`upcast/models/metrics.py`)

基于 `upcast/prometheus_metrics_scanner/export.py`:

```python
"""Data models for Prometheus metrics scanner."""

from pydantic import BaseModel, Field
from upcast.models.base import ScannerSummary, ScannerOutput

class MetricUsage(BaseModel):
    """A usage of a metric."""
    location: str = Field(..., description="file:line format")
    pattern: str = Field(..., description="Usage pattern")
    statement: str = Field(..., description="Code statement")

class MetricInfo(BaseModel):
    """Information about a Prometheus metric."""
    name: str = Field(..., description="Metric name")
    type: str = Field(..., description="Metric type (Counter, Gauge, Histogram, Summary)")
    help: str = Field(..., description="Metric help text")
    labels: list[str] = Field(default_factory=list)
    namespace: str | None = None
    subsystem: str | None = None
    unit: str | None = None
    custom_collector: bool = Field(default=False)
    buckets: list[float] | None = Field(None, description="For Histogram")
    usages: list[MetricUsage] = Field(default_factory=list)

class PrometheusMetricSummary(ScannerSummary):
    """Summary statistics for Prometheus metrics."""
    total_metrics: int = Field(ge=0)
    by_type: dict[str, int] = Field(default_factory=dict)

class PrometheusMetricOutput(ScannerOutput[dict[str, MetricInfo]]):
    """Complete output from Prometheus metrics scanner."""
    summary: PrometheusMetricSummary
    results: dict[str, MetricInfo] = Field(..., alias="metrics")
```

#### 2.11 Signals (`upcast/models/signals.py`)

从 `upcast/scanners/signals.py` 提取,保持不变:

```python
"""Data models for signal scanner."""
# 与现有 upcast/scanners/signals.py 中的模型定义相同
# SignalUsage, SignalInfo, SignalSummary, SignalOutput
```

#### 2.12 Unit Tests (`upcast/models/unit_tests.py`)

基于 `upcast/unit_test_scanner/export.py`:

```python
"""Data models for unit test scanner."""

from pydantic import BaseModel, Field
from upcast.models.base import ScannerSummary, ScannerOutput

class TargetModule(BaseModel):
    """A module targeted by test imports."""
    module: str = Field(..., description="Module path")
    symbols: list[str] = Field(default_factory=list, description="Imported symbols")

class UnitTestInfo(BaseModel):
    """Information about a unit test function."""
    name: str = Field(..., description="Test function name")
    file: str = Field(..., description="File path")
    line_range: tuple[int, int] = Field(..., description="(start_line, end_line)")
    body_md5: str = Field(..., description="MD5 hash of test body")
    assert_count: int = Field(ge=0, description="Number of assertions")
    targets: list[TargetModule] = Field(default_factory=list)

class UnitTestSummary(ScannerSummary):
    """Summary statistics for unit tests."""
    total_tests: int = Field(ge=0)
    total_files: int = Field(ge=0)
    total_assertions: int = Field(ge=0)

class UnitTestOutput(ScannerOutput[dict[str, list[UnitTestInfo]]]):
    """Complete output from unit test scanner."""
    summary: UnitTestSummary
    results: dict[str, list[UnitTestInfo]] = Field(
        ...,
        alias="tests",
        description="Tests grouped by file path"
    )
```

### 3. Module Initialization (`upcast/models/__init__.py`)

导出所有模型以便使用:

```python
"""Pydantic data models for all scanners.

This module provides standardized, type-safe data models for scanner outputs,
enabling both scanners and future analyzers to work with structured data.

Usage:
    from upcast.models import (
        BlockingOperationsOutput,
        DjangoModelOutput,
        EnvVarOutput,
        # ... other models
    )
"""

# Base models
from upcast.models.base import ScannerSummary, ScannerOutput

# Blocking operations
from upcast.models.blocking_operations import (
    BlockingOperation,
    BlockingOperationsSummary,
    BlockingOperationsOutput,
)

# Concurrency patterns
from upcast.models.concurrency import (
    ConcurrencyUsage,
    ConcurrencyPatternSummary,
    ConcurrencyPatternOutput,
)

# ... (export all other models)

__all__ = [
    # Base
    "ScannerSummary",
    "ScannerOutput",
    # Blocking operations
    "BlockingOperation",
    "BlockingOperationsSummary",
    "BlockingOperationsOutput",
    # ... (list all exports)
]
```

## Implementation Notes

### 1. 模型字段命名

- 使用 `snake_case` 命名字段(遵循 Python 约定)
- 当 scanner 输出使用不同的键名时,使用 `Field(alias=...)`
- 例如: `results: dict = Field(..., alias="operations")`

### 2. 类型约束

- 所有计数字段使用 `Field(ge=0)` 确保非负
- 所有行号使用 `Field(ge=1)` 确保有效
- 可选字段使用 `| None` 和 `default=None`

### 3. 文档字符串

- 每个类和字段都应有清晰的 `description`
- 对于复杂字段,在注释中说明数据结构

### 4. 数据转换

- 所有 Output 模型提供 `to_dict()` 方法
- 使用 `model_dump(mode="python", exclude_none=True)` 生成 dict
- `upcast/common/models.py` 将被删除,所有导入改为 `upcast.models.base`

### 5. 迁移路径

**Phase 1: 定义模型(本 change)**

- 创建所有模型定义
- 不修改 scanner 实现

**Phase 2: 更新 signals scanner(后续 change)**

- `upcast/scanners/signals.py` 从 `upcast/models.signals` 导入模型
- 验证现有测试仍然通过

**Phase 3: 逐步迁移其他 scanner(后续 changes)**

- 一次迁移一个 scanner
- 为每个 scanner 添加测试
- 更新 export 函数使用 Pydantic 模型

## Testing Strategy

### 模型验证测试(后续添加)

```python
def test_blocking_operations_output_validation():
    """Test that BlockingOperationsOutput validates correctly."""
    output = BlockingOperationsOutput(
        summary=BlockingOperationsSummary(
            total_count=1,
            files_scanned=1,
            by_category={"time_based": 1}
        ),
        results={
            "time_based": [
                BlockingOperation(
                    file="test.py",
                    line=10,
                    category="time_based",
                    operation="sleep"
                )
            ]
        }
    )

    # Test to_dict conversion
    data = output.to_dict()
    assert "summary" in data
    assert "operations" in data  # uses alias
```

### 与现有 export 输出对比测试(后续添加)

```python
def test_model_matches_legacy_output():
    """Test that Pydantic model output matches legacy dict output."""
    # Run legacy export
    legacy_data = format_operations_output(...)

    # Create Pydantic model
    model_output = BlockingOperationsOutput(...)
    model_data = model_output.to_dict()

    # Compare structures (keys, types, values)
    assert model_data.keys() == legacy_data.keys()
```

## Open Issues

1. **Django Settings 的多种输出格式**: 已决定使用 3 个不同的 Output 模型
2. **Signal Scanner 模型重复**: 已决定移动到 `upcast/models/signals.py`,scanners/signals.py 导入
3. **测试策略**: 先定义模型,测试在 scanner 迁移时添加

## References

- Existing implementation: `upcast/scanners/signals.py`
- Scanner export implementations: `upcast/*_scanner/export.py`
- Base models: `upcast/common/models.py`
- Pydantic docs: https://docs.pydantic.dev/
