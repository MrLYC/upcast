# Unit Test Scanner Proposal

## Why

Python 项目单元测试缺乏结构化分析工具。开发者需要快速了解测试覆盖情况、测试目标和测试质量指标。当前没有工具能自动分析单元测试的结构、测试目标依赖关系和断言数量。

这个扫描器将帮助：

- 快速生成项目单元测试清单
- 识别每个测试的目标模块和符号
- 通过断言数量评估测试质量
- 追踪测试代码变化（通过 MD5）

## What Changes

- 新增 `unit-test-scanner` 规范和实现
- 新增 `scan-unit-tests` CLI 命令
- 实现基于 AST 的 pytest/unittest 测试函数解析
- 实现测试目标依赖分析（基于 root_modules 配置）
- 实现断言计数和函数体 MD5 计算
- 复用 `common-utilities` 中的文件发现、AST 推断和导出功能
- 输出格式：YAML/JSON，包含测试名称、位置、断言数量、MD5 和测试目标

## Impact

- 新增规范: `unit-test-scanner`
- 新增代码: `upcast/unit_test_scanner/` 目录
  - `cli.py` - CLI 命令实现
  - `test_parser.py` - 测试函数解析逻辑
  - `checker.py` - AST 遍历和测试检测
  - `export.py` - YAML/JSON 导出
- 新增测试: `tests/test_unit_test_scanner/`
- 更新: `upcast/main.py` 注册新命令
- 复用: `upcast/common/` 模块（file_utils, ast_utils, export）
