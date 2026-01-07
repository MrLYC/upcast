# 日志扫描器 (logging)

## 概述

日志扫描器用于分析 Python 代码中的日志语句。它支持多种日志库（标准库 logging、loguru、structlog、Django 日志），能够检测日志级别、消息内容、敏感信息模式，以及日志器的创建和使用。

该扫描器对于以下场景特别有用：

- 审查日志级别使用是否合理
- 检测日志中的敏感信息泄露（密码、token 等）
- 统计日志使用情况
- 生成日志文档
- 日志标准化和优化

## 命令使用

```bash
upcast scan-logging [OPTIONS] [PATH]
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
- `--sensitive-keywords KEYWORD` - 自定义敏感关键词（可多次指定）

### 使用示例

```bash
# 扫描当前目录
upcast scan-logging ./src

# 保存结果到文件
upcast scan-logging ./myproject --output logs.yaml

# 输出为 JSON 格式
upcast scan-logging ./app --format json --verbose

# 添加自定义敏感关键词
upcast scan-logging ./src --sensitive-keywords password --sensitive-keywords token

# 仅扫描特定目录
upcast scan-logging ./app --include "app/services/**"
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

| 字段名           | 类型                 | 必填 | 说明                       |
| ---------------- | -------------------- | ---- | -------------------------- |
| total_log_calls  | integer              | 是   | 日志调用总数               |
| by_level         | map[string, integer] | 是   | 按日志级别分组的数量       |
| by_library       | map[string, integer] | 是   | 按日志库分组的数量         |
| sensitive_calls  | integer              | 是   | 包含敏感信息的日志调用数量 |
| files_scanned    | integer              | 是   | 扫描的文件总数             |
| scan_duration_ms | integer              | 是   | 扫描耗时（毫秒）           |
| total_count      | integer              | 是   | 日志调用总数               |

### results 字段

`results` 是一个字典，键为文件路径，值为日志分类对象列表。

#### 日志分类对象

每个文件的日志调用按使用的库类别进行分组：

| 字段名    | 类型  | 必填 | 说明                    |
| --------- | ----- | ---- | ----------------------- |
| logging   | array | 是   | 标准库 logging 日志列表 |
| loguru    | array | 是   | loguru 日志列表         |
| structlog | array | 是   | structlog 日志列表      |
| django    | array | 是   | Django 日志列表         |

#### 日志条目对象

| 字段名             | 类型          | 必填 | 说明                                                                     |
| ------------------ | ------------- | ---- | ------------------------------------------------------------------------ |
| lineno             | integer       | 是   | 行号                                                                     |
| library            | string        | 是   | 使用的日志库名称（`logging`, `loguru`, `structlog`）                     |
| level              | string        | 是   | 日志级别（`debug`, `info`, `warning`, `error`, `critical`, `exception`） |
| logger_name        | string        | 是   | 日志器名称（标准库 logging 特有）                                        |
| message            | string        | 是   | 日志消息内容                                                             |
| type               | string        | 是   | 消息类型（`string`, `fstring`, `format`, `percent`）                     |
| block              | string        | 是   | 代码块类型（`module`, `function`, `class`, `if`, `try`, `except`）       |
| args               | array[string] | 是   | 日志参数列表（变量名或表达式）                                           |
| sensitive_patterns | array[string] | 是   | 检测到的敏感信息模式列表                                                 |
| statement          | string        | 否   | 完整的日志调用语句                                                       |

## 示例

以下是扫描结果的示例：

```yaml
metadata:
  scanner_name: logging
  command_args:
    - upcast
    - scan-logging
    - ./app
    - --include
    - "app/**"
    - --format
    - yaml
summary:
  total_count: 8
  total_log_calls: 8
  files_scanned: 3
  scan_duration_ms: 142
  by_library:
    logging: 4
    loguru: 2
    structlog: 1
    django: 1
  by_level:
    debug: 1
    info: 4
    warning: 1
    error: 1
    exception: 1
  sensitive_calls: 2
results:
  app/services/user_service.py:
    - lineno: 12
      level: info
      library: logging
      logger_name: <__name__>
      message: "User created: %s"
      type: string
      block: function
      args:
        - user_id
      sensitive_patterns: []
      statement: logger.info("User created: %s", user_id)
    - lineno: 25
      level: warning
      library: logging
      logger_name: <__name__>
      message: "Login attempt with invalid token for {username}"
      type: fstring
      block: if
      args:
        - username
      sensitive_patterns:
        - token
      statement: logger.warning(f"Login attempt with invalid token for {username}")
    - lineno: 45
      level: debug
      library: logging
      logger_name: <__name__>
      message: "user.update() called with {}"
      type: format
      block: function
      args: []
      sensitive_patterns: []
      statement: logger.debug("user.update() called with {}".format(data))
    - lineno: 58
      level: info
      library: loguru
      logger_name: null
      message: "User {user_id} logged in successfully"
      type: fstring
      block: class
      args:
        - user_id
      sensitive_patterns: []
      statement: logger.info(f"User {user_id} logged in successfully")
  app/models/account.py:
    - lineno: 88
      level: error
      library: logging
      logger_name: root
      message: "Password reset failed: %s"
      type: string
      block: try
      args:
        - error_msg
      sensitive_patterns:
        - password
      statement: logger.error("Password reset failed: %s", error_msg)
    - lineno: 102
      level: exception
      library: logging
      logger_name: root
      message: "Database connection failed with api_key {key}"
      type: fstring
      block: except
      args:
        - key
      sensitive_patterns:
        - api_key
      statement: logger.exception(f"Database connection failed with api_key {key}")
  app/middleware/auth.py:
    - lineno: 15
      level: info
      library: logging
      logger_name: django.security
      message: "CSRF verification failed for {request.path}"
      type: fstring
      block: module
      args:
        - request.path
      sensitive_patterns: []
      statement: logger.info(f"CSRF verification failed for {request.path}")
```

## 注意事项

1. **支持的日志库**：

   - **标准库 logging** - `logger.info()`, `logger.debug()` 等
   - **loguru** - `logger.info()` (from loguru)
   - **structlog** - `logger.info()` (from structlog)

2. **日志级别**：

   - `debug` - 调试信息
   - `info` - 一般信息
   - `warning` - 警告信息
   - `error` - 错误信息
   - `critical` - 严重错误
   - `exception` - 异常信息（包含堆栈跟踪）

3. **消息类型**：

   - `string` - 普通字符串，使用 `%` 格式化：`logger.info("Value: %s", value)`
   - `fstring` - f-string 格式化字符串： `logger.info(f"Value: {value}")`
   - `format` - 使用 `.format()` 的字符串： `logger.info("Value: {}".format(value))`
   - `template` - 模板字符串： `logger.info("Value: {value}", value=value)`

4. **敏感信息检测**: 扫描器可通过 `--sensitive-keywords` 参数添加自定义模式，检测日志参数中的敏感信息

   - 密码相关：password, passwd, pwd
   - 认证相关：token, secret, key, api_key
   - 凭证相关：credential, auth

5. **代码块识别**：`block` 字段表示日志语句所在的代码块类型：

   - `module` - 模块级别
   - `function` - 函数内
   - `class` - 类方法内
   - `if` - if 语句块
   - `try` / `except` - 异常处理块

6. **日志器名称**：对于标准库 logging，记录日志器的名称，即 `logger = logging.getLogger(__name__)` 中的名称，如果无法变量使用尖括号包裹表示，如 `<__name__>`。

7. **参数提取** - `args` 字段列出推导出的日志消息的位置参数，`kwargs` 字段列出关键字参数及其推导值。
