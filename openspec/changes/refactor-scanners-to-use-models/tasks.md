# Tasks for: Refactor Scanners to Use Pydantic Models

## Phase 1: Preparation and Common Module Enhancement (1.5 hours)

### Task 1.1: Create scanner template (15 min)

- [ ] 创建 `docs/scanner_template.py` 作为标准模板
- [ ] 基于 `scanners/signals.py` 编写通用模式
- [ ] 包含注释说明各部分的作用和如何使用 common 工具

### Task 1.2: Audit existing scanners for common patterns (30 min)

- [ ] 检查所有 11 个旧 scanner 的实现
- [ ] 识别重复的代码模式：
  - AST 节点遍历和模式匹配
  - 值推断和类型提取
  - 文件路径处理
  - 错误处理模式
- [ ] 列出需要提取到 common 的候选函数

### Task 1.3: Enhance common/ast_utils.py (30 min)

- [ ] 添加 `find_function_calls()` - 查找特定函数调用
- [ ] 添加 `extract_decorator_info()` - 提取装饰器信息
- [ ] 添加 `get_import_info()` - 获取导入信息
- [ ] 添加 `safe_infer_value()` - 安全推断节点值
- [ ] 为新增函数编写单元测试

### Task 1.4: Enhance common/file_utils.py (15 min)

- [ ] 添加 `is_test_file()` - 判断是否为测试文件
- [ ] 添加 `get_relative_path_str()` - 获取相对路径字符串
- [ ] 确保与现有功能兼容
- [ ] 为新增函数编写单元测试

### Task 1.5: Enhance common/scanner_base.py (15 min)

- [ ] 添加 `parse_file()` - 统一的文件解析方法
- [ ] 添加 `track_progress()` - 进度跟踪（如果需要）
- [ ] 确保所有 scanner 都能复用
- [ ] 更新 BaseScanner 文档字符串

### Task 1.6: Verify common/export.py (15 min)

- [ ] 确认 `export_scanner_output()` 支持所有 Pydantic 模型
- [ ] 测试各种模型类型的导出
- [ ] 如需修改，确保向后兼容

## Phase 2: Migrate Simple Scanners (4.5 hours)

### Task 2.1: Migrate env_vars scanner (40 min)

- [ ] 创建 `upcast/scanners/env_vars.py`
- [ ] 从 `env_var_scanner/` 迁移代码
- [ ] **使用 common 工具简化代码**:
  - 使用 `BaseScanner.parse_file()` 解析
  - 使用 `ast_utils` 的辅助函数
  - 识别可提取的模式
- [ ] 使用 `models.env_vars` 中的模型
- [ ] 更新测试导入路径
- [ ] 运行测试验证
- [ ] **代码审查**: 确保代码简洁（< 200 行）
- [ ] 删除 `env_var_scanner/` 目录

### Task 2.2: Migrate complexity scanner (40 min)

- [ ] 创建 `upcast/scanners/complexity.py`
- [ ] 从 `cyclomatic_complexity_scanner/` 迁移代码
- [ ] **复用已提取的 common 函数**
- [ ] 使用 `models.complexity` 中的模型
- [ ] 更新测试导入路径
- [ ] 运行测试验证
- [ ] 删除 `cyclomatic_complexity_scanner/` 目录

### Task 2.3: Review and extract common patterns (20 min)

- [ ] 审查前两个 scanner 的实现
- [ ] **识别新的可提取模式**
- [ ] 如有需要，添加新的 common 辅助函数
- [ ] 回顾并更新已迁移的 scanner

### Task 2.4: Migrate blocking_operations scanner (40 min)

- [ ] 创建 `upcast/scanners/blocking_operations.py`
- [ ] 从 `blocking_operation_scanner/` 迁移代码
- [ ] **使用最新的 common 工具**
- [ ] 使用 `models.blocking_operations` 中的模型
- [ ] 更新测试导入路径
- [ ] 运行测试验证
- [ ] 删除 `blocking_operation_scanner/` 目录

### Task 2.5: Migrate http_requests scanner (40 min)

- [ ] 创建 `upcast/scanners/http_requests.py`
- [ ] 从 `http_request_scanner/` 迁移代码
- [ ] **复用 common 工具**
- [ ] 使用 `models.http_requests` 中的模型
- [ ] 更新测试导入路径
- [ ] 运行测试验证
- [ ] 删除 `http_request_scanner/` 目录

### Task 2.6: Migrate metrics scanner (40 min)

- [ ] 创建 `upcast/scanners/metrics.py`
- [ ] 从 `prometheus_metrics_scanner/` 迁移代码
- [ ] **复用 common 工具**
- [ ] 使用 `models.metrics` 中的模型
- [ ] 更新测试导入路径
- [ ] 运行测试验证
- [ ] 删除 `prometheus_metrics_scanner/` 目录

### Task 2.7: Migrate concurrency scanner (40 min)

- [ ] 创建 `upcast/scanners/concurrency.py`
- [ ] 从 `concurrency_pattern_scanner/` 迁移代码
- [ ] **复用 common 工具**
- [ ] 使用 `models.concurrency` 中的模型
- [ ] 更新测试导入路径
- [ ] 运行测试验证
- [ ] 删除 `concurrency_pattern_scanner/` 目录

## Phase 3: Migrate Complex Scanners (3.5 hours)

### Task 3.1: Review and consolidate common patterns (20 min)

- [ ] 审查已迁移的 7 个 scanner
- [ ] **确认 common 工具的效果**
- [ ] **识别剩余 scanner 可能需要的新工具**
- [ ] 更新 common 模块文档

