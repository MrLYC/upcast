# Proposal: Refactor Scanners to Use Pydantic Models

## Metadata

- **Change ID**: `refactor-scanners-to-use-models`
- **Status**: PROPOSED
- **Created**: 2025-12-21
- **Author**: Assistant
- **Related Issues**: N/A
- **Depends On**: `define-scanner-data-models` (completed)

## Problem Statement

在完成了数据模型定义后（`define-scanner-data-models`），现在有以下问题：

1. **目录结构混乱**: 目前有 11 个 scanner 散落在根目录下（如 `blocking_operation_scanner/`, `django_model_scanner/` 等），只有 1 个新的 `scanners/signals.py` 在统一目录中
2. **未使用新模型**: 除了 signals scanner，其他 11 个 scanner 仍然使用 dict 输出，未利用已定义的 Pydantic 模型
3. **命名不一致**: scanner 目录名使用下划线（如 `blocking_operation_scanner`），而模型文件使用简洁命名（如 `blocking_operations.py`）
4. **代码重复严重**: 每个 scanner 都有自己的实现，存在大量重复逻辑：
   - 文件搜索和过滤逻辑（pattern matching）
   - AST 解析和推断逻辑（astroid usage）
   - 导出逻辑（YAML/JSON output）
   - CLI 参数处理
   - 错误处理和日志记录

这种结构不利于：

- 代码维护和查找
- 未来添加新 scanner
- 与 Analyzer 模块集成
- 统一的 CLI 和导出行为
- 代码质量的提升（重复代码难以统一优化）

## Proposed Solution

### 核心方案

**重构所有 scanner 到统一的 `upcast/scanners/` 目录，并使用已定义的 Pydantic 模型，同时提取通用逻辑到 common 模块**

1. **目录结构重组**:

   ```
   upcast/scanners/
   ├── __init__.py                    # 导出所有 scanner 类
   ├── signals.py                     # 已有（作为参考模板）
   ├── blocking_operations.py         # 从 blocking_operation_scanner/ 重构
   ├── concurrency.py                 # 从 concurrency_pattern_scanner/ 重构
   ├── complexity.py                  # 从 cyclomatic_complexity_scanner/ 重构
   ├── django_models.py               # 从 django_model_scanner/ 重构
   ├── django_settings.py             # 从 django_settings_scanner/ 重构
   ├── django_urls.py                 # 从 django_url_scanner/ 重构
   ├── env_vars.py                    # 从 env_var_scanner/ 重构
   ├── exceptions.py                  # 从 exception_handler_scanner/ 重构
   ├── http_requests.py               # 从 http_request_scanner/ 重构
   ├── metrics.py                     # 从 prometheus_metrics_scanner/ 重构
   └── unit_tests.py                  # 从 unit_test_scanner/ 重构
   ```

2. **增强 common 模块**:

   在迁移过程中识别并提取可复用逻辑到 `upcast/common/`：

   - **ast_utils.py** (已有，需增强):

     ```python
     # 添加常用的 AST 模式匹配辅助函数
     def find_function_calls(module, function_names: set) -> list
     def extract_decorator_info(node) -> dict
     def get_import_info(module) -> dict
     ```

   - **file_utils.py** (已有，需增强):

     ```python
     # 添加更多文件搜索辅助
     def find_python_files(path, include, exclude) -> list[Path]
     def get_relative_path(file_path, root_path) -> str
     def is_test_file(file_path) -> bool
     ```

   - **export.py** (已有，需优化):

     ```python
     # 统一 Pydantic 模型导出
     def export_scanner_output(output: ScannerOutput, ...)
     # 已有，确保支持所有模型类型
     ```

   - **scanner_base.py** (已有，需完善):

     ```python
     # 提供更多基础功能
     class BaseScanner(ABC, Generic[T]):
         def get_files_to_scan(self, path: Path) -> list[Path]  # 已有
         def should_scan_file(self, file_path: Path) -> bool    # 已有
         # 新增通用辅助方法
         def parse_file(self, file_path: Path) -> astroid.Module
         def track_scan_progress(self, current: int, total: int)
     ```

   - **patterns.py** (已有):
     ```python
     # 文件模式匹配（已有，无需修改）
     def match_patterns(path, patterns) -> bool
     ```

