# Django 设置扫描器 (django-settings)

## 概述

Django 设置扫描器用于分析 Django 项目中的配置设置（settings）的定义和使用情况。它能够追踪设置变量的定义位置、值类型、以及在代码中的所有使用位置。

该扫描器对于以下场景特别有用：

- 审查应用配置结构
- 识别未使用或过时的配置项
- 追踪配置在项目中的使用情况
- 生成配置文档
- 配置迁移和重构

## 命令用法

```bash
upcast scan-django-settings [OPTIONS] [PATH]
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
- `--settings-files TEXT` - Django 设置模块的文件名模式（可多次指定，默认：`**/settings*.py` 和 `**/settings/*.py`）

### 使用示例

```bash
# 扫描 Django 设置
upcast scan-django-settings .

# 保存结果到文件
upcast scan-django-settings . -o settings.yaml

# 输出为 JSON 格式
upcast scan-django-settings . --format json

# 启用详细模式
upcast scan-django-settings ./myproject --verbose
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

| 字段名            | 类型    | 必填 | 说明             |
| ----------------- | ------- | ---- | ---------------- |
| total_settings    | integer | 是   | 配置项总数       |
| total_definitions | integer | 是   | 配置定义总数     |
| total_usages      | integer | 是   | 配置使用总数     |
| files_scanned     | integer | 是   | 扫描的文件总数   |
| scan_duration_ms  | integer | 是   | 扫描耗时（毫秒） |
| total_count       | integer | 是   | 配置项总数       |

### results 字段

`results` 是一个字典，键为配置变量名，值为该配置的详细信息。

#### 配置对象（DjangoSetting）

| 字段名           | 类型              | 必填 | 说明                                           |
| ---------------- | ----------------- | ---- | ---------------------------------------------- |
| definition_count | integer           | 是   | 定义次数（通常为 1，多次定义可能表示配置覆盖） |
| definitions      | array[Definition] | 是   | 定义位置信息，键为文件路径，值为定义对象列表   |
| definition_types | array[string]     | 是   | 定义的值类型列表                               |
| usage_count      | integer           | 是   | 使用次数                                       |
| usages           | array[Usage]      | 是   | 使用位置信息，键为文件路径，值为使用对象列表   |

#### 配置定义对象（Definition）

| 字段名    | 类型    | 必填 | 说明                                                                   |
| --------- | ------- | ---- | ---------------------------------------------------------------------- |
| file      | string  | 是   | 定义所在文件路径                                                       |
| lineno    | integer | 是   | 定义所在行号                                                           |
| statement | string  | 是   | 定义语句的源代码                                                       |
| type      | string  | 是   | 值类型（`int`, `str`, `bool`, `list`, `dict`, `object`, `unknown` 等） |
| value     | any     | 是   | 配置的推导值（推导失败时为 `null`）                                    |

#### 配置使用对象（Usage）

| 字段名    | 类型    | 必填 | 说明             |
| --------- | ------- | ---- | ---------------- |
| file      | string  | 是   | 使用所在文件路径 |
| lineno    | integer | 是   | 使用所在行号     |
| statement | string  | 是   | 使用语句的源代码 |

## 示例

以下是扫描结果的示例：

```yaml
metadata:
  command_args:
    - .
    - --settings-files
    - "**/settings*.py"
  scanner_name: django-settings
summary:
  files_scanned: 42
  scan_duration_ms: 156
  total_count: 127
  total_definitions: 135
  total_settings: 127
  total_usages: 423
results:
  ACCESS_CONTROL_STRATEGY_DEFAULT_EXPIRES_DAYS:
    definition_count: 1
    definitions:
      - file: apiserver/paasng/paasng/settings/__init__.py
        lineno: 1232
        statement: ACCESS_CONTROL_STRATEGY_DEFAULT_EXPIRES_DAYS = 90
        type: int
        value: 90
    definition_types:
      - int
    usage_count: 0
    usages: []

  ADMIN_USERNAME:
    definition_count: 1
    definitions:
      - file: apiserver/paasng/paasng/settings/__init__.py
        lineno: 257
        statement: ADMIN_USERNAME = env.str('ADMIN_USERNAME', default='admin')
        type: str
        value: admin
    definition_types:
      - str
    usage_count: 4
    usages:
      - file: apiserver/paasng/paasng/infras/iam/client.py
        lineno: 189
        statement: usernames = [u for u in usernames if u != settings.ADMIN_USERNAME]
      - file: apiserver/paasng/paasng/infras/iam/client.py
        lineno: 341
        statement: usernames = [u for u in usernames if u != settings.ADMIN_USERNAME]
      - file: apiserver/paasng/paasng/infras/iam/helpers.py
        lineno: 96
        statement: "if username == settings.ADMIN_USERNAME:"
      - file: apiserver/paasng/paasng/infras/iam/helpers.py
        lineno: 112
        statement: "if username == settings.ADMIN_USERNAME:"

  ACCESS_CONTROL_CONFIG:
    definition_count: 1
    definitions:
      - file: apiserver/paasng/paasng/settings/__init__.py
        lineno: 1216
        statement: "ACCESS_CONTROL_CONFIG = env('ACCESS_CONTROL_CONFIG', default=get_default_access_control_config())"
        type: unknown
        value: null
    definition_types:
      - unknown
    usage_count: 0
    usages: []
```

## 注意事项

1. **定义识别逻辑**：对于所有匹配 settings-files 模式的文件，扫描并推导所有全大写的变量赋值

   - 直接赋值：`SETTING_NAME = value`
   - 通过 `locals()` 或 `globals()` 赋值: `locals()['SETTING_NAME'] = value` 或者 `locals().update({'SETTING_NAME': value})`，包括赋值的多种变体
   - 使用 django-environ 赋值的配置：`SETTING_NAME = env.str(...)`, `SETTING_NAME = env.int(...)` 等

2. **定义导入跟踪** ：如果存在以下导入语句，扫描器会追踪 `project.config.xxx` 中的设置定义，避免遗漏

   - `from project.config.xxx import MY_SETTING`
   - `import project.config.xxx import *`

3. **值类型**：`type_list` 包含该配置的所有可能类型

   - `unknown` 表示未知，在无法推导时使用
   - 根据 `definitions.type` 合并去重
   - 特殊的，如果存在一个具体的类型时，去掉 `unknown`
   - 当为空或者只有 `unknown` 时，最终结果为 `unknown`

4. **值类型推导**：扫描器会尝试静态推导配置的值

   - 支持基本类型（整数、字符串、布尔值、列表、字典等）
   - 对于复杂表达式或函数调用，可能无法推导，结果为 `unknown`
   - 使用 django-environ 时，使用访问方法获取类型，如 `env.str()`, `env.int()`, `env.bool()` 等

5. **使用追踪** - 扫描器追踪 `settings.SETTING_NAME` 形式的使用，可以识别：

   - 属性访问（大写），如 `settings.MY_SETTING` 和 `getattr(settings, 'MY_SETTING')`
   - 条件判断
   - 函数参数
   - 赋值语句右侧表达式
   - 注意：需要判断访问的属性来自于 `django.conf.settings`