### Task 3.2: Migrate exceptions scanner (40 min)

- [ ] 创建 `upcast/scanners/exceptions.py`
- [ ] 从 `exception_handler_scanner/` 迁移代码
- [ ] **使用 common 工具**（AST 遍历、节点匹配等）
- [ ] 使用 `models.exceptions` 中的模型
- [ ] 更新测试导入路径
- [ ] 运行测试验证
- [ ] 删除 `exception_handler_scanner/` 目录

### Task 3.3: Migrate unit_tests scanner (40 min)

- [ ] 创建 `upcast/scanners/unit_tests.py`
- [ ] 从 `unit_test_scanner/` 迁移代码
- [ ] **使用 common 工具**
- [ ] 使用 `models.unit_tests` 中的模型
- [ ] 更新测试导入路径
- [ ] 运行测试验证
- [ ] 删除 `unit_test_scanner/` 目录

### Task 3.4: Migrate django_urls scanner (40 min)

- [ ] 创建 `upcast/scanners/django_urls.py`
- [ ] 从 `django_url_scanner/` 迁移代码
- [ ] **使用 common 工具**
- [ ] 使用 `models.django_urls` 中的模型
- [ ] 更新测试导入路径
- [ ] 运行测试验证
- [ ] 删除 `django_url_scanner/` 目录

### Task 3.5: Migrate django_models scanner (50 min)

- [ ] 创建 `upcast/scanners/django_models.py`
- [ ] 从 `django_model_scanner/` 迁移代码
- [ ] **使用 common 工具简化字段和关系解析**
- [ ] 使用 `models.django_models` 中的模型
- [ ] 处理复杂的字段和关系解析
- [ ] 更新测试导入路径
- [ ] 运行测试验证
- [ ] 删除 `django_model_scanner/` 目录

### Task 3.6: Migrate django_settings scanner (50 min)

- [ ] 创建 `upcast/scanners/django_settings.py`
- [ ] 从 `django_settings_scanner/` 迁移代码
- [ ] **使用 common 工具**
- [ ] 使用 `models.django_settings` 中的 3 种输出模型
- [ ] 处理 usage/definition/combined 三种模式
- [ ] 更新测试导入路径
- [ ] 运行测试验证
- [ ] 删除 `django_settings_scanner/` 目录

## Phase 4: Integration and Cleanup (1.5 hours)

### Task 4.1: Update scanners/**init**.py (15 min)

- [ ] 导出所有 scanner 类
- [ ] 添加 `__all__` 列表
- [ ] 确保可以 `from upcast.scanners import *`

### Task 4.2: Update pyproject.toml (15 min)

- [ ] 更新所有 CLI entry points 指向新路径
- [ ] 验证所有 `upcast scan-xxx` 命令工作

### Task 4.3: Update internal imports (30 min)

- [ ] 搜索并更新所有 `from upcast.xxx_scanner` 导入
- [ ] 更新 `main.py` 中的导入
- [ ] 更新测试中的导入（如果有遗漏）

### Task 4.4: Clean up old directories (15 min)

- [ ] 确认所有 `xxx_scanner/` 目录已删除
- [ ] 验证没有残留的旧代码
- [ ] 检查 git status 确保变更正确

### Task 4.5: Update documentation (15 min)

- [ ] 更新 README.md 中的导入示例
- [ ] 如果有 API 文档，更新导入路径
- [ ] 更新 Architecture 部分说明新的目录结构

## Phase 5: Quality Assurance (1.5 hours)

### Task 5.1: Test common module enhancements (20 min)

- [ ] 运行 common 模块的单元测试
- [ ] 确保所有新增函数有测试覆盖
- [ ] 验证测试覆盖率 >= 80%

### Task 5.2: Run all scanner tests (20 min)

- [ ] `uv run pytest tests/ -v`
- [ ] 确保所有 640+ 测试通过
- [ ] 修复任何失败的测试

### Task 5.3: Code quality metrics (20 min)

- [ ] **检查代码重复率**: 使用工具或手动审查
- [ ] **验证 scanner 代码量**: 每个 scanner < 200 行
- [ ] **审查 common 模块使用**: 确保所有 scanner 都在使用
- [ ] 记录改进指标（减少的代码行数、重复率等）

### Task 5.4: Type checking (15 min)

- [ ] `uv run mypy upcast/scanners/`
- [ ] `uv run mypy upcast/common/`
- [ ] 修复任何类型错误
- [ ] 确保所有新代码都有正确的类型注解

### Task 5.5: Linting (15 min)

- [ ] `uv run ruff check upcast/scanners/`
- [ ] `uv run ruff format upcast/scanners/`
- [ ] `uv run ruff check upcast/common/`
- [ ] 修复任何代码风格问题

### Task 5.6: Integration testing (10 min)

- [ ] 手动运行每个 CLI 命令验证输出
- [ ] 确保输出格式与之前保持一致
- [ ] 测试 --help 输出正确

## Estimated Total Time: 12 hours

**Notes**:

- **重点关注代码复用**: 每迁移 2-3 个 scanner 就审查一次，提取通用模式
- **保持简洁**: scanner 应该专注于业务逻辑，< 200 行代码
- **测试驱动**: 新增的 common 函数必须有测试覆盖
- 每个 scanner 迁移后立即运行测试，避免积累问题
- 如果某个 scanner 特别复杂，可以单独增加时间
- 保持与 signals.py 的一致性，它是最佳实践模板