3. **Scanner 实现标准化**:

   每个 scanner 文件遵循统一模式，保持逻辑单一简洁：

   ```python
   """Scanner implementation with Pydantic models."""

   from pathlib import Path
   from upcast.common.scanner_base import BaseScanner
   from upcast.common import ast_utils, file_utils  # 使用 common 工具
   from upcast.models.xxx import XxxOutput, XxxSummary, XxxResult

   class XxxScanner(BaseScanner[XxxOutput]):
       """Scanner for XXX patterns.

       核心职责：
       1. 定义扫描逻辑（what to scan）
       2. 解析特定模式（how to parse）
       3. 构建结果模型（how to structure）

       复用 common 模块：
       - 文件搜索：BaseScanner.get_files_to_scan()
       - AST 解析：common.ast_utils
       - 数据导出：通过返回 Pydantic 模型，由 common.export 处理
       """

       def scan(self, path: Path) -> XxxOutput:
           """Scan and return typed output."""
           # 使用基类的文件搜索
           files = self.get_files_to_scan(path)

           # 专注于扫描逻辑
           results = []
           for file in files:
               module = self.parse_file(file)  # 使用基类方法
               results.extend(self._scan_module(module))

           # 构建 Pydantic 输出
           return XxxOutput(summary=..., results=...)

       def _scan_module(self, module) -> list[XxxResult]:
           """核心扫描逻辑 - scanner 特定的实现."""
           # 使用 common.ast_utils 辅助函数
           # 保持此方法简洁，专注业务逻辑
   ```

4. **迁移策略**:

   - **识别可复用代码**: 在迁移每个 scanner 时，识别可以提取到 common 的逻辑
   - **逐步提取**: 每迁移 2-3 个 scanner，就回顾并提取共同模式
   - **保持简洁**: scanner 代码应该专注于"扫描什么"和"如何识别"，而非"如何搜索"和"如何导出"
   - **测试驱动**: 确保提取到 common 的逻辑有测试覆盖

5. **CLI 命令保持不变**:
   - 所有 `upcast scan-xxx` 命令保持原样
   - 在 `pyproject.toml` 中更新 entry points 指向新路径

### 设计原则

1. **统一架构**: 所有 scanner 遵循相同的代码结构和模式
2. **类型安全**: 使用 Pydantic 模型提供强类型输出
3. **单一职责**: Scanner 专注于"识别什么"，而非"如何搜索"或"如何导出"
4. **复用优先**: 提取通用逻辑到 common 模块，避免代码重复
5. **向后兼容**: 保持 CLI 接口和输出格式不变
6. **最小改动**: 保留核心扫描逻辑，重构数据流和组织结构
7. **可测试**: 保持现有测试套件通过，common 模块新增逻辑需要测试

## Benefits

1. **统一的代码组织**: 所有 scanner 在一个目录，易于浏览和维护
2. **类型安全输出**: 利用已定义的 Pydantic 模型，减少错误
3. **更好的可维护性**: 统一的代码结构，降低维护成本
4. **消除重复代码**: 通用逻辑集中在 common 模块，易于优化和测试
5. **更简洁的 Scanner**: 每个 scanner 专注于业务逻辑，代码更清晰
6. **简化导入**: `from upcast.scanners import XxxScanner`
7. **为 Analyzer 做准备**: 统一的输出模型便于分析器集成
8. **便于扩展**: 添加新 scanner 只需实现核心逻辑，复用所有基础设施
9. **质量提升**: common 模块的集中优化惠及所有 scanner

## Risks and Mitigations

### Risk 1: 大规模重构可能引入 bug

**Mitigation**:

- 逐个 scanner 迁移，每次确保测试通过
- 保留核心扫描逻辑不变，只改变输出层
- 现有 640 个测试作为回归测试保障

### Risk 2: 导入路径变更可能影响用户代码

**Mitigation**:

