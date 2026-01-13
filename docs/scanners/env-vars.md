# 环境变量扫描器 (env-vars)

## 概述

环境变量扫描器用于分析 Python 代码中的环境变量使用情况。它能够检测通过 `os.getenv()`, `os.environ.get()`, `os.environ[]` 等方式访问的环境变量，识别环境变量名称、默认值、是否必需，以及所有使用位置。

该扫描器对于以下场景特别有用：

- 审查应用程序的配置依赖
- 检查环境变量的一致性使用
- 识别缺少默认值的必需环境变量
- 生成环境变量配置文档

## 命令用法

```bash
upcast scan-env-vars [OPTIONS] [PATH]
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
upcast scan-env-vars .

# 扫描指定目录并输出到文件
upcast scan-env-vars ./src --output env-vars.yaml

# 以 JSON 格式输出
upcast scan-env-vars ./app --format json

# 启用详细模式
upcast scan-env-vars ./myproject --verbose
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

| 字段名           | 类型    | 必填 | 说明                                       |
| ---------------- | ------- | ---- | ------------------------------------------ |
| total_env_vars   | integer | 是   | 环境变量总数                               |
| required_count   | integer | 是   | 必需环境变量数量                           |
| optional_count   | integer | 是   | 可选环境变量数量                           |
| files_scanned    | integer | 是   | 扫描的文件总数                             |
| scan_duration_ms | integer | 是   | 扫描耗时（毫秒）                           |
| total_count      | integer | 是   | 环境变量总数（通常与 total_env_vars 相同） |

### results 字段

`results` 是一个字典，键为环境变量名称，值为该环境变量的详细信息（极端情况下键可能为空字符串）。

#### 环境变量对象（EnvVar）

| 字段名        | 类型            | 必填 | 说明                                                                                        |
| ------------- | --------------- | ---- | ------------------------------------------------------------------------------------------- |
| name          | string          | 是   | 代码的环境变量名称，如果无法推导成明确的值则跳过                                            |
| default_value | string/null     | 是   | 推导的默认值，如果未提供默认值则为 `null`                                                   |
| required      | boolean         | 是   | 是否必需，分析代码使用，如果不填会报错的话，就是必填                                        |
| types         | array[string]   | 是   | locations 提供的所有 type 集合（如 `string`, `int`, `bool` 等），如果无法推导则为 `unknown` |
| locations     | array[Location] | 是   | 环境变量使用位置列表                                                                        |

#### 位置对象（Location）

| 字段名    | 类型        | 必填 | 说明                                                                    |
| --------- | ----------- | ---- | ----------------------------------------------------------------------- |
| file      | string      | 是   | 文件路径（相对于扫描根目录）                                            |
| line      | integer     | 是   | 行号                                                                    |
| statement | string      | 是   | 代码片段（包含环境变量访问的完整表达式）                                |
| type      | string/null | 是   | 推导的类型（如 `string`, `int`, `bool` 等），如果无法推导则为 `unknown` |

## 示例

以下是扫描结果的示例：

```yaml
metadata:
  command_args:
    - ./src
  scanner_name: env-vars
summary:
  files_scanned: 42
  optional_count: 3
  required_count: 2
  scan_duration_ms: 89
  total_count: 5
  total_env_vars: 5
results:
  DATABASE_URL:
    default_value: null
    locations:
      - file: svc-bkrepo/svc_bk_repo/settings/__init__.py
        line: 140
        statement: os.getenv('DATABASE_URL')
        type: unknown
      - file: svc-mysql/svc_mysql/settings/__init__.py
        line: 139
        statement: os.getenv('DATABASE_URL')
        type: unknown
    name: DATABASE_URL
    required: true
    types:
      - unknown

  CELERY_TASK_DEFAULT_QUEUE:
    default_value: celery
    locations:
      - file: apiserver/paasng/paasng/settings/__init__.py
        line: 656
        statement: os.environ.get('CELERY_TASK_DEFAULT_QUEUE', 'celery')
        type: string
    name: CELERY_TASK_DEFAULT_QUEUE
    required: false
    types:
      - string

  BKPAAS_BUILD_VERSION:
    default_value: unset
    locations:
      - file: apiserver/paasng/paasng/plat_admin/admin42/context_processors.py
        line: 24
        statement: os.getenv('BKPAAS_BUILD_VERSION', 'unset')
        type: string
    name: BKPAAS_BUILD_VERSION
    required: false
    types:
      - string

  DEBUG:
    default_value: false
    locations:
      - file: apiserver/paasng/paasng/settings/__init__.py
        line: 45
        statement: env('DEBUG')
        type: bool
    name: DEBUG
    required: false
    types:
      - bool

  MAX_CONNECTIONS:
    default_value: null
    locations:
      - file: apiserver/paasng/paasng/settings/database.py
        line: 78
        statement: int(os.getenv('MAX_CONNECTIONS'))
        type: int
      - file: apiserver/paasng/paasng/settings/cache.py
        line: 34
        statement: env.int('MAX_CONNECTIONS', default=100)
        type: int
    name: MAX_CONNECTIONS
    required: true
    types:
      - int
```

## 注意事项

1. **支持的访问模式**：支持多种环境变量访问模式，会确认引用的模块来避免同名导致的误判：

   - `os.getenv(name, default)`
   - `os.environ.get(name, default)`
   - `os.environ[name]`
   - `os.environ.setdefault(name, default)`
   - django-environ 的访问模式，如 `env = environ.Env(DEBUG=(bool, False))`，`env.str(name, default)`， `env.int(name, default=xxx)`，`env("DEBUG")` 等

2. **默认值与必需**：会根据代码逻辑推导默认值，无法推导时为 `null`。

   - `os.getenv('VAR', 'default')` 推导为 `'default'`
   - `os.environ.get('VAR', 42)` 推导为 `42`
   - `os.environ.get('VAR') or 'Value'` 推导为 `Value`
   - `os.environ['VAR']` 推导为 `null`（无默认值，且因为访问会报错，标记为必需）
   - `env = environ.Env(DEBUG=(bool, False))` 中的 `DEBUG` 推导为 `false`
   - `env.str('VAR', default='value')` 推导为 `'value'`
   - `env.int('VAR')` 推导为 `null`（无默认值，标记为必需）

3. **类型推导**：扫描器会尝试静态推导环境变量的类型，支持基本类型（字符串、整数、布尔值等），优先使用明确的类型转换，如果没有的话，基于默认值推导。如果 locations 有一个具体值，则 types 中只保留具体类型，去掉 `unknown`。
   - `os.getenv('VAR', '42')` 推导为 `string`

- `int(os.getenv('VAR', '42'))` 推导为 `int`
- `env = environ.Env(DEBUG=(bool, False))` 中的 `DEBUG` 推导为 `bool`
- `env.str('VAR')` 推导为 `string`

4. **结果聚合**：所有使用同一环境变量的位置会被聚合在一起，方便查看某个环境变量在整个项目中的使用情况。
