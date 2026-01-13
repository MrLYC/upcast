# 模块符号扫描器 (module-symbols)

## 概述

模块符号扫描器用于分析 Python 模块中的导入语句和符号定义。它能够提取模块导入、符号导入、星号导入、以及模块级别的变量、函数和类定义。

该扫描器对于以下场景特别有用：

- 分析模块依赖关系
- 识别未使用的导入
- 生成模块接口文档
- 重构和依赖优化
- 代码结构分析

## 命令使用

```bash
upcast scan-module-symbols [OPTIONS] [PATH]
```

### 参数

- `PATH` - 要扫描的 Python 文件或目录路径（可选，默认为当前目录 `.`）

### 选项

- `-o, --output PATH` - 输出文件路径
- `-v, --verbose` - 启用详细输出
- `--format [yaml|json|markdown]` - 输出格式（默认：yaml）
- `--markdown-language [en|zh]` - Markdown 输出语言（默认：zh）
- `--markdown-title TEXT` - Markdown 输出标题
- `--include PATTERN` - 包含的文件模式（可多次指定）
- `--exclude PATTERN` - 排除的文件模式（可多次指定）
- `--no-default-excludes` - 禁用默认排除模式
- `--include-private` - 包含私有符号（以 `_` 开头）

### 使用示例

```bash
# 扫描当前目录
upcast scan-module-symbols .

# 包含私有符号
upcast scan-module-symbols ./src --include-private

# 保存结果到文件
upcast scan-module-symbols ./myproject --output symbols.yaml

# 输出为 JSON 格式
upcast scan-module-symbols ./app --format json
```

## 字段说明

### metadata 字段

存放扫描命令的参数和配置信息。

| 字段名       | 类型          | 必填 | 说明               |
| ------------ | ------------- | ---- | ------------------ |
| scanner_name | string        | 是   | 扫描器名称         |
| command_args | array[string] | 否   | 扫描命令的参数列表 |

### summary 字段

`summary` 包含扫描统计信息。

| 字段名           | 类型    | 必填 | 说明             |
| ---------------- | ------- | ---- | ---------------- |
| total_modules    | integer | 是   | 模块总数         |
| total_symbols    | integer | 是   | 符号总数         |
| total_imports    | integer | 是   | 导入语句总数     |
| files_scanned    | integer | 是   | 扫描的文件总数   |
| scan_duration_ms | integer | 是   | 扫描耗时（毫秒） |
| total_count      | integer | 是   | 符号总数         |

### results 字段

`results` 是一个字典，键为模块文件路径，值为模块符号对象。

#### 模块符号对象

| 字段名           | 类型                  | 必填 | 说明                                             |
| ---------------- | --------------------- | ---- | ------------------------------------------------ |
| imported_modules | array[ImportedModule] | 是   | 导入的模块（仅处理 `import module`）             |
| imported_symbols | array[ImportedSymbol] | 是   | 导入的符号（仅处理 `from module import symbol`） |
| variables        | array[Variable]       | 是   | 模块级变量定义                                   |
| functions        | array[Function]       | 是   | 模块级函数定义                                   |
| classes          | array[Class]          | 是   | 模块级类定义                                     |

#### 导入的模块（ImportedModule）

| 字段名      | 类型        | 必填 | 说明                                                           |
| ----------- | ----------- | ---- | -------------------------------------------------------------- |
| module_path | string      | 是   | 模块路径（仅收集作用域为模块级别的导入）                       |
| name        | string      | 是   | 导入的名称列表（ `import a ` 时为 `a`，`import b.c` 时为 `b`） |
| lineno      | integer     | 是   | 导入语句所在行号                                               |
| statement   | string      | 是   | 导入语句的源代码字符串                                         |
| block       | string/null | 是   | 变量值的代码块（`if`、`try`、`except`等）                      |

#### 导入的符号（ImportedSymbol）

| 字段名      | 类型          | 必填 | 说明                                                                             |
| ----------- | ------------- | ---- | -------------------------------------------------------------------------------- |
| module_path | string        | 是   | 来源模块的完整路径（仅收集作用域为模块级别的导入）                               |
| imports     | array[string] | 是   | 导入的符号列表，`from a import b, c` 时为 `[b, c]`，`from a import *` 时为 `[*]` |
| lineno      | integer       | 是   | 导入语句所在行号                                                                 |
| statement   | string        | 是   | 导入语句的源代码字符串                                                           |
| block       | string/null   | 是   | 变量值的代码块（`if`、`try`、`except`等）                                        |

#### 变量声明（Variable）

| 字段名 | 类型        | 必填 | 说明                                      |
| ------ | ----------- | ---- | ----------------------------------------- |
| name   | string      | 是   | 变量名(作用域为模块级别)                  |
| lineno | integer     | 是   | 变量声明所在行号                          |
| value  | object      | 是   | 推导的变量值                              |
| type   | string/null | 是   | 推导的变量类型（无法推导时为 `null`）     |
| block  | string/null | 是   | 变量值的代码块（`if`、`try`、`except`等） |

