# 异常处理扫描器 (exception-handlers)

## 概述

异常处理扫描器用于分析 Python 代码中的异常处理模式。它能够检测 try-except-else-finally 块，统计异常类型、日志记录、控制流等信息。

该扫描器对于以下场景特别有用：

- 审查异常处理策略
- 识别静默异常（空 except 块）
- 检查错误日志完整性
- 分析异常传播路径
- 提高代码健壮性

## 命令使用

```bash
upcast scan-exception-handlers [OPTIONS] [PATH]
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

### 使用示例

```bash
# 扫描当前目录
upcast scan-exception-handlers .

# 保存结果到文件
upcast scan-exception-handlers ./src --output exceptions.yaml

# 输出为 JSON 格式
upcast scan-exception-handlers ./app --format json
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

| 字段名               | 类型    | 必填 | 说明             |
| -------------------- | ------- | ---- | ---------------- |
| total_handlers       | integer | 是   | 异常处理块总数   |
| total_except_clauses | integer | 是   | except 子句总数  |
| files_scanned        | integer | 是   | 扫描的文件总数   |
| scan_duration_ms     | integer | 是   | 扫描耗时（毫秒） |
| total_count          | integer | 是   | except 子句总数  |

### results 字段

`results` 是一个数组，每个元素是一个异常处理块对象。

#### 异常处理块对象（ExceptionHandler）

| 字段名            | 类型                  | 必填 | 说明                                      |
| ----------------- | --------------------- | ---- | ----------------------------------------- |
| file              | string                | 是   | 文件路径                                  |
| try_lineno        | integer               | 是   | try 语句起始行号                          |
| try_lines         | integer               | 是   | try 块的行数                              |
| else_lineno       | integer/null          | 是   | else 语句起始行号（不存在时为 `null`）    |
| else_lines        | integer/null          | 是   | else 块的行数（不存在时为 `null`）        |
| finally_lineno    | integer/null          | 是   | finally 语句起始行号（不存在时为 `null`） |
| finally_lines     | integer/null          | 是   | finally 块的行数（不存在时为 `null`）     |
| nested_exceptions | bool                  | 是   | 嵌套的异常处理块列表                      |
| exception_blocks  | array[ExceptionBlock] | 是   | except 子句列表                           |

#### 异常处理块对象（ExceptionBlock）

| 字段名              | 类型          | 必填 | 说明                   |
| ------------------- | ------------- | ---- | ---------------------- |
| lineno              | integer       | 是   | except 语句行号        |
| lines               | integer       | 是   | except 块的行数        |
| exceptions          | array[string] | 是   | 捕获的异常类型列表     |
| raise_count         | integer       | 是   | raise 语句数量         |
| return_count        | integer       | 是   | return 语句数量        |
| break_count         | integer       | 是   | break 语句数量         |
| continue_count      | integer       | 是   | continue 语句数量      |
| pass_count          | integer       | 是   | pass 语句数量          |
| log_debug_count     | integer       | 是   | debug 级别日志数量     |
| log_info_count      | integer       | 是   | info 级别日志数量      |
| log_warning_count   | integer       | 是   | warning 级别日志数量   |
| log_error_count     | integer       | 是   | error 级别日志数量     |
| log_critical_count  | integer       | 是   | critical 级别日志数量  |
| log_exception_count | integer       | 是   | exception 方法调用数量 |

## 示例

以下是扫描结果的示例：