- 主要影响内部代码，外部用户使用 CLI 不受影响
- 在 `upcast/__init__.py` 中添加兼容性导入（如果需要）
- 在 CHANGELOG 中明确说明变更

### Risk 3: 迁移工作量大

**Mitigation**:

- signals.py 已经是成功模板，其他 scanner 可以参考
- 核心扫描逻辑不变，主要是移动代码和调整输出
- 可以分阶段完成，不必一次性完成所有

## Alternatives Considered

### Alternative 1: 保持现有目录结构，只使用模型

**Rejected because**:

- 目录结构仍然混乱
- 不利于未来维护
- 与新的 signals.py 结构不一致

### Alternative 2: 创建新的 v2 版本，保留旧版本

**Rejected because**:

- 增加维护负担
- 用户困惑（两套 API）
- 不必要的复杂性

### Alternative 3: 只移动文件，不改变实现

**Rejected because**:

- 错失利用 Pydantic 模型的机会
- 仍需后续再次重构
- 无法充分发挥数据模型的优势

## Implementation Scope

### In Scope

- 重构所有 11 个旧 scanner 到 `upcast/scanners/` 目录
- 更新所有 scanner 使用对应的 Pydantic 模型输出
- **识别并提取可复用逻辑到 common 模块**:
  - AST 解析和推断的通用辅助函数
  - 文件搜索和过滤的增强功能
  - Scanner 基类的完善（如 parse_file 等）
  - 确保 export.py 支持所有 Pydantic 模型
- 为新增的 common 功能编写单元测试
- 更新 `pyproject.toml` 中的 CLI entry points
- 更新所有内部导入路径
- 删除旧的 `xxx_scanner/` 目录
- 更新测试以使用新的导入路径
- 确保所有 640 个测试继续通过

### Out of Scope

- 改变扫描算法或核心逻辑（除非是为了使用 common 工具简化）
- 改变 CLI 命令名称或参数
- 改变输出格式（YAML/JSON 结构保持不变）
- 添加新功能或新 scanner
- 实现 Analyzer 模块

## Success Criteria

1. ✅ 所有 scanner 位于 `upcast/scanners/` 目录
2. ✅ 所有 scanner 使用对应的 Pydantic 模型输出
3. ✅ 所有旧的 `xxx_scanner/` 目录已删除
4. ✅ **通用逻辑已提取到 common 模块**:
   - AST 辅助函数在 common/ast_utils.py
   - 文件处理辅助在 common/file_utils.py
   - Scanner 基类功能完善
   - 新增功能有测试覆盖
5. ✅ **Scanner 代码简洁清晰**:
   - 平均每个 scanner < 200 行代码
   - 专注于业务逻辑，复用 common 工具
   - 代码重复率显著降低
6. ✅ CLI 命令仍然正常工作（`upcast scan-xxx`）
7. ✅ 所有测试通过（包括现有的 640 个测试 + 新增的 common 模块测试）
8. ✅ ruff 和 mypy 检查通过
9. ✅ 可以成功导入: `from upcast.scanners import XxxScanner`
10. ✅ 输出格式与之前保持一致（向后兼容）

## Migration Order

建议的迁移顺序（从简单到复杂）：

1. **env_vars** - 结构简单，适合作为第一个
2. **complexity** - 结构简单
3. **blocking_operations** - 中等复杂度
4. **http_requests** - 中等复杂度
5. **metrics** - 中等复杂度
6. **concurrency** - 中等复杂度
7. **exceptions** - 稍复杂
8. **unit_tests** - 稍复杂
9. **django_urls** - 稍复杂
10. **django_models** - 较复杂
11. **django_settings** - 最复杂（3 种输出格式）

每个 scanner 迁移后立即运行测试验证。

## Open Questions

1. ~~是否需要在 `upcast/__init__.py` 中提供兼容性导入?~~ → 如果测试需要，可以添加
2. ~~是否需要更新 README 中的使用示例?~~ → 是的，需要更新导入示例
3. ~~如何处理 scanner 特定的工具模块（如 checker.py）?~~ → 迁移到对应的 scanner 文件中或作为私有模块
