# Proposal: Add Module Symbol Scanner

## Why

Python 项目中，了解模块导出的公共 API 和符号对于以下场景至关重要：

1. **API 分析**：识别可被外部模块导入和使用的符号
2. **依赖追踪**：理解模块之间的导入关系和符号使用
3. **重构支持**：在重构时了解哪些符号是公共 API，避免破坏性变更
4. **文档生成**：自动提取模块的公共接口用于文档
5. **代码迁移**：分析模块的导入模式，识别可能的迁移点

目前 upcast 缺少一个专门分析模块符号和导入关系的扫描器。添加此功能可以：

- 提供模块级别的符号可见性分析
- 追踪导入的模块和符号的使用情况
- 识别模块定义的公共变量、函数和类
- 检测属性访问模式，了解符号的实际使用方式

## What Changes

### 核心修改

添加一个新的 `Module Symbol Scanner`，扫描 Python 模块并提取：

1. **导入分析**

   - `imported_module`: 完整导入的模块（如 `import xxx.yyy`）
   - `imported_symbols`: 从模块导入的符号（如 `from xxx import yyy`）
   - `star_imported`: 星号导入的模块（如 `from xxx import *`）

2. **模块级别符号**

   - `variables`: 模块级别的变量（排除私有变量）
   - `functions`: 模块级别的函数（排除私有函数）
   - `classes`: 模块级别的类（排除私有类）

3. **符号元数据**
   - 定义所在的块类型（module, if, try, except, function）
   - 属性访问模式（追踪使用了哪些属性）
   - 装饰器信息
   - 函数签名、docstring、body_md5
   - 类的基类、方法、属性

### 输出格式

```yaml
summary:
  total_modules: 10
  total_imports: 50
  total_symbols: 100
  files_scanned: 10
  scan_duration_ms: 150

results:
  path/to/file.py:
    imported_modules:
      xxx:
        module_path: xxx
        attributes: ["yyy"]
        blocks: ["module"]
    imported_symbols:
      yyy:
        module_path: xxx.yyy
        attributes: ["zzz"]
        blocks: ["module", "try"]
    star_imported:
      - module_path: xxx.yyy
        blocks: ["module"]
    variables:
      my_var:
        module_path: path.to.file
        attributes: []
        value: "computed_value"
        statement: "my_var = compute()"
        blocks: ["module"]
    functions:
      my_func:
        signature: "def my_func(arg1: int, arg2: str) -> bool"
        docstring: "Function description"
        body_md5: "abc123..."
        attributes: []
        decorators:
          - name: decorator_name
            args: []
            kwargs: {}
        blocks: ["module"]
    classes:
      MyClass:
        docstring: "Class description"
        body_md5: "def456..."
        attributes: ["attr1", "attr2"]
        methods: ["method1", "method2"]
        bases: ["BaseClass"]
        decorators:
          - name: dataclass
            args: []
            kwargs: {}
        blocks: ["module"]
```

### 技术实现

1. **新增文件**

   - `upcast/models/module_symbols.py`: 数据模型定义
   - `upcast/scanners/module_symbols.py`: 扫描器实现
   - `tests/test_module_symbol_scanner/`: 单元测试

2. **扫描器架构**

   - 继承 `BaseScanner[ModuleSymbolOutput]`
   - 使用 astroid 进行 AST 分析
   - 追踪符号定义的块上下文
   - 分析属性访问模式

3. **CLI 集成**
   - 添加 `scan-module-symbols` 命令
   - 支持标准的文件过滤选项

## Benefits

1. **完整性**：与其他扫描器形成互补，提供模块级别的符号视图
2. **可扩展**：为未来的依赖分析、影响面分析等功能奠定基础
3. **实用性**：帮助开发者理解代码结构和模块接口
4. **一致性**：遵循现有扫描器的架构和输出格式
5. **性能**：静态分析，无需执行代码

## Risks & Mitigations

| Risk                   | Mitigation                                         |
| ---------------------- | -------------------------------------------------- |
| 复杂的动态导入难以分析 | 专注于静态可分析的导入模式，对动态导入提供有限支持 |
| 属性访问追踪可能不准确 | 使用启发式方法，提供"最佳努力"的结果               |
| 性能问题（大型项目）   | 优化 AST 遍历，支持增量扫描                        |
| 输出数据量大           | 提供过滤选项，只输出感兴趣的符号类型               |

## Alternatives Considered

1. **使用 AST 模块而非 astroid**

   - ❌ astroid 提供更好的类型推断和名称解析

2. **只扫描导入，不分析符号定义**

   - ❌ 功能不完整，无法提供模块的完整视图

3. **集成到现有扫描器（如 django-models）**

   - ❌ 职责混乱，不符合单一职责原则

4. **创建独立的符号扫描器（推荐）**
   - ✅ 清晰的职责划分，可复用，易维护
