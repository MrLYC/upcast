# Django 模型扫描器 (django-models)

## 概述

Django 模型扫描器用于分析 Django 项目中的模型定义。它能够提取模型类、字段、关系、Meta 配置等信息，为项目的数据模型提供全面的文档和分析。

该扫描器对于以下场景特别有用：

- 生成数据模型文档
- 分析数据库表结构
- 识别模型间的关系（外键、多对多等）
- 审查模型字段配置
- 项目迁移和重构规划

## 命令用法

```bash
upcast scan-django-models [OPTIONS] [PATH]
```

### 参数

- `PATH` - 要扫描的 Python 文件或目录路径（可选，默认为当前目录 `.`）

### 选项

- `-o, --output PATH` - 输出文件路径（YAML 或 JSON）
- `--format [yaml|json|markdown]` - 输出格式（默认：yaml）
- `--markdown-language [en|zh]` - Markdown 输出语言（默认：zh）
- `--markdown-title TEXT` - Markdown 输出标题
- `-v, --verbose` - 启用详细日志
- `--include PATTERN` - 包含的文件模式（例如：`**/models.py`）
- `--exclude PATTERN` - 排除的文件模式
- `--no-default-excludes` - 禁用默认排除模式

### 使用示例

```bash
# 扫描 Django 模型
upcast scan-django-models ./myproject

# 扫描特定 models.py 文件
upcast scan-django-models myapp/models.py

# 保存结果到 JSON 文件
upcast scan-django-models ./myproject --output models.json --format json

# 仅扫描特定应用的模型
upcast scan-django-models . --include "myapp/**/models.py"
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

| 字段名              | 类型    | 必填 | 说明             |
| ------------------- | ------- | ---- | ---------------- |
| total_models        | integer | 是   | 模型总数         |
| total_fields        | integer | 是   | 字段总数         |
| total_relationships | integer | 是   | 关系总数         |
| files_scanned       | integer | 是   | 扫描的文件总数   |
| scan_duration_ms    | integer | 是   | 扫描耗时（毫秒） |
| total_count         | integer | 是   | 模型总数         |

### results 字段

`results` 是一个字典，键为模型的完全限定名（格式：`module.path.ModelName`），值为模型详细信息对象。

#### 推导对象（InferredValue）

| 字段名    | 类型     | 必填 | 说明                                                             |
| --------- | -------- | ---- | ---------------------------------------------------------------- |
| value     | any/null | 是   | 推导值（使用代码推导并尽可能解析为可读格式，如果解析失败则为空） |
| statement | string   | 是   | 代码语句                                                         |

#### 模型对象（DjangoModel）

| 字段名        | 类型                           | 必填 | 说明                                               |
| ------------- | ------------------------------ | ---- | -------------------------------------------------- |
| name          | string                         | 是   | 模型类名                                           |
| module        | string                         | 是   | 模型所在模块路径                                   |
| line          | integer                        | 是   | 模型定义的起始行号                                 |
| description   | string/null                    | 是   | 模型描述（来自 docstring；无 docstring 为 `null`） |
| bases         | array[string]                  | 是   | 模型继承的基类列表                                 |
| fields        | map[string, DjangoModelField]  | 是   | 模型字段定义，键为字段名，值为字段对象             |
| relationships | array[DjangoModelRelationship] | 是   | 模型关系列表（外键、多对多等）                     |
| meta          | DjangoModelMeta                | 否   | Meta 类配置信息                                    |
| objects       | InferredValue/null             | 否   | 自定义管理器（如果有），value 为类型的完全限定名称 |

#### 字段对象（DjangoModelField）

| 字段名       | 类型                               | 必填 | 说明                                                                         |
| ------------ | ---------------------------------- | ---- | ---------------------------------------------------------------------------- |
| name         | string                             | 是   | 字段名称                                                                     |
| type         | string                             | 是   | 字段类型（例如：`models.CharField`, `models.ForeignKey`）                    |
| line         | integer                            | 是   | 字段定义行号                                                                 |
| parameters   | map[string/integer, InferredValue] | 是   | 字段参数（max_length, default, validators 等），如果是位置参数则键为位置序号 |
| verbose_name | string/null                        | 是   | 字段的可读名称                                                               |
| help_text    | string/null                        | 是   | 字段帮助文本                                                                 |

#### 关系对象（DjangoModelRelationship）

关系字段（ForeignKey, ManyToManyField, OneToOneField）的详细信息。

| 字段名       | 类型        | 必填 | 说明                                                         |
| ------------ | ----------- | ---- | ------------------------------------------------------------ |
| field        | string      | 是   | 关系字段名称                                                 |
| type         | string      | 是   | 字段类型（如 `models.ForeignKey`, `models.OneToOneField`）   |
| to           | string      | 是   | 关联的模型名称（类名）                                       |
| related_name | string/null | 是   | related_name（未设置时为 `null`）                            |
| on_delete    | string/null | 是   | 删除行为（仅 ForeignKey/OneToOneField；未解析到时为 `null`） |

#### 元数据（DjangoModelMeta）

Meta 类中定义的模型元数据，每个字段都是 InferredValue 类型，包括但不限于以下字段（按实际定义提取）：

| 字段名              | 类型          | 说明                   |
| ------------------- | ------------- | ---------------------- |
| unique_together     | InferredValue | 联合唯一约束字段组合   |
| ordering            | InferredValue | 默认排序字段           |
| db_table            | InferredValue | 数据库表名             |
| verbose_name        | InferredValue | 模型的可读名称         |
| verbose_name_plural | InferredValue | 模型复数形式的可读名称 |
| indexes             | InferredValue | 索引定义               |
| constraints         | InferredValue | 约束定义               |
| abstract            | InferredValue | 是否为抽象模型         |
| managed             | InferredValue | 是否由 Django 管理     |
| app_label           | InferredValue | 模型所属应用标签       |

## 示例

以下是扫描结果的示例：

```yaml
metadata:
  command_args:
    - ./myproject
    - --include
    - "**/models.py"
  scanner_name: django-models
