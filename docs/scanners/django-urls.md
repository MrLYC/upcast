# Django URL 路由扫描器 (django-urls)

## 概述

Django URL 路由扫描器用于分析 Django 项目中的 URL 配置。它能够检测 `path()`, `re_path()`, `include()` 以及 Django REST Framework 路由器注册，提取 URL 模式、视图、命名空间等信息。

该扫描器对于以下场景特别有用：

- 生成 API 路由文档
- 审查 URL 结构和命名规范
- 识别重复或冲突的路由
- 分析视图和 URL 的映射关系
- 项目路由重构规划

## 命令用法

```bash
upcast scan-django-urls [OPTIONS] [PATH]
```

### 参数

- `PATH` - 要扫描的 Python 文件或目录路径（可选，默认为当前目录 `.`）

### 选项

- `-o, --output PATH` - 输出文件路径（YAML 或 JSON）
- `--format [yaml|json|markdown]` - 输出格式（默认：yaml）
- `--markdown-language [en|zh]` - Markdown 输出语言（默认：zh）
- `--markdown-title TEXT` - Markdown 输出标题
- `-v, --verbose` - 启用详细日志
- `--include PATTERN` - 包含的文件模式（例如：`**/urls.py`）
- `--exclude PATTERN` - 排除的文件模式
- `--no-default-excludes` - 禁用默认排除模式

### 使用示例

```bash
# 扫描 Django URL 配置
upcast scan-django-urls ./myproject

# 扫描特定 urls.py 文件
upcast scan-django-urls myapp/urls.py

# 保存结果到 JSON 文件
upcast scan-django-urls ./myproject --output urls.json --format json

# 仅扫描 urls.py 文件
upcast scan-django-urls . --include "**/urls.py"
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
| total_patterns   | integer | 是   | URL 模式总数     |
| total_modules    | integer | 是   | URLconf 模块总数 |
| files_scanned    | integer | 是   | 扫描的文件总数   |
| scan_duration_ms | integer | 是   | 扫描耗时（毫秒） |
| total_count      | integer | 是   | URL 模式总数     |

### results 字段

`results` 是一个字典，键为 URLconf 模块路径（如 `apiserver.paasng.paas_wl.apis.admin.urls`），值为包含 `urlpatterns` 的对象。

#### URLconf 对象

| 字段名      | 类型              | 必填 | 说明         |
| ----------- | ----------------- | ---- | ------------ |
| urlpatterns | array[URLPattern] | 是   | URL 模式列表 |

#### URL 模式对象（URLPattern）

| 字段名         | 类型          | 必填 | 说明                                                |
| -------------- | ------------- | ---- | --------------------------------------------------- |
| type           | string        | 是   | URL 类型（`path`, `re_path`, `include`）            |
| pattern        | string        | 是   | URL 模式字符串                                      |
| view_name      | string        | 否   | 视图的模块路径（对于 `path` 和 `re_path`）          |
| name           | string        | 否   | URL 名称（用于反向解析）                            |
| include_module | string        | 否   | 包含的子 URLconf 模块（仅 `include` 类型）          |
| namespace      | string        | 否   | 命名空间（仅 `include` 类型）                       |
| vars           | array[string] | 否   | 变量列表（`path` 时为转换器，`re_path` 时为命名组） |
| block          | string        | 否   | 位于的代码块（如 `if` 语句块）                      |
| is_partial     | boolean       | 是   | 是否为部分路由（由其他路由包含）                    |
| router_type    | string        | 否   | 路由器类型（如 `DefaultRouter`，仅 DRF）            |
| basename       | string        | 否   | 基础名称（仅 DRF 路由器）                           |

## 示例

以下是扫描结果的示例：

```yaml
metadata:
  command_args:
    - ./myproject
    - --include
    - "**/urls.py"
  scanner_name: django-urls
summary:
  files_scanned: 28
  scan_duration_ms: 123
  total_count: 76
  total_modules: 12
  total_patterns: 76
results:
  apiserver.paasng.paas_wl.apis.admin.urls:
    urlpatterns:
      - basename: null
        block: null
        include_module: null
        is_partial: false
        name: null
        namespace: null
        pattern: wl_api/platform/process_spec_plan/manage/
        router_type: null
        type: path
        vars: []
        view_name: paas_wl.apis.admin.views.processes.ProcessSpecPlanManageViewSet

      - basename: null
        block: null
        include_module: null
        is_partial: false
        name: wl_api.process_spec_plan_by_id
        namespace: null
        pattern: wl_api/platform/process_spec_plan/id/<int:id>/
        router_type: null
        type: path
        vars:
          - id
        view_name: paas_wl.apis.admin.views.processes.ProcessSpecPlanManageViewSet

      - basename: null
        block: null
        include_module: null
        is_partial: false
        name: wl_api.process_by_name_version
        namespace: null
        pattern: wl_api/platform/process/(?P<process_name>\w+)/(?P<version>\d+)/
        router_type: null
        type: re_path
        vars:
          - process_name
          - version
        view_name: paas_wl.apis.admin.views.processes.ProcessDetailView

      - basename: null
        block: try
        include_module: paasng.infras.oauth2.urls
        is_partial: false
        name: null
        namespace: oauth2
        pattern: oauth2/
        router_type: null
        type: include
        vars: []
        view_name: null

      - basename: auditable_record
        block: null
        include_module: paasng.infras.audit.rest.urls
        is_partial: false
        name: null
        namespace: audit
        pattern: audit/
        router_type: SimpleRouter
        type: include
        vars: []
        view_name: null

  apiserver.paasng.paasng.settings.urls:
    urlpatterns:
      - basename: null
        block: if
        include_module: django.conf.urls.static
        is_partial: false
        name: null
        namespace: null
        pattern: /media/
        router_type: null
        type: include
        vars: []
        view_name: null
```

## 注意事项

1. **URL 类型** - 扫描器支持三种主要 URL 类型：

   - `path` - Django 2.0+ 的路径路由
   - `re_path` - 正则表达式路由
   - `include` - 包含其他 URLconf

2. **路径转换器** - `converters` 字段提取路径中的转换器，格式为 `name:type`，常见类型：

   - `int` - 整数
   - `str` - 字符串（默认）
   - `slug` - slug 字符串
   - `uuid` - UUID
   - `path` - 路径（包含斜杠）

3. **DRF 路由器** - 扫描器能够识别 Django REST Framework 的路由器注册：

   - `router.register()` 调用
   - `DefaultRouter`, `SimpleRouter` 等路由器类型
   - `basename` 参数

4. **命名空间** - `include()` 支持命名空间，用于避免 URL 名称冲突。

5. **URL 名称** - `name` 参数用于反向解析，应该在项目范围内唯一（考虑命名空间）。

6. **路径变量** - `vars` 字段包含路径中的变量，`path` 类型时为转换器（`id:int` 为 `id`），`re_path` 类型时为命名捕获组（`(?P<name>pattern)` 为 `name`）。

7. **路由嵌套** - 通过 `include()` 可以识别路由的嵌套结构，`include_module` 指向被包含的子 URLconf。

8. **代码块识别** - `block` 字段指示 URL 模式所在的代码块，有助于理解条件路由，取值为 `if`， `for`，`try`，`except`，`with`，`function`，`class` 等。
