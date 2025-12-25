# OpenSpec Change: add-module-symbol-scanner

## Status

✅ **Valid** - 已通过严格验证 (`openspec validate --strict`)

## 概述

添加一个新的 **Module Symbol Scanner**，用于分析 Python 模块的导入关系和公共符号（变量、函数、类）。

## 文件结构

```
openspec/changes/add-module-symbol-scanner/
├── proposal.md                            # 提案文档
├── tasks.md                               # 任务分解和进度追踪
└── specs/
    └── module-symbol-scanner/
        └── spec.md                        # 规范定义（包含需求和场景）
```

## 核心功能

### 1. 导入分析

- `imported_modules`: 完整模块导入（`import xxx`）
- `imported_symbols`: 符号导入（`from xxx import yyy`）
- `star_imported`: 星号导入（`from xxx import *`）
- 追踪导入所在的块上下文（module, if, try, except, function, class）
- 分析符号的属性访问模式

### 2. 符号提取

- `variables`: 模块级别变量（含值、赋值语句、块上下文）
- `functions`: 模块级别函数（含签名、docstring、装饰器、body_md5）
- `classes`: 模块级别类（含基类、方法、属性、装饰器、body_md5）
- 默认排除私有符号（`_xxx`），可通过 `--include-private` 包含

### 3. 输出格式

- 遵循标准的 `ScannerOutput` 格式
- 提供汇总统计（总模块数、总导入数、总符号数等）
- 支持 YAML/JSON 输出

## CLI 接口

```bash
# 基本使用
uv run upcast scan-module-symbols /path/to/project

# 排除测试文件
uv run upcast scan-module-symbols --exclude-files "test_*.py" .

# 包含私有符号
uv run upcast scan-module-symbols --include-private .

# 输出到文件
uv run upcast scan-module-symbols --output-file results.yaml .
```

## 技术实现

### 新增文件

- `upcast/models/module_symbols.py` - 数据模型（Pydantic v2）
- `upcast/scanners/module_symbols.py` - 扫描器实现
- `tests/test_module_symbol_scanner/` - 单元测试

### 架构

- 继承 `BaseScanner[ModuleSymbolOutput]`
- 使用 astroid 进行 AST 分析
- 遵循现有扫描器的模式和约定

## 实施计划

分为 5 个阶段（详见 [tasks.md](tasks.md)）：

1. **Phase 1**: 数据模型定义（2-3 小时）
2. **Phase 2**: 扫描器核心实现（4-6 小时）
3. **Phase 3**: 测试覆盖（3-4 小时）
4. **Phase 4**: CLI 和文档（1-2 小时）
5. **Phase 5**: 质量保证（1 小时）

**预计总时间**: 11-16 小时

## 验收标准

- ✅ 所有需求场景通过测试
- ✅ 测试覆盖率 ≥ 80%
- ✅ 通过 ruff check 和 pre-commit 检查
- ✅ README 和 CHANGELOG 更新完整
- ✅ 在真实项目（example/blueking-paas）上验证成功

## 下一步

1. 用户审查并批准提案
2. 开始实施 Phase 1（数据模型定义）
3. 按阶段完成实现和测试
4. 更新文档和示例
5. 提交代码审查

## 查看详情

```bash
# 查看完整提案
openspec change show add-module-symbol-scanner

# 查看需求和场景
cat openspec/changes/add-module-symbol-scanner/specs/module-symbol-scanner/spec.md

# 查看任务分解
cat openspec/changes/add-module-symbol-scanner/tasks.md
```