summary:
  files_scanned: 15
  scan_duration_ms: 245
  total_count: 12
  total_fields: 89
  total_models: 12
  total_relationships: 18
results:
  apiserver.paasng.paas_wl.bk_app.applications.models.app.App:
    bases:
      - paas_wl.bk_app.applications.models.UuidAuditedModel
    description: App Model
    fields:
      name:
        help_text: null
        line: 23
        name: name
        parameters:
          max_length:
            statement: max_length=64
            value: 64
          validators:
            statement: validators=[validate_app_name]
            value: null
        type: models.SlugField
        verbose_name: null
      owner:
        help_text: null
        line: 24
        name: owner
        parameters:
          max_length:
            statement: max_length=64
            value: 64
        type: models.CharField
        verbose_name: null
      region:
        help_text: null
        line: 25
        name: region
        parameters:
          max_length:
            statement: max_length=32
            value: 32
        type: models.CharField
        verbose_name: null
      type:
        help_text: null
        line: 26
        name: type
        parameters:
          db_index:
            statement: db_index=True
            value: true
          default:
            statement: default=WlAppType.DEFAULT.value
            value: null
          max_length:
            statement: max_length=16
            value: 16
        type: models.CharField
        verbose_name: 应用类型
      user:
        help_text: 关联的用户
        line: 27
        name: user
        parameters:
          "0":
            statement: User
            value: User
          on_delete:
            statement: on_delete=models.CASCADE
            value: models.CASCADE
          related_name:
            statement: related_name="apps"
            value: apps
        type: models.ForeignKey
        verbose_name: 用户
      tags:
        help_text: null
        line: 28
        name: tags
        parameters:
          "0":
            statement: Tag
            value: Tag
          related_name:
            statement: related_name="apps"
            value: apps
        type: models.ManyToManyField
        verbose_name: 标签
    line: 20
    meta:
      db_table:
        statement: db_table = "wl_apps"
        value: wl_apps
      ordering:
        statement: ordering = ["-created"]
        value:
          - -created
      unique_together:
        statement: unique_together = (("region", "name"),)
        value:
          - - region
            - name
      verbose_name:
        statement: verbose_name = "应用"
        value: 应用
      verbose_name_plural:
        statement: verbose_name_plural = "应用"
        value: 应用
      indexes:
        statement: indexes = [models.Index(fields=["region", "type"])]
        value: null
    module: apiserver.paasng.paas_wl.bk_app.applications.models.app
    name: App
    objects: null
    relationships:
      - field: user
        on_delete: models.CASCADE
        related_name: apps
        to: User
        type: models.ForeignKey
      - field: tags
        on_delete: null
        related_name: apps
        to: Tag
        type: models.ManyToManyField
```

## 注意事项

1. **如何识别模型** - 继承自 `django.db.models.Model` 或者使用了 Django 字段（如 `models.CharField`）进行属性声明的类都会被识别为模型。

2. **完全限定名** - 模型以完全限定名作为键，格式为 `module.path.ClassName`，确保唯一性。

3. **字段参数** - 字段的所有参数都会被捕获，包括 `max_length`, `default`, `validators`, `choices` 等，参数值会使用代码推导并尽可能解析为可读格式。

4. **关系识别** - 扫描器能够识别以下关系类型：

   - `ForeignKey` - 外键关系
   - `ManyToManyField` - 多对多关系
   - `OneToOneField` - 一对一关系

5. **继承信息** - `bases` 字段列出模型继承的所有基类，包括 Django 内置基类和自定义基类。

6. **Meta 配置** - Meta 类中的所有配置都会被提取，包括索引、约束、排序等。

7. **Docstring 提取** - 模型类的 docstring 会被提取为 `description` 字段，用于文档生成。
