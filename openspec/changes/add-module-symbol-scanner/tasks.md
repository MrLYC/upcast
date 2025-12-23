# Tasks: Add Module Symbol Scanner

## Implementation Phases

### Phase 1: 数据模型定义 ✅

#### Task 1.1: 创建基础数据模型

- 创建 `upcast/models/module_symbols.py`
- 定义 `ImportedModule`, `ImportedSymbol`, `StarImport` 模型
- 定义 `Variable`, `Function`, `Class` 模型
- 定义 `ModuleSymbols` (文件级结果) 和 `ModuleSymbolOutput` (扫描器输出)
- 确保所有模型继承自 `BaseModel`，使用 Pydantic v2 语法

**验收标准：**

- [ ] 所有数据模型定义完整
- [ ] 符合 Pydantic v2 规范
- [ ] 包含完整的字段文档
- [ ] 通过 ruff 检查

---

### Phase 2: 扫描器核心实现 🔄

#### Task 2.1: 创建扫描器骨架

- 创建 `upcast/scanners/module_symbols.py`
- 实现 `ModuleSymbolScanner` 类，继承 `BaseScanner[ModuleSymbolOutput]`
- 实现 `scan_file()` 方法骨架
- 添加扫描器注册

**验收标准：**

- [ ] 扫描器类结构正确
- [ ] 正确继承 `BaseScanner`
- [ ] 在 `main.py` 中注册
- [ ] 可以被 CLI 调用

#### Task 2.2: 实现导入分析

- 解析 `import xxx` 语句 → `imported_modules`
- 解析 `from xxx import yyy` 语句 → `imported_symbols`
- 解析 `from xxx import *` 语句 → `star_imported`
- 追踪导入所在的块上下文（module, if, try, etc.）
- 分析符号的属性访问模式

**验收标准：**

- [ ] 正确识别所有导入类型
- [ ] 准确追踪块上下文
- [ ] 提取属性访问信息
- [ ] 处理嵌套导入

#### Task 2.3: 实现符号定义分析

- 识别模块级别的变量定义 → `variables`
- 识别模块级别的函数定义 → `functions`
- 识别模块级别的类定义 → `classes`
- 排除私有符号（`_xxx`，可配置）
- 提取装饰器信息
- 提取 docstring
- 计算 body_md5

**验收标准：**

- [ ] 正确识别所有符号类型
- [ ] 准确排除私有符号
- [ ] 提取完整的元数据
- [ ] 处理各种定义位置（module, if, try, etc.）

#### Task 2.4: 实现属性访问追踪

- 分析符号的属性访问（`obj.attr`）
- 追踪链式属性访问（`obj.attr1.attr2`）
- 处理特殊情况（动态属性、`getattr` 等）

**验收标准：**

- [ ] 准确追踪属性访问
- [ ] 处理链式访问
- [ ] 对动态访问提供最佳努力支持

---

### Phase 3: 测试覆盖 📝

#### Task 3.1: 单元测试 - 数据模型

- 测试所有数据模型的序列化/反序列化
- 测试模型验证规则
- 测试边界情况

**验收标准：**

- [ ] 覆盖所有模型
- [ ] 测试通过
- [ ] 覆盖率 ≥ 80%

#### Task 3.2: 单元测试 - 导入分析

- 测试各种导入语句的解析
- 测试块上下文追踪
- 测试属性访问分析
- 测试边界情况（动态导入、条件导入等）

**验收标准：**

- [ ] 覆盖所有导入类型
- [ ] 测试通过
- [ ] 覆盖率 ≥ 80%

#### Task 3.3: 单元测试 - 符号定义分析

- 测试变量、函数、类的识别
- 测试装饰器提取
- 测试 docstring 提取
- 测试 body_md5 计算
- 测试私有符号过滤

**验收标准：**

- [ ] 覆盖所有符号类型
- [ ] 测试通过
- [ ] 覆盖率 ≥ 80%

#### Task 3.4: 集成测试

- 创建 `tests/test_module_symbol_scanner/test_integration.py`
- 使用真实项目样本（example/blueking-paas）
- 验证输出格式和内容
- 测试性能（大型项目）

**验收标准：**

- [ ] 集成测试通过
- [ ] 真实项目扫描成功
- [ ] 输出格式正确
- [ ] 性能可接受

---

### Phase 4: CLI 和文档 📚

#### Task 4.1: CLI 集成

- 在 `main.py` 中添加 `scan-module-symbols` 命令
- 支持标准的文件过滤选项
- 支持输出格式选项（YAML/JSON）

**验收标准：**

- [ ] CLI 命令可用
- [ ] 帮助信息完整
- [ ] 选项正常工作

#### Task 4.2: 文档更新

- 在 `README.md` 中添加使用说明
- 提供示例输出
- 更新 `CHANGELOG.md`
- 在 `example/scan-results/` 中添加示例结果

**验收标准：**

- [ ] 文档完整准确
- [ ] 示例清晰易懂
- [ ] 与其他扫描器风格一致

---

### Phase 5: 质量保证 ✨

#### Task 5.1: 代码质量检查

- 运行 `ruff check` 确保无错误
- 运行 `ruff format` 确保格式一致
- 运行 `pre-commit run --all-files` 确保所有检查通过

**验收标准：**

- [ ] ruff check 通过
- [ ] ruff format 通过
- [ ] pre-commit 通过

#### Task 5.2: 测试覆盖率

- 运行 `uv run pytest --cov=upcast.scanners.module_symbols --cov=upcast.models.module_symbols`
- 确保覆盖率 ≥ 80%
- 补充缺失的测试用例

**验收标准：**

- [ ] 总覆盖率 ≥ 80%
- [ ] 关键路径 100% 覆盖

---

## Progress Tracking

- Phase 1: ⬜ Not Started
- Phase 2: ⬜ Not Started
- Phase 3: ⬜ Not Started
- Phase 4: ⬜ Not Started
- Phase 5: ⬜ Not Started

## Dependencies

- astroid 库（已在 pyproject.toml 中）
- BaseScanner 架构（已存在）
- Pydantic v2（已存在）

## Estimated Effort

- Phase 1: 2-3 小时
- Phase 2: 4-6 小时
- Phase 3: 3-4 小时
- Phase 4: 1-2 小时
- Phase 5: 1 小时

**Total**: 11-16 小时