#### 装饰器声明（Decorator）

| 字段名 | 类型    | 必填 | 说明                   |
| ------ | ------- | ---- | ---------------------- |
| name   | string  | 是   | 装饰器名称             |
| lineno | integer | 是   | 装饰器所在行号         |
| call   | boolean | 是   | 装饰器是否带参数调用   |
| args   | array   | 是   | 位置参数列表（字面量） |
| kwargs | any     | 是   | 关键字参数（字面量）   |

#### 函数声明（Function）

| 字段名     | 类型             | 必填 | 说明                                      |
| ---------- | ---------------- | ---- | ----------------------------------------- |
| name       | string           | 是   | 函数名（作用域为模块级别）                |
| lineno     | integer          | 是   | 函数定义所在行号                          |
| is_async   | boolean          | 是   | 是否为异步函数                            |
| signature  | string           | 是   | 函数签名                                  |
| docstring  | string/null      | 是   | docstring（无 docstring 为 `null`）       |
| decorators | array[Decorator] | 是   | 装饰器列表（结构见下）                    |
| body_md5   | string           | 是   | 函数体的 MD5（用于变更追踪）              |
| block      | string/null      | 是   | 变量值的代码块（`if`、`try`、`except`等） |

#### 类声明（Class）

| 字段名     | 类型             | 必填 | 说明                                      |
| ---------- | ---------------- | ---- | ----------------------------------------- |
| name       | string           | 是   | 类名（作用域为模块级别）                  |
| lineno     | integer          | 是   | 类定义所在行号                            |
| bases      | array[string]    | 是   | 基类列表                                  |
| docstring  | string/null      | 是   | docstring（无 docstring 为 `null`）       |
| decorators | array[Decorator] | 是   | 装饰器列表（结构同上）                    |
| methods    | array[Function]  | 是   | 方法列表                                  |
| body_md5   | string           | 是   | 类体的 MD5（用于变更追踪）                |
| attributes | array[Variable]  | 是   | 类属性/字段名列表                         |
| block      | string/null      | 是   | 变量值的代码块（`if`、`try`、`except`等） |

## 使用示例

以下是扫描结果的示例：