```yaml
metadata: {}
results:
  # 示例 1: 只有 except 块，没有 else 和 finally
  - file: apiserver/paasng/manage.py
    try_lineno: 23
    try_lines: 2
    else_lineno: null
    else_lines: null
    finally_lineno: null
    finally_lines: null
    nested_exceptions: false
    exception_blocks:
      - lineno: 25
        lines: 13
        exceptions:
          - ImportError
        raise_count: 2
        return_count: 0
        break_count: 0
        continue_count: 0
        pass_count: 0
        log_debug_count: 0
        log_info_count: 0
        log_warning_count: 0
        log_error_count: 0
        log_critical_count: 0
        log_exception_count: 0

  # 示例 2: 包含 else 块和日志记录
  - file: apiserver/paasng/paas_wl/apis/admin/serializers/app.py
    try_lineno: 46
    try_lines: 2
    else_lineno: 50
    else_lines: 1
    finally_lineno: null
    finally_lines: null
    nested_exceptions: false
    exception_blocks:
      - lineno: 48
        lines: 2
        exceptions:
          - Exception
        raise_count: 0
        return_count: 0
        break_count: 0
        continue_count: 0
        pass_count: 0
        log_debug_count: 0
        log_info_count: 0
        log_warning_count: 0
        log_error_count: 1
        log_critical_count: 0
        log_exception_count: 0

  # 示例 3: 包含 finally 块和多个 except 子句
  - file: apiserver/paasng/paasng/core/region/manager.py
    try_lineno: 100
    try_lines: 5
    else_lineno: null
    else_lines: null
    finally_lineno: 112
    finally_lines: 2
    nested_exceptions: false
    exception_blocks:
      - lineno: 105
        lines: 3
        exceptions:
          - ValueError
          - TypeError
        raise_count: 0
        return_count: 1
        break_count: 0
        continue_count: 0
        pass_count: 0
        log_debug_count: 0
        log_info_count: 0
        log_warning_count: 1
        log_error_count: 0
        log_critical_count: 0
        log_exception_count: 0
      - lineno: 108
        lines: 4
        exceptions:
          - Exception
        raise_count: 0
        return_count: 0
        break_count: 0
        continue_count: 0
        pass_count: 0
        log_debug_count: 0
        log_info_count: 0
        log_warning_count: 0
        log_error_count: 0
        log_critical_count: 0
        log_exception_count: 1

  # 示例 4: 嵌套异常处理
  - file: apiserver/paasng/paasng/platform/applications/views.py
    try_lineno: 200
    try_lines: 10
    else_lineno: null
    else_lines: null
    finally_lineno: null
    finally_lines: null
    nested_exceptions: true
    exception_blocks:
      - lineno: 210
        lines: 8
        exceptions:
          - RequestException
        raise_count: 1
        return_count: 0
        break_count: 0
        continue_count: 0
        pass_count: 0
        log_debug_count: 0
        log_info_count: 0
        log_warning_count: 0
        log_error_count: 1
        log_critical_count: 0
        log_exception_count: 0
```

## 注意事项

1. **异常类型**：`exceptions` 列出捕获的异常类型：

   - 空列表表示裸 except（捕获所有异常，不推荐）
   - 具体类型如 `ImportError`, `ValueError` 等
   - 可以捕获多个类型：`except (ValueError, TypeError)`

2. **控制流统计**：统计 except 块中的控制流语句：

   - `raise_count` - 重新抛出异常的次数，包含 `raise` 和 `raise XXX from err`
   - `return_count` - 提前返回的次数
   - `break_count` / `continue_count` - 循环控制
   - `pass_count` - 静默处理（通常不推荐），指 `except` 块中只有 `pass` 或者 `...`，没有其他逻辑，等同于忽略异常

3. **日志统计**：各级别日志计数帮助评估错误可见性

   - `log_error_count` / `log_critical_count` - 应该记录严重错误
   - `log_exception_count` - `logger.exception()` 会记录完整堆栈
   - `log_warning_count` - 非严重但需要注意的情况
   - 识别的代码模式为 `*log*.<level>(...)`，其中 `<level>` 可以是 `debug`, `info`, `warning`, `error`, `critical`, `exception`

4. **嵌套异常处理**：扫描器会单独记录每个 try-except 块，并且会在父块中标记 `nested_exceptions: true`

   - 不区分嵌套层级，只要在块内有另一个 try-except 就视为嵌套
   - 不区分位置，包含 `try` 块、`except` 块、`else` 块、`finally` 块中的嵌套