```yaml
metadata:
  scanner_name: module_symbols
  command_args:
    - scan-module-symbols
    - ./src
    - --format
    - yaml
    - --include-private

summary:
  total_modules: 3
  total_symbols: 18
  total_imports: 8
  files_scanned: 3
  scan_duration_ms: 245
  total_count: 18

results:
  src/config/settings.py:
    imported_modules:
      - name: os
        module_path: os
        lineno: 1
        statement: "import os"
        block: null
      - name: sys
        module_path: sys
        lineno: 2
        statement: "import sys"
        block: if
    imported_symbols:
      - module_path: django.conf.settings
        imports:
          - settings
        lineno: 5
        statement: "from django.conf import settings"
        block: try
      - module_path: config.base
        imports:
          - *
        lineno: 6
        statement: "from config.base import *"
        block: null
    variables:
      - name: DEBUG
        lineno: 8
        value: true
        type: bool
        block: null
      - name: ALLOWED_HOSTS
        lineno: 9
        value:
          - localhost
          - 127.0.0.1
        type: list
        block: null
      - name: SECRET_KEY
        lineno: 10
        value: null
        type: null
        block: null
    functions: []
    classes: []
  src/models/user.py:
    imported_modules:
      - name: django
        module_path: django
        lineno: 1
        statement: "import django"
        block: null
    imported_symbols:
      - module_path: django.db.models
        imports:
          - models
        lineno: 2
        statement: "from django.db import models"
        block: null
      - module_path: django.utils.timezone
        imports:
          - timezone
        lineno: 3
        statement: "from django.utils import timezone"
        block: null
      - module_path: validators.user
        imports:
          - validate_email
        lineno: 4
        statement: "from validators.user import validate_email"
        block: null
    star_imported: []
    variables: []
    functions:
      - name: get_user_by_id
        lineno: 12
        is_async: false
        signature: "def get_user_by_id(user_id: int) -> Optional[User]"
        docstring: "Retrieve user by ID from database"
        decorators: []
        body_md5: "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
        block: null
      - name: get_active_users
        lineno: 18
        is_async: true
        signature: "async def get_active_users(limit: int = 10) -> list[User]"
        docstring: "Fetch all active users asynchronously"
        decorators:
          - name: cache_result
            lineno: 17
            call: true
            args:
              - 3600
            kwargs:
              namespace: users
        body_md5: "f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1"
        block: null
    classes:
      - name: User
        lineno: 25
        bases:
          - models.Model
        docstring: "User model for authentication"
        decorators: []
        methods:
          - name: save
            lineno: 28
            is_async: false
            signature: "def save(self, *args, **kwargs) -> None"
            docstring: null
            decorators: []
            body_md5: "c2d3e4f5g6h7i8j9k0l1m2n3o4p5q6r7"
            block: null
          - name: __str__
            lineno: 31
            is_async: false
            signature: "def __str__(self) -> str"
            docstring: null
            decorators: []
            body_md5: "d3e4f5g6h7i8j9k0l1m2n3o4p5q6r7s8"
            block: null
        attributes:
          - name: username
            lineno: 26
            value: null
            type: CharField
            block: null
          - name: email
            lineno: 27
            value: null
            type: EmailField
            block: null
          - name: created_at
            lineno: 28
            value: null
            type: DateTimeField
            block: null
        body_md5: "b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7"
        block: null

  src/middleware/auth.py:
    imported_modules:
      - name: logging
        module_path: logging
        lineno: 1
        statement: "import logging"
        block: null
    imported_symbols:
      - module_path: django.utils.deprecation
        imports:
          - MiddlewareMixin
        lineno: 2
        statement: "from django.utils.deprecation import MiddlewareMixin"
        block: null
      - module_path: django.contrib.auth.models
        imports:
          - get_user_model
          - AnonymousUser
        lineno: 3
        statement: "from django.contrib.auth.models import get_user_model, AnonymousUser"
        block: null
    star_imported:
      - http.status
    variables:
      - name: logger
        lineno: 6
        value: null
        type: null
        block: null
    functions:
      - name: extract_token
        lineno: 8
        is_async: false
        signature: "def extract_token(request: HttpRequest) -> Optional[str]"
        docstring: null
        decorators: []
        body_md5: "c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8"
        block: null
    classes:
      - name: AuthMiddleware
        lineno: 18
        bases:
          - MiddlewareMixin
        docstring: "Custom authentication middleware"
        decorators:
          - name: deprecated
            lineno: 17
            call: true
            args: []
            kwargs:
              reason: "Use TokenAuth instead"
        methods:
          - name: __init__
            lineno: 19
            is_async: false
            signature: "def __init__(self, get_response: Callable) -> None"
            docstring: null
            decorators: []
            body_md5: "e4f5g6h7i8j9k0l1m2n3o4p5q6r7s8t9"
            block: null
          - name: __call__
            lineno: 22
            is_async: false
            signature: "def __call__(self, request: HttpRequest) -> HttpResponse"
            docstring: null
            decorators: []
            body_md5: "f5g6h7i8j9k0l1m2n3o4p5q6r7s8t9u0"
            block: null
          - name: process_request
            lineno: 25
            is_async: false
            signature: "def process_request(self, request: HttpRequest) -> None"
            docstring: null
            decorators: []
            body_md5: "g6h7i8j9k0l1m2n3o4p5q6r7s8t9u0v1"
            block: null
        attributes:
          - name: allowed_paths
            lineno: 19
            value: null
            type: list
            block: null
          - name: cache_timeout
            lineno: 20
            value: 3600
            type: int
            block: null
        body_md5: "d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9"
        block: null
```

### 示例说明

上述示例展示了三个模块扫描结果，覆盖不同的符号类型和场景：

1. **src/config/settings.py** - 配置模块示例

   - 展示 `imported_modules`（模块导入）
   - 展示 `imported_symbols`（符号导入）
   - 展示 `variables`（配置变量），包含基本类型、复杂类型和无法推导类型的案例
   - 未包含 functions 和 classes（为空）

2. **src/models/user.py** - 数据模型模块示例

   - 展示单个符号和多符号的导入
   - 展示带装饰器的 `functions`（缓存装饰器带参数调用）
   - 展示 `async` 异步函数
   - 展示包含 docstring 的函数和类
   - 展示 `classes` 及其 methods 列表、attributes 列表
   - 展示 body_md5 用于变更追踪

3. **src/middleware/auth.py** - 中间件模块示例
   - 展示多个装饰器参数形式
   - 展示 `classes` 包含多个方法的情况
   - 展示 `deprecated` 装饰器带 kwargs 参数的形式
   - 展示无 docstring 的函数（为 null）

**metadata 字段**：

- `scanner_name`：扫描器标识
- `command_args`：完整的扫描命令参数

**summary 字段统计**：

- `total_modules`：扫描到 3 个模块
- `total_symbols`：共 18 个符号（导入 + 定义）
- `total_imports`：8 条导入语句
- `files_scanned`：3 个文件
- `scan_duration_ms`：耗时 245 毫秒

## 注意事项

1. **私有符号** - 默认情况下不包含以 `_` 开头的私有符号，使用 `--include-private` 包含它们。

2. **签名格式** - 函数签名包含参数名、类型提示（如果有）、默认值等完整信息。

3. **文档字符串** - 如果函数或类有 docstring，会被提取到 `docstring` 字段。

4. **异步函数** - `is_async` 标识函数是否使用 `async def` 定义。
